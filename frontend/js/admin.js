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
async function crearPeriodo(){
    const data={
     nombre:document.getElementById("p_nombre").value,
     inicio:document.getElementById("p_inicio").value,
     fin:document.getElementById("p_fin").value
    }
    if(!data.nombre || !data.inicio || !data.fin) return alert("Complete todo");

    await fetch("http://127.0.0.1:8000/admin/periodo",{
     method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify(data)
    })
    alert("Periodo creado");
    listarPeriodos(); cargarCombos(); cargarStatsInicio();
}

async function listarPeriodos(){
    const div = document.getElementById("lista_periodos");
    div.innerHTML = "Cargando...";
    try {
        const res = await fetch("http://127.0.0.1:8000/admin/periodos/listar");
        const periodos = await res.json();
        
        if(periodos.length === 0){ div.innerHTML = "No hay periodos"; return; }
        
        let html = `<table style="width:100%; border-collapse:collapse; font-size:14px;">
                      <tr style="background:#eee; text-align:left;">
                        <th style="padding:8px;">Nombre</th><th style="padding:8px;">Fechas</th><th style="padding:8px;">Estado</th><th style="padding:8px;">Acción</th>
                      </tr>`;
        
        periodos.forEach(p => {
            const esActivo = p.estado === 'activo';
            html += `<tr style="border-bottom:1px solid #ddd;">
                        <td style="padding:8px; font-weight:bold;">${p.nombreperiodo}</td>
                        <td style="padding:8px;">${p.fecha_inicio} a ${p.fecha_fin}</td>
                        <td style="padding:8px;">
                            <span style="background:${esActivo?'#2ecc71':'#95a5a6'}; color:white; padding:3px 8px; border-radius:10px; font-size:11px;">
                                ${p.estado ? p.estado.toUpperCase() : 'CERRADO'}
                            </span>
                        </td>
                        <td style="padding:8px;">
                            ${esActivo ? 
                              `<button style="background:#e74c3c; color:white; border:none; padding:5px 10px; border-radius:4px; cursor:pointer;" onclick="cambiarEstadoPeriodo(${p.idperiodo}, 'cerrado')">Cerrar</button>` : 
                              `<button style="background:#3498db; color:white; border:none; padding:5px 10px; border-radius:4px; cursor:pointer;" onclick="cambiarEstadoPeriodo(${p.idperiodo}, 'activo')">Activar</button>`
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
    const res = await fetch("http://127.0.0.1:8000/admin/periodo/estado", {
        method: "PUT", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ idperiodo: id, nuevo_estado: nuevoEstado })
    });
    if(res.ok){ alert("Estado actualizado"); listarPeriodos(); cargarStatsInicio(); }
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
async function cargarCombos(){
    try {
        const res = await fetch("http://127.0.0.1:8000/admin/datos_auxiliares");
        const data = await res.json();
        const selPer = document.getElementById("o_periodo");
        if(data.periodos.length > 0) selPer.innerHTML = data.periodos.map(p => `<option value="${p.idperiodo}">${p.nombreperiodo}</option>`).join("");
        const selSede = document.getElementById("o_sede");
        if(data.sedes.length > 0) selSede.innerHTML = data.sedes.map(s => `<option value="${s.sede_id}">${s.nombre_sede}</option>`).join("");
        const selAsig = document.getElementById("a_periodo");
        if(selAsig && data.periodos.length > 0) selAsig.innerHTML = data.periodos.map(p => `<option value="${p.idperiodo}">${p.nombreperiodo}</option>`).join("");
    } catch (e) { console.error(e); }
}

// 5. BUSCADOR
async function buscarAspirante() {
    const criterio = document.getElementById("txt_buscar").value;
    const div = document.getElementById("resultados_busqueda");
    if (criterio.length < 3) { div.innerHTML = "<p style='text-align:center;'>Min 3 caracteres...</p>"; return; }

    const res = await fetch("http://127.0.0.1:8000/admin/aspirante/buscar/" + criterio);
    const aspirantes = await res.json();
    if (aspirantes.length === 0) { div.innerHTML = "<p style='text-align:center;'>No encontrado.</p>"; return; }

    div.innerHTML = aspirantes.map(a => `
        <div class="aspirante-card ${a.estado_inscripcion==='INVALIDADO'?'invalidado':''}">
            <div style="flex:2">
                <h3 style="margin:0;">${a.nombres} ${a.apellidos}</h3>
                <p style="margin:5px 0; color:#7f8c8d; font-size:14px;">C.I: ${a.identificacion} | Carrera: <b>${a.carrera_seleccionada}</b></p>
                <div class="aspirante-tags">
                    <span class="tag">🏆 Nota: ${a.puntaje_final||0} <i class="fas fa-pencil-alt btn-edit-icon" onclick="editarNota('${a.id_inscripcion}', ${a.puntaje_final||0})"></i></span>
                </div>
            </div>
            <div style="flex:1; text-align:right;">
                <button class="${a.estado_inscripcion==='INVALIDADO'?'btn-success':'btn-danger'}" onclick="cambiarEstado('${a.id_inscripcion}', '${a.estado_inscripcion==='INVALIDADO'?'REGISTRADO':'INVALIDADO'}')">
                 ${a.estado_inscripcion==='INVALIDADO'?'Habilitar':'Invalidar'}
                </button>
            </div>
        </div>`).join("");
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
    const periodo = document.getElementById("a_periodo").value;
    if(!periodo) return alert("Seleccione periodo");
    if(!confirm("⚠️ ¿Ejecutar?")) return;
    const div = document.getElementById("reporte_asignacion");
    div.innerHTML = "Procesando...";
    const res = await fetch("http://127.0.0.1:8000/admin/asignacion/ejecutar", {
        method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ periodo_id: periodo })
    });
    const r = await res.json();
    if(res.ok){
        let html = `<h3>✅ Listo</h3><table><tr><th>Carrera</th><th>Cupos</th><th>Entraron</th><th>Fuera</th></tr>`;
        r.detalles.forEach(d => html += `<tr><td>${d.carrera}</td><td>${d.cupos}</td><td>${d.asignados}</td><td>${d.rechazados}</td></tr>`);
        div.innerHTML = html + "</table>";
        cargarStatsInicio();
    } else { div.innerHTML = "Error: " + r.detail; }
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
