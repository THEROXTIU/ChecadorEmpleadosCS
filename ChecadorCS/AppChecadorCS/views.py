from django.shortcuts import render,redirect
from datetime import datetime
from appCS.models import Empleados, Proyectos, AsistenciaProyectoForaneo

#Para mandar telegram
import telepot
from AppChecadorCS import keysBotAsistencia


# Create your views here.
def inicio(request):
    if "sesionIniciada" in request.session:
        return redirect('/registro/')
        ##fechaActual = datetime.now()
    else:
      
        return redirect("/login/")

def login(request):
    if "sesionIniciada" in request.session:
        return redirect('/registro/')
    else:
        if request.method == "POST":
            usuario = request.POST["usuario"]
            contrasena = request.POST["contrasena"]
            consultaEmpleado = Empleados.objects.filter(correo = usuario, activo = "A")

            if consultaEmpleado:
                for datoEmpleado in consultaEmpleado:
                    idEmpleado = datoEmpleado.id_empleado
                    pswdReal = datoEmpleado.contraseña

                if contrasena == pswdReal:
                    request.session["sesionIniciada"] = idEmpleado
                    return redirect('/registro/')
                else:
                    errorContrasena = True
                    return render(request,"login/login.html",{"errorContrasena":errorContrasena, "usuario":usuario})
                
            else:
                errorUsuario = True
                return render(request,"login/login.html",{"errorUsuario":errorUsuario})

        else:
            
            return render(request,"login/login.html")


