let paso = 1
let seleccion = {}
let periodoSeleccionado = null
let tipoDoc = null
let limite = 0
let seleccionadas = [] // Guardará objetos {ofa_id, carrera, bloque, sede, modalidad, jornada}
let permiteMultiCampos = true;
let camposSeleccionados = new Set(); // Rastrea los nombres de los bloques (Campos de Conocimiento)

const user = JSON.parse(localStorage.getItem("user"))

if(!user){
 window.location="login.html"
}

// ===================== UI =====================

function activar(n){
 document.querySelectorAll(".steps span")
 .forEach(s=>s.classList.remove("active"))
 document.getElementById("p"+n).classList.add("active")
}

// ===================== PASO 1 =====================

function cargarPaso1() {
    activar(1);

    fetch("http://127.0.0.1:8000/inscripcion/datos/" + user.cedula)
    .then(r => r.json())
    .then(d => {
        // Mapeo manual para controlar el orden y las etiquetas exactas de la imagen
        const camposVisuales = [
            { id: 'identificacion', label: 'CÉDULA' },
            { id: 'nombres', label: 'NOMBRES' },
            { id: 'apellidos', label: 'APELLIDOS' },
            { id: 'nacionalidad', label: 'NACIONALIDAD' },
            { id: 'fechanacimiento', label: 'FECHA NAC.' },
            { id: 'genero', label: 'GÉNERO' },
            // Puedes añadir aquí 'correo', 'nota', etc., si tu API los devuelve
        ];

        // Si quieres incluir todos tus datos originales pero con este formato:
        const todosMisCampos = [
            { id: 'tipodocumento', label: 'TIPO DOCUMENTO' },
            { id: 'identificacion', label: 'IDENTIFICACIÓN' },
            { id: 'nombres', label: 'NOMBRES' },
            { id: 'apellidos', label: 'APELLIDOS' },
            { id: 'nacionalidad', label: 'NACIONALIDAD' },
            { id: 'fechanacimiento', label: 'FECHA NACIMIENTO' },
            { id: 'estadocivil', label: 'ESTADO CIVIL' },
            { id: 'sexo', label: 'SEXO' },
            { id: 'genero', label: 'GÉNERO' },
            { id: 'autoidentificacion', label: 'AUTOIDENTIFICACIÓN' }
        ];

        const contenidoHTML = todosMisCampos.map(campo => {
            const valor = d[campo.id] !== undefined ? d[campo.id] : "No disponible";
            return `
                <div class="fila-dato">
                    <span class="dato-etiqueta">${campo.label}</span>
                    <span class="dato-valor">${valor}</span>
                </div>
            `;
        }).join("");

        document.getElementById("contenido").innerHTML = `
            <div class="box">
                <h3 style="border-bottom: 2px solid #3b82f6; display: inline-block; padding-bottom: 5px;">
                    Datos del Registro Nacional
                </h3>
                
                <div class="tabla-datos">
                    ${contenidoHTML}
                </div>

                <p style="font-size: 0.8rem; color: #94a3b8; margin-top: 15px;">
                    * Verifique que sus datos sean correctos.
                </p>

                <div class="footer-paso1">
                    <button class="btn-salir" onclick="window.location='dashboard.html'">
                        Cancelar / Salir
                    </button>
                    <button class="btn-siguiente-blue" onclick="cargarPaso2()">
                        Siguiente
                    </button>
                </div>
            </div>
        `;
    });
}

// ===================== PASO 2 =====================

// Variable global para almacenar las ofertas y permitir filtrado rápido
let ofertasGlobales = {}; 

