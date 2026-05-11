from google.cloud import storage
from google.cloud import firestore
import vertexai
from vertexai.generative_models import GenerativeModel, GenerationConfig
import json
import os
import hashlib

# Initialize clients
PROJECT_ID = os.environ.get('PROJECT_ID', 'your-project-id')
db = firestore.Client(project=PROJECT_ID)

# Initialize Vertex AI
try:
    vertexai.init(project=PROJECT_ID, location="us-central1")
    model = GenerativeModel("gemini-1.5-flash-001")
except Exception as e:
    print(f"Vertex AI initialization failed: {e}")
    model = None

def heuristic_score(item_data):
    """Fallback scoring for AI research relevance."""
    score = 0
    reasoning = []
    
    # Generic AI Research Keywords
    tech_keywords = {
        "LLM": 25, "Generative AI": 25, "Transformer": 20, 
        "RAG": 20, "Agent": 15, "PyTorch": 10, "TensorFlow": 10,
        "Fine-tuning": 15, "Inference": 10, "GPU": 10
    }
    high_signal_keywords = {
        "Paper": 15, "Benchmark": 15, "SOTA": 20, 
        "Open Source": 15, "Release": 10, "Arxiv": 20
    }
    
    full_text = f"{item_data.get('title', '')} {item_data.get('summary', '')}".lower()
    
    for kw, val in tech_keywords.items():
        if kw.lower() in full_text:
            score += val
            reasoning.append(f"Tech: {kw}")
            
    for kw, val in high_signal_keywords.items():
        if kw.lower() in full_text:
            score += val
            reasoning.append(f"Signal: {kw}")
    
    score = min(score, 100)
    if not reasoning:
        reasoning = ["General tech insight."]
        score = 20
        
    return {
        "relevance_score": score,
        "reasoning": f"Heuristic: {', '.join(reasoning)}",
        "summary_brief": f"AI research related to {item_data.get('title', 'various topics')}."
    }

def score_insight(item_data):
    """Qualifies a research insight using AI."""
    if model:
        prompt = f"""
        You are a Senior AI Research Analyst.
        Analyze this research data and provide a relevance score (0-100) and a summary.
        
        Data: {json.dumps(item_data)}
        
        Output ONLY valid JSON:
        {{
          "relevance_score": 0-100,
          "reasoning": "Explain the technical significance of this finding.",
          "summary_brief": "A concise one-sentence summary of why this matters."
        }}
        """
        try:
            response = model.generate_content(prompt, generation_config=GenerationConfig(response_mime_type="application/json", temperature=0.1))
            if response.text:
                return json.loads(response.text.strip().replace('```json', '').replace('```', ''))
        except Exception as e:
            print(f"AI scoring failed: {e}")
            
    return heuristic_score(item_data)

def process_insight(data, context):
    """Triggered by GCS, handles raw research data."""
    bucket_name = data["bucket"]
    file_name = data["name"]

    if not file_name.endswith('.json'):
        return

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    
    try:
        content = blob.download_as_text()
        raw_data = json.loads(content)
        items = raw_data if isinstance(raw_data, list) else [raw_data]
        
        for item in items:
            # Flexible mapping for different sources (LinkedIn/Reddit/etc)
            title = item.get('title') or item.get('occupation') or item.get('headline') or "Research Item"
            source_url = item.get('url') or item.get('link') or item.get('profileUrl') or "#"
            summary = item.get('summary') or item.get('description') or item.get('text') or ""

            mapped_item = {
                "title": str(title).strip(),
                "summary": str(summary).strip(),
                "url": source_url
            }

            qualification = score_insight(mapped_item)
            
            doc_id = hashlib.md5(source_url.encode()).hexdigest()
            doc_ref = db.collection("insights").document(doc_id)
            
            insight_document = {
                **item,
                **qualification,
                "status": "new",
                "processed_at": firestore.SERVER_TIMESTAMP,
                "source_file": file_name
            }
            
            doc_ref.set(insight_document, merge=True)
            print(f"Processed: {mapped_item['title']} | Score: {qualification.get('relevance_score')}")
            
    except Exception as e:
        print(f"Error in process_insight: {e}")
