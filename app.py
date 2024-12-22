from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import edge_tts
import asyncio

# Initialisation de l'application Flask
app = Flask(__name__)
CORS(app)  # Activer les CORS pour permettre les requêtes entre frontend et backend

# Route pour récupérer la liste des voix disponibles
@app.route('/voices', methods=['GET'])
def get_voices():
    # Liste des voix disponibles
    voices = [
        "en-US-AriaNeural",
        "fr-FR-DeniseNeural",
        "es-ES-ElviraNeural"
        # Ajoutez d'autres voix si nécessaire
    ]
    return jsonify(voices)

# Route pour la synthèse vocale
@app.route('/synthesize', methods=['POST'])
def synthesize():
    try:
        # Récupération des données de la requête
        data = request.json
        text = data.get('text', '').strip()
        voice = data.get('voice', 'en-US-AriaNeural')
        rate = data.get('rate', '0%')
        volume = data.get('volume', '0%')
        pitch = data.get('pitch', '0Hz')

        # Validation de l'entrée
        if not text:
            return jsonify({'error': 'Le texte est requis.'}), 400

        # Nom du fichier de sortie
        output_file = "output_audio.mp3"

        # Utilisation d'edge-tts pour générer l'audio
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

        # Retourner le fichier audio généré
        return send_file(output_file, as_attachment=True)

    except Exception as e:
        print(f"Erreur : {e}")
        return jsonify({'error': 'Une erreur est survenue lors de la synthèse vocale.'}), 500

# Lancer l'application Flask
if __name__ == '__main__':
    # Récupère le port attribué par Render ou utilise 5000 par défaut
    port = int(os.environ.get('PORT', 5000))
    # Exécute Flask sur toutes les interfaces réseau disponibles (0.0.0.0)
    app.run(host='0.0.0.0', port=port)
