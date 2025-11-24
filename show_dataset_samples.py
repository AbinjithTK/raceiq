"""Show sample entries from the complete RAG dataset"""
import json

# Load the complete dataset
with open('rag_dataset/race_engineer_complete.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Group by category
categories = {}
for entry in data:
    cat = entry['context']['category']
    if cat not in categories:
        categories[cat] = []
    categories[cat].append(entry)

print("=" * 80)
print("COMPLETE RAG DATASET - SAMPLE ENTRIES")
print("=" * 80)
print(f"\nTotal Entries: {len(data)}")
print(f"Categories: {len(categories)}")
print()

# Show samples from each category
for cat, entries in sorted(categories.items()):
    print(f"\n{'='*80}")
    print(f"📁 {cat.upper().replace('_', ' ')} ({len(entries)} entries)")
    print('='*80)
    
    # Show first entry
    sample = entries[0]
    print(f"\n❓ Question: {sample['question']}")
    print(f"\n💡 Answer: {sample['answer'][:200]}...")
    print(f"\n📊 Context:")
    print(f"   - Track: {sample['context'].get('track', 'N/A')}")
    print(f"   - Race: {sample['context'].get('race', 'N/A')}")
    print(f"   - Difficulty: {sample['context']['difficulty']}")
    print(f"   - Source: {sample['context']['data_source']}")

print("\n" + "="*80)
print("✅ Dataset ready for AI training!")
print("="*80)
