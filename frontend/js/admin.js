const user = JSON.parse(localStorage.getItem("user"))

if(!user || user.rol !== "Admin"){
 alert("Acceso restringido")
 window.location="login.html"
}

let chartCarreras = null;
let chartEstados = null;

window.onload = async () => {
    await cargarStatsInicio();
    await cargarCombos();
}

function show(id){
 document.querySelectorAll(".panel").forEach(p => p.classList.remove("active"));
 document.querySelectorAll(".menu-btn").forEach(b => b.classList.remove("active"));
 document.getElementById(id).classList.add("active");
 if(id === 'reportes') cargarReportes();
 if(id === 'periodo') listarPeriodos(); // Cargar tabla al entrar
}

// 1. DASHBOARD
async function cargarStatsInicio(){
    try {
        const res = await fetch("http://127.0.0.1:8000/admin/home_stats");
        const data = await res.json();
        document.getElementById("lbl_periodo").innerText = data.periodo;
        document.getElementById("lbl_total").innerText = data.aspirantes;
    } catch (e) { console.error(e); }
}

// 2. PERIODO (CREAR Y LISTAR)
async function crearPeriodo() {
    const user = JSON.parse(localStorage.getItem("user"));
    
    if (!user || !user.ies_id) {
        return alert("Tu cuenta no tiene una institución asignada. Contacta al soporte técnico.");
    }

    const nombre = document.getElementById("p_nombre").value;
    const inicioStr = document.getElementById("p_inicio").value;
    const finStr = document.getElementById("p_fin").value;

    if (!nombre || !inicioStr || !finStr) {
        return alert("Complete todos los campos del periodo");
    }

    // --- NUEVAS VALIDACIONES DE FECHA ---
    const fechaInicio = new Date(inicioStr + "T00:00:00");
    const fechaFin = new Date(finStr + "T00:00:00");
    const hoy = new Date();
    hoy.setHours(0, 0, 0, 0); // Normalizar hoy para comparar solo fechas

    // 1. Validar que inicio sea hoy o futuro
    if (fechaInicio < hoy) {
        return alert("Error: La fecha de inicio no puede ser anterior a la fecha actual.");
    }

    // 2. Validar que fin sea mayor a inicio
    if (fechaFin <= fechaInicio) {
        return alert("Error: La fecha de fin debe ser posterior a la fecha de inicio.");
    }
    // ------------------------------------

    const data = {
        nombre: nombre,
        inicio: inicioStr,
        fin: finStr,
        ies_id: user.ies_id
    };

    try {
        const res = await fetch("http://127.0.0.1:8000/admin/periodo", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });

        if (res.ok) {
            alert("Periodo creado con éxito");
            // Limpiar y recargar
            document.getElementById("p_nombre").value = "";
            document.getElementById("p_inicio").value = "";
            document.getElementById("p_fin").value = "";
            listarPeriodos(); 
        } else {
            const errorData = await res.json();
            alert("Error: " + (errorData.detail || "No se pudo crear"));
        }
    } catch (e) {
        console.error(e);
        alert("Error de conexión");
    }
}