async function cargarPaso2() {
    activar(2);
    try {
        const resCfg = await fetch("http://127.0.0.1:8000/inscripcion/config-multi-campos").then(r => r.json());
        ofertasGlobales = await fetch("http://127.0.0.1:8000/inscripcion/ofertas-agrupadas").then(r => r.json());

        permiteMultiCampos = resCfg.permitir;

        document.getElementById("contenido").innerHTML = `
          <div class="box">
            <h3>Selección de carreras</h3>
        
            <div class="search-box">
                <input type="text" id="buscador" 
                       placeholder="Escribe el nombre de la carrera..." 
                       onkeyup="filtrarAcordeon()">
            </div>

            <div class="panel">
                <span class="badge" id="contador">${seleccionadas.length}/${limite} seleccionadas</span>
            </div>
            <div id="acordeon-conocimiento"></div>
                <h4>Seleccionadas</h4>
                <ul id="listaSel"></ul>
                <div class="actions">
                    <button class="btn" onclick="cargarPaso1()">Atrás</button>
                    <button class="btn" onclick="cargarPaso3()">Siguiente</button>
                </div>
            </div>`;

        renderAcordeon(ofertasGlobales);
        actualizarLista();
    } catch (error) {
        console.error("Error cargando ofertas:", error);
    }
}
function filtrarAcordeon() {
    let input = document.getElementById("buscador");
    if (!input) return;
    
    let txt = input.value.toLowerCase();
    // Seleccionamos los bloques (los <details>)
    const bloques = document.querySelectorAll(".bloque-moderno");

    bloques.forEach(bloque => {
        let tieneCoincidencia = false;
        // Seleccionamos las tarjetas nuevas
        const tarjetas = bloque.querySelectorAll(".tarjeta-carrera-nueva");

        tarjetas.forEach(tarjeta => {
            // Obtenemos el nombre desde el atributo data-nombre que pusimos en renderAcordeon
            const nombreCarrera = tarjeta.getAttribute("data-nombre") || "";
            
            if (nombreCarrera.includes(txt)) {
                tarjeta.style.display = "flex"; 
                tieneCoincidencia = true;
            } else {
                tarjeta.style.display = "none";
            }
        });

        // Si hay texto, manejamos la visibilidad del bloque completo
        if (txt.length > 0) {
            if (tieneCoincidencia) {
                bloque.style.display = "block";
                bloque.open = true; // Abre automáticamente para mostrar resultados
            } else {
                bloque.style.display = "none"; // Oculta bloques sin resultados
            }
        } else {
            // Si el buscador está vacío, mostramos todos los bloques y los cerramos
            bloque.style.display = "block";
            bloque.open = false;
            tarjetas.forEach(t => t.style.display = "flex");
        }
    });
}

function renderAcordeon(data) {
    const container = document.getElementById("acordeon-conocimiento");
    container.innerHTML = "";

    for (const [bloque, carreras] of Object.entries(data)) {
        let details = document.createElement("details");
        details.className = "bloque-moderno";
        
        let htmlCarreras = Object.entries(carreras).map(([nombre, opciones]) => {
            const idSafe = nombre.replace(/\s+/g, '_');
            const sedesUnicas = [...new Set(opciones.map(o => o.sede))];

            // IMPORTANTE: Se añade data-nombre para que el buscador lo encuentre
            return `
                <div class="tarjeta-carrera-nueva" data-nombre="${nombre.toLowerCase()}">
                    <div class="info-principal">
                        <span class="carrera-titulo">${nombre}</span>
                    </div>
                    <div class="seleccion-multiple">
                        <select id="sede_${idSafe}" class="select-mini" onchange="actualizarFiltros('${nombre}')">
                            ${sedesUnicas.map(s => `<option value="${s}">${s}</option>`).join('')}
                        </select>
                        <select id="mod_${idSafe}" class="select-mini" onchange="actualizarFiltros('${nombre}')"></select>
                        <select id="jor_${idSafe}" class="select-mini"></select>
                    </div>
                    <button class="btn-agregar-estilo" onclick="ejecutarSeleccion('${nombre}', '${bloque}')">
                        Elegir
                    </button>
                </div>`;
        }).join("");

        details.innerHTML = `<summary class="summary-estilo">▶ <b>${bloque}</b></summary>
                             <div class="carreras-grid">${htmlCarreras}</div>`;
        container.appendChild(details);
        
        Object.keys(carreras).forEach(n => actualizarFiltros(n));
    }
}

