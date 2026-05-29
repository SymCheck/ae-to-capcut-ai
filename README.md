# 🎬 After Effects → CapCut AI

Ein intelligentes System, das After Effects-Edits analysiert und automatisch CapCut-Edits im gleichen Stil generiert.

## 🎯 Features

- **Effekt-Mapping**: Konvertiert After Effects Effekte zu CapCut-Äquivalenten
- **KI-Stil-Transfer**: Lernt den visuellen Stil von AE-Projekten
- **Keyframe-Animation**: Übernimmt Animationen und Timings
- **Farb-Grading**: Exportiert Farbkorrektionen und LUTs
- **Text-Animation**: Generiert Text-Effekte mit Entrance/Exit
- **Übergänge**: Mapped Transitions zwischen den Formaten
- **Batch-Processing**: Verarbeitet mehrere Projekte gleichzeitig

## 📋 Tech-Stack

- **Python 3.10+**
- **PyTorch** - Deep Learning
- **OpenCV** - Video-Frame Analyse
- **FFmpeg** - Video-Processing
- **FastAPI** - REST API
- **PostgreSQL** - Datenbank für Trainingsdaten

## 🚀 Quick Start

### Installation

```bash
# Repository klonen
git clone https://github.com/SymCheck/ae-to-capcut-ai.git
cd ae-to-capcut-ai

# Virtual Environment erstellen
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Dependencies installieren
pip install -r requirements.txt
```

### Erstes Projekt

```bash
# Training starten
python src/ai_model/train.py --data data/training_data

# Inference auf neuem AE-Projekt
python src/video_processor/capcut_generator.py --input my_ae_project.aep --output my_capcut_project.json
```

## 📁 Projekt-Struktur

```
ae-to-capcut-ai/
├── data/
│   ├── raw_ae_projects/          # After Effects Projekte (JSON-Export)
│   ├── capcut_projects/          # CapCut Projekte zum Vergleich
│   ├── training_data/            # Verarbeitete Trainingsdaten
│   └── models/                   # Trainierte ML-Modelle
├── src/
│   ├── ai_model/
│   │   ├── __init__.py
│   │   ├── train.py              # Modell trainieren
│   │   ├── model.py              # Neural Network Definition
│   │   └── inference.py          # Vorhersagen generieren
│   ├── video_processor/
│   │   ├── __init__.py
│   │   ├── ae_parser.py          # After Effects JSON parsen
│   │   ├── capcut_generator.py   # CapCut-Befehle generieren
│   │   ├── effects_mapper.py     # AE → CapCut Effekte mappen
│   │   └── keyframe_processor.py # Keyframe-Animation
│   ├── api/
│   │   ├── __init__.py
│   │   ├── server.py             # FastAPI Server
│   │   └── routes.py             # API Routes
│   └── utils/
│       ├── __init__.py
│       ├── config.py             # Konfiguration
│       ├── logger.py             # Logging
│       └── validators.py         # Validierung
├── notebooks/
│   └── exploratory_analysis.ipynb
├── tests/
│   ├── test_parser.py
│   ├── test_mapper.py
│   └── test_model.py
├── requirements.txt
├── setup.py
├── .gitignore
├── .env.example
└── docker-compose.yml
```

## 🔄 Workflow

```
After Effects Projekt
    ↓
JSON Export / AE File Parser
    ↓
Feature Extraction (Effekte, Keyframes, Timing, Farben)
    ↓
ML Model Training (PyTorch - Style Transfer)
    ↓
Pattern Recognition & Style Learning
    ↓
CapCut Format Generator
    ↓
CapCut Projekt Output
```

## 📊 Unterstützte After Effects Effekte

### Standard Effekte
- Color Correction (Curves, Levels, Hue/Saturation)
- Blur (Gaussian, Motion, Directional)
- Distortion (Warp, Lens Distortion)
- Stylize (Glow, Sharpen, Posterize)

### Text Effekte
- Opacity Animation
- Position/Scale Animation
- Rotation Animation
- Character Animation

### Übergänge
- Dissolve / Fade
- Wipe / Slide
- Zoom / Scale
- Custom Transitions

## 🧠 AI-Modell

Das System nutzt einen **Convolutional Neural Network (CNN)** + **LSTM** Stack:

1. **Feature Extractor**: Extrahiert AE-Effekt-Features
2. **Style Encoder**: Encoded den visuellen Stil
3. **CapCut Generator**: Generiert CapCut-äquivalente Effekte
4. **Validator**: Stellt sicher, dass Output in CapCut funktioniert

## 📖 API Dokumentation

```bash
# Server starten
python src/api/server.py

# Swagger UI: http://localhost:8000/docs
```

### Endpoints

```
POST /api/v1/convert - AE zu CapCut konvertieren
GET /api/v1/models - Verfügbare Modelle auflisten
POST /api/v1/train - Neues Modell trainieren
GET /api/v1/status - System-Status
```

## 🗂️ Datenformat

### Input (After Effects JSON)

```json
{
  "project": {
    "name": "My Video",
    "fps": 30,
    "duration": 120,
    "compositions": [
      {
        "name": "Main Comp",
        "layers": [
          {
            "name": "Video Layer",
            "type": "video",
            "effects": [
              {
                "name": "Curves",
                "parameters": {...}
              }
            ],
            "keyframes": [...]
          }
        ]
      }
    ]
  }
}
```

### Output (CapCut Project)

```json
{
  "project": {
    "name": "My Video",
    "fps": 30,
    "duration": 120,
    "tracks": [
      {
        "type": "video",
        "clips": [
          {
            "id": "clip_1",
            "effects": [
              {
                "type": "color_adjustment",
                "intensity": 0.8
              }
            ],
            "animations": [...]
          }
        ]
      }
    ]
  }
}
```

## 🤝 Beitragen

Contributions sind willkommen! Bitte:

1. Fork das Repository
2. Erstelle einen Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit deine Changes (`git commit -m 'Add AmazingFeature'`)
4. Push zum Branch (`git push origin feature/AmazingFeature`)
5. Öffne einen Pull Request

## 📝 Lizenz

MIT License - siehe LICENSE Datei

## 📧 Support

Für Fragen und Support: [GitHub Issues](https://github.com/SymCheck/ae-to-capcut-ai/issues)

---

**Made with ❤️ by SymCheck**
