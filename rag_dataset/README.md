# RAG Dataset - Toyota GR Cup Race Engineering

## Overview

This folder contains clean, structured data for training AI race engineering assistants using RAG (Retrieval-Augmented Generation) or fine-tuning approaches.

## Dataset Files

### Core Datasets
- `race_engineer_qa.jsonl` - Question-answer pairs (JSONL format for training)
- `race_engineer_qa.json` - Same data in readable JSON format
- `track_knowledge.json` - Track-specific information
- `telemetry_insights.json` - Telemetry parameter explanations
- `strategy_playbook.json` - Race strategy scenarios
- `driver_coaching.json` - Coaching tips and techniques

### Metadata
- `dataset_stats.json` - Statistics about the dataset
- `README.md` - This file

## Data Structure

Each entry follows this format:

```json
{
  "id": "unique_identifier",
  "question": "User question or query",
  "answer": "Detailed, actionable answer",
  "context": {
    "category": "track_info|strategy|telemetry|coaching",
    "track": "barber|cota|etc",
    "difficulty": "beginner|intermediate|advanced",
    "data_source": "telemetry|results|analysis"
  },
  "metadata": {
    "source": "toyota_gr_cup_2025",
    "domain": "motorsports_race_engineering",
    "verified": true
  }
}
```

## Categories

1. **Track Information** - Circuit characteristics, layout, difficulty
2. **Telemetry Analysis** - Parameter interpretation, data analysis
3. **Race Strategy** - Pit stops, tire management, fuel strategy
4. **Driver Coaching** - Technique improvement, racing line, braking
5. **Performance Analysis** - Lap times, sectors, consistency
6. **Weather & Conditions** - Temperature, wet conditions, grip
7. **Vehicle Dynamics** - Setup, balance, handling
8. **Championship** - Points, standings, season strategy

## Usage

### For Fine-Tuning
```python
import json

with open('rag_dataset/race_engineer_qa.jsonl', 'r') as f:
    for line in f:
        entry = json.loads(line)
        # Use for training
```

### For RAG (Vector Database)
```python
from chromadb import Client

client = Client()
collection = client.create_collection("race_engineer")

with open('rag_dataset/race_engineer_qa.json', 'r') as f:
    data = json.load(f)
    for entry in data:
        collection.add(
            documents=[entry['answer']],
            metadatas=[entry['context']],
            ids=[entry['id']]
        )
```

## Data Quality

- ✅ All data verified against source telemetry
- ✅ Technical accuracy reviewed
- ✅ Actionable insights provided
- ✅ Clear, concise language
- ✅ Appropriate difficulty levels

## Statistics

- Total entries: 100+
- Categories: 8
- Tracks covered: 7
- Difficulty levels: 3
- Data sources: 4

## Updates

Dataset is expandable. To add more data:
```bash
python src/rag_data_generator.py --expand
```

## License

Data derived from Toyota GR Cup telemetry for educational and training purposes.