function actualizarFiltros(nombreCarrera) {
    const idSafe = nombreCarrera.replace(/\s+/g, '_');
    const sedeSel = document.getElementById(`sede_${idSafe}`).value;
    
    // Buscar las opciones de esta carrera en el objeto global
    let opcionesCarrera = [];
    for (let b in ofertasGlobales) {
        if (ofertasGlobales[b][nombreCarrera]) {
            opcionesCarrera = ofertasGlobales[b][nombreCarrera];
            break;
        }
    }

    // 1. Filtrar y actualizar Modalidades basadas en la Sede
    const opcionesDeSede = opcionesCarrera.filter(o => o.sede === sedeSel);
    const modsUnicas = [...new Set(opcionesDeSede.map(o => o.modalidad))];
    const selectMod = document.getElementById(`mod_${idSafe}`);
    
    // Guardamos el valor previo para intentar mantenerlo si existe en la nueva sede
    const valorPrevioMod = selectMod.value;
    selectMod.innerHTML = modsUnicas.map(m => `<option value="${m}">${m}</option>`).join('');
    if (modsUnicas.includes(valorPrevioMod)) selectMod.value = valorPrevioMod;

    // 2. Filtrar y actualizar Jornadas basadas en Sede + Modalidad
    const modSel = selectMod.value;
    const opcionesFinales = opcionesDeSede.filter(o => o.modalidad === modSel);
    const selectJor = document.getElementById(`jor_${idSafe}`);
    
    selectJor.innerHTML = opcionesFinales.map(o => 
        `<option value="${o.jornada_id}">${o.jornada_texto}</option>`
    ).join('');
}

function ejecutarSeleccion(nombreCarrera, bloque) {
    const idSafe = nombreCarrera.replace(/\s+/g, '_');
    const sede = document.getElementById(`sede_${idSafe}`).value;
    const mod = document.getElementById(`mod_${idSafe}`).value;
    const jorId = document.getElementById(`jor_${idSafe}`).value;
    const jorTexto = document.getElementById(`jor_${idSafe}`).options[document.getElementById(`jor_${idSafe}`).selectedIndex].text;

    // Buscamos el ofa_id que coincida exactamente con lo seleccionado
    const match = ofertasGlobales[bloque][nombreCarrera].find(o => 
        o.sede === sede && o.modalidad === mod && o.jornada_id == jorId
    );

    if (match) {
        intentarAgregar(match.ofa_id, nombreCarrera, bloque, sede, mod, jorTexto);
    }
}

// Función intermedia para extraer los datos del select antes de agregar
function prepararSeleccion(idElemento, nombreCarrera, bloque) {
    const select = document.getElementById("sel_" + idElemento);
    const opt = select.options[select.selectedIndex];
    
    const ofa_id = select.value;
    const sede = opt.getAttribute("data-sede");
    const mod = opt.getAttribute("data-mod");
    const jor = opt.getAttribute("data-jor");

    intentarAgregar(ofa_id, nombreCarrera, bloque, sede, mod, jor);
}

// ===================== LÓGICA DE SELECCIÓN =====================

function intentarAgregar(ofa_id, carrera, bloque, sede, mod, jor) {
    // 1. Validación de Límite Máximo
    if (seleccionadas.length >= limite) {
        alert("Límite de " + limite + " carreras alcanzado.");
        return;
    }

    // 2. Validación de Carrera Única (Global: No repetir nombre en otra sede)
    if (seleccionadas.find(s => s.carrera === carrera)) {
        alert(`La carrera "${carrera}" ya está en tu lista. Solo puedes postular a una misma carrera una vez.`);
        return;
    }

    // 3. Validación de Multi-Campos de Conocimiento
    // Si la configuración es 'NO' (permiteMultiCampos === false)
    if (!permiteMultiCampos && camposSeleccionados.size > 0 && !camposSeleccionados.has(bloque)) {
        const campoActual = Array.from(camposSeleccionados)[0];
        alert(`RESTRICCIÓN: Por reglamento, solo puedes elegir carreras pertenecientes al mismo campo.`);
        return;
    }

    // Si pasa todas las validaciones, agregamos
    seleccionadas.push({ 
        ofa_id, 
        carrera, 
        bloque, 
        sede, 
        modalidad: mod, 
        jornada: jor 
    });
    
    // Registrar el bloque para futuras validaciones
    camposSeleccionados.add(bloque);
    
    actualizarLista();
    document.getElementById("contador").innerText = `${seleccionadas.length}/${limite} seleccionadas`;
}