def registro(request):
    if "sesionIniciada" in request.session:
        idEmpleado = request.session["sesionIniciada"]
        intIdEmpleado = int(idEmpleado)
        consultaEmpleado = Empleados.objects.filter(id_empleado = idEmpleado)
        for datoEmpleado in consultaEmpleado:
            nombresEmpleado = datoEmpleado.nombre
        consultaProyectos = Proyectos.objects.all()

        #Consulta de empleados exceptuando al empleado que está logueqado.

        consultaEmpleados = Empleados.objects.filter(correo__icontains = "@customco.com.mx", activo = "A")
        listaEmpleados = []

        for empleado in consultaEmpleados:
            idEmpleadofor = empleado.id_empleado
            if idEmpleadofor != intIdEmpleado:
                apellidoEmpleado = empleado.apellidos
                arregloApellidos = apellidoEmpleado.split(" ")

                nombreEmpleado = empleado.nombre + " "+arregloApellidos[0]
                listaEmpleados.append([idEmpleadofor, nombreEmpleado])
                
                
                
        #Verificar si el empleado ya tiene una entrada el dia de hoy, solo la entrada, porque puede tener una salida
        fechaEntrada = datetime.now()
        consultaEntrada = AsistenciaProyectoForaneo.objects.filter(id_empleado_id = idEmpleado, fecha_entrada = fechaEntrada)
        
        empleadoTieneEntradaHoy = False
        empleadoTieneSalidaHoy = False
        
        horaEntrada = ""
        proyecto = ""
        listaEmpleadosConLaMismaAsistencia = []
        
        if consultaEntrada:
            empleadoTieneEntradaHoy = True #Si tiene una entrada
            for datosConsultaEntrada in consultaEntrada:
                fechaSalida = datosConsultaEntrada.fecha_salida
                
                horaEntrada = datosConsultaEntrada.hora_entrada
                proyecto = datosConsultaEntrada.proyecto_interno_id
                
                if proyecto == None:
                    proyecto = datosConsultaEntrada.motivo
                    
                    #Ver todos los empleados con esa misma asistencia en el proyecto o tarea
                    consultaEmpleadosConLaMismaAsistencia = AsistenciaProyectoForaneo.objects.filter(fecha_entrada = fechaEntrada, motivo = proyecto)
                     
                else:
                    consultaProyecto = Proyectos.objects.filter(id_proyecto = proyecto)
                     #Ver todos los empleados con esa misma asistencia en el proyecto o tarea
                    consultaEmpleadosConLaMismaAsistencia = AsistenciaProyectoForaneo.objects.filter(fecha_entrada = fechaEntrada, proyecto_interno_id = proyecto)
                    
                    for datoProyecto in consultaProyecto:
                        proyecto = "#"+datoProyecto.numero_proyecto_interno + " - "+datoProyecto.nombre_proyecto
                        
                   
                
                for asistencia in consultaEmpleadosConLaMismaAsistencia:
                    idEmpleado = asistencia.id_empleado_id
                    
                    if idEmpleado == None:
                        personalExterno = asistencia.personal_externo
                        
                        listaEmpleadosConLaMismaAsistencia.append("Personal externo:"+personalExterno)
                    else:
                        
                    
                        consultaEmpleadoConLaMisma = Empleados.objects.filter(id_empleado = idEmpleado)
                        for dato in consultaEmpleadoConLaMisma:
                            nombreCompletoEmpleadoConLaMisma = dato.nombre + " " + dato.apellidos
                            
                        listaEmpleadosConLaMismaAsistencia.append(nombreCompletoEmpleadoConLaMisma)
                    
                        
                        
                    
                    
                
            if fechaSalida == None:
                empleadoTieneSalidaHoy = False
            else:
                empleadoTieneSalidaHoy = True
                
        else:
            empleadoTieneEntradaHoy = False
            empleadoTieneSalidaHoy = False
            
       
        if "actividadAgregada" in request.session:
            actividadAgregada = request.session["actividadAgregada"]
            del request.session["actividadAgregada"]
            
            return render(request,"registro/registro.html",{"nombresEmpleado":nombresEmpleado,"consultaProyectos":consultaProyectos,"listaEmpleados":listaEmpleados,
                                                            "actividadAgregada":actividadAgregada, "empleadoTieneEntradaHoy":empleadoTieneEntradaHoy,
                                                            "empleadoTieneSalidaHoy":empleadoTieneSalidaHoy, "horaEntrada":horaEntrada, "proyecto":proyecto,"listaEmpleadosConLaMismaAsistencia":listaEmpleadosConLaMismaAsistencia})
            
        
        

        if "entradaRegistradaCorrectamente" in request.session:
            entradaRegistradaCorrectamente = request.session["entradaRegistradaCorrectamente"]
            del request.session["entradaRegistradaCorrectamente"]

            return render(request,"registro/registro.html",{"nombresEmpleado":nombresEmpleado,"consultaProyectos":consultaProyectos,"listaEmpleados":listaEmpleados,
                                                            "entradaRegistradaCorrectamente":entradaRegistradaCorrectamente, "empleadoTieneEntradaHoy":empleadoTieneEntradaHoy,
                                                            "empleadoTieneSalidaHoy":empleadoTieneSalidaHoy, "horaEntrada":horaEntrada, "proyecto":proyecto,"listaEmpleadosConLaMismaAsistencia":listaEmpleadosConLaMismaAsistencia})
        
        if "errorEnEntrada" in request.session:
            errorEnEntrada = request.session["errorEnEntrada"]
            del request.session["errorEnEntrada"]
            
            return render(request,"registro/registro.html",{"nombresEmpleado":nombresEmpleado,"consultaProyectos":consultaProyectos,"listaEmpleados":listaEmpleados,
                                                            "errorEnEntrada":errorEnEntrada, "empleadoTieneEntradaHoy":empleadoTieneEntradaHoy,
                                                            "empleadoTieneSalidaHoy":empleadoTieneSalidaHoy, "horaEntrada":horaEntrada, "proyecto":proyecto, "listaEmpleadosConLaMismaAsistencia":listaEmpleadosConLaMismaAsistencia})


        return render(request,"registro/registro.html",{"nombresEmpleado":nombresEmpleado,"consultaProyectos":consultaProyectos,"listaEmpleados":listaEmpleados, "empleadoTieneEntradaHoy":empleadoTieneEntradaHoy,
                                                        "empleadoTieneSalidaHoy":empleadoTieneSalidaHoy, "horaEntrada":horaEntrada, "proyecto":proyecto, "listaEmpleadosConLaMismaAsistencia":listaEmpleadosConLaMismaAsistencia})
    else:
        return redirect("/login/")

def salir(request):
    del request.session["sesionIniciada"]
    return redirect("/login/")

