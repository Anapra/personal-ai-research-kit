from flask import Flask, render_template, request, redirect, url_for
from google.cloud import firestore
import os

app = Flask(__name__)

# Initialize Firestore
PROJECT_ID = os.environ.get('PROJECT_ID', 'your-project-id')
db = firestore.Client(project=PROJECT_ID)

@app.route('/')
def index():
    # Fetch high-relevance insights
    insights_ref = db.collection('insights').where('relevance_score', '>', 50).order_by('relevance_score', direction=firestore.Query.DESCENDING)
    insights = [doc.to_dict() for doc in insights_ref.stream()]
    return render_template('index.html', insights=insights)

@app.route('/action/<insight_id>/<action>')
def take_action(insight_id, action):
    doc_ref = db.collection('insights').document(insight_id)
    doc_ref.update({'status': action})
    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
