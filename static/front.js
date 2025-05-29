async function inviaRichiesta() {
    const input = document.getElementById("user-input").value.trim();
    const output = document.getElementById("risposta-ia");
    const fumetto = document.getElementById("fumetto");

    if (!input) {
        output.innerHTML = "Inserisci una domanda prima di inviare! 🚀";
        fumetto.textContent = "Per favore, scrivi qualcosa da risolvere insieme!";
        return;
    }

    output.innerHTML = "Sto pensando... 🤔";
    fumetto.textContent = "Un attimo, sto ragionando! 🧠";

    try {
        const res = await fetch("/richiesta", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ domanda: input })
        });

        if (!res.ok) throw new Error(`Errore HTTP: ${res.status}`);

        const data = await res.json();
        output.innerHTML = `<strong>Risposta IA:</strong><br>${data.risposta}`;
        fumetto.textContent = "Ecco come possiamo risolverlo insieme! ✨";

    } catch (error) {
        output.innerHTML = `Errore nella comunicazione con il server 😥<br><small>${error.message}</small>`;
        fumetto.textContent = "Oops! C'è stato un errore 😢";
    }
}
document.getElementById("send-btn").addEventListener("click", inviaRichiesta);
