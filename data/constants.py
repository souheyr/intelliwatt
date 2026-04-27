# data/constants.py
# Static datasets: buildings, scenarios, chart data

import numpy as np
import pandas as pd
from datetime import datetime

np.random.seed(42)

# ── Buildings ─────────────────────────────────────────────────
BUILDINGS_DATA = [
    {"id": 1, "nom": "Bâtiment A — Sciences",       "type": "Laboratoire",          "conso": 340, "capacite": 400, "statut": "Critique",    "etage": 3, "surface": 2500},
    {"id": 2, "nom": "Bâtiment B — Informatique",   "type": "Laboratoire",          "conso": 280, "capacite": 350, "statut": "Actif",        "etage": 4, "surface": 3000},
    {"id": 3, "nom": "Bâtiment C — Administration", "type": "Bureau Administratif", "conso": 190, "capacite": 250, "statut": "Actif",        "etage": 2, "surface": 1800},
    {"id": 4, "nom": "Bâtiment D — Amphithéâtres",  "type": "Salle de Cours",       "conso": 220, "capacite": 300, "statut": "Actif",        "etage": 2, "surface": 4000},
    {"id": 5, "nom": "Bâtiment E — Bibliothèque",   "type": "Bibliothèque",         "conso": 155, "capacite": 200, "statut": "Actif",        "etage": 3, "surface": 2200},
    {"id": 6, "nom": "Bâtiment F — Résidence",      "type": "Bureau Administratif", "conso": 210, "capacite": 260, "statut": "Maintenance",  "etage": 5, "surface": 3500},
    {"id": 7, "nom": "Bâtiment G — Cafétéria",      "type": "Cafétéria",            "conso": 175, "capacite": 220, "statut": "Actif",        "etage": 1, "surface": 800},
    {"id": 8, "nom": "Bâtiment H — Recherche",      "type": "Laboratoire",          "conso": 390, "capacite": 420, "statut": "Critique",     "etage": 4, "surface": 3200},
]

df_buildings = pd.DataFrame(BUILDINGS_DATA)

# ── 30-day evolution series ───────────────────────────────────
dates = pd.date_range(end=datetime.today(), periods=30)
evolution_data: dict[str, list[float]] = {}
for b in BUILDINGS_DATA:
    base = b["conso"]
    evolution_data[b["nom"].split("—")[0].strip()] = [
        max(50, base + np.random.normal(0, base * 0.08)) for _ in range(30)
    ]
df_evolution = pd.DataFrame(evolution_data, index=dates)

# ── Heatmap (hour × day) ─────────────────────────────────────
hours    = list(range(24))
days_fr  = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
heatmap_data = np.random.uniform(50, 400, (7, 24))
for d in range(7):
    for h in range(24):
        if 8 <= h <= 18:
            heatmap_data[d][h] *= 1.5
        elif h <= 6 or h >= 22:
            heatmap_data[d][h] *= 0.3

# ── Test scenarios ────────────────────────────────────────────
SCENARIOS = [
    {
        "id": 1,
        "nom_fr": "Surcharge Laboratoire de Physique",
        "params": "Bât. A | 340 kWh | Cap: 400 kWh | 14h–18h",
        "obtained": "340 kWh détectés, seuil 85% dépassé",
        "expected": "Alerte critique générée",
        "comment_fr": "Le laboratoire dépasse 85%. Intervention requise.",
        "status": "PASS",
        "saving_pct": 15.3,
        "type": "critique",
    },
    {
        "id": 2,
        "nom_fr": "Optimisation Nuit Bibliothèque",
        "params": "Bât. E | 155 kWh | HC 22h–6h",
        "obtained": "Réduction 32.1% détectée",
        "expected": "Économie maximale HC",
        "comment_fr": "Excellent résultat en heures creuses.",
        "status": "PASS",
        "saving_pct": 32.1,
        "type": "normal",
    },
    {
        "id": 3,
        "nom_fr": "Gaspillage Résidence Week-end",
        "params": "Bât. F | 210 kWh | Sam-Dim",
        "obtained": "Consommation identique week-end",
        "expected": "Réduction 20% détectée",
        "comment_fr": "Absence d'occupation non détectée.",
        "status": "FAIL",
        "saving_pct": 0,
        "type": "gaspillage",
    },
    {
        "id": 4,
        "nom_fr": "Panne Capteur Cafétéria",
        "params": "Bât. G | Capteur T3 défaillant",
        "obtained": "Données manquantes 6h",
        "expected": "Alerte maintenance générée",
        "comment_fr": "Panne détectée avec délai de 6h.",
        "status": "PASS",
        "saving_pct": 8.7,
        "type": "panne",
    },
    {
        "id": 5,
        "nom_fr": "Pic Consommation Amphithéâtres",
        "params": "Bât. D | 220 kWh | 9h–11h | Exam",
        "obtained": "Pic 280 kWh détecté",
        "expected": "Alerte dépassement seuil HP",
        "comment_fr": "Pic bien détecté pendant examens.",
        "status": "PASS",
        "saving_pct": 12.5,
        "type": "critique",
    },
]
