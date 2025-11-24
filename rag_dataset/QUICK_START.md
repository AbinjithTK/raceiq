# Quick Start - Toyota GR Cup RAG Dataset

## 🚀 Get Started in 60 Seconds

### Load the Dataset

```python
import json

# For training (JSONL format)
with open('race_engineer_complete.jsonl', 'r') as f:
    training_data = [json.loads(line) for line in f]

# For review (JSON format)
with open('race_engineer_complete.json', 'r') as f:
    dataset = json.load(f)

print(f"Loaded {len(dataset)} entries")
```

### Basic Usage

```python
# Get a sample entry
entry = dataset[0]

print(f"Question: {entry['question']}")
print(f"Answer: {entry['answer']}")
print(f"Category: {entry['context']['category']}")
print(f"Track: {entry['context']['track']}")
print(f"Difficulty: {entry['context']['difficulty']}")
```

### Filter by Category

```python
# Get all strategy entries
strategy = [e for e in dataset if e['context']['category'] == 'strategy']
print(f"Found {len(strategy)} strategy entries")
```

### Filter by Track

```python
# Get all Barber entries
barber = [e for e in dataset if e['context']['track'] == 'barber']
print(f"Found {len(barber)} Barber entries")
```

### Filter by Difficulty

```python
# Get beginner-level entries
beginner = [e for e in dataset if e['context']['difficulty'] == 'beginner']
print(f"Found {len(beginner)} beginner entries")
```

## 📊 Dataset Stats

```
Total Entries:    98
Tracks:           7 (Barber, Indianapolis, COTA, Sebring, Road America, Sonoma, VIR)
Races:            14
Categories:       9 (race_results, weather, track_info, lap_times, strategy, telemetry, coaching, vehicle_dynamics, championship)
Difficulty:       Beginner (33), Intermediate (47), Advanced (18)
```

## 📁 Available Files

### Main Files
- `race_engineer_complete.jsonl` - Training format
- `race_engineer_complete.json` - Readable format

### By Category
- `race_results_complete.json` (26 entries)
- `weather_complete.json` (15 entries)
- `track_info_complete.json` (14 entries)
- `lap_times_complete.json` (14 entries)
- `strategy_complete.json` (11 entries)
- `telemetry_complete.json` (6 entries)
- `coaching_complete.json` (5 entries)
- `vehicle_dynamics_complete.json` (4 entries)
- `championship_complete.json` (3 entries)

### By Track
- `track_barber.json` (11 entries)
- `track_indianapolis.json` (11 entries)
- `track_sebring.json` (11 entries)
- `track_road_america.json` (11 entries)
- `track_vir.json` (11 entries)
- `track_cota.json` (10 entries)
- `track_sonoma.json` (8 entries)

## 🎯 Common Use Cases

### 1. Fine-Tune LLM
```python
# Prepare for OpenAI fine-tuning
training_examples = []
for entry in training_data:
    training_examples.append({
        "messages": [
            {"role": "user", "content": entry['question']},
            {"role": "assistant", "content": entry['answer']}
        ]
    })
```

### 2. Create Embeddings
```python
from openai import OpenAI
client = OpenAI()

for entry in dataset:
    text = f"Q: {entry['question']}\nA: {entry['answer']}"
    embedding = client.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )
    # Store in vector DB
```

### 3. Build RAG System
```python
# Simple retrieval example
def find_relevant(query, dataset, top_k=3):
    # In production, use vector similarity
    # This is a simple keyword match example
    results = []
    for entry in dataset:
        if query.lower() in entry['question'].lower():
            results.append(entry)
    return results[:top_k]

# Query the dataset
results = find_relevant("strategy", dataset)
for r in results:
    print(f"Q: {r['question']}")
    print(f"A: {r['answer'][:100]}...\n")
```

## 📖 Entry Structure

```json
{
  "id": "rag_0001",
  "question": "Tell me about Barber Motorsports Park",
  "answer": "Barber Motorsports Park is a 3.7km circuit...",
  "context": {
    "category": "track_info",
    "subcategory": "overview",
    "track": "barber",
    "race": null,
    "difficulty": "beginner",
    "data_source": "track_config"
  },
  "metadata": {
    "source": "toyota_gr_cup_2025",
    "domain": "motorsports_race_engineering",
    "verified": true,
    "created": "2025-11-23T..."
  }
}
```

## ✅ You're Ready!

The dataset is production-ready. Start building your AI race engineer! 🏁

For more details, see `COMPLETE_DATASET_README.md`
