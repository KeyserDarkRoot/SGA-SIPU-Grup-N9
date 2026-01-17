const user = JSON.parse(localStorage.getItem("user"))

if(!user){
 window.location="login.html"
}

// ================= PINTAR DATOS USUARIO =================

document.getElementById("userName")
.innerText = user.nombres+" "+user.apellidos

document.getElementById("avatar")
.src += user.nombres


// ================= CONSULTAS BACKEND =================

async function estadoRegistro(){

 const res = await fetch(
 "http://127.0.0.1:8000/dashboard/estado/"+user.cedula)

 return await res.json()
}

async function estaInscrito(){

 const res = await fetch(
 "http://127.0.0.1:8000/inscripcion/verificar/"+user.cedula)

 return await res.json()
}

async function tieneEvaluacion(){

 const res = await fetch(
 "http://127.0.0.1:8000/evaluacion/verificar/"+user.cedula)

 return await res.json()
}


// ================= UI PRINCIPAL =================

async function cargarFases(){

 const rn = await estadoRegistro()
 const ins = await estaInscrito()
 const evalua = await tieneEvaluacion()

 document.getElementById("fases").innerHTML = `

 <div class="card">
  <h3>Registro Nacional</h3>
  <p>${rn.estado==="HABILITADO" ? "✅ HABILITADO" : "❌ BLOQUEADO"}</p>
 </div>

 <div class="card">
  <h3>Inscripción</h3>
  <p>${ins.ok ? "✔ Completada" : "⏳ Pendiente"}</p>

  ${ins.ok ? `
    <button onclick="descargarCertificadoInscripcion()" class="btn-cert" style="background: #007bff; color: white; padding: 10px; border: none; border-radius: 5px; cursor: pointer;">
    📄 Generar Certificado
  </button>
  ` : `
    <button onclick="irInscripcion()">
      Ir a inscripción
    </button>
  `}
  </div>

 <div class="card">
  <h3>Evaluación</h3>
  <p>${evalua.ok ? "✔ Rendido" : "⏳ Pendiente"}</p>

  ${ins.ok && !evalua.ok ? `
   <button onclick="irExamen()">
    Rendir examen
   </button>` : ""}
 </div>

 <div class="card">
  <h3>Resultados</h3>

  ${evalua.ok ? `
   <button onclick="verPuntaje()">
    Ver puntaje
   </button>` : `
   <button disabled>
    Bloqueado
   </button>`}
 </div>
 `

 // progreso
 let progreso = 0
 if(rn.estado==="HABILITADO") progreso+=33
 if(ins.ok) progreso+=33
 if(evalua.ok) progreso+=34

 progressBar.style.width = progreso+"%"
}



// ================= TOAST =================

function notify(msg){
 const toast = document.getElementById("toast")

 toast.innerText = msg
 toast.style.display="block"

 setTimeout(()=>{
  toast.style.display="none"
 },3000)
}


// ================= ACCIONES =================

function irInscripcion(){
 window.location="inscripcion.html"

}

async function descargarCertificadoInscripcion() {
    notify("Conectando con el servicio de certificados...");
    
    // IMPORTANTE: Esta URL debe coincidir con la ruta que creaste en FastAPI/Flask
    try {
        const res = await fetch(`http://127.0.0.1:8000/certificados/inscripcion/${user.cedula}`);
        
        if (res.ok) {
            const blob = await res.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `Comprobante_Inscripcion.pdf`;
            a.click();
            notify("✅ PDF Generado con éxito");
        } else {
            notify("❌ El servidor de Python no pudo generar el PDF");
        }
    } catch (error) {
        notify("❌ Error: Verifica que tu backend esté corriendo y tengas internet");
    }
}

function irExamen(){
 window.location="examen.html"
}

function verPuntaje(){
 window.location="puntaje.html"
}

function logout(){
 localStorage.clear()
 window.location="login.html"
}

function modoOscuro(){
 document.body.classList.toggle("dark")
}


// ================= INIT =================

cargarFases()
notify("Bienvenido al sistema SIPU")
