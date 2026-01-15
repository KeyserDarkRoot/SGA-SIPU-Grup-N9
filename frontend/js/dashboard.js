async function cargar(){

const res = await fetch("http://127.0.0.1:8000/dashboard/stats")
const r = await res.json()

document.getElementById("total").innerText =
"Inscripciones: "+r.total
}

cargar()


const user = JSON.parse(localStorage.getItem("user"))

if(!user){
 window.location="login.html"
}

document.getElementById("cedula").innerText =
"C.I: "+user.cedula

document.getElementById("correo").innerText =
user.correo

document.getElementById("bienvenida").innerText =
"Bienvenido(a), "+user.nombres+" "+user.apellidos


// CONSULTAR ESTADO REGISTRO NACIONAL
async function cargarFases(){

 const res = await fetch(
 "http://127.0.0.1:8000/dashboard/estado/"+user.cedula)

 const r = await res.json()

 let color="gray"
 let icon="❓"

 if(r.estado==="HABILITADO"){
  color="#2ecc71"
  icon="✅"
 }
 if(r.estado==="CONDICIONADO"){
  color="#f1c40f"
  icon="⚠️"
 }
 if(r.estado==="NO HABILITADO"){
  color="#e74c3c"
  icon="❌"
 }

 document.getElementById("fases").innerHTML=`

 <div class="card">
   <b>FASE 1: REGISTRO NACIONAL</b>
   <p class="status" style="color:${color}">
     ${r.estado} ${icon}
   </p>
 </div>

 <div class="card">
   <b>FASE 2: INSCRIPCIÓN Y EVALUACIÓN</b>
   <p>Complete su inscripción para la sede de examen.</p>

   <button onclick="irInscripcion()">
    Realizar Inscripción
   </button>

   <button>
    Descargar Certificado
   </button>
 </div>
 `
}

cargarFases()

function irInscripcion(){
 window.location = "inscripcion.html"
}

function logout(){
 localStorage.clear()
 window.location="login.html"
}
