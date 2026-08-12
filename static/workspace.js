const API_BASE = window.location.origin;
const boleto = localStorage.getItem("boleto");
const rol = localStorage.getItem("rol") || "";
const user = localStorage.getItem("user");


function tieneRol(listaPermitida) {
  return listaPermitida.includes(rol);
}

if (!boleto) { window.location.href = "/"; }

document.getElementById("tituloUsuario").textContent = `Hola, ${user || ''} (${rol})`;
document.getElementById("salir").addEventListener("click", () => {
  localStorage.clear();
  window.location.href = "/";
});


const MODULOS = {
  becas: {
    titulo: "Becas", endpoint: "/becas",
    permisos: { ver: ["Administrador","Profesor"], crear: ["Administrador"], editar: ["Administrador"], borrar: ["Administrador"] },
    campos: [
      { nombre: "tipo_beca", etiqueta: "Tipo de beca", tipo: "text" },
      { nombre: "porcentaje_descuento", etiqueta: "% Descuento", tipo: "number" },
      { nombre: "duracion", etiqueta: "Duración", tipo: "number" }
    ]
  },
  carreras: {
    titulo: "Carreras", endpoint: "/carreras",
    permisos: { ver: ["Administrador","Profesor"], crear: ["Administrador"], editar: ["Administrador"], borrar: ["Administrador"] },
    campos: [
      { nombre: "nombre", etiqueta: "Nombre", tipo: "text" },
      { nombre: "duracion", etiqueta: "Duración", tipo: "text" },
      { nombre: "cantidad_clases", etiqueta: "Cantidad de clases", tipo: "number" }
    ]
  },
  clases: {
    titulo: "Clases", endpoint: "/clases",
    permisos: { ver: ["Administrador","Profesor"], crear: ["Administrador","Profesor"], editar: ["Administrador","Profesor"], borrar: ["Administrador"] },
    campos: [
      { nombre: "nombre", etiqueta: "Nombre", tipo: "text" },
      { nombre: "creditos", etiqueta: "Créditos", tipo: "number" },
      { nombre: "codigo", etiqueta: "Código", tipo: "text" },
      { nombre: "modalidad", etiqueta: "Modalidad", tipo: "text" },
      { nombre: "dia", etiqueta: "Día", tipo: "text" },
      { nombre: "horario", etiqueta: "Horario", tipo: "text" }
    ]
  },
  estudiantes: {
    titulo: "Estudiantes", endpoint: "/estudiantes",
    permisos: { ver: ["Administrador","Profesor"], crear: ["Administrador"], editar: ["Administrador","Profesor"], borrar: ["Administrador"] },
    campos: [
      { nombre: "nombre", etiqueta: "Nombre", tipo: "text" },
      { nombre: "telefono", etiqueta: "Teléfono", tipo: "text" },
      { nombre: "cuenta", etiqueta: "Cuenta", tipo: "text" },
      { nombre: "correo", etiqueta: "Correo", tipo: "email" },
      { nombre: "direccion", etiqueta: "Dirección", tipo: "text" },
      { nombre: "estado_civil", etiqueta: "Estado civil", tipo: "text" },
      { nombre: "edad", etiqueta: "Edad", tipo: "number" },
      { nombre: "modalidad", etiqueta: "Modalidad", tipo: "text" },
      { nombre: "id_beca", etiqueta: "ID Beca (opcional)", tipo: "number", opcional: true },
      { nombre: "id_carrera", etiqueta: "ID Carrera", tipo: "number" },
      { nombre: "id_usuario", etiqueta: "ID Usuario", tipo: "number" }
    ]
  },
  profesores: {
    titulo: "Profesores", endpoint: "/profesores",
    permisos: { ver: ["Administrador","Profesor"], crear: ["Administrador"], editar: ["Administrador","Profesor"], borrar: ["Administrador"] },
    campos: [
      { nombre: "nombre", etiqueta: "Nombre", tipo: "text" },
      { nombre: "telefono", etiqueta: "Telefono", tipo: "text" },
      { nombre: "correo", etiqueta: "Correo", tipo: "email" },
      { nombre: "direccion", etiqueta: "Direccion", tipo: "text" },
      { nombre: "estado_civil", etiqueta: "Estado civil", tipo: "text" },
      { nombre: "edad", etiqueta: "Edad", tipo: "number" },
      { nombre: "modalidad", etiqueta: "Modalidad", tipo: "text" },
      { nombre: "codigo_empleado", etiqueta: "Codigo empleado", tipo: "text" },
      { nombre: "salario", etiqueta: "Salario", tipo: "number" },
      { nombre: "id_usuario", etiqueta: "ID Usuario", tipo: "number" }
    ]
  },
  nomina: {
    titulo: "Nómina", endpoint: "/nomina",
    permisos: { ver: ["Administrador","Profesor"], crear: ["Administrador","Profesor"], editar: ["Administrador","Profesor"], borrar: ["Administrador"] },
    campos: [
      { nombre: "id_profesor", etiqueta: "ID Profesor", tipo: "number" },
      { nombre: "id_rrhh", etiqueta: "ID RRHH", tipo: "number" }
    ]
  },
  usuarios: {
    titulo: "Usuarios", endpoint: "/usuarios",
    permisos: { ver: ["Administrador"], crear: ["Administrador"], editar: ["Administrador"], borrar: ["Administrador"] },
    campos: [
      { nombre: "user", etiqueta: "Usuario", tipo: "text" },
      { nombre: "password", etiqueta: "Contraseña", tipo: "password" },
      { nombre: "rol", etiqueta: "Rol", tipo: "text" }
    ]
  },
  seguros: {
    titulo: "Seguros", endpoint: "/seguros",
    permisos: { ver: ["Administrador","Profesor"], crear: ["Administrador"], editar: ["Administrador"], borrar: ["Administrador"] },
    campos: [
      { nombre: "tipo_seguro", etiqueta: "Tipo de seguro", tipo: "text" },
      { nombre: "porcentaje_descuento", etiqueta: "% Descuento", tipo: "number" },
      { nombre: "contrato", etiqueta: "Contrato", tipo: "text" }
    ]
  },
  rrhh: {
    titulo: "RRHH", endpoint: "/rrhh",
    permisos: { ver: ["Administrador"], crear: ["Administrador"], editar: ["Administrador"], borrar: ["Administrador"] },
    campos: [
      { nombre: "nombre", etiqueta: "Nombre", tipo: "text" },
      { nombre: "telefono", etiqueta: "Teléfono", tipo: "text" },
      { nombre: "correo", etiqueta: "Correo", tipo: "email" },
      { nombre: "direccion", etiqueta: "Dirección", tipo: "text" },
      { nombre: "codigo_empleado", etiqueta: "Código empleado", tipo: "number" },
      { nombre: "id_usuario", etiqueta: "ID Usuario", tipo: "number" }
    ]
  }
};

