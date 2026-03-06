# Control PC prin Gesturi și Voce

Aplicație desktop de control al calculatorului folosind gesturi ale mâinii recunoscute prin camera web și comenzi vocale, fără conexiune la internet. Întreaga procesare se realizează local, garantând confidențialitatea datelor.

## Descriere

Acest proiect implementează un sistem de interacțiune om-calculator (HCI) bazat pe viziune computerizată și procesare a vorbirii. Utilizatorul poate controla cursorul mouse-ului, efectua click-uri, scroll și alte acțiuni folosind gesturi ale mâinii detectate prin MediaPipe, sau poate da comenzi vocale recunoscute prin modelul Whisper (faster-whisper).

### Funcționalități principale

- **Control cursor** — mișcarea cursorului prin gestul de arătare (index ridicat)
- **Click stânga** — gest de ciupire (thumb + index)
- **Click dreapta** — palmă deschisă (4-5 degete extinse)
- **Double click** — ciupire menținută
- **Scroll** — două degete ridicate (V), mișcare sus/jos
- **Drag & Drop** — trei degete ridicate
- **Comutare desktop** — swipe lateral cu încheietura
- **Comenzi vocale** — „deschide calculator", „închide fereastra", „mărește volum", etc.
- **Dictare vocală** — mod de dictare pentru introducere de text
- **Suport bilingv** — comenzi în română și engleză

## Structura proiectului

```
├── main.py                  # Punct de intrare principal
├── config.py                # Gestionare configurări (load/save/merge)
├── settings.json            # Parametri configurabili
├── requirements.txt         # Dependențe Python
│
├── modules/                 # Module funcționale
│   ├── orchestrator.py      # Coordonator central (thread-uri, cozi)
│   ├── camera.py            # Captură video (OpenCV)
│   ├── hand_tracker.py      # Detecție mână (MediaPipe Tasks API)
│   ├── gestures.py          # Clasificare gesturi + buffer de stabilitate
│   ├── mouse_controller.py  # Control mouse (Win32 SendInput)
│   ├── keyboard_controller.py # Simulare tastatură
│   ├── window_manager.py    # Gestionare ferestre (focus, minimize, etc.)
│   ├── audio_capture.py     # Captură audio (sounddevice)
│   ├── vad.py               # Detecție activitate vocală (WebRTC VAD)
│   ├── speech_recognizer.py # Recunoaștere vocală (faster-whisper)
│   └── command_parser.py    # Parsare comenzi text → acțiuni
│
├── utils/                   # Utilități
│   ├── geometry.py          # Funcții matematice (distanțe, unghiuri, mapare ROI)
│   ├── one_euro_filter.py   # Filtru trece-jos adaptiv (1€ Filter)
│   └── smoothing.py         # Netezire cursor (backend 1€ Filter, zonă moartă)
│
├── tests/                   # Teste automate (93 teste)
│   ├── test_command_parser.py
│   ├── test_config.py
│   ├── test_geometry.py
│   ├── test_gestures.py
│   └── test_smoothing.py
│
├── assets/                  # Modele ML (descărcate automat la prima rulare)
│   └── hand_landmarker.task
│
└── build/                   # Configurare PyInstaller
    ├── build.spec
    └── build.bat
```

## Cerințe sistem

- **OS**: Windows 10/11 (64-bit)
- **Python**: 3.11+
- **Cameră web**: orice cameră compatibilă (USB sau integrată)
- **Microfon**: pentru comenzile vocale (opțional)
- **RAM**: minim 4 GB (recomandat 8 GB)

## Instalare

### 1. Clonare repository

```bash
git clone https://github.com/cata2lin/Licenta.git
cd Licenta
```

### 2. Creare mediu virtual

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Instalare dependențe

```bash
pip install -r requirements.txt
```

**Notă**: La prima rulare, modelul MediaPipe pentru detecție mână (~10 MB) se descarcă automat.

## Utilizare

### Pornire aplicație

```bash
venv\Scripts\python main.py --no-tray
```

### Opțiuni de pornire

| Parametru | Descriere |
|-----------|-----------|
| `--mode hand` | Doar control prin gesturi (fără voce) |
| `--mode voice` | Doar comenzi vocale (fără cameră) |
| `--mode combined` | Ambele moduri (implicit) |
| `--no-preview` | Fără fereastra de previzualizare |
| `--no-tray` | Fără pictograma din system tray |

### Oprire aplicație

- Apasă **Q** sau **Escape** pe fereastra de previzualizare
- **Ctrl+C** în terminal

## Ghid gesturi