async function listarPeriodos(){
    const div = document.getElementById("lista_periodos");
    div.innerHTML = "Cargando...";

    try {
        // Quitamos el /${user.ies_id} de la URL
        const res = await fetch("http://127.0.0.1:8000/admin/periodos/listar");
        const periodos = await res.json();
        
        if(periodos.length === 0){ div.innerHTML = "No hay periodos"; return; }
        
        let html = `<table style="width:100%; border-collapse:collapse; font-size:14px;">
                      <tr style="background:#eee; text-align:left;">
                        <th style="padding:8px;">Nombre</th><th style="padding:8px;">Fechas</th><th style="padding:8px;">Estado</th><th style="padding:8px;">Acción</th>
                      </tr>`;
        
        periodos.forEach(p => {
            const esActivo = p.estado === 'activo';
            // Usar exactamente los nombres de tu tabla universidad/periodo
            const f_inicio = p.fechainicio || 'S/N';
            const f_fin = p.fechafin || 'S/N';

            html += `<tr style="border-bottom:1px solid #ddd;">
                        <td style="padding:8px; font-weight:bold;">${p.nombreperiodo}</td>
                        <td style="padding:8px;">${f_inicio} a ${f_fin}</td>
                        <td style="padding:8px;">
                            <span style="background:${esActivo?'#2ecc71':'#95a5a6'}; color:white; padding:3px 8px; border-radius:10px; font-size:11px;">
                                ${p.estado ? p.estado.toUpperCase() : 'CERRADO'}
                            </span>
                        </td>
                        <td style="padding:8px;">
                            ${esActivo ? 
                              `<button ... onclick="cambiarEstadoPeriodo(${p.idperiodo}, 'cerrado')">Cerrar</button>` : 
                              `<button ... onclick="cambiarEstadoPeriodo(${p.idperiodo}, 'activo')">Activar</button>`
                            }
                        </td>
                      </tr>`;
        });
        html += "</table>";
        div.innerHTML = html;
    } catch (e) { console.error(e); div.innerHTML = "Error al listar"; }
}

async function cambiarEstadoPeriodo(id, nuevoEstado){
    if(!confirm(`¿${nuevoEstado === 'activo' ? 'ACTIVAR' : 'CERRAR'} este periodo?`)) return;
    
    // URL EXACTA SEGÚN TU admin.py
    const res = await fetch("http://127.0.0.1:8000/admin/periodo/estado", {
        method: "PUT", 
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
            idperiodo: id,           // Tu backend espera este nombre
            nuevo_estado: nuevoEstado // Tu backend espera este nombre
        })
    });

    if(res.ok){ 
        alert("Estado actualizado con éxito"); 
        await listarPeriodos(); // RECARGA LA LISTA
        await cargarStatsInicio(); // ACTUALIZA EL DASHBOARD
    } else {
        const error = await res.json();
        alert("Error: " + (error.detail || "No se pudo actualizar"));
    }
}
// 3. OFERTA
async function crearOferta(){
    const data = {
        nombre_carrera: document.getElementById("o_carrera").value,
        periodo_id: document.getElementById("o_periodo").value,
        cupos_disponibles: document.getElementById("o_cupos").value,
        sede_id: document.getElementById("o_sede").value,
        modalidad: document.getElementById("o_modalidad").value,
        BloqueConocimiento: document.getElementById("o_bloque").value,
        jornada: document.getElementById("o_jornada").value,
        fecha_publicacion: document.getElementById("o_fecha").value,
        estado_oferta: document.getElementById("o_estado").value
    };
    if(!data.nombre_carrera) return alert("Faltan datos");
    const res = await fetch("http://127.0.0.1:8000/admin/oferta",{
        method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify(data)
    });
    if(res.ok){ alert("Oferta Creada"); document.getElementById("o_carrera").value = ""; } 
    else { alert("Error"); }
}

