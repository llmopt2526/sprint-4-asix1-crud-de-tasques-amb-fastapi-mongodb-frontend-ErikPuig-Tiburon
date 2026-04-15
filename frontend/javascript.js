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

// Estes dos son per al GET individual
const ID_PA_BUSCAR = document.getElementById("idTasca");
const RESULTAT_DE_LA_BUSQUEDA = document.getElementById("resultat");

let EDIT_ID
let TASQUES = [];

// Farem la funcio per despres no repetir pases
async function carregar() {
    const res = await fetch(AndroidPerroIaia);
    TASQUES = (await res.json()).tasques;
	pintar();
}

// Per aconseguir nomes un document per id
async function buscarUNA() {
    const id = ID_PA_BUSCAR.value;
    const respostaa = await fetch(AndroidPerroIaia + id);
    const dades = await respostaa.json();

    RESULTAT_DE_LA_BUSQUEDA.textContent = JSON.stringify(dades, null, 2);
}

// despres conseguirla, per si volem editarla
async function buscarUNA_i_editar() {
    const id = ID_PA_BUSCAR.value;
    const respostaa = await fetch(AndroidPerroIaia + id);
    const JSONEADO = await respostaa.json();

    editar(JSONEADO);
}

// Creacio del form, tenin en conte els valors creats al app.py
const getForm = () => ({
    titol: titol.value,
    descripcio: descripcio.value,
    estat: estat.value,
    prioritat: prioritat.value,
    categoria: categoria.value,
    persona_assignada: persona_assignada.value
});

// Y aixo es basicament per a reiniciar el formulari cada vegada que enviesem info
const resetForm = () => {
    FORMULARI_TO_GUAPO.reset();
    estat.value = "pendent";
    prioritat.value = "mitjana";
    EDIT_ID = null;
    PA_ATRAS.classList.add("ocult");
};
