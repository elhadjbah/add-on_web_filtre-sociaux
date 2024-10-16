from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline
from nudenet import NudeDetector
import requests
from PIL import Image
import numpy as np
import io

app = Flask(__name__)
CORS(app)

# Charger le modèle d'analyse de sentiment
sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

@app.after_request
def add_cors_headers(response):
    # Ajoute des en-têtes CORS
    response.headers.add('Access-Control-Allow-Origin', 'https://x.com')  # Spécifie l'origine autorisée
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')  # Méthodes autorisées
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')  # En-têtes autorisés
    return response

@app.route('/proxy', methods=['POST'])
def proxy_request():
    # Relayer une requête à une autre API
    url = 'https://x.com/*'  # Remplacez par l'URL de votre API
    response = requests.post(url, json=request.json)  # Relayer la requête
    return jsonify(response.json()), response.status_code  # Retourner la réponse

@app.route('/analyze_content', methods=['POST'])
def analyze_content():
    # Vérifier si le texte est fourni
    if 'text' not in request.form:
        return jsonify({'error': 'No text provided'}), 400
    
    content_text = request.form['text']
    
    # Analyse du texte
    result = sentiment_pipeline(content_text)
    is_text_inappropriate = result[0]['label'] == 'NEGATIVE'  # Considérer comme inapproprié si le label est 'NEGATIVE'
    
    return jsonify({
        'isTextInappropriate': is_text_inappropriate
    })

@app.route('/filtered_tweets', methods=['GET'])
def filtered_tweets():
    # Logique pour renvoyer les tweets filtrés
    return jsonify({'message': 'This route would return filtered tweets.'})

if __name__ == '__main__':
    app.run(debug=True)
