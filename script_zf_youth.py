import pandas as pd
import os
from glob import glob

# Pfad zu deinen Jugendspielern
ORDNER = "/Users/fabianfacalbiemmi/Desktop/AI_Applications/youth_wyscout"
AUSGABE_DATEI = "youth_players_final.csv"

alle_spieler = []

for dateipfad in glob(os.path.join(ORDNER, "*.xlsx")):
    if os.path.basename(dateipfad).startswith("~$"):
        continue  # Temporäre Excel-Dateien ignorieren

    try:
        xls = pd.ExcelFile(dateipfad)
        df = xls.parse("PlayerStats")

        spielername = os.path.basename(dateipfad).replace("Player stats ", "").replace(".xlsx", "").strip()
        spielerdaten = {"name": spielername}

        def add_spalte(spalte, ziel):
            if spalte in df.columns:
                spielerdaten[ziel] = df[spalte].mean()

        # Grunddaten
        add_spalte("Gespielte Minuten", "minutes_played")
        add_spalte("Tore", "goals")
        add_spalte("Vorlage", "assists")

        # Schüsse
        if "Schüsse / aus Tor" in df.columns:
            col = df.columns.get_loc("Schüsse / aus Tor")
            shots_total = df.iloc[:, col].dropna()
            shots_on_target = df.iloc[:, col + 1].dropna()
            if not shots_total.empty and not shots_on_target.empty:
                spielerdaten["shots_total"] = shots_total.mean()
                spielerdaten["shots_on_target"] = shots_on_target.mean()

        # Pässe
        passes_total, passes_success = None, None
        if "Pässe / genau" in df.columns:
            col = df.columns.get_loc("Pässe / genau")
            p_total = df.iloc[:, col].dropna()
            p_success = df.iloc[:, col + 1].dropna()
            if not p_total.empty and not p_success.empty:
                passes_total = p_total.mean()
                passes_success = p_success.mean()

        if "Langpässe / genau" in df.columns:
            col = df.columns.get_loc("Langpässe / genau")
            l_total = df.iloc[:, col].dropna()
            l_success = df.iloc[:, col + 1].dropna()
            if not l_total.empty and not l_success.empty:
                passes_total = (passes_total or 0) + l_total.mean()
                passes_success = (passes_success or 0) + l_success.mean()

        if passes_total is not None and passes_success is not None:
            spielerdaten["passes_total"] = passes_total
            spielerdaten["passes_success"] = passes_success

        # Zweikämpfe
        if "Zweikämpfe / gewonnen" in df.columns and "Unnamed: 21" in df.columns:
            gewonnen = df["Zweikämpfe / gewonnen"].fillna(0)
            rest = df["Unnamed: 21"].fillna(0)
            spielerdaten["duels_won"] = gewonnen.mean()
            spielerdaten["duels_total"] = (gewonnen + rest).mean()

        # Ballverluste
        if "Ballverluste / eigene Hälfte" in df.columns and "Unnamed: 26" in df.columns:
            verluste = df["Ballverluste / eigene Hälfte"].fillna(0) + df["Unnamed: 26"].fillna(0)
            spielerdaten["ball_losses"] = verluste.mean()

        # Balleroberungen
        if "Balleroberungen / gegnerische Hälfte" in df.columns and "Unnamed: 28" in df.columns:
            recoveries = df["Balleroberungen / gegnerische Hälfte"].fillna(0) + df["Unnamed: 28"].fillna(0)
            spielerdaten["recoveries"] = recoveries.mean()

        # Zielwert hinzufügen
        spielerdaten["is_pro"] = 0  # Jugendspieler = keine Profis

        alle_spieler.append(spielerdaten)

    except Exception as e:
        print(f"❌ Fehler bei Datei {dateipfad}: {e}")

# DataFrame erzeugen
df_youth = pd.DataFrame(alle_spieler)

# Auf 2 Nachkommastellen runden
for col in df_youth.select_dtypes(include="number").columns:
    df_youth[col] = df_youth[col].round(2)

# CSV speichern
df_youth.to_csv(AUSGABE_DATEI, index=False)
print(f"✅ Jugendspieler gespeichert als: {AUSGABE_DATEI}")