function actualizarLista() {
    const lista = document.getElementById("listaSel");
    const contador = document.getElementById("contador");
    
    if (!lista) return;

    contador.innerText = `${seleccionadas.length}/${limite} seleccionadas`;
    contador.className = seleccionadas.length >= limite ? "badge badge-full" : "badge";

    lista.innerHTML = "";

    seleccionadas.forEach((item, index) => {
        const li = document.createElement("li");
        
        // --- ATRIBUTOS PARA DRAG & DROP NATIVO ---
        li.draggable = true;
        li.setAttribute("ondragstart", `drag(event, ${index})`);
        li.setAttribute("ondrop", `drop(event, ${index})`);
        li.setAttribute("ondragover", "allowDrop(event)");
        // -----------------------------------------

        li.className = "item-seleccionado-detallado cursor-move";

        li.innerHTML = `
            <div class="drag-handle">⠿</div>
            <div class="orden-numero">${index + 1}</div>
            <div class="detalles-carrera">
                <div class="fila-principal">
                    <span class="nombre-carrera-sel">${item.carrera}</span>
                    <span class="bloque-tag">${item.bloque}</span>
                </div>
                <div class="fila-secundaria">
                    <span><b>Sede:</b> ${item.sede}</span>
                    <span><b>Mod:</b> ${item.modalidad}</span>
                    <span><b>Jornada:</b> ${item.jornada}</span>
                </div>
            </div>
            <button class="btn-eliminar" onclick="eliminarSeleccion(${index})" title="Eliminar">
                &times;
            </button>
        `;
        lista.appendChild(li);
    });
}

function eliminarSeleccion(index) {
    seleccionadas.splice(index, 1);
    
    // Recalcular los campos activos
    camposSeleccionados.clear();
    seleccionadas.forEach(s => camposSeleccionados.add(s.bloque));
    
    actualizarLista();
}

// ===================== PASO 3 Y FINALIZAR =====================

function cargarPaso3(){
    activar(3)
    let html = seleccionadas.map((s,i) => `<p>${i+1}. ${s.carrera} - ${s.sede}</p>`).join("")

    document.getElementById("contenido").innerHTML=`
        <div class="box">
            <h3>Confirmación final</h3>
            <div class="resumen">${html}</div>
            <button class="btn" onclick="cargarPaso2()">Atrás</button>
            <button class="btn" onclick="finalizar()">Confirmar inscripción</button>
        </div>`
}

function finalizar(){
    fetch("http://127.0.0.1:8000/inscripcion/finalizar",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({
            periodo_id: periodoSeleccionado,
            tipo_documento: tipoDoc,
            cedula: user.cedula,
            nombres: user.nombres,
            apellidos: user.apellidos,
            carreras: seleccionadas.map(s => s.ofa_id) // Enviamos solo IDs para la tabla intermedia
        })
    })
    .then(r=>r.json())
    .then(r=>{
        if(r.ok){
            alert("Inscripción registrada correctamente");
            window.location="dashboard.html";
        }else{
            alert("Error: " + r.msg);
        }
    })
}

// ===================== UTILIDADES =====================

// Variable global para rastrear qué índice se está moviendo
let dragIndex = null;

function allowDrop(ev) {
    ev.preventDefault(); // Necesario para permitir soltar
}

function drag(ev, i) {
    dragIndex = i;
    // Opcional: añadir efecto visual al elemento que se arrastra
    ev.dataTransfer.setData("text", i); 
}

function drop(ev, i) {
    ev.preventDefault();
    
    // Evitamos errores si se suelta en el mismo lugar
    if (dragIndex === null || dragIndex === i) return;

    // Lógica de intercambio de posiciones en el array
    let temp = seleccionadas[dragIndex];
    seleccionadas[dragIndex] = seleccionadas[i];
    seleccionadas[i] = temp;

    // Refrescar la lista para actualizar los números de prioridad (1, 2, 3...)
    actualizarLista();
}

// ===================== INIT =====================

async function init() {
    cargarPaso1();
    await cargarPeriodos();
    await cargarTipoDocumento();
    await cargarLimite();
}

async function cargarPeriodos(){
    const res = await fetch("http://127.0.0.1:8000/inscripcion/periodos");
    const data = await res.json();
    if(data.length > 0) periodoSeleccionado = data[0].idperiodo;
}

async function cargarTipoDocumento(){
    const res = await fetch("http://127.0.0.1:8000/inscripcion/tipo-documento/"+user.cedula);
    const data = await res.json();
    if(data) tipoDoc = data.tipodocumento;
}

async function cargarLimite(){
    const r = await fetch("http://127.0.0.1:8000/inscripcion/config-max-carreras");
    const d = await r.json();
    limite = d.max;
}

init();