// 4. COMBOS
// 4. COMBOS (Actualizada)
async function cargarCombos(){
    try {
        const res = await fetch("http://127.0.0.1:8000/admin/datos_auxiliares");
        const data = await res.json();
        
        // Función auxiliar para llenar selects
        const llenar = (id, lista, val, txt) => {
            const el = document.getElementById(id);
            if(el && lista.length > 0) {
                el.innerHTML = lista.map(p => `<option value="${p[val]}">${p[txt]}</option>`).join("");
            } else if (el) {
                el.innerHTML = "<option value=''>No hay datos</option>";
            }
        };

        // Llenar los combos existentes
        llenar("o_periodo", data.periodos, "idperiodo", "nombreperiodo");
        llenar("o_sede", data.sedes, "sede_id", "nombre_sede");
        llenar("a_periodo", data.periodos, "idperiodo", "nombreperiodo");
        llenar("conf_periodo", data.periodos, "idperiodo", "nombreperiodo"); // Configuración
        
        // ---> ESTA ES LA LÍNEA NUEVA PARA EL FILTRO DE DESCARGA <---
        llenar("filtro_periodo_descarga", data.periodos, "idperiodo", "nombreperiodo");

        // ... resto de combos (lab_sede, mon_lab, etc.)

    } catch (e) { console.error(e); }
}
// 5. BUSCADOR
async function buscarAspirante() {
    const criterio = document.getElementById("txt_buscar").value;
    const div = document.getElementById("resultados_busqueda");

    if (criterio.length < 3) { 
        div.innerHTML = "<p style='text-align:center;'>Min 3 caracteres...</p>"; 
        return; 
    }

    try {
        const res = await fetch("http://127.0.0.1:8000/admin/aspirante/buscar/" + criterio);
        const aspirantes = await res.json();

        if (aspirantes.length === 0) { 
            div.innerHTML = "<p style='text-align:center;'>No encontrado.</p>"; 
            return; 
        }

        div.innerHTML = aspirantes.map(a => {
            // Verificamos si está invalidado
            const esInvalidado = a.estado === 'INVALIDADO';

            return `
            <div class="aspirante-card ${esInvalidado ? 'invalidado' : ''}">
                <div style="flex:2">
                    <h3 style="margin:0;">${a.nombres} ${a.apellidos}</h3>
                    <p style="margin:5px 0; color:#7f8c8d; font-size:14px;">
                        C.I: ${a.identificacion} | Carrera: <b>${a.carrera_seleccionada || 'Sin carrera'}</b>
                    </p>
                    <div class="aspirante-tags">
                        <span class="tag" style="background:${esInvalidado ? '#e74c3c' : '#2ecc71'}; color:white;">
                            ${a.estado}
                        </span>
                        <span class="tag">
                            🏆 Nota: ${a.puntaje_final || 0} 
                            <i class="fas fa-pencil-alt btn-edit-icon" onclick="editarNota('${a.id_inscripcion}', ${a.puntaje_final || 0})"></i>
                        </span>
                    </div>
                </div>
                <div style="flex:1; text-align:right;">
                    <button class="${esInvalidado ? 'btn-success' : 'btn-danger'}" 
                        onclick="cambiarEstado('${a.id_inscripcion}', '${esInvalidado ? 'registrado' : 'INVALIDADO'}')">
                        ${esInvalidado ? 'Habilitar' : 'Invalidar'}
                    </button>
                </div>
            </div>`;
        }).join("");

    } catch (error) {
        console.error(error);
        div.innerHTML = "<p style='color:red; text-align:center'>Error de conexión</p>";
    }
}

async function editarNota(idInscripcion, notaActual){
    const nuevaNota = prompt("Nueva nota (0-1000):", notaActual);
    if(nuevaNota === null) return;
    const valor = parseInt(nuevaNota);
    if(isNaN(valor) || valor < 0 || valor > 1000) return alert("Inválido");
    
    await fetch("http://127.0.0.1:8000/admin/aspirante/nota", {
        method: "PUT", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id_inscripcion: idInscripcion, nota: valor })
    });
    alert("Nota actualizada"); buscarAspirante();
}

async function cambiarEstado(id, nuevo) {
    if(!confirm(`¿Cambiar estado?`)) return;
    await fetch("http://127.0.0.1:8000/admin/aspirante/estado", {
        method: "PUT", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id_inscripcion: id, nuevo_estado: nuevo })
    });
    alert("Actualizado"); buscarAspirante();
}

// 6. ASIGNACIÓN
async function ejecutarAsignacion(){

 const periodo = document.getElementById("a_periodo").value

 if(!periodo){
  alert("Seleccione un período")
  return
 }

 if(!confirm("¿Seguro que desea ejecutar la asignación masiva?")){
  return
 }

 const res = await fetch(
 "http://127.0.0.1:8000/admin/asignacion/ejecutar",{
  method:"POST",
  headers:{ "Content-Type":"application/json"},
  body:JSON.stringify({
    periodo_id: periodo
  })
 })

 const data = await res.json()

 if(data.ok){
   alert("Asignación ejecutada correctamente")
 }else{
   alert("Error: "+data.msg)
 }
}


