//Método para sacar la fecha y la hora
const mesesAnio = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'];
const diasSemana = ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'];

const fecha = new Date();

const diaSemana = diasSemana[fecha.getDay()];
const dia = fecha.getDate();
const mes = mesesAnio[fecha.getMonth()];
const anio = fecha.getFullYear();

const fechaHoy = `${diaSemana}, ${dia} de ${mes} de ${anio}`;






var fechaActual = document.getElementById("fechaActual");
var horaActual = document.getElementById("horaActual");
var divHoraManualnual = document.getElementById("divHoraManual");
var divBotonesHora = document.getElementById("divBotonesHora");
var divProyectos = document.getElementById("divProyectos");
var contenedorProyecto = document.getElementById("contenedorProyecto");
var divSinProyecto = document.getElementById("divSinProyecto");


fechaActual.innerHTML = fechaHoy;
divHoraManualnual.style.display="none";
divProyectos.style.display="none";
divSinProyecto.style.display="none";
function mostrarHoraActual() {
    const fecha = new Date();
    let hora = fecha.getHours();
    let minutos = fecha.getMinutes();
    let segundos = fecha.getSeconds();

    // Agregar un cero inicial si la hora, minutos o segundos tienen un solo dígito
    hora = hora < 10 ? '0' + hora : hora;
    minutos = minutos < 10 ? '0' + minutos : minutos;
    segundos = segundos < 10 ? '0' + segundos : segundos;

    const horaActualQueSeActualiza = `${hora}:${minutos}:${segundos}`;
    horaActual.innerHTML = horaActualQueSeActualiza;
    console.log(horaActualQueSeActualiza);
}

setInterval(mostrarHoraActual, 10);

function ocultarDivBotones(){
    var interfazBotones = document.getElementById("interfazBotones");
    interfazBotones.style.display="none";
    var horasTrabajadas = document.getElementById("horasTrabajadas");
    horasTrabajadas.style.display="block";
    

}
function mostrarInputHoraManual(){
    divHoraManualnual.style.display="block";
    divBotonesHora.style.display="none";

    
}

function mostrarOpcionesHora(){
    divHoraManualnual.style.display = "none";
    divBotonesHora.style.display="block";
}

function mostrarDivProyecto(){
    divBotonesHora.style.display ="none";
    divHoraManualnual.style.display = "none";
    divProyectos.style.display ="block";

}

$(document).ready(function() {
    $('#selectProyectos').select2();
});	

function ocultarProyectos(){
    idCheckbox = document.getElementById("switch-label");
    if(idCheckbox.checked){
        contenedorProyecto.style.display ="none";
        divSinProyecto.style.display="block";

    }
    else{
        contenedorProyecto.style.display ="block";
        divSinProyecto.style.display="none";
        
    }
}
function ocultarProyectoMostrarOpcionesHora(){
    divProyectos.style.display = "none";
    divBotonesHora.style.display="block";

}
