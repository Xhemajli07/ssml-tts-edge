from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import edge_tts
import asyncio
import os 

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
        # Récupération des données
        data = request.json
        print(f"Données reçues : {data}")

        text = data.get('text', '').strip()
        voice = data.get('voice', 'en-US-AriaNeural')
        rate = data.get('rate', '0%')
        volume = data.get('volume', '0%')
        pitch = data.get('pitch', '0Hz')

        print(f"Paramètres : text='{text}', voice='{voice}', rate='{rate}', volume='{volume}', pitch='{pitch}'")

        # Validation de l'entrée
        if not text:
            return jsonify({'error': 'Le texte est requis.'}), 400

        # Nom du fichier de sortie
        output_file = "/tmp/output_audio.mp3"
        print(f"Fichier de sortie : {output_file}")

        # Génération de l'audio
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
        print("Synthèse terminée avec succès")
        return send_file(output_file, as_attachment=True)

    except Exception as e:
        print(f"Erreur lors de la synthèse : {e}")
        return jsonify({'error': str(e)}), 500

# Lancer l'application Flask
if __name__ == '__main__':
    # Récupère le port attribué par Render ou utilise 5000 par défaut
    port = int(os.environ.get('PORT', 5000))
    # Exécute Flask sur toutes les interfaces réseau disponibles (0.0.0.0)
    app.run(host='0.0.0.0', port=port)