// ------------------ RENDER DE TARJETAS ------------------
const cardsDiv = document.getElementById("cards");

function puedeVer(modulo) {
  return tieneRol(MODULOS[modulo].permisos.ver);
}

Object.keys(MODULOS).forEach(clave => {
  const mod = MODULOS[clave];
  const div = document.createElement("div");
  const bloqueada = !puedeVer(clave);
  div.className = "glass-card" + (bloqueada ? " bloqueada" : "");
  div.textContent = mod.titulo;
  if (!bloqueada) {
    div.addEventListener("click", () => cargarModulo(clave));
  }
  cardsDiv.appendChild(div);
});

const divInsc = document.createElement("div");
divInsc.className = "glass-card";
divInsc.textContent = "Inscripciones";
divInsc.addEventListener("click", cargarInscripciones);
cardsDiv.appendChild(divInsc);

// ------------------ FETCH CON AUTENTICACIÓN ------------------
async function llamarAPI(ruta, metodo = "GET", body = null) {
  const opciones = {
    method: metodo,
    headers: {
      "Content-Type": "application/json",
      "token": boleto
    }
  };
  if (body) opciones.body = JSON.stringify(body);

  const resp = await fetch(`${API_BASE}${ruta}`, opciones);

  if (resp.status === 401 || resp.status === 403) {
    localStorage.clear();
    window.location.href = "/";
    throw new Error("Sesión expirada");
  }

  let data = null;
  try { data = await resp.json(); } catch (e) { data = null; }

  if (!resp.ok) {
    const detalle = (data && data.detail) ? data.detail : `Error ${resp.status}`;
    throw new Error(detalle);
  }
  return data;
}

// ------------------ CARGA DE MÓDULO (TABLA) ------------------
const contenido = document.getElementById("contenido");
let moduloActual = null;
let idEditando = null;

async function cargarModulo(clave) {
  moduloActual = clave;
  const mod = MODULOS[clave];
  const puedeCrear = tieneRol(mod.permisos.crear);
  const puedeEditar = tieneRol(mod.permisos.editar);
  const puedeBorrar = tieneRol(mod.permisos.borrar);

  contenido.innerHTML = `
    <div class="panel-box">
      <h3>${mod.titulo}</h3>
      ${puedeCrear ? `<button class="btn btn-primary" id="btnNuevo">+ Nuevo</button>` : ""}
      <div id="estado">Cargando ${mod.titulo.toLowerCase()}...</div>
      <div id="tablaContenedor"></div>
    </div>
  `;

  if (puedeCrear) {
    document.getElementById("btnNuevo").addEventListener("click", () => abrirModal(clave, null));
  }

  const estado = document.getElementById("estado");

  try {
    const data = await llamarAPI(mod.endpoint + "/", "GET");
    const claveLista = Object.keys(data).find(k => Array.isArray(data[k]));
    const lista = claveLista ? data[claveLista] : [];

    estado.textContent = "";
    renderTabla(clave, lista, puedeEditar, puedeBorrar);
  } catch (err) {
    estado.textContent = "No hay registros o error: " + err.message;
    document.getElementById("tablaContenedor").innerHTML = "";
  }
}

