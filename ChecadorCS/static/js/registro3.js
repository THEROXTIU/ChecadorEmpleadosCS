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


fechaActual.innerHTML = fechaHoy;

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
