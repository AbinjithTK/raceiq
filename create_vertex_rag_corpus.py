"""
Create Vertex AI RAG Corpus for RaceIQ
Uploads RAG dataset to Google Cloud Storage for Vertex AI Search
"""

import json
import os
from google.cloud import storage

# Configuration
PROJECT_ID = "hackthetrack-479019"
BUCKET_NAME = "raceiq-data-bucket"
RAG_DATASET_PATH = "rag_dataset/race_engineer_enhanced.jsonl"
CORPUS_FOLDER = "vertex_rag_corpus"

def prepare_rag_documents():
    """Prepare RAG documents in format suitable for Vertex AI"""
    
    print(f"📖 Reading RAG dataset from {RAG_DATASET_PATH}")
    
    documents = []
    with open(RAG_DATASET_PATH, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            try:
                entry = json.loads(line)
                
                # Create document in Vertex AI format
                doc = {
                    'id': entry['id'],
                    'structData': {
                        'question': entry['question'],
                        'answer': entry['answer'],
                        'category': entry['context'].get('category', 'general'),
                        'track': entry['context'].get('track', 'all'),
                        'difficulty': entry['context'].get('difficulty', 'intermediate')
                    },
                    'content': {
                        'mimeType': 'text/plain',
                        'rawBytes': f"{entry['question']}\n\n{entry['answer']}".encode('utf-8').hex()
                    }
                }
                
                documents.append(doc)
                
                if line_num % 20 == 0:
                    print(f"   Processed {line_num} entries...")
                    
            except json.JSONDecodeError as e:
                print(f"⚠️  Skipping line {line_num}: {e}")
    
    print(f"✅ Prepared {len(documents)} documents")
    return documents


def upload_to_gcs(documents):
    """Upload documents to Google Cloud Storage"""
    
    print(f"\n📤 Uploading to gs://{BUCKET_NAME}/{CORPUS_FOLDER}/")
    
    try:
        storage_client = storage.Client(project=PROJECT_ID)
        bucket = storage_client.bucket(BUCKET_NAME)
        
        # Upload as individual JSON files (better for Vertex AI Search)
        for i, doc in enumerate(documents):
            blob_name = f"{CORPUS_FOLDER}/doc_{doc['id']}.json"
            blob = bucket.blob(blob_name)
            
            # Create simplified document
            simple_doc = {
                'id': doc['id'],
                'title': doc['structData']['question'][:100],
                'content': f"{doc['structData']['question']}\n\n{doc['structData']['answer']}",
                'category': doc['structData']['category'],
                'track': doc['structData']['track']
            }
            
            blob.upload_from_string(
                json.dumps(simple_doc, indent=2),
                content_type='application/json'
            )
            
            if (i + 1) % 20 == 0:
                print(f"   Uploaded {i + 1}/{len(documents)} documents...")
        
        print(f"✅ Successfully uploaded {len(documents)} documents to GCS!")
        
        # Also create a single JSONL file for easy import
        jsonl_blob = bucket.blob(f"{CORPUS_FOLDER}/all_documents.jsonl")
        jsonl_content = '\n'.join([json.dumps({
            'id': doc['id'],
            'content': f"{doc['structData']['question']}\n\n{doc['structData']['answer']}",
            'metadata': {
                'category': doc['structData']['category'],
                'track': doc['structData']['track']
            }
        }) for doc in documents])
        
        jsonl_blob.upload_from_string(jsonl_content, content_type='application/x-ndjson')
        print(f"✅ Created combined JSONL file: gs://{BUCKET_NAME}/{CORPUS_FOLDER}/all_documents.jsonl")
        
        return True
        
    except Exception as e:
        print(f"❌ Error uploading to GCS: {e}")
        import traceback
        traceback.print_exc()
        return False


def create_vertex_search_instructions():
    """Print instructions for creating Vertex AI Search"""
    
    print("\n" + "=" * 70)
    print("📋 Next Steps: Create Vertex AI Search Data Store")
    print("=" * 70)
    print("""
To complete the RAG setup in Vertex AI:

1. Go to Vertex AI Search in Google Cloud Console:
   https://console.cloud.google.com/gen-app-builder/engines

2. Click "Create App" or "Create Data Store"

3. Choose "Search" as the app type

4. Configure the data store:
   - Name: raceiq-race-engineer-knowledge
   - Data source: Cloud Storage
   - Location: gs://raceiq-data-bucket/vertex_rag_corpus/
   - Import type: JSONL (use all_documents.jsonl)

5. Enable "Advanced LLM features" for RAG capabilities

6. Once created, you can use the data store ID in your API calls

Alternative: Use Vertex AI Agent Builder
   https://console.cloud.google.com/gen-app-builder/agents

Your RAG corpus is ready at:
   gs://raceiq-data-bucket/vertex_rag_corpus/

Total documents: {doc_count}
""")


def main():
    """Main execution"""
    
    print("=" * 70)
    print("🏁 RaceIQ - Vertex AI RAG Corpus Setup")
    print("=" * 70)
    
    # Check if dataset exists
    if not os.path.exists(RAG_DATASET_PATH):
        print(f"❌ RAG dataset not found at {RAG_DATASET_PATH}")
        return
    
    # Prepare documents
    documents = prepare_rag_documents()
    
    if not documents:
        print("❌ No documents to upload")
        return
    
    # Upload to GCS
    success = upload_to_gcs(documents)
    
    if success:
        print("\n" + "=" * 70)
        print("✅ RAG Corpus Upload Complete!")
        print("=" * 70)
        
        # Print next steps
        create_vertex_search_instructions()
        
        print(f"\n📊 Summary:")
        print(f"   - Documents uploaded: {len(documents)}")
        print(f"   - GCS location: gs://{BUCKET_NAME}/{CORPUS_FOLDER}/")
        print(f"   - Ready for Vertex AI Search integration")
    else:
        print("\n❌ Failed to upload corpus")


if __name__ == "__main__":
    main()
