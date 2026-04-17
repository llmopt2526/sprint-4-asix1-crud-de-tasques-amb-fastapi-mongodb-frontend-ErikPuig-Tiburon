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

// Esta funcio es la del POST, o siga crear una tasca nova
const crear = async () => {
    await fetch(AndroidPerroIaia, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(getForm())
    });
    resetForm();
    carregar();
};

// Esta funcio es la del PUT, o siga actualitzar una tasca que ja existeix
const actualitzar = async (id) => {
    await fetch(AndroidPerroIaia + id, {
        method: "PUT",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(getForm())
    });
    resetForm();
    carregar();
};

// Esta es la de eliminar, que li passa la id a la API i la borra
const eliminar = async (id) => {
    await fetch(AndroidPerroIaia + id, {
        method: "DELETE"
    });
    carregar();
};

// Esta funcio ompli el formulari en les dades de la tasca per poder editarla
function editar(t) {
    EDIT_ID = t.id || t._id;

    titol.value = t.titol;
    descripcio.value = t.descripcio;
    estat.value = t.estat;
    prioritat.value = t.prioritat;
    categoria.value = t.categoria;
    persona_assignada.value = t.persona_assignada;

    PA_ATRAS.classList.remove("ocult");
}

// Esta funcio canvia l'estat de la tasca, si esta feta la posa pendent i al reves
const toggleEstat = async (t) => {
    await fetch(AndroidPerroIaia + (t.id || t._id), {
        method: "PUT",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            ...t,
            estat: t.estat === "feta" ? "pendent" : "feta"
        })
    });
    carregar();
};

// Aixo es lo de dalt del tot que diu quantes tasques hi han
COMPTADOR_TASQUES.textContent = TASQUES.length === 1 ? "1 tasca" : `${TASQUES.length} tasques`;

// Esta es la funcio important que pinta totes les targetes al llistat i els posa els colors i els botons
function pintar() {
    LLISTA_TO_GUAPA.innerHTML = "";

    // Aci actualitzem tambe el contador perque vaja canviant cada vegada
    COMPTADOR_TASQUES.textContent = `${TASQUES.length} tasques`;

    TASQUES.forEach(t => {
        // Clonem la plantilla del HTML per no escriure el codi a saco en JS
        const node = PLANTILLITA.content.cloneNode(true);

        // Aci fiquem les dades que venen de la API dins de cada targeta
        node.querySelector(".tasca-id").textContent = t.id || t._id;
        node.querySelector(".tasca-titol").textContent = t.titol;
        node.querySelector(".tasca-descripcio").textContent = t.descripcio;
        node.querySelector(".tasca-prioritat").textContent = t.prioritat;
        node.querySelector(".tasca-categoria").textContent = t.categoria;
        node.querySelector(".tasca-persona").textContent = t.persona_assignada;

        // Aci li posem el text del estat i la classe per al color
        const estatEl = node.querySelector(".tasca-estat");
        estatEl.textContent = t.estat;
        estatEl.classList.add(t.estat === "feta" ? "estat-feta" : "estat-pendent");

        // Estos son els events dels botons de cada targeta
        node.querySelector(".boto-editar").onclick = () => editar(t);
        node.querySelector(".boto-estat").onclick = () => toggleEstat(t);
        node.querySelector(".boto-eliminar").onclick = () => eliminar(t.id || t._id);

        // I finalment afegim la targeta al contenidor gran del llistat
        LLISTA_TO_GUAPA.appendChild(node);
    });
}

// Aci fem que quan envies el formulari, si estas editant actualitze, i si no cree
FORMULARI_TO_GUAPO.onsubmit = (e) => {
    e.preventDefault();
    EDIT_ID ? actualitzar(EDIT_ID) : crear();
};

// Este boto es per cancelar l'edicio i deixar el formulari net
PA_ATRAS.onclick = resetForm;

// I al final carreguem totes les tasques nomes entrar a la pagina
carregar();

