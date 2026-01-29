from flask import Flask, request, render_template, jsonify
import requests
import os
from dotenv import load_dotenv  # ← AJOUTER CETTE LIGNE

# Charger les variables d'environnement depuis .env
load_dotenv()  # ← AJOUTER CETTE LIGNE

app = Flask(__name__)

# Configuration GitHub - REMPLACEZ LE TOKEN ICI
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_OWNER = "Moesthetics-code"
GITHUB_REPO = "projet-iac-ec2"
WORKFLOW_ID = "terraform.yml"

@app.route("/")
def index():
    return render_template("form.html")

@app.route("/trigger", methods=["POST"])
def trigger_pipeline():
    try:
        # Récupération des données du formulaire
        instance_name = request.form.get("instance_name", "").strip()
        instance_os = request.form.get("instance_os", "").strip()
        instance_size = request.form.get("instance_size", "").strip()
        instance_env = request.form.get("instance_env", "").strip()
        
        # Validation
        if not all([instance_name, instance_os, instance_size, instance_env]):
            return error_response("Tous les champs sont obligatoires")
        
        # Vérification de l'AMI
        if not instance_os.startswith("ami-"):
            return error_response(f"AMI invalide: {instance_os}. Doit commencer par 'ami-'")
        
        # URL de l'API GitHub
        url = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/actions/workflows/{WORKFLOW_ID}/dispatches"
        
        # Headers avec authentification
        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "X-GitHub-Api-Version": "2022-11-28"
        }
        
        # Payload pour déclencher le workflow
        payload = {
            "ref": "main",
            "inputs": {
                "instance_name": instance_name,
                "instance_os": instance_os,
                "instance_size": instance_size,
                "instance_env": instance_env
            }
        }
        
        # Debug : afficher dans le terminal
        print("=" * 60)
        print("🚀 DÉCLENCHEMENT DU WORKFLOW")
        print(f"URL: {url}")
        print(f"Instance: {instance_name}")
        print(f"AMI: {instance_os}")
        print(f"Type: {instance_size}")
        print(f"Env: {instance_env}")
        print("=" * 60)
        
        # Envoi de la requête
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        
        # Debug : afficher la réponse
        print(f"Status Code: {response.status_code}")
        if response.status_code != 204:
            print(f"Response: {response.text}")
        print("=" * 60)
        
        if response.status_code == 204:
            return success_response(instance_name, instance_os, instance_size, instance_env)
        else:
            return error_response(
                f"Erreur GitHub API (Code: {response.status_code})",
                response.text
            )
            
    except requests.exceptions.Timeout:
        return error_response("Timeout: La requête a pris trop de temps")
    except requests.exceptions.RequestException as e:
        return error_response("Erreur de connexion", str(e))
    except Exception as e:
        return error_response("Erreur inattendue", str(e))

def success_response(name, os, size, env):
    """Génère une page de succès"""
    return f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <title>Succès</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 40px;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                margin: 0;
            }}
            .container {{
                background-color: white;
                padding: 40px;
                border-radius: 15px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.2);
                max-width: 600px;
                text-align: center;
            }}
            .success-icon {{
                font-size: 80px;
                margin-bottom: 20px;
            }}
            h1 {{
                color: #28a745;
                margin-bottom: 20px;
            }}
            .details {{
                background-color: #f8f9fa;
                padding: 20px;
                border-radius: 10px;
                margin: 20px 0;
                text-align: left;
            }}
            .detail-row {{
                padding: 10px 0;
                border-bottom: 1px solid #dee2e6;
            }}
            .detail-row:last-child {{
                border-bottom: none;
            }}
            .btn {{
                display: inline-block;
                padding: 12px 30px;
                margin: 10px;
                background-color: #007bff;
                color: white;
                text-decoration: none;
                border-radius: 8px;
                font-weight: bold;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="success-icon">✅</div>
            <h1>Pipeline déclenché avec succès !</h1>
            <div class="details">
                <div class="detail-row"><strong>Instance:</strong> {name}</div>
                <div class="detail-row"><strong>AMI:</strong> {os}</div>
                <div class="detail-row"><strong>Type:</strong> {size}</div>
                <div class="detail-row"><strong>Environnement:</strong> {env}</div>
            </div>
            <a href="https://github.com/{GITHUB_OWNER}/{GITHUB_REPO}/actions" class="btn" target="_blank">
                📊 Voir le déploiement
            </a>
            <a href="/" class="btn">🏠 Nouvelle instance</a>
        </div>
    </body>
    </html>
    """

def error_response(title, details=""):
    """Génère une page d'erreur"""
    return f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <title>Erreur</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                padding: 40px;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
            }}
            .container {{
                background-color: white;
                padding: 40px;
                border-radius: 15px;
                max-width: 600px;
                text-align: center;
            }}
            .error-icon {{
                font-size: 80px;
                margin-bottom: 20px;
            }}
            h1 {{
                color: #dc3545;
            }}
            .error-details {{
                background-color: #f8d7da;
                padding: 15px;
                margin: 20px 0;
                border-radius: 5px;
                color: #721c24;
                word-wrap: break-word;
            }}
            .btn {{
                display: inline-block;
                padding: 12px 30px;
                margin-top: 20px;
                background-color: #007bff;
                color: white;
                text-decoration: none;
                border-radius: 8px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="error-icon">❌</div>
            <h1>Erreur</h1>
            <p><strong>{title}</strong></p>
            {f'<div class="error-details"><strong>Détails:</strong><br>{details}</div>' if details else ''}
            <a href="/" class="btn">🔄 Réessayer</a>
        </div>
    </body>
    </html>
    """

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Serveur Flask démarré")
    print(f"📍 URL: http://localhost:5000")
    print(f"👤 GitHub Owner: {GITHUB_OWNER}")
    print(f"📦 Repository: {GITHUB_REPO}")
    print(f"🔑 Token configuré: {GITHUB_TOKEN[:10]}...") 
    print("=" * 60)
    app.run(debug=True, host="0.0.0.0", port=5000)