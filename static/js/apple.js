
// Verificar si el usuario ha visitado la página antes
var hasVisited = localStorage.getItem('hasVisited');
        
if (hasVisited) {
    // Si ha visitado la página antes, ocultar el contenido
    document.getElementById("appleSafariContent").classList.add("hidden");
    document.getElementById("arrow").classList.add("hidden");
} else {
    // Si es la primera visita, mostrar el contenido y almacenar el indicador en localStorage
    document.getElementById("appleSafariContent").classList.remove("hidden");
    document.getElementById("arrow").classList.remove("hidden");
    localStorage.setItem('hasVisited', 'true');
}