// 7. REPORTES
async function cargarReportes() {
    const res = await fetch("http://127.0.0.1:8000/admin/reportes/stats");
    const data = await res.json();
    const ctx1 = document.getElementById('chartCarreras').getContext('2d');
    if(chartCarreras) chartCarreras.destroy();
    chartCarreras = new Chart(ctx1, { type: 'bar', data: { labels: data.carreras.labels, datasets: [{ label: 'Aspirantes', data: data.carreras.values, backgroundColor: '#3498db' }] } });
    const ctx2 = document.getElementById('chartEstados').getContext('2d');
    if(chartEstados) chartEstados.destroy();
    chartEstados = new Chart(ctx2, { type: 'doughnut', data: { labels: data.estados.labels, datasets: [{ data: data.estados.values, backgroundColor: ['#2ecc71', '#e74c3c', '#95a5a6', '#f1c40f'] }] } });
}

function logout(){ localStorage.clear(); window.location="login.html"; }



// -------- ASIGNACIÓN MASIVA DE EXÁMENES --------
async function asignarMasivo(){

 const idperiodo = 1 // activo

 const res = await fetch(
 "http://127.0.0.1:8000/admin/asignar-examenes/"+idperiodo,
 { method:"POST" }
 )

 const r = await res.json()

 alert(r.data.msg+" → "+r.data.total)
}


// Guardar Fecha de Examen
async function guardarFechaExamen(){

 const fecha = document.getElementById("fechaInicioExamen").value
 const periodo = document.getElementById("a_periodo").value

 if(!fecha || !periodo){
  alert("Seleccione fecha y período")
  return
 }

 const res = await fetch(
 "http://127.0.0.1:8000/admin/config-examen",
 {
  method:"POST",
  headers:{ "Content-Type":"application/json" },
  body: JSON.stringify({
    periodo_id: periodo,
    fecha_inicio: fecha
  })
 })

 const data = await res.json()

 if(data.ok){
  alert("Fecha guardada correctamente")
 }else{
  alert("Error al guardar")
 }
}

// Validar estado del período antes de asignar exámenes
async function validarPeriodo(){
    const periodoId = document.getElementById("a_periodo").value;
    if(!periodoId) return;

    try {
        // En tu admin.py NO tienes /periodos/listar/${user.ies_id}
        // Tienes /periodos/listar (que trae todos). Vamos a usar esa:
        const res = await fetch(`http://127.0.0.1:8000/admin/periodos/listar`);
        const periodos = await res.json();

        const per = periodos.find(p => p.idperiodo == periodoId);
        const btn = document.getElementById("btnAsignar");

        if(per && per.estado === "cerrado"){
            btn.disabled = false;
            btn.innerText = "Ejecutar asignación";
        } else {
            btn.disabled = true;
            btn.innerText = "Solo se asigna en periodos CERRADOS";
        }
    } catch (e) {
        console.error("Error al validar periodo:", e);
    }
 if(per.estado === "cerrado"){
   btn.disabled = false
   btn.innerText = "Ejecutar asignación"
 }else{
   btn.disabled = true
   btn.innerText = "Periodo activo (bloqueado)"
 }
 validarAsignacionEjecutada()

}
    
// Bloquear botón si ya se realizó asignación
async function bloquearSiYaAsignado(){

 const periodo = document.getElementById("a_periodo").value

 const res = await fetch(
 "http://127.0.0.1:8000/admin/asignacion/existe/"+periodo
 )

 const data = await res.json()

 document.getElementById("btnAsignar").disabled = data.existe
}


async function validarAsignacionEjecutada(){

 const periodo = document.getElementById("a_periodo").value

 if(!periodo) return

 const res = await fetch(
  "http://127.0.0.1:8000/admin/asignacion/estado/"+periodo
 )

 const r = await res.json()

 const btn = document.getElementById("btnAsignar")

 if(r.ejecutado){
  btn.disabled = true
  btn.innerHTML = "✔ Ya ejecutado"
  btn.style.background = "#95a5a6"
 }else{
  btn.disabled = false
  btn.innerHTML = "▶ Ejecutar"
  btn.style.background = "#3498db"
 }
}
/* =========================================================
   1. GESTIÓN DE CONFIGURACIÓN DEL SISTEMA
   ========================================================= */
