const API_BASE = window.location.origin;

document.getElementById('formLogin').addEventListener('submit', async (e) => {
  e.preventDefault();
  const mensaje = document.getElementById('mensaje');
  mensaje.textContent = "Verificando...";

  const user = document.getElementById('user').value;
  const password = document.getElementById('password').value;

  try {
    const resp = await fetch(`${API_BASE}/recepcion/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user, password })
    });

    const data = await resp.json();

    if (!resp.ok) {
      mensaje.textContent = data.detail || "Error al iniciar sesion";
      return;
    }

    localStorage.setItem("boleto", data.boleto);
    localStorage.setItem("rol", data.rol);
    localStorage.setItem("user", data.user);

    window.location.href = "/workspace";

  } catch (err) {
    mensaje.textContent = "No se pudo conectar con el servidor (" + err.message + ")";
  }
});