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
var divPersonal = document.getElementById("divPersonal");
var divSelectEmpleado = document.getElementById("divSelectEmpleado");
var divEmpleadosYaGuardados = document.getElementById("divEmpleadosYaGuardados");
var divInputsDePersonalExterno = document.getElementById("divInputsDePersonalExterno");
var divSpanNumeroPersonalExterno = document.getElementById("divSpanNumeroPersonalExterno");
var divDosBotonesPersonal = document.getElementById("divDosBotonesPersonal");
var divSpanNombresPersonalExterno = document.getElementById("divSpanNombresPersonalExterno");



fechaActual.innerHTML = fechaHoy;
divHoraManualnual.style.display="none";
divProyectos.style.display="none";
divSinProyecto.style.display="none";
divPersonal.style.display="none";
divSelectEmpleado.style.display="none";
divEmpleadosYaGuardados.style.display = "none";
divInputsDePersonalExterno.style.display = "none";
divSpanNumeroPersonalExterno.style.display = "none";
divDosBotonesPersonal.style.display = "none";
divSpanNombresPersonalExterno.style.display = "none";

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

function mostrarDivPersonal(){
    divProyectos.style.display="none";
    divPersonal.style.display="block";
    //Hacer chiquita la fecha y la hora
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


$(document).ready(function() {
    $('#selectEmpleados').select2();
    tags: true;

});	