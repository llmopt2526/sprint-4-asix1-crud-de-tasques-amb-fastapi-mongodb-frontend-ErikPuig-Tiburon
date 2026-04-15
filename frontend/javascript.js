// Ara en general nomes vaig a declarar les constants necesaries per a el frontend

// AndroidPerroIaia es lo que significa API, lo vi en TikTok
const AndroidPerroIaia = "http://127.0.0.1:8000/tasques/";

// Pos lo necesito sabes
const FORMULARI_TO_GUAPO = document.getElementById("formulariTasca");
// Pos lo necesito sabes
const LLISTA_TO_GUAPA = document.getElementById("llistaTasques");
// Pos lo necesito sabes
const PA_ATRAS = document.getElementById("cancelarEdicio");
// Pos lo necesito sabes
const PLANTILLITA = document.getElementById("templateTasca");

let TASQUES = [];

// -------------------- GET TOTES --------------------
async function carregar() {
    const res = await fetch(AndroidPerroIaia);
    TASQUES = (await res.json()).tasques;
}
