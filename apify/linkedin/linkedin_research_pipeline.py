import requests
import json
import os
import sys

# Configuration
APIFY_TOKEN = os.environ.get("APIFY_TOKEN", "your_apify_token_here")
ACTOR_ID = "get-leads~linkedin-scraper"

COMPANIES = [
    "NEOM", "Saudi Aramco", "Salla", "STC", "Mobily", "Zain Saudi Arabia",
    "Al Rajhi Bank", "SABIC", "Ma'aden", "Saudi National Bank", "PIF",
    "Aramco Digital", "THIQAH", "SDAIA", "Lean Business Services", "Elm",
    "SITE", "PwC Middle East", "Deloitte Middle East", "KPMG Saudi Arabia",
    "EY Saudi Arabia", "Accenture Saudi Arabia"
]

def run_discovery(query, location="Saudi Arabia", max_results=10):
    """Triggers the Apify LinkedIn scraper actor."""
    # API URL for starting a run: https://api.apify.com/v2/acts/{ACTOR_ID}/runs
    url = f"https://api.apify.com/v2/acts/{ACTOR_ID}/runs?token={APIFY_TOKEN}"
    
    payload = {
        "mode": "search_profiles",
        "searchQuery": query,
        "location": location,
        "maxResults": max_results,
        "proxyConfiguration": {"useApifyProxy": True}
    }
    
    print(f"🔍 Starting discovery for: {query} in {location}...")
    response = requests.post(url, json=payload)
    
    if response.status_code == 201:
        run_data = response.json()
        print(f"✅ Run started! Run ID: {run_data['data']['id']}")
        return run_data['data']['id']
    else:
        print(f"❌ Failed to start run: {response.text}")
        return None

if __name__ == "__main__":
    # If no arguments, run for the first company in the list
    target = sys.argv[1] if len(sys.argv) > 1 else COMPANIES[0]
    run_discovery(f"GCP Data Engineer {target}")
