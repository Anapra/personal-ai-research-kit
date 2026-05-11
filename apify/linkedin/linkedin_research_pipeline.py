import requests
import json
import os
import sys
import time
import subprocess

# Configuration
APIFY_TOKEN = os.environ.get("APIFY_TOKEN", "your_apify_token_here")
ACTOR_ID = "get-leads~linkedin-scraper"
BUCKET_NAME = os.environ.get("GCS_BUCKET_NAME", "your_bucket_name_here")
LOCAL_DATA_DIR = "research-pipeline/linkedin/data/raw"

# Generic high-growth AI and Tech companies for research
COMPANIES = [
    "OpenAI", "Google DeepMind", "Meta AI", "Anthropic", "Mistral AI",
    "NVIDIA", "Microsoft Research", "Hugging Face", "Scale AI", "Databricks"
]

def run_discovery(query, location="San Francisco Bay Area", max_results=10):
    """Triggers the Apify LinkedIn scraper actor for tech research."""
    url = f"https://api.apify.com/v2/acts/{ACTOR_ID}/runs?token={APIFY_TOKEN}"
    
    payload = {
        "mode": "search_profiles",
        "searchQuery": query,
        "location": location,
        "maxResults": max_results,
        "proxyConfiguration": {"useApifyProxy": True}
    }
    
    print(f"🔍 Starting research discovery for: {query} in {location}...")
    response = requests.post(url, json=payload)
    
    if response.status_code != 201:
        print(f"❌ Failed to start run: {response.text}")
        return None

    run_id = response.json()["data"]["id"]
    print(f"✅ Run started! Run ID: {run_id}")

    # Wait for completion
    while True:
        status_response = requests.get(f"https://api.apify.com/v2/actor-runs/{run_id}?token={APIFY_TOKEN}").json()
        status = status_response["data"]["status"]
        print(f"Status: {status}")
        if status == "SUCCEEDED": break
        if status in ["FAILED", "ABORTED"]: 
            print(f"Run {status}. Check Apify console.")
            return None
        time.sleep(15)

    dataset_id = status_response["data"]["defaultDatasetId"]
    items_response = requests.get(f"https://api.apify.com/v2/datasets/{dataset_id}/items?token={APIFY_TOKEN}")
    items = items_response.json()
    
    print(f"Dataset ID: {dataset_id} | Items count: {len(items)}")
    
    if not items:
        print(f"No items found in dataset.")
        return None

    # Filename generation
    timestamp = int(time.time())
    filename = f"linkedin_research_{timestamp}.json"
    
    # Ensure local directory exists
    os.makedirs(LOCAL_DATA_DIR, exist_ok=True)
    local_path = os.path.join(LOCAL_DATA_DIR, filename)

    # Save Locally
    with open(local_path, 'w') as f:
        json.dump(items, f, indent=2)
    print(f"Results saved locally to {local_path}")

    # Upload to GCS
    if BUCKET_NAME != "your_bucket_name_here":
        remote_path = f"gs://{BUCKET_NAME}/linkedin/raw/{filename}"
        try:
            subprocess.run(["gcloud", "storage", "cp", local_path, remote_path], check=True)
            print(f"Results uploaded to GCS: {remote_path}")
        except subprocess.CalledProcessError as e:
            print(f"Error uploading to GCS: {e}")
    
    return local_path

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else COMPANIES[0]
    run_discovery(f"AI Researcher {target}")
