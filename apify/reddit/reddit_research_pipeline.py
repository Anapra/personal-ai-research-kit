import os
import json
import requests
import time
import subprocess
import tempfile
import sys

# --- Configuration ---
APIFY_API_TOKEN = os.environ.get("APIFY_TOKEN", "your_apify_token_here")
ACTOR_ID = "trudax~reddit-scraper-lite"
BUCKET_NAME = os.environ.get("GCS_BUCKET_NAME", "your_bucket_name_here")
LOCAL_DATA_DIR = "lead-gen-pipeline/reddit-run/data/raw"

# Monitor Configuration
MONITOR_SUBREDDITS = [
    "googlecloud", "dataengineering", "MachineLearning", "bigdata", 
    "SaaS", "devops", "CloudComputing", "SaudiArabia", "Dubai", "UAE"
]
MONITOR_KEYWORDS = [
    # Primary Technical & Role Focus
    "GCP", "Google Cloud", "Cloud Architect", "Data Engineer", "FinOps", 
    "BigQuery", "Dataflow", "Looker", "Vertex AI", "Anthos", "Sovereign Cloud",
    # Regional & Compliance Focus
    "Saudi", "Riyadh", "KSA", "NEOM", "SAMA", "CMA", "MENA", "Dubai", "Abu Dhabi",
    # High-Intent Hiring Signals
    "hiring", "we're hiring", "looking for", "open role", "joining the team",
    "recruiting", "job opening", "apply now", "position available"
]

def run_apify_reddit(search_terms, max_items=20, mode="posts"):
    """
    Triggers the Apify Reddit Scraper.
    Modes: posts, comments, subreddits, users, search, monitor
    """
    if mode == "monitor":
        print(f"--- Starting Reddit MONITOR Run ---")
        # For monitor, we construct a search query that targets specific subreddits and keywords
        # Example: (subreddit:googlecloud OR subreddit:dataengineering) "hiring"
        sub_query = " OR ".join([f"subreddit:{s}" for s in MONITOR_SUBREDDITS])
        key_query = " OR ".join([f'"{k}"' for k in MONITOR_KEYWORDS])
        final_query = f"({sub_query}) ({key_query})"
        print(f"Monitor Query: {final_query}")
        search_terms = final_query
        mode = "search" # Reuse search logic

    print(f"--- Starting Reddit Scraper Run ---")
    print(f"Search Terms: {search_terms} | Max Items: {max_items} | Mode: {mode}")
    
    run_url = f"https://api.apify.com/v2/acts/{ACTOR_ID}/runs?token={APIFY_API_TOKEN}"
    
    if mode == "subreddits":
        payload = {
            "startUrls": [{"url": f"https://www.reddit.com/r/{search_terms}/"}],
            "maxItems": max_items,
            "proxy": {"useApifyProxy": True}
        }
    elif mode == "search":
        # Encode search terms for URL
        query = search_terms.replace(" ", "+").replace('"', '%22')
        payload = {
            "startUrls": [{"url": f"https://www.reddit.com/search/?q={query}&sort=new"}],
            "maxItems": max_items,
            "proxy": {"useApifyProxy": True}
        }
    else: # Default posts/general
        payload = {
            "search": search_terms,
            "maxItems": max_items,
            "maxPostCount": max_items,
            "proxy": {"useApifyProxy": True}
        }

    response = requests.post(run_url, json=payload)
    if response.status_code != 201:
        print(f"Error triggering actor: {response.text}")
        return None

    run_id = response.json()["data"]["id"]
    print(f"Run started: {run_id}")

    # Wait for completion
    while True:
        status_response = requests.get(f"https://api.apify.com/v2/actor-runs/{run_id}?token={APIFY_API_TOKEN}").json()
        status = status_response["data"]["status"]
        print(f"Status: {status}")
        if status == "SUCCEEDED": break
        if status in ["FAILED", "ABORTED"]: 
            print(f"Run {status}. Check Apify console.")
            return None
        time.sleep(15)

    dataset_id = status_response["data"]["defaultDatasetId"]
    items_response = requests.get(f"https://api.apify.com/v2/datasets/{dataset_id}/items?token={APIFY_API_TOKEN}")
    items = items_response.json()
    
    print(f"Dataset ID: {dataset_id} | Items count: {len(items)}")
    
    if not items:
        print(f"No items found in dataset. Response: {items_response.text[:200]}")
        return None

    # Filename generation
    timestamp = int(time.time())
    filename = f"reddit_{mode}_{timestamp}.json"
    
    # Ensure local directory exists
    os.makedirs(LOCAL_DATA_DIR, exist_ok=True)
    local_path = os.path.join(LOCAL_DATA_DIR, filename)

    # Save Locally
    with open(local_path, 'w') as f:
        json.dump(items, f, indent=2)
    print(f"Results saved locally to {local_path}")

    # Upload to GCS
    remote_path = f"gs://{BUCKET_NAME}/reddit/raw/{filename}"
    try:
        subprocess.run(["gcloud", "storage", "cp", local_path, remote_path], check=True)
        print(f"Results uploaded to GCS: {remote_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error uploading to GCS: {e}")
    
    return local_path

if __name__ == "__main__":
    # Usage: python3 script.py [search_term] [max_items] [mode]
    # Example: python3 script.py "GCP Cloud Architect" 10 posts
    # Example: python3 script.py "" 20 monitor
    
    search = sys.argv[1] if len(sys.argv) > 1 else "Google Cloud Saudi Arabia"
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    mode = sys.argv[3] if len(sys.argv) > 3 else "posts"
    
    run_apify_reddit(search, limit, mode)
