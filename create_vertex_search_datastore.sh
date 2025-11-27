#!/bin/bash

# Create Vertex AI Search Data Store for RaceIQ
# This script creates a search data store and imports the RAG corpus

PROJECT_ID="hackthetrack-479019"
LOCATION="global"
DATA_STORE_ID="raceiq-race-engineer-knowledge"
DATA_STORE_NAME="RaceIQ Race Engineer Knowledge Base"
GCS_URI="gs://raceiq-data-bucket/vertex_rag_corpus/all_documents.jsonl"

echo "======================================================================"
echo "Creating Vertex AI Search Data Store"
echo "======================================================================"

# Create the data store
echo "Creating data store: $DATA_STORE_ID"
gcloud alpha discovery-engine data-stores create \
  --data-store-id="$DATA_STORE_ID" \
  --display-name="$DATA_STORE_NAME" \
  --industry-vertical=GENERIC \
  --solution-types=SOLUTION_TYPE_SEARCH \
  --content-config=CONTENT_REQUIRED \
  --location="$LOCATION" \
  --project="$PROJECT_ID"

echo ""
echo "Data store created successfully!"
echo ""

# Import documents
echo "Importing documents from $GCS_URI"
gcloud alpha discovery-engine documents import \
  --data-store="$DATA_STORE_ID" \
  --location="$LOCATION" \
  --project="$PROJECT_ID" \
  --gcs-uri="$GCS_URI" \
  --reconciliation-mode=INCREMENTAL

echo ""
echo "======================================================================"
echo "✅ Vertex AI Search Data Store Setup Complete!"
echo "======================================================================"
echo ""
echo "Data Store ID: $DATA_STORE_ID"
echo "Location: $LOCATION"
echo "Documents: 128 race engineering Q&A pairs"
echo ""
echo "You can now use this data store for RAG-powered search!"
echo ""
