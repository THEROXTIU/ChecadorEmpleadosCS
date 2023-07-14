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
var interfazBotones = document.getElementById("interfazBotones");
var divIngresarActividad = document.getElementById("divIngresarActividad");
var divAgregerarPersonalAAsistencia = document.getElementById("divAgregerarPersonalAAsistencia");
var divSelectEmpleado = document.getElementById("divSelectEmpleado");
var divEmpleadosYaGuardados = document.getElementById("divEmpleadosYaGuardados");
var divSpanEmpleadosCustom = document.getElementById("divSpanEmpleadosCustom");
var divInputsDePersonalExterno = document.getElementById("divInputsDePersonalExterno");
var divDosBotonesPersonal = document.getElementById("divDosBotonesPersonal");
var divSpanNombresPersonalExterno = document.getElementById("divSpanNombresPersonalExterno");
var divHorasSalida = document.getElementById("divHorasSalida");
var divHoraManual = document.getElementById("divHoraManual");
var divActividadesFinalesSalida = document.getElementById("divActividadesFinalesSalida");

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


divIngresarActividad.style.display = "none";
divAgregerarPersonalAAsistencia.style.display = "none";
divSelectEmpleado.style.display="none";
divEmpleadosYaGuardados.style.display = "none";
divSpanEmpleadosCustom.style.display = "none";
divInputsDePersonalExterno.style.display = "none";
divDosBotonesPersonal.style.display = "none";
divSpanNombresPersonalExterno.style.display = "none";
divHorasSalida.style.display = "none";
divHoraManual.style.display = "none";
divActividadesFinalesSalida.style.display = "none";


function mostrarDivReportarActividad(){
    interfazBotones.style.display = "none";
    divIngresarActividad.style.display = "block";
}

function regresarDivBotones(){
    divIngresarActividad.style.display = "none";
    interfazBotones.style.display = "block";
    divAgregerarPersonalAAsistencia.style.display = "none";

    const textoHoraActual = document.getElementById("horaActual");
    textoHoraActual.style.cssText = "font-size: 60px!important;";
    const textoFechaActual = document.getElementById("fechaActual");
    textoFechaActual.style.fontSize = "30px";
}


function mostrarDivAgregarPersonalAAsistencia(){
    interfazBotones.style.display = "none";
    divAgregerarPersonalAAsistencia.style.display = "block";

    const textoHoraActual = document.getElementById("horaActual");
    textoHoraActual.style.cssText = "font-size: 30px!important;";
    const textoFechaActual = document.getElementById("fechaActual");
    textoFechaActual.style.fontSize = "15px";
}

function mostrarSelectEmpleados(){
    var switchlabel2 = document.getElementById("switch-label2");
    if(switchlabel2.checked){
        divSelectEmpleado.style.display="block";
    }
    else{
        divSelectEmpleado.style.display="none";
    }
}

function guardarEmpleados(){
    var stringEmpleadosAgregados = "";

    //Contar el numero de empleados que se agregaron
    const select = document.getElementById("selectEmpleados");
    let contador = 0;
    for (let i = 0; i < select.options.length; i++) {
    if (select.options[i].selected) {
        contador++;
        if(contador == 1){
            stringEmpleadosAgregados = select.options[i].text;
        }
        else{
            stringEmpleadosAgregados = stringEmpleadosAgregados + ","+select.options[i].text;
        }
        
    }
    }
    console.log(contador);

    if (contador == 0){

    }
    else{
        var spanSwitchAgregarEmpleados = document.getElementById("spanSwitchAgregarEmpleados");
        spanSwitchAgregarEmpleados.style.display = "none";
        divSelectEmpleado.style.display="none";
    
        
    
        contadorEmpleadosGuardados = document.getElementById("contadorEmpleadosGuardados");
        contadorEmpleadosGuardados.innerHTML = contador.toString();
    
        textoContadorEmpleados = document.getElementById("textoContadorEmpleados");
        textoContadorEmpleados.style.display = "block";
    
        divEmpleadosYaGuardados.style.display = "block";
    
        var botonEditarEmpleadosAgregados = document.getElementById("botonEditarEmpleadosAgregados");
        botonEditarEmpleadosAgregados.style.display = "block";

        //Mostrar empleados seleccionados.. 
        var listadoEmpleadosCustom = document.getElementById("listadoEmpleadosCustom");
        listadoEmpleadosCustom.innerHTML = stringEmpleadosAgregados;
        var divSpanEmpleadosCustom = document.getElementById("divSpanEmpleadosCustom");
        divSpanEmpleadosCustom.style.display = "block";
    }
    
    

}


function volverAAgregarEmpleados(){
    var spanSwitchAgregarEmpleados = document.getElementById("spanSwitchAgregarEmpleados");
    spanSwitchAgregarEmpleados.style.display = "block";
    divSelectEmpleado.style.display="block";

    var botonEditarEmpleadosAgregados = document.getElementById("botonEditarEmpleadosAgregados");
    botonEditarEmpleadosAgregados.style.display = "none";

    textoContadorEmpleados = document.getElementById("textoContadorEmpleados");
    textoContadorEmpleados.style.display = "none";

    var divSpanEmpleadosCustom = document.getElementById("divSpanEmpleadosCustom");
    divSpanEmpleadosCustom.style.display = "none";
}


