# ChessPlayer: AI-Powered Computer Vision Chess Assistant

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An intelligent chess assistant that leverages **Computer Vision** and **Deep Learning** to synchronize physical or digital chess boards with the **Stockfish** engine. The application captures the board state through image processing and provides real-time move suggestions.

*This project was developed for a college-level competition, focusing on the practical application of AI and CV in gaming.*

---

## 🚀 Key Features

- **Automated Board Detection:** Real-time extraction of chess board grids using optimized OpenCV pipelines.
- **Deep Learning Piece Recognition:** Custom CNN model trained to classify chess pieces with high precision.
- **Engine-Driven Analysis:** Integrated with the Stockfish engine for top-tier move recommendations.
- **Interactive UI:** A feature-rich PyQt5 dashboard for board configuration, move visualization, and settings management.
- **Hybrid Support:** Works with both physical board captures and screen-based digital chess.

## 🛠️ Technology Stack

- **Core:** Python 3.x
- **Computer Vision:** OpenCV, Scikit-image
- **Artificial Intelligence:** TensorFlow/Keras (CNN)
- **GUI Framework:** PyQt5
- **Backend Logic:** `python-chess` for game state and move validation
- **Automation:** `PyAutoGUI` for seamless screen interaction

## 📋 Installation & Setup

### Prerequisites
- Python 3.7 or higher
- [Stockfish Engine](https://stockfishchess.org/download/) (Binary required)

### Steps
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/dyaa-adel/ChessPlayer.git
   cd ChessPlayer
   ```

2. **Initialize Virtual Environment:**
   ```bash
   python -m venv .venv
   # Activate on Windows:
   .venv\Scripts\activate
   # Activate on Linux/macOS:
   source .venv/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install .
   ```

4. **Configure Stockfish:**
   - Download the Stockfish binary.
   - Upon launching ChessPlayer, navigate to settings and point the "Engine Path" to your Stockfish executable (e.g., `stockfish_20011801_x64.exe`).

## 🎮 Usage

Launch the application using the entry point:
```bash
chess-player
```

### Key Shortcuts (Manual Calibration)
| Piece | White | Black |
| :--- | :---: | :---: |
| **Rook** | `r` | `Shift + r` |
| **Knight** | `n` | `Shift + n` |
| **Bishop** | `b` | `Shift + b` |
| **Queen** | `q` | `Shift + q` |
| **King** | `k` | `Shift + k` |
| **Pawn** | `p` | `Shift + p` |
| **Action** | **Key** | |
| Remove Piece | `Backspace` | |

## 📺 Project Demo
Watch the application in action: [YouTube Video Link](https://youtu.be/krWVJiINemk)

## 👥 Contributors
- **Dyaa Adel** ([@dyaa-adel](https://github.com/dyaa-adel))
- **Abdullah Emad**
- **Abdulrahman Mamdouh**

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
*Icons provided by ultimatearm from Flaticon.*