| Gest | Descriere | Acțiune |
|------|-----------|---------|
| ☝️ **Arătare** | Index ridicat, restul degete strânse | Mișcare cursor |
| 🤏 **Ciupire** | Vârf thumb atinge vârf index | Click stânga |
| 🤏 **Ciupire menținută** | Menține ciupirea ~4 cadre | Double click |
| ✊ **Pumn** | Toate degetele strânse | Neutru / eliberare drag |
| 🖐️ **Palmă deschisă** | 4+ degete extinse | Click dreapta |
| ✌️ **Două degete** | Index + mijlociu (semnul V) | Scroll sus/jos |
| 🤟 **Trei degete** | Index + mijlociu + inelar | Drag & Drop |
| 👋 **Swipe stânga** | Mișcare rapidă laterală ← | Desktop anterior |
| 👋 **Swipe dreapta** | Mișcare rapidă laterală → | Desktop următor |

## Comenzi vocale (selecție)

| Comandă (RO) | Comandă (EN) | Acțiune |
|--------------|--------------|---------|
| „click stânga" | „left click" | Click stânga |
| „click dreapta" | „right click" | Click dreapta |
| „sus" / „jos" | „scroll up" / „scroll down" | Scroll |
| „deschide calculator" | „open calculator" | Lansare Calculator |
| „deschide notepad" | „open notepad" | Lansare Notepad |
| „închide fereastra" | „close window" | Închidere fereastră activă |
| „minimizează" | „minimize" | Minimizare fereastră |
| „mărește volum" | „volume up" | Volum + |
| „fără sunet" | „mute" | Mut |
| „captură de ecran" | „screenshot" | Print Screen |
| „mod dictare" | „dictation mode" | Activare dictare text |

## Arhitectură

### Pipeline-ul de procesare

```
Camera → HandTracker → GestureRecognizer → Smoother → MouseController
                                                    ↘ KeyboardController

Microfon → AudioCapture → VAD → SpeechRecognizer → CommandParser → Acțiuni
```

### Tehnologii utilizate

| Componentă | Tehnologie | Scop |
|-----------|-----------|------|
| Detecție mână | MediaPipe Tasks API | 21 de puncte de reper per mână |
| Netezire cursor | Filtru 1€ (Casiez et al., 2012) | Reducere jitter adaptivă |
| Detecție voce | WebRTC VAD | Identificare segmente de vorbire |
| Recunoaștere vocală | faster-whisper (model base) | Transcriere audio → text |
| Simulare input | Win32 SendInput (ctypes) | Control mouse/tastatură nativ |
| Interfață | pystray + OpenCV | Tray icon + previzualizare |

### Algoritmi de procesare

- **Filtrul One-Euro (1€ Filter)** — filtru trece-jos adaptiv care ajustează automat frecvența de tăiere în funcție de viteza mâinii. La viteze mici, aplică netezire agresivă (elimină tremurul). La viteze mari, permite tracking responsiv (fără lag). Parametrii sunt configurabili din `settings.json`.

- **Buffer de stabilitate** — clasificarea gesturilor trece printr-un buffer temporal care necesită N cadre consecutive cu aceeași clasificare înainte de a confirma o schimbare de gest. Previne activarea falsă din cadre cu zgomot.

- **Histereză** — praguri diferite de intrare și ieșire pentru gesturi (ex. pinch), prevenind oscilația rapidă la valorile limită.

- **Mapare ROI** — coordonatele mâinii din spațiul normalizat 0-1 sunt mapate pe ecran printr-o Regiune de Interes configurabilă, permițând utilizarea confortabilă a întregului ecran cu mișcări restrânse ale mâinii.

## Configurare

Parametrii sunt configurabili din fișierul `settings.json`. Principalele secțiuni:

- **hand_tracking** — confidențe detecție/tracking, parametri ROI, parametri filtru 1€
- **gestures** — praguri pinch, cadre stabilitate, cooldown click-uri
- **voice** — model Whisper, limba, agresivitate VAD
- **app** — mod implicit, previzualizare, nivel de logging

## Teste

```bash
venv\Scripts\python -m pytest tests/ -v
```

Suita de teste conține 93 de teste automate care acoperă:
- Parsarea comenzilor vocale (36 teste, RO + EN)
- Încărcare/salvare configurări (14 teste)
- Funcții geometrice și mapare ROI (15 teste)
- Clasificare gesturi și buffer de stabilitate (20 teste)
- Filtrul 1€ și netezire cursor (8 teste)

## Compilare executabil

```bash
cd build
build.bat
```

Se generează un executabil standalone în `build/dist/` care nu necesită Python instalat.

## Referințe

- MediaPipe Hand Landmarker: https://developers.google.com/mediapipe/solutions/vision/hand_landmarker
- Casiez, G., Roussel, N., Vogel, D. (2012). „1€ Filter: A Simple Speed-Based Low-Pass Filter for Noisy Input in Interactive Systems". CHI '12.
- faster-whisper: https://github.com/SYSTRAN/faster-whisper
- WebRTC VAD: https://webrtc.org/
