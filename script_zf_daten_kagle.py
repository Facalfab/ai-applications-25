import pandas as pd
import os
from glob import glob

# Pfad zum Ordner mit den Kaggle-Dateien
ORDNER = "/Users/fabianfacalbiemmi/Desktop/AI_Applications/Pro_kagle"
AUSGABE_DATEI = "kaggle_players_final.csv"

# Spaltenmapping: Kaggle → Zielstruktur wie bei wyscout
SPALTEN_MAPPING = {
    "Player": "name",
    "Min": "minutes_played",
    "Gls": "goals",
    "Ast": "assists",
    "PasTotCmp": "passes_success",
    "PasTotAtt": "passes_total",
    "SoT": "shots_on_target",
    "TklWon": "duels_won",
    "Tkl": "duels_total",
    "Dispossessed": "ball_losses",
    "Recov": "recoveries"
}

# Zielstruktur (Spaltenreihenfolge wie bei Wyscout)
ZIEL_SPALTEN = [
    "name", "minutes_played", "goals", "assists",
    "passes_total", "passes_success",
    "shots_total", "shots_on_target",
    "duels_total", "duels_won",
    "ball_losses", "recoveries"
]

alle_spieler = []

# Alle CSVs im Ordner durchgehen
for dateipfad in glob(os.path.join(ORDNER, "*.csv")):
    try:
        df = pd.read_csv(dateipfad, sep=";", encoding="ISO-8859-1", engine="python")

        # Nur relevante Spalten behalten und umbenennen
        neue_spalten = {}
        for orig_spalte, ziel_spalte in SPALTEN_MAPPING.items():
            if orig_spalte in df.columns:
                neue_spalten[orig_spalte] = ziel_spalte

        df_auszug = df[list(neue_spalten.keys())].rename(columns=neue_spalten)

        # Fehlende Zielspalten ergänzen mit None
        for ziel in ZIEL_SPALTEN:
            if ziel not in df_auszug.columns:
                df_auszug[ziel] = None

        # Spaltenreihenfolge anpassen
        df_auszug = df_auszug[ZIEL_SPALTEN]

        # Rundung der numerischen Spalten auf 2 Nachkommastellen
        for col in df_auszug.select_dtypes(include="number").columns:
            df_auszug[col] = df_auszug[col].round(2)

        alle_spieler.append(df_auszug)

    except Exception as e:
        print(f"Fehler bei Datei {dateipfad}: {e}")

# Kombiniere alle zu einem DataFrame
df_alle_profis = pd.concat(alle_spieler, ignore_index=True)

# Speichere als CSV
df_alle_profis.to_csv(AUSGABE_DATEI, index=False)
print(f"Datei gespeichert: {AUSGABE_DATEI}")