async function listarConfiguraciones() {
    const div = document.getElementById("lista_configs");
    const res = await fetch("http://127.0.0.1:8000/admin/configuraciones");
    const data = await res.json();

    if (data.length === 0) { div.innerHTML = "Sin configuraciones."; return; }

    let html = `<table class="table-config"><tr><th>Periodo</th><th>Configuración</th><th>Valor</th><th>Acción</th></tr>`;
    data.forEach(c => {
        // Pasamos el objeto completo para editar
        const objStr = encodeURIComponent(JSON.stringify(c));
        html += `<tr>
            <td>${c.periodo ? c.periodo.nombreperiodo : c.idperiodo}</td>
            <td>${c.tipo_config}</td>
            <td>${c.valor}</td>
            <td>
                <button onclick="cargarFormConfig(decodeURIComponent('${objStr}'))" class="btn-edit"><i class="fas fa-edit"></i></button>
            </td>
        </tr>`;
    });
    html += "</table>";
    div.innerHTML = html;
}

function cargarFormConfig(jsonStr) {
    const c = JSON.parse(jsonStr);
    document.getElementById("conf_id").value = c.id_config;
    document.getElementById("conf_periodo").value = c.idperiodo;
    document.getElementById("conf_tipo").value = c.tipo_config;
    document.getElementById("conf_valor").value = c.valor;
    
    document.getElementById("txt_accion_conf").innerText = "Editar";
    document.getElementById("btn_cancelar_conf").style.display = "block";
}

async function guardarConfig() {
    const id = document.getElementById("conf_id").value;
    const data = {
        idperiodo: document.getElementById("conf_periodo").value,
        tipo_config: document.getElementById("conf_tipo").value,
        valor: document.getElementById("conf_valor").value
    };
    if (id) data.id_config = id; // Si hay ID, es edición

    const res = await fetch("http://127.0.0.1:8000/admin/configuracion", {
        method: id ? "PUT" : "POST", // Usamos PUT si es edición
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });

    if (res.ok) {
        alert("Guardado correctamente");
        limpiarConfig();
        listarConfiguraciones();
    } else {
        alert("Error al guardar");
    }
}

function limpiarConfig() {
    document.getElementById("conf_id").value = "";
    document.getElementById("conf_valor").value = "";
    document.getElementById("txt_accion_conf").innerText = "Nueva";
    document.getElementById("btn_cancelar_conf").style.display = "none";
}


/* =========================================================
   2. GESTIÓN DE INFRAESTRUCTURA (SEDES, LABS, MONITORES)
   ========================================================= */

// --- SEDES ---
async function listarSedes() {
    const res = await fetch("http://127.0.0.1:8000/admin/sedes/listar"); // Endpoint nuevo
    const data = await res.json();
    let html = `<table class="table-config"><tr><th>Nombre</th><th>Capacidad</th><th>Acción</th></tr>`;
    data.forEach(s => {
        const objStr = encodeURIComponent(JSON.stringify(s));
        html += `<tr><td>${s.nombre_sede}</td><td>${s.capacidad_total}</td>
        <td><button onclick="cargarFormSede(decodeURIComponent('${objStr}'))" class="btn-edit">✏️</button></td></tr>`;
    });
    document.getElementById("tabla_sedes").innerHTML = html + "</table>";
}

function cargarFormSede(json) {
    const s = JSON.parse(json);
    document.getElementById("sede_id").value = s.sede_id;
    document.getElementById("sede_nombre").value = s.nombre_sede;
    document.getElementById("sede_dir").value = s.direccion;
    document.getElementById("sede_ies").value = s.ies_id;
    document.getElementById("sede_cap").value = s.capacidad_total;
    document.getElementById("btn_cancelar_sede").style.display = "block";
}