function renderTabla(clave, lista, puedeEditar, puedeBorrar) {
  const mod = MODULOS[clave];
  const contenedor = document.getElementById("tablaContenedor");

  if (!lista || lista.length === 0) {
    contenedor.innerHTML = "<p>No hay registros.</p>";
    return;
  }

  const columnas = ["id", ...mod.campos.map(c => c.nombre)];

  let html = "<table><thead><tr>";
  columnas.forEach(c => html += `<th>${c}</th>`);
  if (puedeEditar || puedeBorrar) html += "<th>Acciones</th>";
  html += "</tr></thead><tbody>";

  lista.forEach(fila => {
    html += "<tr>";
    columnas.forEach(c => html += `<td>${fila[c] !== null && fila[c] !== undefined ? fila[c] : ""}</td>`);
    if (puedeEditar || puedeBorrar) {
      html += "<td>";
      if (puedeEditar) html += `<button class="btn btn-warn" onclick='abrirModal("${clave}", ${JSON.stringify(fila).replace(/'/g, "&apos;")})'>Editar</button>`;
      if (puedeBorrar) html += `<button class="btn btn-danger" onclick="borrarRegistro('${clave}', ${fila.id})">Borrar</button>`;
      html += "</td>";
    }
    html += "</tr>";
  });

  html += "</tbody></table>";
  contenedor.innerHTML = html;
}

// ------------------ BORRAR ------------------
async function borrarRegistro(clave, id) {
  if (!confirm("¿Seguro que deseas eliminar el registro #" + id + "?")) return;
  const mod = MODULOS[clave];
  try {
    await llamarAPI(`${mod.endpoint}/${id}`, "DELETE");
    cargarModulo(clave);
  } catch (err) {
    alert("Error al eliminar: " + err.message);
  }
}

// ------------------ MODAL CREAR / EDITAR ------------------
const modalFondo = document.getElementById("modalFondo");
const modalForm = document.getElementById("modalForm");
const modalTitulo = document.getElementById("modalTitulo");

document.getElementById("modalCancelar").addEventListener("click", cerrarModal);

function cerrarModal() {
  modalFondo.classList.remove("activo");
  modalForm.innerHTML = "";
  idEditando = null;
}

function abrirModal(clave, filaExistente) {
  const mod = MODULOS[clave];
  idEditando = filaExistente ? filaExistente.id : null;
  modalTitulo.textContent = (filaExistente ? "Editar " : "Nuevo/a ") + mod.titulo;

  let html = "";
  mod.campos.forEach(campo => {
    const valor = filaExistente && filaExistente[campo.nombre] !== undefined && filaExistente[campo.nombre] !== null
      ? filaExistente[campo.nombre] : "";
    html += `
      <label>${campo.etiqueta}</label>
      <input type="${campo.tipo}" name="${campo.nombre}" value="${valor}" ${campo.opcional ? "" : "required"}>
    `;
  });
  modalForm.innerHTML = html;
  modalFondo.classList.add("activo");
}

modalForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const mod = MODULOS[moduloActual];
  const formData = new FormData(modalForm);
  const cuerpo = {};

  mod.campos.forEach(campo => {
    let valor = formData.get(campo.nombre);
    if (campo.tipo === "number") {
      valor = valor === "" ? null : Number(valor);
    }
    cuerpo[campo.nombre] = valor;
  });

  try {
    if (idEditando) {
      await llamarAPI(`${mod.endpoint}/${idEditando}`, "PUT", cuerpo);
    } else {
      await llamarAPI(`${mod.endpoint}/`, "POST", cuerpo);
    }
    cerrarModal();
    cargarModulo(moduloActual);
  } catch (err) {
    alert("Error al guardar: " + err.message);
  }
});

