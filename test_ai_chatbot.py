"""Test the AI Race Engineer chatbot endpoint"""
import requests
import json

API_URL = "http://localhost:8000/ai/query"

# Test queries
test_queries = [
    "Tell me about Barber Motorsports Park",
    "What's the best pit strategy?",
    "Where am I losing time?",
    "When should I pit?",
    "What were the weather conditions at Indianapolis?",
    "How many cars competed at Barber Race 1?",
    "What's the optimal tire strategy?",
]

print("🤖 Testing AI Race Engineer Chatbot\n")
print("=" * 60)

for query in test_queries:
    print(f"\n❓ Query: {query}")
    
    try:
        response = requests.post(API_URL, json={
            "query": query,
            "context": {
                "track": "barber",
                "lap": 15,
                "sector": 2
            }
        })
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Response: {data['response']}")
            print(f"   Type: {data['type']} | Confidence: {data['confidence']:.0%}")
            print(f"   Sources: {len(data['sources'])} knowledge entries")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

print("\n" + "=" * 60)
print("✅ Test complete!")
