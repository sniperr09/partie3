import json
import os
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class PersonnageWebhook(BaseModel):
    nom: str
    score: int

@app.post("/webhook/personnage")
def recevoir_webhook(p: PersonnageWebhook):
    if p.score >= 90:
        niveau = "Expert"
    elif p.score >= 70:
        niveau = "Confirmé"
    else:
        niveau = "Débutant"

    personnage_avec_niveau = {
        "nom": p.nom,
        "score": p.score,
        "niveau": niveau
    }

    try:
        if os.path.exists("webhook_log.json"):
            with open("webhook_log.json", "r+", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = []
                data.append(personnage_avec_niveau)
                f.seek(0)
                json.dump(data, f, ensure_ascii=False, indent=2)
        else:
            with open("webhook_log.json", "w", encoding="utf-8") as f:
                json.dump([personnage_avec_niveau], f, ensure_ascii=False, indent=2)
    except Exception as e:
        return {"erreur": str(e)}

    print(f"✅ Personnage ajouté avec succès : {personnage_avec_niveau['nom']}")
    with open("notifications.txt", "a", encoding="utf-8") as notif_file:
        notif_file.write(f"Personnage ajouté : {personnage_avec_niveau['nom']} ({personnage_avec_niveau['niveau']})\n")

    return personnage_avec_niveau
