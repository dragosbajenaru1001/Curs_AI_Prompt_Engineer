import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from flask import Flask, render_template_string
from image_agent import main as run_agent

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Image to Text</title>
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      font-family: 'Segoe UI', system-ui, sans-serif;
      background: #0f1117;
      color: #e2e8f0;
      min-height: 100vh;
      padding: 2rem;
    }

    h1 {
      text-align: center;
      font-size: 2rem;
      font-weight: 700;
      margin-bottom: 2.5rem;
      background: linear-gradient(135deg, #7c3aed, #3b82f6);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }

    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(420px, 1fr));
      gap: 1.5rem;
      max-width: 1400px;
      margin: 0 auto;
    }

    .card {
      background: #1e2130;
      border: 1px solid #2d3148;
      border-radius: 1rem;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      transition: transform 0.2s, box-shadow 0.2s;
    }

    .card:hover {
      transform: translateY(-4px);
      box-shadow: 0 12px 40px rgba(124, 58, 237, 0.2);
    }

    .card img {
      width: 100%;
      aspect-ratio: 16 / 9;
      object-fit: cover;
    }

    .card-body {
      padding: 1.25rem 1.5rem 1.5rem;
      flex: 1;
    }

    .card-body p {
      line-height: 1.7;
      font-size: 0.95rem;
      color: #cbd5e1;
    }

    .tag {
      display: inline-block;
      background: #7c3aed22;
      color: #a78bfa;
      border: 1px solid #7c3aed55;
      border-radius: 999px;
      font-size: 0.75rem;
      font-weight: 600;
      padding: 0.2rem 0.75rem;
      margin-bottom: 0.75rem;
    }

    .error {
      text-align: center;
      color: #f87171;
      margin-top: 4rem;
      font-size: 1.1rem;
    }
  </style>
</head>
<body>
  <h1>Image to Text</h1>
  {% if results %}
    <div class="grid">
      {% for item in results %}
        <div class="card">
          <img src="{{ item.image }}" alt="Image" loading="lazy">
          <div class="card-body">
            <span class="tag">Analysis</span>
            {% for line in item.text.splitlines() %}
              {% if line.strip() %}
                <p>{{ line.replace('*', '') }}</p>
              {% endif %}
            {% endfor %}
          </div>
        </div>
      {% endfor %}
    </div>
  {% else %}
    <p class="error">No results returned.</p>
  {% endif %}
</body>
</html>
"""

@app.get("/image_to_text")
def image_to_text():
    return render_template_string(HTML, results=run_agent())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
