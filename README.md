# ChessInsights

ChessInsights is a full-stack chess application powered by a custom Python chess engine. The engine uses **bitboards** to efficiently generate legal moves, while a responsive web interface allows users to play games, explore positions, and review move history.

The current engine selects a random move from all valid moves in a given position. Ongoing development focuses on implementing a stronger evaluation system to enable more strategic move selection and deeper analysis.

---

## Features

* **Custom Bitboard Engine:** Implements full chess rules (castling, en passant, promotion) using optimized bitwise logic.
* **Responsive Play:** A clean, modern UI designed for both desktop and mobile browsers.
* **Stateful Sessions:** Powered by **Redis**, ensuring game states are preserved across refreshes and handled securely server-side.
* **Standardized Formats:** Full support for **FEN** (position importing) and **PGN** (move history/notation).
* **Move Navigation:** Step through your game history with a dedicated "Undo" and "Replay" system.
---

## Architecture Overview

| Layer          | Technology            | Role                                           |
| :------------- |:----------------------| :--------------------------------------------- |
| **Frontend** | HTML, CSS, JavaScript | Responsive UI, move animations, & API polling  |
| **Backend** | Python, Flask         | RESTful API & Game orchestration              |
| **Engine** | Python                | Move generation via Bitboard logic            |
| **Storage** | Redis                 | High-speed session & game state caching       |
| **Tooling** | Poetry                | Dependency management & Virtual environments |
| **Deployment** | AWS EC2 (Linux)       | Cloud infrastructure                          |

---

## Getting Started

### 1. Prerequisites

Ensure you have the following installed
* **Python 3.10+:** [Download here](https://www.python.org/downloads/)
* **Poetry:** Install via `pip install poetry`
* **Redis:** [Install locally](https://redis.io/docs/latest/get-started/)


### 2. Installation & Setup

Clone the repository and enter the directory:

```bash
git clone https://github.com/gknudtson/ChessInsights
cd ChessInsights
```
Install dependencies:

```bash
poetry install
```
---

### 3. Environment Configuration

Create a `.env` file from the provided example:

```bash
cp .env.example .env
```

Edit `.env` to match your redis credentials:

```env
# Flask secret for signing sessions
SECRET_KEY=replace-with-random-string

# Redis configuration
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=
```

### 4. Run the Application

First, ensure your Redis server is running. Then, start the Flask application:

```bash
poetry shell
python src/chess_insights/backend/api/app.py
```
The app will be available at http://127.0.0.1:5000.

---

## Testing

Unit tests are written using **Pytest** to validate core engine logic.

Run the test suite:

```bash
pytest
```

To generate a coverage report:

```bash
poetry run pytest --cov=chess_insights --cov-report=html
```

This produces an HTML coverage report that can be opened locally for detailed inspection.

---

## Roadmap

* Replace random move selection with scored move ranking
* Add analysis tools to help users improve their play
* Improve engine performance and test coverage

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
