let paso=1
let seleccion={}

const user=JSON.parse(localStorage.getItem("user"))

function activar(n){
 document.querySelectorAll(".steps span")
 .forEach(s=>s.classList.remove("active"))
 document.getElementById("p"+n).classList.add("active")
}

function cargarPaso1(){

 activar(1)

 fetch("http://127.0.0.1:8000/inscripcion/datos/"+user.cedula)
 .then(r=>r.json())
 .then(d=>{

 document.getElementById("contenido").innerHTML=`

 <div class="box">
 <h3>Datos del Registro Nacional</h3>

 ${Object.entries(d).map(e=>
 `<p><b>${e[0]}</b>: ${e[1]}</p>`
 ).join("")}

 <button onclick="cargarPaso2()">Siguiente</button>
 </div>
 `
 })
}

function cargarPaso2(){

 activar(2)

 Promise.all([
  fetch("http://127.0.0.1:8000/inscripcion/universidades"),
  fetch("http://127.0.0.1:8000/inscripcion/oferta")
 ])
 .then(async([u,o])=>[await u.json(),await o.json()])
 .then(([unis,oferta])=>{

 document.getElementById("contenido").innerHTML=`

 <div class="box">
 <h3>Selección Universidad y Carrera</h3>

 <select id="uni">
 ${unis.map(u=>`<option value="${u.ies_id}">
 ${u.nombre}</option>`)}
 </select>

 <table border="1" width="100%">
 <tr><th>Bloque</th><th>Carrera</th><th>Cupos</th></tr>
 ${oferta.map(o=>
 `<tr onclick="sel('${o.BloqueConocimiento}',
 '${o.nombre_carrera}')">
 <td>${o.BloqueConocimiento}</td>
 <td>${o.nombre_carrera}</td>
 <td>${o.cupos_disponibles}</td>
 </tr>`)}
 </table>

 <button onclick="cargarPaso1()">Atrás</button>
 <button onclick="cargarPaso3()">Siguiente</button>
 </div>
 `
 })
}

function sel(b,c){
 seleccion.bloque=b
 seleccion.carrera=c
}

function cargarPaso3(){

 activar(3)

 seleccion.ies_id=document.getElementById("uni").value

 document.getElementById("contenido").innerHTML=`

 <div class="box">
 <h3>Confirmación</h3>

 <pre>
 Carrera: ${seleccion.carrera}
 Bloque: ${seleccion.bloque}
 IES ID: ${seleccion.ies_id}
 </pre>

 <button onclick="cargarPaso2()">Atrás</button>
 <button onclick="finalizar()">FINALIZAR</button>
 </div>
 `
}

function finalizar(){

 fetch("http://127.0.0.1:8000/inscripcion/finalizar",{
  method:"POST",
  headers:{"Content-Type":"application/json"},
  body:JSON.stringify({
   cedula:user.cedula,
   nombres:user.nombres,
   apellidos:user.apellidos,
   carrera:seleccion.carrera,
   ies_id:seleccion.ies_id
  })
 })

 alert("Inscripción registrada correctamente")
 window.location="dashboard.html"
}

cargarPaso1()
