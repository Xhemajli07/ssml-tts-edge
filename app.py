from flask import Flask, request, jsonify, send_file
import edge_tts
import asyncio
import os

app = Flask(__name__)

@app.route('/synthesize', methods=['POST'])
async def synthesize():
    try:
        # Récupération des données JSON
        data = request.json
        ssml = data.get('ssml', '')
        voice = data.get('voice', 'en-US-AriaNeural')

        if not ssml:
            return jsonify({'error': 'Le texte SSML est requis.'}), 400

        # Nom du fichier temporaire pour l'audio
        output_file = "output_audio.mp3"

        # Génération de l'audio avec edge-tts
        tts = edge_tts.Communicate(ssml, voice)
        await tts.save(output_file)

        # Envoi du fichier audio généré
        return send_file(output_file, as_attachment=True)
    except Exception as e:
        print(f"Erreur : {e}")
        return jsonify({'error': 'Une erreur est survenue lors de la synthèse vocale.'}), 500

if __name__ == '__main__':
    # Récupère le port attribué par Render ou utilise 5000 par défaut
    port = int(os.environ.get('PORT', 5000))
    # Exécute Flask sur toutes les interfaces réseau disponibles (0.0.0.0)
    app.run(host='0.0.0.0', port=port)
