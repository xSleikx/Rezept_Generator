# 🍳 Rezept-Anleitung Generator mit Audio-Erklärungen

Dieses Tool erstellt automatisch Schritt-für-Schritt-Rezepte aus Zutaten und Video-Transkripten – und erklärt jeden Schritt auf Englisch mit Audio! Perfekt für alle, die beim Kochen Unterstützung brauchen oder einfach Spaß am Experimentieren haben. 😄

---

## ✨ Features

- 📝 **Rezept automatisch erstellen:** Basierend auf Zutatenliste und Video-Transkript.
- 🎧 **Schritte auf Englisch erklären:** Mit Text und Audio.
- 🔊 **Audio-Generierung:** Hört sich wie ein persönlicher Kochassistent an (via [Kokoro](https://github.com/hexgrad/kokoro)).
- 🖥️ **Gradio-Interface:** Einfach, interaktiv und benutzerfreundlich.
  - Tab 1: **Rezept erstellen**
  - Tab 2: **Schritt erklären & Audio hören (Englisch)**

---

## 🚀 Installation

Abhängigkeiten installieren:
```bash
pip install -r requirements.txt
```

API-Key einrichten:
- Erstelle eine `.env` Datei im Projektordner:
```env
GROQ_API_KEY ='your_groq_api_key_here'
```
- Verwendet das Groq-Modell als Agent über [Pydantic AI](https://ai.pydantic.dev/).
---

## 🎯 Nutzung

### 0️⃣ YouTube-Transkript und Zutaten kopieren
1. Öffne das gewünschte Koch YouTube-Video.
2. Klicke auf die drei Punkte unter dem Video → **Transkript öffnen**.
3. Kopiere den Text in eine `.txt` Datei (z. B. `transkript.txt`) oder direkt ins Textfeld vom Generator.
💡 **Hinweis:** Manche Videos haben kein Transkript. Meistens sind die Zutaten in der Beschreibung.

### 1️⃣ Rezept erstellen
1. Gradio starten:
```bash
python app.py
```
2. Zutaten und Video-Transkript eingeben.
3. **Rezept Erstellen** klicken.
4. Optional: **Clear** Button, um alle Felder zurückzusetzen.

### 2️⃣ Schritt erklären
1. Zum Tab „Schritt erklären auf Englisch (mit Audio)“ wechseln.
2. Schritt-Nummer auswählen und optional eine Frage zu diesem Schritt stellen.
3. **Erklären** klicken → Text + Audio werden angezeigt.
4. **Rezept anzeigen** lädt die aktuelle Rezeptanleitung, falls sie noch nicht sichtbar ist.

💡 **Tipp:** Du kannst mehrere Schritte hintereinander abspielen, um eine Mini-Kochstunde zu haben!  

---

## 📁 Projektstruktur

```
.
├── app.py            # Gradio-Interface und Logik
├── load_models.py     # Lädt den KI-Agenten (GroqModel)
├── zutaten.txt        # Beispiel-Zutaten
├── transkript.txt     # Beispiel-Video-Transkript
├── kokoro_audio.py    # Kokoro Audio-Generierung
├── requirements.txt   # Python-Abhängigkeiten
└── README.md
```

---


## ⚠️ Hinweise

- Audio-Erklärungen sind aktuell **nur auf Englisch**.
- Schritt-Nummer muss innerhalb der erzeugten Rezeptanleitung liegen.
- Du kannst die Beispiel-Dateien `zutaten.txt` und `transkript.txt` löschen und eigene Inhalte einfügen.
- Maximal **10 Schritte empfohlen**, um die Anleitung übersichtlich zu halten. Agent kann nach belieben angepasst werden. 

---

## 📜 Lizenz

MIT License

---

## 🖤 Danke

Viel Spaß beim Kochen! 😋🍽️

