Pentru a rula script-ul, rulati urmatoarele comenzi in terminalul Powershell:
```powershell
# creaza un virtual environment
python -m venv venv

# activeaza viatual envronment-ul
. .\venv\Scripts\activate

# instaleaza requirements
pip install -r .\requirements.txt
```

Redenumiti .env.sample in .env si cautati keys pe:
- https://groq.com/

Scriptul se ruleaza in terminalul Powershell cu:
```powershell
python .\agent_memorie.py
```

Pentru a vedea diferenta comentati si decomentati liniile 16 si 18