def registrarEntrada(request):
    if "sesionIniciada" in request.session:
        idEmpleadoPrincipal = request.session["sesionIniciada"]
        
        horaManualInput = request.POST["horaManualInput"] #Puuede estar vacio o no..
        
        conProyectoInterno = False
        #checkbox de proyecto
        if request.POST.get("switchProyecto", False): #Checkeado
            motivoProyectoInput = request.POST["motivoProyectoInput"] #Se toma el motivo
            proyectoElegidoSelect = ""
        elif request.POST.get("switchProyecto", True): #No chequeado
            proyectoElegidoSelect = request.POST["proyectoElegidoSelect"] #Se toma el valor del select del empleado
            motivoProyectoInput = ""
            conProyectoInterno = True
        
        #Obtener lista de select
        listaEmpleadosExtras = request.POST.getlist('listaEmpleadosExtras') #Puede ser vacio o no..
        
        #Obtener lista de empleados
        listaNombresPersonalExterno = request.POST["listaNombresPersonalExterno"] #Puuese estar vacio o no..
        
        #Actividad realizada
        actividadARealizar = request.POST["actividadARealizar"]
        
        fechaAsistencia = datetime.now()
        if horaManualInput == "":
            horaEntrada = datetime.now().time()
            horaEntrada = horaEntrada.strftime("%H:%M:%S")
        else:
            horaEntrada = horaManualInput
            
        listaEmpleadosTelegram = []
            
        
        #Arreglo de empleados customitas
        empleadosRegistroEntrada = []
        empleadosRegistroEntrada.append(int(idEmpleadoPrincipal)) #Se agrega el empleado al arreglo
        
        if len(listaEmpleadosExtras) > 0:
            #Si se selecciono un empleado customita extra
            for empleadoExtra in listaEmpleadosExtras:
                idEmpleadoExtra = int(empleadoExtra)
                empleadosRegistroEntrada.append(idEmpleadoExtra)
          
        try:      
            for empleado in empleadosRegistroEntrada:
                idEmpleado = empleado
                
                consultaEmpleado = Empleados.objects.filter(id_empleado = idEmpleado)
                for datoEmpleado in consultaEmpleado:
                    nombreEmpleado = datoEmpleado.nombre + " " +datoEmpleado.apellidos
                    
                listaEmpleadosTelegram.append(nombreEmpleado)
                

                if conProyectoInterno:
                
                    registroAsistencia = AsistenciaProyectoForaneo(id_empleado = Empleados.objects.get(id_empleado = idEmpleado),
                                                                    personal_externo = "",
                                                                    fecha_entrada = fechaAsistencia, 
                                                                    hora_entrada = horaEntrada,
                                                                    hora_salida = "", 
                                                                    proyecto_interno = Proyectos.objects.get(id_proyecto = proyectoElegidoSelect),
                                                                    motivo = "",
                                                                    actividad_realizada = actividadARealizar,
                                                                    actividades_realizadas = "")
                else:
                    registroAsistencia = AsistenciaProyectoForaneo(id_empleado = Empleados.objects.get(id_empleado = idEmpleado),
                                                                    personal_externo = "",
                                                                    fecha_entrada = fechaAsistencia, 
                                                                    hora_entrada = horaEntrada,
                                                                    hora_salida = "", 
                                                                    motivo = motivoProyectoInput,
                                                                    actividad_realizada = actividadARealizar,
                                                                    actividades_realizadas = "")

                registroAsistencia.save() #Se guarda la asistencia del empleado
                
                #AUN NO SE CALCULARÁN LAS HORAS EXTRAS, YA HASTA LA SALIDA..
        
            if listaNombresPersonalExterno != "":
                arregloListaNombresPersonalExterno = listaNombresPersonalExterno.split(",")
                
                for personaExterna in arregloListaNombresPersonalExterno:
                    nombrePersonaExterna = personaExterna
                    
                    listaEmpleadosTelegram.append(nombrePersonaExterna)
                    

                    if conProyectoInterno:
                    
                        registroAsistencia = AsistenciaProyectoForaneo(personal_externo = nombrePersonaExterna,
                                                                        fecha_entrada = fechaAsistencia, 
                                                                        hora_entrada = horaEntrada,
                                                                        hora_salida = "", 
                                                                        proyecto_interno = Proyectos.objects.get(id_proyecto = proyectoElegidoSelect),
                                                                        motivo = "",
                                                                        actividad_realizada = actividadARealizar,
                                                                        actividades_realizadas = "")
                    else:
                        registroAsistencia = AsistenciaProyectoForaneo(personal_externo = nombrePersonaExterna,
                                                                        fecha_entrada = fechaAsistencia, 
                                                                        hora_entrada = horaEntrada,
                                                                        hora_salida = "", 
                                                                        motivo = motivoProyectoInput,
                                                                        actividad_realizada = actividadARealizar,
                                                                        actividades_realizadas = "")
                    

                    registroAsistencia.save() #Guardar registro de asistencia de personal externo sin horas extras de entrada..

            #Todo bien!
            request.session["entradaRegistradaCorrectamente"] = "Entrada registrada correctamente!"
            
            #NOTIFICAR POR TELEGRAM
            #Mandar notificación de telegram
            try:
                tokenTelegram = keysBotAsistencia.tokenBotAsistencia
                botCustom = telepot.Bot(tokenTelegram)

                idGrupoTelegram = keysBotAsistencia.idGrupoAsistencia

                if conProyectoInterno:
                    consultaProyecto = Proyectos.objects.filter(id_proyecto = proyectoElegidoSelect)
                    for datoProyecto in consultaProyecto:
                        nombreProyecto = datoProyecto.nombre_proyecto
                        
                    stringNombresEmpleados = ""
                    contadorEmpleados = 0
                    
                    for empleado in listaEmpleadosTelegram:
                        contadorEmpleados = contadorEmpleados +1
                        
                        if contadorEmpleados == 1:
                            stringNombresEmpleados = empleado + "\n"
                        else:
                            stringNombresEmpleados = stringNombresEmpleados+ empleado + " \n"
                    
                    mensaje = "\U0001F55B NUEVA ENTRADA \U0001F55B \n Proyecto: "+nombreProyecto+" \U0001F4BC \n \n "+stringNombresEmpleados+"\n"+"Actividad a realizar: "+actividadARealizar
                else:
                    mensaje = "\U0001F55B NUEVA ENTRADA \U0001F55B \n Sin proyecto, actividad: "+motivoProyectoInput+" \U0001F4BC \n \n "+stringNombresEmpleados+"\n"+"Actividad a realizar: "+actividadARealizar
                
                
                botCustom.sendMessage(idGrupoTelegram,mensaje)
            except:
                print("An exception occurred")
            
            return redirect("/registro/")
        except:
            request.session["errorEnEntrada"] = "Error en entrada! Consultar a soporte!"
            return redirect("/registro/")
            
        
        
        
        
        
    else:
        return redirect("/login/")


