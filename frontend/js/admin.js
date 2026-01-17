const user = JSON.parse(localStorage.getItem("user"))

// Validación de Seguridad (Rol)
if(!user || user.rol !== "Admin"){
 alert("Acceso restringido")
 window.location="login.html"
}

// AL CARGAR LA PÁGINA: Traer datos para los selects y tabla
window.onload = async () => {
    cargarCombos();
    cargarPost();
}

function show(id){
 document.querySelectorAll(".panel")
 .forEach(p=>p.classList.remove("active"))
 document.getElementById(id).classList.add("active")
}

// FUNCIÓN PARA LLENAR SELECTS DESDE LA BASE DE DATOS
async function cargarCombos(){
    try {
        const res = await fetch("http://127.0.0.1:8000/admin/datos_auxiliares");
        const data = await res.json();
        
        // Llenar Select de Periodos
        const selPer = document.getElementById("o_periodo");
        if(data.periodos.length > 0){
            selPer.innerHTML = data.periodos.map(p => 
                `<option value="${p.idperiodo}">${p.nombreperiodo}</option>`
            ).join("");
        } else {
            selPer.innerHTML = "<option>No hay periodos creados</option>";
        }

        // Llenar Select de Sedes
        const selSede = document.getElementById("o_sede");
        if(data.sedes.length > 0){
            selSede.innerHTML = data.sedes.map(s => 
                `<option value="${s.sede_id}">${s.nombre_sede}</option>`
            ).join("");
        } else {
            selSede.innerHTML = "<option>No hay sedes creadas</option>";
        }

    } catch (e) {
        console.error("Error cargando combos", e);
    }
}

// -------- CREAR OFERTA (LÓGICA ACTUALIZADA 10 CAMPOS) --------
async function crearOferta(){
    // 1. Recolección de datos del DOM
    const data = {
        ofa_id: document.getElementById("o_id").value,
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

    // 2. Validación simple
    if(!data.ofa_id || !data.nombre_carrera || !data.fecha_publicacion){
        alert("Por favor llene los campos obligatorios"); return;
    }

    // 3. Envío al Backend
    const res = await fetch("http://127.0.0.1:8000/admin/oferta",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify(data)
    });

    const r = await res.json();
    if(res.ok){
        alert("¡Oferta Creada con Éxito!");
        // Limpiar ID para facilitar siguiente ingreso
        document.getElementById("o_id").value = "";
        document.getElementById("o_carrera").value = "";
    } else {
        alert("Error: " + r.detail);
    }
}

// -------- PERIODO --------
async function crearPeriodo(){
    const data={
     nombre:document.getElementById("p_nombre").value,
     inicio:document.getElementById("p_inicio").value,
     fin:document.getElementById("p_fin").value
    }
    await fetch("http://127.0.0.1:8000/admin/periodo",{
     method:"POST",
     headers:{"Content-Type":"application/json"},
     body:JSON.stringify(data)
    })
    alert("Periodo creado")
    cargarCombos(); // Recargar el combo de periodos
}

// -------- UNIVERSIDAD --------
async function crearUniversidad(){
    const data={
     nombre:document.getElementById("u_nombre").value,
     direccion:document.getElementById("u_dir").value
    }
    await fetch("http://127.0.0.1:8000/admin/universidad",{
     method:"POST",
     headers:{"Content-Type":"application/json"},
     body:JSON.stringify(data)
    })
    alert("Universidad creada")
}

// -------- POSTULACIONES --------
async function cargarPost(){
    const res=await fetch("http://127.0.0.1:8000/admin/postulaciones")
    const r=await res.json()
    
    const div = document.getElementById("tabla_post");
    if(r.length === 0){
        div.innerHTML = "<p>No hay postulaciones registradas.</p>";
        return;
    }

    div.innerHTML=r.map(p=>
     `<div class="card">
        <p><b>Aspirante:</b> ${p.nombres} ${p.apellidos} (${p.identificacion})</p>
        <p><b>Carrera:</b> ${p.carrera_seleccionada}</p>
        <p><b>IES ID:</b> ${p.ies_id}</p>
      </div>`
    ).join("")
}

function logout(){
 localStorage.clear()
 window.location="login.html"
}