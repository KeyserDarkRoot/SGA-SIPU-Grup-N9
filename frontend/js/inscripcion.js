let paso = 1
let seleccion = {}
let periodoSeleccionado = null
let tipoDoc = null
let limite = 0
let seleccionadas = []


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

function cargarPaso1(){
    activar(1);

    fetch("http://127.0.0.1:8000/inscripcion/datos/" + user.cedula)
    .then(r => r.json())
    .then(d => {
        // 1. Definimos exactamente qué campos queremos mostrar
        const camposPermitidos = [
            'tipodocumento', 
            'identificacion', 
            'nombres', 
            'apellidos', 
            'nacionalidad', 
            'fechanacimiento', 
            'estadocivil', 
            'sexo', 
            'genero', 
            'autoidentificacion'
        ];

        // 2. Filtramos los datos que vienen del servidor
        const contenidoHTML = camposPermitidos.map(campo => {
            // Verificamos si el dato existe para evitar errores
            const valor = d[campo] !== undefined ? d[campo] : "No disponible";
            // Formateamos el nombre del campo para que se vea bien (ej: tipodocumento -> Tipo documento)
            const etiqueta = campo.charAt(0).toUpperCase() + campo.slice(1);
            
            return `<p><b>${etiqueta}</b>: ${valor}</p>`;
        }).join("");

        // 3. Renderizamos en el HTML
        document.getElementById("contenido").innerHTML = `
            <div class="box">
                <h3>Datos del Registro Nacional</h3>
                <div class="datos-personales">
                    ${contenidoHTML}
                </div>
                <button class="btn" onclick="cargarPaso2()">Siguiente</button>
            </div>
        `;
    });
}
// ===================== PASO 2 =====================

function cargarPaso2(){

 activar(2)

 fetch("http://127.0.0.1:8000/inscripcion/ofertas")
 .then(r=>r.json())
 .then(oferta=>{

 document.getElementById("contenido").innerHTML=`

 <div class="box">

 <h3>Selección de carreras</h3>

 <div class="panel">
  <span class="badge">
   ${seleccionadas.length}/${limite} seleccionadas
  </span>
 </div>

 <div class="search-box">
  <input id="buscador" 
  placeholder="Buscar carrera..."
  onkeyup="filtrar()">
 </div>

 <h4>Carreras disponibles</h4>
 <div id="cards"></div>

 <h4>Seleccionadas (arrastre para ordenar)</h4>
 <ul id="listaSel"></ul>

 <button class="btn" onclick="cargarPaso1()">Atrás</button>
 <button class="btn" onclick="cargarPaso3()">Siguiente</button>

 </div>
 `

 window.dataOferta = oferta
 renderCards(oferta)
 actualizarLista()
 })
}



// ===================== SELECCIÓN =====================

function sel(id,carrera,sede_id){

 if(seleccionadas.includes(id)){
  alert("Ya seleccionó esta carrera")
  return
 }

 if(seleccionadas.length >= limite){
  alert("Solo puede escoger "+limite+" carreras")
  return
 }

 seleccionadas.push(id)
 seleccion.sede_id = sede_id

 actualizarLista()
}



// Mostrar SELECCIÓN

function actualizarLista(){

 let ul = document.getElementById("listaSel")
 if(!ul) return

 ul.innerHTML=""

 seleccionadas.forEach((id,i)=>{

  ul.innerHTML+=`
  <li draggable="true"
  ondragstart="drag(event,${i})"
  ondrop="drop(event,${i})"
  ondragover="allowDrop(event)"
  class="drag">

   ${i+1}. Oferta ${id}
   <button class="btn btn-danger"
   onclick="eliminar(${i})">X</button>
  </li>`
 })
}

function allowDrop(ev){
 ev.preventDefault()
 ev.target.classList.add("drag-over")
}


let dragIndex=null

function drag(ev,i){
 dragIndex=i
 ev.target.classList.add("dragging") // 👈 efecto visual
}

function drop(ev,i){

 ev.target.classList.remove("dragging") // 👈 quitar efecto

 let temp = seleccionadas[dragIndex]
 seleccionadas[dragIndex] = seleccionadas[i]
 seleccionadas[i] = temp

 actualizarLista()
}




// Eliminar de SELECCIÓN

function eliminar(pos){

 seleccionadas.splice(pos,1)
 actualizarLista()
}



// ===================== PASO 3 =====================

function cargarPaso3(){

 activar(3)

 let html = seleccionadas.map((c,i)=>
 `<p>${i+1}. Oferta ${c}</p>`).join("")

 document.getElementById("contenido").innerHTML=`

 <div class="box">
 <h3>Confirmación final</h3>

 ${html}

 <button class="btn" onclick="cargarPaso2()">Atrás</button>
 <button class="btn" onclick="finalizar()">Confirmar inscripción</button>
 </div>
 `
}



// ===================== GUARDAR =====================

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
   sede_id: seleccion.sede_id,

   carreras: seleccionadas   // 👈 ARRAY
  })
 })
 .then(r=>r.json())
 .then(r=>{
   if(r.ok){
     alert("Inscripción registrada correctamente")
     window.location="dashboard.html"
   }else{
     alert("Error: "+r.msg)
   }
 })
}



// ===================== CARGA DATOS BD =====================

async function cargarPeriodos(){

 const res = await fetch(
 "http://127.0.0.1:8000/inscripcion/periodos")

 const data = await res.json()

 if(data.length === 0){
  alert("No hay periodos activos")
  return
 }

 periodoSeleccionado = data[0].idperiodo
}


async function cargarTipoDocumento(){

 const res = await fetch(
 "http://127.0.0.1:8000/inscripcion/tipo-documento/"+user.cedula)

 const data = await res.json()

 if(!data){
  alert("No se encontró tipo de documento")
  return
 }

 tipoDoc = data.tipodocumento
}

async function cargarLimite(){

 const r = await fetch(
 "http://127.0.0.1:8000/inscripcion/config-max-carreras")

 const d = await r.json()
 limite = d.max

 document.getElementById("info")
 .innerHTML=`Puede escoger ${limite} carreras`
}

function renderCards(data){

 let div=document.getElementById("cards")
 div.innerHTML=""

 data.forEach(o=>{

  div.innerHTML+=`
  <div class="card">
   <div>
    <b>${o.nombre_carrera}</b><br>
    <span class="tag">${o.BloqueConocimiento}</span>
   </div>

   <button class="btn"
   onclick="sel('${o.ofa_id}',
   '${o.nombre_carrera}',
   '${o.sede_id}')">
    Agregar
   </button>
  </div>`
 })
}


function filtrar(){

 let txt = buscador.value.toLowerCase()

 let f = dataOferta.filter(o=>
  o.nombre_carrera.toLowerCase().includes(txt))

 renderCards(f)
}

function allowDrop(ev){
 ev.preventDefault()
 ev.target.classList.add("drag-over")
}

function drag(ev,i){
 dragIndex=i
}

function drop(ev,i){

 ev.target.classList.remove("drag-over")

 let temp=seleccionadas[dragIndex]
 seleccionadas[dragIndex]=seleccionadas[i]
 seleccionadas[i]=temp

 actualizarLista()
}

// ===================== INIT =====================

cargarPaso1()
cargarPeriodos()
cargarTipoDocumento()
cargarLimite()
