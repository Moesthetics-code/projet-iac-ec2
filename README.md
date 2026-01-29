# 🚀 Projet IAC SONATEL - Déploiement EC2 avec Terraform

Projet d'Infrastructure as Code pour créer des instances EC2 sur AWS via une interface web et GitHub Actions.

## 📋 Prérequis

- Compte AWS avec accès programmatique
- Compte GitHub
- Python 3.8 ou supérieur
- Git installé

## 🔧 Configuration pas à pas

### Étape 1 : Créer le compte AWS et récupérer les credentials

1. Connectez-vous à [AWS Console](https://aws.amazon.com/)
2. Allez dans **IAM** → **Users** → **Create User**
3. Nom d'utilisateur : `tr-user`
4. Cochez **Programmatic access**
5. Attachez la politique : `AmazonEC2FullAccess`
6. **IMPORTANT** : Notez l'`AWS_ACCESS_KEY_ID` et `AWS_SECRET_ACCESS_KEY`

### Étape 2 : Créer le dépôt GitHub

1. Allez sur [GitHub](https://github.com/)
2. Cliquez sur **New repository**
3. Nom : `projet-iac-ec2`
4. Public ou Private (votre choix)
5. Cliquez sur **Create repository**

### Étape 3 : Créer un Personal Access Token GitHub

1. GitHub → **Settings** (votre profil) → **Developer settings**
2. **Personal access tokens** → **Tokens (classic)**
3. **Generate new token (classic)**
4. Note : `Terraform Deployment Token`
5. Expirationː 90 days
6. Cochez les permissions :
   - ✅ `repo` (Full control)
   - ✅ `workflow` (Update GitHub Action workflows)
7. Cliquez sur **Generate token**
8. **COPIEZ LE TOKEN** (format: `ghp_xxxxxxxxxxxxx`)

### Étape 4 : Configurer les Secrets GitHub

1. Allez dans votre dépôt → **Settings** → **Secrets and variables** → **Actions**
2. Cliquez sur **New repository secret**
3. Ajoutez ces 2 secrets :

   **Secret 1:**
   - Name : `AWS_ACCESS_KEY_ID`
   - Value : `AKIAXXXXXXXXXXXXX` (votre clé AWS)

   **Secret 2:**
   - Name : `AWS_SECRET_ACCESS_KEY`
   - Value : `xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` (votre clé secrète AWS)

### Étape 5 : Cloner et configurer le projet
```bash
# Cloner le dépôt
git clone https://github.com/VOTRE_USERNAME/projet-iac-ec2.git
cd projet-iac-ec2

# Créer la structure
mkdir -p infra templates .github/workflows

# Copier tous les fichiers fournis dans leurs dossiers respectifs
```

### Étape 6 : Modifier app.py

Ouvrez `app.py` et modifiez ces lignes :
```python
GITHUB_TOKEN = "ghp_VOTRE_TOKEN_ICI"  # Votre token GitHub
GITHUB_OWNER = "VOTRE_USERNAME_GITHUB"  # Votre username GitHub
GITHUB_REPO = "projet-iac-ec2"  # Nom de votre dépôt
```

### Étape 7 : Pousser le code sur GitHub
```bash
git add .
git commit -m "Initial commit - Projet IAC EC2"
git branch -M main
git push -u origin main
```

### Étape 8 : Installer et lancer l'application Flask
```bash
# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
python app.py
```

### Étape 9 : Utiliser l'application

1. Ouvrez votre navigateur : `http://localhost:5000`
2. Remplissez le formulaire :
   - Nom de l'instance
   - Choisissez une image (AMI)
   - Type d'instance
   - Environnement
3. Cliquez sur **Lancer l'instance**
4. Le workflow GitHub Actions va se déclencher
5. Suivez l'exécution : `https://github.com/Moesthetics-code/projet-iac-ec2/actions`

## 📊 Vérifier le déploiement

### Via GitHub Actions
```
GitHub → Votre dépôt → Actions → Terraform EC2 Deployment
```

### Via AWS Console
```
AWS Console → EC2 → Instances
```

### Via Terraform (si vous voulez voir les outputs)
```bash
cd infra
terraform init
terraform output
```

## 🔍 Débogage

### Erreur 403 GitHub
- Vérifiez que votre token a les bonnes permissions
- Régénérez un nouveau token si nécessaire

### Erreur AWS Credentials
- Vérifiez que les secrets GitHub sont bien configurés
- Testez vos credentials AWS :
```bash
aws configure
aws sts get-caller-identity
```

### Workflow ne se déclenche pas
- Vérifiez que le fichier `.github/workflows/terraform.yml` existe
- Vérifiez les noms de variables dans `app.py`

## 📚 Ressources

- [Documentation Terraform](https://developer.hashicorp.com/terraform/docs)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [AWS EC2 Documentation](https://docs.aws.amazon.com/ec2/)
- [Flask Documentation](https://flask.palletsprojects.com/)

## 🤝 Support

Pour toute question, ouvrez une issue sur GitHub.