const user = JSON.parse(localStorage.getItem("user"));

if (!user) {
    window.location = "login.html";
}

window.onload = async () => {
    // 1. SIDEBAR: Cargar Nombre
    document.getElementById("lbl_nombre_lateral").innerText = `${user.nombres}\n${user.apellidos}`;

    // 2. FICHA: Cargar Datos (Usando innerText porque son DIVs en tu HTML)
    document.getElementById("f_cedula").innerText = user.cedula || "N/A";
    document.getElementById("f_nombre").innerText = `${user.nombres} ${user.apellidos}`;
    document.getElementById("f_correo").innerText = user.correo || "N/A";
    document.getElementById("f_telefono").innerText = user.telefono || "N/A";
    // Si tienes nota guardada:
    document.getElementById("f_nota").innerText = user.nota_grado ? user.nota_grado : "9.50"; 
    // Dirección y Civil son estáticos en tu HTML o puedes cargarlos si están en 'user'
    
    // 3. ESTADO GENERAL
    await cargarEstadoGeneral();
};

function show(id) {
    document.querySelectorAll(".panel").forEach(p => p.classList.remove("active"));
    document.querySelectorAll(".menu-btn").forEach(b => b.classList.remove("active"));
    
    document.getElementById(id).classList.add("active");
    
    // Activar botón menú manualmente basado en el orden
    const btns = document.querySelectorAll(".menu-btn");
    if(id === 'inicio') btns[0].classList.add("active");
    if(id === 'ficha') btns[1].classList.add("active");
}

async function cargarEstadoGeneral() {
    try {
        const res = await fetch(`http://127.0.0.1:8000/dashboard/resumen/${user.cedula}`);
        const data = await res.json();

        // --- PASO 1: REGISTRO NACIONAL (ID: status_rn) ---
        const statusRn = document.getElementById("status_rn");
        const cardRn = document.getElementById("card_rn");

        if (data.registro_nacional === "HABILITADO") {
            cardRn.classList.add("done-step");
            statusRn.innerHTML = "<b style='color:#27ae60'>✔ HABILITADO</b>";
        } else {
            statusRn.innerHTML = "<b style='color:#c0392b'>❌ NO HABILITADO</b>";
        }

        // --- PASO 2: INSCRIPCIÓN (ID: container_btn_inscripcion) ---
        const containerBtn = document.getElementById("container_btn_inscripcion");
        const cardIns = document.getElementById("card_ins");
        containerBtn.innerHTML = "";

        if (data.inscripcion === "COMPLETADA") {
            cardIns.classList.add("done-step");
            containerBtn.innerHTML = `
                <div style="color:#27ae60; font-weight:bold; margin-bottom:5px;">✔ INSCRITO</div>
                <button onclick="descargarComprobante()" class="btn-action btn-green">
                    <i class="fas fa-file-pdf"></i> Comprobante
                </button>
            `;
        } else {
            cardIns.classList.add("active-step");
            containerBtn.innerHTML = `
                <div style="color:#e67e22; margin-bottom:5px;">Pendiente</div>
                <button onclick="irAInscripcion()" class="btn-action btn-blue">
                    <i class="fas fa-pen"></i> Inscribirse
                </button>
            `;
        }

        // --- PASO 3: EVALUACIÓN (ID: status_exa) ---
        const statusExa = document.getElementById("status_exa");
        if(data.examen === "RENDIDO"){
            document.getElementById("card_exa").classList.add("done-step");
            statusExa.innerHTML = "<b style='color:#27ae60'>✔ RENDIDO</b>";
        }

        // --- PASO 4: ASIGNACIÓN (ID: status_res) ---
        const statusRes = document.getElementById("status_res");
        if(data.asignacion === "ASIGNADO"){
            document.getElementById("card_res").classList.add("done-step");
            statusRes.innerHTML = "<b style='color:#27ae60'>✔ CUPO ASIGNADO</b>";
        }

    } catch (e) {
        console.error("Error al conectar", e);
    }
}

// Navegación Ofertas
async function irAInscripcion() {
    show('panel_ofertas');
    // Activar panel ofertas manualmente y desactivar inicio
    document.getElementById("inicio").classList.remove("active");
    document.getElementById("panel_ofertas").classList.add("active");

    const div = document.getElementById("gridOfertas");
    div.innerHTML = "Cargando ofertas...";

    try {
        const res = await fetch("http://127.0.0.1:8000/dashboard/ofertas-disponibles");
        const ofertas = await res.json();

        if(ofertas.length === 0) {
            div.innerHTML = "<p>No hay ofertas disponibles.</p>";
            return;
        }

        div.innerHTML = ofertas.map(o => `
            <div class="oferta-item">
                <span style="background:#e0f2f1; color:#00695c; padding:2px 8px; border-radius:4px; font-size:12px;">${o.BloqueConocimiento || 'General'}</span>
                <h3 style="margin:10px 0; color:#2c3e50;">${o.nombre_carrera}</h3>
                <p style="font-size:13px; color:#7f8c8d;">${o.modalidad} | ${o.jornada===1?'Matutina':'Vespertina'}</p>
                <button onclick="confirmarInscripcion('${o.nombre_carrera}', ${o.ofa_id})" class="btn-action btn-blue">
                    Seleccionar
                </button>
            </div>
        `).join("");
    } catch (e) { div.innerHTML = "Error cargando ofertas"; }
}

async function confirmarInscripcion(carrera, idOferta) {
    if(!confirm(`¿Deseas inscribirte en ${carrera}?`)) return;

    const payload = {
        cedula: user.cedula,
        nombres: user.nombres,
        apellidos: user.apellidos,
        carrera: carrera,
        id_oferta: idOferta
    };

    try {
        const res = await fetch("http://127.0.0.1:5500/frontend/inscripcion.html", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
        
        if (res.ok) {
            alert("¡Inscripción exitosa!");
            location.reload();
        } else {
            const d = await res.json();
            alert("Error: " + d.detail);
        }
    } catch (e) { alert("Error de conexión"); }
}

function descargarComprobante() {
    window.open(`http://127.0.0.1:8000/certificados/inscripcion/${user.cedula}`);
}

function logout() {
    localStorage.clear();
    window.location = "login.html";
}