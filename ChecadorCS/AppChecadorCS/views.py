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
        
        #Datos de asistencia
        fechaAsistenciaMostrar = ""
        horaAsistenciaMostrar = ""
        proyectoMotivoMostrar = ""
        actividadesRealizadas = ""
        fechaSalidaMostrar = ""
        horaSalidaMostrar = ""
        
    
        
        horaEntrada = ""
        proyecto = ""
        listaEmpleadosConLaMismaAsistencia = []
        
        if consultaEntrada:
            empleadoTieneEntradaHoy = True #Si tiene una entrada
            for datosConsultaEntrada in consultaEntrada:
                
                #DATOS PARA INTERFAZ FINAL..
                fechaAsistenciaMostrar = datosConsultaEntrada.fecha_entrada
                horaAsistenciaMostrar = datosConsultaEntrada.hora_entrada
                
                
                
                #AQUI TERMINA
                
                
                fechaSalida = datosConsultaEntrada.fecha_salida
                
                horaEntrada = datosConsultaEntrada.hora_entrada
                proyecto = datosConsultaEntrada.proyecto_interno_id
                
                if proyecto == None:
                    proyecto = datosConsultaEntrada.motivo
                    proyectoMotivoMostrar = proyecto
                    
                    #Ver todos los empleados con esa misma asistencia en el proyecto o tarea
                    consultaEmpleadosConLaMismaAsistencia = AsistenciaProyectoForaneo.objects.filter(fecha_entrada = fechaEntrada, motivo = proyecto)
                     
                else:
                    consultaProyecto = Proyectos.objects.filter(id_proyecto = proyecto)
                     #Ver todos los empleados con esa misma asistencia en el proyecto o tarea
                    consultaEmpleadosConLaMismaAsistencia = AsistenciaProyectoForaneo.objects.filter(fecha_entrada = fechaEntrada, proyecto_interno_id = proyecto)
                    
                    for datoProyecto in consultaProyecto:
                        proyecto = "#"+datoProyecto.numero_proyecto_interno + " - "+datoProyecto.nombre_proyecto
                    proyectoMotivoMostrar = proyecto
                        
                   
                
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
                    actividadesRealizadas = datosConsultaEntrada.actividades_realizadas
                    fechaSalidaMostrar = fechaSalida
                    horaSalidaMostrar = datosConsultaEntrada.hora_salida
                
                
            
                
        else:
            empleadoTieneEntradaHoy = False
            empleadoTieneSalidaHoy = False
            
        
        
        
       
        if "actividadAgregada" in request.session:
            actividadAgregada = request.session["actividadAgregada"]
            del request.session["actividadAgregada"]
            
            return render(request,"registro/registro.html",{"nombresEmpleado":nombresEmpleado,"consultaProyectos":consultaProyectos,"listaEmpleados":listaEmpleados,
                                                            "actividadAgregada":actividadAgregada, "empleadoTieneEntradaHoy":empleadoTieneEntradaHoy,
                                                            "empleadoTieneSalidaHoy":empleadoTieneSalidaHoy, "horaEntrada":horaEntrada, "proyecto":proyecto,"listaEmpleadosConLaMismaAsistencia":listaEmpleadosConLaMismaAsistencia,
                                                            "fechaAsistenciaMostrar":fechaAsistenciaMostrar, "horaAsistenciaMostrar":horaAsistenciaMostrar, "proyectoMotivoMostrar":proyectoMotivoMostrar, "actividadesRealizadas":actividadesRealizadas, "fechaSalidaMostrar":fechaSalidaMostrar, "horaSalidaMostrar":horaSalidaMostrar})
            
        
        
        #Si se registra la entrada correctamente
        if "entradaRegistradaCorrectamente" in request.session:
            entradaRegistradaCorrectamente = request.session["entradaRegistradaCorrectamente"]
            del request.session["entradaRegistradaCorrectamente"]

            return render(request,"registro/registro.html",{"nombresEmpleado":nombresEmpleado,"consultaProyectos":consultaProyectos,"listaEmpleados":listaEmpleados,
                                                            "entradaRegistradaCorrectamente":entradaRegistradaCorrectamente, "empleadoTieneEntradaHoy":empleadoTieneEntradaHoy,
                                                            "empleadoTieneSalidaHoy":empleadoTieneSalidaHoy, "horaEntrada":horaEntrada, "proyecto":proyecto,"listaEmpleadosConLaMismaAsistencia":listaEmpleadosConLaMismaAsistencia,
                                                            "fechaAsistenciaMostrar":fechaAsistenciaMostrar, "horaAsistenciaMostrar":horaAsistenciaMostrar, "proyectoMotivoMostrar":proyectoMotivoMostrar, "actividadesRealizadas":actividadesRealizadas, "fechaSalidaMostrar":fechaSalidaMostrar, "horaSalidaMostrar":horaSalidaMostrar})
        
        #Si hay un error al registrar la entrada
        if "errorEnEntrada" in request.session:
            errorEnEntrada = request.session["errorEnEntrada"]
            del request.session["errorEnEntrada"]
            
            return render(request,"registro/registro.html",{"nombresEmpleado":nombresEmpleado,"consultaProyectos":consultaProyectos,"listaEmpleados":listaEmpleados,
                                                            "errorEnEntrada":errorEnEntrada, "empleadoTieneEntradaHoy":empleadoTieneEntradaHoy,
                                                            "empleadoTieneSalidaHoy":empleadoTieneSalidaHoy, "horaEntrada":horaEntrada, "proyecto":proyecto, "listaEmpleadosConLaMismaAsistencia":listaEmpleadosConLaMismaAsistencia,
                                                            "fechaAsistenciaMostrar":fechaAsistenciaMostrar, "horaAsistenciaMostrar":horaAsistenciaMostrar, "proyectoMotivoMostrar":proyectoMotivoMostrar, "actividadesRealizadas":actividadesRealizadas, "fechaSalidaMostrar":fechaSalidaMostrar, "horaSalidaMostrar":horaSalidaMostrar})
        #Si se añadieron los empleados correctamente
        if "empleadosAñadidosCorrectamente" in request.session:
            empleadosAñadidosCorrectamente = request.session["empleadosAñadidosCorrectamente"]
            del request.session["empleadosAñadidosCorrectamente"]
            
            return render(request,"registro/registro.html",{"nombresEmpleado":nombresEmpleado,"consultaProyectos":consultaProyectos,"listaEmpleados":listaEmpleados, "empleadoTieneEntradaHoy":empleadoTieneEntradaHoy,
                                                        "empleadoTieneSalidaHoy":empleadoTieneSalidaHoy, "horaEntrada":horaEntrada, "proyecto":proyecto, "listaEmpleadosConLaMismaAsistencia":listaEmpleadosConLaMismaAsistencia,
                                                        "empleadosAñadidosCorrectamente":empleadosAñadidosCorrectamente,
                                                        "fechaAsistenciaMostrar":fechaAsistenciaMostrar, "horaAsistenciaMostrar":horaAsistenciaMostrar, "proyectoMotivoMostrar":proyectoMotivoMostrar, "actividadesRealizadas":actividadesRealizadas, "fechaSalidaMostrar":fechaSalidaMostrar, "horaSalidaMostrar":horaSalidaMostrar})
            
            
        #Si hay un error al añadir empleados
        if "errorAñadirEmpleados" in request.session:
            errorAñadirEmpleados = request.session["errorAñadirEmpleados"]
            del request.session["errorAñadirEmpleados"]
            
            return render(request,"registro/registro.html",{"nombresEmpleado":nombresEmpleado,"consultaProyectos":consultaProyectos,"listaEmpleados":listaEmpleados, "empleadoTieneEntradaHoy":empleadoTieneEntradaHoy,
                                                        "empleadoTieneSalidaHoy":empleadoTieneSalidaHoy, "horaEntrada":horaEntrada, "proyecto":proyecto, "listaEmpleadosConLaMismaAsistencia":listaEmpleadosConLaMismaAsistencia,
                                                        "errorAñadirEmpleados":errorAñadirEmpleados,
                                                        "fechaAsistenciaMostrar":fechaAsistenciaMostrar, "horaAsistenciaMostrar":horaAsistenciaMostrar, "proyectoMotivoMostrar":proyectoMotivoMostrar, "actividadesRealizadas":actividadesRealizadas, "fechaSalidaMostrar":fechaSalidaMostrar, "horaSalidaMostrar":horaSalidaMostrar})
            
        if "salidaRegistradaCorrectamente" in request.session:
            salidaRegistradaCorrectamente = request.session["salidaRegistradaCorrectamente"]
            del request.session["salidaRegistradaCorrectamente"]
            
            return render(request,"registro/registro.html",{"nombresEmpleado":nombresEmpleado,"consultaProyectos":consultaProyectos,"listaEmpleados":listaEmpleados, "empleadoTieneEntradaHoy":empleadoTieneEntradaHoy,
                                                        "empleadoTieneSalidaHoy":empleadoTieneSalidaHoy, "horaEntrada":horaEntrada, "proyecto":proyecto, "listaEmpleadosConLaMismaAsistencia":listaEmpleadosConLaMismaAsistencia,
                                                        "salidaRegistradaCorrectamente":salidaRegistradaCorrectamente,
                                                        "fechaAsistenciaMostrar":fechaAsistenciaMostrar, "horaAsistenciaMostrar":horaAsistenciaMostrar, "proyectoMotivoMostrar":proyectoMotivoMostrar, "actividadesRealizadas":actividadesRealizadas, "fechaSalidaMostrar":fechaSalidaMostrar, "horaSalidaMostrar":horaSalidaMostrar}) 
           
        
        if "errorEnSalida" in request.session:
            errorEnSalida = request.session["errorEnSalida"]
            del request.session["errorEnSalida"]
            
            return render(request,"registro/registro.html",{"nombresEmpleado":nombresEmpleado,"consultaProyectos":consultaProyectos,"listaEmpleados":listaEmpleados, "empleadoTieneEntradaHoy":empleadoTieneEntradaHoy,
                                                        "empleadoTieneSalidaHoy":empleadoTieneSalidaHoy, "horaEntrada":horaEntrada, "proyecto":proyecto, "listaEmpleadosConLaMismaAsistencia":listaEmpleadosConLaMismaAsistencia,
                                                        "errorEnSalida":errorEnSalida,
                                                        "fechaAsistenciaMostrar":fechaAsistenciaMostrar, "horaAsistenciaMostrar":horaAsistenciaMostrar, "proyectoMotivoMostrar":proyectoMotivoMostrar, "actividadesRealizadas":actividadesRealizadas, "fechaSalidaMostrar":fechaSalidaMostrar, "horaSalidaMostrar":horaSalidaMostrar})
            
            
            
            
        return render(request,"registro/registro.html",{"nombresEmpleado":nombresEmpleado,"consultaProyectos":consultaProyectos,"listaEmpleados":listaEmpleados, "empleadoTieneEntradaHoy":empleadoTieneEntradaHoy,
                                                        "empleadoTieneSalidaHoy":empleadoTieneSalidaHoy, "horaEntrada":horaEntrada, "proyecto":proyecto, "listaEmpleadosConLaMismaAsistencia":listaEmpleadosConLaMismaAsistencia,
                                                        "fechaAsistenciaMostrar":fechaAsistenciaMostrar, "horaAsistenciaMostrar":horaAsistenciaMostrar, "proyectoMotivoMostrar":proyectoMotivoMostrar, "actividadesRealizadas":actividadesRealizadas, "fechaSalidaMostrar":fechaSalidaMostrar, "horaSalidaMostrar":horaSalidaMostrar})
        
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
            horaEntrada = horaManualInput+":00"
            
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

                stringNombresEmpleados = ""
                contadorEmpleados = 0
                
                for empleado in listaEmpleadosTelegram:
                    contadorEmpleados = contadorEmpleados +1
                    
                    if contadorEmpleados == 1:
                        stringNombresEmpleados = empleado + "\n"
                    else:
                        stringNombresEmpleados = stringNombresEmpleados+ empleado + " \n"
                            
                if conProyectoInterno:
                    consultaProyecto = Proyectos.objects.filter(id_proyecto = proyectoElegidoSelect)
                    for datoProyecto in consultaProyecto:
                        nombreProyecto = datoProyecto.nombre_proyecto
                        
                    mensaje = "\U0001F55B NUEVA ENTRADA \U0001F55B \n Proyecto: "+nombreProyecto+" \U0001F4BC \n \n "+stringNombresEmpleados+"\n"+"Actividad a realizar: "+actividadARealizar
                else:
                    mensaje = "\U0001F55B NUEVA ENTRADA \U0001F55B \n Sin proyecto, actividad: "+motivoProyectoInput+" \U0001F4BC \n \n "+stringNombresEmpleados+"\n"+"Actividad a realizar: "+actividadARealizar
                
                
                botCustom.sendMessage(idGrupoTelegram,mensaje)
            except Exception as e:
                print("An exception occurred",e)
            
            return redirect("/registro/")
        except Exception as e:
            print("ERROR:",e)
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
                    motivo = datosConsultaEntrada.motivo
                    
                    #Ver todos los empleados con esa misma asistencia en el proyecto o tarea
                    consultaEmpleadosConLaMismaAsistencia = AsistenciaProyectoForaneo.objects.filter(fecha_entrada = fechaEntrada, motivo = motivo)
                     
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
            
            if proyecto == None:
                mensaje = "\U0001F97E NUEVA ACTIVIDAD \U0001F97E \n Tarea: "+motivo+" \U0001F4BC \n \n "+stringNombresEmpleados+"\n"+"Nueva Actividad: "+activiadReportada
            else:
                mensaje = "\U0001F97E NUEVA ACTIVIDAD \U0001F97E \n Proyecto: "+proyecto+" \U0001F4BC \n \n "+stringNombresEmpleados+"\n"+"Nueva Actividad: "+activiadReportada
                
            botCustom.sendMessage(idGrupoTelegram,mensaje)
            
            request.session["actividadAgregada"] = "Actividad agregada satisfactoriamente!"
            
            return redirect("/registro/")
        except Exception as e:
            print("An exception occurred",e)
        
        
        
        
        
        
    else:
        return redirect("/login/")
    
    
