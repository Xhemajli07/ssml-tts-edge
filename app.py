from flask import Flask, request, jsonify, send_file
import edge_tts
import asyncio
import os
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def home():
    return "Bienvenue sur l'API edge-tts !", 200

@app.route('/synthesize', methods=['POST'])
def synthesize():
    try:
        data = request.json
        text = data.get('text', '')
        voice = data.get('voice', 'en-US-AriaNeural')
        rate = data.get('rate', '0%')  # Par défaut, pas de changement de taux
        volume = data.get('volume', '0%')  # Par défaut, pas de changement de volume
        pitch = data.get('pitch', '0Hz')  # Par défaut, pas de changement de hauteur

        if not text:
            return jsonify({'error': 'Le texte est requis.'}), 400

        output_file = "output_audio.mp3"
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(
            edge_tts.Communicate(
                text,
                voice=voice,
                rate=rate,
                volume=volume,
                pitch=pitch
            ).save(output_file)
        )

        return send_file(output_file, as_attachment=True)
    except Exception as e:
        print(f"Erreur : {e}")
        return jsonify({'error': 'Une erreur est survenue lors de la synthèse vocale.'}),

if __name__ == '__main__':
    # Récupère le port attribué par Render ou utilise 5000 par défaut
    port = int(os.environ.get('PORT', 5000))
    # Exécute Flask sur toutes les interfaces réseau disponibles (0.0.0.0)
    app.run(host='0.0.0.0', port=port)