function mostrarDivPersonalExterno(){
    var switchlabel3 = document.getElementById("switch-label3");
    if(switchlabel3.checked){
        divInputsDePersonalExterno.style.display = "block";

        


    }
    else{
        divInputsDePersonalExterno.style.display = "none";
        
    }
}


var contadorPersonalExterno = 0;
var stringPersonalExterno = "";

function agregarUnPersonalExterno(){
    var nombrePersonalExterno = document.getElementById("nombrePersonalExterno");

    if (nombrePersonalExterno.value == ""){

    }else{
        contadorPersonalExterno = contadorPersonalExterno + 1;
        var mensaje = "";

        if (contadorPersonalExterno == 1){
            stringPersonalExterno = nombrePersonalExterno.value;
            mensaje = contadorPersonalExterno.toString()+" persona";
        }
        else{
            stringPersonalExterno = stringPersonalExterno+","+nombrePersonalExterno.value;
            mensaje = contadorPersonalExterno.toString()+" personas";

        }
        //Borrar texto de un input
        nombrePersonalExterno.value = "";
        var numeroPersonalExterno = document.getElementById("numeroPersonalExterno");

        numeroPersonalExterno.innerHTML = mensaje;


        divSpanNumeroPersonalExterno.style.display = "block";
        
        var botonSoloAgregarPersonal = document.getElementById("botonSoloAgregarPersonal")
        botonSoloAgregarPersonal.style.display = "none";

        var divDosBotonesPersonal = document.getElementById("divDosBotonesPersonal");
        divDosBotonesPersonal.style.display = "block";

        //Agregar lista de nombres a input, que estara oculto...
        var listaNombresPersonalExterno = document.getElementById("listaNombresPersonalExterno");
        listaNombresPersonalExterno.value = stringPersonalExterno;
    }
    
}


function finalizarPersonalExterno(){
    var stringNombresPersonalExterno = document.getElementById("stringNombresPersonalExterno");
    stringNombresPersonalExterno.innerHTML = stringPersonalExterno;
    divSpanNombresPersonalExterno.style.display = "block";

    var nombrePersonalExterno = document.getElementById("nombrePersonalExterno");
    nombrePersonalExterno.style.display = "none";
    divDosBotonesPersonal.style.display = "none";
}

function mostrarDivHorasSalida(){
    interfazBotones.style.display = "none";
    divActividadesFinalesSalida.style.display = "none";
    divHorasSalida.style.display = "block";
    divActividadesFinalesSalida.style.display = "block";

    const textoHoraActual = document.getElementById("horaActual");
    textoHoraActual.style.cssText = "font-size: 30px!important;";
    const textoFechaActual = document.getElementById("fechaActual");
    textoFechaActual.style.fontSize = "15px";
}
function regresarDivSalida(){
    console.log("REGRESAR");
    interfazBotones.style.display = "none";
    
}
function mostrarInputHoraManual(){
    var divBotonesHora = document.getElementById("divBotonesHora");
    divBotonesHora.style.display="none";
    divHoraManual.style.display="block";
        
}

function mostrarOpcionesHora(){

    divHoraManual.style.display = "none";
    var divBotonesHora = document.getElementById("divBotonesHora");
    divBotonesHora.style.display="block";
}

function mostrarDivActuvidadesRealizadas(){
    divHorasSalida.style.display = "none";
    divActividadesFinalesSalida.style.display = "block";
}

function clicBotonGuardarActividad(){
    var input = document.getElementById("activiadReportada");
    var boton = document.getElementById("botonAgregarActividad"); // Seleccionamos el boton de tipo submit

    if (input.value !== "") {
      boton.disabled = true; // Deshabilitamos el boton de submit
      return true;  // Si el input no está deshabilitado y tiene un valor, envía el formulario
      
    }
    return false;   // Si el input está deshabilitado o no tiene valor, no envía el formulario

}

function clicBotonAgregarPersonal(){
    var input2 = document.getElementById("actividadRealizadaPersonal");
    var botonPersonal = document.getElementById("botonAgregarPersonal"); // Seleccionamos el boton de tipo submit

    if (input2.value !== "") {
        botonPersonal.disabled = true; // Deshabilitamos el boton de submit
        return true;  // Si el input no está deshabilitado y tiene un valor, envía el formulario
      
    }
    return false;   // Si el input está deshabilitado o no tiene valor, no envía el formulario
}

function clicGuardarSalida(){
    var input3 = document.getElementById("actividadesRealizadas");
    var botonSalida = document.getElementById("botonSalida"); // Seleccionamos el boton de tipo submit

    if (input3.value !== "") {
        botonSalida.disabled = true; // Deshabilitamos el boton de submit
        return true;  // Si el input no está deshabilitado y tiene un valor, envía el formulario
      
    }
    return false;   // Si el input está deshabilitado o no tiene valor, no envía el formulario
}

$(document).ready(function() {
    $('#selectEmpleados').select2();
    tags: true;

});	