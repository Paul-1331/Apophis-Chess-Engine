# Apophis

A chess project built with Python and Pygame.

## Requirements

- Python 3
- pip

## Installation and Setup

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd Apophis
```

### 2. Create a virtual environment

#### Linux / macOS

```bash
python3 -m venv .venv
```

#### Windows

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

#### Linux / macOS

```bash
source .venv/bin/activate
```

#### Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

#### Windows CMD

```cmd
.venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Run the project

```bash
python ChessMain.py
```

Replace `ChessMain.py` with your actual main file if it is different.

## Notes

- Always activate the virtual environment before running the project.
- If `python3` does not work on your system, try `python` instead.
- Do not upload the `.venv` folder to GitHub.

## Updating Dependencies

If you add a new package later, update the dependency file with:

```bash
pip freeze > requirements.txt
```

## Recommended `.gitignore`

Make sure your `.gitignore` contains:

```gitignore
.venv/
__pycache__/
*.pyc
```

## Project Structure

```text
Apophis/
├── main.py
├── requirements.txt
├── README.md
└── ...
```

## License

Add a license here if you want to make the project open source.