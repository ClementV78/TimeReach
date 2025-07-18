# Configuration des logs

## Variables d'environnement

### LOG_LEVEL
Contrôle le niveau de logging de l'application.

**Valeurs possibles :**
- `INFO` (par défaut) - Logs normaux
- `DEBUG` - Logs détaillés pour le débogage
- `WARNING` - Seulement les avertissements et erreurs
- `ERROR` - Seulement les erreurs

**Exemples d'utilisation :**

### En local
```bash
# Mode DEBUG pour le développement
export LOG_LEVEL=DEBUG
uvicorn main:app --reload

# Mode INFO (par défaut)
uvicorn main:app

# Mode WARNING pour moins de logs
export LOG_LEVEL=WARNING
uvicorn main:app
```

### Sur Render
Dans le dashboard Render, aller dans Environment Variables et ajouter :
- Key: `LOG_LEVEL`
- Value: `DEBUG` (ou `INFO`, `WARNING`, `ERROR`)

### Avec Docker
```bash
docker run -e LOG_LEVEL=DEBUG your-image
```

## Niveaux de logging

### INFO (par défaut)
- Logs les requêtes importantes
- Temps de réponse des APIs externes
- Messages de statut

### DEBUG
- Tous les logs INFO +
- Détails des paramètres de requête
- Réponses complètes des APIs externes
- Messages de débogage détaillés

### Exemple de sortie

**Mode INFO :**
```
2025-07-18 10:30:00 [INFO] __main__: 🚀 [STARTUP] TimeReach API - Logging configuré en mode INFO
2025-07-18 10:30:01 [INFO] __main__: [LOG] /places endpoint called (GET)
2025-07-18 10:30:01 [INFO] __main__: [Google Geocoding] Response time: 0.45s
```

**Mode DEBUG :**
```
2025-07-18 10:30:00 [INFO] __main__: 🚀 [STARTUP] TimeReach API - Logging configuré en mode DEBUG
2025-07-18 10:30:00 [DEBUG] __main__: 🔧 [STARTUP] Debug logging activé - mode détaillé
2025-07-18 10:30:01 [INFO] __main__: [LOG] /places endpoint called (GET)
2025-07-18 10:30:01 [DEBUG] __main__: [API Request] location=Paris, lat=None, lon=None, minutes=20...
2025-07-18 10:30:01 [DEBUG] __main__: [Google Geocoding] Request params: {'address': 'Paris', 'key': '***'}
2025-07-18 10:30:01 [DEBUG] __main__: [Google Geocoding] Response JSON: {'results': [...]}
```
