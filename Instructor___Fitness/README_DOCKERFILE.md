Pentru a genera Dockerfile folositi GitHub Copilot cu prompt-urile:

Prompt 1 — imagine de bază mică:
Genereaza Dockerfile pentru aplicația instructor_fitness folosind o imagine cât mai mică

Prompt 2 — multi-stage build:
Folosește 2 etape de construire a imaginii: una pentru a extrage ce este esențial 
din imagine (builder) și a doua pentru a rula imaginea

Prompt 3 — dependințe din requirements-prod.txt:
În etapa builder, instalează dependințele din requirements-prod.txt ca wheels, 
apoi în etapa finală instalează-le fără conexiune la internet folosind --no-index

Prompt 4 — variabile de mediu și volume:
Adaugă variabilele de mediu TFHUB_CACHE_DIR și FITNESS_DATA_DIR, 
creează directoarele necesare și definește VOLUME pentru /app/models și /app/data

Prompt 5 — preîncărcare model TensorFlow Hub:
Adaugă un pas RUN care preîncarcă modelul universal-sentence-encoder/4 
din TensorFlow Hub la build time

Prompt 6 — comandă de start:
Expune portul 80 și setează CMD pentru a rula gradio_app/app.py cu python