def agregarPersonalAAsistencia(request):
    if "sesionIniciada" in request.session:
        idEmpleadoPrincipal = request.session["sesionIniciada"]
        
        consultaEmpleadoQueRegistro = Empleados.objects.filter(id_empleado = idEmpleadoPrincipal)
        for datoEmpleado in consultaEmpleadoQueRegistro:
            nombreCompletoEmpleado = datoEmpleado.nombre + " " + datoEmpleado.apellidos
            
        
        
        #Obtener lista de select
        listaEmpleadosExtras = request.POST.getlist('listaEmpleadosExtras') #Puede ser vacio o no..
        
        #Obtener lista de empleados
        listaNombresPersonalExterno = request.POST["listaNombresPersonalExterno"] #Puuese estar vacio o no..
        
        #Actividad realizada
        actividadRealizada = request.POST["actividadRealizada"]
        
        fechaAsistencia = datetime.now()
        horaEntrada = datetime.now().time()
        horaEntrada = horaEntrada.strftime("%H:%M:%S")
        
        #Consulta de la asistencia del empleado
        consultaAsistenciaEmpleado = AsistenciaProyectoForaneo.objects.filter(id_empleado_id = idEmpleadoPrincipal, fecha_entrada = fechaAsistencia)
        for datoConsulta in consultaAsistenciaEmpleado:
            proyecto = datoConsulta.proyecto_interno_id
            motivo = datoConsulta.motivo
        
        conProyectoInterno = False
        if proyecto == None:
            conProyectoInterno = False
        else:
            conProyectoInterno = True
        
        
        listaEmpleadosTelegram = []
        
        empleadosRegistroEntrada = []
        
        if len(listaEmpleadosExtras) > 0:
            #Si se selecciono un empleado customita extra
            for empleadoExtra in listaEmpleadosExtras:
                idEmpleadoExtra = int(empleadoExtra)
                empleadosRegistroEntrada.append(idEmpleadoExtra)
                
        try:      
            #De todos los empleados de custom
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
                                                                    proyecto_interno = Proyectos.objects.get(id_proyecto = proyecto),
                                                                    motivo = "",
                                                                    actividad_realizada = actividadRealizada,
                                                                    actividades_realizadas = "")
                else:
                    registroAsistencia = AsistenciaProyectoForaneo(id_empleado = Empleados.objects.get(id_empleado = idEmpleado),
                                                                    personal_externo = "",
                                                                    fecha_entrada = fechaAsistencia, 
                                                                    hora_entrada = horaEntrada,
                                                                    hora_salida = "", 
                                                                    motivo = motivo,
                                                                    actividad_realizada = actividadRealizada,
                                                                    actividades_realizadas = "")

                registroAsistencia.save() #Se guarda la asistencia del empleado
                
                #AUN NO SE CALCULARÁN LAS HORAS EXTRAS, YA HASTA LA SALIDA..

            #De todo el personal externo
            if listaNombresPersonalExterno != "":
                arregloListaNombresPersonalExterno = listaNombresPersonalExterno.split(",")
                
                for personaExterna in arregloListaNombresPersonalExterno:
                    nombrePersonaExterna = personaExterna
                    
                    listaEmpleadosTelegram.append("Personal externo: "+nombrePersonaExterna)
                    

                    if conProyectoInterno:
                    
                        registroAsistencia = AsistenciaProyectoForaneo(personal_externo = nombrePersonaExterna,
                                                                        fecha_entrada = fechaAsistencia, 
                                                                        hora_entrada = horaEntrada,
                                                                        hora_salida = "", 
                                                                        proyecto_interno = Proyectos.objects.get(id_proyecto = proyecto),
                                                                        motivo = "",
                                                                        actividad_realizada = actividadRealizada,
                                                                        actividades_realizadas = "")
                    else:
                        registroAsistencia = AsistenciaProyectoForaneo(personal_externo = nombrePersonaExterna,
                                                                        fecha_entrada = fechaAsistencia, 
                                                                        hora_entrada = horaEntrada,
                                                                        hora_salida = "", 
                                                                        motivo = motivo,
                                                                        actividad_realizada = actividadRealizada,
                                                                        actividades_realizadas = "")
                    

                    registroAsistencia.save() #Guardar registro de asistencia de personal externo sin horas extras de entrada..
            
            #Todo bien!
            request.session["empleadosAñadidosCorrectamente"] = "Se añadieron los empleados correctamente!"
            
            #NOTIFICAR POR TELEGRAM
            #Mandar notificación de telegram
            try:
                tokenTelegram = keysBotAsistencia.tokenBotAsistencia
                botCustom = telepot.Bot(tokenTelegram)

                idGrupoTelegram = keysBotAsistencia.idGrupoAsistencia

                stringNombresEmpleados = ""
                contadorEmpleados = 0
                
                for empleado in listaEmpleadosTelegram:
                    contadorEmpleados = contadorEmpleados +1
                    
                    if contadorEmpleados == 1:
                        stringNombresEmpleados = empleado + "\n"
                    else:
                        stringNombresEmpleados = stringNombresEmpleados+ empleado + " \n"
                            
                            
                if conProyectoInterno:
                    consultaProyecto = Proyectos.objects.filter(id_proyecto = proyecto)
                    for datoProyecto in consultaProyecto:
                        nombreProyecto = "#"+datoProyecto.numero_proyecto_interno + " - "+datoProyecto.nombre_proyecto
                        
                    
                    
                    mensaje = "\U0001F477 INCORPORACIÓN DE PERSONAL \U0001F477 \n Agregados por: "+nombreCompletoEmpleado+"\nProyecto: "+nombreProyecto+" \U0001F4BC \n \n "+stringNombresEmpleados+"\n"+"Actividad realizada: "+actividadRealizada
                else:
                    mensaje = "\U0001F477 INCORPORACIÓN DE PERSONAL \U0001F477 \n Agregados por: "+nombreCompletoEmpleado+"\nSin proyecto, actividad: "+motivo+" \U0001F4BC \n \n "+stringNombresEmpleados+"\n"+"Actividad realizada: "+actividadRealizada
                
                
                botCustom.sendMessage(idGrupoTelegram,mensaje)
            except Exception as e:
                print("An exception occurred",e)
            
            return redirect("/registro/")
        except Exception as e:
            print("Error: ",e)
            request.session["errorAñadirEmpleados"] = "Error al añadir empleado! Consultar a soporte!"
            return redirect("/registro/")
        
        
        
    else:
        return redirect("/login/")
    
    
