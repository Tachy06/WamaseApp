document.addEventListener("DOMContentLoaded", function() {
    var inputFecha = document.getElementById("date");
    
    // Obtener la fecha actual
    var fechaActual = new Date();
    var añoActual = fechaActual.getFullYear();
    var mesActual = fechaActual.getMonth() + 1; // Nota: getMonth() devuelve el mes comenzando desde 0
    
    // Ajustar el valor mínimo y máximo del input de fecha
    var primerDiaDelMes = new Date(añoActual, mesActual - 1, 1); // El mes comienza desde 0
    var ultimoDiaDelMes = new Date(añoActual, mesActual, 0); // Al restar 1 al mes, obtenemos el último día del mes actual
    
    var fechaMinima = primerDiaDelMes.toISOString().split('T')[0];
    var fechaMaxima = ultimoDiaDelMes.toISOString().split('T')[0];
    
    inputFecha.setAttribute("min", fechaMinima);
    inputFecha.setAttribute("max", fechaMaxima);
});