import os
import json
import hashlib
from google.cloud import bigquery
import vertexai
from vertexai.generative_models import GenerativeModel, GenerationConfig

# --- Configuration & Client Initialization ---
PROJECT_ID = os.environ.get('PROJECT_ID', 'project-305165e7-efbc-4317-a56')
LOCATION = "us-central1"
DATASET_ID = "research"
TABLE_ID = f"{PROJECT_ID}.{DATASET_ID}.scored_signals"

# Clients
bq_client = bigquery.Client(project=PROJECT_ID)

# Vertex SDK
vertexai.init(project=PROJECT_ID, location=LOCATION)
model = GenerativeModel("gemini-1.5-flash-001")

def score_with_vertex_sdk(item_data):
    """Enriches data via Vertex SDK."""
    prompt = f"""Analyze this AI research signal: {json.dumps(item_data)}
    Output ONLY valid JSON: {{"relevance_score": int, "technical_significance": "string", "pii_detected": bool, "tags": ["string"], "executive_summary": "string"}}"""
    
    generation_config = GenerationConfig(response_mime_type="application/json", temperature=0.1)
    
    try:
        response = model.generate_content(prompt, generation_config=generation_config)
        return json.loads(response.text.strip())
    except:
        return {"relevance_score": 50, "technical_significance": "N/A", "pii_detected": False, "tags": [], "executive_summary": "N/A"}

def ingest_json_file(file_path, source_name):
    """Manually ingests a local JSON file into BigQuery."""
    print(f"📥 Ingesting {file_path} into {TABLE_ID}...")
    with open(file_path, 'r') as f:
        items = json.load(f)
    
    scored_rows = []
    for item in items:
        title = item.get('title') or item.get('headline') or item.get('name') or "Unknown Signal"
        source_url = item.get('url') or item.get('link') or "#"
        summary = item.get('summary') or item.get('text') or item.get('body') or ""
        
        analysis = score_with_vertex_sdk({"title": title, "summary": summary})
        
        row = {
            "signal_id": hashlib.md5(source_url.encode()).hexdigest(),
            "source": source_name,
            "title": title,
            "relevance_score": analysis['relevance_score'],
            "technical_significance": analysis['technical_significance'],
            "pii_detected": analysis['pii_detected'],
            "tags": analysis['tags'],
            "executive_summary": analysis['executive_summary'],
            "url": source_url
            # ingested_at handled by default value in BQ
        }
        scored_rows.append(row)

    if scored_rows:
        errors = bq_client.insert_rows_json(TABLE_ID, scored_rows)
        if not errors:
            print(f"✅ Successfully ingested {len(scored_rows)} rows.")
        else:
            print(f"❌ BQ Errors: {errors}")

if __name__ == "__main__":
    # Ingest Sample Data
    linkedin_file = "personal-ai-research-kit/data/linkedin/linkedin_research_1778531575.json"
    reddit_file = "personal-ai-research-kit/data/reddit/reddit_search_1778530686.json"
    
    if os.path.exists(linkedin_file):
        ingest_json_file(linkedin_file, "LinkedIn")
    if os.path.exists(reddit_file):
        ingest_json_file(reddit_file, "Reddit")
