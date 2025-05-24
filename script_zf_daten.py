import pandas as pd
import os
from glob import glob

# Pfad zum Ordner mit allen Excel-Dateien
ORDNER = "/Users/fabianfacalbiemmi/Desktop/AI_Applications/Pro_wyscout"
AUSGABE_DATEI = "wyscout_players_combined.csv"

# Spalten extrahieren und aggregieren
RELEVANTE_SPALTEN = {
    "Gespielte Minuten": "minutes",
    "Tore": "goals",
    "Vorlage": "assists",
    "Pässe / erfolgreich": "passes_success",
    "Pässe / gesamt": "passes_total",
    "Schüsse / aus Tor": "shots_on_target",
    "Zweikämpfe / gewonnen": "duels_won",
    "Zweikämpfe / gesamt": "duels_total",
    "Ballverluste / eigene Hälfte": "ball_losses",
    "Balleroberungen / gegnerische Hälfte": "recoveries_high"
}

alle_spieler = []

# Durchlaufe alle .xlsx-Dateien im Ordner
for dateipfad in glob(os.path.join(ORDNER, "*.xlsx")):
    try:
        xls = pd.ExcelFile(dateipfad)
        df = xls.parse("PlayerStats")

        # Spielername aus Dateiname extrahieren
        spielername = os.path.basename(dateipfad).replace("Player stats ", "").replace(".xlsx", "").strip()

        # Dictionary mit Spielername
        spielerdaten = {"name": spielername}

        for wyscout_spalte, ziel_spalte in RELEVANTE_SPALTEN.items():
            if wyscout_spalte in df.columns:
                wert = df[wyscout_spalte].mean()
                spielerdaten[ziel_spalte] = round(wert, 2) if pd.notna(wert) else None
            else:
                spielerdaten[ziel_spalte] = None

        alle_spieler.append(spielerdaten)

    except Exception as e:
        print(f"Fehler beim Verarbeiten von {dateipfad}: {e}")

# DataFrame erstellen und speichern
df_alle_spieler = pd.DataFrame(alle_spieler)
df_alle_spieler.to_csv(AUSGABE_DATEI, index=False)
print(f"Datei gespeichert: {AUSGABE_DATEI}")
