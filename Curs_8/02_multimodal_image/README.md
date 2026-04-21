# Multimodal Image — Image to Text

GOOGLE_API_KEY se gaseste in https://aistudio.google.com/ la secțiunea Api Keys

---

## Cum am creat acest proiect folosind GitHub Copilot

Mai jos sunt prompt-urile pe care le-am scris în GitHub Copilot pentru a construi agentul și aplicația web de la zero.

---

### 1. Crearea agentului cu tool

> "I want to create an agent that has a tool for searching images in the specified url path"

Primul pas a fost să definim agentul și tool-ul său. Copilot a creat:
- funcția `search_images` marcată cu `@tool` — tool-ul pe care agentul îl poate apela
- `model.bind_tools([search_images])` — leagă tool-ul de modelul AI
- `agent.invoke(...)` — agentul decide singur când și cum să folosească tool-ul

---

### 2. Folosirea LangChain pentru cod simplu

> "use langchain, instead of the Google SDK"

Am ales LangChain pentru că sintaxa sa este clară și ușor de înțeles.
Copilot a folosit `ChatGoogleGenerativeAI` și `HumanMessage` din LangChain în loc de SDK-ul raw Google.

---

### 3. Reducerea numărului de apeluri către AI

> "with as few calls as possible to the llm"

Am cerut ca agentul să descrie toate imaginile într-un singur apel în loc de unul per imagine.
Copilot a modificat codul să trimită toate imaginile deodată și să separe răspunsurile cu `---`.

---

### 4. Simplificarea codului

> "simplify the code, use functions wherever possible"

Am cerut să se reducă complexitatea liniilor lungi.
Copilot a extras funcția `image_part(url)` care ascunde encodarea base64, astfel încât `main` să rămână ușor de citit.

---

### 5. Crearea aplicației web

> "create main.py as a nice Flask interface"

Am cerut crearea interfeței web care să afișeze rezultatele agentului.
Copilot a creat aplicația Flask cu ruta `/image_to_text` care apelează agentul și afișează imaginile cu descrierile lor.

---

## Structura proiectului

```
multimodal_qa/
├── src/
│   └── image_agent.py   ← agentul AI și tool-ul său
├── app/
│   └── main.py          ← aplicația web (Flask)
├── requirements.txt
└── .env                 ← cheile secrete (creează-l tu)
```

## Pornirea aplicației

```bash
python -m venv venv
. venv/Scripts/activate
pip install -r requirements.txt
python app/main.py
```

Deschide browserul la `http://localhost:8000/image_to_text`.
</content>
