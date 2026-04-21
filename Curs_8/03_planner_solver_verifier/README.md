Instrucțiuni de folosire (în terminalul PowerShell):

```powershell
# creați un virtual environment
python -m venv venv

# activați virtual environment-ul
. .\venv\Scripts\activate

# instalați requirements
pip install -r .\requirements.txt
```

Redenumiți .env.sample în .env și adăugați cheia de Groq în fișierul .env

```powershell
# rulați script-ul
python .\planner_solver_verifier.py
```