async function guardarSede() {
    const id = document.getElementById("sede_id").value;
    const data = {
        nombre_sede: document.getElementById("sede_nombre").value,
        direccion: document.getElementById("sede_dir").value,
        ies_id: document.getElementById("sede_ies").value,
        capacidad_total: document.getElementById("sede_cap").value
    };
    if(id) data.sede_id = id;

    await enviarDatos("http://127.0.0.1:8000/admin/sede", id ? "PUT" : "POST", data);
    limpiarSede();
    listarSedes();
    cargarCombos(); // Recargar combo sedes
}

function limpiarSede(){
    document.getElementById("sede_id").value = "";
    document.getElementById("sede_nombre").value = "";
    document.getElementById("sede_dir").value = "";
    document.getElementById("sede_cap").value = "";
    document.getElementById("btn_cancelar_sede").style.display = "none";
}

// --- LABORATORIOS ---
async function listarLabs() {
    const res = await fetch("http://127.0.0.1:8000/admin/laboratorios/listar");
    const data = await res.json();
    let html = `<table class="table-config"><tr><th>Nombre</th><th>Sede</th><th>Piso</th><th>Acción</th></tr>`;
    data.forEach(l => {
        const objStr = encodeURIComponent(JSON.stringify(l));
        html += `<tr><td>${l.nombre_lab}</td><td>${l.sede ? l.sede.nombre_sede : 'N/A'}</td><td>${l.piso}</td>
        <td><button onclick="cargarFormLab(decodeURIComponent('${objStr}'))" class="btn-edit">✏️</button></td></tr>`;
    });
    document.getElementById("tabla_labs").innerHTML = html + "</table>";
}

function cargarFormLab(json) {
    const l = JSON.parse(json);
    document.getElementById("lab_id").value = l.lab_id;
    document.getElementById("lab_nombre").value = l.nombre_lab;
    document.getElementById("lab_sede").value = l.sede_id;
    document.getElementById("lab_piso").value = l.piso;
    document.getElementById("lab_cap").value = l.capacidad_total || 0; // Ajusta si la columna es distinta
    document.getElementById("btn_cancelar_lab").style.display = "block";
}

async function guardarLaboratorio() {
    const id = document.getElementById("lab_id").value;
    const data = {
        nombre_lab: document.getElementById("lab_nombre").value,
        sede_id: document.getElementById("lab_sede").value,
        piso: document.getElementById("lab_piso").value,
        // Asumiendo que laboratorio tiene capacidad, si no, quita esta línea
        // capacidad: document.getElementById("lab_cap").value 
    };
    if(id) data.lab_id = id;

    await enviarDatos("http://127.0.0.1:8000/admin/laboratorio", id ? "PUT" : "POST", data);
    limpiarLab();
    listarLabs();
    cargarCombos(); // Recargar combo laboratorios para monitor
}

function limpiarLab(){
    document.getElementById("lab_id").value = "";
    document.getElementById("lab_nombre").value = "";
    document.getElementById("btn_cancelar_lab").style.display = "none";
}

// --- MONITORES ---
async function listarMonitores() {
    const res = await fetch("http://127.0.0.1:8000/admin/monitores/listar");
    const data = await res.json();
    let html = `<table class="table-config"><tr><th>Nombre</th><th>Teléfono</th><th>Lab</th><th>Acción</th></tr>`;
    data.forEach(m => {
        const objStr = encodeURIComponent(JSON.stringify(m));
        html += `<tr><td>${m.nombre_completo}</td><td>${m.telefono}</td><td>${m.laboratorio ? m.laboratorio.nombre_lab : 'N/A'}</td>
        <td><button onclick="cargarFormMonitor(decodeURIComponent('${objStr}'))" class="btn-edit">✏️</button></td></tr>`;
    });
    document.getElementById("tabla_monitores").innerHTML = html + "</table>";
}