def registrarSalida(request):
    if "sesionIniciada" in request.session:
        try:
            idEmpleadoPrincipal = request.session["sesionIniciada"]
            
            horaManualInput = request.POST["horaManualInput"] #Puuede estar vacio o no..
            fechaAsistencia = datetime.now()
            
            if horaManualInput == "":
                horaSalida = datetime.now().time()
                horaSalida = horaSalida.strftime("%H:%M:%S")
            else:
                horaSalida = horaManualInput+":00"

            actividadesRealizadas = request.POST["actividadesRealizadas"] 
            consultaAsistenciaEmpleado = AsistenciaProyectoForaneo.objects.filter(id_empleado_id = idEmpleadoPrincipal, fecha_salida__isnull = True)

            for datoAsistencia in consultaAsistenciaEmpleado:
                proyectoInterno = datoAsistencia.proyecto_interno    #O puede tener un id de proyecto o es None
                motivo = datoAsistencia.motivo   #O puede tener uun motivo o es ""
                fechaEntrada = datoAsistencia.fecha_entrada

            
                
            if proyectoInterno != None:
                consultaAsistenciaEmpleadosIguales = AsistenciaProyectoForaneo.objects.filter(fecha_entrada = fechaEntrada, fecha_salida__isnull = True, proyecto_interno_id = proyectoInterno)
                
            else: 
                consultaAsistenciaEmpleadosIguales = AsistenciaProyectoForaneo.objects.filter(fecha_entrada = fechaEntrada, motivo = motivo,fecha_salida__isnull = True)
                
            listaEmpleadosTelegram = []
            for asistencia in consultaAsistenciaEmpleadosIguales:
                idEmpleado = asistencia.id_empleado_id
                if idEmpleado == None:
                    personalExterno = asistencia.personal_externo
                    listaEmpleadosTelegram.append("Personal externo: "+personalExterno)
                    
                    if proyectoInterno != None:
                        actualizacionSalida = AsistenciaProyectoForaneo.objects.filter(fecha_entrada = fechaEntrada, fecha_salida__isnull = True, proyecto_interno_id = proyectoInterno, personal_externo = personalExterno).update(fecha_salida = fechaAsistencia, hora_salida = horaSalida, actividades_realizadas = actividadesRealizadas)
                    else: 
                        actualizacionSalida = AsistenciaProyectoForaneo.objects.filter(fecha_entrada = fechaEntrada, motivo = motivo,fecha_salida__isnull = True, personal_externo = personalExterno).update(fecha_salida = fechaAsistencia, hora_salida = horaSalida, actividades_realizadas = actividadesRealizadas)
                else:
                    
                    consultaEmpleado = Empleados.objects.filter(id_empleado = idEmpleado)
                    for datoEmpleado in consultaEmpleado:
                        nombreEmpleado = datoEmpleado.nombre + " "+datoEmpleado.apellidos
                    listaEmpleadosTelegram.append(nombreEmpleado)
                        
                    if proyectoInterno != None:
                        actualizacionSalida = AsistenciaProyectoForaneo.objects.filter(fecha_entrada = fechaEntrada, fecha_salida__isnull = True, proyecto_interno_id = proyectoInterno, id_empleado_id = idEmpleado).update(fecha_salida = fechaAsistencia, hora_salida = horaSalida, actividades_realizadas = actividadesRealizadas)
                    else: 
                        actualizacionSalida = AsistenciaProyectoForaneo.objects.filter(fecha_entrada = fechaEntrada, motivo = motivo,fecha_salida__isnull = True, id_empleado_id = idEmpleado).update(fecha_salida = fechaAsistencia, hora_salida = horaSalida, actividades_realizadas = actividadesRealizadas)
            
            #Todo bien!
            request.session["salidaRegistradaCorrectamente"] = "Salida registrada correctamente!"
            
            #NOTIFICAR POR TELEGRAM
            #Mandar notificación de telegram
            try:
                tokenTelegram = keysBotAsistencia.tokenBotAsistencia
                botCustom = telepot.Bot(tokenTelegram)

                idGrupoTelegram = keysBotAsistencia.idGrupoAsistencia

                stringNombresEmpleados = ""
                contadorEmpleados = 0
                
                for empleado in listaEmpleadosTelegram:
                    contadorEmpleados = contadorEmpleados +1
                    
                    if contadorEmpleados == 1:
                        stringNombresEmpleados = empleado + "\n"
                    else:
                        stringNombresEmpleados = stringNombresEmpleados+ empleado + " \n"
                            
                            
                if proyectoInterno != None:
                    consultaProyecto = Proyectos.objects.filter(id_proyecto = proyectoInterno)
                    for datoProyecto in consultaProyecto:
                        nombreProyecto = datoProyecto.nombre_proyecto
                        
                    mensaje = "\U0001F6A9 SALIDA REGISTRADA \U0001F6A9 \n Proyecto: "+nombreProyecto+" \U0001F4BC \n \n "+stringNombresEmpleados+"\n"+"Actividades realizadas: "+actividadesRealizadas
                else:
                    mensaje = "\U0001F6A9 SALIDA REGISTRADA \U0001F6A9 \n Sin proyecto, actividad: "+motivo+" \U0001F4BC \n \n "+stringNombresEmpleados+"\n"+"Actividades realizadas: "+actividadesRealizadas
                
                
                botCustom.sendMessage(idGrupoTelegram,mensaje)
            except Exception as e:
                print("An exception occurred", e)

            return redirect("/registro/")
        except Exception as e:
            request.session["errorEnSalida"] = "Error en salida! Consultar a soporte!"
            print("Ha ocurrido una excepción:", e)
            return redirect("/registro/")

                
                

        
            
        
        
        
        
        
    else:
        return redirect("/login/")
