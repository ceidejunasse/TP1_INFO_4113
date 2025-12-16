# Utiliser une image Python de base
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les dépendances et les installer
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du code (y compris Devoir1.py, data_kpi.xlsx)
COPY . .

# Commande de démarrage (lance Gunicorn)
# Nous allons utiliser le port 8000 par convention Docker/App Runner
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "Devoir1:server"]