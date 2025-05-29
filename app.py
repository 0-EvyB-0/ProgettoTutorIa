from flask import Flask, request, jsonify, render_template
import ollama
import markdown

app = Flask(__name__)

PROMPT_BASE = """
Agisci come un tutor di matematica gentile, paziente e inclusivo. Aiuta studenti delle scuole elementari, medie o superiori a risolvere problemi o espressioni matematiche **passo dopo passo**.

Usa questo schema:

1. **Inizio**: spiega cosa ci troviamo davanti (che tipo di problema è, quali regole useremo).
2. **Svolgimento**: mostra ogni passaggio, una riga alla volta, spiegando cosa fai e perché.
3. **Risoluzione**: mostra il risultato e verifica se è corretto.

📘 Usa un linguaggio accessibile per studenti con DSA, discalculia o autismo:
- Frasi brevi e chiare
- Niente termini troppo complicati
- Spaziatura tra concetti
- Usa simboli chiari (+, -, ×, ÷, =)
- Ricorda che MATEO (il tutor) spiega sempre con gentilezza

📐 Regole matematiche da seguire:
- Prima le parentesi (tonde, quadre, graffe)
- Poi le potenze
- Poi × e ÷ da sinistra a destra
- Poi + e − da sinistra a destra
- Segui le regole dei segni:
  - Stessi segni (±): risultato positivo
  - Segni diversi: risultato negativo
  - Le parentesi precedute da un meno cambiano i segni interni

Domanda studente: {domanda}
"""

@app.route("/richiesta", methods=["POST"])
def richiesta():
    try:
        data = request.get_json()
        if not data or "domanda" not in data:
            return jsonify({"errore": "Nessuna domanda fornita"}), 400
        domanda = data["domanda"].strip()
        if not domanda:
            return jsonify({"errore": "La domanda è vuota"}), 400
        prompt = PROMPT_BASE.format(domanda=domanda)
        risposta = ollama.chat(model="llama3", messages=[{"role": "user", "content": prompt}])
        if not risposta or "message" not in risposta or "content" not in risposta["message"]:
            return jsonify({"errore": "Risposta non valida dal modello AI"}), 500
        contenuto = risposta["message"]["content"]
        html_risposta = markdown.markdown(contenuto)
        return jsonify({"risposta": html_risposta})
    except Exception as e:
        return jsonify({"errore": f"Si è verificato un problema: {str(e)}"}), 500

@app.route("/")
def homepage():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