def reportarActividadEmpleado(request):
    if "sesionIniciada" in request.session:
        idEmpleadoPrincipal = request.session["sesionIniciada"]
        
        activiadReportada = request.POST["activiadReportada"]
        
        #Verificar si el empleado ya tiene una entrada el dia de hoy, solo la entrada, porque puede tener una salida
        fechaEntrada = datetime.now()
        consultaEntrada = AsistenciaProyectoForaneo.objects.filter(id_empleado_id = idEmpleadoPrincipal, fecha_entrada = fechaEntrada)
        
        
        proyecto = ""
        listaEmpleadosConLaMismaAsistencia = []
        
        if consultaEntrada:
            for datosConsultaEntrada in consultaEntrada:
                proyecto = datosConsultaEntrada.proyecto_interno_id
                
                if proyecto == None:
                    proyecto = datosConsultaEntrada.motivo
                    
                    #Ver todos los empleados con esa misma asistencia en el proyecto o tarea
                    consultaEmpleadosConLaMismaAsistencia = AsistenciaProyectoForaneo.objects.filter(fecha_entrada = fechaEntrada, motivo = proyecto)
                     
                else:
                    consultaProyecto = Proyectos.objects.filter(id_proyecto = proyecto)
                     #Ver todos los empleados con esa misma asistencia en el proyecto o tarea
                    consultaEmpleadosConLaMismaAsistencia = AsistenciaProyectoForaneo.objects.filter(fecha_entrada = fechaEntrada, proyecto_interno_id = proyecto)
                    
                    for datoProyecto in consultaProyecto:
                        proyecto = "#"+datoProyecto.numero_proyecto_interno + " - "+datoProyecto.nombre_proyecto
                        
                   
                
                for asistencia in consultaEmpleadosConLaMismaAsistencia:
                    idEmpleado = asistencia.id_empleado_id
                    
                    if idEmpleado == None:
                        personalExterno = asistencia.personal_externo
                        
                        listaEmpleadosConLaMismaAsistencia.append("Personal externo:"+personalExterno)
                    else:
                        
                    
                        consultaEmpleadoConLaMisma = Empleados.objects.filter(id_empleado = idEmpleado)
                        for dato in consultaEmpleadoConLaMisma:
                            nombreCompletoEmpleadoConLaMisma = dato.nombre + " " + dato.apellidos
                            
                        listaEmpleadosConLaMismaAsistencia.append(nombreCompletoEmpleadoConLaMisma)
                        
        stringNombresEmpleados = ""
        
        for empleado in listaEmpleadosConLaMismaAsistencia:
            stringNombresEmpleados = stringNombresEmpleados + empleado + "\n"
        
        try:
            tokenTelegram = keysBotAsistencia.tokenBotAsistencia
            botCustom = telepot.Bot(tokenTelegram)

            idGrupoTelegram = keysBotAsistencia.idGrupoAsistencia

                
            mensaje = "\U0001F97E NUEVA ACTIVIDAD \U0001F97E \n Proyecto: "+proyecto+" \U0001F4BC \n \n "+stringNombresEmpleados+"\n"+"Nueva Actividad: "+activiadReportada
            
            
            
            botCustom.sendMessage(idGrupoTelegram,mensaje)
            
            request.session["actividadAgregada"] = "Actividad agregada satisfactoriamente!"
            
            return redirect("/registro/")
        except:
            print("An exception occurred")
        
        
        
        
        
        
    else:
        return redirect("/login/")