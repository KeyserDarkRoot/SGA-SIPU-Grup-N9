const user = JSON.parse(localStorage.getItem("user"))

if(!user || user.rol !== "Admin"){
 alert("Acceso restringido")
 window.location="login.html"
}



function show(id){
 document.querySelectorAll(".panel")
 .forEach(p=>p.classList.remove("active"))
 document.getElementById(id).classList.add("active")
}

// -------- PERIODO --------
async function crearPeriodo(){

const data={
 nombre:p_nombre.value,
 inicio:p_inicio.value,
 fin:p_fin.value
}

await fetch("http://127.0.0.1:8000/admin/periodo",{
 method:"POST",
 headers:{"Content-Type":"application/json"},
 body:JSON.stringify(data)
})

alert("Periodo creado")
}

// -------- OFERTA --------
async function crearOferta(){

const data={
 carrera:o_carrera.value,
 bloque:o_bloque.value,
 cupos:o_cupos.value
}

await fetch("http://127.0.0.1:8000/admin/oferta",{
 method:"POST",
 headers:{"Content-Type":"application/json"},
 body:JSON.stringify(data)
})

alert("Oferta creada")
}

// -------- UNIVERSIDAD --------
async function crearUniversidad(){

const data={
 nombre:u_nombre.value,
 direccion:u_dir.value
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

const res=await fetch(
"http://127.0.0.1:8000/admin/postulaciones")

const r=await res.json()

tabla_post.innerHTML=r.map(p=>
 `<p>${p.cedula} - ${p.carrera}</p>`
).join("")
}

cargarPost()

function logout(){
 localStorage.clear()
 window.location="login.html"
}