// ------------------ INSCRIPCIONES ------------------
function cargarInscripciones() {
  moduloActual = "inscripciones";
  contenido.innerHTML = `
    <div class="panel-box">
      <h3>Inscripciones</h3>
      <label>Tipo de relación</label>
      <select id="tipoInsc" style="padding:8px;border-radius:6px;">
        <option value="estudiante-clase">Estudiante - Clase</option>
        <option value="profesor-clase">Profesor - Clase</option>
        <option value="profesor-carrera">Profesor - Carrera</option>
        <option value="profesor-seguro">Profesor - Seguro</option>
      </select>
      <div style="margin-top:12px;" id="camposInsc"></div>
      <button class="btn btn-primary" id="btnAsignar">Asignar</button>
      <button class="btn btn-danger" id="btnDesasignar">Desasignar</button>
      <div id="estado"></div>
      <hr style="opacity:0.2;margin:20px 0;">
      <h3>Buscar inscripciones</h3>
      <label>Buscar estudiantes por ID de clase</label>
      <input type="number" id="buscarClase" placeholder="ID de clase" style="padding:8px;border-radius:6px;width:150px;">
      <button class="btn btn-primary" id="btnBuscarClase">Buscar</button>
      <br><br>
      <label>Buscar clases por ID de estudiante</label>
      <input type="number" id="buscarEstudiante" placeholder="ID de estudiante" style="padding:8px;border-radius:6px;width:150px;">
      <button class="btn btn-primary" id="btnBuscarEstudiante">Buscar</button>
      <div id="tablaContenedor" style="margin-top:16px;"></div>
    </div>
  `;

  const CAMPOS_INSC = {
    "estudiante-clase": [{ n: "id_estudiante", l: "ID Estudiante" }, { n: "id_clase", l: "ID Clase" }],
    "profesor-clase": [{ n: "id_profesor", l: "ID Profesor" }, { n: "id_clase", l: "ID Clase" }],
    "profesor-carrera": [{ n: "id_profesor", l: "ID Profesor" }, { n: "id_carrera", l: "ID Carrera" }],
    "profesor-seguro": [{ n: "id_profesor", l: "ID Profesor" }, { n: "id_seguro", l: "ID Seguro" }]
  };

  function pintarCampos() {
    const tipo = document.getElementById("tipoInsc").value;
    const campos = CAMPOS_INSC[tipo];
    document.getElementById("camposInsc").innerHTML = campos.map(c =>
      `<label>${c.l}</label><input type="number" id="insc_${c.n}" style="padding:8px;border-radius:6px;width:150px;margin-right:10px;">`
    ).join("");
  }
  document.getElementById("tipoInsc").addEventListener("change", pintarCampos);
  pintarCampos();

  async function accionInsc(metodo) {
    const tipo = document.getElementById("tipoInsc").value;
    const campos = CAMPOS_INSC[tipo];
    const cuerpo = {};
    campos.forEach(c => cuerpo[c.n] = Number(document.getElementById(`insc_${c.n}`).value));
    const estado = document.getElementById("estado");
    try {
      const data = await llamarAPI(`/inscripciones/${tipo}`, metodo, cuerpo);
      estado.style.color = "#c9ffd2";
      estado.textContent = data.Mensaje || "Operacion exitosa";
    } catch (err) {
      estado.style.color = "#ffd2d2";
      estado.textContent = "Error: " + err.message;
    }
  }

  document.getElementById("btnAsignar").addEventListener("click", () => accionInsc("POST"));
  document.getElementById("btnDesasignar").addEventListener("click", () => accionInsc("DELETE"));

  document.getElementById("btnBuscarClase").addEventListener("click", async () => {
    const id = document.getElementById("buscarClase").value;
    const cont = document.getElementById("tablaContenedor");
    try {
      const data = await llamarAPI(`/inscripciones/clase/${id}`, "GET");
      pintarInsc(data.inscripciones, ["id", "id_estudiante", "id_clase"]);
    } catch (err) {
      cont.innerHTML = "<p>" + err.message + "</p>";
    }
  });

  document.getElementById("btnBuscarEstudiante").addEventListener("click", async () => {
    const id = document.getElementById("buscarEstudiante").value;
    const cont = document.getElementById("tablaContenedor");
    try {
      const data = await llamarAPI(`/inscripciones/estudiante/${id}`, "GET");
      pintarInsc(data.inscripciones, ["id", "id_estudiante", "id_clase"]);
    } catch (err) {
      cont.innerHTML = "<p>" + err.message + "</p>";
    }
  });

  function pintarInsc(lista, columnas) {
    const cont = document.getElementById("tablaContenedor");
    if (!lista || lista.length === 0) { cont.innerHTML = "<p>Sin resultados.</p>"; return; }
    let html = "<table><thead><tr>";
    columnas.forEach(c => html += `<th>${c}</th>`);
    html += "</tr></thead><tbody>";
    lista.forEach(fila => {
      html += "<tr>";
      columnas.forEach(c => html += `<td>${fila[c]}</td>`);
      html += "</tr>";
    });
    html += "</tbody></table>";
    cont.innerHTML = html;
  }
}