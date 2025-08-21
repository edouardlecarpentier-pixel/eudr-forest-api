from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

def verifier_coordonnees_en_ligne(geojson):
    coordinates = geojson.get("geometry", {}).get("coordinates", None)
    if not coordinates or not isinstance(coordinates, list):
        return {"error": "Coordonnées GeoJSON invalides."}
    lon, lat = coordinates
    url_verif = f"https://api.openforest.ai/v1/eudr?lon={lon}&lat={lat}"
    try:
        r = requests.get(url_verif)
        resultat = r.json()
    except Exception:
        resultat = {"status": "erreur", "message": "Service non accessible"}
    return resultat

@app.route('/')
def home():
    return jsonify({"message": "Bienvenue sur l'API EUDR Forest ! Utilise POST /verifier."})

@app.route('/favicon.ico')
def favicon():
    return '', 204

@app.route('/verifier', methods=['POST'])
def verifier():
    data = request.get_json()
    if not data or "geojson" not in data:
        return jsonify({"error": "Requête invalide : champ 'geojson' absent."}), 400
    geojson = data.get("geojson")
    res = verifier_coordonnees_en_ligne(geojson)
    return jsonify(res)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
