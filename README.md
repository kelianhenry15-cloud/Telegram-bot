# Telegram Signal Bot

Bot Python qui copie et reformate les signaux de deux canaux Telegram vers ton canal privé.

## Fonctionnalités

- Surveillance de 2 canaux Telegram.
- Formatage automatique des signaux (achat/vente, TP, SL).
- Envoi dans ton canal privé.
- Uptime avec Flask pour rester actif sur Replit.

## Installation

1. Remplace `api_id` et `api_hash` dans `bot.py` par tes identifiants Telegram.
2. Mets les URLs des canaux source et l’ID du canal cible.
3. Lance le bot avec :
   ```bash
   python bot.py