function cargarFormMonitor(json) {
    const m = JSON.parse(json);
    document.getElementById("mon_id").value = m.monitor_id;
    document.getElementById("mon_nombre").value = m.nombre_completo;
    document.getElementById("mon_cedula").value = m.identificacion;
    document.getElementById("mon_tel").value = m.telefono;
    document.getElementById("mon_lab").value = m.lab_id;
    document.getElementById("mon_estado").value = m.estado_disponibilidad || 'ACTIVO';
    document.getElementById("btn_cancelar_mon").style.display = "block";
}

async function guardarMonitor() {
    const id = document.getElementById("mon_id").value;
    const data = {
        nombre_completo: document.getElementById("mon_nombre").value,
        identificacion: document.getElementById("mon_cedula").value,
        telefono: document.getElementById("mon_tel").value,
        lab_id: document.getElementById("mon_lab").value,
        estado_disponibilidad: document.getElementById("mon_estado").value
    };
    if(id) data.monitor_id = id;

    await enviarDatos("http://127.0.0.1:8000/admin/monitor", id ? "PUT" : "POST", data);
    limpiarMonitor();
    listarMonitores();
}

function limpiarMonitor(){
    document.getElementById("mon_id").value = "";
    document.getElementById("mon_nombre").value = "";
    document.getElementById("mon_cedula").value = "";
    document.getElementById("mon_tel").value = "";
    document.getElementById("btn_cancelar_mon").style.display = "none";
}

// --- UTILIDAD ---
async function enviarDatos(url, metodo, data) {
    const res = await fetch(url, {
        method: metodo,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });
    if(res.ok) alert("Operación exitosa");
    else alert("Error al guardar");
}

// Actualizar la función show() para que cargue las listas al abrir las pestañas
const originalShow = show; // Guardar referencia si existe
// Actualizar la función show() para manejar el menú activo y cargas
function show(id) {
    // 1. Ocultar todos los paneles
    document.querySelectorAll(".panel").forEach(p => p.classList.remove("active"));
    
    // 2. Desactivar todos los botones del menú (quitar clase active)
    document.querySelectorAll(".menu-btn").forEach(b => b.classList.remove("active"));
    
    // 3. Mostrar el panel seleccionado
    const panel = document.getElementById(id);
    if(panel) panel.classList.add("active");

    // 4. Activar visualmente el botón del menú presionado
    // El "event" detecta qué botón se clickeó
    if (event && event.currentTarget && event.currentTarget.classList.contains('menu-btn')) {
        event.currentTarget.classList.add("active");
    }

    // 5. Cargas específicas por panel
    if(id === 'reportes') cargarReportes();
    if(id === 'periodo') listarPeriodos();
    if(id === 'config') listarConfiguraciones();
    if(id === 'infra') { listarSedes(); listarLabs(); listarMonitores(); }
    
    // Nota: 'matrices' no necesita carga extra aquí porque el combo de periodos 
    // ya se llena al inicio con cargarCombos()
}
/* =========================================
   FUNCIÓN PARA DESCARGAR MATRICES
   ========================================= */
function descargarMatriz(tipo) {
    // 1. Obtener el periodo seleccionado
    const select = document.getElementById("filtro_periodo_descarga");
    const periodoId = select.value;
    
    if (!periodoId) {
        alert("⚠️ Por favor, selecciona un periodo primero.");
        return;
    }

    // 2. Construir la URL según el botón presionado
    let url = "";
    if (tipo === 'oferta') {
        url = `http://127.0.0.1:8000/admin/reportes/matriz-oferta/${periodoId}`;
    } else if (tipo === 'postulaciones') {
        url = `http://127.0.0.1:8000/admin/reportes/matriz-postulaciones/${periodoId}`;
    }

    // 3. Forzar la descarga abriendo la URL
    // Esto hace que el navegador descargue el archivo automáticamente
    window.location.href = url;
}
    // Mantener las cargas antiguas
    if(id === 'reportes' && typeof cargarReportes === 'function') cargarReportes();
    if(id === 'periodo' && typeof listarPeriodos === 'function') listarPeriodos();
}
