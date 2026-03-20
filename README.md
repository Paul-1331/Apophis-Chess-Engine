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

### 2. Create a virtual environment
Linux / macOS
python3 -m venv .venv
Windows
python -m venv .venv
### 3. Activate the virtual environment
Linux / macOS
source .venv/bin/activate
Windows PowerShell
.venv\Scripts\Activate.ps1
Windows CMD
.venv\Scripts\activate
### 4. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
### 5. Run the project
python main.py

Replace main.py with your actual main file if it is different.

Notes

Always activate the virtual environment before running the project.

If python3 does not work on your system, try python instead.

Do not upload the .venv folder to GitHub.

Updating Dependencies

If you add a new package later, update the dependency file with:

pip freeze > requirements.txt
Recommended .gitignore

Make sure your .gitignore contains:

.venv/
__pycache__/
*.pyc
Project Structure
Apophis/
├── main.py
├── requirements.txt
├── README.md
└── ...
License

Add a license here if you want to make the project open source.


And copy this entire file as your `.gitignore`:

```gitignore
.venv/
__pycache__/
*.pyc

After setting up your virtual environment and installing packages, run this once inside the project:

pip freeze > requirements.txt

Then replace:

<your-repository-url> with your actual GitHub link

main.py if your entry file has a different name