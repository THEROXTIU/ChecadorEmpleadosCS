                                                                                                                                                                                                                                                                                                                                                                                                                                               
#Librerías
from email.mime import text
import mimetypes
import os
import base64
from io  import BytesIO
from io import StringIO

#Renderizado
from django.http import response
from django.http.response import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from reportlab import cmp

#Importación de modelos
from appCS.models import Areas, Empleados, Equipos, Carta, Impresoras, Cartuchos, CalendarioMantenimiento, Programas, ProgramasArea, EquipoPrograma, Bitacora, Renovacion_Equipos, Renovacion_Impresoras, Preguntas, Encuestas, Respuestas, EncuestaEmpleadoResuelta, Mouses, Teclados, Monitores, ImplementacionSoluciones, Vehiculos, documentacionVehiculos, tenenciasVehiculos, serviciosVehiculos, alineacionyBalanceo, reparacionVehiculo, EvaluacionesDesempeno, IndicadorEvaluador, ResultadosDesempeno, EmpleadosCara, Asistencia, IncidenciaLlegadaTardia, IncidenciaSalidaTemprana, IncidenciaSalidaFuera, PermisosAsistencia, FaltasAsistencia, IncidenciaLlegadaTardia, IncidenciaSalidaTemprana, IncidenciaSalidaFuera, AsistenciaProyectoForaneo, AsistenciaProyectoForaneo, HorasExtras, AsistenciaProyectoForaneo, HorasExtrasForaneas, RelacionNFCEmpleado, Proyectos

#Librería para manejar archivos en Python
from django.core.files.base import ContentFile

#Librerías de fecha
from datetime import date, datetime
from datetime import timedelta
from calendar import calendar
from dateutil.relativedelta import relativedelta

#Archivo configuración Django
from django.conf import settings

#Correo
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

#Librerias reportes pdf
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm
from reportlab.platypus import Image, Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.graphics.shapes import Drawing 
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.barcharts import BarChart
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics import renderPDF

#Libreria excel.
import xlwt

#Para mandar telegram
import telepot
from appCS import keysBotCustom

import locale

#libreria PARA RECONOCIMIENTO FACIAL





def fotoAdmin(request):
    idadministrador=request.session["idSesion"]
    datosEmpleado = Empleados.objects.filter(id_empleado=idadministrador)
        
    for dato in datosEmpleado:
        foto = dato.imagen_empleado
        
    return foto

def accesoEmpleado(request):

    #Si ya existe una sesión
    if "idSesion" in request.session:
        if request.session['correoSesion'] == "adminSistemas0817":
                    
            return redirect('/inicio/') #redirecciona a url de inicio
        else:
            return redirect('/principal/') #redirecciona a la pagina normal del empleado

    #Si no hay una sesión iniciada
    else:

        #si se apretó el botón.
        if request.method == "POST":
            
            correousuario = request.POST['usernameEmpleado']
            

            datosUsuario = Empleados.objects.filter(correo=correousuario)

            #Si encontro a un usuario con ese correo...
            if datosUsuario:

                for dato in datosUsuario:
                    id = dato.id_empleado
                    nombres = dato.nombre
                    apellidos = dato.apellidos
                    correo = dato.correo
                    contraReal = dato.contraseña
                    
                #mandar correo...
                asunto = "CS | Solicitud de acceso de " + nombres + " " + apellidos
                plantilla = "empleadosCustom/solicitudAcceso/correo.html"
                html_mensaje = render_to_string(plantilla, {"nombre": nombres, "apellidos": apellidos, "correo": correo, "contraseña": contraReal})
                email_remitente = settings.EMAIL_HOST_USER
                email_destino = [correo]
                mensaje = EmailMessage(asunto, html_mensaje, email_remitente, email_destino)
                mensaje.content_subtype = 'html'
                mensaje.send()
                
                textoCorreo = "Se ha enviado un correo con tus datos de acceso."
                request.session['textoCorreo'] = textoCorreo #variable global.. 
                return redirect('/login/')
                    

            #Si no se encuentra a nadie con ese correo...
            else:
                hayError = True
                error = "No se ha encontrado al usuario"
                return render(request, "Login/accesoEmpleado.html", {"hayError":hayError, "textoError":error})

        #se carga la pagina por primera vez.
        return render(request, "Login/accesoEmpleado.html")


    
            

def principal(request):
    
    #Si ya hay una sesión iniciada..
    if "idSesion" in request.session:
        
        
        
        estaEnInicio = True
        id_admin=request.session["idSesion"]
        nombreini = request.session['nombres']
        apellidosini = request.session['apellidos']
        correo = request.session['correoSesion']
        foto = fotoAdmin(request)
        nombreCompleto = nombreini + " " + apellidosini #Blanca Yesenia Gaeta Talamantes

        if correo == "recursos.humanos@customco.com.mx":
            rh = True
        
        
            return render(request, "empleadosCustom/inicio/inicio.html", {"estaEnInicio":estaEnInicio,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo, 
            "rh": rh})
         #Agregar a codigo principal
        if correo == "almacen01@customco.com.mx":
            almacen = True
            solicitantePrestamo = True
            administradordeVehiculos = True

            return render(request, "empleadosCustom/inicio/inicio.html", {"estaEnInicio":estaEnInicio,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo, 
            "almacen": almacen, "solicitantePrestamo":solicitantePrestamo, "administradordeVehiculos":administradordeVehiculos})
        
        if correo == "egutierrez@customco.com.mx":
            subdirector = True
            return render(request, "empleadosCustom/inicio/inicio.html", {"estaEnInicio":estaEnInicio,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo, 
            "subdirector": subdirector})
            
        
        #Sacar el area
        empleado = Empleados.objects.filter(id_empleado = id_admin)
        for dato in empleado:
            area = dato.id_area_id
        
        if "recienIniciado" in request.session:
            del request.session['recienIniciado']
            recienIniciado = True

            if area == 1 or area ==5 or area == 7 or area == 8 or area == 9 or area == 10:
                if area == 5:
                    solicitantePrestamo = True
                    administradordeVehiculos = True
                    return render(request, "empleadosCustom/inicio/inicio.html", {"estaEnInicio":estaEnInicio,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo, "recienIniciado":recienIniciado, "solicitantePrestamo":solicitantePrestamo, "administradordeVehiculos":administradordeVehiculos})
                
                solicitantePrestamo = True
                return render(request, "empleadosCustom/inicio/inicio.html", {"estaEnInicio":estaEnInicio,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo, "recienIniciado":recienIniciado, "solicitantePrestamo":solicitantePrestamo})



            return render(request, "empleadosCustom/inicio/inicio.html", {"estaEnInicio":estaEnInicio,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo, "recienIniciado":recienIniciado})
        else:

            if area == 1 or area ==5 or area == 7 or area == 8 or area == 9 or area == 10:
                if area == 5:
                    solicitantePrestamo = True
                    administradordeVehiculos = True
                    return render(request, "empleadosCustom/inicio/inicio.html", {"estaEnInicio":estaEnInicio,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo, "solicitantePrestamo":solicitantePrestamo, "administradordeVehiculos":administradordeVehiculos})
                
                solicitantePrestamo = True
                return render(request, "empleadosCustom/inicio/inicio.html", {"estaEnInicio":estaEnInicio,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo, "solicitantePrestamo":solicitantePrestamo})

            
            return render(request, "empleadosCustom/inicio/inicio.html", {"estaEnInicio":estaEnInicio,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo})
    #Si le da al inicio y no hay una sesión iniciada..
    else:
        return redirect('/login/') #redirecciona a url de inicio


def encuestas(request):
    
    #Si ya hay una sesión iniciada..
    if "idSesion" in request.session:
        
        
        
        enAño = True
        estaEnEncuesta = True
        id_admin=request.session["idSesion"]
        nombreini = request.session['nombres']
        apellidosini = request.session['apellidos']
        correo = request.session['correoSesion']
        foto = fotoAdmin(request)
        nombreCompleto = nombreini + " " + apellidosini #Blanca Yesenia Gaeta Talamantes
        if correo  == "recursos.humanos@customco.com.mx":
            rh = True
        else:
            rh= False

        if correo == "almacen01@customco.com.mx":
            almacen = True
        else:
            almacen=False

        if correo == "egutierrez@customco.com.mx":
            subdirector = True
        else:
            subdirector = False

        solicitantePrestamo = False
        administradordeVehiculos = False

        empleado = Empleados.objects.filter(id_empleado = id_admin)
        for dato in empleado:
            area = dato.id_area_id

        if area == 1 or area ==5 or area == 7 or area == 8 or area == 9 or area == 10:
            solicitantePrestamo = True
            if area == 5:
                administradordeVehiculos = True
        else:
            solicitantePrestamo = False
            administradordeVehiculos = False

        preguntas = Preguntas.objects.filter(id_encuesta = 1)
        
        empleado = Empleados.objects.filter(id_empleado = id_admin)
        for dato in empleado:
            area = dato.id_area_id
            
        

        preguntasMultiples = []
        preguntasAbiertas = []
        preguntasAbiertas2 =[]
        contadorPreguntas = 0
        for pregunta in preguntas:
            id_pregunta = pregunta.id_pregunta
            texto_pregunta = pregunta.pregunta
            tipo = pregunta.tipo
            clasificacionPregunta = pregunta.clasificacion

            if tipo== "M":
                preguntasMultiples.append([id_pregunta, texto_pregunta, clasificacionPregunta])
                contadorPreguntas = contadorPreguntas +1 
            else:
                preguntasAbiertas.append([id_pregunta, texto_pregunta])
                preguntasAbiertas2.append([id_pregunta,texto_pregunta])
                contadorPreguntas = contadorPreguntas +1 

        

        #Condicion para saber si el empleado ya contesto algo..

        empleadoTieneRespuestas = Respuestas.objects.filter(id_empleado = id_admin) #Consulta a la tabla de respuestas para ver si alguna tiene el id del empleado

        #Si el empleado ya tiene aunque sea una pregunta resuelta..
        if empleadoTieneRespuestas:
            aunqueseaunapregunta = True
            contadorRespuestas = 0
            for respuesta in empleadoTieneRespuestas:
                contadorRespuestas = contadorRespuestas + 1

            porcentajeBarraint = (contadorRespuestas*100)/29
            porcentajeBarraintDecimales = round(porcentajeBarraint,2)
            porcentajeBarra = str(porcentajeBarraintDecimales)
            colorBarra =""
            if porcentajeBarraintDecimales <= 33:
                colorBarra = "progress-bar-danger"
            elif porcentajeBarraintDecimales >33 and porcentajeBarraintDecimales <=66:
                colorBarra = "progress-bar-warning"
            elif porcentajeBarraintDecimales >66:
                colorBarra = "progress-bar-success"

            return render(request, "empleadosCustom/encuestas/año2022/encuestaEnero.html", {"enAño":enAño, "estaEnEncuesta": estaEnEncuesta, "preguntasMultiples":preguntasMultiples,"preguntasAbiertas":preguntasAbiertas,"preguntasAbiertas2":preguntasAbiertas2, "id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo,
            "aunqueseaunapregunta":aunqueseaunapregunta, "contadorPreguntas": contadorPreguntas, "contadorRespuestas":contadorRespuestas, "rh": rh,"almacen":almacen, "solicitantePrestamo":solicitantePrestamo, "porcentajeBarra":porcentajeBarra, "colorBarra":colorBarra, "subdirector":subdirector, "administradordeVehiculos":administradordeVehiculos})

        #Si el empleado no tiene ninguna pregunta resuelta
        else:
            #Mostrar solo la introducción.
            aunqueseaunapregunta = False
            introduccion = True
        
        
            return render(request, "empleadosCustom/encuestas/año2022/encuestaEnero.html", {"enAño":enAño, "estaEnEncuesta": estaEnEncuesta, "preguntasMultiples":preguntasMultiples,"preguntasAbiertas":preguntasAbiertas,"preguntasAbiertas2":preguntasAbiertas2, "id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo,
            "aunqueseaunapregunta":aunqueseaunapregunta, "contadorPreguntas": contadorPreguntas, "introduccion":introduccion, "rh": rh,"almacen":almacen, "solicitantePrestamo":solicitantePrestamo, "subdirector":subdirector, "administradordeVehiculos":administradordeVehiculos})
    
    #Si le da al inicio y no hay una sesión iniciada..
    else:
        return redirect('/login/') #redirecciona a url de inicio

def resultadosEncuestas(request):
    
    #Si ya hay una sesión iniciada..
    if "idSesion" in request.session:
        
        
        
        enAño = True
        estaEnReseultados = True
        rh= True
        id_admin=request.session["idSesion"]
        nombreini = request.session['nombres']
        apellidosini = request.session['apellidos']
        correo = request.session['correoSesion']
        foto = fotoAdmin(request)
        nombreCompleto = nombreini + " " + apellidosini #Blanca Yesenia Gaeta Talamantes

        empleadosActivos = Empleados.objects.filter(activo = "A", correo__icontains="@customco.com.mx")
        contadorEmpleadosActivos = 0

        for activos in empleadosActivos:
            contadorEmpleadosActivos = contadorEmpleadosActivos + 1

        empleadosContestados = EncuestaEmpleadoResuelta.objects.filter(id_encuesta = 1)
        contadorEmpleadoscontestados = 0

        for contestado in empleadosContestados:
            contadorEmpleadoscontestados = contadorEmpleadoscontestados + 1

        empleadosFaltantes = contadorEmpleadosActivos - contadorEmpleadoscontestados

        br = " <br> "
        empleadosIrresponsables = ""

            
        idsContestados = []
        idsActivos = []

        for empleadosTotales in empleadosActivos:

            idEmpleado = empleadosTotales.id_empleado
            idsActivos.append(str(idEmpleado))



        for empleadosResueltos in empleadosContestados:

            id_empleado = empleadosResueltos.id_empleado_id
            idsContestados.append(str(id_empleado))

        for activos in idsActivos:
            if activos in idsContestados:
                yaContesto = True
            else:
                datosEmpleadoSinContestar = Empleados.objects.filter(id_empleado = activos)

                for datos in datosEmpleadoSinContestar:
                    nombres = datos.nombre
                    apellidos = datos.apellidos
                
                nombreCompleto2= nombres + " " + apellidos

                empleadosIrresponsables += nombreCompleto2 + br
                


        porcentaje = (contadorEmpleadoscontestados * 100) / contadorEmpleadosActivos

        pregMultiples = []
        pregAbiertas =[]
        porcentajesPreguntasMultiples = []
        contadorSiNo = []

        preguntas = Preguntas.objects.filter(id_encuesta = 1)

        for pregunta in preguntas:
            id_pregunta = pregunta.id_pregunta
            texto = pregunta.pregunta
            tipo = pregunta.tipo
            clasificacion = pregunta.clasificacion

            if tipo == "M":
                pregMultiples.append([id_pregunta, texto, clasificacion])

            elif tipo == "A":
                pregAbiertas.append([id_pregunta, texto])
        
        
        for multiple in pregMultiples:
            respuestasFinalizadas = []
            idPregunta = multiple[0]

            

            respuestas = Respuestas.objects.filter(id_pregunta =idPregunta) #en este caso devuelve dos respuestas de dos diferentes empleados
            cont = 0
            for datos in respuestas:
                empleadoID = datos.id_empleado_id

                encuestaEmpleado = EncuestaEmpleadoResuelta.objects.filter(id_encuesta = 1, id_empleado = empleadoID)

                if encuestaEmpleado:
                    preguntaID = datos.id_pregunta_id
                    respuestaEm = datos.respuesta
                    respuestasFinalizadas.append(respuestaEm)
                    cont = cont +1
                    
            contadorSI = 0
            contadorNO = 0
            for respuesta in respuestasFinalizadas:
                res = respuesta #SI o NO
                
                if res == "SI":
                    contadorSI = contadorSI + 1
                elif res == "NO":
                    contadorNO = contadorNO +1
                
            contadorSiNo.append([contadorSI, contadorNO])
            
            if contadorSI == 0 and cont == 0:
                porcentajePregunta = 0
                p = 0
            else:
                
                porcentajePregunta = (contadorSI * 100)/ cont
                p = ("{0:.2f}".format(float(porcentajePregunta)))
            
            criterio = ""
            if porcentajePregunta >= 90 and porcentajePregunta <= 100:
                criterio = "EXCELENTE"
            elif porcentajePregunta >= 80 and porcentajePregunta <= 89:
                criterio = "MUY BUENO"
            elif porcentajePregunta >= 70 and porcentajePregunta <= 79:
                criterio = "BUENO"
            elif porcentajePregunta >= 60 and porcentajePregunta <= 69:
                criterio = "REGULAR"
            elif porcentajePregunta >= 0 and porcentajePregunta <= 59:
                criterio = "DEFICIENTE"

            porcentajesPreguntasMultiples.append([float(p),criterio])

        listaMultiples = zip(pregMultiples,porcentajesPreguntasMultiples, contadorSiNo)
        listaMultiples2 = zip(pregMultiples,porcentajesPreguntasMultiples, contadorSiNo)

        suma = 0

        for porcentajesMultiples in porcentajesPreguntasMultiples:
            porcentajeSuma = porcentajesMultiples[0]
            suma = suma + porcentajeSuma

        contadorPreguntasMultiples = 0

        for m in pregMultiples:

            contadorPreguntasMultiples = contadorPreguntasMultiples + 1

        promedio = suma / contadorPreguntasMultiples

        criterioPromedio = ""
        if promedio >= 90 and promedio <= 100:
            criterioPromedio = "EXCELENTE"
        elif promedio >= 80 and promedio <= 89:
            criterioPromedio = "MUY BUENO"
        elif promedio >= 70 and promedio <= 79:
            criterioPromedio = "BUENO"
        elif promedio >= 60 and promedio <= 69:
            criterioPromedio = "REGULAR"
        elif promedio >= 0 and promedio <= 59:
            criterioPromedio = "DEFICIENTE"

        numeros =[1,2]


        return render(request, "empleadosCustom/encuestas/año2022/resultadosEnero.html", {"enAño":enAño, "estaEnReseultados": estaEnReseultados, "id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo,
              "rh":rh, "contadorEmpleadosActivos":contadorEmpleadosActivos, "contadorEmpleadoscontestados":contadorEmpleadoscontestados, "porcentaje":porcentaje, "pregMultiples":pregMultiples, "pregAbiertas":pregAbiertas,
              "porcentajesPreguntasMultiples":porcentajesPreguntasMultiples,"listaMultiples":listaMultiples, "promedio":promedio, "criterioPromedio": criterioPromedio, "numeros":numeros, "listaMultiples2":listaMultiples2, "empleadosFaltantes":empleadosFaltantes
              , "empleadosIrresponsables":empleadosIrresponsables, "idsActivos":idsActivos, "idsContestados":idsContestados })
    
    #Si le da al inicio y no hay una sesión iniciada..
    else:
        return redirect('/login/') #redirecciona a url de inicio

def guardarRespuesta(request):
    
    #Si ya hay una sesión iniciada..
    if "idSesion" in request.session:
        
        
        
        enAño = True
        estaEnEncuesta = True
        id_admin=request.session["idSesion"]
        nombreini = request.session['nombres']
        apellidosini = request.session['apellidos']
        correo = request.session['correoSesion']
        foto = fotoAdmin(request)
        nombreCompleto = nombreini + " " + apellidosini #Blanca Yesenia Gaeta Talamantes

        if request.method == "POST":
            
            empleadoID = request.POST['empleadoEncuesta']
            id_pregunta = request.POST['preguntaID']
            respuesta = ""
            nameInput = "respuesta"

            if request.POST.get(nameInput, False): #Checkeado
                respuesta = "SI"
            elif request.POST.get(nameInput, True): #No checkeado
                respuesta = "NO"

         

            registroRespuesta = Respuestas(id_pregunta = Preguntas.objects.get(id_pregunta = id_pregunta), id_empleado = Empleados.objects.get(id_empleado = empleadoID), respuesta = respuesta)
            registroRespuesta.save()

        
        return redirect('/encuestas/') #redirecciona a url de inicio
   
        

        
        

    
    #Si le da al inicio y no hay una sesión iniciada..
    else:
        return redirect('/login/') #redirecciona a url de inicio


def guardarRespuestaTextbox(request):
    
    #Si ya hay una sesión iniciada..
    if "idSesion" in request.session:
        
        
        
        enAño = True
        estaEnEncuesta = True
        id_admin=request.session["idSesion"]
        nombreini = request.session['nombres']
        apellidosini = request.session['apellidos']
        correo = request.session['correoSesion']
        foto = fotoAdmin(request)
        nombreCompleto = nombreini + " " + apellidosini #Blanca Yesenia Gaeta Talamantes

        if request.method == "POST":
            
            empleadoID = request.POST['empleadoEncuesta']
            id_pregunta = request.POST['preguntaID']
            respuesta = request.POST['respuestaText']

            registroRespuesta = Respuestas(id_pregunta = Preguntas.objects.get(id_pregunta = id_pregunta), id_empleado = Empleados.objects.get(id_empleado = empleadoID), respuesta = respuesta)
            registroRespuesta.save()

            numeroPreguntas = Preguntas.objects.filter(id_encuesta = 1)
            contadorPreguntas = 0
            for pregunta in numeroPreguntas:
                contadorPreguntas = contadorPreguntas +1

            respuestasEmpleado = Respuestas.objects.filter(id_empleado = id_admin) #4 registros

            contadorRespuestas = 0
            for respuesta in respuestasEmpleado:
                contadorRespuestas = contadorRespuestas +1

            if (contadorRespuestas == contadorPreguntas):
                registroEmpleadoCompletoEncuesta = EncuestaEmpleadoResuelta(id_empleado = Empleados.objects.get(id_empleado = id_admin), id_encuesta = Encuestas.objects.get(id_encuesta = 1))
                registroEmpleadoCompletoEncuesta.save()


        
        return redirect('/encuestas/') #redirecciona a url de inicio
   
        

        
        

    
    #Si le da al inicio y no hay una sesión iniciada..
    else:
        return redirect('/login/') #redirecciona a url de inicio


def verRespuestasAbiertas(request):
    
    #Si ya hay una sesión iniciada..
    if "idSesion" in request.session:
        
        
        
        enAño = True
        estaEnReseultados = True
        rh= True
        id_admin=request.session["idSesion"]
        nombreini = request.session['nombres']
        apellidosini = request.session['apellidos']
        correo = request.session['correoSesion']
        foto = fotoAdmin(request)
        nombreCompleto = nombreini + " " + apellidosini #Blanca Yesenia Gaeta Talamantes

        if request.method == "POST":
            
            pregunta = request.POST['idPregunta']

            datosPregunta = Preguntas.objects.filter(id_pregunta=pregunta)

            for datos in datosPregunta:
                idPregunta = datos.id_pregunta
                texto = datos.pregunta

            datosRespuestas = Respuestas.objects.filter(id_pregunta = idPregunta)





        


        return render(request, "empleadosCustom/encuestas/año2022/verRespuestasAbiertas.html", {"enAño":enAño, "estaEnReseultados": estaEnReseultados, "id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo,
              "rh":rh, "idPregunta": idPregunta, "texto":texto, "datosRespuestas": datosRespuestas})
    
    #Si le da al inicio y no hay una sesión iniciada..
    else:
        return redirect('/login/') #redirecciona a url de inicio


def equipo(request):
    
    #Si ya hay una sesión iniciada..
    if "idSesion" in request.session:
        
        
        estaEnVerEquipo = True
        id_admin=request.session["idSesion"]
        nombreini = request.session['nombres']
        apellidosini = request.session['apellidos']
        correo = request.session['correoSesion']
        foto = fotoAdmin(request)
        nombreCompleto = nombreini + " " + apellidosini #Blanca Yesenia Gaeta Talamantes
        if correo  == "recursos.humanos@customco.com.mx":
            rh = True
        else:
            rh= False
        if correo  == "almacen01@customco.com.mx":
            almacen = True
        else:
            almacen= False
        
        if correo == "egutierrez@customco.com.mx":
            subdirector = True
        else:
            subdirector = False

        

        #Codigo de info equipos.
        datosEquipo = Equipos.objects.filter(id_empleado =id_admin)
        
                #Si hay un equipo asignado a es empleado...
        if datosEquipo: 
            tieneEquipo = True  

            #Sacar datos del empleado
            datosPropietario= Empleados.objects.filter(id_empleado=id_admin)
            for datos in datosPropietario:
                nombre= datos.nombre
                apellidos=datos.apellidos
                nombreEmpleado= nombre + " " + apellidos
                departamento=datos.id_area_id
                datosDepa= Areas.objects.filter(id_area=departamento)
                for datos in datosDepa:
                    nombreArea= datos.nombre
                    colorArea=datos.color
            empleado = Empleados.objects.filter(id_empleado = id_admin)
            
            for dato in empleado:
                area = dato.id_area_id

            if area == 1 or area ==5 or area == 7 or area == 8 or area == 9 or area == 10:
                solicitantePrestamo = True
                if area == 5:
                    administradordeVehiculos = True
                else:
                    administradordeVehiculos = False
            else:
                solicitantePrestamo = False
                administradordeVehiculos = False
        

            #Sacar id de equipo para consultar renovación
            for dato in datosEquipo:
                id_equipo = dato.id_equipo

            #Sacar datos de renovación
            datosRenovacion= Renovacion_Equipos.objects.filter(id_equipo=id_equipo)
            for datos in datosRenovacion:
                compra= datos.fecha_compra
                renovar=  datos.fecha_renov
                        
            
            #Verificar si tiene mantenimientos.      
            mantenimientos= CalendarioMantenimiento.objects.filter(id_equipo_id__id_equipo=id_equipo)
            mouses = Mouses.objects.filter(id_equipo = id_equipo)
            teclados = Teclados.objects.filter(id_equipo = id_equipo)
            monitores = Monitores.objects.filter(id_equipo = id_equipo)
                        
            if mouses or  mantenimientos or teclados or monitores:
                return render(request, "empleadosCustom/miEquipo/verInfoEquipo.html", { "estaEnVerEquipo": estaEnVerEquipo, "id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo,
                "tieneEquipo":tieneEquipo, "datosPropietario":datosPropietario, "nombreEmpleado":nombreEmpleado, "nombreArea":nombreArea, "colorArea":colorArea, "compra":compra, "renovar":renovar, "mantenimientos":mantenimientos, "datosEquipo": datosEquipo,  "rh":rh, 
                "mouses":mouses,"teclados":teclados,"monitores":monitores,"almacen":almacen, "solicitantePrestamo":solicitantePrestamo, "subdirector":subdirector, "administradordeVehiculos":administradordeVehiculos})
            else:
                return render(request, "empleadosCustom/miEquipo/verInfoEquipo.html", { "estaEnVerEquipo": estaEnVerEquipo, "id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo,
                "tieneEquipo":tieneEquipo, "datosPropietario":datosPropietario, "nombreEmpleado":nombreEmpleado,"nombreArea":nombreArea, "colorArea":colorArea, "compra":compra, "renovar":renovar, "datosEquipo": datosEquipo,  "rh":rh,"almacen":almacen, "solicitantePrestamo":solicitantePrestamo, "subdirector":subdirector, "administradordeVehiculos":administradordeVehiculos})
                    
        else:
            noTieneEquipo = True
            return render(request, "empleadosCustom/miEquipo/verInfoEquipo.html", { "estaEnVerEquipo": estaEnVerEquipo, "id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo,
            "noTieneEquipo":noTieneEquipo,  "rh":rh,"almacen":almacen, "solicitantePrestamo":solicitantePrestamo, "subdirector":subdirector,"administradordeVehiculos":administradordeVehiculos})
    
    #Si le da al inicio y no hay una sesión iniciada..
    else:
        return redirect('/login/') #redirecciona a url de inicio

def carta(request):
    
    #Si ya hay una sesión iniciada..
    if "idSesion" in request.session:
        
        
        
      
        estaEnVerCarta = True
        id_admin=request.session["idSesion"]
        nombreini = request.session['nombres']
        apellidosini = request.session['apellidos']
        correo = request.session['correoSesion']
        foto = fotoAdmin(request)
        nombreCompleto = nombreini + " " + apellidosini #Blanca Yesenia Gaeta Talamantes
        if correo  == "recursos.humanos@customco.com.mx":
            rh = True
        else:
            rh= False
        if correo  == "almacen01@customco.com.mx":
            almacen = True
        else:
            almacen= False 
        if correo == "egutierrez@customco.com.mx":
            subdirector = True
        else:
            subdirector = False

        empleado = Empleados.objects.filter(id_empleado = id_admin)
        for dato in empleado:
            area = dato.id_area_id

        if area == 1 or area ==5 or area == 7 or area == 8 or area == 9 or area == 10:
            solicitantePrestamo = True
            if area == 5:
                administradordeVehiculos = True
            else:
                administradordeVehiculos = False
        else:
            solicitantePrestamo = False
            administradordeVehiculos = False

        datosRegistro = Carta.objects.filter(id_empleado = id_admin)
        
        empleados=[]
        equipos=[]
        
        for registros in datosRegistro:
            empleado= registros.id_empleado_id
            equipo = registros.id_equipo_id
            
            datosEmpleado = Empleados.objects.filter(id_empleado=empleado)
            for datos in datosEmpleado:
                nombres= datos.nombre
                apellido= datos.apellidos
                
            datosEquipos =Equipos.objects.filter(id_equipo=equipo)
            for datos in datosEquipos:
                marca=datos.marca
                modelo=datos.modelo
                
            empleados.append([nombres,apellido])
            equipos.append([marca, modelo])
        
        lista1=zip(datosRegistro,empleados,equipos)
        
        
        return render(request, "empleadosCustom/miEquipo/verCartaResponsiva.html", { "estaEnVerCarta": estaEnVerCarta, "id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo, "lista1":lista1,  "rh":rh, "almacen":almacen,"solicitantePrestamo":solicitantePrestamo, "subdirector":subdirector,"administradordeVehiculos":administradordeVehiculos})

    
    #Si le da al inicio y no hay una sesión iniciada..
    else:
        return redirect('/login/') #redirecciona a url de inicio

def directorio(request):
    
    #Si ya hay una sesión iniciada..
    if "idSesion" in request.session:
        
        
        
      
        estaEnVerCorreos = True
        id_admin=request.session["idSesion"]
        nombreini = request.session['nombres']
        apellidosini = request.session['apellidos']
        correo = request.session['correoSesion']
        foto = fotoAdmin(request)
        nombreCompleto = nombreini + " " + apellidosini #Blanca Yesenia Gaeta Talamantes
        if correo  == "recursos.humanos@customco.com.mx":
            rh = True
        else:
            rh= False

        if correo  == "almacen01@customco.com.mx":
            almacen = True
        else:
            almacen= False 

        if correo == "egutierrez@customco.com.mx":
            subdirector = True
        else:
            subdirector = False

        empleado = Empleados.objects.filter(id_empleado = id_admin)
        for dato in empleado:
            area = dato.id_area_id

        if area == 1 or area ==5 or area == 7 or area == 8 or area == 9 or area == 10:
            solicitantePrestamo = True
            if area == 5:
                administradordeVehiculos = True
            else:
                administradordeVehiculos = False
        else:
            solicitantePrestamo = False
            administradordeVehiculos = False 

        empleadosActivos = Empleados.objects.filter(activo__icontains= "A", correo__icontains = "customco.com.mx")
        
        #empleados Actvos
        areasEnActivos = []
        datosAreasEnActivos = []
        
        for empleado in empleadosActivos:
            areasEnActivos.append(empleado.id_area_id)
            
        for id in areasEnActivos:
            datosArea = Areas.objects.filter(id_area = id) 
            
            if datosArea:
                for dato in datosArea:
                    nombreArea = dato.nombre
                    colorArea = dato.color
            
            datosAreasEnActivos.append([nombreArea, colorArea])
            
        lista = zip(empleadosActivos, datosAreasEnActivos)
        
        
        return render(request, "empleadosCustom/directorioCorreos/verDirectorio.html", { "estaEnVerCorreos": estaEnVerCorreos, "id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo, "lista":lista,  "rh":rh,"almacen":almacen, "solicitantePrestamo":solicitantePrestamo, "subdirector":subdirector, "administradordeVehiculos":administradordeVehiculos})
    
    #Si le da al inicio y no hay una sesión iniciada..
    else:
        return redirect('/login/') #redirecciona a url de inicio
    
    

def documentosAplicablesATodos(request):
    
    #Si ya hay una sesión iniciada..
    if "idSesion" in request.session:
        
        
        
        estaEnVerDocumentos = True
        estaEnEncuesta = True
        id_admin=request.session["idSesion"]
        nombreini = request.session['nombres']
        apellidosini = request.session['apellidos']
        correo = request.session['correoSesion']
        foto = fotoAdmin(request)
        nombreCompleto = nombreini + " " + apellidosini #Blanca Yesenia Gaeta Talamantes
        if correo  == "recursos.humanos@customco.com.mx":
            rh = True
        else:
            rh= False
        
        if correo  == "almacen01@customco.com.mx":
            almacen = True
        else:
            almacen= False 
        
        if correo  == "egutierrez@customco.com.mx":
            subdirector = True
        else:
            subdirector= False 
        
        empleado = Empleados.objects.filter(id_empleado = id_admin)
        for dato in empleado:
            area = dato.id_area_id

        if area == 1 or area ==5 or area == 7 or area == 8 or area == 9 or area == 10:
            solicitantePrestamo = True
            if area == 5:
                administradordeVehiculos = True
            else:
                administradordeVehiculos = False
        else:
            solicitantePrestamo = False
            administradordeVehiculos = False
        return render(request, "empleadosCustom/documentos/aplicablesatodos.html", {"estaEnVerDocumentos":estaEnVerDocumentos, "id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo,  "rh":rh,"almacen":almacen, "solicitantePrestamo":solicitantePrestamo, "subdirector":subdirector,"administradordeVehiculos":administradordeVehiculos})
    
    #Si le da al inicio y no hay una sesión iniciada..
    else:
        return redirect('/login/') #redirecciona a url de inicio

def aplicable1(request):
    
    #Si ya hay una sesión iniciada..
    if "idSesion" in request.session:
        
        
        
        if request.method == "POST":
            
            formato = request.POST['fto1']


            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            nombreArchivo = formato+".xlsx"
            ubicacionArchivo = BASE_DIR + '/media/documentosAreas/'+ nombreArchivo

            path = open(ubicacionArchivo, 'rb')

            mime_type, _= mimetypes.guess_type(ubicacionArchivo)
            response = HttpResponse(path, content_type=mime_type)
            response['Content-Disposition'] = "attachment; filename=%s" %nombreArchivo
            return response

    
    #Si le da al inicio y no hay una sesión iniciada..
    else:
        return redirect('/login/') #redirecciona a url de inicio

def aplicable2(request):
    
    #Si ya hay una sesión iniciada..
    if "idSesion" in request.session:
        

        
        if request.method == "POST":
            
            formato = request.POST['fto1']


            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            nombreArchivo = formato+".docx"
            ubicacionArchivo = BASE_DIR + '/media/documentosAreas/'+ nombreArchivo

            path = open(ubicacionArchivo, 'rb')

            mime_type, _= mimetypes.guess_type(ubicacionArchivo)
            response = HttpResponse(path, content_type=mime_type)
            response['Content-Disposition'] = "attachment; filename=%s" %nombreArchivo
            return response


           
    
    #Si le da al inicio y no hay una sesión iniciada..
    else:
        return redirect('/login/') #redirecciona a url de inicio

def aplicable3(request):
    
    #Si ya hay una sesión iniciada..
    if "idSesion" in request.session:
        
        
     
        
        if request.method == "POST":
            
            formato = request.POST['fto1']


            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            nombreArchivo = formato+".pdf"
            ubicacionArchivo = BASE_DIR + '/media/documentosAreas/'+ nombreArchivo

            path = open(ubicacionArchivo, 'rb')

            mime_type, _= mimetypes.guess_type(ubicacionArchivo)
            response = HttpResponse(path, content_type=mime_type)
            response['Content-Disposition'] = "attachment; filename=%s" %nombreArchivo
            return response


           
    
    #Si le da al inicio y no hay una sesión iniciada..
    else:
        return redirect('/login/') #redirecciona a url de inicio

def pruebaPDF(request):
    
    #Si ya hay una sesión iniciada..
    if "idSesion" in request.session:

       #crear el http response con pdf
        respuesta = HttpResponse(content_type='application/pdf')
        respuesta['Content-Disposition'] = 'attachment; filename=Reporte Resultados Encuesta Clima Laboral - Enero 2022.pdf'
        #Crear objeto PDF 
        buffer =BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        base_dir = str(settings.BASE_DIR) #C:\Users\AuxSistemas\Desktop\CS Escritorio\Custom-System\djangoCS
        #nombre de empresa
        logo = base_dir+'/static/images/logoCustom.PNG'   
        c.drawImage(logo, 40,700,120,70, preserveAspectRatio=True)
            
        c.setFont('Helvetica-Bold', 14)
        c.drawString(150,750, 'Custom & Co S.A. de C.V.')
            
        c.setFont('Helvetica', 8)
        c.drawString(150,735, 'Allende #646 Sur Colonia Centro, Durango, CP: 35000')
            
        c.setFont('Helvetica', 8)
        c.drawString(150,720, 'RFC: CAC070116IS9')
            
        c.setFont('Helvetica', 8)
        c.drawString(150,705, 'Tel: 8717147716')
        #fecha
        hoy=datetime.now()
        fecha = str(hoy.date())
        color_guinda="#B03A2E"
        color_azul = "#cf1515"
        c.setFillColor(color_guinda)
        
            
        c.setFont('Helvetica-Bold', 12)
        c.drawString(425,750, "CLIMA LABORAL 2022")
        color_negro="#030305"
        c.setFillColor(color_negro)
        c.setFont('Helvetica-Bold', 10)
        c.drawString(405,730, "Fecha de impresión: " +fecha)
        #linea guinda
            
        c.setFillColor(color_guinda)
        c.setStrokeColor(color_guinda)
        c.line(40,695,560,695)
        #nombre departamento
        color_negro="#030305"
        c.setFillColor(color_negro)
        c.setFont('Helvetica', 12)
        c.drawString(405,710, 'Departamento de Sistemas')
        #titulo
        c.setFont('Helvetica-Bold', 22)
            
        c.drawString(55,660, 'Resultados Encuesta Clima Laboral Enero 2022')


        #tabla1
        c.setFont('Helvetica-Bold', 18)
        c.drawString(215,620, 'Criterios de Evaluación')


        #header de tabla
        styles = getSampleStyleSheet()
        styleBH =styles["Normal"]
        styleBH.alignment = TA_CENTER
        styleBH.fontSize = 10
        
        
        rango = Paragraph('''Rango Porcentaje''', styleBH)
        criterio = Paragraph('''Criterio''', styleBH)
       
      
        filasTabla=[]
        filasTabla.append([rango, criterio])
        #Tabla
        styleN = styles["BodyText"]
        styleN.alignment = TA_CENTER
        styleN.fontSize = 7
        
        high = 590
        porcentajes = ["100% - 90%", "89% - 80%", "79% - 70%","69% - 60%", "59% - 0%" ]
        criterios = ["Excelente", "Muy bueno", "Bueno", "Regular", "Deficiente"]
        
        contador = 0
        for x in porcentajes:
            if contador == 0:
                fila = [porcentajes[contador], criterios[contador]]
                contador= 1

            elif contador != 0:
                fila = [porcentajes[contador], criterios[contador]]
                contador= contador+1
            filasTabla.append(fila)
            high= high - 18 
            
        #escribir tabla
        width, height = letter
        tabla = Table(filasTabla, colWidths=[4 * cm, 4 * cm])
        
        tabla.setStyle(TableStyle([
           
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BACKGROUND', (0, 0), (-1, 0), '#e9c7ae'),
            
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
            ('BACKGROUND', (1,1), (-1,-5), '#4CAF50'),
            ('BACKGROUND', (1,2), (-1,-4), '#2196F3'),
            ('BACKGROUND', (1,3), (-1,-3), '#FFC107'),
            ('BACKGROUND', (1,4), (-1,-2), '#FF5722'),
            ('BACKGROUND', (1,5), (-1,-1), '#F44336'),
        ]))

        tabla.wrapOn(c, width, height)
        tabla.drawOn(c, 200, high)

        #tabla2

        c.setFont('Helvetica-Bold', 18)
        c.drawString(215,475, 'Encuestas contestadas')

        empleadosActivos = Empleados.objects.filter(activo = "A", correo__icontains="@customco.com.mx")
        contadorEmpleadosActivos = 0

        for activos in empleadosActivos:
            contadorEmpleadosActivos = contadorEmpleadosActivos + 1

        contadorEmpleadosActivos = str(contadorEmpleadosActivos)

        c.setFont('Helvetica-Bold', 16)
        c.drawString(80,440, 'Número de empleados')
        c.drawString(85,415, 'activos en la empresa:')
        c.setFont('Helvetica-Bold', 36)
        c.setFillColor(color_azul)
        c.drawString(140,375, contadorEmpleadosActivos)


        c.setFillColor(color_negro)
        c.setFont('Helvetica-Bold', 16)
        c.drawString(360,440, 'Número de encuestas')
        c.drawString(365,415, 'resueltas esperadas:')
        c.setFont('Helvetica-Bold', 36)
        c.setFillColor(color_azul)
        c.drawString(425,375, contadorEmpleadosActivos)
        c.setFillColor(color_negro)

        c.setFont('Helvetica-Bold', 16)
        c.drawString(80,340, 'Relación contestadas/')
        c.drawString(85,320, 'no contestadas:')

        empleadosContestados = EncuestaEmpleadoResuelta.objects.filter(id_encuesta = 1)
        contadorEmpleadoscontestados = 0

        for contestado in empleadosContestados:
            contadorEmpleadoscontestados = contadorEmpleadoscontestados + 1
        
        

        empleadosFaltantes = int(contadorEmpleadosActivos) - int(contadorEmpleadoscontestados)

        empleadosFaltantes = int(empleadosFaltantes)

      

       

        

        #grafico de pastel
        b = Drawing()
        pie = Pie()
        pie.x = 0
        pie.y = 0
        pie.height = 160
        pie.width = 160
        pie.data = [contadorEmpleadoscontestados, empleadosFaltantes ]
        strContestadas = "Contestadas "+str(contadorEmpleadoscontestados)
        strFaltantes = "No Contestadas "+str(empleadosFaltantes)
        pie.labels = [strContestadas, strFaltantes]
        pie.slices.strokeWidth = 0.5
        pie.slices[1].popout = 20
        pie.slices[0].fillColor= colors.HexColor("#e91e63")
        pie.slices[1].fillColor=colors.HexColor("#009688")
        b.add(pie)
        x,y = 100,130 
        renderPDF.draw(b, c, x, y, showBoundary=False)

        c.setFont('Helvetica-Bold', 16)
        c.drawString(360,340, 'Porcentaje total')
        c.drawString(365,320, 'resuelto:')

        porcentajeTotal = 100
        porcentaje = int(contadorEmpleadoscontestados * 100) / int(contadorEmpleadosActivos)

        porcentaje = str(porcentaje)

        porcentajeDigitos = ("{0:.4f}".format(float(porcentaje))) + "%"

        porcentajeBarra = ("{0:.0f}".format(float(porcentaje)))

        porcentajeBarraa = int(porcentajeBarra)

        c.setStrokeColorRGB(0.7, 0, 0.7) #color de contorno
        c.setFillColorRGB(255, 255, 255) #color de relleno
        c.rect(360, 275, 200, 25, fill=True)

        c.setStrokeColorRGB(0.7, 0, 0.7) #color de contorno

        if porcentajeBarraa >= 0 and porcentajeBarraa <= 33:
            c.setFillColorRGB(255, 0, 0) #color de relleno
            c.rect(360, 275, porcentajeBarra, 25, fill=True)
        elif porcentajeBarraa >= 34 and porcentajeBarraa <= 66:
            c.setFillColorRGB(255, 165, 0) #color de relleno
            c.rect(360, 275, porcentajeBarra, 25, fill=True)
        elif porcentajeBarraa >= 67 and porcentajeBarraa <= 100:
            c.setFillColorRGB(0, 128, 0) #color de relleno
            c.rect(360, 275, porcentajeBarra, 25, fill=True)

        c.setFont('Helvetica-Bold', 28)
        c.setFillColor(color_azul)
        c.drawString(380,240, porcentajeDigitos+" ("+str(contadorEmpleadoscontestados)+")")
        c.setFont('Helvetica-Bold', 18)
        c.setFillColor(color_negro)
        c.drawString(340,210, "del 100% ("+str(contadorEmpleadosActivos)+") de empleados")
        
        c.drawString(320, 180, "Resultados preguntas Múltiples:")
        
        promediosMultiples = []
        
        
        preguntas = Preguntas.objects.filter(id_encuesta = 1)
        multiples = []
        for preg in preguntas:
            idp = preg.id_pregunta
            if preg.tipo == "M":
                
                multiples.append(idp)
        
        for multiple in multiples:
            respuestasFinalizadas = []
            respuestas = Respuestas.objects.filter(id_pregunta =multiple) #en este caso devuelve dos respuestas de dos diferentes empleados
            cont = 0
            for datos in respuestas:
                empleadoID = datos.id_empleado_id

                encuestaEmpleado = EncuestaEmpleadoResuelta.objects.filter(id_encuesta = 1, id_empleado = empleadoID)

                if encuestaEmpleado:
                    preguntaID = datos.id_pregunta_id
                    respuestaEm = datos.respuesta
                    respuestasFinalizadas.append(respuestaEm)
                    cont = cont +1

            contadorSI = 0
                
            for respuestaX in respuestasFinalizadas:
                res = respuestaX #SI o NO
                        
                    
                if res == "SI":
                    contadorSI = contadorSI + 1
                       
                
                
            porcentajePregunta = (contadorSI * 100)/ contadorEmpleadoscontestados
            promediosMultiples.append(porcentajePregunta)
            
        suma2 = 0

        for porcentajesMultiples in promediosMultiples:
            porcentajeSuma = int(porcentajesMultiples)
            suma2 += porcentajeSuma

        contadorPreguntasMultiples = 0

        for m in multiples:

            contadorPreguntasMultiples = contadorPreguntasMultiples + 1

        promedio = suma2 / contadorPreguntasMultiples
        promedioGeneral = str(promedio)
        
        colorCriterio = ""
        if promedio >= 90 and promedio <= 100:
            criterio = "EXCELENTE"
            colorCriterio = "#acaf50"
        elif promedio >= 80 and promedio < 90:
            criterio = "MUY BUENO"
            colorCriterio = "#2196f3"
        elif promedio >= 70 and promedio < 80:
            criterio = "BUENO"
            colorCriterio = "#ffc107"
        elif promedio >= 60 and promedio < 70:
            criterio = "REGULAR"
            colorCriterio = "#ff5722"
        elif promedio >= 0 and promedio < 60:
            criterio = "DEFICIENTE"
            colorCriterio = "#f44336"
            
        
        
                    
                    
        c.drawString(320, 140, "Promedio General: "+promedioGeneral)
        c.drawString(320, 100, "Criterio: ")
        c.setFont('Helvetica-Bold', 20)
        c.setFillColor(colorCriterio)
        c.drawString(400, 100, criterio)
        c.setFillColor(color_negro)
        
       



  

        
        
        f = Drawing()
        barra = VerticalBarChart()
        barra.x = 0
        barra.y = 0
        barra.height = 100
        barra.width = 50
        data = [(10,2)]
        barra.valueAxis.valueMin = 0
        barra.valueAxis.valueMax = 20 
        barra.data = data
        barra.categoryAxis.categoryNames = ['SI', 'NO']
        barra.bars[(0,0)].fillColor = colors.HexColor("#E91E63")
        barra.bars[(0,1)].fillColor = colors.red
        f.add(barra)
        x,y = 60, 300
        #renderPDF.draw(f, c, x, y, showBoundary=False)  


        #linea guinda
        color_guinda="#B03A2E"
        c.setFillColor(color_guinda)
        c.setStrokeColor(color_guinda)
        c.line(40,60,560,60)
        
        color_negro="#030305"
        c.setFillColor(color_negro)
        c.setFont('Helvetica-Bold', 11)
        c.drawString(170,48, '2021 - Administrador de Custom System. - Versión: 1.0.0 ')
        
        
        c.showPage()
        
        
        
        #guardar pdf
        c.save()
        #obtener valores de bytesIO y esribirlos en la respuesta
        pdf = buffer.getvalue()
        buffer.close()
        respuesta.write(pdf)
        return respuesta


        
    #Si le da al inicio y no hay una sesión iniciada..
    else:
        return redirect('/login/') #redirecciona a url de inicio


def resultadosMultiples(request):
    
    #Si ya hay una sesión iniciada..
    if "idSesion" in request.session:

        preguntas = Preguntas.objects.filter(id_encuesta = 1)
        hojas =0
        contPreguntas = 0
        multiples = []
        for preg in preguntas:
            idp = preg.id_pregunta
            if preg.tipo == "M":
                
                multiples.append(idp)
                contPreguntas = contPreguntas + 1
                
        
        #contPreguntas equivale a 10
        numeroHojasExactas = 0
        numeroHojas = contPreguntas / 4 
        
        residuo = contPreguntas%4

        if residuo == 0:
            numeroHojasExactas = ("{0:.0f}".format(float(numeroHojas)))
        
        elif residuo > 0:
            numeroHojasExtras = ("{0:.0f}".format(float(numeroHojas)))
            numeroHojasExactas = int(numeroHojasExtras) + 1

        #crear el http response con pdf
        respuesta = HttpResponse(content_type='application/pdf')
        respuesta['Content-Disposition'] = 'attachment; filename=Reporte Resultados Preguntas Multiples Encuesta Clima Laboral - Enero 2022.pdf'
        #Crear objeto PDF 
        buffer =BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        contadorHojas = 0
        
        for x in range(numeroHojasExactas):
           
            contadorHojas = contadorHojas + 1

            if contadorHojas == 1:
                contadorPreguntas = 0

                
                pregMultiples = []
                
                porcentajesPreguntasMultiples = []
                contadorSiNo = []

                preguntas = Preguntas.objects.filter(id_encuesta = 1)

                for pregunta in preguntas:
                    id_pregunta = pregunta.id_pregunta
                    texto = pregunta.pregunta
                    tipo = pregunta.tipo
                    clasificacion = pregunta.clasificacion

                    contadorPreguntas = contadorPreguntas + 1

                    if contadorPreguntas >=1 and contadorPreguntas <=4:
                        if tipo == "M":
                            pregMultiples.append([id_pregunta, texto, clasificacion])
        
            if contadorHojas == 2:
                contadorPreguntas = 0

                
                pregMultiples = []
                
                porcentajesPreguntasMultiples = []
                contadorSiNo = []

                preguntas = Preguntas.objects.filter(id_encuesta = 1)

                for pregunta in preguntas:
                    id_pregunta = pregunta.id_pregunta
                    texto = pregunta.pregunta
                    tipo = pregunta.tipo
                    clasificacion = pregunta.clasificacion

                    contadorPreguntas = contadorPreguntas + 1

                    if contadorPreguntas >=5 and contadorPreguntas <=8:
                        if tipo == "M":
                            pregMultiples.append([id_pregunta, texto, clasificacion])
            
            if contadorHojas == 3:
                contadorPreguntas = 0

                
                pregMultiples = []
                
                porcentajesPreguntasMultiples = []
                contadorSiNo = []

                preguntas = Preguntas.objects.filter(id_encuesta = 1)

                for pregunta in preguntas:
                    id_pregunta = pregunta.id_pregunta
                    texto = pregunta.pregunta
                    tipo = pregunta.tipo
                    clasificacion = pregunta.clasificacion

                    contadorPreguntas = contadorPreguntas + 1

                    if contadorPreguntas >=9 and contadorPreguntas <=12:
                        if tipo == "M":
                            pregMultiples.append([id_pregunta, texto, clasificacion])

            if contadorHojas == 4:
                contadorPreguntas = 0

                
                pregMultiples = []
                
                porcentajesPreguntasMultiples = []
                contadorSiNo = []

                preguntas = Preguntas.objects.filter(id_encuesta = 1)

                for pregunta in preguntas:
                    id_pregunta = pregunta.id_pregunta
                    texto = pregunta.pregunta
                    tipo = pregunta.tipo
                    clasificacion = pregunta.clasificacion

                    contadorPreguntas = contadorPreguntas + 1

                    if contadorPreguntas >=13 and contadorPreguntas <=16:
                        if tipo == "M":
                            pregMultiples.append([id_pregunta, texto, clasificacion])

            if contadorHojas == 5:
                contadorPreguntas = 0

                
                pregMultiples = []
                
                porcentajesPreguntasMultiples = []
                contadorSiNo = []

                preguntas = Preguntas.objects.filter(id_encuesta = 1)

                for pregunta in preguntas:
                    id_pregunta = pregunta.id_pregunta
                    texto = pregunta.pregunta
                    tipo = pregunta.tipo
                    clasificacion = pregunta.clasificacion

                    contadorPreguntas = contadorPreguntas + 1

                    if contadorPreguntas >=17 and contadorPreguntas <=20:
                        if tipo == "M":
                            pregMultiples.append([id_pregunta, texto, clasificacion])
                        

            if contadorHojas == 6:
                contadorPreguntas = 0

                
                pregMultiples = []
                
                porcentajesPreguntasMultiples = []
                contadorSiNo = []

                preguntas = Preguntas.objects.filter(id_encuesta = 1)

                for pregunta in preguntas:
                    id_pregunta = pregunta.id_pregunta
                    texto = pregunta.pregunta
                    tipo = pregunta.tipo
                    clasificacion = pregunta.clasificacion

                    contadorPreguntas = contadorPreguntas + 1

                    if contadorPreguntas >=21 and contadorPreguntas <=24:
                        if tipo == "M":
                            pregMultiples.append([id_pregunta, texto, clasificacion])

            if contadorHojas == 7:
                contadorPreguntas = 0

                
                pregMultiples = []
                
                porcentajesPreguntasMultiples = []
                contadorSiNo = []

                preguntas = Preguntas.objects.filter(id_encuesta = 1)

                for pregunta in preguntas:
                    id_pregunta = pregunta.id_pregunta
                    texto = pregunta.pregunta
                    tipo = pregunta.tipo
                    clasificacion = pregunta.clasificacion

                    contadorPreguntas = contadorPreguntas + 1

                    if contadorPreguntas >=25 and contadorPreguntas <=28:
                        if tipo == "M":
                            pregMultiples.append([id_pregunta, texto, clasificacion])



            base_dir = str(settings.BASE_DIR) #C:\Users\AuxSistemas\Desktop\CS Escritorio\Custom-System\djangoCS
            #nombre de empresa
            logo = base_dir+'/static/images/logoCustom.PNG'   
            c.drawImage(logo, 40,700,120,70, preserveAspectRatio=True)
                
            c.setFont('Helvetica-Bold', 14)
            c.drawString(150,750, 'Custom & Co S.A. de C.V.')
                
            c.setFont('Helvetica', 8)
            c.drawString(150,735, 'Allende #646 Sur Colonia Centro, Durango, CP: 35000')
                
            c.setFont('Helvetica', 8)
            c.drawString(150,720, 'RFC: CAC070116IS9')
                
            c.setFont('Helvetica', 8)
            c.drawString(150,705, 'Tel: 8717147716')
            #fecha
            hoy=datetime.now()
            fecha = str(hoy.date())
            color_guinda="#B03A2E"
            color_azul = "#cf1515"
            c.setFillColor(color_guinda)
            
                
            c.setFont('Helvetica-Bold', 12)
            c.drawString(425,750, "CLIMA LABORAL 2022")
            color_negro="#030305"
            c.setFillColor(color_negro)
            c.setFont('Helvetica-Bold', 10)
            c.drawString(405,730, "Fecha de impresión: " +fecha)
            #linea guinda
                
            c.setFillColor(color_guinda)
            c.setStrokeColor(color_guinda)
            c.line(40,695,560,695)
            #nombre departamento
            color_negro="#030305"
            c.setFillColor(color_negro)
            c.setFont('Helvetica', 12)
            c.drawString(405,710, 'Departamento de Sistemas')
            #titulo
            c.setFont('Helvetica-Bold', 22)
                
            c.drawString(140,660, 'Resultados Preguntas Múltiples')
            


            

            empleadosContestados = EncuestaEmpleadoResuelta.objects.filter(id_encuesta = 1)
            contadorEmpleadoscontestados = 0

            for contestado in empleadosContestados:
                contadorEmpleadoscontestados = contadorEmpleadoscontestados + 1


    
            
            unaSolaPalabra = False
            for multiple in pregMultiples:
                idPregunta = multiple[0]
                clasificacion = multiple[2]
                respuestasFinalizadas = []
                
                
                palabrasClasificacion = clasificacion.split(" ")
                contPalabras = 0
                for x in palabrasClasificacion:
                    contPalabras = contPalabras + 1
                
                if contPalabras == 1:
                    unaSolaPalabra = True
                elif contPalabras > 1:
                    unaSolaPalabra = False

                respuestas = Respuestas.objects.filter(id_pregunta =idPregunta) #en este caso devuelve dos respuestas de dos diferentes empleados
                cont = 0

                for datos in respuestas:
                    empleadoID = datos.id_empleado_id

                    encuestaEmpleado = EncuestaEmpleadoResuelta.objects.filter(id_encuesta = 1, id_empleado = empleadoID)

                    if encuestaEmpleado:
                     
                        respuestaEm = datos.respuesta
                        respuestasFinalizadas.append(respuestaEm)
                        cont = cont +1

                contadorSI = 0
                contadorNO = 0

                contadorRespuestas = 0
                for respuestaX in respuestasFinalizadas:
                    res = respuestaX #SI o NO
                    contadorRespuestas = contadorRespuestas + 1
                    
                    if res == "SI":
                        contadorSI = contadorSI + 1
                    elif res == "NO":
                        contadorNO = contadorNO +1
                
                contadorSiNo.append([contadorSI, contadorNO,contadorRespuestas])
                
                porcentajePregunta = (contadorSI * 100)/ contadorEmpleadoscontestados
                p = ("{0:.2f}".format(float(porcentajePregunta)))
                
                criterio = ""
                if porcentajePregunta >= 90 and porcentajePregunta <= 100:
                    criterio = "EXCELENTE"
                elif porcentajePregunta >= 80 and porcentajePregunta < 90:
                    criterio = "MUY BUENO"
                elif porcentajePregunta >= 70 and porcentajePregunta < 80:
                    criterio = "BUENO"
                elif porcentajePregunta >= 60 and porcentajePregunta < 70:
                    criterio = "REGULAR"
                elif porcentajePregunta >= 0 and porcentajePregunta < 60:
                    criterio = "DEFICIENTE"

                porcentajesPreguntasMultiples.append([float(p),criterio])

        
            listaMultiples = zip(pregMultiples, porcentajesPreguntasMultiples, contadorSiNo)
            
            
        
        

            
            valorHigh = 550
            contador = 0
            alturaTituloPregunta = 0
            alturaClasificación = 0
            high = 0

            xBarra = 0
            yBarra = 0
            
            for preguntaX, porcentajeX, contsino in listaMultiples:

                contador = contador + 1

            

                idPregunta = preguntaX[0]
                idp= str(idPregunta)

                barra = "barra" 

            
                if contador == 1:
                    alturaTituloPregunta = 630
                    high = 520
                    xBarra = 405
                    yBarra = 540
                    alturaClasificación = 520

                if contador > 1:
                    alturaTituloPregunta = alturaTituloPregunta - 135
                    high = high - 135
                        
                    yBarra = yBarra - 135 
                    alturaClasificación = alturaClasificación - 138
                
                c.setFont('Helvetica-Bold', 18)
                c.drawString(80,alturaTituloPregunta, "Pregunta"+ idp)
                
                colorClasificacion = ""
                if clasificacion == "COMUNICACIÓN INTERNA":
                    colorClasificacion="#4CAF50"
                    c.setFillColor(colorClasificacion)
                elif  clasificacion == "TRABAJO EN EQUIPO":
                    colorClasificacion="#E91E63"
                    c.setFillColor(colorClasificacion)
                elif  clasificacion == "LIDERAZGO":
                    colorClasificacion="#9C27B0"
                    c.setFillColor(colorClasificacion)
                elif  clasificacion == "SUPERVISIÓN":
                    colorClasificacion="#3F51B5"
                    c.setFillColor(colorClasificacion)
                elif  clasificacion == "CONDICIONES GENERALES Y PARTICULARES":
                    colorClasificacion="#00BCD4"
                    c.setFillColor(colorClasificacion)
                elif  clasificacion == "FELICIDAD DEL TRABAJADOR":
                    colorClasificacion="#009688"
                    c.setFillColor(colorClasificacion)
                elif  clasificacion == "OPORTUNIDADES PARA EL CRECIMIENTO":
                    colorClasificacion="#FFC107"
                    c.setFillColor(colorClasificacion)
                elif  clasificacion == "POLÍTICAS DE COMPENSACIÓN Y RETRIBUCIÓN":
                    colorClasificacion="#795548"
                    c.setFillColor(colorClasificacion)
                elif  clasificacion == "MOTIVACIÓN":
                    colorClasificacion="#FF5722"
                    c.setFillColor(colorClasificacion)
                
                
                if unaSolaPalabra:
                    c.rotate(90)
                    c.setFont('Helvetica-Bold', 14)
                    c.drawString(alturaClasificación, -50, clasificacion)
                    c.rotate(-90)
                    c.setFillColor(color_negro)
                elif unaSolaPalabra == False:
                    if contPalabras == 2:
                        palabra1 = palabrasClasificacion[0]
                        palabra2 = palabrasClasificacion[1]
                        c.rotate(90)
                        c.setFont('Helvetica-Bold', 12)
                        c.drawString(alturaClasificación+10, -50, palabra1)
                        c.drawString(alturaClasificación+10, -35, palabra2)
                        c.rotate(-90)
                        c.setFillColor(color_negro)
                    if contPalabras == 3:
                        palabra1 = palabrasClasificacion[0]
                        palabra2 = palabrasClasificacion[1] + " " + palabrasClasificacion[2]
                        c.rotate(90)
                        c.setFont('Helvetica-Bold', 12)
                        c.drawString(alturaClasificación+10, -50, palabra2)
                        c.drawString(alturaClasificación+10, -35, palabra1)
                        c.rotate(-90)
                        c.setFillColor(color_negro)
                    if contPalabras == 4:
                        palabra1 = palabrasClasificacion[0] + " "+palabrasClasificacion[1]
                        palabra2 = palabrasClasificacion[2] + " " + palabrasClasificacion[3]
                        c.rotate(90)
                        c.setFont('Helvetica-Bold', 12)
                        c.drawString(alturaClasificación+10, -50, palabra2)
                        c.drawString(alturaClasificación+10, -35, palabra1)
                        c.rotate(-90)
                        c.setFillColor(color_negro)
                    if contPalabras == 5:
                        palabra1 = palabrasClasificacion[0] + " "+palabrasClasificacion[1]
                        palabra2 = palabrasClasificacion[2] + " " + palabrasClasificacion[3]
                        palabra3 = palabrasClasificacion[4]
                        c.rotate(90)
                        c.setFont('Helvetica-Bold', 8)
                        c.drawString(alturaClasificación+10, -50, palabra3)
                        c.drawString(alturaClasificación+10, -35, palabra2)
                        c.drawString(alturaClasificación+10, -15, palabra1)
                        c.rotate(-90)
                        c.setFillColor(color_negro)
                

                #header de tabla
                styles = getSampleStyleSheet()
                styleBH =styles["Normal"]
                styleBH.alignment = TA_CENTER
                styleBH.fontSize = 10
                    
                    
                preguntaE = Paragraph('''Texto Pregunta''', styleBH)
                promedioE = Paragraph('''Promedio''', styleBH)
                graficoE = Paragraph('''Gráfico''', styleBH)
                criterioE = Paragraph('''Criterio''', styleBH)
                
                
                filasTabla=[]
                filasTabla.append([preguntaE, promedioE, graficoE, criterioE])
                    #Tabla
                styleN = styles["BodyText"]
                styleN.alignment = TA_CENTER
                styleN.fontSize = 9

        

    


                f = Drawing()
                barra= VerticalBarChart()
                barra.x = 0
                barra.y = 0
                barra.height = 45
                barra.width = 40
                data = [(contsino[0],contsino[1])]
                barra.valueAxis.valueMin = 0
                barra.valueAxis.valueMax = 35 
                barra.data = data
                barra.categoryAxis.categoryNames = ['SI', 'NO']
                barra.bars[(0,0)].fillColor = colors.HexColor("#E91E63")
                barra.bars[(0,1)].fillColor = colors.red
                f.add(barra)
                        
                renderPDF.draw(f, c, xBarra, yBarra, showBoundary=False) 

 
                suma = 0

                for porcentajesMultiples in porcentajesPreguntasMultiples:
                    porcentajeSuma = porcentajesMultiples[0]
                    suma = suma + porcentajeSuma

                contadorPreguntasMultiples = 0

                for m in pregMultiples:

                    contadorPreguntasMultiples = contadorPreguntasMultiples + 1

                promedio = suma / contadorPreguntasMultiples

                criterio = ""
                if porcentajeX[0] >= 90 and porcentajeX[0] <= 100:
                    criterio = "EXCELENTE"
                    campo_texto = Paragraph(str(preguntaX[1]), styleN)
                    #campo_promedio = Paragraph("Promedio General"+"<br/>" + str(porcentajeX[0]) + "<br/>"+ "# respuestas totales: 2" + "<br/>"+ "# respuestas SI: 0" +  "<br/>"+ "# respuestas NO: 1"  , styleN)
                    campo_promedio = Paragraph('''<para align=center>Promedio General <br/> <br/><b><font color="#4caf50" fontsize=20> '''+ str(porcentajeX[0]) +''' </font></b> <br/># respuestas totales: <b>'''+ str(contsino[2]) +'''</b> <br/># respuestas SI: <b>'''+ str(contsino[0]) +'''</b><br/># respuestas NO: <b>'''+ str(contsino[1]) +'''</b></para>''',styleN)
                    campo_grafico = Paragraph(str(barra), styleN)
                    campo_criterio = Paragraph('''<para align=center><b><font color="#4caf50" fontsize=16>'''+str(porcentajeX[1]) +'''</font></b></para>''', styleN)
                elif porcentajeX[0] >= 80 and porcentajeX[0] < 90:
                    criterio = "MUY BUENO"
                    campo_texto = Paragraph(str(preguntaX[1]), styleN)
                    #campo_promedio = Paragraph("Promedio General"+"<br/>" + str(porcentajeX[0]) + "<br/>"+ "# respuestas totales: 2" + "<br/>"+ "# respuestas SI: 0" +  "<br/>"+ "# respuestas NO: 1"  , styleN)
                    campo_promedio = Paragraph('''<para align=center>Promedio General <br/> <br/><b><font color="#2196f3" fontsize=20> '''+ str(porcentajeX[0]) +''' </font></b> <br/># respuestas totales: <b>'''+ str(contsino[2]) +'''</b> <br/># respuestas SI: <b>'''+ str(contsino[0]) +'''</b><br/># respuestas NO: <b>'''+ str(contsino[1]) +'''</b></para>''',styleN)
                    campo_grafico = Paragraph(str(barra), styleN)
                    campo_criterio = Paragraph('''<para align=center><b><font color="#2196f3" fontsize=16>'''+str(porcentajeX[1]) +'''</font></b></para>''', styleN)
                elif porcentajeX[0] >= 70 and porcentajeX[0] < 80:
                    criterio = "BUENO"
                    campo_texto = Paragraph(str(preguntaX[1]), styleN)
                    #campo_promedio = Paragraph("Promedio General"+"<br/>" + str(porcentajeX[0]) + "<br/>"+ "# respuestas totales: 2" + "<br/>"+ "# respuestas SI: 0" +  "<br/>"+ "# respuestas NO: 1"  , styleN)
                    campo_promedio = Paragraph('''<para align=center>Promedio General <br/> <br/><b><font color="#ffc107" fontsize=20> '''+ str(porcentajeX[0]) +''' </font></b> <br/># respuestas totales: <b>'''+ str(contsino[2]) +'''</b> <br/># respuestas SI: <b>'''+ str(contsino[0]) +'''</b><br/># respuestas NO: <b>'''+ str(contsino[1]) +'''</b></para>''',styleN)
                    campo_grafico = Paragraph(str(barra), styleN)
                    campo_criterio = Paragraph('''<para align=center><b><font color="#ffc107" fontsize=16>'''+str(porcentajeX[1]) +'''</font></b></para>''', styleN)
                elif porcentajeX[0] >= 60 and porcentajeX[0] < 70:
                    criterio = "REGULAR"
                    campo_texto = Paragraph(str(preguntaX[1]), styleN)
                    #campo_promedio = Paragraph("Promedio General"+"<br/>" + str(porcentajeX[0]) + "<br/>"+ "# respuestas totales: 2" + "<br/>"+ "# respuestas SI: 0" +  "<br/>"+ "# respuestas NO: 1"  , styleN)
                    campo_promedio = Paragraph('''<para align=center>Promedio General <br/> <br/><b><font color="#ff5722" fontsize=20> '''+ str(porcentajeX[0]) +''' </font></b> <br/># respuestas totales: <b>'''+ str(contsino[2]) +'''</b> <br/># respuestas SI: <b>'''+ str(contsino[0]) +'''</b><br/># respuestas NO: <b>'''+ str(contsino[1]) +'''</b></para>''',styleN)
                    campo_grafico = Paragraph(str(barra), styleN)
                    campo_criterio = Paragraph('''<para align=center><b><font color="#ff5722" fontsize=16>'''+str(porcentajeX[1]) +'''</font></b></para>''', styleN)
                elif porcentajeX[0] >= 0 and porcentajeX[0] < 60:
                    criterio = "DEFICIENTE"
                    campo_texto = Paragraph(str(preguntaX[1]), styleN)
                    #campo_promedio = Paragraph("Promedio General"+"<br/>" + str(porcentajeX[0]) + "<br/>"+ "# respuestas totales: 2" + "<br/>"+ "# respuestas SI: 0" +  "<br/>"+ "# respuestas NO: 1"  , styleN)
                    campo_promedio = Paragraph('''<para align=center>Promedio General <br/> <br/><b><font color="#f44336" fontsize=20> '''+ str(porcentajeX[0]) +''' </font></b> <br/># respuestas totales: <b>'''+ str(contsino[2]) +'''</b> <br/># respuestas SI: <b>'''+ str(contsino[0]) +'''</b><br/># respuestas NO: <b>'''+ str(contsino[1]) +'''</b></para>''',styleN)
                    campo_grafico = Paragraph(str(barra), styleN)
                    campo_criterio = Paragraph('''<para align=center><b><font color="#f44336" fontsize=16>'''+str(porcentajeX[1]) +'''</font></b></para>''', styleN)
                
                                                    
                fila = [campo_texto, campo_promedio, campo_grafico, campo_criterio ]
                                                                    
                filasTabla.append(fila)
                                                                    
                        #high= high - 18

            
                    #escribir tabla
                width, height = letter
                tabla = Table(filasTabla, colWidths=[5 * cm, 5 * cm, 4 * cm, 4 * cm])
                                                                                            
                tabla.setStyle(TableStyle([
                                                                                            
                        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                        ('BACKGROUND', (0, 0), (-1, 0), '#FFC107'),
                        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                        ('VALIGN', (1,1), (-3,-1), 'MIDDLE'),
                    
                                                                    
                                                                                            ]))

                tabla.wrapOn(c, width, height)
                tabla.drawOn(c, 65, high)

            if contadorHojas == numeroHojasExactas:

                alturaPromedio = high-30
                alturaCriterio = alturaPromedio-25
                
                promediosMultiples = []
                
                for multiple in multiples:
                    respuestasFinalizadas = []
                    respuestas = Respuestas.objects.filter(id_pregunta =multiple) #en este caso devuelve dos respuestas de dos diferentes empleados
                    cont = 0

                    for datos in respuestas:
                        empleadoID = datos.id_empleado_id

                        encuestaEmpleado = EncuestaEmpleadoResuelta.objects.filter(id_encuesta = 1, id_empleado = empleadoID)

                        if encuestaEmpleado:
                        
                            respuestaEm = datos.respuesta
                            respuestasFinalizadas.append(respuestaEm)
                            cont = cont +1

                    contadorSI = 0
                
                    for respuestaX in respuestasFinalizadas:
                        res = respuestaX #SI o NO
                        
                    
                        if res == "SI":
                            contadorSI = contadorSI + 1
                       
                
                
                    porcentajePregunta = (contadorSI * 100)/ contadorEmpleadoscontestados
                    promediosMultiples.append(porcentajePregunta)
                
                
            

                suma2 = 0

                for porcentajesMultiples in promediosMultiples:
                    porcentajeSuma = int(porcentajesMultiples)
                    suma2 += porcentajeSuma

                contadorPreguntasMultiples = 0

                for m in multiples:

                    contadorPreguntasMultiples = contadorPreguntasMultiples + 1

                promedio = suma2 / contadorPreguntasMultiples
                promedioGeneral = str(promedio)

                criterio = ""
                if promedio >= 90 and promedio <= 100:
                    
                    criterio = "EXCELENTE"
                    c.setFont('Helvetica-Bold', 18)
                    c.drawString(200,alturaPromedio, "Promedio General: "+ promedioGeneral)
                    c.drawString(205,alturaCriterio, "Criterio: ")
                    color_verde="#4caf50"
                    c.setFillColor(color_verde)
                    c.drawString(280,alturaCriterio, criterio)

                    
                elif promedio >= 80 and promedio <= 89:
                
                    criterio = "MUY BUENO"
                
                    c.setFont('Helvetica-Bold', 18)
                    c.drawString(200,alturaPromedio, "Promedio General: "+ promedioGeneral)
                    
                    c.drawString(205,alturaCriterio, "Criterio: ")
                    color_azul="#2196f3"
                    c.setFillColor(color_azul)
                    c.drawString(280,alturaCriterio, criterio)
                
                elif promedio >= 70 and promedio <= 79:
                    
                    criterio = "BUENO"
            
                    c.setFont('Helvetica-Bold', 18)
                    c.drawString(200,alturaPromedio, "Promedio General: " + promedioGeneral)
                    
                    c.drawString(205,alturaCriterio, "Criterio: ")
                    color_amarillo="#ffc107"
                    c.setFillColor(color_amarillo)
                    c.drawString(280,alturaCriterio, criterio)
                
                elif promedio >= 60 and promedio <= 69:
                
                    criterio = "REGULAR"
                
                    c.setFont('Helvetica-Bold', 18)
                    c.drawString(200,alturaPromedio, "Promedio General: "+ promedioGeneral)
                    
                    c.drawString(205,alturaCriterio, "Criterio: ")
                    color_naranja="#ff5722"
                    c.setFillColor(color_naranja)
                    c.drawString(280,alturaCriterio, criterio)
                
                elif promedio >= 0 and promedio <= 59:
                
                    criterio = "DEFICIENTE"
                    
                    c.setFont('Helvetica-Bold', 18)
                    c.drawString(200,alturaPromedio, "Promedio General: ")
                
                    c.drawString(205,alturaCriterio, "Criterio: ")
                    color_rojo="#f44336"
                    c.setFillColor(color_rojo)
                    c.drawString(280,alturaCriterio, criterio)
                


            #linea guinda
            color_guinda="#B03A2E"
            c.setFillColor(color_guinda)
            c.setStrokeColor(color_guinda)
            c.line(40,60,560,60)
            
            color_negro="#030305"
            c.setFillColor(color_negro)
            c.setFont('Helvetica-Bold', 11)
            c.drawString(170,48, '2021 - Administrador de Custom System. - Versión: 1.0.0 ')
            
            
            c.showPage()
            
            
        
        #guardar pdf
        c.save()
        #obtener valores de bytesIO y esribirlos en la respuesta
        pdf = buffer.getvalue()
        buffer.close()
        respuesta.write(pdf)
        return respuesta


        
    #Si le da al inicio y no hay una sesión iniciada..
    else:
        return redirect('/login/') #redirecciona a url de inicio



def resultadosAbiertas(request):
    
    #Si ya hay una sesión iniciada..
    if "idSesion" in request.session:

        if request.method == "POST":
            
            preguntaA = request.POST['pregunta']
        
        preguntaAbierta = Preguntas.objects.filter(id_pregunta = preguntaA)
        for pregA in preguntaAbierta:
            texto = pregA.pregunta
            
        textoSeparado = texto.split(' ')
        primeraLineaPregunta = ""
        segundaLineaPregunta = ""
        contadorPalabras = 0
        for palabra in textoSeparado:
            contadorPalabras = contadorPalabras + 1
            
            if contadorPalabras < 11:
                primeraLineaPregunta += " "+palabra
            if contadorPalabras >11:
                segundaLineaPregunta += " "+palabra
                
        titulo = "Resultados Pregunta Abierta #" + str(preguntaA)
            
            
        

        #crear el http response con pdf
        respuesta = HttpResponse(content_type='application/pdf')
        respuesta['Content-Disposition'] = 'attachment; filename=Reporte Resultados Preguntas Abiertas Encuesta Clima Laboral - Enero 2022.pdf'
        #Crear objeto PDF 
        buffer =BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
       
        
        

        base_dir = str(settings.BASE_DIR) #C:\Users\AuxSistemas\Desktop\CS Escritorio\Custom-System\djangoCS
            #nombre de empresa
        logo = base_dir+'/static/images/logoCustom.PNG'   
        c.drawImage(logo, 40,700,120,70, preserveAspectRatio=True)
                
        c.setFont('Helvetica-Bold', 14)
        c.drawString(150,750, 'Custom & Co S.A. de C.V.')
                
        c.setFont('Helvetica', 8)
        c.drawString(150,735, 'Allende #646 Sur Colonia Centro, Durango, CP: 35000')
                
        c.setFont('Helvetica', 8)
        c.drawString(150,720, 'RFC: CAC070116IS9')
                
        c.setFont('Helvetica', 8)
        c.drawString(150,705, 'Tel: 8717147716')
        #fecha
        hoy=datetime.now()
        fecha = str(hoy.date())
        color_guinda="#B03A2E"
        color_azul = "#cf1515"
        c.setFillColor(color_guinda)
            
                
        c.setFont('Helvetica-Bold', 12)
        c.drawString(425,750, "CLIMA LABORAL 2022")
        color_negro="#030305"
        c.setFillColor(color_negro)
        c.setFont('Helvetica-Bold', 10)
        c.drawString(405,730, "Fecha de impresión: " +fecha)
        #linea guinda
                
        c.setFillColor(color_guinda)
        c.setStrokeColor(color_guinda)
        c.line(40,695,560,695)
        #nombre departamento
        color_negro="#030305"
        c.setFillColor(color_negro)
        c.setFont('Helvetica', 12)
        c.drawString(405,710, 'Departamento de Sistemas')
        #titulo
        c.setFont('Helvetica-Bold', 22)
                
        c.drawString(140,670, titulo)

        c.setFont('Helvetica-Bold', 16)
                
        c.drawString(45,640, primeraLineaPregunta)
        c.drawString(60,620, segundaLineaPregunta)
        
    #Encabezado Tabla
        styles = getSampleStyleSheet()
        styleBH =styles["Normal"]
        styleBH.alignment = TA_CENTER
        styleBH.fontSize = 10
        
        
        titulo_empleado = Paragraph('''Empleado''', styleBH)
        titulo_respuesta = Paragraph('''Respuesta''', styleBH)
        filasTabla=[]
        filasTabla.append([titulo_empleado, titulo_respuesta])
        
    #Elementos Tabla
        styleN = styles["BodyText"]
        styleN.fontSize = 8
        
    #Consulta para sacar respuestas de pregunta

        datosRespuestas = Respuestas.objects.filter(id_pregunta = preguntaA)
        
        
        high = 585
        contadorEmpleado = 0
        for res in datosRespuestas:
            contadorEmpleado = contadorEmpleado + 1
            campo_empleado = Paragraph('''Empleado <b>#'''+str(res.id_empleado_id)+'''</b>''', styleN)
            campo_respuesta = Paragraph('''<b>R: </b>'''+res.respuesta, styleN)
            filasTabla.append([campo_empleado, campo_respuesta])
            high= high - 18 
        
    #Escribir tabla
        width, height = letter
        tabla = Table(filasTabla, colWidths=[4 * cm, 14 * cm])
        tabla.setStyle(TableStyle([
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BACKGROUND', (0, 0), (-1, 0), '#F5CD04'),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
            ('VALIGN', (0,1), (-1,-1), 'RIGHT')
        ]))
        
        tabla.wrapOn(c, width, height)
        tabla.drawOn(c, 50, high)
        
        
        


            

           

    #linea guinda
        color_guinda="#B03A2E"
        c.setFillColor(color_guinda)
        c.setStrokeColor(color_guinda)
        c.line(40,40,560,40)
            
        color_negro="#030305"
        c.setFillColor(color_negro)
        c.setFont('Helvetica-Bold', 11)
        c.drawString(170,28, '2021 - Administrador de Custom System. - Versión: 1.0.0 ')
            
            
        c.showPage()
            
            
        
        #guardar pdf
        c.save()
        #obtener valores de bytesIO y esribirlos en la respuesta
        pdf = buffer.getvalue()
        buffer.close()
        respuesta.write(pdf)
        return respuesta


        
    #Si le da al inicio y no hay una sesión iniciada..
    else:
        return redirect('/login/') #redirecciona a url de inicio



    
def implementacionesSistemas(request):

    #Si ya hay una sesión iniciada..
    if "idSesion" in request.session:

        estaEnVerImplementacionesSistemas = True
        enAño = True
        estaEnEncuesta = True
        id_admin=request.session["idSesion"]
        nombreini = request.session['nombres']
        apellidosini = request.session['apellidos']
        correo = request.session['correoSesion']
        foto = fotoAdmin(request)
        nombreCompleto = nombreini + " " + apellidosini #Blanca Yesenia Gaeta Talamantes
        subdirector = True
        
        listaImplementaciones = ImplementacionSoluciones.objects.all()
        listaImplementacionesModal = ImplementacionSoluciones.objects.all()
        listaImplementacionesModal2 = ImplementacionSoluciones.objects.all()

        if "firmaGuardada" in request.session:
            firmaGuardada = True
            del request.session['firmaGuardada']
            return render(request, "empleadosCustom/direccion/implementacionesSistemas.html",{"estaEnVerImplementacionesSistemas":estaEnVerImplementacionesSistemas,"id_admin":id_admin,
                                                                                          "nombreini":nombreini,"apellidosini":apellidosini,"correo":correo,"foto":foto,"nombreCompleto":nombreCompleto,"subdirector":subdirector, "listaImplementaciones":listaImplementaciones, "listaImplementacionesModal":listaImplementacionesModal, "listaImplementacionesModal2":listaImplementacionesModal2, "firmaGuardada":firmaGuardada})

        return render(request, "empleadosCustom/direccion/implementacionesSistemas.html",{"estaEnVerImplementacionesSistemas":estaEnVerImplementacionesSistemas,"id_admin":id_admin,
                                                                                          "nombreini":nombreini,"apellidosini":apellidosini,"correo":correo,"foto":foto,"nombreCompleto":nombreCompleto,"subdirector":subdirector, "listaImplementaciones":listaImplementaciones, "listaImplementacionesModal":listaImplementacionesModal, "listaImplementacionesModal2":listaImplementacionesModal2})
    else:
        return redirect("/login/")
    
    
def revisarImplementacion(request):

    #Si ya hay una sesión iniciada..
    if "idSesion" in request.session:

        estaEnVerImplementacionesSistemas = True
      
        id_admin=request.session["idSesion"]
        nombreini = request.session['nombres']
        apellidosini = request.session['apellidos']
        correo = request.session['correoSesion']
        foto = fotoAdmin(request)
        nombreCompleto = nombreini + " " + apellidosini #Blanca Yesenia Gaeta Talamantes
        subdirector = True
        
        if request.method == "POST":
            idImplementacionRecibida = request.POST['idImplemenatcionARevisar']

            datosImplementacion = ImplementacionSoluciones.objects.filter(id_implementacion = idImplementacionRecibida)

            return render(request, "empleadosCustom/direccion/revisarImplementacion.html",{"estaEnVerImplementacionesSistemas":estaEnVerImplementacionesSistemas,"id_admin":id_admin,
                                                                                          "nombreini":nombreini,"apellidosini":apellidosini,"correo":correo,"foto":foto,"nombreCompleto":nombreCompleto,"subdirector":subdirector, "datosImplementacion":datosImplementacion})

        
    else:
        return redirect("/login/")



def firmarImplementacion(request):

    #Si ya hay una sesión iniciada..
    if "idSesion" in request.session:

        if request.method == "POST":
            idImplementacionRecibidaParaFirma = request.POST['idImplementacionAFirmar']
            comentarios = request.POST['comentarios']
            canvas = request.POST['canvasData']

            firma = "firmaImplementacion"+str(idImplementacionRecibidaParaFirma)

            format, imgstr = canvas.split(';base64,')
            ext = format.split('/')[-1]
            archivo = ContentFile(base64.b64decode(imgstr), name= str(firma) + '.' + ext)

            if comentarios == "":
                actualizacion = ImplementacionSoluciones.objects.get(id_implementacion=idImplementacionRecibidaParaFirma)
                actualizacion.comentarios_direccion = "Sin comentarios."
                actualizacion.revisado = "S"
                actualizacion.firma_direccion = archivo
                actualizacion.save()
                
            else:
                actualizacion = ImplementacionSoluciones.objects.get(id_implementacion=idImplementacionRecibidaParaFirma)
                actualizacion.comentarios_direccion = comentarios
                actualizacion.revisado = "S"
                actualizacion.firma_direccion = archivo
                actualizacion.save()

            
            request.session['firmaGuardada'] = "sesionNotificacionFirma"

            return redirect("/implementacionesSistemas/")

        estaEnVerImplementacionesSistemas = True
        enAño = True
        estaEnEncuesta = True
        id_admin=request.session["idSesion"]
        nombreini = request.session['nombres']
        apellidosini = request.session['apellidos']
        correo = request.session['correoSesion']
        foto = fotoAdmin(request)
        nombreCompleto = nombreini + " " + apellidosini #Blanca Yesenia Gaeta Talamantes
        subdirector = True
        
        listaImplementaciones = ImplementacionSoluciones.objects.all()
        listaImplementacionesModal = ImplementacionSoluciones.objects.all()
        listaImplementacionesModal2 = ImplementacionSoluciones.objects.all()


        return render(request, "empleadosCustom/direccion/implementacionesSistemas.html",{"estaEnVerImplementacionesSistemas":estaEnVerImplementacionesSistemas,"id_admin":id_admin,
                                                                                          "nombreini":nombreini,"apellidosini":apellidosini,"correo":correo,"foto":foto,"nombreCompleto":nombreCompleto,"subdirector":subdirector, "listaImplementaciones":listaImplementaciones, "listaImplementacionesModal":listaImplementacionesModal, "listaImplementacionesModal2":listaImplementacionesModal2})
    else:
        return redirect("/login/")

def excelImplementacion(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Reporte Implementaciones '+str(datetime.today().strftime('%Y-%m-%d'))+'.xls'
    
    #creación de libro de excel
    libro = xlwt.Workbook(encoding='utf-8')
    hoja = libro.add_sheet('Implementaciones Sistemas')
    
    numero_fila = 0
    estilo_fuente = xlwt.XFStyle()
    estilo_fuente.font.bold = True
    
    columnas = ['Id Implementacion','Problema', 'Descripcion', 'Fecha Comienzo', 'Fecha Solución', 'Resuelto','Revisado','comentarios']
    for columna in range(len(columnas)):
        hoja.write(numero_fila, columna, columnas[columna], estilo_fuente)
        
    #lista la lista de cantidad_empleados

    listaImplementaciones = []
    implementaciones = ImplementacionSoluciones.objects.all()
    for implementacion in implementaciones:
        idim = implementacion.id_implementacion
        problema = implementacion.titulo_problema
        descripcion = implementacion.descripcion
        fechaComienzo = implementacion.fecha_comienzo
        fechaTerminado = implementacion.fecha_terminada
        if implementacion.resuelto == "S":
            resuelto = "Si"
        elif implementacion.resuelto == "N":
            resuelto = "No"

        if implementacion.revisado == "S":
            revisado = "Si"
        elif implementacion.revisado == "N":
            revisado = "No"
        
        comentarios = implementacion.comentarios_direccion

        listaImplementaciones.append([idim,problema,descripcion,fechaComienzo,fechaTerminado,resuelto,revisado,comentarios])
        


    
    estilo_fuente = xlwt.XFStyle()
    for imp in listaImplementaciones:
        numero_fila+=1
        for columna in range(len(imp)):
            hoja.write(numero_fila, columna, str(imp[columna]), estilo_fuente)
        
    
    
    
        
    libro.save(response)
    return response  
 







##DOCUMENTACIÓN  
def agregarDocumentosVehiculo(request):
    if "idSesion" in request.session:
        estaEnAgregarDocumentacion = True
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        if correo == "almacen01@customco.com.mx":
            almacen = True
        else:
            almacen = False
        nombreCompleto = nombre + " " + apellidos
        
        foto = fotoAdmin(request)

        if request.method == "POST": #Clic a boton guardar documentación
            idVehiculoSeleccionado = request.POST["selectVehi"]
            facturaVehiculo = request.FILES.get("documentoFacturaVehiculo")
            tarjetaCirculacion = request.FILES.get("documentoFacturaCirculacion")

            if "documentoPagoSeguro" in request.FILES:
                seguroVehiculo = request.FILES.get("documentoPagoSeguro")
                seGuardaraElSeguro = True
            else:
                seGuardaraElSeguro = False

            if "documentoArrendamiento" in request.FILES:
                arrendamiento = request.FILES.get("documentoArrendamiento")
                seGuardoArrendamiento = True
            else:
                seGuardoArrendamiento  = False
                

            if seGuardaraElSeguro == False and seGuardoArrendamiento == False:  #No se guardara ni seguro ni arrendamiento.
                registroDocumentacion = documentacionVehiculos(
                    vehiculo = Vehiculos.objects.get(id_vehiculo = idVehiculoSeleccionado),
                    factura_vehiculo = facturaVehiculo,
                    tarjeta_circulacion = tarjetaCirculacion)
            elif seGuardaraElSeguro == False and seGuardoArrendamiento == True:  #No se guardará el seguro pero si el arrendamiento
                registroDocumentacion = documentacionVehiculos(
                    vehiculo = Vehiculos.objects.get(id_vehiculo = idVehiculoSeleccionado),
                    factura_vehiculo = facturaVehiculo,
                    tarjeta_circulacion = tarjetaCirculacion,
                    contrato_arrendamiento = arrendamiento)
            elif seGuardaraElSeguro == True and seGuardoArrendamiento == False: #No se guardará el arrendamiento pero si el seguro
                registroDocumentacion = documentacionVehiculos(
                    vehiculo = Vehiculos.objects.get(id_vehiculo = idVehiculoSeleccionado),
                    factura_vehiculo = facturaVehiculo,
                    tarjeta_circulacion = tarjetaCirculacion,
                    pago_seguro = seguroVehiculo)
            elif seGuardaraElSeguro and seGuardoArrendamiento: #Se guardarán ambos
                registroDocumentacion = documentacionVehiculos(
                    vehiculo = Vehiculos.objects.get(id_vehiculo = idVehiculoSeleccionado),
                    factura_vehiculo = facturaVehiculo,
                    tarjeta_circulacion = tarjetaCirculacion,
                    pago_seguro = seguroVehiculo,
                    contrato_arrendamiento = arrendamiento)

            registroDocumentacion.save()

            if registroDocumentacion:
                request.session["documentacionAgregada"] = "La documentación ha sido agregada satisfactoriamente!"
                return redirect("/agregarDocumentosVehiculo/")

        else:
        
            empleado = Empleados.objects.filter(id_empleado = id_admin)
            for dato in empleado:
                area = dato.id_area_id

            consultaVehiculos = Vehiculos.objects.all()
            consultaDocumentosVehiculos = documentacionVehiculos.objects.all()

            idsVehiculosYaConDocumentacion = []

            vehiculosSinDocumentacion = []

            for documentacion in consultaDocumentosVehiculos:
                idVehiculo = documentacion.vehiculo_id
                idsVehiculosYaConDocumentacion.append(str(idVehiculo))

            for vehiculo in consultaVehiculos:
                idVehiculo = vehiculo.id_vehiculo
                idVehiculoStr = str(idVehiculo)
                if idVehiculoStr in idsVehiculosYaConDocumentacion:
                    yaTieneDocumentacion = True
                else:
                    codigoVehiculo = vehiculo.codigo_vehiculo
                    marcaVehiculo = vehiculo.marca_vehiculo
                    modeloVehiculo = vehiculo.modelo_vehiculo
                    colorVehiculo = vehiculo.color_vehiculo

                    vehiculosSinDocumentacion.append([idVehiculo, codigoVehiculo, marcaVehiculo, modeloVehiculo, colorVehiculo])

            if len(vehiculosSinDocumentacion) == 0:
                todosLosVehiculosTienenDocumentacion = True
            else:
                todosLosVehiculosTienenDocumentacion = False
    
            if area == 1 or area ==5 or area == 7 or area == 8 or area == 9 or area == 10:
                if area == 5:
                    solicitantePrestamo = True
                    administradordeVehiculos = True
                    

                    if "documentacionAgregada" in request.session:
                        documentacionAgregada = request.session["documentacionAgregada"]
                        del request.session["documentacionAgregada"]
                        return render(request,"empleadosCustom/ControlVehicular/Documentacion/agregarDocumentosVehiculo.html",{"estaEnAgregarDocumentacion":estaEnAgregarDocumentacion,"id_admin":id_admin,"nombre":nombre,"apellidos":apellidos,"correo":correo,"nombreCompleto":nombreCompleto,"solicitantePrestamo":solicitantePrestamo, "administradordeVehiculos":administradordeVehiculos,"foto":foto,"vehiculosSinDocumentacion":vehiculosSinDocumentacion, "documentacionAgregada":documentacionAgregada, "todosLosVehiculosTienenDocumentacion":todosLosVehiculosTienenDocumentacion, "almacen":almacen})

                    return render(request,"empleadosCustom/ControlVehicular/Documentacion/agregarDocumentosVehiculo.html",{"estaEnAgregarDocumentacion":estaEnAgregarDocumentacion,"id_admin":id_admin,"nombre":nombre,"apellidos":apellidos,"correo":correo,"nombreCompleto":nombreCompleto,"solicitantePrestamo":solicitantePrestamo, "administradordeVehiculos":administradordeVehiculos,"foto":foto,"vehiculosSinDocumentacion":vehiculosSinDocumentacion, "todosLosVehiculosTienenDocumentacion":todosLosVehiculosTienenDocumentacion, "almacen":almacen})
            
                solicitantePrestamo = True
                return render(request,"empleadosCustom/ControlVehicular/Documentacion/agregarDocumentosVehiculo.html",{"estaEnAgregarDocumentacion":estaEnAgregarDocumentacion,"id_admin":id_admin,"nombre":nombre,"apellidos":apellidos,"correo":correo,"nombreCompleto":nombreCompleto,"solicitantePrestamo":solicitantePrestamo, "almacen":almacen})
                
            return render(request,"empleadosCustom/ControlVehicular/Documentacion/agregarDocumentosVehiculo.html",{"estaEnAgregarDocumentacion":estaEnAgregarDocumentacion,"id_admin":id_admin,"nombre":nombre,"apellidos":apellidos,"correo":correo,"nombreCompleto":nombreCompleto, "almacen":almacen})
    else:
        return redirect('/login/')

def agregarPagoTenencia(request):
    if "idSesion" in request.session:
        estaEnAgregarPagoTenencia = True
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        if correo == "almacen01@customco.com.mx":
            almacen = True
        else:
            almacen = False
        nombreCompleto = nombre + " " + apellidos
        
        foto = fotoAdmin(request)

        if request.method == "POST":
            selectVehi = request.POST["selectVehi"]
            reciboTenencia = request.FILES.get("reciboTenencia")
            agregadoPor = id_admin
            añoTenencia = request.POST["añoTenencia"]
            fechaPagoTenencia = request.POST["fechaPago"]
            referenciaPago = request.POST["referenciaPago"]
            montoPagado = request.POST["montoPagado"]

            fecha_separada = fechaPagoTenencia.split("/") #29   06    2018            2018     29   06
            fecha_normal = fecha_separada[2] + "-" + fecha_separada[0] + "-" + fecha_separada[1]

            #Ver si hay placas nuevas
            if request.POST.get("checkboxPlaca", False): #Checkeado
                placaNueva = "Si"
                placaNuevaMandada = request.POST["placaNueva"]

                registroTenencia = tenenciasVehiculos(
                    vehiculo = Vehiculos.objects.get(id_vehiculo = selectVehi),
                    agregado_por = Empleados.objects.get(id_empleado = agregadoPor),
                    recibio_tenencia_vehiculo = reciboTenencia,
                    ano_pagado = añoTenencia,
                    fecha_tenencia = fecha_normal,
                    placas_nuevas = "Si",
                    referencia_pago_tenencia = referenciaPago,
                    monto_pagado_vehiculo = montoPagado
                )
                registroTenencia.save()

                #Actualizar placa.
                actualizacionPlaca = Vehiculos.objects.filter(id_vehiculo = selectVehi).update(placa_vehiculo = placaNuevaMandada)


            elif request.POST.get("checkboxPlaca", True): #No checkeado
                placaNueva = "No"
                registroTenencia = tenenciasVehiculos(
                    vehiculo = Vehiculos.objects.get(id_vehiculo = selectVehi),
                    agregado_por = Empleados.objects.get(id_empleado = agregadoPor),
                    recibio_tenencia_vehiculo = reciboTenencia,
                    ano_pagado = añoTenencia,
                    fecha_tenencia = fecha_normal,
                    placas_nuevas = "No",
                    referencia_pago_tenencia = referenciaPago,
                    monto_pagado_vehiculo = montoPagado
                )
                registroTenencia.save()

                
            


            if registroTenencia:
                request.session["tenenciaRegistrada"] = "Se ha registrado la tenencia correctamente!"

                #Mandar notificación de telegram
                try:
                    tokenTelegram = keysBotCustom.tokenBotVehiculos
                    botCustom = telepot.Bot(tokenTelegram)

                    idGrupoTelegram = keysBotCustom.idGrupoVehiculos

                    consultaVehiculo = Vehiculos.objects.filter(id_vehiculo = selectVehi)
                    for datoVehiculo in consultaVehiculo:
                        codigoVehiculo = datoVehiculo.codigo_vehiculo
                        marcaVehiculo = datoVehiculo.marca_vehiculo
                        modeloVehiculo = datoVehiculo.modelo_vehiculo
                        añoVehiculo = datoVehiculo.año_vehiculo
                        imagenVehiculo = datoVehiculo.imagen_frontal_vehiculo
                    

                    
                    mensaje = "\U0001F4B5 PAGO DE TENENCIA \U0001F4B5 \n Hola \U0001F44B! \n Se ha agregado al sistema el pago de tenencia del año "+str(añoTenencia)+" por un total de $"+str(montoPagado)+", vehículo #"+codigoVehiculo+"\n    Marca: "+marcaVehiculo+"\n    Modelo: "+modeloVehiculo+"\n    Año: "+añoVehiculo
                    botCustom.sendMessage(idGrupoTelegram,mensaje)
                except:
                    print("An exception occurred")


                #Mandar correo electrónico.
                asunto = "CS | Nueva Tenencia Vehicular."
                plantilla = "empleadosCustom/ControlVehicular/Documentacion/correoTenencia.html"
                

                #Datos de quien agrego.
                consultaEmpleadoAgrego = Empleados.objects.filter(id_empleado = agregadoPor)
                for datosEmpleado in consultaEmpleadoAgrego:
                    nombreEmpleado = datosEmpleado.nombre
                    apellidosEmpleado = datosEmpleado.apellidos

                nombreCompletoDeQuienAgrego = nombreEmpleado + " " + apellidosEmpleado

                            
                #Datos del empleado
                html_mensaje = render_to_string(plantilla, {"codigoVehiculo":codigoVehiculo,
                "marcaVehiculo":marcaVehiculo, "modeloVehiculo":modeloVehiculo, "añoVehiculo":añoVehiculo,
                "añoTenencia":añoTenencia,"placaNueva":placaNueva, "referenciaPago":referenciaPago,
                "montoPagado":montoPagado, "nombreCompletoDeQuienAgrego":nombreCompletoDeQuienAgrego, "imagenVehiculo":imagenVehiculo})
                email_remitente = settings.EMAIL_HOST_USER
                email_destino = ['sistemas@customco.com.mx']
                mensaje = EmailMessage(asunto, html_mensaje, email_remitente, email_destino)
                mensaje.content_subtype = 'html'
                mensaje.send()
                
                #Fin de mandar correo

                return redirect("/agregarPagoTenencia/")
            


        else:
            
            consultaVehiculos = Vehiculos.objects.all()
            consultaTenencias = tenenciasVehiculos.objects.all()

            idsVehiculosYaConTenencia = []

            vehiculosSinTenencia = []

            for tenencia in consultaTenencias:
                idVehiculo = tenencia.vehiculo_id
                idsVehiculosYaConTenencia.append(str(idVehiculo))

            for vehiculo in consultaVehiculos:
                idVehiculo = vehiculo.id_vehiculo
                idVehiculoStr = str(idVehiculo)
                if idVehiculoStr in idsVehiculosYaConTenencia:
                    yaTieneTenencia = True
                else:
                    codigoVehiculo = vehiculo.codigo_vehiculo
                    marcaVehiculo = vehiculo.marca_vehiculo
                    modeloVehiculo = vehiculo.modelo_vehiculo
                    colorVehiculo = vehiculo.color_vehiculo

                    vehiculosSinTenencia.append([idVehiculo, codigoVehiculo, marcaVehiculo, modeloVehiculo, colorVehiculo])

            if len(vehiculosSinTenencia) == 0:
                todosLosVehiculosTienenTenencia = True
            else:
                todosLosVehiculosTienenTenencia = False

            now = datetime.now()
            añoActual = now.strftime('%Y')
















            empleado = Empleados.objects.filter(id_empleado = id_admin)
            for dato in empleado:
                area = dato.id_area_id

            if area == 1 or area ==5 or area == 7 or area == 8 or area == 9 or area == 10:
                if area == 5:
                    solicitantePrestamo = True
                    administradordeVehiculos = True
                    if "tenenciaRegistrada" in request.session:
                        tenenciaRegistrada = request.session["tenenciaRegistrada"]
                        del request.session["tenenciaRegistrada"]
                        return render(request,"empleadosCustom/ControlVehicular/Documentacion/agregarPagoTenencia.html",{"estaEnAgregarPagoTenencia":estaEnAgregarPagoTenencia,"id_admin":id_admin,"nombre":nombre,"apellidos":apellidos,"correo":correo,"nombreCompleto":nombreCompleto,"solicitantePrestamo":solicitantePrestamo, "administradordeVehiculos":administradordeVehiculos,"foto":foto, "todosLosVehiculosTienenTenencia":todosLosVehiculosTienenTenencia, "vehiculosSinTenencia":vehiculosSinTenencia, "almacen":almacen, "añoActual":añoActual, "tenenciaRegistrada":tenenciaRegistrada})


                    return render(request,"empleadosCustom/ControlVehicular/Documentacion/agregarPagoTenencia.html",{"estaEnAgregarPagoTenencia":estaEnAgregarPagoTenencia,"id_admin":id_admin,"nombre":nombre,"apellidos":apellidos,"correo":correo,"nombreCompleto":nombreCompleto,"solicitantePrestamo":solicitantePrestamo, "administradordeVehiculos":administradordeVehiculos,"foto":foto, "todosLosVehiculosTienenTenencia":todosLosVehiculosTienenTenencia, "vehiculosSinTenencia":vehiculosSinTenencia, "almacen":almacen, "añoActual":añoActual})
                
                solicitantePrestamo = True
                return render(request,"empleadosCustom/ControlVehicular/Documentacion/agregarPagoTenencia.html",{"estaEnAgregarPagoTenencia":estaEnAgregarPagoTenencia,"id_admin":id_admin,"nombre":nombre,"apellidos":apellidos,"correo":correo,"nombreCompleto":nombreCompleto,"solicitantePrestamo":solicitantePrestamo, "almacen":almacen})
                
    
    

    
        return render(request,"empleadosCustom/ControlVehicular/Documentacion/agregarPagoTenencia.html",{"estaEnAgregarPagoTenencia":estaEnAgregarPagoTenencia,"id_admin":id_admin,"nombre":nombre,"apellidos":apellidos,"correo":correo,"nombreCompleto":nombreCompleto, "almacen":almacen})
    else:
        return redirect('/login/') 


##GESTIÓN
def agregarVehiculos (request):
    if "idSesion" in request.session:
        estaEnAgregarVehiculos = True
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        if correo == "almacen01@customco.com.mx":
            almacen = True
        else:
            almacen = False
        nombreCompleto = nombre + " " + apellidos
        
        foto = fotoAdmin(request)
        if request.method=="POST":
            marcaVehiculo = request.POST["marcVehi"]
            modeloVehiculo = request.POST["modelVehi"]
            numeroSerie = request.POST["numSerie"]
            añoVehiculo = request.POST["añoVehi"]
            colorVehiculo = request.POST["colorVehi"]
            placaVehiculo = request.POST["numPlaca"]
            transmisionVehiculo = request.POST["transmisionVehi"]
            responsableVehiculo = request.POST["responsableVehi"]
            ultimoKilometrajeVehiculo = request.POST["ultimoKilom"]
            ultimoKilometrajeVehiculo = int(ultimoKilometrajeVehiculo)
            estatusVehiculo = request.POST["estatusVehi"]
            fotografiaFrontal = request.FILES.get('fotografiaFrontal')
            fotografiaTrasera = request.FILES.get('fotografiaTrasera')
            fotografiaLateralIzquierda = request.FILES.get('fotografiaLateralIzquierda')
            fotografiaLateralDerecha = request.FILES.get('fotografiaLateralDerecha')

            consultaVehiculos = Vehiculos.objects.all()
            if consultaVehiculos:
                ultimoCodigoVehiculo = ""
                for vehiculo in consultaVehiculos:
                    ultimoCodigoVehiculo = vehiculo.codigo_vehiculo

                splitCodigo = ultimoCodigoVehiculo.split("-")
                codigoCodigo = splitCodigo[1]
                codigoNuevo = int(codigoCodigo)+1

                codigoNuevoAAgregar = "VEH-"+str(codigoNuevo)
            else:
                codigoNuevoAAgregar = "VEH-1000"

            fechaAltaVehiculo = datetime.now()

            registroVehiculo = Vehiculos(
                codigo_vehiculo = codigoNuevoAAgregar,
                marca_vehiculo = marcaVehiculo,
                modelo_vehiculo = modeloVehiculo,
                numero_serie_vehiculo = numeroSerie,
                color_vehiculo = colorVehiculo,
                año_vehiculo = añoVehiculo,
                placa_vehiculo = placaVehiculo,
                transmision_vehiculo = transmisionVehiculo,
                responsable_actual = Empleados.objects.get(id_empleado = responsableVehiculo),
                ultimo_km_registrado = ultimoKilometrajeVehiculo,
                status_vehiculo = estatusVehiculo,
                fecha_alta_vehiculo = fechaAltaVehiculo,
                imagen_frontal_vehiculo = fotografiaFrontal,
                imagen_trasera_vehiculo = fotografiaTrasera,
                imagen_lateralIzquierda_vehiculo = fotografiaLateralIzquierda,
                imagen_lateralDerecha_vehiculo = fotografiaLateralDerecha
            )

            registroVehiculo.save()

            if registroVehiculo:

                 #Mandar notificación de telegram
                try:
                    tokenTelegram = keysBotCustom.tokenBotVehiculos
                    botCustom = telepot.Bot(tokenTelegram)

                    idGrupoTelegram = keysBotCustom.idGrupoVehiculos

                    consultaEmpleado = Empleados.objects.filter(id_empleado = responsableVehiculo)
                    for datoEmpleado in consultaEmpleado:
                        nombre = datoEmpleado.nombre
                        apellidos = datoEmpleado.apellidos

                    nombreResponsableActual = nombre + " "+ apellidos
                    

                    
                    mensaje = "\U0001F698 VEHÍCULO AGREGADO \U0001F698 \n Hola \U0001F44B! \n Se ha agregado al sistema el vehículo #"+codigoNuevoAAgregar+"\n    Marca: "+marcaVehiculo+"\n    Modelo: "+modeloVehiculo+"\n    Año: "+añoVehiculo+"\n    Num Serie: "+numeroSerie+"\n    Placas: "+placaVehiculo+"\n    Responsable actual:  "+nombreResponsableActual
                    botCustom.sendMessage(idGrupoTelegram,mensaje)
                except:
                    print("An exception occurred")


                request.session["vehiculoAgregado"] = "El vehiculo "+modeloVehiculo+" se ha agregado satisfactoriamente!"
                return redirect("/agregarVehiculos/")

 
        else:
            empleado = Empleados.objects.filter(id_empleado = id_admin)
            for dato in empleado:
                area = dato.id_area_id
                
            ##Sacar todos los datos de los empleados activos en el sistema
            consultaEmpleados = Empleados.objects.filter(activo= "A")
            

            if area == 1 or area ==5 or area == 7 or area == 8 or area == 9 or area == 10:
                if area == 5:
                    solicitantePrestamo = True
                    administradordeVehiculos = True
                    if "vehiculoAgregado" in request.session:
                        vehiculoAgregado = request.session["vehiculoAgregado"]
                        del request.session["vehiculoAgregado"]
                        return render(request,"empleadosCustom/ControlVehicular/Gestion/agregarVehiculos.html",{"estaEnAgregarVehiculos":estaEnAgregarVehiculos,"id_admin":id_admin,"nombre":nombre,"apellidos":apellidos,"correo":correo,"nombreCompleto":nombreCompleto,"solicitantePrestamo":solicitantePrestamo, "administradordeVehiculos":administradordeVehiculos,"foto":foto,"consultaEmpleados":consultaEmpleados,"vehiculoAgregado":vehiculoAgregado, "almacen":almacen})
                    
                    return render(request,"empleadosCustom/ControlVehicular/Gestion/agregarVehiculos.html",{"estaEnAgregarVehiculos":estaEnAgregarVehiculos,"id_admin":id_admin,"nombre":nombre,"apellidos":apellidos,"correo":correo,"nombreCompleto":nombreCompleto,"solicitantePrestamo":solicitantePrestamo, "administradordeVehiculos":administradordeVehiculos,"foto":foto,"consultaEmpleados":consultaEmpleados, "almacen":almacen})
                
                solicitantePrestamo = True
                return render(request,"empleadosCustom/ControlVehicular/Gestion/agregarVehiculos.html",{"estaEnAgregarVehiculos":estaEnAgregarVehiculos,"id_admin":id_admin,"nombre":nombre,"apellidos":apellidos,"correo":correo,"nombreCompleto":nombreCompleto,"solicitantePrestamo":solicitantePrestamo,"consultaEmpleados":consultaEmpleados, "almacen":almacen})
                
            
    
    


        return render(request,"empleadosCustom/ControlVehicular/Gestion/agregarVehiculos.html",{"estaEnAgregarVehiculos":estaEnAgregarVehiculos,"id_admin":id_admin,"nombre":nombre,"apellidos":apellidos,"correo":correo,"nombreCompleto":nombreCompleto, "almacen":almacen})
    else:
        return redirect('/login/')
 
def verVehiculos (request):
    if "idSesion" in request.session:
        estaEnVerVehiculos = True
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        if correo == "almacen01@customco.com.mx":
            almacen = True
        else:
            almacen = False
        nombreCompleto = nombre + " " + apellidos
        
        foto = fotoAdmin(request)
        
        empleado = Empleados.objects.filter(id_empleado = id_admin)
        for dato in empleado:
            area = dato.id_area_id

        if area == 1 or area ==5 or area == 7 or area == 8 or area == 9 or area == 10:
            if area == 5:
                solicitantePrestamo = True
                administradordeVehiculos = True

                listaVehiculos = Vehiculos.objects.all()

                listaResponsables = []
                for vehiculo in listaVehiculos:
                    idEncargado = vehiculo.responsable_actual_id
                    consultaEmpleado = Empleados.objects.filter(id_empleado = idEncargado)
                    for datoEmpleado in consultaEmpleado:
                        nombreEmpleado = datoEmpleado.nombre
                        apellidosEmpleado = datoEmpleado.apellidos

                    nombreCompletoEmpleado = nombreEmpleado + " " + apellidosEmpleado
                    listaResponsables.append(nombreCompletoEmpleado)

                listaVehiculosResponsables = zip(listaVehiculos, listaResponsables)


                if "kmActualizado" in request.session:
                    kmActualizado = request.session["kmActualizado"]
                    del request.session["kmActualizado"]

                    return render(request,"empleadosCustom/ControlVehicular/Gestion/verVehiculos.html",{"estaEnVerVehiculos":estaEnVerVehiculos,"id_admin":id_admin,"nombre":nombre,"apellidos":apellidos,"correo":correo,"nombreCompleto":nombreCompleto,"solicitantePrestamo":solicitantePrestamo, "administradordeVehiculos":administradordeVehiculos,"foto":foto, "listaVehiculosResponsables":listaVehiculosResponsables, "almacen":almacen, "kmActualizado":kmActualizado})

                if "bajaVehiculo" in request.session:
                    bajaVehiculo = request.session["bajaVehiculo"]
                    del request.session["bajaVehiculo"]
                    return render(request,"empleadosCustom/ControlVehicular/Gestion/verVehiculos.html",{"estaEnVerVehiculos":estaEnVerVehiculos,"id_admin":id_admin,"nombre":nombre,"apellidos":apellidos,"correo":correo,"nombreCompleto":nombreCompleto,"solicitantePrestamo":solicitantePrestamo, "administradordeVehiculos":administradordeVehiculos,"foto":foto, "listaVehiculosResponsables":listaVehiculosResponsables, "almacen":almacen, "bajaVehiculo":bajaVehiculo})

                


                return render(request,"empleadosCustom/ControlVehicular/Gestion/verVehiculos.html",{"estaEnVerVehiculos":estaEnVerVehiculos,"id_admin":id_admin,"nombre":nombre,"apellidos":apellidos,"correo":correo,"nombreCompleto":nombreCompleto,"solicitantePrestamo":solicitantePrestamo, "administradordeVehiculos":administradordeVehiculos,"foto":foto, "listaVehiculosResponsables":listaVehiculosResponsables, "almacen":almacen})
            
            solicitantePrestamo = True
            return render(request,"empleadosCustom/ControlVehicular/Gestion/verVehiculos.html",{"estaEnVerVehiculos":estaEnVerVehiculos,"id_admin":id_admin,"nombre":nombre,"apellidos":apellidos,"correo":correo,"nombreCompleto":nombreCompleto,"solicitantePrestamo":solicitantePrestamo, "almacen":almacen})
            
        
    
    


        return render(request,"empleadosCustom/ControlVehicular/gestion/verVehiculos.html",{"estaEnVerVehiculos":estaEnVerVehiculos,"id_admin":id_admin,"nombre":nombre,"apellidos":apellidos,"correo":correo,"nombreCompleto":nombreCompleto, "almacen":almacen})
    else:
        return redirect('/login/')


#ALINEACION Y BALANCEO
def agregarAltaMantenimientoVehiculo (request):
    if "idSesion" in request.session:
        estaEnAgregarMantenimientos = True
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        if correo == "almacen01@customco.com.mx":
            almacen = True
        else:
            almacen = False
        nombreCompleto = nombre + " " + apellidos
        
        foto = fotoAdmin(request)
        

        if request.method == "POST":
            botonApretado = True
            idVehiculo = request.POST["idVehiculo"]
            agregadoPor = id_admin


            alineacionRealizada = ""
            balanceoRealizado = ""
            cambioLlantasRealizado= ""

            #Ver si se realizo alineacion
            if request.POST.get("checkboxAlineacion", False): #Checkeado
                alineacion = "Si"
                alineacionRealizada = "Si"
            elif request.POST.get("checkboxAlineacion", True): #No chequeado
                alineacion = "No"
                alineacionRealizada = "No"

            #Ver si se realizo balanceo
            if request.POST.get("checkboxBalanceo", False): #Checkeado
                balanceo = "Si"
                balanceoRealizado = "Si"
            elif request.POST.get("checkboxBalanceo", True): #No chequeado
                balanceo = "No"
                balanceoRealizado = "No"

            #Ver si se realizo cambio de llantas
            if request.POST.get("checkboxCambioLlantaspython", False): #Checkeado
                cambioLlantas = "Si"
                cambioLlantasRealizado = "Si"

                llantasCambiadas = request.POST["numeroLlantasCambiadas"]
                intLlantasCambiadas = int(llantasCambiadas)
                medidaLlantaNueva = request.POST["medidaLlantaNueva"]
                medidaLlanta = medidaLlantaNueva
                marcaLlantasNuevas = request.POST["marcaLlantasNuevas"]
                marcaLlanta = marcaLlantasNuevas
            elif request.POST.get("checkboxCambioLlantaspython", True): #No chequeado
                cambioLlantas = "No"
                cambioLlantasRealizado = "No"
                llantasCambiadas = "x"
                medidaLlanta = "x"
                marcaLlanta = "x"
            
            observaciones = request.POST["observaciones"]
            kilometrajePreAlineacion = request.POST["ultimoKilometraje"]
            kilometrajePreAlineacionInt = int(kilometrajePreAlineacion)
            
            fechaAlineacion = request.POST["fechaAlineacion"]
            fecha_separada = fechaAlineacion.split("/") #29   06    2018            2018     29   06
            fecha_normal = fecha_separada[2] + "-" + fecha_separada[0] + "-" + fecha_separada[1]
            facturaAlineacion = request.FILES.get('facturaAlineacionBalanceo')

            montoPagado = request.POST["montoPagado"]

            #Si se realizo cambio de llantas...
            if cambioLlantas == "Si":
                registroAlineacionYBalanceo = alineacionyBalanceo(
                    id_vehiculo = Vehiculos.objects.get(id_vehiculo = idVehiculo),
                    agregado_por = Empleados.objects.get(id_empleado = agregadoPor),
                    alineacion_realizada = alineacion,
                    balanceo_realizado = balanceo,
                    cambio_llantas = cambioLlantas,
                    numero_cambio_llantas = intLlantasCambiadas,
                    medida_llanta_nueva = medidaLlantaNueva,
                    marca_llanta_nueva = marcaLlantasNuevas,
                    observaciones = observaciones,
                    kilometraje_prealineacion = kilometrajePreAlineacionInt,
                    fecha_alineacion = fecha_normal,
                    factura_alineacion = facturaAlineacion,
                    monto_pagado = montoPagado
                )
                registroAlineacionYBalanceo.save()

            #Si no...
            else:
                registroAlineacionYBalanceo = alineacionyBalanceo(
                    id_vehiculo = Vehiculos.objects.get(id_vehiculo = idVehiculo),
                    agregado_por = Empleados.objects.get(id_empleado = agregadoPor),
                    alineacion_realizada = alineacion,
                    balanceo_realizado = balanceo,
                    cambio_llantas = cambioLlantas,
                    observaciones = observaciones,
                    kilometraje_prealineacion = kilometrajePreAlineacionInt,
                    fecha_alineacion = fecha_normal,
                    factura_alineacion = facturaAlineacion,
                    monto_pagado = montoPagado
                )
                registroAlineacionYBalanceo.save()

            if registroAlineacionYBalanceo:
                #Actualizar kilometraje del vehiculo
                actualizacionVehiculo = Vehiculos.objects.filter(id_vehiculo = idVehiculo).update(ultimo_km_registrado = kilometrajePreAlineacionInt)

                 #Mandar notificación de telegram
                try:
                    tokenTelegram = keysBotCustom.tokenBotVehiculos
                    botCustom = telepot.Bot(tokenTelegram)

                    idGrupoTelegram = keysBotCustom.idGrupoVehiculos


                    consultaVehiculo = Vehiculos.objects.filter(id_vehiculo = idVehiculo)
                    for datoVehiculo in consultaVehiculo:
                        codigoVehiculo = datoVehiculo.codigo_vehiculo
                        marcaVehiculo = datoVehiculo.marca_vehiculo
                        modeloVehiculo = datoVehiculo.modelo_vehiculo
                        añoVehiculo = datoVehiculo.año_vehiculo
                        imagenVehiculo = datoVehiculo.imagen_frontal_vehiculo
                        idEmpleadoResponsable = datoVehiculo.responsable_actual_id
                    
                    consultaEmpleado = Empleados.objects.filter(id_empleado = idEmpleadoResponsable)
                    for datoEmpleado in consultaEmpleado:
                        nombre = datoEmpleado.nombre
                        apellidos = datoEmpleado.apellidos

                    nombreResponsableActual = nombre + " "+ apellidos
                    

                    
                    mensaje = "\U0001F6DE ALINEACIÓN Y BALANCEO \U0001F6DE \n Hola \U0001F44B! \n Se ha agregado registro de alineación y balanceo para el vehículo #"+codigoVehiculo+"\n    Marca: "+marcaVehiculo+"\n    Modelo: "+modeloVehiculo+"\n    Año: "+añoVehiculo+"\n    Responsable actual:  "+nombreResponsableActual
                    botCustom.sendMessage(idGrupoTelegram,mensaje)
                except:
                    print("An exception occurred")

                #Mandar correo electrónico.
                asunto = "CS | Nueva alineación y balanceo."
                plantilla = "empleadosCustom/ControlVehicular/Mantenimiento/correoAlineacion.html"
                

                

                            
                #Datos del empleado
                html_mensaje = render_to_string(plantilla, {"codigoVehiculo":codigoVehiculo,"imagenVehiculo":imagenVehiculo,"marcaVehiculo":marcaVehiculo,"modeloVehiculo":modeloVehiculo,"añoVehiculo":añoVehiculo,"alineacionRealizada":alineacionRealizada,"balanceoRealizado":balanceoRealizado,"cambioLlantasRealizado":cambioLlantasRealizado,
                "llantasCambiadas":llantasCambiadas,"medidaLlanta":medidaLlanta,"marcaLlanta":marcaLlanta,"observaciones":observaciones,"montoPagado":montoPagado,"kilometraje":kilometrajePreAlineacion,"fechaAlineacion":fecha_normal, "nombreResponsableActual":nombreResponsableActual})
                email_remitente = settings.EMAIL_HOST_USER
                email_destino = ['sistemas@customco.com.mx']
                
                mensaje = EmailMessage(asunto, html_mensaje, email_remitente, email_destino)
                mensaje.content_subtype = 'html'
                mensaje.send()
                
                #Fin de mandar correo


                



                request.session["alineacionYBalanceoRegistrado"] = "La alineación y balanceo fue guardada satisfactoriamente!"

                return redirect("/agregarAltaMantenimientoVehiculo/")


        else:
            empleado = Empleados.objects.filter(id_empleado = id_admin)
            for dato in empleado:
                area = dato.id_area_id

            if area == 1 or area ==5 or area == 7 or area == 8 or area == 9 or area == 10:
                if area == 5:
                    solicitantePrestamo = True
                    administradordeVehiculos = True

                    listaVehiculos = Vehiculos.objects.filter(status_vehiculo = "En uso")

                    if "alineacionYBalanceoRegistrado" in request.session:
                        alineacionYBalanceoRegistrado = request.session["alineacionYBalanceoRegistrado"]
                        del request.session["alineacionYBalanceoRegistrado"]

                        return render(request,"empleadosCustom/ControlVehicular/Mantenimiento/agregarMantenimientosVehiculo.html",{"estaEnAgregarMantenimientos":estaEnAgregarMantenimientos,"id_admin":id_admin,"nombre":nombre,"apellidos":apellidos,"correo":correo,"nombreCompleto":nombreCompleto,"solicitantePrestamo":solicitantePrestamo, "administradordeVehiculos":administradordeVehiculos,"foto":foto, "almacen":almacen, 
                        "listaVehiculos":listaVehiculos, "alineacionYBalanceoRegistrado":alineacionYBalanceoRegistrado})


                    return render(request,"empleadosCustom/ControlVehicular/Mantenimiento/agregarMantenimientosVehiculo.html",{"estaEnAgregarMantenimientos":estaEnAgregarMantenimientos,"id_admin":id_admin,"nombre":nombre,"apellidos":apellidos,"correo":correo,"nombreCompleto":nombreCompleto,"solicitantePrestamo":solicitantePrestamo, "administradordeVehiculos":administradordeVehiculos,"foto":foto, "almacen":almacen, 
                    "listaVehiculos":listaVehiculos})
                
                solicitantePrestamo = True
                return render(request,"empleadosCustom/ControlVehicular/Mantenimiento/agregarMantenimientosVehiculo.html",{"estaEnAgregarMantenimientos":estaEnAgregarMantenimientos,"id_admin":id_admin,"nombre":nombre,"apellidos":apellidos,"correo":correo,"nombreCompleto":nombreCompleto,"solicitantePrestamo":solicitantePrestamo, "almacen":almacen})
                
        
            return render(request,"empleadosCustom/ControlVehicular/Mantenimiento/agregarMantenimientosVehiculo.html",{"estaEnAgregarMantenimientos":estaEnAgregarMantenimientos,"id_admin":id_admin,"nombre":nombre,"apellidos":apellidos,"correo":correo,"nombreCompleto":nombreCompleto,"almacen":almacen})
    else:
        return redirect('/login/')
    
def verMantenimientosVehiculo (request):
    if "idSesion" in request.session:
        estaEnVerMantenimientos = True
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        if correo == "almacen01@customco.com.mx":
            almacen = True
        else:
            almacen = False
        nombreCompleto = nombre + " " + apellidos
        
        foto = fotoAdmin(request)
        
        empleado = Empleados.objects.filter(id_empleado = id_admin)
        for dato in empleado:
            area = dato.id_area_id

        if area == 1 or area ==5 or area == 7 or area == 8 or area == 9 or area == 10:
            if area == 5:
                solicitantePrestamo = True
                administradordeVehiculos = True

                consultaAlineacionesBalanceos = alineacionyBalanceo.objects.all()

                datosTabla = []

                for alineacion in consultaAlineacionesBalanceos:
                    idAlineacion = alineacion.id_alineacion_balanceo
                    idVehiculo = alineacion.id_vehiculo_id
                    consultaVehiculo = Vehiculos.objects.filter(id_vehiculo = idVehiculo)

                    for datoVehiculo in consultaVehiculo:
                        codigoVehiculo = datoVehiculo.codigo_vehiculo
                        marcaVehiculo = datoVehiculo.marca_vehiculo
                        modeloVehiculo = datoVehiculo.modelo_vehiculo
                        añoVehiculo =   datoVehiculo.año_vehiculo

                    fechaAlineacion = alineacion.fecha_alineacion
                    alineacionRealizada = alineacion.alineacion_realizada
                    balanceoRealizado = alineacion.balanceo_realizado
                    cambioLlantas = alineacion.cambio_llantas
                    factura = alineacion.factura_alineacion

                    arrayCambioLlantas = []
                    if cambioLlantas == "Si":
                        numeroLlantasCambiadas = alineacion.numero_cambio_llantas
                        medidaLlantaNueva = alineacion.medida_llanta_nueva
                        marcaLlantaNueva = alineacion.marca_llanta_nueva
                        arrayCambioLlantas.append([numeroLlantasCambiadas,medidaLlantaNueva, marcaLlantaNueva])

                    else:
                        arrayCambioLlantas.append("jaja")

                    observaciones = alineacion.observaciones
                    kmPreAlineacion = alineacion.kilometraje_prealineacion
                    
                    datosTabla.append([idAlineacion, codigoVehiculo, marcaVehiculo,
                    modeloVehiculo, añoVehiculo, fechaAlineacion, alineacionRealizada,
                    balanceoRealizado, cambioLlantas, arrayCambioLlantas, observaciones, kmPreAlineacion, factura])


                return render(request,"empleadosCustom/ControlVehicular/Mantenimiento/verMantenimientosVehiculo.html",{"estaEnVerMantenimientos":estaEnVerMantenimientos,"id_admin":id_admin,"nombre":nombre,"apellidos":apellidos,"correo":correo,"nombreCompleto":nombreCompleto,"solicitantePrestamo":solicitantePrestamo, "administradordeVehiculos":administradordeVehiculos,"foto":foto,"almacen":almacen,
                "datosTabla":datosTabla})
            
            solicitantePrestamo = True
            return render(request,"empleadosCustom/ControlVehicular/Mantenimiento/verMantenimientosVehiculo.html",{"estaEnVerMantenimientos":estaEnVerMantenimientos,"id_admin":id_admin,"nombre":nombre,"apellidos":apellidos,"correo":correo,"nombreCompleto":nombreCompleto,"solicitantePrestamo":solicitantePrestamo,"almacen":almacen})
            
    
    

    
        return render(request,"empleadosCustom/ControlVehicular/Mantenimiento/verMantenimientosVehiculo.html",{"estaEnVerMantenimientos":estaEnVerMantenimientos,"id_admin":id_admin,"nombre":nombre,"apellidos":apellidos,"correo":correo,"nombreCompleto":nombreCompleto,"almacen":almacen})
    else:
        return redirect('/login/')
    

##SERVICIOS
def agregarAltaServicio(request):
    if "idSesion" in request.session:
        estaEnAgregarAltaServicio = True
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        if correo == "almacen01@customco.com.mx":
            almacen = True
        else:
            almacen = False
        nombreCompleto = nombre + " " + apellidos
        
        foto = fotoAdmin(request)
        
        if request.method == "POST":
            idVehiculo = request.POST["selectVehi"]
            tipoServicio = request.POST["tipoServicio"]

            serviciosRealizados = request.POST.getlist('serviciosRealizados')  #ES un arreglo de todo lo que se manda en el select
            kilometrajePreServicio = request.POST["ultimoKilometraje"]
            fechaServicio = request.POST["fechaServicio"]
            tallerMecanico = request.POST["tallerMecanico"]
            montoPagado = request.POST["montoPagado"]

            facturaServicio = request.FILES.get('facturaServicio')
            
            listaServiciosRealizados = ""
            contadorServicios = 0
            for servicio in serviciosRealizados:
                contadorServicios = contadorServicios + 1
                if contadorServicios == 1:
                    listaServiciosRealizados = listaServiciosRealizados
                else:
                    listaServiciosRealizados = listaServiciosRealizados +","+servicio


            fechaSeparada = fechaServicio.split("/") #29   06    2018
            fechaNormal = fechaSeparada[2] + "-" + fechaSeparada[0] + "-" + fechaSeparada[1]

            kilometrajePreServicioInt = int(kilometrajePreServicio)
            

            #Registrar servicio

            registroServicio = serviciosVehiculos(
                vehiculo = Vehiculos.objects.get(id_vehiculo = idVehiculo),
                fecha_servicios_vehiculo = fechaNormal,
                tipo_servicio = tipoServicio,
                servicios_realizados = listaServiciosRealizados,
                kilometraje_preservicio = kilometrajePreServicioInt,
                taller_servicio = tallerMecanico,
                monto_pagado = montoPagado,
                agregado_por = Empleados.objects.get(id_empleado = id_admin),
                factura_servicios = facturaServicio
            )

            registroServicio.save()

            if registroServicio:
                #Actualizar kilometraje del vehiculo
                actualizacionVehiculo = Vehiculos.objects.filter(id_vehiculo = idVehiculo).update(ultimo_km_registrado = kilometrajePreServicioInt)


                #Mandar notificación de telegram
                try:
                    tokenTelegram = keysBotCustom.tokenBotVehiculos
                    botCustom = telepot.Bot(tokenTelegram)

                    idGrupoTelegram = keysBotCustom.idGrupoVehiculos


                    consultaVehiculo = Vehiculos.objects.filter(id_vehiculo = idVehiculo)
                    for datoVehiculo in consultaVehiculo:
                        codigoVehiculo = datoVehiculo.codigo_vehiculo
                        marcaVehiculo = datoVehiculo.marca_vehiculo
                        modeloVehiculo = datoVehiculo.modelo_vehiculo
                        añoVehiculo = datoVehiculo.año_vehiculo
                        idEmpleadoResponsable = datoVehiculo.responsable_actual_id
                        imagenVehiculo = datoVehiculo.imagen_frontal_vehiculo
                    
                    consultaEmpleado = Empleados.objects.filter(id_empleado = idEmpleadoResponsable)
                    for datoEmpleado in consultaEmpleado:
                        nombre = datoEmpleado.nombre
                        apellidos = datoEmpleado.apellidos

                    nombreResponsableActual = nombre + " "+ apellidos
                    
                    serviciosRealizados = ""

                    listaArrayServicios = listaServiciosRealizados.split(",")
                    for serv in listaArrayServicios:
                        serviciosRealizados = serviciosRealizados + "\n "+str(serv)
                    
                    mensaje = "\U0001F6E0 SERVICIO VEHICULAR \U0001F6E0 \n Hola \U0001F44B! \n Se ha agregado un nuevo servicio de tipo "+tipoServicio+" por $"+str(montoPagado)+" MXN. para el vehículo #"+codigoVehiculo+"\n    Marca: "+marcaVehiculo+"\n    Modelo: "+modeloVehiculo+"\n    Año: "+añoVehiculo+"\n    Responsable actual:  "+nombreResponsableActual+"\n\n Servicios realizados:"+serviciosRealizados
                    botCustom.sendMessage(idGrupoTelegram,mensaje)
                except:
                    print("An exception occurred")


                #Mandar correo electrónico.
                asunto = "CS | Nuevo servicio vehicular."
                plantilla = "empleadosCustom/ControlVehicular/Servicio/correoServicio.html"
                

                
            
                            
                #Datos del empleado
                html_mensaje = render_to_string(plantilla, {"codigoVehiculo":codigoVehiculo,"imagenVehiculo":imagenVehiculo,"marcaVehiculo":marcaVehiculo,"modeloVehiculo":modeloVehiculo,"añoVehiculo":añoVehiculo,"nombreResponsableActual":nombreResponsableActual,"tipoServicio":tipoServicio,"kilometrajePreServicioInt":kilometrajePreServicioInt,"tallerServicio":tallerMecanico,"montoPagado":montoPagado,"listaArrayServicios":listaArrayServicios})
                email_remitente = settings.EMAIL_HOST_USER
                email_destino = ['sistemas@customco.com.mx']
                
                mensaje = EmailMessage(asunto, html_mensaje, email_remitente, email_destino)
                mensaje.content_subtype = 'html'
                mensaje.send()
                
                #Fin de mandar correo






                request.session["servicioAgregado"] = "El servicio fue agregado satisfactoriamente al sistema!!"

                return redirect("/agregarAltaServicio/")
            



        else:
                
            empleado = Empleados.objects.filter(id_empleado = id_admin)
            for dato in empleado:
                area = dato.id_area_id

            if area == 1 or area ==5 or area == 7 or area == 8 or area == 9 or area == 10:
                if area == 5:
                    solicitantePrestamo = True
                    administradordeVehiculos = True

                    listaVehiculos = Vehiculos.objects.filter(status_vehiculo = "En uso")

                    if "servicioAgregado" in request.session:
                        servicioAgregado = request.session["servicioAgregado"]
                        del request.session["servicioAgregado"]

                        return render(request,"empleadosCustom/ControlVehicular/Servicio/altaServicio.html",{"estaEnAgregarAltaServicio":estaEnAgregarAltaServicio,"id_admin":id_admin,"nombre":nombre,"apellidos":apellidos,"correo":correo,"nombreCompleto":nombreCompleto,"solicitantePrestamo":solicitantePrestamo, "administradordeVehiculos":administradordeVehiculos,"foto":foto,"almacen":almacen, 
                        "listaVehiculos":listaVehiculos, "servicioAgregado":servicioAgregado})

                    return render(request,"empleadosCustom/ControlVehicular/Servicio/altaServicio.html",{"estaEnAgregarAltaServicio":estaEnAgregarAltaServicio,"id_admin":id_admin,"nombre":nombre,"apellidos":apellidos,"correo":correo,"nombreCompleto":nombreCompleto,"solicitantePrestamo":solicitantePrestamo, "administradordeVehiculos":administradordeVehiculos,"foto":foto,"almacen":almacen, 
                    "listaVehiculos":listaVehiculos})
                
                solicitantePrestamo = True
                return render(request,"empleadosCustom/ControlVehicular/Servicio/altaServicio.html",{"estaEnAgregarAltaServicio":estaEnAgregarAltaServicio,"id_admin":id_admin,"nombre":nombre,"apellidos":apellidos,"correo":correo,"nombreCompleto":nombreCompleto,"solicitantePrestamo":solicitantePrestamo,"almacen":almacen})
            
    
    

    
        return render(request,"empleadosCustom/ControlVehicular/Servicio/altaServicio.html",{"estaEnAgregarAltaServicio":estaEnAgregarAltaServicio,"id_admin":id_admin,"nombre":nombre,"apellidos":apellidos,"correo":correo,"nombreCompleto":nombreCompleto,"almacen":almacen})
    else:
        return redirect('/login/')
    
def verServicio (request):
    if "idSesion" in request.session:
        estaEnVerServicio = True
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        if correo == "almacen01@customco.com.mx":
            almacen = True
        else:
            almacen = False
        nombreCompleto = nombre + " " + apellidos
        
        foto = fotoAdmin(request)
        
        empleado = Empleados.objects.filter(id_empleado = id_admin)
        for dato in empleado:
            area = dato.id_area_id

        if area == 1 or area ==5 or area == 7 or area == 8 or area == 9 or area == 10:
            if area == 5:
                solicitantePrestamo = True
                administradordeVehiculos = True

                listaServiciosTabla = []

                consultaServicios = serviciosVehiculos.objects.all()
                
                totalGastadoEnServicios = 0
                for servicio in consultaServicios:
                    idServicio = servicio.id_servicio
                    idVehiculo = servicio.vehiculo_id

                    consultaVehiculo = Vehiculos.objects.filter(id_vehiculo = idVehiculo)
                    for datoVehiculo in consultaVehiculo:
                        codigoVehiculo = datoVehiculo.codigo_vehiculo
                        marcaVehiculo = datoVehiculo.marca_vehiculo
                        modeloVehiculo = datoVehiculo.modelo_vehiculo
                        añoVehiculo = datoVehiculo.año_vehiculo

                    fechaServicio = servicio.fecha_servicios_vehiculo
                    tipoServicio = servicio.tipo_servicio
                    serviciosRealizados = servicio.servicios_realizados #String con comas.

                   
                    arregloServicios = serviciosRealizados.split(",")

                    kmPreServicio = servicio.kilometraje_preservicio
                    tallerServicio = servicio.taller_servicio
                    montoPagado = servicio.monto_pagado
                    idEmpleadoAgregadoPor = servicio.agregado_por_id

                    monto_pagadoFloat = float(montoPagado)
                    totalGastadoEnServicios = totalGastadoEnServicios + monto_pagadoFloat
                    consultaEmpleadoAgregadoPor = Empleados.objects.filter(id_empleado = idEmpleadoAgregadoPor)
                    for datoEmpleado in consultaEmpleadoAgregadoPor:
                        nombreEmpleado = datoEmpleado.nombre
                        apellidoEmpleado = datoEmpleado.apellidos

                    nombreCompletoEmpleadoQueAgrego = nombreEmpleado + " " + apellidoEmpleado

                    





                    listaServiciosTabla.append([idServicio,codigoVehiculo,marcaVehiculo, modeloVehiculo, añoVehiculo, fechaServicio,
                    tipoServicio, arregloServicios, kmPreServicio, tallerServicio, montoPagado, nombreCompletoEmpleadoQueAgrego])






                return render(request,"empleadosCustom/ControlVehicular/Servicio/verServicio.html",{"estaEnVerServicio":estaEnVerServicio,"id_admin":id_admin,"nombre":nombre,"apellidos":apellidos,"correo":correo,"nombreCompleto":nombreCompleto,"solicitantePrestamo":solicitantePrestamo, "administradordeVehiculos":administradordeVehiculos,"foto":foto,"almacen":almacen, "listaServiciosTabla":listaServiciosTabla, "totalGastadoEnServicios":totalGastadoEnServicios})
            
            solicitantePrestamo = True
            return render(request,"empleadosCustom/ControlVehicular/Servicio/verServicio.html",{"estaEnAgregarAltaServicio":estaEnVerServicio,"id_admin":id_admin,"nombre":nombre,"apellidos":apellidos,"correo":correo,"nombreCompleto":nombreCompleto,"solicitantePrestamo":solicitantePrestamo,"almacen":almacen})
            
    
    

    
        return render(request,"empleadosCustom/ControlVehicular/Servicio/verServicio.html",{"estaEnAgregarAltaServicio":estaEnVerServicio,"id_admin":id_admin,"nombre":nombre,"apellidos":apellidos,"correo":correo,"nombreCompleto":nombreCompleto,"almacen":almacen})
    else:
        return redirect('/login/')


#REPARACIÓN
def agregarAltaReparacion(request):
    if "idSesion" in request.session:
        estaEnAgregarAltaReparacion = True
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        if correo == "almacen01@customco.com.mx":
            almacen = True
        else:
            almacen = False
        nombreCompleto = nombre + " " + apellidos
        
        foto = fotoAdmin(request)

        if request.method == "POST":
            
            vehiculoReparado = request.POST["selectVehi"]
            fechaReparacion = request.POST["fechaReparacion"]
            motivoReparacion = request.POST["motivoReparacion"]
            descripcionFalla = request.POST["descripcion"]
            tallerReparacion = request.POST["tallerReparacion"]
            montoPagado = request.POST["montoPagado"]
            facturaReparacion = request.FILES.get('facturaReparacion')

            fechaSeparada = fechaReparacion.split("/") #29   06    2018
            fechaNormal = fechaSeparada[2] + "-" + fechaSeparada[0] + "-" + fechaSeparada[1]

            floatmontoPagado = float(montoPagado)
            #Registro de reparación de falla.

            registroReparacion = reparacionVehiculo(
                id_vehiculo = Vehiculos.objects.get(id_vehiculo = vehiculoReparado),
                agregado_por = Empleados.objects.get(id_empleado = id_admin),
                fecha_reparacion = fechaNormal,
                motivo_reparacion = motivoReparacion,
                descripcion_reparacion = descripcionFalla,
                taller_reparacion = tallerReparacion,
                costo_reparacion = floatmontoPagado,
                factura_reparacion = facturaReparacion
            )
            registroReparacion.save()

            if registroReparacion:
                request.session["reparacionAgregada"] = "La reparación fue agregada satisfactoriamente al sistema!!"

                #Mandar notificación de telegram
                try:
                    tokenTelegram = keysBotCustom.tokenBotVehiculos
                    botCustom = telepot.Bot(tokenTelegram)

                    idGrupoTelegram = keysBotCustom.idGrupoVehiculos


                    consultaVehiculo = Vehiculos.objects.filter(id_vehiculo = vehiculoReparado)
                    for datoVehiculo in consultaVehiculo:
                        codigoVehiculo = datoVehiculo.codigo_vehiculo
                        marcaVehiculo = datoVehiculo.marca_vehiculo
                        modeloVehiculo = datoVehiculo.modelo_vehiculo
                        añoVehiculo = datoVehiculo.año_vehiculo
                        idEmpleadoResponsable = datoVehiculo.responsable_actual_id
                        imagenVehiculo = datoVehiculo.imagen_frontal_vehiculo
                    
                    consultaEmpleado = Empleados.objects.filter(id_empleado = idEmpleadoResponsable)
                    for datoEmpleado in consultaEmpleado:
                        nombre = datoEmpleado.nombre
                        apellidos = datoEmpleado.apellidos

                    nombreResponsableActual = nombre + " "+ apellidos
                    
                    
                    mensaje = "\U0001F6A8 REPARACIÓN VEHICULAR \U0001F6A8 \n Hola \U0001F44B! \n Se ha agregado una nueva reparación al siguiente vehiculo: "+"\n\n  Codigo Vehículo: "+codigoVehiculo+"\n  Marca: "+marcaVehiculo+"\n  Modelo: "+modeloVehiculo+"\n  Responsable actual: "+nombreResponsableActual+"\n\n Motivo Reparación: "+motivoReparacion+"\n Descripción: "+descripcionFalla+"\n Taller de reparación: "+tallerReparacion+"\n Costo reparación: $"+str(floatmontoPagado)+"MXN."
                    botCustom.sendMessage(idGrupoTelegram,mensaje)
                except:
                    print("An exception occurred")

                #Mandar correo electrónico.
                asunto = "CS | Nueva reparación vehicular."
                plantilla = "empleadosCustom/ControlVehicular/Reparacion/correoReparacion.html"
                

                
            
                            
                #Datos del empleado
                html_mensaje = render_to_string(plantilla, {"codigoVehiculo":codigoVehiculo,"imagenVehiculo":imagenVehiculo,"marcaVehiculo":marcaVehiculo,"modeloVehiculo":modeloVehiculo,"añoVehiculo":añoVehiculo,"nombreResponsableActual":nombreResponsableActual,"motivoReparacion":motivoReparacion,"tallerReparacion":tallerReparacion,"costoReparacion":floatmontoPagado,"fechaReparacion":fechaNormal,"descripcionReparacion":descripcionFalla})
                email_remitente = settings.EMAIL_HOST_USER
                email_destino = ['sistemas@customco.com.mx']
                
                mensaje = EmailMessage(asunto, html_mensaje, email_remitente, email_destino)
                mensaje.content_subtype = 'html'
                mensaje.send()
                
                #Fin de mandar correo
                return redirect("/agregarAltaReparacion/")







        else:
            empleado = Empleados.objects.filter(id_empleado = id_admin)
            for dato in empleado:
                area = dato.id_area_id

            if area == 1 or area ==5 or area == 7 or area == 8 or area == 9 or area == 10:
                if area == 5:
                    solicitantePrestamo = True
                    administradordeVehiculos = True

                    listaVehiculos = Vehiculos.objects.filter(status_vehiculo = "En uso")

                    if "reparacionAgregada" in request.session:
                        reparacionAgregada = request.session["reparacionAgregada"]
                        del request.session["reparacionAgregada"]
                        return render(request,"empleadosCustom/ControlVehicular/Reparacion/AltaReparacion.html",{"estaEnAgregarAltaReparacion":estaEnAgregarAltaReparacion,"id_admin":id_admin,"nombre":nombre,"apellidos":apellidos,"correo":correo,"nombreCompleto":nombreCompleto,"solicitantePrestamo":solicitantePrestamo, "administradordeVehiculos":administradordeVehiculos,"foto":foto,"almacen":almacen, "listaVehiculos":listaVehiculos,
                        "reparacionAgregada":reparacionAgregada})
                        

                    return render(request,"empleadosCustom/ControlVehicular/Reparacion/AltaReparacion.html",{"estaEnAgregarAltaReparacion":estaEnAgregarAltaReparacion,"id_admin":id_admin,"nombre":nombre,"apellidos":apellidos,"correo":correo,"nombreCompleto":nombreCompleto,"solicitantePrestamo":solicitantePrestamo, "administradordeVehiculos":administradordeVehiculos,"foto":foto,"almacen":almacen, "listaVehiculos":listaVehiculos})
                
                solicitantePrestamo = True
                return render(request,"empleadosCustom/ControlVehicular/Reparacion/AltaReparacion.html",{"estaEnAgregarAltaReparacion":estaEnAgregarAltaReparacion,"id_admin":id_admin,"nombre":nombre,"apellidos":apellidos,"correo":correo,"nombreCompleto":nombreCompleto,"solicitantePrestamo":solicitantePrestamo,"almacen":almacen})
                1
        
        

        
            return render(request,"empleadosCustom/ControlVehicular/Reparacion/AltaReparacion.html",{"estaEnAgregarAltaReparacion":estaEnAgregarAltaReparacion,"id_admin":id_admin,"nombre":nombre,"apellidos":apellidos,"correo":correo,"nombreCompleto":nombreCompleto,"almacen":almacen})
    else:
        return redirect('/login/')

def verReparacion(request):
    if "idSesion" in request.session:
        estaEnVerReparacion = True
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        if correo == "almacen01@customco.com.mx":
            almacen = True
        else:
            almacen = False
        nombreCompleto = nombre + " " + apellidos
        
        foto = fotoAdmin(request)
        
        empleado = Empleados.objects.filter(id_empleado = id_admin)
        for dato in empleado:
            area = dato.id_area_id

        if area == 1 or area ==5 or area == 7 or area == 8 or area == 9 or area == 10:
            if area == 5:
                solicitantePrestamo = True
                administradordeVehiculos = True


                datosTabla = []
                #Consulta de reparaciones

                montoTotalCostoReparaciones = 0
                reparaciones = reparacionVehiculo.objects.all()
                for reparacion in reparaciones:
                    idReparacion = reparacion.id_reparacion
                    idVehiculo = reparacion.id_vehiculo_id

                    consultaVehiculo = Vehiculos.objects.filter(id_vehiculo = idVehiculo)
                    for datoVehiculo in consultaVehiculo:
                        codigoVehiculo = datoVehiculo.codigo_vehiculo
                        marcaVehiculo = datoVehiculo.marca_vehiculo
                        modeloVehiculo = datoVehiculo.modelo_vehiculo
                        añoVehiculo = datoVehiculo.año_vehiculo


                    fechaReparacion = reparacion.fecha_reparacion
                    motivoReparacion = reparacion.motivo_reparacion
                    descripcionReparacion = reparacion.descripcion_reparacion
                    tallerReparacion = reparacion.taller_reparacion
                    montoPagado = reparacion.costo_reparacion
                    factura = reparacion.factura_reparacion

                    montoTotalCostoReparaciones = montoTotalCostoReparaciones + montoPagado







                    datosTabla.append([idReparacion,codigoVehiculo, marcaVehiculo,modeloVehiculo,
                    añoVehiculo, fechaReparacion, motivoReparacion, descripcionReparacion,
                    tallerReparacion, montoPagado, factura])




                return render(request,"empleadosCustom/ControlVehicular/Reparacion/verReparacion.html",{"estaEnVerReparacion":estaEnVerReparacion,"id_admin":id_admin,"nombre":nombre,"apellidos":apellidos,"correo":correo,"nombreCompleto":nombreCompleto,"solicitantePrestamo":solicitantePrestamo, "administradordeVehiculos":administradordeVehiculos,"foto":foto,"almacen":almacen, "datosTabla":datosTabla, "montoTotalCostoReparaciones":montoTotalCostoReparaciones})
            
            solicitantePrestamo = True
            return render(request,"empleadosCustom/ControlVehicular/Reparacion/verReparacion.html",{"estaEnVerReparacion":estaEnVerReparacion,"id_admin":id_admin,"nombre":nombre,"apellidos":apellidos,"correo":correo,"nombreCompleto":nombreCompleto,"solicitantePrestamo":solicitantePrestamo,"almacen":almacen})
            
    
    

    
        return render(request,"empleadosCustom/ControlVehicular/Reparacion/verReparacion.html",{"estaEnVerReparacion":estaEnVerReparacion,"id_admin":id_admin,"nombre":nombre,"apellidos":apellidos,"correo":correo,"nombreCompleto":nombreCompleto,"almacen":almacen})
    else:
        return redirect('/login/')


#Descargar factura de alineacion y balanceo
def descargarFacturaAlineacion(request):
    if "idSesion" in request.session:
        
        if request.method == "POST":
            
            rutaArchivo = request.POST['rutaArchivo']
            idAlineacion = request.POST['idAlineacion']

            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            
            ubicacionArchivo = BASE_DIR + '/media/'+ rutaArchivo

            path = open(ubicacionArchivo, 'rb')

            mime_type, _= mimetypes.guess_type(ubicacionArchivo)
            response = HttpResponse(path, content_type=mime_type)

            consultaAlineacion = alineacionyBalanceo.objects.filter(id_alineacion_balanceo = idAlineacion)
            for datoAlineacion in consultaAlineacion:
                idVehiculo = datoAlineacion.id_vehiculo_id
            
            consultaVehiculo = Vehiculos.objects.filter(id_vehiculo = idVehiculo)
            for datoVehiculo in consultaVehiculo:
                marcaVehiculo = datoVehiculo.marca_vehiculo
                modeloVehiculo = datoVehiculo.modelo_vehiculo
                añoVehiculo = datoVehiculo.año_vehiculo
            
            nombreArchivo = "Factura alineacion #"+str(idAlineacion)+" - "+marcaVehiculo+" "+modeloVehiculo+" "+añoVehiculo
            response['Content-Disposition'] = "attachment; filename=%s" %nombreArchivo
            return response

        #return render(request, "Equipos/equipo.html", {"idEquipo":BASE_DIR})
    else:
        return redirect('/login/') #redirecciona a url de inicio

def descargarFacturaReparacion(request):
    if "idSesion" in request.session:
        
        if request.method == "POST":
            
            rutaArchivo = request.POST['rutaArchivo']
            idReparacion = request.POST['idReparacion']

            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            
            ubicacionArchivo = BASE_DIR + '/media/'+ rutaArchivo

            path = open(ubicacionArchivo, 'rb')

            mime_type, _= mimetypes.guess_type(ubicacionArchivo)
            response = HttpResponse(path, content_type=mime_type)

            consultaReparacion = reparacionVehiculo.objects.filter(id_reparacion = idReparacion)
            for datoReparacion in consultaReparacion:
                idVehiculo = datoReparacion.id_vehiculo_id
            
            consultaVehiculo = Vehiculos.objects.filter(id_vehiculo = idVehiculo)
            for datoVehiculo in consultaVehiculo:
                marcaVehiculo = datoVehiculo.marca_vehiculo
                modeloVehiculo = datoVehiculo.modelo_vehiculo
                añoVehiculo = datoVehiculo.año_vehiculo
            
            nombreArchivo = "Factura reparacion #"+str(idReparacion)+" - "+marcaVehiculo+" "+modeloVehiculo+" "+añoVehiculo
            response['Content-Disposition'] = "attachment; filename=%s" %nombreArchivo
            return response

        #return render(request, "Equipos/equipo.html", {"idEquipo":BASE_DIR})
    else:
        return redirect('/login/') #redirecciona a url de inicio



def verInformacionVehiculo(request):
    if "idSesion" in request.session:
        estaEnVerVehiculos = True
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        if correo == "almacen01@customco.com.mx":
            almacen = True
        else:
            almacen = False
        nombreCompleto = nombre + " " + apellidos
        
        foto = fotoAdmin(request)
        empleado = Empleados.objects.filter(id_empleado = id_admin)
        for dato in empleado:
            area = dato.id_area_id


        solicitantePrestamo = True
        administradordeVehiculos = True

        if request.method == "POST":
            
            idVehiculo = request.POST["idVehiculo"]

            consultaVehiculo = Vehiculos.objects.filter(id_vehiculo = idVehiculo)
            for datoVehiculo in consultaVehiculo:
                codigoVehiculo = datoVehiculo.codigo_vehiculo
                marcaVehiculo = datoVehiculo.marca_vehiculo
                modeloVehiculo = datoVehiculo.modelo_vehiculo
                numeroSerieVehiculo = datoVehiculo.numero_serie_vehiculo
                colorVehiculo = datoVehiculo.color_vehiculo
                añoVehiculo = datoVehiculo.año_vehiculo
                placaVehiculo = datoVehiculo.placa_vehiculo
                transmisionVehiculo = datoVehiculo.transmision_vehiculo
                ultimoKilometraje = datoVehiculo.ultimo_km_registrado
                estatusVehiculo = datoVehiculo.status_vehiculo
                motivoEstatus = datoVehiculo.motivo_status_vehiculo
                fechaAltaVehiculo = datoVehiculo.fecha_alta_vehiculo

                imagenFrontalVehiculo = datoVehiculo.imagen_frontal_vehiculo
                imagenTraseraVehiculo = datoVehiculo.imagen_trasera_vehiculo
                imagenLateralIzquierdaVehiculo = datoVehiculo.imagen_lateralIzquierda_vehiculo
                imagenLateralDerechaVehiculo = datoVehiculo.imagen_lateralDerecha_vehiculo


                idEmpleadoResponsable = datoVehiculo.responsable_actual_id

            #Datos de empleado
            consultaEmpleado = Empleados.objects.filter(id_empleado = idEmpleadoResponsable)
            for datoEmpleado in consultaEmpleado:
                nombreEmpleado = datoEmpleado.nombre
                apellidoEmpleado = datoEmpleado.apellidos
                correoEmpleado = datoEmpleado.correo
                departamento = datoEmpleado.id_area_id

            consultaDepartamento = Areas.objects.filter(id_area = departamento)
            for datoDepartamento in consultaDepartamento:
                nombreDepartamentoEmpleadoResponsable = datoDepartamento.nombre

            #DOCUMENTACION VEHICULO
            consultaDocumentacion = documentacionVehiculos.objects.filter(vehiculo = idVehiculo)
            if consultaDocumentacion:
                    
                for datoDocumentacion in consultaDocumentacion:
                    facturaVehiculo = datoDocumentacion.factura_vehiculo
                    tarjetaCirculacion = datoDocumentacion.tarjeta_circulacion
                    pagoSeguro = datoDocumentacion.pago_seguro
                    contratoArrendamiento = datoDocumentacion.contrato_arrendamiento
            else:
                facturaVehiculo = None
                tarjetaCirculacion = None
                pagoSeguro = None
                contratoArrendamiento = None

            arregloDatosVehiculo = []
            arregloDatosVehiculo.append([codigoVehiculo, marcaVehiculo, modeloVehiculo,
            numeroSerieVehiculo, colorVehiculo, añoVehiculo, placaVehiculo, transmisionVehiculo,
            ultimoKilometraje, estatusVehiculo, motivoEstatus, fechaAltaVehiculo,
            imagenFrontalVehiculo, imagenTraseraVehiculo, imagenLateralIzquierdaVehiculo,
            imagenLateralDerechaVehiculo])

            arregloDatosEncargado = []
            arregloDatosEncargado.append([nombreEmpleado, apellidoEmpleado, correoEmpleado, nombreDepartamentoEmpleadoResponsable])

            arregloDocumentacionVehiculo = []
            arregloDocumentacionVehiculo.append([codigoVehiculo,facturaVehiculo, tarjetaCirculacion, pagoSeguro, contratoArrendamiento])




            #TENENCIAS DEL VEHICULO
            montototalTenencias = 0
            consultaTenencias = tenenciasVehiculos.objects.filter(vehiculo = idVehiculo)
            tenenciasVehiculo = []
            for tenencia in consultaTenencias:
                idTenencia = tenencia.id_tenencia
                tenenciaAgregadaPor = tenencia.agregado_por_id
                consultaAgregadorTenencia = Empleados.objects.filter(id_empleado = tenenciaAgregadaPor)
                for dato in consultaAgregadorTenencia:
                    nombreAgregadorTenencia = dato.nombre
                    apellidoAgregadorTenencia = dato.apellidos
                nombreCompletoAgregadorTenencia = nombreAgregadorTenencia + " " + apellidoAgregadorTenencia
                reciboTenencia = tenencia.recibio_tenencia_vehiculo
                añoPagado = tenencia.ano_pagado
                fechaTenencia = tenencia.fecha_tenencia
                placasNuevas = tenencia.placas_nuevas
                referenciaPagoTenencia = tenencia.referencia_pago_tenencia
                montoPagado = tenencia.monto_pagado_vehiculo
                montototalTenencias = montototalTenencias + float(montoPagado)
            
                #Agregar cada tenencia en arreglo de tenencias.
                tenenciasVehiculo.append([idTenencia, nombreCompletoAgregadorTenencia,reciboTenencia,
                añoPagado, fechaTenencia, placasNuevas, referenciaPagoTenencia, montoPagado])

            
            #SERVICIOS DEL VEHICULO
            montoTotalServicios = 0
            consultaServicios = serviciosVehiculos.objects.filter(vehiculo = idVehiculo)
            serviciosVehiculo = []
            for servicio in consultaServicios:
                idServicio = servicio.id_servicio
                fechaServicio = servicio.fecha_servicios_vehiculo

                servicioAgregadoPor = servicio.agregado_por_id
                consultaAgregadorServicio = Empleados.objects.filter(id_empleado = servicioAgregadoPor)
                for dato in consultaAgregadorServicio:
                    nombreAgregadorServicio = dato.nombre
                    apellidoAgregadorServicio = dato.apellidos
                nombreCompletoAgregadorServicio = nombreAgregadorServicio + " " + apellidoAgregadorServicio


                tipoServicio = servicio.tipo_servicio
                serviciosRealizados = servicio.servicios_realizados
                arrayServiciosRealizados = serviciosRealizados.split(",")
                kilometrajePreServicio = servicio.kilometraje_preservicio
                tallerServicio = servicio.taller_servicio
                montoPagado = servicio.monto_pagado
                facturaServicio = servicio.factura_servicios

                montoTotalServicios = montoTotalServicios + float(montoPagado)

                #Agregar cada servicio en arreglo de servicios
                serviciosVehiculo.append([idServicio, fechaServicio, nombreCompletoAgregadorServicio,
                tipoServicio, arrayServiciosRealizados, kilometrajePreServicio, tallerServicio, montoPagado, facturaServicio])

            #ALINEACIONES Y BALANCEOS DEL VEHICULO.
            consultaAlineacionBalanceo = alineacionyBalanceo.objects.filter(id_vehiculo = idVehiculo)
            alineacionesVehiculo = []
            montoTotalAlineacion = 0
            for alineacion in consultaAlineacionBalanceo:
                idAlineacionBalanceo = alineacion.id_alineacion_balanceo
                
                alineacionAgregadoPor = alineacion.agregado_por_id
                consultaAgregadorAlineacion = Empleados.objects.filter(id_empleado = alineacionAgregadoPor)
                for dato in consultaAgregadorAlineacion:
                    nombreAgregadorAlineacion = dato.nombre
                    apellidoAgregadorAlineacion = dato.apellidos
                nombreCompletoAgregadorAlineacion = nombreAgregadorAlineacion + " " + apellidoAgregadorAlineacion

                alineacionRealizada = alineacion.alineacion_realizada
                balanceoRealizado = alineacion.balanceo_realizado
                cambioLlantas = alineacion.cambio_llantas

                if cambioLlantas == "Si":
                    numeroLlantasCambiadas = alineacion.numero_cambio_llantas
                    medidaLlantaNueva = alineacion.medida_llanta_nueva
                    marcaLlanta = alineacion.marca_llanta_nueva
                
                else:
                    numeroLlantasCambiadas = "nada"
                    medidaLlantaNueva = "nada"
                    marcaLlanta = "nada"
                
                observaciones = alineacion.observaciones
                kilometrajePreAlineacion = alineacion.kilometraje_prealineacion
                fechaAlineacion = alineacion.fecha_alineacion
                factuaAlineacion = alineacion.factura_alineacion
                montoPagado = alineacion.monto_pagado

                montoTotalAlineacion = montoTotalAlineacion + float(montoPagado)

                alineacionesVehiculo.append([idAlineacionBalanceo, nombreCompletoAgregadorAlineacion,
                alineacionRealizada, balanceoRealizado, cambioLlantas, numeroLlantasCambiadas,
                medidaLlantaNueva, marcaLlanta, observaciones, kilometrajePreAlineacion,
                fechaAlineacion, factuaAlineacion, montoPagado])
                
            #REPARACIONES DEL VEHICULO.
            montoTotalReparaciones = 0
            consultaReparacionesVehiculo = reparacionVehiculo.objects.filter(id_vehiculo = idVehiculo)
            reparacionesDelVehiculo = []
            for reparacion in consultaReparacionesVehiculo:
                idReparacion = reparacion.id_reparacion

                reparacionAgregadoPor = reparacion.agregado_por_id
                consultaAgregadorReparacion= Empleados.objects.filter(id_empleado = reparacionAgregadoPor)
                for dato in consultaAgregadorReparacion:
                    nombreAgregadorReparacion = dato.nombre
                    apellidoAgregadorReparacion = dato.apellidos
                nombreCompletoAgregadorReparacion = nombreAgregadorReparacion + " " + apellidoAgregadorReparacion

                fechaReparacion = reparacion.fecha_reparacion
                motivoReparacion = reparacion.motivo_reparacion
                descripcionReparacion = reparacion.descripcion_reparacion
                tallerReparacion = reparacion.taller_reparacion
                costoReparacion = reparacion.costo_reparacion
                facturaReparacion = reparacion.factura_reparacion

                montoTotalReparaciones = montoTotalReparaciones + float(costoReparacion)

                reparacionesDelVehiculo.append([idReparacion, fechaReparacion,
                nombreCompletoAgregadorReparacion, motivoReparacion, descripcionReparacion,
                tallerReparacion, costoReparacion, facturaReparacion])

            return render(request,"empleadosCustom/ControlVehicular/Gestion/verInfoVehiculo.html",{"estaEnVerVehiculos":estaEnVerVehiculos,"id_admin":id_admin,"nombre":nombre,"apellidos":apellidos,"correo":correo,"nombreCompleto":nombreCompleto,"solicitantePrestamo":solicitantePrestamo, "administradordeVehiculos":administradordeVehiculos,"foto":foto, "almacen":almacen,
            "arregloDatosVehiculo":arregloDatosVehiculo,"arregloDatosEncargado":arregloDatosEncargado, "arregloDocumentacionVehiculo":arregloDocumentacionVehiculo,
            "tenenciasVehiculo":tenenciasVehiculo, "serviciosVehiculo":serviciosVehiculo,"alineacionesVehiculo":alineacionesVehiculo,"reparacionesDelVehiculo":reparacionesDelVehiculo, "montototalTenencias":montototalTenencias, "montoTotalServicios":montoTotalServicios,
            "montoTotalReparaciones":montoTotalReparaciones, "ultimoKilometraje":ultimoKilometraje, "idVehiculo":idVehiculo, "montoTotalAlineacion":montoTotalAlineacion, "estatusVehiculo":estatusVehiculo})

    else:
        return redirect('/login/') #redirecciona a url de inicio








#Views para descargar documentos vehiculares
def descargarFacturaVehiculo(request):
    if "idSesion" in request.session:
        
        if request.method == "POST":
            
            codigoVehiculo = request.POST['codigoVehiculo']

            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            
            #Consulta para sacar el id del vehiculo
            consultaVehiculo = Vehiculos.objects.filter(codigo_vehiculo = codigoVehiculo)
            for datoVehiculo in consultaVehiculo:

                idVehiculo = datoVehiculo.id_vehiculo
            
            consultaDocumentacion = documentacionVehiculos.objects.filter(vehiculo_id__id_vehiculo = idVehiculo )
            for datoDocumentacion in consultaDocumentacion:

                facturaVehiculo = datoDocumentacion.factura_vehiculo

            
           
            ubicacionArchivo = BASE_DIR + '/media/'+ str(facturaVehiculo)

            path = open(ubicacionArchivo, 'rb')


            mime_type= mimetypes.guess_type(ubicacionArchivo)
            print(str(mime_type))
            response = HttpResponse(path, content_type='application/pdf')
            response['Content-Disposition'] = "attachment; filename=%s" %"Factura Vehiculo "+codigoVehiculo+".pdf"
            return response

       
    else:
        return redirect('/login/') #redirecciona a url de inicio

def descargarTarjetaCirculacionVehiculo(request):
    if "idSesion" in request.session:
        
        if request.method == "POST":
            
            codigoVehiculo = request.POST['codigoVehiculo']

            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            
            #Consulta para sacar el id del vehiculo
            consultaVehiculo = Vehiculos.objects.filter(codigo_vehiculo = codigoVehiculo)
            for datoVehiculo in consultaVehiculo:

                idVehiculo = datoVehiculo.id_vehiculo
            
            consultaDocumentacion = documentacionVehiculos.objects.filter(vehiculo_id__id_vehiculo = idVehiculo )
            for datoDocumentacion in consultaDocumentacion:

                tarjetacirculacion = datoDocumentacion.tarjeta_circulacion

            
           
            ubicacionArchivo = BASE_DIR + '/media/'+ str(tarjetacirculacion)


            path = open(ubicacionArchivo, 'rb')

            mime_type, _= mimetypes.guess_type(ubicacionArchivo)
            response = HttpResponse(path, content_type=mime_type)
            response['Content-Disposition'] = "attachment; filename=%s" %"Tarjeta Ciculación Vehiculo "+codigoVehiculo+".pdf"
            return response
    else:
        return redirect('/login/') #redirecciona a url de inicio


def descargarPolizaVehiculo(request):
    if "idSesion" in request.session:
        
        if request.method == "POST":
            
            codigoVehiculo = request.POST['codigoVehiculo']

            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            
            #Consulta para sacar el id del vehiculo
            consultaVehiculo = Vehiculos.objects.filter(codigo_vehiculo = codigoVehiculo)
            for datoVehiculo in consultaVehiculo:

                idVehiculo = datoVehiculo.id_vehiculo
            
            consultaDocumentacion = documentacionVehiculos.objects.filter(vehiculo_id__id_vehiculo = idVehiculo )
            for datoDocumentacion in consultaDocumentacion:

                polizaSeguro = datoDocumentacion.pago_seguro

           
            ubicacionArchivo = BASE_DIR + '/media/'+ str(polizaSeguro)


            path = open(ubicacionArchivo, 'rb')

            mime_type, _= mimetypes.guess_type(ubicacionArchivo)
            response = HttpResponse(path, content_type=mime_type)
            response['Content-Disposition'] = "attachment; filename=%s" %"Póliza de Seguro Vehiculo "+codigoVehiculo+".pdf"
            return response
    else:
        return redirect('/login/') #redirecciona a url de inicio

def descargarContratoArrendamientoVehiculo(request):
    if "idSesion" in request.session:
        
        if request.method == "POST":
            
            codigoVehiculo = request.POST['codigoVehiculo']

            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            
            #Consulta para sacar el id del vehiculo
            consultaVehiculo = Vehiculos.objects.filter(codigo_vehiculo = codigoVehiculo)
            for datoVehiculo in consultaVehiculo:

                idVehiculo = datoVehiculo.id_vehiculo
            
            consultaDocumentacion = documentacionVehiculos.objects.filter(vehiculo_id__id_vehiculo = idVehiculo )
            for datoDocumentacion in consultaDocumentacion:

                contratoArrendamiento = datoDocumentacion.contrato_arrendamiento

           
            ubicacionArchivo = BASE_DIR + '/media/'+ str(contratoArrendamiento)


            path = open(ubicacionArchivo, 'rb')

            mime_type, _= mimetypes.guess_type(ubicacionArchivo)
            response = HttpResponse(path, content_type=mime_type)
            response['Content-Disposition'] = "attachment; filename=%s" %"ContratoArrendamiento Vehiculo "+codigoVehiculo+".pdf"
            return response
    else:
        return redirect('/login/') #redirecciona a url de inicio

def descargarComprobanteTenencia(request):
    if "idSesion" in request.session:
        
        if request.method == "POST":
            
            idTenencia = request.POST['idTenencia']

            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            
            #Consulta para sacar la factura de tenencia
            consultaTenencia = tenenciasVehiculos.objects.filter(id_tenencia = idTenencia)
            for datoTenencia in consultaTenencia:

                factura = datoTenencia.recibio_tenencia_vehiculo
                idVehiculo = datoTenencia.vehiculo_id

            consultaVehiculo = Vehiculos.objects.filter(id_vehiculo = idVehiculo)
            for datoVehiculo in consultaVehiculo:
                codigoVehiculo = datoVehiculo.codigo_vehiculo
            
           
            ubicacionArchivo = BASE_DIR + '/media/'+ str(factura)


            path = open(ubicacionArchivo, 'rb')

            mime_type, _= mimetypes.guess_type(ubicacionArchivo)
            response = HttpResponse(path, content_type=mime_type)
            response['Content-Disposition'] = "attachment; filename=%s" %"Factura Tenencia # "+str(idTenencia)+" - Vehículo "+str(codigoVehiculo)+".pdf"
            return response
    else:
        return redirect('/login/') #redirecciona a url de inicio

def descargarFacturaBalanceo(request):
    if "idSesion" in request.session:
        
        if request.method == "POST":
            
            idBalanceo = request.POST['idBalanceo']

            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            
            #Consulta para sacar la factura de tenencia
            consultaBalanceo = alineacionyBalanceo.objects.filter(id_alineacion_balanceo = idBalanceo)
            for datoBalanceo in consultaBalanceo:

                factura = datoBalanceo.factura_alineacion
                idVehiculo = datoBalanceo.id_vehiculo_id

            consultaVehiculo = Vehiculos.objects.filter(id_vehiculo = idVehiculo)
            for datoVehiculo in consultaVehiculo:
                codigoVehiculo = datoVehiculo.codigo_vehiculo
            
           
            ubicacionArchivo = BASE_DIR + '/media/'+ str(factura)


            path = open(ubicacionArchivo, 'rb')

            mime_type, _= mimetypes.guess_type(ubicacionArchivo)
            response = HttpResponse(path, content_type=mime_type)
            response['Content-Disposition'] = "attachment; filename=%s" %"Factura Alineación # "+str(idBalanceo)+" - Vehículo "+str(codigoVehiculo)+".pdf"
            return response
    else:
        return redirect('/login/')

def descargarFacturaReparacion(request):
    if "idSesion" in request.session:
        
        if request.method == "POST":
            
            idReparacion = request.POST['idReparacion']

            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            
            #Consulta para sacar la factura de tenencia
            consultaReparacion = reparacionVehiculo.objects.filter(id_reparacion = idReparacion)
            for datoReparacion in consultaReparacion:

                factura = datoReparacion.factura_reparacion
                idVehiculo = datoReparacion.id_vehiculo_id

            consultaVehiculo = Vehiculos.objects.filter(id_vehiculo = idVehiculo)
            for datoVehiculo in consultaVehiculo:
                codigoVehiculo = datoVehiculo.codigo_vehiculo
            
           
            ubicacionArchivo = BASE_DIR + '/media/'+ str(factura)


            path = open(ubicacionArchivo, 'rb')

            mime_type, _= mimetypes.guess_type(ubicacionArchivo)
            response = HttpResponse(path, content_type=mime_type)
            response['Content-Disposition'] = "attachment; filename=%s" %"Factura Reparación # "+str(idReparacion)+" - Vehículo "+str(codigoVehiculo)+".pdf"
            return response
    else:
        return redirect('/login/')

def descargarFacturaServicio(request):
    if "idSesion" in request.session:
        
        if request.method == "POST":
            
            idServicio = request.POST['idServicio']

            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            
            #Consulta para sacar la factura de servicio
            consultaServicio = serviciosVehiculos.objects.filter(id_servicio = idServicio)
            for datoServicio in consultaServicio:

                factura = datoServicio.factura_servicios
                idVehiculo = datoServicio.vehiculo_id

            consultaVehiculo = Vehiculos.objects.filter(id_vehiculo = idVehiculo)
            for datoVehiculo in consultaVehiculo:
                codigoVehiculo = datoVehiculo.codigo_vehiculo
            
           
            ubicacionArchivo = BASE_DIR + '/media/'+ str(factura)


            path = open(ubicacionArchivo, 'rb')

            mime_type, _= mimetypes.guess_type(ubicacionArchivo)
            response = HttpResponse(path, content_type=mime_type)
            response['Content-Disposition'] = "attachment; filename=%s" %"Factura Servicio # "+str(idServicio)+" - Vehículo "+str(codigoVehiculo)+".pdf"
            return response
    else:
        return redirect('/login/')


def actualizarKilometraje(request):
    if "idSesion" in request.session:
        
        if request.method == "POST":
            
            nuevoKm = request.POST['nuevoKm']
            idVehiculo = request.POST['idVehiculo']

            #actualizacion kilometro
            actualizacion = Vehiculos.objects.filter(id_vehiculo = idVehiculo).update(ultimo_km_registrado = nuevoKm)

            consultaVehiculo = Vehiculos.objects.filter(id_vehiculo = idVehiculo)
            for datoVehiculo in consultaVehiculo:
                codigoVehiculo = datoVehiculo.codigo_vehiculo

            request.session["kmActualizado"] = "El kilometraje del vehículo "+codigoVehiculo+" ha sido actualizado satisfactoriamente!"

            return redirect("/verVehiculos/")


            
            return response
    else:
        return redirect('/login/')


def verCalendarioServicios(request):
    if "idSesion" in request.session:
        estaEnVerCalendarioServicios = True
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        if correo == "almacen01@customco.com.mx":
            almacen = True
        else:
            almacen = False
        nombreCompleto = nombre + " " + apellidos
        
        foto = fotoAdmin(request)
        
        empleado = Empleados.objects.filter(id_empleado = id_admin)
        for dato in empleado:
            area = dato.id_area_id

        if area == 1 or area ==5 or area == 7 or area == 8 or area == 9 or area == 10:
            if area == 5:
                solicitantePrestamo = True
                administradordeVehiculos = True


                #Vehiculos Activos
                consultaVehiculos = Vehiculos.objects.filter(status_vehiculo = "En uso")
                arregloVehiculosFechas = []
                arregloVehiculosFechasProximas = []
                mensajeVehiculoFechas = []
                mensajeVehiculoFechasProximas = []

                fechaDeHoy = date.today()
                contadorVehiculos = 0
                for vehiculo in consultaVehiculos:
                    idVehiculo = vehiculo.id_vehiculo
                    codigoVehiculo = vehiculo.codigo_vehiculo
                    marcaVehiculo = vehiculo.marca_vehiculo
                    modeloVehiculo = vehiculo.modelo_vehiculo
                    añoVehiculo = vehiculo.año_vehiculo
                    fotografiaFrontal = vehiculo.imagen_frontal_vehiculo


                    encargadoActual = vehiculo.responsable_actual_id

                    #Consulta datos reponsable actual
                    consultaDatosReponsable = Empleados.objects.filter(id_empleado = encargadoActual)
                    for dato in consultaDatosReponsable:
                        nombreEmpleado = dato.nombre
                        apellidosEmpleado = dato.apellidos

                    nombreCompletoEncargadoActual = nombreEmpleado + " " + apellidosEmpleado

                    consultaServicios = serviciosVehiculos.objects.filter(vehiculo__id_vehiculo = idVehiculo)
                    if consultaServicios: #Solo los vehiculos que tengan servicios..
                        contadorVehiculos = contadorVehiculos + 1
                        arregloDeFechasDeServicios = []
                        kilometrajes = []
                        tiposServicios = []

                        diferenciaDeDiasDeFechas = []
                        idsServicios = []
                        montosServicios = []
                        tallerServicios = []

                        for servicio in consultaServicios:
                            fechaServicioRealizado = servicio.fecha_servicios_vehiculo
                            kilometraje = servicio.kilometraje_preservicio
                            tipo = servicio.tipo_servicio
                            idServicio = servicio.id_servicio
                            montoServicio = servicio.monto_pagado
                            tallerServicio = servicio.taller_servicio
                            arregloDeFechasDeServicios.append(fechaServicioRealizado)
                            kilometrajes.append(kilometraje)
                            tiposServicios.append(tipo)
                            idsServicios.append(idServicio)
                            montosServicios.append(montoServicio)
                            tallerServicios.append(tallerServicio)
                        #arreglo de fechas lleno..
                        for fecha in arregloDeFechasDeServicios:
                            diferenciaDeDias = fechaDeHoy - fecha
                            diferenciaDeDiasDeFechas.append(int(diferenciaDeDias.days))

                        menor = 0
                        contadorDias = 0
                        for diferencia in diferenciaDeDiasDeFechas:
                            contadorDias = contadorDias + 1
                            if contadorDias == 1:

                                menor = diferencia
                            else:
                                if diferencia < menor:
                                    menor = diferencia
                                
                        #Encontrar la posición de la cantidadMenor y a su vez, la posición de la fecha
                        indice = diferenciaDeDiasDeFechas.index(menor)

                        fechaMasReciente = arregloDeFechasDeServicios[indice]
                        ultimoKilometraje = kilometrajes[indice]
                        ultimoTipo = tiposServicios[indice]
                        ultimoId = idsServicios[indice]
                        ultimoMonto = montosServicios[indice]
                        ultimoTaller = tallerServicios[indice]
                        
                        fechaEn4Meses = fechaMasReciente + relativedelta(months = 4)

                        arregloVehiculosFechas.append(str(fechaMasReciente))
                        arregloVehiculosFechasProximas.append(str(fechaEn4Meses))

                        mensajeUltimo = "U - Vehículo #"+codigoVehiculo
                        mensajeProximo = "P - Vehículo #"+codigoVehiculo

                        idUltimo = "Ulti"+str(contadorVehiculos)
                        idPendiente = "Pendi"+str(contadorVehiculos)
                        

                        mensajeVehiculoFechas.append([mensajeUltimo,idUltimo, codigoVehiculo, marcaVehiculo, modeloVehiculo, añoVehiculo, fotografiaFrontal, nombreCompletoEncargadoActual, ultimoKilometraje,ultimoTipo, fechaMasReciente, ultimoId, ultimoMonto, ultimoTaller])
                        mensajeVehiculoFechasProximas.append([mensajeProximo,idPendiente, codigoVehiculo, marcaVehiculo, modeloVehiculo, añoVehiculo, fotografiaFrontal, nombreCompletoEncargadoActual, fechaEn4Meses, fechaMasReciente])

                
                listaFechasUltimas = zip(arregloVehiculosFechas, mensajeVehiculoFechas)
                listaFechasProximas = zip(arregloVehiculosFechasProximas, mensajeVehiculoFechasProximas)


                return render(request,"empleadosCustom/ControlVehicular/Servicio/verCalendarioServicios.html",{"estaEnVerCalendarioServicios":estaEnVerCalendarioServicios,"id_admin":id_admin,"nombre":nombre,"apellidos":apellidos,"correo":correo,"nombreCompleto":nombreCompleto,"solicitantePrestamo":solicitantePrestamo, "administradordeVehiculos":administradordeVehiculos,"foto":foto,"almacen":almacen, "listaFechasUltimas":listaFechasUltimas,
                "listaFechasProximas":listaFechasProximas, "mensajeVehiculoFechas":mensajeVehiculoFechas,
                "mensajeVehiculoFechasProximas":mensajeVehiculoFechasProximas})
            
            solicitantePrestamo = True
            return render(request,"empleadosCustom/ControlVehicular/Servicio/verCalendarioServicios.html",{"estaEnVerCalendarioServicios":estaEnVerCalendarioServicios,"id_admin":id_admin,"nombre":nombre,"apellidos":apellidos,"correo":correo,"nombreCompleto":nombreCompleto,"solicitantePrestamo":solicitantePrestamo,"almacen":almacen})
            
    
    

    
        return render(request,"empleadosCustom/ControlVehicular/Servicio/verCalendarioServicios.html",{"estaEnVerCalendarioServicios":estaEnVerCalendarioServicios,"id_admin":id_admin,"nombre":nombre,"apellidos":apellidos,"correo":correo,"nombreCompleto":nombreCompleto,"almacen":almacen})
    else:
        return redirect('/login/')




def bajaVehiculo(request):
    if "idSesion" in request.session:
        if request.method == "POST":
            idVehiculoBaja = request.POST["idVehiculo"]

            #Actualizar estatus del vehículo y dejar el mismo encargado para saber quien fue el último.
            consultaVehiculo = Vehiculos.objects.filter(id_vehiculo = idVehiculoBaja).update(status_vehiculo = "Baja")

            otraConsultaVehiculo = Vehiculos.objects.filter(id_vehiculo = idVehiculoBaja)
            for datoVehiculo in otraConsultaVehiculo:
                codigoVehiculo = datoVehiculo.codigo_vehiculo
                marcaVehiculo = datoVehiculo.marca_vehiculo
                modeloVehiculo = datoVehiculo.modelo_vehiculo

                encargadoActual = datoVehiculo.responsable_actual_id
            
            consultaEncargadoActual = Empleados.objects.filter(id_empleado = encargadoActual)
            for datoEncargado in consultaEncargadoActual:
                nombreEncargado = datoEncargado.nombre
                apellidosEncargado = datoEncargado.apellidos

            nombreCompletoEncargadoActual = nombreEncargado + " " + apellidosEncargado


            if consultaVehiculo:
                request.session["bajaVehiculo"] = "Se ha dado de baja el vehículo #"+codigoVehiculo+ " - "+marcaVehiculo+" "+modeloVehiculo+" a cargo de "+nombreCompletoEncargadoActual

                return redirect("/verVehiculos/")
    
    
    else:
        return redirect('/login/')
        

def cambiosVehiculos(request):
    if "idSesion" in request.session:
        estaEnCambioVehiculo = True
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        if correo == "almacen01@customco.com.mx":
            almacen = True
        else:
            almacen = False
        nombreCompleto = nombre + " " + apellidos
        
        foto = fotoAdmin(request)
        
        empleado = Empleados.objects.filter(id_empleado = id_admin)
        for dato in empleado:
            area = dato.id_area_id

        if area == 1 or area ==5 or area == 7 or area == 8 or area == 9 or area == 10:
            if area == 5:
                solicitantePrestamo = True
                administradordeVehiculos = True
                return render(request,"empleadosCustom/ControlVehicular/Gestion/verCambios.html",{"estaEnCambioVehiculo":estaEnCambioVehiculo,"id_admin":id_admin,"nombre":nombre,"apellidos":apellidos,"correo":correo,"nombreCompleto":nombreCompleto,"solicitantePrestamo":solicitantePrestamo,"almacen":almacen,"foto":foto, "administradordeVehiculos":administradordeVehiculos})

    
    else:
        return redirect('/login/')




def agregarEvaluacion(request):
    if "idSesion" in request.session:
        estaEnAgregarEvaluacion = True
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        if correo == "almacen01@customco.com.mx":
            almacen = True
        else:
            almacen = False

        if correo == "recursos.humanos@customco.com.mx":
            rh = True
        else:
            rh = False

        nombreCompleto = nombre + " " + apellidos
        
        foto = fotoAdmin(request)
        
        empleado = Empleados.objects.filter(id_empleado = id_admin)
        for dato in empleado:
            area = dato.id_area_id

        if area == 1 or area ==5 or area == 7 or area == 8 or area == 9 or area == 10:
            if area == 5:
                solicitantePrestamo = True
                administradordeVehiculos = True
            else:
                solicitantePrestamo = True

        else:
            solicitantePrestamo = False
            administradordeVehiculos = False
        
        
        return render(request,"empleadosCustom/Evaluaciones/agregarEvaluaciones.html",{"estaEnAgregarEvaluacion":estaEnAgregarEvaluacion,"id_admin":id_admin,"nombre":nombre,"apellidos":apellidos,"correo":correo,"nombreCompleto":nombreCompleto,"solicitantePrestamo":solicitantePrestamo,"almacen":almacen,"foto":foto, "administradordeVehiculos":administradordeVehiculos, "rh":rh})

    
    else:
        return redirect('/login/')


def verEvaluaciones(request):
    if "idSesion" in request.session:
        estaEnVerEvaluaciones = True
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        if correo == "almacen01@customco.com.mx":
            almacen = True
        else:
            almacen = False

        if correo == "recursos.humanos@customco.com.mx":
            rh = True
        else:
            rh = False

        nombreCompleto = nombre + " " + apellidos
        
        foto = fotoAdmin(request)
        
        empleado = Empleados.objects.filter(id_empleado = id_admin)
        for dato in empleado:
            area = dato.id_area_id

        if area == 1 or area ==5 or area == 7 or area == 8 or area == 9 or area == 10:
            if area == 5:
                solicitantePrestamo = True
                administradordeVehiculos = True
            else:
                solicitantePrestamo = True

        else:
            solicitantePrestamo = False
            administradordeVehiculos = False


        #Aqui empieza lo de las evaluaciones
        consultasEvaluaciones = EvaluacionesDesempeno.objects.all()



        evaluacionesPendientes = []
        evaluacionesTerminadas = []

        porcentajeProgresBar = ""
        cantidadEmpleados = 0

        cantidadEmpleadosEstatusFinalizados = 0

        for evaluacion in consultasEvaluaciones:
            idEvaluacion = evaluacion.id_evaluacion_desempeno
            periodo = evaluacion.periodo_evaluacion
            nombre = evaluacion.nombre_evaluacion
            estatus = evaluacion.estatus_general
            agregadoPor = evaluacion.creado_por_id
            estatusEvaluadores = evaluacion.estatus_evaluadores

            #Agregado por
            consultaEmpleado = Empleados.objects.filter(id_empleado = agregadoPor)
            for datoEmpleado in consultaEmpleado:
                nombreEmpleadoAgregadoPor = datoEmpleado.nombre
                apellidoEmpleadoAgregadoPor = datoEmpleado.apellidos

            nombreCompletoAgregadoPor = nombreEmpleadoAgregadoPor + " " + apellidoEmpleadoAgregadoPor
        
            if estatus == "PENDIENTE":
                
                progreso = ""

                porcentajeProgresBar = ""

                cantidadEmpleados = 0
                cantidadEmpleadosEstatusFinalizados = 0

                #Consultar si la evaluación tiene evaluadores..
                consultaEvaluadores = IndicadorEvaluador.objects.filter(evaluacion_desempeno_id__id_evaluacion_desempeno = idEvaluacion)
                if consultaEvaluadores:
                    if estatusEvaluadores == "PENDIENTE":
                        progreso = "Evaluadores sin finalizar"

                    else:
                        progreso = "activa"


                        #CALCULO DE PROGRESSBAR

                        for evaluador in consultaEvaluadores:
                            idsEmpleadosEvaluados = evaluador.empleados_evaluados
                            estatusEmpleadosEvaluados = evaluador.estatus_empleados_evaluador

                            arrayEmpleados = idsEmpleadosEvaluados.split(",")
                            arrayEstatus = estatusEmpleadosEvaluados.split(",")

                            listaZipeada = zip(arrayEmpleados, arrayEstatus)

                            for empleado, estatus in listaZipeada:
                                cantidadEmpleados = cantidadEmpleados+1

                                if estatus == "F":
                                    cantidadEmpleadosEstatusFinalizados = cantidadEmpleadosEstatusFinalizados + 1
                        
                        #regla de 3
                        
                        porcentajeProgresBarFloat = (cantidadEmpleadosEstatusFinalizados * 100)/cantidadEmpleados
                        porcentajeRedondeado = round(porcentajeProgresBarFloat)
                        porcentajeProgresBar = str(porcentajeRedondeado)





                else:
                    progreso = "Aún sin evaluadores"

                evaluacionesPendientes.append([idEvaluacion, periodo, nombre,progreso, nombreCompletoAgregadoPor, porcentajeProgresBar])
            
            #else:

        
        
        if "evaluacionAgregada" in request.session:
            evaluacionAgregada = request.session["evaluacionAgregada"]
            del request.session["evaluacionAgregada"]
            return render(request,"empleadosCustom/Evaluaciones/verEvaluaciones.html",{"estaEnVerEvaluaciones":estaEnVerEvaluaciones,"id_admin":id_admin,"nombre":nombre,"apellidos":apellidos,"correo":correo,"nombreCompleto":nombreCompleto,"solicitantePrestamo":solicitantePrestamo,"almacen":almacen,"foto":foto, "administradordeVehiculos":administradordeVehiculos, "rh":rh,
            "evaluacionAgregada":evaluacionAgregada, "evaluacionesPendientes":evaluacionesPendientes, "porcentajeProgresBar":porcentajeProgresBar
            , "cantidadEmpleados":cantidadEmpleados, "cantidadEmpleadosEstatusFinalizados":cantidadEmpleadosEstatusFinalizados})

        if "registroEvaluadorExitoso" in request.session:
            registroEvaluadorExitoso = request.session["registroEvaluadorExitoso"]
            del request.session["registroEvaluadorExitoso"]

            return render(request,"empleadosCustom/Evaluaciones/verEvaluaciones.html",{"estaEnVerEvaluaciones":estaEnVerEvaluaciones,"id_admin":id_admin,"nombre":nombre,"apellidos":apellidos,"correo":correo,"nombreCompleto":nombreCompleto,"solicitantePrestamo":solicitantePrestamo,"almacen":almacen,"foto":foto, "administradordeVehiculos":administradordeVehiculos, "rh":rh,"evaluacionesPendientes":evaluacionesPendientes,
            "registroEvaluadorExitoso":registroEvaluadorExitoso, "porcentajeProgresBar":porcentajeProgresBar, "cantidadEmpleados":cantidadEmpleados, "cantidadEmpleadosEstatusFinalizados":cantidadEmpleadosEstatusFinalizados})

        if "evaluadoresFinalizados" in request.session:
            evaluadoresFinalizados = request.session["evaluadoresFinalizados"]
            del request.session["evaluadoresFinalizados"]

            return render(request,"empleadosCustom/Evaluaciones/verEvaluaciones.html",{"estaEnVerEvaluaciones":estaEnVerEvaluaciones,"id_admin":id_admin,"nombre":nombre,"apellidos":apellidos,"correo":correo,"nombreCompleto":nombreCompleto,"solicitantePrestamo":solicitantePrestamo,"almacen":almacen,"foto":foto, "administradordeVehiculos":administradordeVehiculos, "rh":rh,"evaluacionesPendientes":evaluacionesPendientes,
            "evaluadoresFinalizados":evaluadoresFinalizados, "porcentajeProgresBar":porcentajeProgresBar, "cantidadEmpleados":cantidadEmpleados, "cantidadEmpleadosEstatusFinalizados":cantidadEmpleadosEstatusFinalizados})


        return render(request,"empleadosCustom/Evaluaciones/verEvaluaciones.html",{"estaEnVerEvaluaciones":estaEnVerEvaluaciones,"id_admin":id_admin,"nombre":nombre,"apellidos":apellidos,"correo":correo,"nombreCompleto":nombreCompleto,"solicitantePrestamo":solicitantePrestamo,"almacen":almacen,"foto":foto, "administradordeVehiculos":administradordeVehiculos, "rh":rh,"evaluacionesPendientes":evaluacionesPendientes, "porcentajeProgresBar":porcentajeProgresBar
        , "cantidadEmpleados":cantidadEmpleados, "cantidadEmpleadosEstatusFinalizados":cantidadEmpleadosEstatusFinalizados})

    
    else:
        return redirect('/login/')


def guardarRegistroEvaluacion(request):
    if "idSesion" in request.session:
        id_admin=request.session["idSesion"]

        if request.method == "POST":
            periodo = request.POST["periodo"]
            nombreEvaluacion = request.POST["nombreEvaluacion"]

            #Guardar evaluacion
            registroEvaluacion = EvaluacionesDesempeno(periodo_evaluacion = periodo, nombre_evaluacion = nombreEvaluacion,
            creado_por = Empleados.objects.get(id_empleado = id_admin), estatus_general = "PENDIENTE", estatus_evaluadores = "PENDIENTE")
            registroEvaluacion.save()
            if registroEvaluacion:
                request.session["evaluacionAgregada"] = "La evaluación ha sido agregada al sistema de manera correcta!"

                return redirect('/verEvaluaciones/')
    
    else:
        return redirect('/login/')

def asignarEvaluadores(request):
    if "idSesion" in request.session:
        estaEnVerEvaluaciones = True
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        if correo == "almacen01@customco.com.mx":
            almacen = True
        else:
            almacen = False

        if correo == "recursos.humanos@customco.com.mx":
            rh = True
        else:
            rh = False

        nombreCompleto = nombre + " " + apellidos
        
        foto = fotoAdmin(request)
        
        empleado = Empleados.objects.filter(id_empleado = id_admin)
        for dato in empleado:
            area = dato.id_area_id

        if area == 1 or area ==5 or area == 7 or area == 8 or area == 9 or area == 10:
            if area == 5:
                solicitantePrestamo = True
                administradordeVehiculos = True
            else:
                solicitantePrestamo = True

        else:
            solicitantePrestamo = False
            administradordeVehiculos = False

        #Aqui empieza todo
        if request.method == "POST":
            idEvaluacion = request.POST["idEvaluacion"]

            #Verificar si ya tiene evaluadores
            consultaEvaluadores = IndicadorEvaluador.objects.filter(evaluacion_desempeno_id__id_evaluacion_desempeno = idEvaluacion)

            listaEvaluadoresYaAsignados = []
            if consultaEvaluadores:
                tieneEvaluadores = "SI"

                for evaluador in consultaEvaluadores:
                    empleadoEvaluador = evaluador.empleado_evaluador_id

                    consultaEmpleadoEvaluador = Empleados.objects.filter(id_empleado = empleadoEvaluador)
                    for dato in consultaEmpleadoEvaluador:
                        nombreEmpleadoEvaluador = dato.nombre
                        apellidosEmpleadoEvaluador = dato.apellidos
                        departamento = dato.id_area_id
                        imagenEmpleadoEvaluador = dato.imagen_empleado
                        puesto = dato.puesto


                    

                    nombreCompletoEvaluador = nombreEmpleadoEvaluador + " " + apellidosEmpleadoEvaluador

                    consultaDepartamentoEvaluador = Areas.objects.filter(id_area = departamento)
                    for datoArea in consultaDepartamentoEvaluador:
                        nombreDepartamento = datoArea.nombre
                        colorDepartamento = datoArea.color

                    estatusGeneral = evaluador.estatus_general
                    
                    #Empleados evaluados
                    empleadosEvaluados = evaluador.empleados_evaluados
                    estatusEmpleadosEvaluados = evaluador.estatus_empleados_evaluador

                    listaEmpleadosEvaluados = empleadosEvaluados.split(",")

                    listaNombreEmpleadosEvaluados = []
                    listaIdsEmpleadosEvaluados = []

                    for empleado in listaEmpleadosEvaluados:
                        idEmpleado = empleado
                        consultaEmpleado = Empleados.objects.filter(id_empleado = idEmpleado)

                        for datoEmpleado in consultaEmpleado:
                            nombreEmpleado = datoEmpleado.nombre
                            apellidoEmpleado = datoEmpleado.apellidos

                        nombreCompletoEmpleado = nombreEmpleado + " " + apellidoEmpleado

                        listaNombreEmpleadosEvaluados.append(nombreCompletoEmpleado)
                        listaIdsEmpleadosEvaluados.append(idEmpleado)

                    listaPendientes = estatusEmpleadosEvaluados.split(",")

                    listaEmpladosYSuEstatus = zip(listaNombreEmpleadosEvaluados,listaPendientes, listaEmpleadosEvaluados)


                    agregadoPor = evaluador.agregado_por
                    agregadoPorInt = int(agregadoPor)

                    consultaAgregadoPor = Empleados.objects.filter(id_empleado = agregadoPorInt)
                    for datoEmpleado in consultaAgregadoPor:
                        nombreEmpleadoAgregadoPor = datoEmpleado.nombre
                        apellidosAgregadoPor = datoEmpleado.apellidos

                    nombreCompletoAgregadoPor = nombreEmpleadoAgregadoPor + " " +apellidosAgregadoPor
                    fechaCreado = evaluador.fecha_creacion

                    listaEvaluadoresYaAsignados.append([estatusGeneral,listaEmpladosYSuEstatus, nombreCompletoAgregadoPor,
                    fechaCreado, nombreCompletoEvaluador, nombreDepartamento, imagenEmpleadoEvaluador,puesto])

                
                

            else:
                tieneEvaluadores = "NO"
                listaEvaluadoresYaAsignados = None

            infoAreas = Areas.objects.all()

            #consultaEmpleadosSistemas
            empleadosSistemas = Empleados.objects.filter(id_area_id__id_area = 1)

            infoEmpleadosSistemas = []
            for empleado in empleadosSistemas:
                correo = empleado.correo
                estatus = empleado.activo
                if "customco.com.mx" in correo and estatus == "A":
                    idEmpleado = empleado.id_empleado
                    nombreEmpleado = empleado.nombre
                    apellidoEmpleado = empleado.apellidos

                    nombreCompletoEmpleado = nombreEmpleado +" "+apellidoEmpleado

                    infoEmpleadosSistemas.append([idEmpleado, nombreCompletoEmpleado])


            empleadosPorArea = []

            for area in infoAreas:
                idArea = area.id_area

                empleadosDelArea = []
                #Consulta de empleados de esa area
                consultaEmpleadosArea = Empleados.objects.filter(id_area_id__id_area = idArea)

                for empleado in consultaEmpleadosArea:
                    idEmpleado = empleado.id_empleado
                    nombreEmpleado = empleado.nombre
                    apellidoEmpleado = empleado.apellidos

                    nombreCompletoEmpleadoArea = nombreEmpleado +" "+apellidoEmpleado
                    estatusEmpleado = empleado.activo
                    correo = empleado.correo

                    if "customco.com.mx" in correo and estatusEmpleado == "A":
                        empleadosDelArea.append([idArea,idEmpleado, nombreCompletoEmpleadoArea])

                empleadosPorArea.append(empleadosDelArea)

            #El arreglo ya tiene a todos los empleados por areas

            empleadosTabla = []
            empleadosTablaJS = []

            consultaEmpleados = Empleados.objects.all()

            if consultaEvaluadores:

                arregloPurosIds = []
                for evaluador in consultaEvaluadores:
                    empleadosEvaluados = evaluador.empleados_evaluados

                    arrayEmpleados = empleadosEvaluados.split(",")

                    for empleado in arrayEmpleados:
                        idEmpleadoStr = empleado

                        arregloPurosIds.append(idEmpleadoStr)

            for empleado in consultaEmpleados:
                estatusEmpleado = empleado.activo
                correo = empleado.correo

                if "customco.com.mx" in correo and estatusEmpleado == "A":
                    idEmpleado = empleado.id_empleado
                    idEmpleadoString = str(idEmpleado)
                    nombreEmpleado = empleado.nombre
                    apellidosEmpleado = empleado.apellidos
                    imagenEmpleado = empleado.imagen_empleado
                    idDepartamento = empleado.id_area_id

                    consultaDepartamento = Areas.objects.filter(id_area = idDepartamento)
                    for datoDepa in consultaDepartamento:
                        nombreDepartamento = datoDepa.nombre
                        colorDepartamento = datoDepa.color

                    puestoEmpleado = empleado.puesto
                    correoEmpleado = empleado.correo

                    #ConsultaEmpleadosEvaluados

                   
                    if consultaEvaluadores:
                            

                        if idEmpleadoString in arregloPurosIds:
                                
                            yaPorEvaluar = True
                            

                        else:
                            empleadosTabla.append([idEmpleado, nombreEmpleado, apellidosEmpleado,
                            imagenEmpleado, nombreDepartamento, colorDepartamento, puestoEmpleado, correoEmpleado])

                            empleadosTablaJS.append([idEmpleado, nombreEmpleado, apellidosEmpleado,
                            imagenEmpleado, nombreDepartamento, colorDepartamento, puestoEmpleado, correoEmpleado])
                    
                    else:

                        empleadosTabla.append([idEmpleado, nombreEmpleado, apellidosEmpleado,
                        imagenEmpleado, nombreDepartamento, colorDepartamento, puestoEmpleado, correoEmpleado])

                        empleadosTablaJS.append([idEmpleado, nombreEmpleado, apellidosEmpleado,
                        imagenEmpleado, nombreDepartamento, colorDepartamento, puestoEmpleado, correoEmpleado])

            return render(request,"empleadosCustom/Evaluaciones/asignarEvaluadores.html",{"estaEnVerEvaluaciones":estaEnVerEvaluaciones,"id_admin":id_admin,"nombre":nombre,"apellidos":apellidos,"correo":correo,"nombreCompleto":nombreCompleto,"solicitantePrestamo":solicitantePrestamo,"almacen":almacen,"foto":foto, "administradordeVehiculos":administradordeVehiculos, "rh":rh, "idEvaluacion":idEvaluacion, "tieneEvaluadores":tieneEvaluadores,
            "infoAreas":infoAreas, "infoEmpleadosSistemas":infoEmpleadosSistemas, "empleadosPorArea":empleadosPorArea, "empleadosTabla":empleadosTabla, "empleadosTablaJS":empleadosTablaJS,
            "listaEvaluadoresYaAsignados":listaEvaluadoresYaAsignados})

    
    else:
        return redirect('/login/')



def guardarEvaluador(request):
    if "idSesion" in request.session:
        id_admin=request.session["idSesion"]
        
        fechaHoy = datetime.now()
        idEvaluacion = request.POST["idEvaluacion"]
        evaluador = request.POST["evaluador"]
        idsEmpleadosEvaluados = request.POST["idsEmpleadosInput"]
        splitEmpleadosEvaluados = idsEmpleadosEvaluados.split(",")
        numeroPosiciones= len(splitEmpleadosEvaluados)
        guardarEstatusEvaluador = ""
        contador = 0
        for x in range(numeroPosiciones):
            contador = contador+1
            if contador == 1:
                guardarEstatusEvaluador= "P"
            else:
                guardarEstatusEvaluador = guardarEstatusEvaluador+",P"

        registroEvaluador = IndicadorEvaluador(fecha_creacion = fechaHoy, evaluacion_desempeno = EvaluacionesDesempeno.objects.get(id_evaluacion_desempeno = idEvaluacion), empleado_evaluador=Empleados.objects.get(id_empleado = evaluador),estatus_general = "PENDIENTE", empleados_evaluados = idsEmpleadosEvaluados, estatus_empleados_evaluador = guardarEstatusEvaluador,agregado_por = str(id_admin) )
        
        registroEvaluador.save()

        #Guardar respuestas de cada evaluador.
        if registroEvaluador:

            #Obtener el id del ultimo indicadorEvaluador
            contador = 0
            consultasEvaluacionesEmpleados = IndicadorEvaluador.objects.all()
            for evaluador in consultasEvaluacionesEmpleados:
                contador = evaluador.id_indicador_evaluador #Viene siendo el ultimo id que se guardo
            
            for empleado in splitEmpleadosEvaluados:
                idEmpleado = empleado

                #String de 42 respuestas en 1

                respuestas = "1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1"
                estadosPreguntas = "p,p,p,p,p,p,p,p,p,p,p,p,p,p,p,p,p,p,p,p,p,p,p,p,p,p,p,p,p,p,p,p,p,p,p,p,p,p,p,p,p,p"
                #Registrar empleado en tabla donde se registrarán sus respuestas
                registroRespuestasPendientesEmpleado = ResultadosDesempeno(indicador_evaluador = IndicadorEvaluador.objects.get(id_indicador_evaluador = contador),
                id_empleado_evaluado = Empleados.objects.get(id_empleado = idEmpleado),
                resultado_preguntas = respuestas, estatus_resultado_preguntas = estadosPreguntas,
                estatus_resultado = "PENDIENTE")

                registroRespuestasPendientesEmpleado.save()


            request.session["registroEvaluadorExitoso"] = "El registro del Evaluador Se Realizó Con Éxito"
            return redirect('/verEvaluaciones/')

    
    else:
        return redirect('/login/')

def finalizarConfiguracionEvaluador(request):
    if "idSesion" in request.session:
       
        idEvaluacion = request.POST["idEvaluacion"]

        #Actualizar estatus de evaluadores
        actualizacion = EvaluacionesDesempeno.objects.filter(id_evaluacion_desempeno = idEvaluacion).update(estatus_evaluadores = "FINALIZADO")

        request.session["evaluadoresFinalizados"] = "La asignación de evaluadores ha sido finalizada con éxito!"
        return redirect('/verEvaluaciones/')

    
    else:
        return redirect('/login/')


def verResultadosEvaluadores(request):
    if "idSesion" in request.session:
        estaEnVerEvaluaciones = True
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        if correo == "almacen01@customco.com.mx":
            almacen = True
        else:
            almacen = False

        if correo == "recursos.humanos@customco.com.mx":
            rh = True
        else:
            rh = False

        nombreCompleto = nombre + " " + apellidos
        
        foto = fotoAdmin(request)
        
        empleado = Empleados.objects.filter(id_empleado = id_admin)
        for dato in empleado:
            area = dato.id_area_id

        if area == 1 or area ==5 or area == 7 or area == 8 or area == 9 or area == 10:
            if area == 5:
                solicitantePrestamo = True
                administradordeVehiculos = True
            else:
                solicitantePrestamo = True

        else:
            solicitantePrestamo = False
            administradordeVehiculos = False

        #Aqui empieza todo
        if request.method == "POST":
            idEvaluacion = request.POST["idEvaluacion"]

            #Verificar si ya tiene evaluadores
            consultaEvaluadores = IndicadorEvaluador.objects.filter(evaluacion_desempeno_id__id_evaluacion_desempeno = idEvaluacion)

            listaEvaluadoresYaAsignados = []
            if consultaEvaluadores:
                tieneEvaluadores = "SI"

                for evaluador in consultaEvaluadores:
                    idConsultaEvaluador = evaluador.id_indicador_evaluador
                    empleadoEvaluador = evaluador.empleado_evaluador_id

                    consultaEmpleadoEvaluador = Empleados.objects.filter(id_empleado = empleadoEvaluador)
                    for dato in consultaEmpleadoEvaluador:
                        nombreEmpleadoEvaluador = dato.nombre
                        apellidosEmpleadoEvaluador = dato.apellidos
                        departamento = dato.id_area_id
                        imagenEmpleadoEvaluador = dato.imagen_empleado
                        puesto = dato.puesto


                    

                    nombreCompletoEvaluador = nombreEmpleadoEvaluador + " " + apellidosEmpleadoEvaluador

                    consultaDepartamentoEvaluador = Areas.objects.filter(id_area = departamento)
                    for datoArea in consultaDepartamentoEvaluador:
                        nombreDepartamento = datoArea.nombre
                        colorDepartamento = datoArea.color

                    estatusGeneral = evaluador.estatus_general
                    
                    #Empleados evaluados
                    empleadosEvaluados = evaluador.empleados_evaluados
                    estatusEmpleadosEvaluados = evaluador.estatus_empleados_evaluador

                    listaEmpleadosEvaluados = empleadosEvaluados.split(",")

                    listaNombreEmpleadosEvaluados = []

                    for empleado in listaEmpleadosEvaluados:
                        idEmpleado = empleado
                        consultaEmpleado = Empleados.objects.filter(id_empleado = idEmpleado)

                        for datoEmpleado in consultaEmpleado:
                            nombreEmpleado = datoEmpleado.nombre
                            apellidoEmpleado = datoEmpleado.apellidos

                        nombreCompletoEmpleado = nombreEmpleado + " " + apellidoEmpleado

                        listaNombreEmpleadosEvaluados.append(nombreCompletoEmpleado)

                    listaPendientes = estatusEmpleadosEvaluados.split(",")

                    listaEmpladosYSuEstatus = zip(listaNombreEmpleadosEvaluados,listaPendientes, listaEmpleadosEvaluados)


                    agregadoPor = evaluador.agregado_por
                    agregadoPorInt = int(agregadoPor)

                    consultaAgregadoPor = Empleados.objects.filter(id_empleado = agregadoPorInt)
                    for datoEmpleado in consultaAgregadoPor:
                        nombreEmpleadoAgregadoPor = datoEmpleado.nombre
                        apellidosAgregadoPor = datoEmpleado.apellidos

                    nombreCompletoAgregadoPor = nombreEmpleadoAgregadoPor + " " +apellidosAgregadoPor
                    fechaCreado = evaluador.fecha_creacion

                    listaEvaluadoresYaAsignados.append([estatusGeneral,listaEmpladosYSuEstatus, nombreCompletoAgregadoPor,
                    fechaCreado, nombreCompletoEvaluador, nombreDepartamento, imagenEmpleadoEvaluador,puesto, idConsultaEvaluador])

                
                

            else:
                tieneEvaluadores = "NO"
                listaEvaluadoresYaAsignados = None

            infoAreas = Areas.objects.all()

            #consultaEmpleadosSistemas
            empleadosSistemas = Empleados.objects.filter(id_area_id__id_area = 1)

            infoEmpleadosSistemas = []
            for empleado in empleadosSistemas:
                correo = empleado.correo
                estatus = empleado.activo
                if "customco.com.mx" in correo and estatus == "A":
                    idEmpleado = empleado.id_empleado
                    nombreEmpleado = empleado.nombre
                    apellidoEmpleado = empleado.apellidos

                    nombreCompletoEmpleado = nombreEmpleado +" "+apellidoEmpleado

                    infoEmpleadosSistemas.append([idEmpleado, nombreCompletoEmpleado])


            empleadosPorArea = []

            for area in infoAreas:
                idArea = area.id_area

                empleadosDelArea = []
                #Consulta de empleados de esa area
                consultaEmpleadosArea = Empleados.objects.filter(id_area_id__id_area = idArea)

                for empleado in consultaEmpleadosArea:
                    idEmpleado = empleado.id_empleado
                    nombreEmpleado = empleado.nombre
                    apellidoEmpleado = empleado.apellidos

                    nombreCompletoEmpleadoArea = nombreEmpleado +" "+apellidoEmpleado
                    estatusEmpleado = empleado.activo
                    correo = empleado.correo

                    if "customco.com.mx" in correo and estatusEmpleado == "A":
                        empleadosDelArea.append([idArea,idEmpleado, nombreCompletoEmpleadoArea])

                empleadosPorArea.append(empleadosDelArea)

            #El arreglo ya tiene a todos los empleados por areas

            empleadosTabla = []
            empleadosTablaJS = []

            consultaEmpleados = Empleados.objects.all()

            if consultaEvaluadores:

                arregloPurosIds = []
                for evaluador in consultaEvaluadores:
                    empleadosEvaluados = evaluador.empleados_evaluados

                    arrayEmpleados = empleadosEvaluados.split(",")

                    for empleado in arrayEmpleados:
                        idEmpleadoStr = empleado

                        arregloPurosIds.append(idEmpleadoStr)

            for empleado in consultaEmpleados:
                estatusEmpleado = empleado.activo
                correo = empleado.correo

                if "customco.com.mx" in correo and estatusEmpleado == "A":
                    idEmpleado = empleado.id_empleado
                    idEmpleadoString = str(idEmpleado)
                    nombreEmpleado = empleado.nombre
                    apellidosEmpleado = empleado.apellidos
                    imagenEmpleado = empleado.imagen_empleado
                    idDepartamento = empleado.id_area_id

                    consultaDepartamento = Areas.objects.filter(id_area = idDepartamento)
                    for datoDepa in consultaDepartamento:
                        nombreDepartamento = datoDepa.nombre
                        colorDepartamento = datoDepa.color

                    puestoEmpleado = empleado.puesto
                    correoEmpleado = empleado.correo

                    #ConsultaEmpleadosEvaluados

                   
                    if consultaEvaluadores:
                            

                        if idEmpleadoString in arregloPurosIds:
                                
                            yaPorEvaluar = True
                            

                        else:
                            empleadosTabla.append([idEmpleado, nombreEmpleado, apellidosEmpleado,
                            imagenEmpleado, nombreDepartamento, colorDepartamento, puestoEmpleado, correoEmpleado])

                            empleadosTablaJS.append([idEmpleado, nombreEmpleado, apellidosEmpleado,
                            imagenEmpleado, nombreDepartamento, colorDepartamento, puestoEmpleado, correoEmpleado])
                    
                    else:

                        empleadosTabla.append([idEmpleado, nombreEmpleado, apellidosEmpleado,
                        imagenEmpleado, nombreDepartamento, colorDepartamento, puestoEmpleado, correoEmpleado])

                        empleadosTablaJS.append([idEmpleado, nombreEmpleado, apellidosEmpleado,
                        imagenEmpleado, nombreDepartamento, colorDepartamento, puestoEmpleado, correoEmpleado])

            return render(request,"empleadosCustom/Evaluaciones/verResultadosEvaluadores.html",{"estaEnVerEvaluaciones":estaEnVerEvaluaciones,"id_admin":id_admin,"nombre":nombre,"apellidos":apellidos,"correo":correo,"nombreCompleto":nombreCompleto,"solicitantePrestamo":solicitantePrestamo,"almacen":almacen,"foto":foto, "administradordeVehiculos":administradordeVehiculos, "rh":rh, "idEvaluacion":idEvaluacion, "tieneEvaluadores":tieneEvaluadores,
            "infoAreas":infoAreas, "infoEmpleadosSistemas":infoEmpleadosSistemas, "empleadosPorArea":empleadosPorArea, "empleadosTabla":empleadosTabla, "empleadosTablaJS":empleadosTablaJS,
            "listaEvaluadoresYaAsignados":listaEvaluadoresYaAsignados})

    
    else:
        return redirect('/login/')



def verMisEvaluaciones(request):
    if "idSesion" in request.session:
        estaEnVerMisEvaluaciones = True
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        if correo == "almacen01@customco.com.mx":
            almacen = True
        else:
            almacen = False

        if correo == "recursos.humanos@customco.com.mx":
            rh = True
        else:
            rh = False

        nombreCompleto = nombre + " " + apellidos
        
        foto = fotoAdmin(request)
        
        empleado = Empleados.objects.filter(id_empleado = id_admin)
        for dato in empleado:
            area = dato.id_area_id

        solicitantePrestamo = False
        administradordeVehiculos = False

        if area == 1 or area ==5 or area == 7 or area == 8 or area == 9 or area == 10:
            if area == 5:
                solicitantePrestamo = True
                administradordeVehiculos = True
            else:
                solicitantePrestamo = True

        else:
            solicitantePrestamo = False
            administradordeVehiculos = False

        
        #Aqui empieza todo
        consultasEvaluaciones = IndicadorEvaluador.objects.filter(empleado_evaluador_id__id_empleado = id_admin)

        if consultasEvaluaciones:
            tieneEvaluacionesAsignadas = True

            datosTabla = []
            for evaluacion in consultasEvaluaciones:
                idEvaluacionDesempeno = evaluacion.evaluacion_desempeno_id
                fechaCreacion = evaluacion.fecha_creacion
                agregadoPor = evaluacion.agregado_por

                #Info de evaluación desempeño
                consultaEvaluacion = EvaluacionesDesempeno.objects.filter(id_evaluacion_desempeno = idEvaluacionDesempeno)
                for datoEvaluacion in consultaEvaluacion:
                    nombreEvaluacion = datoEvaluacion.nombre_evaluacion
                    periodoEvaluacion = datoEvaluacion.periodo_evaluacion
                
                #Consulta de agregado por
                consultaAgregadoPor = Empleados.objects.filter(id_empleado = agregadoPor)
                for datoAgregadoPor in consultaAgregadoPor:
                    nombreAgregadoPor = datoAgregadoPor.nombre
                    apellidoAgregadoPor = datoAgregadoPor.apellidos

                nombreCompletoAgregadoPor = nombreAgregadoPor + " "+apellidoAgregadoPor

                estatusGeneral = evaluacion.estatus_general

                datosEmpleadosEvaluados = []
                idEmpleadosEvaluados = []
                estatusRespuestasEmpleados = []

                empleadosEvaluados = evaluacion.empleados_evaluados

                listaEmpleadosEvaluados = empleadosEvaluados.split(",")

                for empleado in listaEmpleadosEvaluados:
                    idEmpleado = empleado
                    consultaEmpleado = Empleados.objects.filter(id_empleado = idEmpleado)

                    for dato in consultaEmpleado:
                        idEmpleado = dato.id_empleado
                        nombreEmpleado = dato.nombre
                        apellidoEmpleado = dato.apellidos
                    nombreCompletoEmpleadoEvaluado = nombreEmpleado + " "+apellidoEmpleado

                    datosEmpleadosEvaluados.append(nombreCompletoEmpleadoEvaluado)
                    idEmpleadosEvaluados.append(idEmpleado)

                    estatusRespuestas = ""
                    consultaEmpleadoRespuestas = ResultadosDesempeno.objects.filter(id_empleado_evaluado_id__id_empleado = idEmpleado)
                    for datoConsultaEmpleados in consultaEmpleadoRespuestas:
                        estatusRespuestas = datoConsultaEmpleados.estatus_resultado
                        idEvaluacionDesempenoForanea = datoConsultaEmpleados.indicador_evaluador_id

                    estatusRespuestasEmpleados.append(estatusRespuestas)


                listaEmpleadosEvaluadosZipeada = zip(datosEmpleadosEvaluados, idEmpleadosEvaluados, estatusRespuestasEmpleados)



                datosTabla.append([idEvaluacionDesempenoForanea,
                fechaCreacion, nombreCompletoAgregadoPor, nombreEvaluacion, periodoEvaluacion,estatusGeneral,listaEmpleadosEvaluadosZipeada])


        else:
            tieneEvaluacionesAsignadas = False
            datosTabla = []
        

        if "respuestaGuardada" in request.session:
            respuestaGuardada = request.session["respuestaGuardada"]
            del request.session["respuestaGuardada"]
            
            return render(request,"empleadosCustom/Evaluaciones/verMisEvaluaciones.html",{"estaEnVerMisEvaluaciones":estaEnVerMisEvaluaciones,"id_admin":id_admin,"nombre":nombre,"apellidos":apellidos,"correo":correo,"nombreCompleto":nombreCompleto,"solicitantePrestamo":solicitantePrestamo,"almacen":almacen,"foto":foto, "administradordeVehiculos":administradordeVehiculos, "rh":rh,
            "tieneEvaluacionesAsignadas":tieneEvaluacionesAsignadas,"datosTabla":datosTabla, "respuestaGuardada":respuestaGuardada})

        return render(request,"empleadosCustom/Evaluaciones/verMisEvaluaciones.html",{"estaEnVerMisEvaluaciones":estaEnVerMisEvaluaciones,"id_admin":id_admin,"nombre":nombre,"apellidos":apellidos,"correo":correo,"nombreCompleto":nombreCompleto,"solicitantePrestamo":solicitantePrestamo,"almacen":almacen,"foto":foto, "administradordeVehiculos":administradordeVehiculos, "rh":rh,
        "tieneEvaluacionesAsignadas":tieneEvaluacionesAsignadas,"datosTabla":datosTabla})

    
    else:
        return redirect('/login/')


def realizarVerEvaluacionEmpleado(request):
    if "idSesion" in request.session:
        estaEnVerMisEvaluaciones = True
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        if correo == "almacen01@customco.com.mx":
            almacen = True
        else:
            almacen = False

        if correo == "recursos.humanos@customco.com.mx":
            rh = True
        else:
            rh = False

        nombreCompleto = nombre + " " + apellidos
        
        foto = fotoAdmin(request)
        
        empleado = Empleados.objects.filter(id_empleado = id_admin)
        for dato in empleado:
            area = dato.id_area_id

        solicitantePrestamo = False
        administradordeVehiculos = False

        if area == 1 or area ==5 or area == 7 or area == 8 or area == 9 or area == 10:
            if area == 5:
                solicitantePrestamo = True
                administradordeVehiculos = True
            else:
                solicitantePrestamo = True

        else:
            solicitantePrestamo = False
            administradordeVehiculos = False

        
        #Aqui empieza todo
        if request.method == "POST":
            idEmpleadoAEvaluar = request.POST["idEmpleado"]
            idAsignacion = request.POST["idAsignacionEvaluador"]

            print("EMPLEADO EVALUAR "+str(idEmpleadoAEvaluar))
            print("ASIGNACION "+str(idAsignacion))

            #Tenemos que saber si ya la empezó o apenas la va a empezar

            #Consulta de las respuestas

            consultaRespuestas = ResultadosDesempeno.objects.filter(indicador_evaluador_id__id_indicador_evaluador = idAsignacion, id_empleado_evaluado_id__id_empleado = idEmpleadoAEvaluar)

            if consultaRespuestas:
                print("ASJDLASLDFJLKASJDLFJLKASJFLKJASLKFJLKAJDFLKJAKLDFSKLAKLSDFKAJSLDFKJKL")
            for datosRespuestas in consultaRespuestas:
                estadosRespuestas = datosRespuestas.estatus_resultado_preguntas
                idRespuestaEmpleadito = datosRespuestas.id_resultado_desempeno
            
            arrayEstadosRespuestas = estadosRespuestas.split(",")

            primerRespuesta = arrayEstadosRespuestas[0]
            segundaRespuesta = arrayEstadosRespuestas[5]
            tercerRespuesta = arrayEstadosRespuestas[8]
            cuartaRespuesta = arrayEstadosRespuestas[11]
            quintaRespuesta = arrayEstadosRespuestas[16]
            sextaRespuesta = arrayEstadosRespuestas[18]
            septimaRespuesta = arrayEstadosRespuestas[21]
            octavaRespuesta = arrayEstadosRespuestas[25]
            novenaRespuesta = arrayEstadosRespuestas[27]
            decimaRespuesta = arrayEstadosRespuestas[28]
            onceavaRespuesta = arrayEstadosRespuestas[31]
            
            if primerRespuesta == "p":
                aunNoEsEvaluado = "sinEvaluarAun"
                enCualVa = "primera"
            else:
                aunNoEsEvaluado = "yaEmpezoSuEvaluacion"

                #Ver en cual va..
                if segundaRespuesta == "p":
                    enCualVa = "segunda"
                elif tercerRespuesta == "p":
                    enCualVa = "tercera"
                elif cuartaRespuesta == "p":
                    enCualVa = "cuarta"
                elif quintaRespuesta == "p":
                    enCualVa = "quinta"
                elif sextaRespuesta == "p":
                    enCualVa = "sexta"
                elif septimaRespuesta == "p":
                    enCualVa = "septima"
                elif octavaRespuesta == "p":
                    enCualVa = "octava"
                elif novenaRespuesta == "p":
                    enCualVa = "novena"
                elif decimaRespuesta == "p":
                    enCualVa = "decima"
                elif onceavaRespuesta == "p":
                    enCualVa = "onceava"

                elif onceavaRespuesta == "c":
                    enCualVa = "finalizada"


            #Consulta empleado a evaluar
            consultaEmpleadoAEvaluar = Empleados.objects.filter(id_empleado = idEmpleadoAEvaluar)
            for datoEmpleado in consultaEmpleadoAEvaluar:
                nombreEmpleado = datoEmpleado.nombre
                apellidoEmpleado = datoEmpleado.apellidos

            nombreCompletoEmpleadoEvaluar = nombreEmpleado + " " + apellidoEmpleado

            #Consulta asignacion
            consultaAsignacion = IndicadorEvaluador.objects.filter(id_indicador_evaluador = idAsignacion)
            for datoAsignacion in consultaAsignacion:
                idEvaluacion = datoAsignacion.evaluacion_desempeno_id

            #Consulta evaluacion
            consultaEvaluacion = EvaluacionesDesempeno.objects.filter(id_evaluacion_desempeno = idEvaluacion)
            for datoEvaluacion in consultaEvaluacion:
                nombreEvaluacion = datoEvaluacion.nombre_evaluacion
                periodoEvaluacion = datoEvaluacion.periodo_evaluacion
        
        return render(request,"empleadosCustom/Evaluaciones/evaluarEmpleado.html",{"estaEnVerMisEvaluaciones":estaEnVerMisEvaluaciones,"id_admin":id_admin,"nombre":nombre,"apellidos":apellidos,"correo":correo,"nombreCompleto":nombreCompleto,"solicitantePrestamo":solicitantePrestamo,"almacen":almacen,"foto":foto, "administradordeVehiculos":administradordeVehiculos, "rh":rh,
        "aunNoEsEvaluado":aunNoEsEvaluado, "nombreCompletoEmpleadoEvaluar":nombreCompletoEmpleadoEvaluar, "nombreEvaluacion":nombreEvaluacion, "periodoEvaluacion":periodoEvaluacion, "enCualVa":enCualVa, "idRespuestaEmpleadito":idRespuestaEmpleadito})

    
    else:
        return redirect('/login/')


def guardarRespuestaEvaluacion(request):
    if "idSesion" in request.session:
        
        if request.method == "POST":
            seccion = request.POST["enCualVa"]

            idRespuestaEmpleadito = request.POST["idRespuestaEmpleadito"]

            consultaRespuestas = ResultadosDesempeno.objects.filter(id_resultado_desempeno = idRespuestaEmpleadito)

            for datoRespuestas in consultaRespuestas:
                resultadoPreguntas = datoRespuestas.resultado_preguntas
                estadoPreguntas = datoRespuestas.estatus_resultado_preguntas
                indicadorEvaluador = datoRespuestas.indicador_evaluador_id
                idEmpleadoEvaluado = datoRespuestas.id_empleado_evaluado_id

            
                
            if seccion == "primera":
                pregunta1 = request.POST["pregunta1"]
                pregunta2 = request.POST["pregunta2"]
                pregunta3 = request.POST["pregunta3"]
                pregunta4 = request.POST["pregunta4"]
                pregunta5 = request.POST["pregunta5"]

                #Posiciones 0 a la 4
                arregloResultadoPreguntas = resultadoPreguntas.split(",") #[]
                arregloEsotadosPreguntas = estadoPreguntas.split(",")

                arregloResultadoPreguntas[0] = pregunta1
                arregloResultadoPreguntas[1] = pregunta2
                arregloResultadoPreguntas[2] = pregunta3
                arregloResultadoPreguntas[3] = pregunta4
                arregloResultadoPreguntas[4] = pregunta5

                arregloEsotadosPreguntas[0] = "c"
                arregloEsotadosPreguntas[1] = "c"
                arregloEsotadosPreguntas[2] = "c"
                arregloEsotadosPreguntas[3] = "c"
                arregloEsotadosPreguntas[4] = "c"

                resultadoActualizado = ""
                contador1 = 0
                resultadoEstados = ""
                contador2 = 0

                for respuesta in arregloResultadoPreguntas:
                    contador1 = contador1 + 1

                    if contador1 == 1:
                        resultadoActualizado = respuesta
                    else:
                        resultadoActualizado = resultadoActualizado + ","+respuesta

                for estado in arregloEsotadosPreguntas:
                    contador2 = contador2 + 1

                    if contador2 == 1:
                        resultadoEstados = estado
                    else:
                        resultadoEstados = resultadoEstados + ","+estado

                #Actualizacion
                actualizacion = ResultadosDesempeno.objects.filter(id_resultado_desempeno = idRespuestaEmpleadito).update(
                    resultado_preguntas = resultadoActualizado, estatus_resultado_preguntas = resultadoEstados,
                    estatus_resultado = "INICIADO"
                )

                mensajeNotificacion = "Se han guardado las respuestas correctamente! Continúe evaluando."
                

            if seccion == "segunda":
                pregunta6 = request.POST["pregunta6"]
                pregunta7 = request.POST["pregunta7"]
                pregunta8 = request.POST["pregunta8"]
                
                #Posiciones 5 a la 7

                arregloResultadoPreguntas = resultadoPreguntas.split(",") #[]
                arregloEsotadosPreguntas = estadoPreguntas.split(",")

                arregloResultadoPreguntas[5] = pregunta6
                arregloResultadoPreguntas[6] = pregunta7
                arregloResultadoPreguntas[7] = pregunta8

                arregloEsotadosPreguntas[5] = "c"
                arregloEsotadosPreguntas[6] = "c"
                arregloEsotadosPreguntas[7] = "c"

                resultadoActualizado = ""
                contador1 = 0
                resultadoEstados = ""
                contador2 = 0

                for respuesta in arregloResultadoPreguntas:
                    contador1 = contador1 + 1

                    if contador1 == 1:
                        resultadoActualizado = respuesta
                    else:
                        resultadoActualizado = resultadoActualizado + ","+respuesta

                for estado in arregloEsotadosPreguntas:
                    contador2 = contador2 + 1

                    if contador2 == 1:
                        resultadoEstados = estado
                    else:
                        resultadoEstados = resultadoEstados + ","+estado

                #Actualizacion
                actualizacion = ResultadosDesempeno.objects.filter(id_resultado_desempeno = idRespuestaEmpleadito).update(
                    resultado_preguntas = resultadoActualizado, estatus_resultado_preguntas = resultadoEstados,
                    estatus_resultado = "INICIADO"
                )

                mensajeNotificacion = "Se han guardado las respuestas correctamente! Continúe evaluando."

            if seccion == "tercera":
                pregunta9 = request.POST["pregunta9"]
                pregunta10 = request.POST["pregunta10"]
                pregunta11 = request.POST["pregunta11"]

                #Posiciones 8 a la 10

                arregloResultadoPreguntas = resultadoPreguntas.split(",") #[]
                arregloEsotadosPreguntas = estadoPreguntas.split(",")

                arregloResultadoPreguntas[8] = pregunta9
                arregloResultadoPreguntas[9] = pregunta10
                arregloResultadoPreguntas[10] = pregunta11

                arregloEsotadosPreguntas[8] = "c"
                arregloEsotadosPreguntas[9] = "c"
                arregloEsotadosPreguntas[10] = "c"

                resultadoActualizado = ""
                contador1 = 0
                resultadoEstados = ""
                contador2 = 0

                for respuesta in arregloResultadoPreguntas:
                    contador1 = contador1 + 1

                    if contador1 == 1:
                        resultadoActualizado = respuesta
                    else:
                        resultadoActualizado = resultadoActualizado + ","+respuesta

                for estado in arregloEsotadosPreguntas:
                    contador2 = contador2 + 1

                    if contador2 == 1:
                        resultadoEstados = estado
                    else:
                        resultadoEstados = resultadoEstados + ","+estado

                #Actualizacion
                actualizacion = ResultadosDesempeno.objects.filter(id_resultado_desempeno = idRespuestaEmpleadito).update(
                    resultado_preguntas = resultadoActualizado, estatus_resultado_preguntas = resultadoEstados,
                    estatus_resultado = "INICIADO"
                )

                mensajeNotificacion = "Se han guardado las respuestas correctamente! Continúe evaluando."

            if seccion == "cuarta":
                pregunta12 = request.POST["pregunta12"]
                pregunta13 = request.POST["pregunta13"]
                pregunta14 = request.POST["pregunta14"]
                pregunta15 = request.POST["pregunta15"]
                pregunta16 = request.POST["pregunta16"]

                #Posiciones 11 a la 15

                arregloResultadoPreguntas = resultadoPreguntas.split(",") #[]
                arregloEsotadosPreguntas = estadoPreguntas.split(",")

                arregloResultadoPreguntas[11] = pregunta12
                arregloResultadoPreguntas[12] = pregunta13
                arregloResultadoPreguntas[13] = pregunta14
                arregloResultadoPreguntas[14] = pregunta15
                arregloResultadoPreguntas[15] = pregunta16

                arregloEsotadosPreguntas[11] = "c"
                arregloEsotadosPreguntas[12] = "c"
                arregloEsotadosPreguntas[13] = "c"
                arregloEsotadosPreguntas[14] = "c"
                arregloEsotadosPreguntas[15] = "c"

                resultadoActualizado = ""
                contador1 = 0
                resultadoEstados = ""
                contador2 = 0

                for respuesta in arregloResultadoPreguntas:
                    contador1 = contador1 + 1

                    if contador1 == 1:
                        resultadoActualizado = respuesta
                    else:
                        resultadoActualizado = resultadoActualizado + ","+respuesta

                for estado in arregloEsotadosPreguntas:
                    contador2 = contador2 + 1

                    if contador2 == 1:
                        resultadoEstados = estado
                    else:
                        resultadoEstados = resultadoEstados + ","+estado

                #Actualizacion
                actualizacion = ResultadosDesempeno.objects.filter(id_resultado_desempeno = idRespuestaEmpleadito).update(
                    resultado_preguntas = resultadoActualizado, estatus_resultado_preguntas = resultadoEstados,
                    estatus_resultado = "INICIADO"
                )

                mensajeNotificacion = "Se han guardado las respuestas correctamente! Continúe evaluando."

            if seccion == "quinta":
                pregunta17 = request.POST["pregunta17"]
                pregunta18 = request.POST["pregunta18"]

                #Posiciones 16 a la 17

                arregloResultadoPreguntas = resultadoPreguntas.split(",") #[]
                arregloEsotadosPreguntas = estadoPreguntas.split(",")

                arregloResultadoPreguntas[16] = pregunta17
                arregloResultadoPreguntas[17] = pregunta18

                arregloEsotadosPreguntas[16] = "c"
                arregloEsotadosPreguntas[17] = "c"

                resultadoActualizado = ""
                contador1 = 0
                resultadoEstados = ""
                contador2 = 0

                for respuesta in arregloResultadoPreguntas:
                    contador1 = contador1 + 1

                    if contador1 == 1:
                        resultadoActualizado = respuesta
                    else:
                        resultadoActualizado = resultadoActualizado + ","+respuesta

                for estado in arregloEsotadosPreguntas:
                    contador2 = contador2 + 1

                    if contador2 == 1:
                        resultadoEstados = estado
                    else:
                        resultadoEstados = resultadoEstados + ","+estado

                #Actualizacion
                actualizacion = ResultadosDesempeno.objects.filter(id_resultado_desempeno = idRespuestaEmpleadito).update(
                    resultado_preguntas = resultadoActualizado, estatus_resultado_preguntas = resultadoEstados,
                    estatus_resultado = "INICIADO"
                )

                mensajeNotificacion = "Se han guardado las respuestas correctamente! Continúe evaluando."

            if seccion == "sexta":
                pregunta19 = request.POST["pregunta19"]
                pregunta20 = request.POST["pregunta20"]
                pregunta21 = request.POST["pregunta21"]

                #Posiciones 18 a la 20

                arregloResultadoPreguntas = resultadoPreguntas.split(",") #[]
                arregloEsotadosPreguntas = estadoPreguntas.split(",")

                arregloResultadoPreguntas[18] = pregunta19
                arregloResultadoPreguntas[19] = pregunta20
                arregloResultadoPreguntas[20] = pregunta21

                arregloEsotadosPreguntas[18] = "c"
                arregloEsotadosPreguntas[19] = "c"
                arregloEsotadosPreguntas[20] = "c"

                resultadoActualizado = ""
                contador1 = 0
                resultadoEstados = ""
                contador2 = 0

                for respuesta in arregloResultadoPreguntas:
                    contador1 = contador1 + 1

                    if contador1 == 1:
                        resultadoActualizado = respuesta
                    else:
                        resultadoActualizado = resultadoActualizado + ","+respuesta

                for estado in arregloEsotadosPreguntas:
                    contador2 = contador2 + 1

                    if contador2 == 1:
                        resultadoEstados = estado
                    else:
                        resultadoEstados = resultadoEstados + ","+estado

                #Actualizacion
                actualizacion = ResultadosDesempeno.objects.filter(id_resultado_desempeno = idRespuestaEmpleadito).update(
                    resultado_preguntas = resultadoActualizado, estatus_resultado_preguntas = resultadoEstados,
                    estatus_resultado = "INICIADO"
                )

                mensajeNotificacion = "Se han guardado las respuestas correctamente! Continúe evaluando."


            if seccion == "septima":
                pregunta22 = request.POST["pregunta22"]
                pregunta23 = request.POST["pregunta23"]
                pregunta24 = request.POST["pregunta24"]
                pregunta25 = request.POST["pregunta25"]

                #Posiciones 21 a la 24

                arregloResultadoPreguntas = resultadoPreguntas.split(",") #[]
                arregloEsotadosPreguntas = estadoPreguntas.split(",")

                arregloResultadoPreguntas[21] = pregunta22
                arregloResultadoPreguntas[22] = pregunta23
                arregloResultadoPreguntas[23] = pregunta24
                arregloResultadoPreguntas[24] = pregunta25

                arregloEsotadosPreguntas[21] = "c"
                arregloEsotadosPreguntas[22] = "c"
                arregloEsotadosPreguntas[23] = "c"
                arregloEsotadosPreguntas[24] = "c"


                resultadoActualizado = ""
                contador1 = 0
                resultadoEstados = ""
                contador2 = 0

                for respuesta in arregloResultadoPreguntas:
                    contador1 = contador1 + 1

                    if contador1 == 1:
                        resultadoActualizado = respuesta
                    else:
                        resultadoActualizado = resultadoActualizado + ","+respuesta

                for estado in arregloEsotadosPreguntas:
                    contador2 = contador2 + 1

                    if contador2 == 1:
                        resultadoEstados = estado
                    else:
                        resultadoEstados = resultadoEstados + ","+estado

                #Actualizacion
                actualizacion = ResultadosDesempeno.objects.filter(id_resultado_desempeno = idRespuestaEmpleadito).update(
                    resultado_preguntas = resultadoActualizado, estatus_resultado_preguntas = resultadoEstados,
                    estatus_resultado = "INICIADO"
                )

                mensajeNotificacion = "Se han guardado las respuestas correctamente! Continúe evaluando."


            if seccion == "octava":
                pregunta26 = request.POST["pregunta26"]
                pregunta27 = request.POST["pregunta27"]
                
                #Posiciones 25 a la 26

                arregloResultadoPreguntas = resultadoPreguntas.split(",") #[]
                arregloEsotadosPreguntas = estadoPreguntas.split(",")

                arregloResultadoPreguntas[25] = pregunta26
                arregloResultadoPreguntas[26] = pregunta27

                arregloEsotadosPreguntas[25] = "c"
                arregloEsotadosPreguntas[26] = "c"


                resultadoActualizado = ""
                contador1 = 0
                resultadoEstados = ""
                contador2 = 0

                for respuesta in arregloResultadoPreguntas:
                    contador1 = contador1 + 1

                    if contador1 == 1:
                        resultadoActualizado = respuesta
                    else:
                        resultadoActualizado = resultadoActualizado + ","+respuesta

                for estado in arregloEsotadosPreguntas:
                    contador2 = contador2 + 1

                    if contador2 == 1:
                        resultadoEstados = estado
                    else:
                        resultadoEstados = resultadoEstados + ","+estado

                #Actualizacion
                actualizacion = ResultadosDesempeno.objects.filter(id_resultado_desempeno = idRespuestaEmpleadito).update(
                    resultado_preguntas = resultadoActualizado, estatus_resultado_preguntas = resultadoEstados,
                    estatus_resultado = "INICIADO"
                )

                mensajeNotificacion = "Se han guardado las respuestas correctamente! Continúe evaluando."


            if seccion == "novena":
                pregunta28 = request.POST["pregunta28"]

                #Posiciones 27

                arregloResultadoPreguntas = resultadoPreguntas.split(",") #[]
                arregloEsotadosPreguntas = estadoPreguntas.split(",")

                arregloResultadoPreguntas[27] = pregunta28

                arregloEsotadosPreguntas[27] = "c"


                resultadoActualizado = ""
                contador1 = 0
                resultadoEstados = ""
                contador2 = 0

                for respuesta in arregloResultadoPreguntas:
                    contador1 = contador1 + 1

                    if contador1 == 1:
                        resultadoActualizado = respuesta
                    else:
                        resultadoActualizado = resultadoActualizado + ","+respuesta

                for estado in arregloEsotadosPreguntas:
                    contador2 = contador2 + 1

                    if contador2 == 1:
                        resultadoEstados = estado
                    else:
                        resultadoEstados = resultadoEstados + ","+estado

                #Actualizacion
                actualizacion = ResultadosDesempeno.objects.filter(id_resultado_desempeno = idRespuestaEmpleadito).update(
                    resultado_preguntas = resultadoActualizado, estatus_resultado_preguntas = resultadoEstados,
                    estatus_resultado = "INICIADO"
                )

                mensajeNotificacion = "Se han guardado las respuestas correctamente! Continúe evaluando."

            if seccion == "decima":
                pregunta29 = request.POST["pregunta29"]
                pregunta30 = request.POST["pregunta30"]
                pregunta31 = request.POST["pregunta31"]

                #Posiciones 28 a la 30

                arregloResultadoPreguntas = resultadoPreguntas.split(",") #[]
                arregloEsotadosPreguntas = estadoPreguntas.split(",")

                arregloResultadoPreguntas[28] = pregunta29
                arregloResultadoPreguntas[29] = pregunta30
                arregloResultadoPreguntas[30] = pregunta31

                arregloEsotadosPreguntas[28] = "c"
                arregloEsotadosPreguntas[29] = "c"
                arregloEsotadosPreguntas[30] = "c"


                resultadoActualizado = ""
                contador1 = 0
                resultadoEstados = ""
                contador2 = 0

                for respuesta in arregloResultadoPreguntas:
                    contador1 = contador1 + 1

                    if contador1 == 1:
                        resultadoActualizado = respuesta
                    else:
                        resultadoActualizado = resultadoActualizado + ","+respuesta

                for estado in arregloEsotadosPreguntas:
                    contador2 = contador2 + 1

                    if contador2 == 1:
                        resultadoEstados = estado
                    else:
                        resultadoEstados = resultadoEstados + ","+estado

                #Actualizacion
                actualizacion = ResultadosDesempeno.objects.filter(id_resultado_desempeno = idRespuestaEmpleadito).update(
                    resultado_preguntas = resultadoActualizado, estatus_resultado_preguntas = resultadoEstados,
                    estatus_resultado = "INICIADO"
                )

                mensajeNotificacion = "Se han guardado las respuestas correctamente! Continúe evaluando."

            if seccion == "onceava":
                pregunta32 = request.POST["pregunta32"]
                pregunta33 = request.POST["pregunta33"]
                pregunta34 = request.POST["pregunta34"]
                pregunta35 = request.POST["pregunta35"]
                pregunta36 = request.POST["pregunta36"]
                pregunta37 = request.POST["pregunta37"]
                pregunta38 = request.POST["pregunta38"]
                pregunta39 = request.POST["pregunta39"]
                pregunta40 = request.POST["pregunta40"]
                pregunta41 = request.POST["pregunta41"]
                pregunta42 = request.POST["pregunta42"]

                #Posiciones 31 a la 41

                arregloResultadoPreguntas = resultadoPreguntas.split(",") #[]
                arregloEsotadosPreguntas = estadoPreguntas.split(",")

                arregloResultadoPreguntas[31] = pregunta32
                arregloResultadoPreguntas[32] = pregunta33
                arregloResultadoPreguntas[33] = pregunta34
                arregloResultadoPreguntas[34] = pregunta35
                arregloResultadoPreguntas[35] = pregunta36
                arregloResultadoPreguntas[36] = pregunta37
                arregloResultadoPreguntas[37] = pregunta38
                arregloResultadoPreguntas[38] = pregunta39
                arregloResultadoPreguntas[39] = pregunta40
                arregloResultadoPreguntas[40] = pregunta41
                arregloResultadoPreguntas[41] = pregunta42

                arregloEsotadosPreguntas[31] = "c"
                arregloEsotadosPreguntas[32] = "c"
                arregloEsotadosPreguntas[33] = "c"
                arregloEsotadosPreguntas[34] = "c"
                arregloEsotadosPreguntas[35] = "c"
                arregloEsotadosPreguntas[36] = "c"
                arregloEsotadosPreguntas[37] = "c"
                arregloEsotadosPreguntas[38] = "c"
                arregloEsotadosPreguntas[39] = "c"
                arregloEsotadosPreguntas[40] = "c"
                arregloEsotadosPreguntas[41] = "c"


                resultadoActualizado = ""
                contador1 = 0
                resultadoEstados = ""
                contador2 = 0

                for respuesta in arregloResultadoPreguntas:
                    contador1 = contador1 + 1

                    if contador1 == 1:
                        resultadoActualizado = respuesta
                    else:
                        resultadoActualizado = resultadoActualizado + ","+respuesta

                for estado in arregloEsotadosPreguntas:
                    contador2 = contador2 + 1

                    if contador2 == 1:
                        resultadoEstados = estado
                    else:
                        resultadoEstados = resultadoEstados + ","+estado

                fechaTerminacion = datetime.now()
                #Actualizacion
                actualizacion = ResultadosDesempeno.objects.filter(id_resultado_desempeno = idRespuestaEmpleadito).update(
                    resultado_preguntas = resultadoActualizado, estatus_resultado_preguntas = resultadoEstados,
                    estatus_resultado = "FINALIZADO", fecha_terminacion = fechaTerminacion
                )

                #aCTUALIZAR DATO DE INDICADOR EVALUADOR..

                consultaEvaluador = IndicadorEvaluador.objects.filter(id_indicador_evaluador = indicadorEvaluador)

                for datoEvaluador in consultaEvaluador:
                    empleadosEvaluados = datoEvaluador.empleados_evaluados
                    estatusEmpleadosEvaluados = datoEvaluador.estatus_empleados_evaluador

                print(empleadosEvaluados)
                print(estatusEmpleadosEvaluados)

                arrayEmpleados = empleadosEvaluados.split(",")
                arrayEstatusEmpleadosEvaluados = estatusEmpleadosEvaluados.split(",")

                estatusActualizados = ""

                posicion = 0
                for empleado in arrayEmpleados:
                    intEmpleado = int(empleado)
                    posicion = posicion +1

                    if idEmpleadoEvaluado == intEmpleado:
                        arrayEstatusEmpleadosEvaluados[posicion-1] = "F"

                contador3 = 0
                for estatus in arrayEstatusEmpleadosEvaluados:
                    contador3 = contador3 + 1

                    if contador3 == 1:
                        estatusActualizados = estatus

                    else:
                        estatusActualizados = estatusActualizados + "," + estatus

                actualizacionEstatusEmpleado = IndicadorEvaluador.objects.filter(id_indicador_evaluador = indicadorEvaluador).update(
                    estatus_empleados_evaluador = estatusActualizados
                )

                if "P" in arrayEstatusEmpleadosEvaluados:
                    aunTienePendientes = True
                else:
                    actualizacionEstatusEmpleado = IndicadorEvaluador.objects.filter(id_indicador_evaluador = indicadorEvaluador).update(
                    estatus_general = "FINALIZADO"
                )

                mensajeNotificacion = "Has terminado la evaluación! Realizar evaluaciones de otros empleados."


            
            request.session["respuestaGuardada"] = mensajeNotificacion
           


                


            return redirect('/verMisEvaluaciones/')

    
    else:
        return redirect('/login/')



def verResultadosEmpleadoEvaluado(request):
    if "idSesion" in request.session:
        estaEnVerEvaluaciones = True
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        if correo == "almacen01@customco.com.mx":
            almacen = True
        else:
            almacen = False

        if correo == "recursos.humanos@customco.com.mx":
            rh = True
        else:
            rh = False

        nombreCompleto = nombre + " " + apellidos
        
        foto = fotoAdmin(request)
        
        empleado = Empleados.objects.filter(id_empleado = id_admin)
        for dato in empleado:
            area = dato.id_area_id


        administradordeVehiculos = False
        solicitantePrestamo = False

        if area == 1 or area ==5 or area == 7 or area == 8 or area == 9 or area == 10:
            if area == 5:
                solicitantePrestamo = True
                administradordeVehiculos = True
            else:
                solicitantePrestamo = True

        else:
            solicitantePrestamo = False
            administradordeVehiculos = False


        #Aqui empieza lo de las evaluaciones

        if request.method == "POST":
            idEmpleado = request.POST["idEmpleado"]
            idAsignacionEvaluador = request.POST["idAsignacionEvaluador"]

            #Datos de evaluacion 
            consultaIndicadorEvaluador = IndicadorEvaluador.objects.filter(id_indicador_evaluador = idAsignacionEvaluador)
            
            for datoIndicador in consultaIndicadorEvaluador:
                idEvaluacionDesempeno = datoIndicador.evaluacion_desempeno_id
                empleadoEvaluador = datoIndicador.empleado_evaluador_id

            consultaEvaluacion = EvaluacionesDesempeno.objects.filter(id_evaluacion_desempeno = idEvaluacionDesempeno)

            for datoEvaluacion in consultaEvaluacion:
                nombreEvaluacion = datoEvaluacion.nombre_evaluacion

            #Datos evaluador

            consultaEvaluador = Empleados.objects.filter(id_empleado = empleadoEvaluador)

            for datoEmpleado in consultaEvaluador:
                nombreEmpleado = datoEmpleado.nombre
                apellidosEmpleado = datoEmpleado.apellidos

            nombreCompletoEmpleadoEvaluador = nombreEmpleado + " "+apellidosEmpleado

            #Datos empleado evaluado
            consultaEmpleadoEvaluado = Empleados.objects.filter(id_empleado = idEmpleado)
            for datoEmpleado in consultaEmpleadoEvaluado:
                nombreEmpleadoEvaluado = datoEmpleado.nombre
                apellidosEmpleadoEvaluado = datoEmpleado.apellidos

            nombreCompletoEmpleadoEvaluado = nombreEmpleadoEvaluado + " " + apellidosEmpleadoEvaluado



            consultaRespuestas = ResultadosDesempeno.objects.filter(indicador_evaluador_id__id_indicador_evaluador = idAsignacionEvaluador, 
            id_empleado_evaluado_id__id_empleado = idEmpleado)

            for datoRespuesta in consultaRespuestas:
                fechaTermino = datoRespuesta.fecha_terminacion
                respuestas = datoRespuesta.resultado_preguntas

            
            resultadosPreguntas = respuestas.split(",")

            contadorUnos = 0
            contadorDoses = 0
            contadorTreses = 0
            contadorCuatros = 0
            contadorCincos = 0

            for respuesta in resultadosPreguntas:
                if respuesta == "1":
                    contadorUnos = contadorUnos + 1
                if respuesta == "2":
                    contadorDoses = contadorDoses + 1
                if respuesta == "3":
                    contadorTreses = contadorTreses + 1
                if respuesta == "4":
                    contadorCuatros = contadorCuatros + 1
                if respuesta == "5":
                    contadorCincos = contadorCincos + 1

            
            contadorUnosFinal = contadorUnos

            contadorDosesFinal = contadorDoses * 2

            contadorTresesFinal = contadorTreses * 3

            contadorCuatrosFinal = contadorCuatros * 4

            contadorCincosFinal = contadorCincos * 5

            sumaTotalPuntaje = contadorUnosFinal + contadorDosesFinal + contadorTresesFinal + contadorCuatrosFinal + contadorCincosFinal
            
            resultadoEvaluacion = ""

            if sumaTotalPuntaje >= 160 and sumaTotalPuntaje <= 199:
                resultadoEvaluacion = "sobresaliente"
            elif sumaTotalPuntaje >= 120 and sumaTotalPuntaje <= 159:
                resultadoEvaluacion = "excelente"
            elif sumaTotalPuntaje >= 80 and sumaTotalPuntaje <= 119:
                resultadoEvaluacion = "bueno"
            elif sumaTotalPuntaje >= 43 and sumaTotalPuntaje <= 79:
                resultadoEvaluacion = "necesitaMejorar"
            elif sumaTotalPuntaje >= 0 and sumaTotalPuntaje <= 42:
                resultadoEvaluacion = "noSatisfactoria"

        

        return render(request,"empleadosCustom/Evaluaciones/verResultadosEmpleadoEvaluado.html",{"estaEnVerEvaluaciones":estaEnVerEvaluaciones,"id_admin":id_admin,"nombre":nombre,"apellidos":apellidos,"correo":correo,"nombreCompleto":nombreCompleto,"solicitantePrestamo":solicitantePrestamo,"almacen":almacen,"foto":foto, "administradordeVehiculos":administradordeVehiculos, "rh":rh,
        "nombreEvaluacion":nombreEvaluacion, "nombreCompletoEmpleadoEvaluador":nombreCompletoEmpleadoEvaluador,
        "nombreCompletoEmpleadoEvaluado":nombreCompletoEmpleadoEvaluado, "fechaTermino":fechaTermino, "sumaTotalPuntaje":sumaTotalPuntaje,
        "resultadoEvaluacion":resultadoEvaluacion})

    
    else:
        return redirect('/login/')




def resultadosEvaluacionDesempeno(request):
    
    #Si ya hay una sesión iniciada..
    if "idSesion" in request.session:

        evaluacionDesempeno = request.POST["evaluacionDesempeno"]

        consultaEvaluacion = EvaluacionesDesempeno.objects.filter(id_evaluacion_desempeno = evaluacionDesempeno)

        for dato in consultaEvaluacion:
            nombreEvaluacion = dato.nombre_evaluacion


       #crear el http response con pdf
        respuesta = HttpResponse(content_type='application/pdf')
        respuesta['Content-Disposition'] = 'attachment; filename=Respuestas '+nombreEvaluacion+'.pdf'
        #Crear objeto PDF 
        buffer =BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        
        contadorHojas = 0

        for x in range(2):
            contadorHojas = contadorHojas + 1

            if contadorHojas == 1:
                base_dir = str(settings.BASE_DIR) #C:\Users\AuxSistemas\Desktop\CS Escritorio\Custom-System\djangoCS
                #nombre de empresa
                logo = base_dir+'/static/images/logoCustom.PNG'   
                c.drawImage(logo, 40,700,120,70, preserveAspectRatio=True)
                    
                c.setFont('Helvetica-Bold', 14)
                c.drawString(150,750, 'Custom & Co S.A. de C.V.')
                    
                c.setFont('Helvetica', 8)
                c.drawString(150,735, 'Allende #646 Sur Colonia Centro, Durango, CP: 35000')
                    
                c.setFont('Helvetica', 8)
                c.drawString(150,720, 'RFC: CAC070116IS9')
                    
                c.setFont('Helvetica', 8)
                c.drawString(150,705, 'Tel: 8717147716')
                #fecha
                hoy=datetime.now()
                fecha = str(hoy.date())
                color_guinda="#B03A2E"
                color_azul = "#cf1515"
                c.setFillColor(color_guinda)
                
                    
                c.setFont('Helvetica-Bold', 12)
                c.drawString(360,750, "RESULTADOS EVALUACIÓN DESEMPEÑO")
                color_negro="#030305"
                c.setFillColor(color_negro)
                c.setFont('Helvetica-Bold', 10)
                c.drawString(405,730, "Fecha de impresión: " +fecha)
                #linea guinda
                    
                c.setFillColor(color_guinda)
                c.setStrokeColor(color_guinda)
                c.line(40,695,560,695)
                #nombre departamento
                color_negro="#030305"
                c.setFillColor(color_negro)
                c.setFont('Helvetica', 12)
                c.drawString(405,710, 'Departamento de Sistemas')
                #titulo
                c.setFont('Helvetica-Bold', 22)
                    
                c.drawString(55,660, 'Resultados '+nombreEvaluacion)


                #tabla1
                c.setFont('Helvetica-Bold', 18)
                c.drawString(215,620, 'Criterios de Evaluación')


                #header de tabla
                styles = getSampleStyleSheet()
                styleBH =styles["Normal"]
                styleBH.alignment = TA_CENTER
                styleBH.fontSize = 10
                
                
                rango = Paragraph('''Rango puntaje''', styleBH)
                criterio = Paragraph('''Criterio''', styleBH)
            
            
                filasTabla=[]
                filasTabla.append([rango, criterio])
                #Tabla
                styleN = styles["BodyText"]
                styleN.alignment = TA_CENTER
                styleN.fontSize = 7
                
                high = 590
                porcentajes = ["199 - 160", "159 - 120", "119 - 80","79 - 43", "42 - 0" ]
                criterios = ["Sobresaliente", "Excelente", "Bueno", "Necesita mejorar", "No satisfactorio"]
                
                contador = 0
                for x in porcentajes:
                    if contador == 0:
                        fila = [porcentajes[contador], criterios[contador]]
                        contador= 1

                    elif contador != 0:
                        fila = [porcentajes[contador], criterios[contador]]
                        contador= contador+1
                    filasTabla.append(fila)
                    high= high - 18 
                    
                #escribir tabla
                width, height = letter
                tabla = Table(filasTabla, colWidths=[4 * cm, 4 * cm])
                
                tabla.setStyle(TableStyle([
                
                    ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                    ('BACKGROUND', (0, 0), (-1, 0), '#e9c7ae'),
                    
                    ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                    ('BACKGROUND', (1,1), (-1,-5), '#4CAF50'),
                    ('BACKGROUND', (1,2), (-1,-4), '#2196F3'),
                    ('BACKGROUND', (1,3), (-1,-3), '#FFC107'),
                    ('BACKGROUND', (1,4), (-1,-2), '#FF5722'),
                    ('BACKGROUND', (1,5), (-1,-1), '#F44336'),
                ]))

                tabla.wrapOn(c, width, height)
                tabla.drawOn(c, 200, high)

                #tabla2

                c.setFont('Helvetica-Bold', 18)
                c.drawString(215,465, 'Empleados evaluadores')

                #header de tabla
                styles = getSampleStyleSheet()
                styleBH =styles["Normal"]
                styleBH.alignment = TA_CENTER
                styleBH.fontSize = 10
                
                
                rango = Paragraph('''Evaluador''', styleBH)
                criterio = Paragraph('''Departamento''', styleBH)
            
            
                filasTabla=[]
                filasTabla.append([rango, criterio])
                #Tabla
                styleN = styles["BodyText"]
                styleN.alignment = TA_CENTER
                styleN.fontSize = 7
                
                highEvaluadores = 430
                
                #OBTENER LISTA DE EMPLEADOS EVALUADORES Y SUS DEPARTAMENTOS
                consultaEvaluadores = IndicadorEvaluador.objects.filter(evaluacion_desempeno_id__id_evaluacion_desempeno = evaluacionDesempeno)


                for evaluador in consultaEvaluadores:
                    idEmpleadoEvaluador = evaluador.empleado_evaluador_id

                    consultaEmpleado = Empleados.objects.filter(id_empleado = idEmpleadoEvaluador)

                    for datoEmpleado in consultaEmpleado:
                        nombreEmpleadoEvaluador = datoEmpleado.nombre
                        apellidoEmpleadoEvaluador = datoEmpleado.apellidos

                        idArea = datoEmpleado.id_area_id

                    nombreCompletoEvaluador = nombreEmpleadoEvaluador + " " +apellidoEmpleadoEvaluador

                    consultaArea = Areas.objects.filter(id_area = idArea)

                    for datoArea in consultaArea:
                        nombreDepartamento = datoArea.nombre

                    
                    filasTabla.append([nombreCompletoEvaluador, nombreDepartamento])
                    highEvaluadores = highEvaluadores - 18 




                #escribir tabla
                width, height = letter
                tablaEvaluadores = Table(filasTabla, colWidths=[8 * cm, 4 * cm])
                
                tablaEvaluadores.setStyle(TableStyle([
                
                    ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                    ('BACKGROUND', (0, 0), (-1, 0), '#FFB100'),
                    
                    ('BOX', (0, 0), (-1, -1), 0.25, colors.black)
                ]))

                tablaEvaluadores.wrapOn(c, width, height)
                tablaEvaluadores.drawOn(c, 150, highEvaluadores)

                




                #linea guinda
                color_guinda="#B03A2E"
                c.setFillColor(color_guinda)
                c.setStrokeColor(color_guinda)
                c.line(40,60,560,60)
                
                color_negro="#030305"
                c.setFillColor(color_negro)
                c.setFont('Helvetica-Bold', 11)
                c.drawString(170,48, '2021 - Administrador de Custom System. - Versión: 1.0.0 ')
                
                
                c.showPage()

            if contadorHojas == 2:
                base_dir = str(settings.BASE_DIR) #C:\Users\AuxSistemas\Desktop\CS Escritorio\Custom-System\djangoCS
                #nombre de empresa
                logo = base_dir+'/static/images/logoCustom.PNG'   
                c.drawImage(logo, 40,700,120,70, preserveAspectRatio=True)
                    
                c.setFont('Helvetica-Bold', 14)
                c.drawString(150,750, 'Custom & Co S.A. de C.V.')
                    
                c.setFont('Helvetica', 8)
                c.drawString(150,735, 'Allende #646 Sur Colonia Centro, Durango, CP: 35000')
                    
                c.setFont('Helvetica', 8)
                c.drawString(150,720, 'RFC: CAC070116IS9')
                    
                c.setFont('Helvetica', 8)
                c.drawString(150,705, 'Tel: 8717147716')
                #fecha
                hoy=datetime.now()
                fecha = str(hoy.date())
                color_guinda="#B03A2E"
                color_azul = "#cf1515"
                c.setFillColor(color_guinda)
                
                    
                c.setFont('Helvetica-Bold', 12)
                c.drawString(360,750, "RESULTADOS EVALUACIÓN DESEMPEÑO")
                color_negro="#030305"
                c.setFillColor(color_negro)
                c.setFont('Helvetica-Bold', 10)
                c.drawString(405,730, "Fecha de impresión: " +fecha)
                #linea guinda
                    
                c.setFillColor(color_guinda)
                c.setStrokeColor(color_guinda)
                c.line(40,695,560,695)
                #nombre departamento
                color_negro="#030305"
                c.setFillColor(color_negro)
                c.setFont('Helvetica', 12)
                c.drawString(405,710, 'Departamento de Sistemas')
                #titulo
                c.setFont('Helvetica-Bold', 22)
                    
                c.drawString(55,660, 'Resultados '+nombreEvaluacion)


                #TABLAAAAAAAAAAAAAAAAAAAAAAAA

                

                c.setFont('Helvetica-Bold', 20)
                c.drawString(195,620, 'Resultados de empleados')

                #Aqui se empieza a formar, por cada evaluador, sacar los evaluados

                consultaEvaluadores = IndicadorEvaluador.objects.filter(evaluacion_desempeno_id__id_evaluacion_desempeno = evaluacionDesempeno)

                highTabla = 0
                contador = 0

                #Creación de la tabla
                styles = getSampleStyleSheet()
                styleBH =styles["Normal"]
                styleBH.alignment = TA_CENTER
                styleBH.fontSize = 10
                
                
                evaluado = Paragraph('''Evaluado''', styleBH)
                evaluadorTabla = Paragraph('''Evaluador''', styleBH)
                puntaje = Paragraph('''Puntaje''', styleBH)
                valor = Paragraph('''Valor''', styleBH)
            
            
                filasTabla=[]
                filasTabla.append([evaluado,evaluadorTabla, puntaje, valor])
                #Tabla
                styleN = styles["BodyText"]
                styleN.alignment = TA_CENTER
                styleN.fontSize = 7
                
                highTabla = 590


                for evaluador in consultaEvaluadores:


                    idIndicador = evaluador.id_indicador_evaluador

                    idEmpleadoEvaluador = evaluador.empleado_evaluador_id

                    consultaEmpleado = Empleados.objects.filter(id_empleado = idEmpleadoEvaluador)

                    for datoEmpleado in consultaEmpleado:
                        nombreEmpleadoEvaluador = datoEmpleado.nombre
                        apellidoEmpleadoEvaluador = datoEmpleado.apellidos

                    nombreCompletoEvaluador = nombreEmpleadoEvaluador + " " +apellidoEmpleadoEvaluador

                    #empleados evaluados
                    consultaEmpleadosEvaluados = ResultadosDesempeno.objects.filter(indicador_evaluador_id__id_indicador_evaluador = idIndicador)
                    
                    for respuestita in consultaEmpleadosEvaluados:
                        idEmpleado = respuestita.id_empleado_evaluado_id

                        #consultar nombre empleado
                        consultaEmpleadoEvaluado = Empleados.objects.filter(id_empleado = idEmpleado)
                        for datoEmpleado in consultaEmpleadoEvaluado:
                            nombreEmpleadoEvaluado = datoEmpleado.nombre
                            apellidosEmpleadoEvaluado = datoEmpleado.apellidos

                        nombreCompletoEmpleadoEvaluado = nombreEmpleadoEvaluado + " " + apellidosEmpleadoEvaluado

                        #Sacar resultado de puntaje
                        estatusRespuestas = respuestita.estatus_resultado

                        if estatusRespuestas == "FINALIZADO":
                            respuestas = respuestita.resultado_preguntas
                            resultadosPreguntas = respuestas.split(",")

                            contadorUnos = 0
                            contadorDoses = 0
                            contadorTreses = 0
                            contadorCuatros = 0
                            contadorCincos = 0

                            for respuestaa in resultadosPreguntas:
                                if respuestaa == "1":
                                    contadorUnos = contadorUnos + 1
                                if respuestaa == "2":
                                    contadorDoses = contadorDoses + 1
                                if respuestaa == "3":
                                    contadorTreses = contadorTreses + 1
                                if respuestaa == "4":
                                    contadorCuatros = contadorCuatros + 1
                                if respuestaa == "5":
                                    contadorCincos = contadorCincos + 1

                            
                            contadorUnosFinal = contadorUnos

                            contadorDosesFinal = contadorDoses * 2

                            contadorTresesFinal = contadorTreses * 3

                            contadorCuatrosFinal = contadorCuatros * 4

                            contadorCincosFinal = contadorCincos * 5

                            sumaTotalPuntaje = contadorUnosFinal + contadorDosesFinal + contadorTresesFinal + contadorCuatrosFinal + contadorCincosFinal
                            
                            resultadoEvaluacion = ""

                            if sumaTotalPuntaje >= 160 and sumaTotalPuntaje <= 199:
                                resultadoEvaluacion = "Sobresaliente"
                            elif sumaTotalPuntaje >= 120 and sumaTotalPuntaje <= 159:
                                resultadoEvaluacion = "Excelente"
                            elif sumaTotalPuntaje >= 80 and sumaTotalPuntaje <= 119:
                                resultadoEvaluacion = "Bueno"
                            elif sumaTotalPuntaje >= 43 and sumaTotalPuntaje <= 79:
                                resultadoEvaluacion = "Nececita Mejorar"
                            elif sumaTotalPuntaje >= 0 and sumaTotalPuntaje <= 42:
                                resultadoEvaluacion = "No Satisfactorio"

                            stringPuntaje = str(sumaTotalPuntaje)
                            filasTabla.append([nombreCompletoEmpleadoEvaluado,nombreCompletoEvaluador, stringPuntaje, resultadoEvaluacion])
                            highTabla = highTabla - 18 



                        else:
                            sumaTotalPuntaje = "PENDIENTE"
                            resultadoEvaluacion = "PENDIENTE"
                            filasTabla.append([nombreCompletoEmpleadoEvaluado,nombreCompletoEvaluador, sumaTotalPuntaje, resultadoEvaluacion])
                            highTabla = highTabla - 18

                    
                #escribir tabla
                width, height = letter
                tablaEvaluadores = Table(filasTabla, colWidths=[6 * cm, 6 * cm, 4 * cm,  4 * cm])
                
                tablaEvaluadores.setStyle(TableStyle([
                
                    ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                    ('BACKGROUND', (0, 0), (-1, 0), '#3C79F5'),
                    
                    ('BOX', (0, 0), (-1, -1), 0.25, colors.black)
                ]))

                tablaEvaluadores.wrapOn(c, width, height)
                tablaEvaluadores.drawOn(c, 25, highTabla)




                




                #linea guinda
                color_guinda="#B03A2E"
                c.setFillColor(color_guinda)
                c.setStrokeColor(color_guinda)
                c.line(40,60,560,60)
                
                color_negro="#030305"
                c.setFillColor(color_negro)
                c.setFont('Helvetica-Bold', 11)
                c.drawString(170,48, '2021 - Administrador de Custom System. - Versión: 1.0.0 ')
                
                
                c.showPage()
        
        
        
        #guardar pdf
        c.save()
        #obtener valores de bytesIO y esribirlos en la respuesta
        pdf = buffer.getvalue()
        buffer.close()
        respuesta.write(pdf)
        return respuesta


        
    #Si le da al inicio y no hay una sesión iniciada..
    else:
        return redirect('/login/') #redirecciona a url de inicio

def registroEntrada(request):
    
    if "registroEntrada" in request.session:
        registroEntrada = request.session["registroEntrada"]
        del request.session["registroEntrada"]

        return render(request,"Checador/registrarEntrada.html",{"registroEntrada":registroEntrada})
    
    if "registroSalida" in request.session:
        registroSalida = request.session["registroSalida"]
        del request.session["registroSalida"]

        return render(request,"Checador/registrarEntrada.html",{"registroSalida":registroSalida})
    

    if "errorAsistencia" in request.session:
        errorAsistencia = request.session["errorAsistencia"]
        del request.session["errorAsistencia"]

        return render(request,"Checador/registrarEntrada.html",{"errorAsistencia":errorAsistencia})

    return render(request,"Checador/registrarEntrada.html")

def altaEmpleadosChecador(request):

    if "idSesion" in request.session:
        estaEnChecador = True
        estaEnAltaEmpleadosChecador = True
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        if correo == "almacen01@customco.com.mx":
            almacen = True
        else:
            almacen = False

        if correo == "recursos.humanos@customco.com.mx":
            rh = True
        else:
            rh = False

        nombreCompleto = nombre + " " + apellidos
        
        foto = fotoAdmin(request)
        
        #Aqui empieza todo..
        consultaCarasActivos = EmpleadosCara.objects.filter(cara_activa="S")
        listaEmpleadosSinCaraRegistrada = []

        if consultaCarasActivos:
            
            listaIdsEmpleadosActivos = []
            consultaEmpleadosActivos = Empleados.objects.filter(activo="A", correo__icontains="@customco.com.mx")

            for empleadoActivo in consultaEmpleadosActivos:
                idEmpleado = empleadoActivo.id_empleado

                listaIdsEmpleadosActivos.append(idEmpleado)

            

            for empleadoConCara in consultaCarasActivos:
                idEmpleadoCara = empleadoConCara.id_empleado_id


                if idEmpleadoCara in listaIdsEmpleadosActivos:
                    listaIdsEmpleadosActivos.remove(idEmpleadoCara) 

            

            for empleadoSinCara in listaIdsEmpleadosActivos:
                idEmpleado = int(empleadoSinCara)

                consultaEmpleado = Empleados.objects.filter(id_empleado = idEmpleado)

                for empleadoActivo in consultaEmpleado:
                    nombreCompleto = empleadoActivo.nombre +" "+ empleadoActivo.apellidos
                    areaEmpleado = empleadoActivo.id_area_id
                    consultaEmpleadoArea = Areas.objects.filter(id_area = areaEmpleado)

                    for empleadoArea in consultaEmpleadoArea:

                        nombreDepartamento = empleadoArea.nombre

                    listaEmpleadosSinCaraRegistrada.append([idEmpleado, nombreCompleto,nombreDepartamento])
        else:
            consultaEmpleadosActivos = Empleados.objects.filter(activo="A", correo__icontains="@customco.com.mx")

            for empleadoActivo in consultaEmpleadosActivos:
                idEmpleado = empleadoActivo.id_empleado
                nombreCompleto = empleadoActivo.nombre +" "+ empleadoActivo.apellidos
                areaEmpleado = empleadoActivo.id_area_id
                consultaEmpleadoArea = Areas.objects.filter(id_area = areaEmpleado)

                for empleadoArea in consultaEmpleadoArea:

                    nombreDepartamento = empleadoArea.nombre

                listaEmpleadosSinCaraRegistrada.append([idEmpleado, nombreCompleto,nombreDepartamento])


        if "caraGuardada" in request.session:
            caraGuardada = request.session["caraGuardada"]
            del request.session["caraGuardada"]

            return render(request,"empleadosCustom/Asistencia/Checador/altaEmpleadosChecador.html",{"estaEnChecador":estaEnChecador,"estaEnAltaEmpleadosChecador":estaEnAltaEmpleadosChecador,"id_admin":id_admin,"nombre":nombre,"apellidos":apellidos,"correo":correo,"nombreCompleto":nombreCompleto,"almacen":almacen,"foto":foto, "rh":rh, "listaEmpleadosSinCaraRegistrada": listaEmpleadosSinCaraRegistrada,
                                                                                                    "caraGuardada":caraGuardada})

        if "caraNoGuardada" in request.session:
            caraNoGuardada = request.session["caraNoGuardada"]
            del request.session["caraNoGuardada"]

            return render(request,"empleadosCustom/Asistencia/Checador/altaEmpleadosChecador.html",{"estaEnChecador":estaEnChecador,"estaEnAltaEmpleadosChecador":estaEnAltaEmpleadosChecador,"id_admin":id_admin,"nombre":nombre,"apellidos":apellidos,"correo":correo,"nombreCompleto":nombreCompleto,"almacen":almacen,"foto":foto, "rh":rh, "listaEmpleadosSinCaraRegistrada": listaEmpleadosSinCaraRegistrada,
                                                                                                    "caraNoGuardada":caraNoGuardada})
        

        return render(request,"empleadosCustom/Asistencia/Checador/altaEmpleadosChecador.html",{"estaEnChecador":estaEnChecador,"estaEnAltaEmpleadosChecador":estaEnAltaEmpleadosChecador,"id_admin":id_admin,"nombre":nombre,"apellidos":apellidos,"correo":correo,"nombreCompleto":nombreCompleto,"almacen":almacen,"foto":foto, "rh":rh, "listaEmpleadosSinCaraRegistrada": listaEmpleadosSinCaraRegistrada})

    
    else:
        return redirect('/login/')



def verEmpleadosChecador(request):
    if "idSesion" in request.session:
        estaEnChecador = True
        estaEnVerEmpleadosChecador = True
        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        if correo == "almacen01@customco.com.mx":
            almacen = True
        else:
            almacen = False

        if correo == "recursos.humanos@customco.com.mx":
            rh = True
        else:
            rh = False

        nombreCompleto = nombre + " " + apellidos
        
        foto = fotoAdmin(request)

        #Aqui se empieza
        
        #Obtener datos para tabla

        empleadosConNfc = []

        consultaEmpleadosConNFC = RelacionNFCEmpleado.objects.all()

        for empleado in consultaEmpleadosConNFC:
            
            idAsignacion = empleado.id_relacion
            
            nfcAsignado = empleado.uid_nfc

            idEmpleado = empleado.id_empleado_id

            consultaEmpleado = Empleados.objects.filter(id_empleado = idEmpleado)

            for datoEmpleado in consultaEmpleado:
                nombreEmpleado = datoEmpleado.nombre
                apellidosEmpleado = datoEmpleado.apellidos

                idArea = datoEmpleado.id_area_id


                consultaArea = Areas.objects.filter(id_area = idArea)
                for datoArea in consultaArea:
                    nombreArea = datoArea.nombre
                    colorArea = datoArea.color

                nombreCompletoEmpleado = nombreEmpleado + " " + apellidosEmpleado
            
            empleadosConNfc.append([idAsignacion, nfcAsignado, nombreCompletoEmpleado, nombreArea, colorArea])



        
        return render(request,"empleadosCustom/Asistencia/Checador/verEmpleadosChecador.html",{"estaEnChecador":estaEnChecador,"estaEnVerEmpleadosChecador":estaEnVerEmpleadosChecador ,"id_admin":id_admin,"nombre":nombre,"apellidos":apellidos,"correo":correo,"nombreCompleto":nombreCompleto,"almacen":almacen,"foto":foto, "rh":rh,
                                                                                               "empleadosConNfc":empleadosConNfc})

    
    else:
        return redirect('/login/')

def escaneoDeCara(request):
    if "idSesion" in request.session:

        idEmpleadoRegistrarCara = request.POST['idEmpleado']

        # try:

        faceRecognition.faceDetect(idEmpleadoRegistrarCara)
        faceRecognition.trainFace()

        #Guardar en la BD.
        registroCara = EmpleadosCara(id_empleado = Empleados.objects.get(id_empleado = idEmpleadoRegistrarCara),
                                        cara_registrada = "S", cara_activa = "S")

        registroCara.save()


        request.session["caraGuardada"] = 'Se ha registrado y entrenado el rostro correctamente!'
        #except:
            #request.session["caraNoGuardada"] = 'Ha ocurrido un error, favor de hablar con soporte!'

        return redirect('/altaEmpleadosChecador/')

        
    else:
        return redirect('/login/')

def registrarEntradaEmpleado(request):

    
    try:
        #Registrar asistencia
        fecha = datetime.now()

        face_id = faceRecognition.recognizeFace()
        print(face_id)

        intIdEmpleado = int(face_id)

        print(" ID DE EMPLEADO ESCANEADO ENTRADA = "+str(face_id))

        
        
        

        
        hora = fecha.hour
        minuto = fecha.minute
        segundos = fecha.second

        anio = fecha.year
        mes = fecha.month
        dia = fecha.day

        fechaFormato = str(anio)+"-"+str(mes)+"-"+str(dia)

        horaEntrada = str(hora) +":"+str(minuto)+":"+str(segundos)

        horaInt = int(hora)
        minuto = int(minuto)

        if horaInt <= 8:
            if minuto <= 10:
                retardo = "NO"
            else:
                retardo = "SI"
        else:
            retardo = "SI"


        registroAsistencia = Asistencia(id_empleado = Empleados.objects.get(id_empleado = intIdEmpleado),
                                        fecha = fechaFormato, hora_entrada = horaEntrada, retardo = retardo,hora_salida = "na", a_tiempo = "na")

        registroAsistencia.save()

        if registroAsistencia:

            consultaEmpleado = Empleados.objects.filter(id_empleado = intIdEmpleado)

            for datoEmpleado in consultaEmpleado:
                nombreEmpleado = datoEmpleado.nombre
                apellidosEmpleado = datoEmpleado.apellidos

            nombreCompletoEmpleado = nombreEmpleado+" "+apellidosEmpleado

            if retardo == "SI":
                request.session["registroEntrada"] = nombreCompletoEmpleado+", entrada registrada con retraso! Ten un buen día!"
            else:
                request.session["registroEntrada"] = nombreCompletoEmpleado+", entrada registrada a tiempo! Ten un buen día!"
    except:
       request.session["errorAsistencia"] = "Error en asistencia. Favor de firmar la hoja con puño y letra indicando la hora de entrada."

    return redirect("/registroEntrada/")
    

def registrarSalidaEmpleado(request):

    
    #try:
        #Registrar asistencia
        fecha = datetime.now()

        face_id = faceRecognition.recognizeFace()
        print(face_id)

        intIdEmpleado = int(face_id)

        print(" ID DE EMPLEADO ESCANEADO SALIDA = "+str(face_id))

        consultaEmpleado = Empleados.objects.filter(id_empleado = face_id)

        for datoEmpleado in consultaEmpleado:
            nombreEmpleado = datoEmpleado.nombre
            apellidosEmpleado = datoEmpleado.apellidos
            idArea = datoEmpleado.id_area_id
            puestoEmpleado = datoEmpleado.puesto

        nombreCompletoEmpleado = nombreEmpleado+" "+apellidosEmpleado

        print(nombreCompletoEmpleado)
        
        
        hora = fecha.hour
        minuto = fecha.minute
        segundos = fecha.second

        anio = fecha.year
        mes = fecha.month
        dia = fecha.day

        fechaFormato = str(anio)+"-"+str(mes)+"-"+str(dia)

        horaSalida = str(hora) +":"+str(minuto)+":"+str(segundos)

        horaInt = int(hora)
        minuto = int(minuto)
        
        #Saber que tipo de horario tiene
        horarioAdministrativo = False   
        horarioOperativo = False

        if idArea == 9:
            if puestoEmpleado == "Jefatura de Soporte Técnico":
                horarioAdministrativo = True
            else:
                horarioOperativo = True
        else:
            horarioAdministrativo = True

        
        #Saber si tiene retardo o no
        numeroDeDiaDeHoy = datetime.today().weekday()
        if numeroDeDiaDeHoy >= 1 and numeroDeDiaDeHoy <=5:

            if horaInt == 17:
                if horarioAdministrativo:
                    if minuto <= 29:
                        aTiempo = "NO"
                    else:
                        aTiempo = "SI"
                elif horarioOperativo:
                    if minuto <= 0:
                        aTiempo = "NO"
                    else:
                        aTiempo = "SI"

            if horaInt > 17:
                aTiempo = "SI"

            else:
                aTiempo = "NO"

        elif numeroDeDiaDeHoy == 6:
            if horarioAdministrativo:
                if horaInt == 14:
                    if minuto <= 0:
                        aTiempo = "NO"
                    else:
                        aTiempo = "SI"

                elif horaInt > 14:
                    aTiempo = "NO"
            if horarioOperativo:
                if horaInt == 13:
                    if minuto <= 0:
                        aTiempo = "NO"
                    else:
                        aTiempo = "SI"

                elif horaInt > 13:
                    aTiempo = "NO"
        elif numeroDeDiaDeHoy == 7:
            #todo es hora extra
            aTiempo = "SI"
        
            
        

        

        #Buscar registro del día de hoy

        registroAsistenciaDeHoy = Asistencia.objects.filter(id_empleado_id__id_empleado = intIdEmpleado, fecha = fechaFormato).update(
            hora_salida = horaSalida, a_tiempo = aTiempo
        )


        if registroAsistenciaDeHoy:

            horasExtras = 0

            #Ver si hay horas extras

            #Checar primero si salio a tiempo.. si no, no hace nada de HE
            if aTiempo == "SI":
                
                #Obtener primero el horario
                numeroDeDiaDeHoy = datetime.today().weekday()
                if numeroDeDiaDeHoy >= 1 and numeroDeDiaDeHoy <=5:
                    if horarioAdministrativo:
                        #Horario de 8 a 5:30
                        horaSalidaOficial = "17:30:00"
                    elif horarioOperativo:
                        #Horario de 8 a 5
                        horaSalidaOficial = "17:00:00"
                    
                    todasLasHorasSonExtras = False
                elif numeroDeDiaDeHoy == 6:
                    if horarioAdministrativo:
                        #Horario de 8 a 2
                        horaSalidaOficial = "14:00:00"
                    elif horarioOperativo:
                        #Horario de 8 a 1
                        horaSalidaOficial = "13:00:00"


                    todasLasHorasSonExtras = False
                elif numeroDeDiaDeHoy == 7:
                    #todo es hora extra
                    todasLasHorasSonExtras = True
                

                if todasLasHorasSonExtras:
                    
                    #Tomar la hora de entrada y hora de salida, comparar la diferencia y hacer lo mismo para saber
                    # los minutos de diferencia y saber las horas que son.

                    asistencia = Asistencia.objects.filter(id_empleado_id__id_empleado = intIdEmpleado, fecha = fechaFormato)
                    for datoAsistencia in asistencia:
                        horaEntrada = datoAsistencia.hora_entrada
                        idAsistencia = datoAsistencia.id_asistencia

                    horaEntradaConFormato = datetime.strptime(horaEntrada,"%H:%M:%S")
                    horaSalidaConFormato = datetime.strptime(horaSalida,"%H:%M:%S")
                    diferenciaDeTiempoEnMinutos = ((horaSalidaConFormato - horaEntradaConFormato).total_seconds()) / 60
                    
                    horasExtras = diferenciaDeTiempoEnMinutos / 60

                    intHorasExtras = int(horasExtras) #Cantidad de horas extras

                
                    registroHorasExtras = HorasExtras(id_asitencia = Asistencia.objects.get(id_asistencia = idAsistencia),
                                                        numero_horas_extras = intHorasExtras)
                    registroHorasExtras.save()

                else:
                    #Calcular diferencia en minutos
                    horaSalidaOficialConFormato = datetime.strptime(horaSalidaOficial,"%H:%M:%S")
                    horaSalidaConFormato = datetime.strptime(horaSalida,"%H:%M:%S")
                    diferenciaDeTiempoEnMinutos = ((horaSalidaConFormato - horaSalidaOficialConFormato).total_seconds()) / 60
                    
                    horasExtras = diferenciaDeTiempoEnMinutos / 60


                    if horasExtras >= 1:
                        #Tiene al menos una hora extra
                        intHorasExtras = int(horasExtras) #Cantidad de horas extras

                        #Registro de horas extras.

                        #Consulta de asistencia para sacar el id
                        consultaAsistencia = Asistencia.objects.filter(id_empleado_id__id_empleado = intIdEmpleado, fecha = fechaFormato)
                        for dato in consultaAsistencia:
                            idAsistencia = dato.id_asistencia
                        registroHorasExtras = HorasExtras(id_asitencia = Asistencia.objects.get(id_asistencia = idAsistencia),
                                                          numero_horas_extras = intHorasExtras)
                        registroHorasExtras.save()

            if aTiempo == "SI":
                if horasExtras >=1:
                    intHorasExtras = int(horasExtras)
                    request.session["registroSalida"] = nombreCompletoEmpleado+", salida registrada a tiempo con "+str(intHorasExtras)+" horas extras! Ten un buen día!"
                else:
                    request.session["registroSalida"] = nombreCompletoEmpleado+", salida registrada a tiempo! Ten un buen día!"
            else:
                request.session["registroSalida"] = nombreCompletoEmpleado+", salida registrada antes de tiempo! Ten un buen día!"
                    



    
    #except:
       #request.session["errorAsistencia"] = "Error en asistencia. Favor de firmar la hoja con puño y letra indicando la hora de entrada."

        return redirect("/registroEntrada/")


def verAsistencia(request):
    if "idSesion" in request.session:
        estaEnAsistencias = True
        estaEnVerAsistencia = True

        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        if correo == "almacen01@customco.com.mx":
            almacen = True
        else:
            almacen = False

        if correo == "recursos.humanos@customco.com.mx":
            rh = True
        else:
            rh = False

        nombreCompleto = nombre + " " + apellidos
        
        foto = fotoAdmin(request)

        #Aqui se empieza

        fechasRangoIguales = False
        fechasRangoMayor = False
        fechasRangoBien = False
        

        if request.method == "POST":
            if "fechaEspecifica" in request.POST:
                fechaEspecifica = request.POST["fechaEspecifica"]
                fechaDeHoy = False
                fechaEspecificaAplicada = True
                fechaConRango = False
                fechaDesdeTexto = ""
                fechaHastaTexto = ""


                fecha_separada = fechaEspecifica.split("-") #29   06    2018            2018     29
                
                dia = fecha_separada[2]
                mesPosicion = fecha_separada[1]
                mesPosicionEntero = int(mesPosicion)
                #Sacar la fecha con letra

                meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto",
                         "Septiembre", "Octubre", "Noviembre", "Diciembre"]
                
                mes = meses[mesPosicionEntero - 1]



                fechaEspecificaConLetra = dia + " de "+mes+" del " +fecha_separada[0]

            elif "fechaDesde" in request.POST:
                fechaDesde = request.POST["fechaDesde"]
                fechaHasta = request.POST["fechaHasta"]

                fechaDeHoy = False
                fechaEspecificaAplicada = False
                fechaEspecifica = ""
                fechaEspecificaConLetra = ""
                fechaConRango = True

                fechaDesdeSeparada = fechaDesde.split("-")
                diaDesde = int(fechaDesdeSeparada[2])
                mesDesde = int(fechaDesdeSeparada[1])
                anioDesde = int(fechaDesdeSeparada[0])

                fechaHastaSeparada = fechaHasta.split("-")
                diaHasta = int(fechaHastaSeparada[2])
                mesHasta = int(fechaHastaSeparada[1])
                anioHasta = int(fechaHastaSeparada[0])

                fechaDesdeParaComparar = datetime.strptime(fechaDesde, '%Y-%m-%d')
                fechaHastaParaComparar = datetime.strptime(fechaHasta, '%Y-%m-%d')


                #Fechas en texto
                meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto",
                         "Septiembre", "Octubre", "Noviembre", "Diciembre"]
                
                mesDesdeTexto = meses[mesDesde - 1]
                mesHastaTexto = meses[mesHasta - 1]

                fechaDesdeTexto = fechaDesdeSeparada[2] + " de "+mesDesdeTexto+" del " +fechaDesdeSeparada[0]
                fechaHastaTexto = fechaHastaSeparada[2] + " de "+mesHastaTexto+" del "+fechaDesdeSeparada[0]

                
                if fechaDesdeParaComparar == fechaHastaParaComparar:
                    fechaDeHoy = True
                    fechaEspecificaAplicada = False
                    fechaConRango = False
                    fechaEspecifica = ""
                    fechaEspecificaConLetra = ""

                    fechaDesdeTexto = ""
                    fechaHastaTexto = ""

                    fechasRangoIguales = True
                elif fechaDesdeParaComparar > fechaHastaParaComparar:
                    fechasRangoMayor = True

                    fechaDeHoy = True
                    fechaEspecificaAplicada = False
                    fechaConRango = False
                    fechaEspecifica = ""
                    fechaEspecificaConLetra = ""

                    fechaDesdeTexto = ""
                    fechaHastaTexto = ""
                    
                else:
                    fechasRangoBien = True

        else:
            fechaDeHoy = True
            fechaEspecificaAplicada = False
            fechaConRango = False
            fechaEspecifica = ""
            fechaEspecificaConLetra = ""

            fechaDesdeTexto = ""
            fechaHastaTexto = ""




        
        now = datetime.now()
        fechaHoy = now.date()

        #Consulta de asistencias
        #Consulta de permisos de faltas
        if fechaDeHoy:
            consultaAsistenciasDiaDeHoy = Asistencia.objects.filter(fecha = fechaHoy)
            consultaPermisosFalta = PermisosAsistencia.objects.filter(fecha = fechaHoy)
            consultaFaltasGraves = FaltasAsistencia.objects.filter(fecha = fechaHoy)
        elif fechaEspecificaAplicada:
            consultaAsistenciasDiaDeHoy = Asistencia.objects.filter(fecha = fechaEspecifica)
            consultaPermisosFalta = PermisosAsistencia.objects.filter(fecha = fechaEspecifica)
            consultaFaltasGraves = FaltasAsistencia.objects.filter(fecha = fechaEspecifica)
        elif fechaConRango:
            if fechasRangoIguales or fechasRangoMayor:
                consultaAsistenciasDiaDeHoy = Asistencia.objects.filter(fecha = fechaHoy)
                consultaPermisosFalta = PermisosAsistencia.objects.filter(fecha = fechaHoy)
                consultaFaltasGraves = FaltasAsistencia.objects.filter(fecha = fechaHoy)
            elif fechasRangoBien:
                consultaAsistenciasDiaDeHoy = Asistencia.objects.filter(fecha__range = (fechaDesde, fechaHasta))
                consultaPermisosFalta = PermisosAsistencia.objects.filter(fecha__range = (fechaDesde, fechaHasta))
                consultaFaltasGraves = FaltasAsistencia.objects.filter(fecha__range = (fechaDesde, fechaHasta))


        listaAsistenciasDiaDeHoy = []
        listaAsistenciasDiaDeHoyModalsEntradaTardia = []
        listaAsistenciasDiaDeHoyModalsSalidaTemprana = []
        listaAsistenciasDiaDeHoyModalsSalidaFuera = []
        listaAsistenciasDiaDeHoyModalsSalidaFuera = []

        for asistenciaHoy in consultaAsistenciasDiaDeHoy:
            idAsistencia = asistenciaHoy.id_asistencia
            idEmpleado = asistenciaHoy.id_empleado_id

            consultaEmpleado = Empleados.objects.filter(id_empleado = idEmpleado)
            for datoEmpleado in consultaEmpleado:
                nombreEmpleado = datoEmpleado.nombre
                apellidoEmpleado = datoEmpleado.apellidos

                idAreaEmpleado = datoEmpleado.id_area_id
            
            nombreCompletoEmpleado = nombreEmpleado + " " +apellidoEmpleado

            consultaDepartamento = Areas.objects.filter(id_area = idAreaEmpleado)
            for datoDepartamento in consultaDepartamento:
                nombreDepartamento = datoDepartamento.nombre
                colorDepartamento = datoDepartamento.color

            fechaAsistencia = asistenciaHoy.fecha

            horaEntrada = asistenciaHoy.hora_entrada

            retardo = asistenciaHoy.retardo

            #Incidencias de entrada tardía

            consultaIncidenciaEntradaTardia = IncidenciaLlegadaTardia.objects.filter(id_asitencia_id__id_asistencia = idAsistencia)

            if consultaIncidenciaEntradaTardia:
                tieneIncidenciaEntradaTardia = "Si"
                for datoIncidenciaEntradaTardia in consultaIncidenciaEntradaTardia:
                    idIncidenciaEntradaTardia = datoIncidenciaEntradaTardia.id_incidencia_llegada_tardia
            else:
                tieneIncidenciaEntradaTardia = "No"
                idIncidenciaEntradaTardia = "No"

            #Hora salida

            horaSalida = asistenciaHoy.hora_salida

            if horaSalida == "na":
                estatusSalida = "Sin checar salida aún."
            else:
                estatusSalida = "Ya checo salida"

            salidaATiempo = asistenciaHoy.a_tiempo

            #Incidencia salida temprana

            consultaIncidenciaSalidaTemprana = IncidenciaSalidaTemprana.objects.filter(id_asitencia_id__id_asistencia = idAsistencia)

            if consultaIncidenciaSalidaTemprana:
                tieneIncidenciaSalidaTemprana = "Si"
                for datoIncidenciaSalidaTemprana in consultaIncidenciaSalidaTemprana:
                    idIncidenciaSalidaTemprana = datoIncidenciaSalidaTemprana.id_incidencia_salida_temprana
            else:
                tieneIncidenciaSalidaTemprana = "No"
                idIncidenciaSalidaTemprana = "No"


            #Incidencia salida por fuera

            consultaIncidenciaSalidaFuera = IncidenciaSalidaFuera.objects.filter(id_asitencia_id__id_asistencia = idAsistencia)

            if consultaIncidenciaSalidaFuera:
                tieneIncidenciaSalidaFuera= "Si"
                for datoIncidenciaSalidaFuera in consultaIncidenciaSalidaFuera:
                    idIncidenciaSalidaFuera = datoIncidenciaSalidaFuera.id_incidencia_salida_fuera
            else:
                tieneIncidenciaSalidaFuera = "No"
                idIncidenciaSalidaFuera = "No"

            #VER SI HAY HORAS EXTRAS!!!!

            #Consulta de horas extras de asistencia
            tieneHorasExtras = ""
            consultaHorasExtras = HorasExtras.objects.filter(id_asitencia_id = idAsistencia)

            if consultaHorasExtras:
                tieneHorasExtras = "SI"

                for datoHoraExtra in consultaHorasExtras:
                    horasExtras = datoHoraExtra.numero_horas_extras

            else:
                tieneHorasExtras = "NO"
                horasExtras = 0

            
            

            listaAsistenciasDiaDeHoy.append([idAsistencia, nombreCompletoEmpleado, nombreDepartamento, colorDepartamento,
                                             fechaAsistencia, horaEntrada, retardo, tieneIncidenciaEntradaTardia, estatusSalida, horaSalida,
                                             salidaATiempo, tieneIncidenciaSalidaTemprana, idIncidenciaEntradaTardia, tieneIncidenciaSalidaFuera,
                                             idIncidenciaSalidaFuera, tieneHorasExtras,horasExtras])
            
            listaAsistenciasDiaDeHoyModalsEntradaTardia.append([idAsistencia, nombreCompletoEmpleado, nombreDepartamento, colorDepartamento,
                                             fechaAsistencia, horaEntrada, retardo, tieneIncidenciaEntradaTardia, estatusSalida, horaSalida,
                                             salidaATiempo, tieneIncidenciaSalidaTemprana, idIncidenciaEntradaTardia, tieneIncidenciaSalidaFuera,
                                             idIncidenciaSalidaFuera, tieneHorasExtras,horasExtras])
            
            listaAsistenciasDiaDeHoyModalsSalidaTemprana.append([idAsistencia, nombreCompletoEmpleado, nombreDepartamento, colorDepartamento,
                                             fechaAsistencia, horaEntrada, retardo, tieneIncidenciaEntradaTardia, estatusSalida, horaSalida,
                                             salidaATiempo, tieneIncidenciaSalidaTemprana, idIncidenciaEntradaTardia, tieneIncidenciaSalidaFuera,
                                             idIncidenciaSalidaFuera, tieneHorasExtras,horasExtras])
            
            listaAsistenciasDiaDeHoyModalsSalidaFuera.append([idAsistencia, nombreCompletoEmpleado, nombreDepartamento, colorDepartamento,
                                             fechaAsistencia, horaEntrada, retardo, tieneIncidenciaEntradaTardia, estatusSalida, horaSalida,
                                             salidaATiempo, tieneIncidenciaSalidaTemprana, idIncidenciaEntradaTardia, tieneIncidenciaSalidaFuera,
                                             idIncidenciaSalidaFuera, tieneHorasExtras,horasExtras])
            
            listaAsistenciasDiaDeHoyModalsSalidaFuera.append([idAsistencia, nombreCompletoEmpleado, nombreDepartamento, colorDepartamento,
                                             fechaAsistencia, horaEntrada, retardo, tieneIncidenciaEntradaTardia, estatusSalida, horaSalida,
                                             salidaATiempo, tieneIncidenciaSalidaTemprana, idIncidenciaEntradaTardia, tieneIncidenciaSalidaFuera,
                                             idIncidenciaSalidaFuera, tieneHorasExtras,horasExtras])
            

        #Vista para agregar Justificante

        
        consultaEmpleadoActivo = Empleados.objects.filter(activo="A", correo__icontains="@customco.com.mx")
        empleadosActivosEnCustom = []


        for dato in consultaEmpleadoActivo:
            nombreCompleto = dato.nombre +" "+dato.apellidos
            idEmpleado = dato.id_empleado
            idArea = dato.id_area_id

            consultaArea = Areas.objects.filter(id_area = idArea)

            for dato in consultaArea:

                nombreArea = dato.nombre

            empleadosActivosEnCustom.append([idEmpleado,nombreCompleto,nombreArea]) 

        #Datos de permisos para modal

        listaDePermisosFalta = []
        contadorPermisosFalta = 0

        for permisoFalta in consultaPermisosFalta:
            idPermisoFalta = permisoFalta.id_permiso_asistencia
            idEmpleadoPermiso = permisoFalta.id_empleado_id
            fechaPermiso = permisoFalta.fecha
            motivoPermiso = permisoFalta.motivo

            #Datos de empleado.
            consultaEmpleadoFalta = Empleados.objects.filter(id_empleado = idEmpleadoPermiso)

            for datoEmpleado in consultaEmpleadoFalta:
                nombreCompletoEmpleadoFalta = datoEmpleado.nombre + " "+datoEmpleado.apellidos

                idArea = datoEmpleado.id_area_id

                consultaDepartamento = Areas.objects.filter(id_area = idArea)
                for datoDepartamento in consultaDepartamento:
                    departamentoEmpleadoFalta = datoDepartamento.nombre
                    colorDepartamentoEmpleadoFalta = datoDepartamento.color

            listaDePermisosFalta.append([idPermisoFalta, nombreCompletoEmpleadoFalta, departamentoEmpleadoFalta, colorDepartamentoEmpleadoFalta, fechaPermiso, motivoPermiso])
            contadorPermisosFalta = contadorPermisosFalta + 1

        #Datos de faltas para modal

        listaDeFaltasGraves = []
        contadorFaltasGraves = 0

        for falta in consultaFaltasGraves:
            idFaltaGrave = falta.id_falta_asistencia
            idEmpleadoFalta = falta.id_empleado_id
            fechaFalta = falta.fecha
            observaciones = falta.observaciones

            #Datos de empleado.
            consultaEmpleadoFaltaGrave = Empleados.objects.filter(id_empleado = idEmpleadoFalta)

            for datoEmpleado in consultaEmpleadoFaltaGrave:
                nombreCompletoEmpleadoFaltaGrave = datoEmpleado.nombre + " "+datoEmpleado.apellidos

                idAreaEmpleadoGrave = datoEmpleado.id_area_id

                consultaDepartamento = Areas.objects.filter(id_area = idAreaEmpleadoGrave)
                for datoDepartamento in consultaDepartamento:
                    departamentoEmpleadoFaltaGrave = datoDepartamento.nombre
                    colorDepartamentoEmpleadoFaltaGrave = datoDepartamento.color

            listaDeFaltasGraves.append([idFaltaGrave, nombreCompletoEmpleadoFaltaGrave, departamentoEmpleadoFaltaGrave, colorDepartamentoEmpleadoFaltaGrave, fechaFalta, observaciones])
            contadorFaltasGraves = contadorFaltasGraves + 1

        
        #LISTA PARA VER INCIDENCIAS LLEGADA TARDIA.

        listaIncidenciasLlegadaTardia = []

        for asistencia in listaAsistenciasDiaDeHoy:
            idAsistencia = asistencia[0]
            
            incidenciaLlegadaTardiaRegistrada = IncidenciaLlegadaTardia.objects.filter(id_asitencia_id = idAsistencia)

            if incidenciaLlegadaTardiaRegistrada:
                for incidencia in incidenciaLlegadaTardiaRegistrada:
                    idIncidenciaLlegadaTardia = incidencia.id_incidencia_llegada_tardia

                    motivoLlegadaTardia = incidencia.motivo

                    #CONSULTA ASISTENCIA

                    consultaAsistencia = Asistencia.objects.filter(id_asistencia = idAsistencia)
                    for datoAsistencia in consultaAsistencia:
                        fechaAsistencia = datoAsistencia.fecha
                        horaEntrada = datoAsistencia.hora_entrada
                        idEmpleado = datoAsistencia.id_empleado_id

                        consultaEmpleado = Empleados.objects.filter(id_empleado = idEmpleado)
                        for datoEmpleado in consultaEmpleado:
                            nombreCompletoEmpleado = datoEmpleado.nombre + " " + datoEmpleado.apellidos
                            idArea = datoEmpleado.id_area_id

                            consultaArea = Areas.objects.filter(id_area = idArea)
                            for datoArea in consultaArea:
                                nombreArea = datoArea.nombre
                                colorArea = datoArea.color
                        
                    listaIncidenciasLlegadaTardia.append([idAsistencia, fechaAsistencia, horaEntrada, nombreCompletoEmpleado,
                    nombreArea, colorArea, motivoLlegadaTardia])

                


            else:
                listaIncidenciasLlegadaTardia.append(["nada", "nada", "nada", "nada", "nada", "nada", "nada"])



        #LISTA PARA VER INCIDENCIAS SALIDA TEMPRANA.

        listaIncidenciasSalidasTempranas = []

        for asistencia in listaAsistenciasDiaDeHoy:
            idAsistencia = asistencia[0]
            
            incidenciaSalidaTemprana = IncidenciaSalidaTemprana.objects.filter(id_asitencia_id = idAsistencia)

            if incidenciaSalidaTemprana:
                for incidencia in incidenciaSalidaTemprana:

                    motivoSalidaTemprana= incidencia.motivo

                    #CONSULTA ASISTENCIA

                    consultaAsistencia = Asistencia.objects.filter(id_asistencia = idAsistencia)
                    for datoAsistencia in consultaAsistencia:
                        fechaAsistencia = datoAsistencia.fecha
                        horaSalida = datoAsistencia.hora_salida
                        idEmpleado = datoAsistencia.id_empleado_id

                        consultaEmpleado = Empleados.objects.filter(id_empleado = idEmpleado)
                        for datoEmpleado in consultaEmpleado:
                            nombreCompletoEmpleado = datoEmpleado.nombre + " " + datoEmpleado.apellidos
                            idArea = datoEmpleado.id_area_id

                            consultaArea = Areas.objects.filter(id_area = idArea)
                            for datoArea in consultaArea:
                                nombreArea = datoArea.nombre
                                colorArea = datoArea.color
                        
                    listaIncidenciasSalidasTempranas.append([idAsistencia, fechaAsistencia, horaSalida, nombreCompletoEmpleado,
                    nombreArea, colorArea, motivoSalidaTemprana])

                


            else:
                listaIncidenciasSalidasTempranas.append(["nada", "nada", "nada", "nada", "nada", "nada", "nada"])

        

         #LISTA PARA VER INCIDENCIAS SALIDA POR FUERA.
        listaIncidenciasSalidaPorFuera = []
        

        for asistencia in listaAsistenciasDiaDeHoy:
            idAsistencia = asistencia[0]
            
            incidenciaSalidaFuera = IncidenciaSalidaFuera.objects.filter(id_asitencia_id = idAsistencia)

            if incidenciaSalidaFuera:
                for incidencia in incidenciaSalidaFuera:

                    motivoSalidaFuera= incidencia.motivo

                    #CONSULTA ASISTENCIA

                    consultaAsistencia = Asistencia.objects.filter(id_asistencia = idAsistencia)
                    for datoAsistencia in consultaAsistencia:
                        fechaAsistencia = datoAsistencia.fecha
                        horaSalida = datoAsistencia.hora_salida
                        idEmpleado = datoAsistencia.id_empleado_id

                        consultaEmpleado = Empleados.objects.filter(id_empleado = idEmpleado)
                        for datoEmpleado in consultaEmpleado:
                            nombreCompletoEmpleado = datoEmpleado.nombre + " " + datoEmpleado.apellidos
                            idArea = datoEmpleado.id_area_id

                            consultaArea = Areas.objects.filter(id_area = idArea)
                            for datoArea in consultaArea:
                                nombreArea = datoArea.nombre
                                colorArea = datoArea.color
                        
                    listaIncidenciasSalidaPorFuera.append([idAsistencia, fechaAsistencia, horaSalida, nombreCompletoEmpleado,
                    nombreArea, colorArea, motivoSalidaFuera])

                


            else:
                listaIncidenciasSalidaPorFuera.append(["nada", "nada", "nada", "nada", "nada", "nada", "nada"])


        if "permisoFaltaGuardado" in request.session:
            permisoFaltaGuardado = request.session["permisoFaltaGuardado"]
            del request.session["permisoFaltaGuardado"]

            return render(request,"empleadosCustom/Asistencia/Asistencia/verAsistencia.html",{"estaEnAsistencias":estaEnAsistencias,"estaEnVerAsistencia":estaEnVerAsistencia ,"id_admin":id_admin,"nombre":nombre,"apellidos":apellidos,"correo":correo,"nombreCompleto":nombreCompleto,"almacen":almacen,"foto":foto, "rh":rh,
                                                                                          "fechaHoy":fechaHoy, "listaAsistenciasDiaDeHoy":listaAsistenciasDiaDeHoy,
                                                                                          "fechaDeHoy":fechaDeHoy, "fechaEspecificaAplicada":fechaEspecificaAplicada, "fechaEspecifica":fechaEspecifica,
                                                                                          "fechaEspecificaConLetra":fechaEspecificaConLetra, "fechaConRango":fechaConRango,"fechaDesdeTexto":fechaDesdeTexto, "fechaHastaTexto":fechaHastaTexto,
                                                                                          "fechasRangoIguales":fechasRangoIguales, "fechasRangoMayor":fechasRangoMayor, "fechasRangoBien":fechasRangoBien,"empleadosActivosEnCustom":empleadosActivosEnCustom,
                                                                                          "permisoFaltaGuardado":permisoFaltaGuardado, "listaDePermisosFalta":listaDePermisosFalta, "contadorPermisosFalta":contadorPermisosFalta,
                                                                                          "listaDeFaltasGraves":listaDeFaltasGraves, "contadorFaltasGraves":contadorFaltasGraves,
                                                                                          "listaAsistenciasDiaDeHoyModalsEntradaTardia":listaAsistenciasDiaDeHoyModalsEntradaTardia, "listaIncidenciasLlegadaTardia":listaIncidenciasLlegadaTardia,
                                                                                          "listaAsistenciasDiaDeHoyModalsSalidaTemprana":listaAsistenciasDiaDeHoyModalsSalidaTemprana, "listaIncidenciasSalidasTempranas":listaIncidenciasSalidasTempranas, "listaAsistenciasDiaDeHoyModalsSalidaFuera":listaAsistenciasDiaDeHoyModalsSalidaFuera, "listaAsistenciasDiaDeHoyModalsSalidaFuera":listaAsistenciasDiaDeHoyModalsSalidaFuera, "listaIncidenciasSalidaPorFuera":listaIncidenciasSalidaPorFuera})
        
        if "faltaGuardada" in request.session:
            faltaGuardada = request.session["faltaGuardada"]
            del request.session["faltaGuardada"]

            return render(request,"empleadosCustom/Asistencia/Asistencia/verAsistencia.html",{"estaEnAsistencias":estaEnAsistencias,"estaEnVerAsistencia":estaEnVerAsistencia ,"id_admin":id_admin,"nombre":nombre,"apellidos":apellidos,"correo":correo,"nombreCompleto":nombreCompleto,"almacen":almacen,"foto":foto, "rh":rh,
                                                                                          "fechaHoy":fechaHoy, "listaAsistenciasDiaDeHoy":listaAsistenciasDiaDeHoy,
                                                                                          "fechaDeHoy":fechaDeHoy, "fechaEspecificaAplicada":fechaEspecificaAplicada, "fechaEspecifica":fechaEspecifica,
                                                                                          "fechaEspecificaConLetra":fechaEspecificaConLetra, "fechaConRango":fechaConRango,"fechaDesdeTexto":fechaDesdeTexto, "fechaHastaTexto":fechaHastaTexto,
                                                                                          "fechasRangoIguales":fechasRangoIguales, "fechasRangoMayor":fechasRangoMayor, "fechasRangoBien":fechasRangoBien,"empleadosActivosEnCustom":empleadosActivosEnCustom,
                                                                                          "listaDePermisosFalta":listaDePermisosFalta, "contadorPermisosFalta":contadorPermisosFalta,
                                                                                          "listaDeFaltasGraves":listaDeFaltasGraves, "contadorFaltasGraves":contadorFaltasGraves, "faltaGuardada":faltaGuardada,
                                                                                          "listaAsistenciasDiaDeHoyModalsEntradaTardia":listaAsistenciasDiaDeHoyModalsEntradaTardia, "listaIncidenciasLlegadaTardia":listaIncidenciasLlegadaTardia,
                                                                                          "listaAsistenciasDiaDeHoyModalsSalidaTemprana":listaAsistenciasDiaDeHoyModalsSalidaTemprana, "listaIncidenciasSalidasTempranas":listaIncidenciasSalidasTempranas, "listaAsistenciasDiaDeHoyModalsSalidaFuera":listaAsistenciasDiaDeHoyModalsSalidaFuera,
                                                                                          "listaIncidenciasSalidaPorFuera":listaIncidenciasSalidaPorFuera})

        if "incidenciaLlegadaTardiaGuardada" in request.session:
            incidenciaLlegadaTardiaGuardada = request.session["incidenciaLlegadaTardiaGuardada"]
            del request.session["incidenciaLlegadaTardiaGuardada"]

            return render(request,"empleadosCustom/Asistencia/Asistencia/verAsistencia.html",{"estaEnAsistencias":estaEnAsistencias,"estaEnVerAsistencia":estaEnVerAsistencia ,"id_admin":id_admin,"nombre":nombre,"apellidos":apellidos,"correo":correo,"nombreCompleto":nombreCompleto,"almacen":almacen,"foto":foto, "rh":rh,
                                                                                          "fechaHoy":fechaHoy, "listaAsistenciasDiaDeHoy":listaAsistenciasDiaDeHoy,
                                                                                          "fechaDeHoy":fechaDeHoy, "fechaEspecificaAplicada":fechaEspecificaAplicada, "fechaEspecifica":fechaEspecifica,
                                                                                          "fechaEspecificaConLetra":fechaEspecificaConLetra, "fechaConRango":fechaConRango,"fechaDesdeTexto":fechaDesdeTexto, "fechaHastaTexto":fechaHastaTexto,
                                                                                          "fechasRangoIguales":fechasRangoIguales, "fechasRangoMayor":fechasRangoMayor, "fechasRangoBien":fechasRangoBien,"empleadosActivosEnCustom":empleadosActivosEnCustom, "listaDePermisosFalta":listaDePermisosFalta
                                                                                          , "contadorPermisosFalta":contadorPermisosFalta,
                                                                                          "listaDeFaltasGraves":listaDeFaltasGraves, "contadorFaltasGraves":contadorFaltasGraves,
                                                                                          "listaAsistenciasDiaDeHoyModalsEntradaTardia":listaAsistenciasDiaDeHoyModalsEntradaTardia, "incidenciaLlegadaTardiaGuardada":incidenciaLlegadaTardiaGuardada, "listaIncidenciasLlegadaTardia":listaIncidenciasLlegadaTardia,
                                                                                          "listaAsistenciasDiaDeHoyModalsSalidaTemprana":listaAsistenciasDiaDeHoyModalsSalidaTemprana, "listaIncidenciasSalidasTempranas":listaIncidenciasSalidasTempranas, "listaAsistenciasDiaDeHoyModalsSalidaFuera":listaAsistenciasDiaDeHoyModalsSalidaFuera,
                                                                                          "listaIncidenciasSalidaPorFuera":listaIncidenciasSalidaPorFuera})
        

        if "incidenciaSalidaTempranaGuardada" in request.session:
            incidenciaSalidaTempranaGuardada = request.session["incidenciaSalidaTempranaGuardada"]
            del request.session["incidenciaSalidaTempranaGuardada"]

            return render(request,"empleadosCustom/Asistencia/Asistencia/verAsistencia.html",{"estaEnAsistencias":estaEnAsistencias,"estaEnVerAsistencia":estaEnVerAsistencia ,"id_admin":id_admin,"nombre":nombre,"apellidos":apellidos,"correo":correo,"nombreCompleto":nombreCompleto,"almacen":almacen,"foto":foto, "rh":rh,
                                                                                          "fechaHoy":fechaHoy, "listaAsistenciasDiaDeHoy":listaAsistenciasDiaDeHoy,
                                                                                          "fechaDeHoy":fechaDeHoy, "fechaEspecificaAplicada":fechaEspecificaAplicada, "fechaEspecifica":fechaEspecifica,
                                                                                          "fechaEspecificaConLetra":fechaEspecificaConLetra, "fechaConRango":fechaConRango,"fechaDesdeTexto":fechaDesdeTexto, "fechaHastaTexto":fechaHastaTexto,
                                                                                          "fechasRangoIguales":fechasRangoIguales, "fechasRangoMayor":fechasRangoMayor, "fechasRangoBien":fechasRangoBien,"empleadosActivosEnCustom":empleadosActivosEnCustom, "listaDePermisosFalta":listaDePermisosFalta
                                                                                          , "contadorPermisosFalta":contadorPermisosFalta,
                                                                                          "listaDeFaltasGraves":listaDeFaltasGraves, "contadorFaltasGraves":contadorFaltasGraves,
                                                                                          "listaAsistenciasDiaDeHoyModalsEntradaTardia":listaAsistenciasDiaDeHoyModalsEntradaTardia, "listaIncidenciasLlegadaTardia":listaIncidenciasLlegadaTardia,
                                                                                          "listaAsistenciasDiaDeHoyModalsSalidaTemprana":listaAsistenciasDiaDeHoyModalsSalidaTemprana, "incidenciaSalidaTempranaGuardada":incidenciaSalidaTempranaGuardada, "listaIncidenciasSalidasTempranas":listaIncidenciasSalidasTempranas,
                                                                                          "listaAsistenciasDiaDeHoyModalsSalidaFuera":listaAsistenciasDiaDeHoyModalsSalidaFuera, "listaIncidenciasSalidaPorFuera":listaIncidenciasSalidaPorFuera})
        
        if "incidenciaSalidaFuera" in request.session:
            incidenciaSalidaFuera = request.session["incidenciaSalidaFuera"]
            del request.session["incidenciaSalidaFuera"]

            return render(request,"empleadosCustom/Asistencia/Asistencia/verAsistencia.html",{"estaEnAsistencias":estaEnAsistencias,"estaEnVerAsistencia":estaEnVerAsistencia ,"id_admin":id_admin,"nombre":nombre,"apellidos":apellidos,"correo":correo,"nombreCompleto":nombreCompleto,"almacen":almacen,"foto":foto, "rh":rh,
                                                                                          "fechaHoy":fechaHoy, "listaAsistenciasDiaDeHoy":listaAsistenciasDiaDeHoy,
                                                                                          "fechaDeHoy":fechaDeHoy, "fechaEspecificaAplicada":fechaEspecificaAplicada, "fechaEspecifica":fechaEspecifica,
                                                                                          "fechaEspecificaConLetra":fechaEspecificaConLetra, "fechaConRango":fechaConRango,"fechaDesdeTexto":fechaDesdeTexto, "fechaHastaTexto":fechaHastaTexto,
                                                                                          "fechasRangoIguales":fechasRangoIguales, "fechasRangoMayor":fechasRangoMayor, "fechasRangoBien":fechasRangoBien,"empleadosActivosEnCustom":empleadosActivosEnCustom, "listaDePermisosFalta":listaDePermisosFalta
                                                                                          , "contadorPermisosFalta":contadorPermisosFalta,
                                                                                          "listaDeFaltasGraves":listaDeFaltasGraves, "contadorFaltasGraves":contadorFaltasGraves,
                                                                                          "listaAsistenciasDiaDeHoyModalsEntradaTardia":listaAsistenciasDiaDeHoyModalsEntradaTardia, "listaIncidenciasLlegadaTardia":listaIncidenciasLlegadaTardia,
                                                                                          "listaAsistenciasDiaDeHoyModalsSalidaTemprana":listaAsistenciasDiaDeHoyModalsSalidaTemprana, "listaIncidenciasSalidasTempranas":listaIncidenciasSalidasTempranas, "listaAsistenciasDiaDeHoyModalsSalidaFuera":listaAsistenciasDiaDeHoyModalsSalidaFuera,
                                                                                          "incidenciaSalidaFuera":incidenciaSalidaFuera, "listaIncidenciasSalidaPorFuera":listaIncidenciasSalidaPorFuera})


        return render(request,"empleadosCustom/Asistencia/Asistencia/verAsistencia.html",{"estaEnAsistencias":estaEnAsistencias,"estaEnVerAsistencia":estaEnVerAsistencia ,"id_admin":id_admin,"nombre":nombre,"apellidos":apellidos,"correo":correo,"nombreCompleto":nombreCompleto,"almacen":almacen,"foto":foto, "rh":rh,
                                                                                          "fechaHoy":fechaHoy, "listaAsistenciasDiaDeHoy":listaAsistenciasDiaDeHoy,
                                                                                          "fechaDeHoy":fechaDeHoy, "fechaEspecificaAplicada":fechaEspecificaAplicada, "fechaEspecifica":fechaEspecifica,
                                                                                          "fechaEspecificaConLetra":fechaEspecificaConLetra, "fechaConRango":fechaConRango,"fechaDesdeTexto":fechaDesdeTexto, "fechaHastaTexto":fechaHastaTexto,
                                                                                          "fechasRangoIguales":fechasRangoIguales, "fechasRangoMayor":fechasRangoMayor, "fechasRangoBien":fechasRangoBien,"empleadosActivosEnCustom":empleadosActivosEnCustom, "listaDePermisosFalta":listaDePermisosFalta
                                                                                          , "contadorPermisosFalta":contadorPermisosFalta,
                                                                                          "listaDeFaltasGraves":listaDeFaltasGraves, "contadorFaltasGraves":contadorFaltasGraves,
                                                                                          "listaAsistenciasDiaDeHoyModalsEntradaTardia":listaAsistenciasDiaDeHoyModalsEntradaTardia, "listaIncidenciasLlegadaTardia":listaIncidenciasLlegadaTardia,
                                                                                          "listaAsistenciasDiaDeHoyModalsSalidaTemprana":listaAsistenciasDiaDeHoyModalsSalidaTemprana, "listaIncidenciasSalidasTempranas":listaIncidenciasSalidasTempranas, "listaAsistenciasDiaDeHoyModalsSalidaFuera":listaAsistenciasDiaDeHoyModalsSalidaFuera,
                                                                                          "listaIncidenciasSalidaPorFuera":listaIncidenciasSalidaPorFuera})

    
    else:
        return redirect('/login/')


def agregarPermiso(request):
    if "idSesion" in request.session:

        if request.method == "POST":
            idEmpleadoPermiso = request.POST["idEmpleadoPermiso"]

            fechaPermiso = request.POST["fechaPermiso"]

            motivoPermiso = request.POST["motivoPermiso"]

            registroPermiso = PermisosAsistencia(id_empleado = Empleados.objects.get(id_empleado = idEmpleadoPermiso),
                                                 fecha = fechaPermiso, motivo = motivoPermiso)
            registroPermiso.save()

            if registroPermiso:

                request.session["permisoFaltaGuardado"] = "Se ha guardado el permiso correctamente!"

                return redirect('/verAsistencia/')

    else:
        return redirect('/login/')


def agregarFalta(request):
    if "idSesion" in request.session:

        if request.method == "POST":
            idEmpleadoFalta = request.POST["idEmpleadoFalta"]

            fechaFalta = request.POST["fechaFalta"]

            observacionesFalta = request.POST["observacionesFalta"]

            registroFalta = FaltasAsistencia(id_empleado = Empleados.objects.get(id_empleado = idEmpleadoFalta),
                                                 fecha = fechaFalta, observaciones = observacionesFalta)
            registroFalta.save()

            if registroFalta:

                request.session["faltaGuardada"] = "Se ha guardado la falta correctamente!"

                return redirect('/verAsistencia/')

    else:
        return redirect('/login/')


def agregarIncidenciaEntradaTardia(request):
    if "idSesion" in request.session:

        if request.method == "POST":
            idAsistenciaConLlegadaTardia = request.POST["idAsistencia"]
            motivoLlegadaTardia = request.POST["motivoLlegadaTardia"]

            registroIncidenciaLlegadaTardia = IncidenciaLlegadaTardia(id_asitencia = Asistencia.objects.get(id_asistencia = idAsistenciaConLlegadaTardia),
                                                                      motivo = motivoLlegadaTardia)

            registroIncidenciaLlegadaTardia.save()

            if registroIncidenciaLlegadaTardia:

                request.session["incidenciaLlegadaTardiaGuardada"] = "Se ha guardado la incidencia de llegada tardia!"

                return redirect('/verAsistencia/')

    else:
        return redirect('/login/')

def agregarIncidenciaSalidaTemprana(request):
    if "idSesion" in request.session:

        if request.method == "POST":
            idAsistenciaConSalidaTemprana = request.POST["idAsistencia"]
            motivoSalidaTemprana = request.POST["motivoSalidaTemprana"]

            registroIncidenciaSalidaTemprana = IncidenciaSalidaTemprana(id_asitencia = Asistencia.objects.get(id_asistencia = idAsistenciaConSalidaTemprana),
                                                                      motivo = motivoSalidaTemprana)

            registroIncidenciaSalidaTemprana.save()

            if registroIncidenciaSalidaTemprana:

                request.session["incidenciaSalidaTempranaGuardada"] = "Se ha guardado la incidencia de salida temprana!"

                return redirect('/verAsistencia/')

    else:
        return redirect('/login/')

def agregarIncidenciaSalidaFuera(request):
    if "idSesion" in request.session:

        if request.method == "POST":
            idAsistenciaConSalidaFuera = request.POST["idAsistencia"]
            horaSalida = request.POST["horaSalida"]
            motivoSalidaFuera = request.POST["motivoSalidaFuera"]

            horaSalidaString = str(horaSalida)+":00"


            registroIncidenciaSalidaFuera= IncidenciaSalidaFuera(id_asitencia = Asistencia.objects.get(id_asistencia = idAsistenciaConSalidaFuera), hora_salida = horaSalidaString ,motivo = motivoSalidaFuera)

            registroIncidenciaSalidaFuera.save()

            if registroIncidenciaSalidaFuera:

                #actualizarSalida su hora y si fue a tiempo o no..
                horaSeparada = horaSalidaString.split(":")
                hora = horaSeparada[0]
                minutos = horaSeparada[1]

                #consulta de area y puesto del empleado
                consultaAsistencia = Asistencia.objects.filter(id_asistencia = idAsistenciaConSalidaFuera)

                for dato in consultaAsistencia:
                    idAsistenciaPoder = dato.id_asistencia
                    idEmpleado = dato.id_empleado_id
                    horaEntrada = dato.hora_entrada
                
                consultaEmpleado = Empleados.objects.filter(id_empleado = idEmpleado)
                for datoEmpleado in consultaEmpleado:
                    idAreaEmpleado = datoEmpleado.id_area_id
                    puestoEmpleado = datoEmpleado.puesto

                horaInt = int(hora)
                minuto = int(minutos)

                #Saber que tipo de horario tiene
                horarioAdministrativo = False   
                horarioOperativo = False

                if idAreaEmpleado == 9:
                    if puestoEmpleado == "Jefatura de Soporte Técnico":
                        horarioAdministrativo = True
                    else:
                        horarioOperativo = True
                else:
                    horarioAdministrativo = True

        
                #Saber si tiene retardo o no
                numeroDeDiaDeHoy = datetime.today().weekday()
                if numeroDeDiaDeHoy >= 1 and numeroDeDiaDeHoy <=5:

                    if horaInt == 17:
                        if horarioAdministrativo:
                            if minuto <= 29:
                                aTiempo = "NO"
                            else:
                                aTiempo = "SI"
                        elif horarioOperativo:
                            if minuto <= 0:
                                aTiempo = "NO"
                            else:
                                aTiempo = "SI"

                    if horaInt > 17:
                        aTiempo = "SI"

                    else:
                        aTiempo = "NO"

                elif numeroDeDiaDeHoy == 6:
                    if horarioAdministrativo:
                        if horaInt == 14:
                            if minuto <= 0:
                                aTiempo = "NO"
                            else:
                                aTiempo = "SI"

                        elif horaInt > 14:
                            aTiempo = "NO"
                    if horarioOperativo:
                        if horaInt == 13:
                            if minuto <= 0:
                                aTiempo = "NO"
                            else:
                                aTiempo = "SI"

                        elif horaInt > 13:
                            aTiempo = "NO"
                elif numeroDeDiaDeHoy == 7:
                    #todo es hora extra
                    aTiempo = "SI"

                
                horasExtras = 0

                #Ver si hay horas extras

                #Checar primero si salio a tiempo.. si no, no hace nada de HE
                if aTiempo == "SI":
                
                    #Obtener primero el horario
                    numeroDeDiaDeHoy = datetime.today().weekday()
                    if numeroDeDiaDeHoy >= 1 and numeroDeDiaDeHoy <=5:
                        if horarioAdministrativo:
                            #Horario de 8 a 5:30
                            horaSalidaOficial = "17:30:00"
                        elif horarioOperativo:
                            #Horario de 8 a 5
                            horaSalidaOficial = "17:00:00"
                        
                        todasLasHorasSonExtras = False
                    elif numeroDeDiaDeHoy == 6:
                        if horarioAdministrativo:
                            #Horario de 8 a 2
                            horaSalidaOficial = "14:00:00"
                        elif horarioOperativo:
                            #Horario de 8 a 1
                            horaSalidaOficial = "13:00:00"


                        todasLasHorasSonExtras = False
                    elif numeroDeDiaDeHoy == 7:
                        #todo es hora extra
                        todasLasHorasSonExtras = True
                    
                    #GUARDAR HORAS EXTRAAAAAAAAAAAAAAAS
                    if todasLasHorasSonExtras:
                        
                        #Tomar la hora de entrada y hora de salida, comparar la diferencia y hacer lo mismo para saber
                        # los minutos de diferencia y saber las horas que son.

                        horaEntradaConFormato = datetime.strptime(horaEntrada,"%H:%M:%S")
                        horaSalidaConFormato = datetime.strptime(horaSalida,"%H:%M:%S")
                        diferenciaDeTiempoEnMinutos = ((horaSalidaConFormato - horaEntradaConFormato).total_seconds()) / 60
                        
                        horasExtras = diferenciaDeTiempoEnMinutos / 60

                        intHorasExtras = int(horasExtras) #Cantidad de horas extras

                    
                        registroHorasExtras = HorasExtras(id_asitencia = Asistencia.objects.get(id_asistencia = idAsistenciaPoder),
                                                            numero_horas_extras = intHorasExtras)
                        registroHorasExtras.save()

                    else:
                        #Calcular diferencia en minutos
                        horaSalidaOficialConFormato = datetime.strptime(horaSalidaOficial,"%H:%M:%S")
                        horaSalidaConFormato = datetime.strptime(horaSalidaString,"%H:%M:%S")
                        diferenciaDeTiempoEnMinutos = ((horaSalidaConFormato - horaSalidaOficialConFormato).total_seconds()) / 60
                        
                        horasExtras = diferenciaDeTiempoEnMinutos / 60


                        if horasExtras >= 1:
                            #Tiene al menos una hora extra
                            intHorasExtras = int(horasExtras) #Cantidad de horas extras

                            #Registro de horas extras.

                            registroHorasExtras = HorasExtras(id_asitencia = Asistencia.objects.get(id_asistencia = idAsistenciaPoder),
                                                            numero_horas_extras = intHorasExtras)
                            registroHorasExtras.save()








                consultaAsistencia = Asistencia.objects.filter(id_asistencia = idAsistenciaConSalidaFuera).update(hora_salida = horaSalidaString, a_tiempo = aTiempo)
                if horasExtras >= 1:    
                    request.session["incidenciaSalidaFuera"] = "Se ha guardado la incidencia fuera de la oficina con horas extras!"
                request.session["incidenciaSalidaFuera"] = "Se ha guardado la incidencia fuera de la oficina!"

                return redirect('/verAsistencia/')

    else:
        return redirect('/login/')



def reporteAsistencia(request):
    if "idSesion" in request.session:
        estaEnAsistencias = True
        estaEnReporteAsistencia = True

        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        if correo == "almacen01@customco.com.mx":
            almacen = True
        else:
            almacen = False

        if correo == "recursos.humanos@customco.com.mx":
            rh = True
        else:
            rh = False

        nombreCompleto = nombre + " " + apellidos
        
        foto = fotoAdmin(request)

        #Aqui se empieza
        
        #Consulta de todos los empleados activos
        consultaEmpleadosActivos = Empleados.objects.filter(correo__icontains = "@customco.com.mx", activo = "A")
        
        #Consulta de todos los proyectos
        consultaAsistenciaForanea = AsistenciaProyectoForaneo.objects.all()
        
        listadoDeProyectos = Proyectos.objects.all()
        
                
        
        
        if "errorEnFecha" in request.session:
            errorEnFecha = request.session["errorEnFecha"]
            del request.session["errorEnFecha"]
            return render(request,"empleadosCustom/Asistencia/Asistencia/reporteAsistencia.html",{"estaEnAsistencias":estaEnAsistencias,"estaEnReporteAsistencia":estaEnReporteAsistencia ,"id_admin":id_admin,"nombre":nombre,"apellidos":apellidos,"correo":correo,"nombreCompleto":nombreCompleto,"almacen":almacen,"foto":foto, "rh":rh,
                                                                                                  "errorEnFecha":errorEnFecha, "consultaEmpleadosActivos":consultaEmpleadosActivos, "listadoDeProyectos":listadoDeProyectos})

        
        return render(request,"empleadosCustom/Asistencia/Asistencia/reporteAsistencia.html",{"estaEnAsistencias":estaEnAsistencias,"estaEnReporteAsistencia":estaEnReporteAsistencia ,"id_admin":id_admin,"nombre":nombre,"apellidos":apellidos,"correo":correo,"nombreCompleto":nombreCompleto,"almacen":almacen,"foto":foto, "rh":rh,
                                                                                              "consultaEmpleadosActivos":consultaEmpleadosActivos, "listadoDeProyectos":listadoDeProyectos})

    
    else:
        return redirect('/login/')



def asistenciaForanea(request):
    if "idSesion" in request.session:
        estaEnAsistencias = True
        estaEnAsistenciaForanea = True

        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        if correo == "almacen01@customco.com.mx":
            almacen = True
        else:
            almacen = False

        if correo == "recursos.humanos@customco.com.mx":
            rh = True
        else:
            rh = False

        nombreCompleto = nombre + " " + apellidos
        
        foto = fotoAdmin(request)

        #Aqui se empieza

        if request.method == "POST":
            fechaDeHoy = False
            fechaHoy = ""

            if "fechaEspecifica" in request.POST:
                fechaEspecifica = request.POST["fechaEspecifica"]

                quiereFechaEspecifica = True
                quiereFechaRango = False

            elif "fechaDesde" in request.POST:
                fechaDesde = request.POST["fechaDesde"]
                fechaHasta = request.POST["fechaHasta"]

                quiereFechaEspecifica = False
                quiereFechaRango = True

        else:
            fechaDeHoy = True
            now = datetime.now()
            fechaHoy = now.date()

            quiereFechaEspecifica = False
            quiereFechaRango = False

        
        #consulta de asistencia foranea dependiendo de lo que se elija en fechas.

        if fechaDeHoy:
            consultaAsistenciaForanea = AsistenciaProyectoForaneo.objects.filter(fecha = fechaHoy)
            estatusFecha = "fechaHoy"
            fechaEspecifica = ""
            fechaDesde = ""
            fechaHasta = ""
        elif quiereFechaEspecifica:
            consultaAsistenciaForanea = AsistenciaProyectoForaneo.objects.filter(fecha = fechaEspecifica)
            estatusFecha = "fechaEspecífica"
            fechaDesde = ""
            fechaHasta = ""

            fecha_separada = fechaEspecifica.split("-") #29   06    2018            2018     29
                
            dia = fecha_separada[2]
            mesPosicion = fecha_separada[1]
            mesPosicionEntero = int(mesPosicion)
            #Sacar la fecha con letra

            meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto",
                        "Septiembre", "Octubre", "Noviembre", "Diciembre"]
            
            mes = meses[mesPosicionEntero - 1]



            fechaEspecifica = dia + " de "+mes+" del " +fecha_separada[0]
            
        elif quiereFechaRango:
            consultaAsistenciaForanea = AsistenciaProyectoForaneo.objects.filter(fecha__range = (fechaDesde, fechaHasta))
            estatusFecha = "rangoFechas"
            fechaEspecifica = ""

            #Fecha desde
            fechaDesdeSeparada = fechaDesde.split("-") #29   06    2018            2018     29
                
            diaDesde = fechaDesdeSeparada[2]
            mesPosicionDesde = fechaDesdeSeparada[1]
            mesPosicionEnteroDesde = int(mesPosicionDesde)
            #Sacar la fecha con letra

            meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto",
                        "Septiembre", "Octubre", "Noviembre", "Diciembre"]
            
            mesDesde = meses[mesPosicionEnteroDesde - 1]



            fechaDesde = diaDesde + " de "+mesDesde+" del " +fechaDesdeSeparada[0]

            #Fecha hasta
            fechaHastaSeparada = fechaHasta.split("-") #29   06    2018            2018     29
                
            diaHasta = fechaHastaSeparada[2]
            mesPosicionHasta = fechaHastaSeparada[1]
            mesPosicionEnteroHasta = int(mesPosicionHasta)
            #Sacar la fecha con letra
            
            mesHasta = meses[mesPosicionEnteroHasta - 1]

            fechaHasta = diaHasta + " de "+mesHasta+" del " +fechaHastaSeparada[0]



        listaAsistenciaForanea = []

        for asistencia in consultaAsistenciaForanea:
            idAsistencia = asistencia.id_asistencia_proyecto_foraneo

            #Empleado
            idEmpleado = asistencia.id_empleado_id
            
            #Si el empleado es de personal externo..
            if idEmpleado == None:
                nombreCompletoEmpleado = asistencia.personal_externo
                nombreDepartamento = ""
                colorDepartamento = ""
                
            else:
                consultaEmpleado = Empleados.objects.filter(id_empleado = idEmpleado)
                for datoEmpleado in consultaEmpleado:
                    nombreCompletoEmpleado = datoEmpleado.nombre + " "+ datoEmpleado.apellidos
                    idDepartamento = datoEmpleado.id_area_id
                    consultaDepartamento = Areas.objects.filter(id_area = idDepartamento)
                    
                    for datoDepartamento in consultaDepartamento:
                        nombreDepartamento = datoDepartamento.nombre
                        colorDepartamento = datoDepartamento.color

            fechaAsistencia = asistencia.fecha
            horaEntradaAsistencia = asistencia.hora_entrada
            horaSalidaAsistencia = asistencia.hora_salida
            proyectoTarea = asistencia.proyecto_interno_id
            actividadesRealizadas = asistencia.actividades_realizadas
            
            #Si es por motivo no ligado a un proyecto..
            if proyectoTarea == None:
                motivoAsistencia = asistencia.motivo
                nombreProyectoCompleto = ""
            else:
                #Consulta de proyecto
                consultaProyecto = Proyectos.objects.filter(id_proyecto = proyectoTarea)
                
                if consultaProyecto:
                    for datoProyecto in consultaProyecto:
                        numeroInternoProyecto = datoProyecto.numero_proyecto_interno
                        nombreProyecto = datoProyecto.nombre_proyecto
                        
                nombreProyectoCompleto = "# "+numeroInternoProyecto+" - "+nombreProyecto
                motivoAsistencia = ""
            
            
            salidaSiguienteDia = asistencia.salida_siguiente_dia


            #VER SI HAY HORAS EXTRAS!!!!

            #Consulta de horas extras de asistencia
            tieneHorasExtras = ""
            consultaHorasExtras = HorasExtrasForaneas.objects.filter(id_asitencia_foraneas = idAsistencia)

            if consultaHorasExtras:
                tieneHorasExtras = "SI"

                for datoHoraExtra in consultaHorasExtras:
                    horasExtras = datoHoraExtra.numero_horas_extras

            else:
                tieneHorasExtras = "NO"
                horasExtras = 0


            listaAsistenciaForanea.append([idAsistencia, nombreCompletoEmpleado, nombreDepartamento, colorDepartamento,
                                           fechaAsistencia, horaEntradaAsistencia, horaSalidaAsistencia, nombreProyectoCompleto,
                                           salidaSiguienteDia, tieneHorasExtras, horasExtras, motivoAsistencia,
                                           actividadesRealizadas])

        #Consulta empleados para agregar asistencia

        listaEmpleadosAgregarAsistencia = []

        consultaEmpleados = Empleados.objects.filter(activo="A", correo__icontains="@customco.com.mx")
        
        for empleadoActivo in consultaEmpleados:
            idEmpleado = empleadoActivo.id_empleado
            nombreCompleto = empleadoActivo.nombre +" "+ empleadoActivo.apellidos
            areaEmpleado = empleadoActivo.id_area_id
            consultaEmpleadoArea = Areas.objects.filter(id_area = areaEmpleado)

            for empleadoArea in consultaEmpleadoArea:

                nombreDepartamento = empleadoArea.nombre

            listaEmpleadosAgregarAsistencia.append([idEmpleado, nombreCompleto,nombreDepartamento])

        
        #Consulta de proyectos
        consultaProyectos = Proyectos.objects.all()
        

        if "asistenciaGuardada" in request.session:
            asistenciaGuardada = request.session["asistenciaGuardada"]
            del request.session["asistenciaGuardada"]

            return render(request,"empleadosCustom/Asistencia/Asistencia/asistenciaForanea.html",{"estaEnAsistencias":estaEnAsistencias,"estaEnAsistenciaForanea":estaEnAsistenciaForanea ,"id_admin":id_admin,"nombre":nombre,"apellidos":apellidos,"correo":correo,"nombreCompleto":nombreCompleto,"almacen":almacen,"foto":foto, "rh":rh,
                                                                                              "fechaDeHoy":fechaDeHoy, "fechaHoy":fechaHoy, "listaAsistenciaForanea":listaAsistenciaForanea, "listaEmpleadosAgregarAsistencia":listaEmpleadosAgregarAsistencia, "asistenciaGuardada":asistenciaGuardada, "estatusFecha":estatusFecha,
                                                                                              "fechaEspecifica":fechaEspecifica, "fechaDesde":fechaDesde, "fechaHasta":fechaHasta, "consultaProyectos":consultaProyectos})



        
        return render(request,"empleadosCustom/Asistencia/Asistencia/asistenciaForanea.html",{"estaEnAsistencias":estaEnAsistencias,"estaEnAsistenciaForanea":estaEnAsistenciaForanea ,"id_admin":id_admin,"nombre":nombre,"apellidos":apellidos,"correo":correo,"nombreCompleto":nombreCompleto,"almacen":almacen,"foto":foto, "rh":rh,
                                                                                              "fechaDeHoy":fechaDeHoy, "fechaHoy":fechaHoy, "listaAsistenciaForanea":listaAsistenciaForanea, "listaEmpleadosAgregarAsistencia":listaEmpleadosAgregarAsistencia, "estatusFecha":estatusFecha,
                                                                                              "fechaEspecifica":fechaEspecifica,  "fechaDesde":fechaDesde, "fechaHasta":fechaHasta, "consultaProyectos":consultaProyectos})

    
    else:
        return redirect('/login/')



def agregarAsistenciaForanea(request):
    if "idSesion" in request.session:
        if request.method == "POST":
            empleadosAsistencia = request.POST.getlist('empleadosAsistencia') 
            proyectoTarea = request.POST["proyecto"]
            fechaAsistencia = request.POST["fechaAsistencia"]
            horaEntrada = request.POST["horaEntrada"]
            horaSalida = request.POST["horaSalida"]

            if horaSalida == "":
                horaSalida = "na"

            #Ver si se realizo alineacion
        
            salidaSiguienteDia = "NO"
            

            #Registro de asistencia por empleado
            for empleado in empleadosAsistencia:
                idEmpleado = int(empleado)

                registroAsistencia = AsistenciaProyectoForaneo(id_empleado = Empleados.objects.get(id_empleado = idEmpleado),
                                                               fecha = fechaAsistencia, hora_entrada = horaEntrada,
                                                               hora_salida = horaSalida, proyecto_interno = Proyectos.objects.get(id_proyecto = proyectoTarea),
                                                               salida_siguiente_dia = salidaSiguienteDia)
                registroAsistencia.save()

                #ConsultaEmpleado
                consultaEmpleado = Empleados.objects.filter(id_empleado = idEmpleado)
                for datoEmpleado in consultaEmpleado:
                    idArea = datoEmpleado.id_area_id
                    puestoEmpleado = datoEmpleado.puesto

                #Saber que tipo de horario tiene
                horarioAdministrativo = False   
                horarioOperativo = False

                if idArea == 9:
                    if puestoEmpleado == "Jefatura de Soporte Técnico":
                        horarioAdministrativo = True
                    else:
                        horarioOperativo = True
                else:
                    horarioAdministrativo = True



                #SABER SI TIENE HORAS EXTRAS

                intHorasExtras = 0

                
                #Obtener primero el horario
                numeroDeDiaDeHoy = datetime.today().weekday()
                if numeroDeDiaDeHoy >= 1 and numeroDeDiaDeHoy <=5:
                    if horarioAdministrativo:
                        #Horario de 8 a 5:30
                        horaEntradaOficial = "8:00:00"
                        horaSalidaOficial = "17:30:00"
                        
                    elif horarioOperativo:
                        #Horario de 8 a 5
                        horaEntradaOficial = "8:00:00"
                        horaSalidaOficial = "17:00:00"
                    
                    todasLasHorasSonExtras = False
                elif numeroDeDiaDeHoy == 6:
                    if horarioAdministrativo:
                        #Horario de 8 a 2
                        horaEntradaOficial = "8:00:00"
                        horaSalidaOficial = "14:00:00"
                    elif horarioOperativo:
                        #Horario de 8 a 1
                        horaEntradaOficial = "8:00:00"
                        horaSalidaOficial = "13:00:00"

                    todasLasHorasSonExtras = False
                elif numeroDeDiaDeHoy == 7:
                    #todo es hora extra
                    todasLasHorasSonExtras = True
                

                if todasLasHorasSonExtras:
                    if horaSalida != "na":
                        #Tomar la hora de entrada y hora de salida, comparar la diferencia y hacer lo mismo para saber
                        # los minutos de diferencia y saber las horas que son.

                        #Sacar ultimo idDeAsistencia

                        ultimaAsistencia = 0
                        todasLasAsistencias = AsistenciaProyectoForaneo.objects.all()
                        for asistencia in todasLasAsistencias:
                            ultimaAsistencia = asistencia.id_asistencia_proyecto_foraneo

                        horaSalidaF = horaSalida+":00"
                        horaEntradaF = horaEntrada+":00"

                        horaEntradaConFormato = datetime.strptime(horaSalidaF,"%H:%M:%S")
                        horaSalidaConFormato = datetime.strptime(horaEntradaF,"%H:%M:%S")
                        diferenciaDeTiempoEnMinutos = ((horaSalidaConFormato - horaEntradaConFormato).total_seconds()) / 60
                        
                        horasExtras = diferenciaDeTiempoEnMinutos / 60

                        intHorasExtras = int(horasExtras) #Cantidad de horas extras


                else:
                    if horaSalida != "na":
                        
                        ultimaAsistencia = 0
                        todasLasAsistencias = AsistenciaProyectoForaneo.objects.all()
                        for asistencia in todasLasAsistencias:
                            ultimaAsistencia = asistencia.id_asistencia_proyecto_foraneo\
                            
                        horaSalidaF = horaSalida+":00"
                        horaEntradaF = horaEntrada+":00"
                        
                        #Calcular diferencia en minutos
                        horaEntradaOficialConFormato = datetime.strptime(horaEntradaOficial, "%H:%M:%S") #Hora de entrada de custom
                        horaSalidaOficialConFormato = datetime.strptime(horaSalidaOficial,"%H:%M:%S") #Hora de salida de custom
                        
                        
                        horaEntradaEmpleadoFormato = datetime.strptime(horaEntradaF,"%H:%M:%S") #Hora de entrada de empleado
                        horaSalidaEmpleadoFormato = datetime.strptime(horaSalidaF,"%H:%M:%S") #Hora de salida de empoleado

                        #HorasExtrasEntrada
                        diferenciaDeTiempoEnMinutosEntrada = ((horaEntradaOficialConFormato - horaEntradaEmpleadoFormato).total_seconds()) / 60
                        
                        horasExtrasEntrada = diferenciaDeTiempoEnMinutosEntrada / 60
                        

                        #Horas extras salida
                        diferenciaDeTiempoEnMinutosSalida = ((horaSalidaEmpleadoFormato - horaSalidaOficialConFormato).total_seconds()) / 60
                        
                        horasExtrasSalida = diferenciaDeTiempoEnMinutosSalida / 60
                        

                        if horasExtrasEntrada >=1:
                            intHorasExtrasEntrada = round(horasExtrasEntrada)
                            intHorasExtrasEntrada = int(intHorasExtrasEntrada)
                        else:
                            intHorasExtrasEntrada = 0


                        if horasExtrasSalida >=1:
                            intHorasExtrasSalida = int(horasExtrasSalida)
                        else:
                            intHorasExtrasSalida = 0

                        intHorasExtras = intHorasExtrasEntrada + intHorasExtrasSalida


                        if intHorasExtras >= 1:
                            registroHorasExtras = HorasExtrasForaneas(id_asitencia_foraneas = AsistenciaProyectoForaneo.objects.get(id_asistencia_proyecto_foraneo = ultimaAsistencia),
                                                                        numero_horas_extras = intHorasExtras)
                            registroHorasExtras.save()


            request.session["asistenciaGuardada"] = "La asistencia de "+proyectoTarea+ " ha sido guardada correctamente!"
                
            return redirect("/asistenciaForanea/")
            
            
    else:
        return redirect('/login/')



def reporteAsistenciaDiario(request):
    if "idSesion" in request.session:
        estaEnAsistencias = True
        estaEnReporteAsistencia = True

        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        if correo == "almacen01@customco.com.mx":
            almacen = True
        else:
            almacen = False

        if correo == "recursos.humanos@customco.com.mx":
            rh = True
        else:
            rh = False

        nombreCompleto = nombre + " " + apellidos
        
        foto = fotoAdmin(request)

        #Aqui se empieza

        if request.method == "POST":
            fechaDiaReporte = request.POST["fechaEspecifica"]
            

            
            #Asistencia perfecta
            if request.POST.get("asistenciaPerfectaDia", False): #Checkeado
                asistenciaPerfecta = True
            elif request.POST.get("asistenciaPerfectaDia", True): #No checkeado
                asistenciaPerfecta = False

            #Retardos
            if request.POST.get("retardosDia", False): #Checkeado
                retardos = True
            elif request.POST.get("retardosDia", True): #No checkeado
                retardos = False

            #Salidas tempranas
            if request.POST.get("salidasTempranasDia", False): #Checkeado
                salidasAntes = True
            elif request.POST.get("salidasTempranasDia", True): #No checkeado
                salidasAntes = False


            #Permisos de falta
            if request.POST.get("permisosFaltaDia", False): #Checkeado
                permisosFalta = True
            elif request.POST.get("permisosFaltaDia", True): #No checkeado
                permisosFalta = False

            #Faltas directas
            if request.POST.get("faltasDirectasDia", False): #Checkeado
                faltasDirectas = True
            elif request.POST.get("faltasDirectasDia", True): #No checkeado
                faltasDirectas = False

            #Horas extras
            if request.POST.get("horasExtrasDia", False): #Checkeado
                horasExtras = True
            elif request.POST.get("horasExtrasDia", True): #No checkeado
                horasExtras = False

            #Consulta de asistencias de ese día ------------------------------------------------------------------------------
            consultaAsistenciasOficina = Asistencia.objects.filter(fecha = fechaDiaReporte)
            consultaAsistenciaForanea = AsistenciaProyectoForaneo.objects.filter(fecha = fechaDiaReporte)

            #LISTAS DE ASISTENCIA DE LA OFICINA SOLAMENTE..
            listaAsistencia = [] #Aun sin llenar..
            listaRetardos = []
            listaIncidenciasLlegadasTardias = []
            listaSalidasTEmpranas = []
            listaIncidenciasSalidasTempranas = []
            listaIncidenciasSalidasFuera = []
            listaPermisosFalta = []
            listaFaltas = []
            listaHorasExtras = []

           

            listaEmpleadosConAsistenciaPerfectaOficina = []

            #LISTA DE ASISTENCIA FORANEA..
            listaAsistenciaForanea = []
            listaHorasExtrasForaneas = []

            #ASISTENCIA EN OFICINA
            for asistencia in consultaAsistenciasOficina:

                 #BOOLEANAS PARA ASISTENCIA PERFECTA.
                entradaPerfecta = False
                salidaPerfecta = False

                #datos de empleado
                idEmpleado = asistencia.id_empleado_id
                consultaEmpleado = Empleados.objects.filter(id_empleado = idEmpleado)
                for datoEmpleado in consultaEmpleado:
                    nombreCompletoEmpleado = datoEmpleado.nombre + " "+ datoEmpleado.apellidos
                    idArea = datoEmpleado.id_area_id
                    consultaArea = Areas.objects.filter(id_area = idArea)
                    for datoArea in consultaArea:
                        nombreArea = datoArea.nombre
                        colorArea = datoArea.color


                idAsistencia = asistencia.id_asistencia
                horaEntrada = asistencia.hora_entrada
                horaSalida = asistencia.hora_salida

                

                #Retardos
                retardo = asistencia.retardo
                
                if retardo == "SI":
                    
                    consultaIncidenciaLlegadaTardia = IncidenciaLlegadaTardia.objects.filter(id_asitencia_id = idAsistencia)
                    if consultaIncidenciaLlegadaTardia:
                        tieneIncidenciaLlegadaTardia = "SI"
                        for datoIncidenciaLlegadaTardia in consultaIncidenciaLlegadaTardia:
                            motivoIncidenciaLlegadaTardia = datoIncidenciaLlegadaTardia.motivo

                        listaIncidenciasLlegadasTardias.append([idAsistencia, nombreCompletoEmpleado, nombreArea, colorArea, horaEntrada, motivoIncidenciaLlegadaTardia])
                    else:
                        tieneIncidenciaLlegadaTardia = "NO"
                        motivoIncidenciaLlegadaTardia = ""
                        #tiene retardo..
                        listaIncidenciasLlegadasTardias.append([idAsistencia, nombreCompletoEmpleado, nombreArea, colorArea, horaEntrada, motivoIncidenciaLlegadaTardia])
                else:
                    entradaPerfecta = True #NO TIENE RETARDOS
                    tieneIncidenciaLlegadaTardia = ""
                    motivoIncidenciaLlegadaTardia = ""


                
                
                #Salidas tempranas
                salidaATiempo = asistencia.a_tiempo
                
                if salidaATiempo == "NO":

                    consultaIncidenciaSalidaTardia = IncidenciaSalidaTemprana.objects.filter(id_asitencia_id = idAsistencia)
                    if consultaIncidenciaSalidaTardia:
                        tieneIncidenciaSalidaTemprana = "SI"
                        for datoIncidenciaSalidaTardia in consultaIncidenciaSalidaTardia:
                            motivoIncidenciaSalidaTardia = datoIncidenciaSalidaTardia.motivo

                        listaIncidenciasSalidasTempranas.append([idAsistencia, nombreCompletoEmpleado, nombreArea, colorArea,horaEntrada, horaSalida, motivoIncidenciaSalidaTardia])
                    else:
                        tieneIncidenciaSalidaTemprana = "NO"
                        motivoIncidenciaSalidaTardia = ""
                        listaIncidenciasSalidasTempranas.append([idAsistencia, nombreCompletoEmpleado, nombreArea, colorArea,horaEntrada, horaSalida, motivoIncidenciaSalidaTardia])

                    tieneIncidenciaSalidaPorFuera = ""
                    motivoIncidenciaSalidaPorFuera = ""
                #Verificar si tiene salidas por fuera
                else:
                    
                    consultaIncidenciaSalidaPorFuera = IncidenciaSalidaFuera.objects.filter(id_asitencia_id = idAsistencia)
                    if consultaIncidenciaSalidaPorFuera:
                        tieneIncidenciaSalidaPorFuera = "SI"
                        for datoIncidenciaSalidaPorFuera in consultaIncidenciaSalidaPorFuera:
                            motivoIncidenciaSalidaPorFuera = datoIncidenciaSalidaPorFuera.motivo
                        
                        listaIncidenciasSalidasFuera.append([idAsistencia, nombreCompletoEmpleado, nombreArea, colorArea,horaEntrada, horaSalida, motivoIncidenciaSalidaPorFuera])

                        tieneIncidenciaSalidaTemprana = "NO"
                        motivoIncidenciaSalidaTardia = ""
                    else:
                        tieneIncidenciaSalidaPorFuera = "NO"
                        motivoIncidenciaSalidaPorFuera = ""
                        tieneIncidenciaSalidaTemprana = "NO"
                        motivoIncidenciaSalidaTardia = ""

                    salidaPerfecta = True #NO TIENE SALIDA TEMPRANA NI NADA, TODO BIEN..

                #CONSULTA DE HORAS EXTRAS ----------------------------------------------------------
                consultaHorasExtras = HorasExtras.objects.filter(id_asitencia_id = idAsistencia)

                if consultaHorasExtras:
                    estatusHorasExtras = "SI"
                    for datoHorasExtras in consultaHorasExtras:
                        numeroHorasExtras = datoHorasExtras.numero_horas_extras
                    
                    listaHorasExtras.append([idAsistencia, nombreCompletoEmpleado, nombreArea, colorArea,horaEntrada, horaSalida, numeroHorasExtras])
                else:
                    estatusHorasExtras = "na"
                    numeroHorasExtras = ""

                listaAsistencia.append([idAsistencia, nombreCompletoEmpleado, nombreArea, colorArea,
                                        horaEntrada, retardo, tieneIncidenciaLlegadaTardia,
                                        motivoIncidenciaLlegadaTardia,horaSalida,salidaATiempo,
                                        tieneIncidenciaSalidaTemprana, motivoIncidenciaSalidaTardia,
                                        tieneIncidenciaSalidaPorFuera, motivoIncidenciaSalidaPorFuera,
                                        estatusHorasExtras, numeroHorasExtras])

                #Asistencia perfecta.
                if entradaPerfecta and salidaPerfecta:
                    proyecto ="na"
                    listaEmpleadosConAsistenciaPerfectaOficina.append([nombreCompletoEmpleado, nombreArea, colorArea, proyecto])

            #CONSULTA DE PERMISOS DE FALTA DE ESE DIA ----------------------------------------------
            consultaPermisosFalta = PermisosAsistencia.objects.filter(fecha = fechaDiaReporte)

            if consultaPermisosFalta:
                for permiso in consultaPermisosFalta:
                    idPermiso = permiso.id_permiso_asistencia
                    idEmpleado = permiso.id_empleado_id
                    motivoPermiso = permiso.motivo
                
                #consultaEmpleado
                consultaEmpleado = Empleados.objects.filter(id_empleado = idEmpleado)
                for datoEmpleado in consultaEmpleado:
                    nombreCompletoEmpleado = datoEmpleado.nombre + " "+ datoEmpleado.apellidos
                    idArea = datoEmpleado.id_area_id
                    consultaArea = Areas.objects.filter(id_area = idArea)
                    for datoArea in consultaArea:
                        nombreArea = datoArea.nombre
                        colorArea = datoArea.color

                listaPermisosFalta.append([idPermiso, nombreCompletoEmpleado, nombreArea, colorArea, motivoPermiso])

            #CONSULTA DE FALTAS DIRECTAS DE ESE DIA ------------------------------------------------
            consultaFaltasDirectas = FaltasAsistencia.objects.filter(fecha = fechaDiaReporte)

            if consultaFaltasDirectas:
                for falta in consultaFaltasDirectas:
                    idFalta = falta.id_falta_asistencia
                    idEmpleado = falta.id_empleado_id
                    motivoFalta = falta.observaciones
                
                #consultaEmpleado
                consultaEmpleado = Empleados.objects.filter(id_empleado = idEmpleado)
                for datoEmpleado in consultaEmpleado:
                    nombreCompletoEmpleado = datoEmpleado.nombre + " "+ datoEmpleado.apellidos
                    idArea = datoEmpleado.id_area_id
                    consultaArea = Areas.objects.filter(id_area = idArea)
                    for datoArea in consultaArea:
                        nombreArea = datoArea.nombre
                        colorArea = datoArea.color

                listaFaltas.append([idFalta, nombreCompletoEmpleado, nombreArea, colorArea, motivoFalta])

            #CONSULTA DE ASISTENCIA FORANEA
            consultaAsistenciaForaneaDeEseDia = AsistenciaProyectoForaneo.objects.filter(fecha = fechaDiaReporte)
            
            if consultaAsistenciaForanea:
                for asistenciaForanea in consultaAsistenciaForaneaDeEseDia:
                    idAsistencia = asistenciaForanea.id_asistencia_proyecto_foraneo
                    idEmpleado = asistenciaForanea.id_empleado_id
                    
                    #Si es personal externo..
                    if idEmpleado == None:
                        nombreCompletoEmpleado = asistenciaForanea.personal_externo
                        nombreArea = ""
                        colorArea = ""
                    else:
                        #datos de empleado
                        consultaEmpleado = Empleados.objects.filter(id_empleado = idEmpleado)
                        for datoEmpleado in consultaEmpleado:
                            nombreCompletoEmpleado = datoEmpleado.nombre + " "+ datoEmpleado.apellidos
                            idArea = datoEmpleado.id_area_id
                            consultaArea = Areas.objects.filter(id_area = idArea)
                            for datoArea in consultaArea:
                                nombreArea = datoArea.nombre
                                colorArea = datoArea.color

                    horaEntrada = asistenciaForanea.hora_entrada
                    horaSalida = asistenciaForanea.hora_salida
                    proyectoInterno = asistenciaForanea.proyecto_interno_id
                    
                    actividadesRealizadas = asistenciaForanea.actividades_realizadas
                    
                    if proyectoInterno == None:
                        proyectoInterno = ""
                        motivoAsistencia = asistenciaForanea.motivo
                    else:
                        #Consulta de proyecto
                        consultaProyecto = Proyectos.objects.filter(id_proyecto = proyectoInterno)
                        
                        if consultaProyecto:
                            for datoProyecto in consultaProyecto:
                                numeroInternoProyecto = datoProyecto.numero_proyecto_interno
                                nombreProyecto = datoProyecto.nombre_proyecto
                                
                        proyectoInterno = "# "+numeroInternoProyecto+" - "+nombreProyecto
                        motivoAsistencia = ""


                    #Consulta de horas extras. 
                    consultaHorasExtrasForaneas = HorasExtrasForaneas.objects.filter(id_asitencia_foraneas_id = idAsistencia)

                    if consultaHorasExtrasForaneas:
                        tieneHorasExtras = "SI"
                        for datoHoraExtra in consultaHorasExtrasForaneas:
                            numeroHorasExtras = datoHoraExtra.numero_horas_extras

                        listaHorasExtrasForaneas.append([idAsistencia, nombreCompletoEmpleado, nombreArea,
                        colorArea, horaEntrada, horaSalida, proyectoInterno, numeroHorasExtras])
                    else:
                        tieneHorasExtras = "NO"
                        numeroHorasExtras = ""


                    listaAsistenciaForanea.append([idAsistencia, nombreCompletoEmpleado, nombreArea, colorArea,
                                                   horaEntrada, horaSalida, proyectoInterno, tieneHorasExtras, numeroHorasExtras, motivoAsistencia, actividadesRealizadas])

                    listaEmpleadosConAsistenciaPerfectaOficina.append([nombreCompletoEmpleado, nombreArea, colorArea, proyectoInterno])
        
        return render(request,"empleadosCustom/Asistencia/Asistencia/reportes/reporteDiario.html",{"estaEnAsistencias":estaEnAsistencias,"estaEnReporteAsistencia":estaEnReporteAsistencia ,"id_admin":id_admin,"nombre":nombre,"apellidos":apellidos,"correo":correo,"nombreCompleto":nombreCompleto,"almacen":almacen,"foto":foto, "rh":rh,
                                                                                              "fechaDiaReporte":fechaDiaReporte,"asistenciaPerfecta":asistenciaPerfecta,"retardos":retardos,
                                                                                              "salidasAntes":salidasAntes,"permisosFalta":permisosFalta, "faltasDirectas":faltasDirectas,
                                                                                              "horasExtras":horasExtras, "listaAsistencia":listaAsistencia, "listaRetardos":listaRetardos, "listaIncidenciasLlegadasTardias":listaIncidenciasLlegadasTardias,
                                                                                              "listaSalidasTEmpranas":listaSalidasTEmpranas, "listaIncidenciasSalidasTempranas":listaIncidenciasSalidasTempranas,
                                                                                              "listaIncidenciasSalidasFuera":listaIncidenciasSalidasFuera, "listaPermisosFalta":listaPermisosFalta,
                                                                                              "listaFaltas":listaFaltas, "listaHorasExtras":listaHorasExtras, "listaEmpleadosConAsistenciaPerfectaOficina":listaEmpleadosConAsistenciaPerfectaOficina,
                                                                                              "listaAsistenciaForanea":listaAsistenciaForanea, "listaHorasExtrasForaneas":listaHorasExtrasForaneas})

    
    else:
        return redirect('/login/')


def reporteExcelAsistenciaDiaria(request):
    if "idSesion" in request.session:
        fechaAsistenciaDiaria = request.POST["fechaDiaReporte"]

        consultaAsistenciasDeEseDia = Asistencia.objects.filter(fecha = fechaAsistenciaDiaria)

        listaDeAsistenciaParaExcel = []

        if consultaAsistenciasDeEseDia:
            
            for asistencia in consultaAsistenciasDeEseDia:

                idAsistencia = asistencia.id_asistencia

                idEmpleado = asistencia.id_empleado_id

                #Consulta de datos de empleado

                consultaEmpleado = Empleados.objects.filter(id_empleado = idEmpleado)
                for datoEmpleado in consultaEmpleado:
                    nombreCompletoEmpleado = datoEmpleado.nombre + " "+datoEmpleado.apellidos
                    areaEmpleado = datoEmpleado.id_area_id

                    consultaAreaEmpleado = Areas.objects.filter(id_area = areaEmpleado)
                    for dato in consultaAreaEmpleado:
                        nombreArea = dato.nombre

                horaEntrada = asistencia.hora_entrada
                horaEntradaStr = horaEntrada + " hrs."

                retardo = asistencia.retardo

                stringRetardo = ""
                if retardo == "SI":
                    stringRetardo = "Si,"
                    #Checar si tiene incidencia
                    consultaIncidenciaLlegadaTardia = IncidenciaLlegadaTardia.objects.filter(id_asitencia_id = idAsistencia)
                    if consultaIncidenciaLlegadaTardia:
                        stringRetardo = stringRetardo +" con permiso"

                    else:
                        stringRetardo = stringRetardo + " sin permiso"
                else:
                    stringRetardo = "Entrada a tiempo"

                horaSalida = asistencia.hora_salida
                salidaATiempo = asistencia.a_tiempo

                salidaATiempoStr = ""
                if horaSalida == "na":
                    horaSalidaStr = "Sin salida aún"
                    salidaATiempoStr = "No aplica"
                    salidaFuera = "No aplica"
                else:
                    horaSalidaStr = str(horaSalida) + " hrs."

                    if salidaATiempo == "SI":
                        salidaATiempoStr = "A tiempo"

                        #Consultar si tiene salida por fuera
                        consultaIncidenciaSalidaPorFuera = IncidenciaSalidaFuera.objects.filter(id_asitencia_id = idAsistencia)
                        if consultaIncidenciaSalidaPorFuera:
                            salidaFuera = "Salida Fuera de oficina"

                        else:
                            salidaFuera = "Salida en oficina"

                    else:
                        salidaATiempoStr = "Salida temprana"

                        salidaFuera = "Salida en oficina"

                        #Checar si tiene incidencia
                        consultaIncidenciaSalidaTemprana = IncidenciaSalidaTemprana.objects.filter(id_asitencia_id = idAsistencia)
                        
                        if consultaIncidenciaSalidaTemprana:
                            salidaATiempoStr = salidaATiempoStr + ", con permiso"

                        else:
                            salidaATiempoStr = salidaATiempoStr + ", sin permiso"

                #Ver si tiene horas extras.  
                consultaHorasExtras = HorasExtras.objects.filter(id_asitencia_id = idAsistencia)

                if consultaHorasExtras:
                    for datoHorasExtras in consultaHorasExtras:
                        numeroHorasExtras = datoHorasExtras.numero_horas_extras


                    horasExtrasStr = str(numeroHorasExtras)+" horas extras"
                else:
                    horasExtrasStr = "Sin horas extras"


                listaDeAsistenciaParaExcel.append([idAsistencia, nombreCompletoEmpleado, nombreArea,horaEntradaStr,
                                                   stringRetardo, horaSalidaStr, salidaATiempoStr,salidaFuera, horasExtrasStr])


        #Consulta de permisos de falta 
        consultaPermisosFalta = PermisosAsistencia.objects.filter(fecha = fechaAsistenciaDiaria)
        listaPermisosFalta = []

        for permiso in consultaPermisosFalta:
            idPermiso = permiso.id_permiso_asistencia
            idEmpleado = permiso.id_empleado_id

            consultaEmpleado = Empleados.objects.filter(id_empleado = idEmpleado)
            for datoEmpleado in consultaEmpleado:
                nombreCompletoEmpleado = datoEmpleado.nombre + " "+datoEmpleado.apellidos
                areaEmpleado = datoEmpleado.id_area_id

                consultaAreaEmpleado = Areas.objects.filter(id_area = areaEmpleado)
                for dato in consultaAreaEmpleado:
                    nombreArea = dato.nombre


            motivo = permiso.motivo

            listaPermisosFalta.append([idPermiso, nombreCompletoEmpleado, nombreArea, motivo])

        #Consulta de faltas directas
        consultaFaltasDirectas = FaltasAsistencia.objects.filter(fecha = fechaAsistenciaDiaria)
        listaFaltasDirectas = []

        for falta in consultaFaltasDirectas:
            idFalta = falta.id_falta_asistencia
            idEmpleado = falta.id_empleado_id

            consultaEmpleado = Empleados.objects.filter(id_empleado = idEmpleado)
            for datoEmpleado in consultaEmpleado:
                nombreCompletoEmpleado = datoEmpleado.nombre + " "+datoEmpleado.apellidos
                areaEmpleado = datoEmpleado.id_area_id

                consultaAreaEmpleado = Areas.objects.filter(id_area = areaEmpleado)
                for dato in consultaAreaEmpleado:
                    nombreArea = dato.nombre

            observaciones = falta.observaciones

            listaFaltasDirectas.append([idFalta, nombreCompletoEmpleado, nombreArea, observaciones])

              

        #METODO PARA EXPORTAR A EXCEL.
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename=Reporte de asistencia diario -'+str(datetime.today().strftime('%Y-%m-%d'))+'.xls'
        
        #creación de libro de excel
        libro = xlwt.Workbook(encoding='utf-8')
        hoja = libro.add_sheet('Asistencia')
        
        numero_fila = 0
        estilo_fuente = xlwt.XFStyle()
        estilo_fuente.font.bold = True
        
        columnas = ['Id Asistencia','Empleado', 'Departamento', 'Hora de entrada', 'Retardo', 'Hora de salida', 'Salida antes', 'Salida fuera', 'Horas Extras?']
        for columna in range(len(columnas)):
            hoja.write(numero_fila, columna, columnas[columna], estilo_fuente)
            
        
            
        estilo_fuente = xlwt.XFStyle()
        for asistencia in listaDeAsistenciaParaExcel:
            numero_fila+=1
            for columna in range(len(asistencia)):
                hoja.write(numero_fila, columna, str(asistencia[columna]), estilo_fuente)
        #Hoja de permisos de falta
        hojaPermisosFalta = libro.add_sheet('Permisos Falta')
        
        numero_fila = 0
        estilo_fuente = xlwt.XFStyle()
        estilo_fuente.font.bold = True
        
        columnas = ['Id permiso','Empleado', 'Departamento', 'Motivo']
        for columna in range(len(columnas)):
            hojaPermisosFalta.write(numero_fila, columna, columnas[columna], estilo_fuente)
            
        
                
            
        estilo_fuente = xlwt.XFStyle()
        for permisito in listaPermisosFalta:
            numero_fila+=1
            for columna in range(len(permisito)):
                hojaPermisosFalta.write(numero_fila, columna, str(permisito[columna]), estilo_fuente)

        #Hoja de faltas directas
        hojaFaltasDirectas = libro.add_sheet('Faltas directas')
        
        numero_fila = 0
        estilo_fuente = xlwt.XFStyle()
        estilo_fuente.font.bold = True
        
        columnas = ['Id permiso','Empleado', 'Departamento', 'Observaciones']
        for columna in range(len(columnas)):
            hojaFaltasDirectas.write(numero_fila, columna, columnas[columna], estilo_fuente)
            
        
                
            
        estilo_fuente = xlwt.XFStyle()
        for faltita in listaFaltasDirectas:
            numero_fila+=1
            for columna in range(len(faltita)):
                hojaFaltasDirectas.write(numero_fila, columna, str(faltita[columna]), estilo_fuente)
            


        
        libro.save(response)
        return response    

    else:
        return redirect('/login/')  


def reporteExcelAsistenciaForaneaDiaria(request):
    if "idSesion" in request.session:
        fechaAsistenciaDiaria = request.POST["fechaDiaReporte"]

        consultaAsistenciaForaneaDeEseDia = AsistenciaProyectoForaneo.objects.filter(fecha = fechaAsistenciaDiaria)

        listaDeAsistenciaParaExcel = []

        if consultaAsistenciaForaneaDeEseDia:
            
            for asistencia in consultaAsistenciaForaneaDeEseDia:

                idAsistencia = asistencia.id_asistencia_proyecto_foraneo

                idEmpleado = asistencia.id_empleado_id

                if idEmpleado == None:
                    nombreCompletoEmpleado = asistencia.personal_externo
                    nombreArea = "Personal externo"
                else:
                    #Consulta de datos de empleado

                    consultaEmpleado = Empleados.objects.filter(id_empleado = idEmpleado)
                    for datoEmpleado in consultaEmpleado:
                        nombreCompletoEmpleado = datoEmpleado.nombre + " "+datoEmpleado.apellidos
                        areaEmpleado = datoEmpleado.id_area_id

                        consultaAreaEmpleado = Areas.objects.filter(id_area = areaEmpleado)
                        for dato in consultaAreaEmpleado:
                            nombreArea = dato.nombre

                horaEntrada = asistencia.hora_entrada
                horaEntradaStr = horaEntrada + " hrs."
                horaSalida = asistencia.hora_salida
                horaSalidaStr = horaSalida + " hrs."
                
                proyecto = asistencia.proyecto_interno_id
                
                if proyecto == None:
                    proyecto = asistencia.motivo
                else:
                    #Consulta de proyecto
                    consultaProyecto = Proyectos.objects.filter(id_proyecto = proyecto)
                    
                    if consultaProyecto:
                        for datoProyecto in consultaProyecto:
                            numeroInternoProyecto = datoProyecto.numero_proyecto_interno
                            nombreProyecto = datoProyecto.nombre_proyecto
                            
                    proyecto = "# "+numeroInternoProyecto+" - "+nombreProyecto


                #Ver si tiene horas extras.  
                consultaHorasExtras = HorasExtrasForaneas.objects.filter(id_asitencia_foraneas_id = idAsistencia)

                if consultaHorasExtras:
                    for datoHorasExtras in consultaHorasExtras:
                        numeroHorasExtras = datoHorasExtras.numero_horas_extras


                    horasExtrasStr = str(numeroHorasExtras)+" horas extras"
                else:
                    horasExtrasStr = "Sin horas extras"


                listaDeAsistenciaParaExcel.append([idAsistencia, nombreCompletoEmpleado, nombreArea,horaEntradaStr,
                                                horaSalidaStr,proyecto, horasExtrasStr])

        #Consulta de permisos de falta 
        consultaPermisosFalta = PermisosAsistencia.objects.filter(fecha = fechaAsistenciaDiaria)
        listaPermisosFalta = []

        for permiso in consultaPermisosFalta:
            idPermiso = permiso.id_permiso_asistencia
            idEmpleado = permiso.id_empleado_id

            consultaEmpleado = Empleados.objects.filter(id_empleado = idEmpleado)
            for datoEmpleado in consultaEmpleado:
                nombreCompletoEmpleado = datoEmpleado.nombre + " "+datoEmpleado.apellidos
                areaEmpleado = datoEmpleado.id_area_id

                consultaAreaEmpleado = Areas.objects.filter(id_area = areaEmpleado)
                for dato in consultaAreaEmpleado:
                    nombreArea = dato.nombre


            motivo = permiso.motivo

            listaPermisosFalta.append([idPermiso, nombreCompletoEmpleado, nombreArea, motivo])

        #Consulta de faltas directas
        consultaFaltasDirectas = FaltasAsistencia.objects.filter(fecha = fechaAsistenciaDiaria)
        listaFaltasDirectas = []

        for falta in consultaFaltasDirectas:
            idFalta = falta.id_falta_asistencia
            idEmpleado = falta.id_empleado_id

            consultaEmpleado = Empleados.objects.filter(id_empleado = idEmpleado)
            for datoEmpleado in consultaEmpleado:
                nombreCompletoEmpleado = datoEmpleado.nombre + " "+datoEmpleado.apellidos
                areaEmpleado = datoEmpleado.id_area_id

                consultaAreaEmpleado = Areas.objects.filter(id_area = areaEmpleado)
                for dato in consultaAreaEmpleado:
                    nombreArea = dato.nombre

            observaciones = falta.observaciones

            listaFaltasDirectas.append([idFalta, nombreCompletoEmpleado, nombreArea, observaciones])


        #METODO PARA EXPORTAR A EXCEL.
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename=Reporte de asistencia foranea diario -'+str(datetime.today().strftime('%Y-%m-%d'))+'.xls'
        
        #creación de libro de excel
        libro = xlwt.Workbook(encoding='utf-8')

        #Hoja de asistencias
        hoja = libro.add_sheet('Asistencia')
        
        numero_fila = 0
        estilo_fuente = xlwt.XFStyle()
        estilo_fuente.font.bold = True
        
        columnas = ['Id Asistencia','Empleado', 'Departamento', 'Hora de entrada', 'Hora de salida', 'Proyecto/Actividad', 'Horas Extras?']
        for columna in range(len(columnas)):
            hoja.write(numero_fila, columna, columnas[columna], estilo_fuente)
            
        
                
            
        estilo_fuente = xlwt.XFStyle()
        for asistencia in listaDeAsistenciaParaExcel:
            numero_fila+=1
            for columna in range(len(asistencia)):
                hoja.write(numero_fila, columna, str(asistencia[columna]), estilo_fuente)

        #Hoja de permisos de falta
        hojaPermisosFalta = libro.add_sheet('Permisos Falta')
        
        numero_fila = 0
        estilo_fuente = xlwt.XFStyle()
        estilo_fuente.font.bold = True
        
        columnas = ['Id permiso','Empleado', 'Departamento', 'Motivo']
        for columna in range(len(columnas)):
            hojaPermisosFalta.write(numero_fila, columna, columnas[columna], estilo_fuente)
            
        
                
            
        estilo_fuente = xlwt.XFStyle()
        for permisito in listaPermisosFalta:
            numero_fila+=1
            for columna in range(len(permisito)):
                hojaPermisosFalta.write(numero_fila, columna, str(permisito[columna]), estilo_fuente)

        #Hoja de faltas directas
        hojaFaltasDirectas = libro.add_sheet('Faltas directas')
        
        numero_fila = 0
        estilo_fuente = xlwt.XFStyle()
        estilo_fuente.font.bold = True
        
        columnas = ['Id permiso','Empleado', 'Departamento', 'Observaciones']
        for columna in range(len(columnas)):
            hojaFaltasDirectas.write(numero_fila, columna, columnas[columna], estilo_fuente)
            
        
                
            
        estilo_fuente = xlwt.XFStyle()
        for faltita in listaFaltasDirectas:
            numero_fila+=1
            for columna in range(len(faltita)):
                hojaFaltasDirectas.write(numero_fila, columna, str(faltita[columna]), estilo_fuente)
            
        
        libro.save(response)
        return response    

    else:
        return redirect('/login/')  

    

def reporteAsistenciaSemanal(request):
    if "idSesion" in request.session:
        estaEnAsistencias = True
        estaEnReporteAsistencia = True

        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        if correo == "almacen01@customco.com.mx":
            almacen = True
        else:
            almacen = False

        if correo == "recursos.humanos@customco.com.mx":
            rh = True
        else:
            rh = False

        nombreCompleto = nombre + " " + apellidos
        
        foto = fotoAdmin(request)

        #Aqui se empieza

        if request.method == "POST":
            fechaDesde = request.POST["fechaDesde"]
            fechaHasta = request.POST["fechaHasta"]

            fechaDesdeParaComparar = datetime.strptime(fechaDesde, '%Y-%m-%d')
            fechaHastaParaComparar = datetime.strptime(fechaHasta, '%Y-%m-%d')
            

            #Fechas iguales
            if fechaDesdeParaComparar == fechaHastaParaComparar:
                request.session["errorEnFecha"] = "Las fechas elegidas son las mismas!"\
                
                return redirect("/reporteAsistencia/")
            
            #Fecha desde es mayor
            elif fechaDesdeParaComparar > fechaHastaParaComparar:
                request.session["errorEnFecha"] = "La fecha 'desde' es mayor a la de 'hasta' !"\
                
                return redirect("/reporteAsistencia/")
            
            #Fechas bien elegidas
            else:

                #Asistencia perfecta
                if request.POST.get("asistenciaPerfectaSemana", False): #Checkeado
                    asistenciaPerfectaVer = True
                elif request.POST.get("asistenciaPerfectaSemana", True): #No checkeado
                    asistenciaPerfectaVer = False

                #Retardos
                if request.POST.get("retardosSemana", False): #Checkeado
                    retardos = True
                elif request.POST.get("retardosSemana", True): #No checkeado
                    retardos = False

                #Salidas tempranas
                if request.POST.get("salidasTempranasSemana", False): #Checkeado
                    salidasAntes = True
                elif request.POST.get("salidasTempranasSemana", True): #No checkeado
                    salidasAntes = False


                #Permisos de falta
                if request.POST.get("permisosFaltaSemana", False): #Checkeado
                    permisosFalta = True
                elif request.POST.get("permisosFaltaSemana", True): #No checkeado
                    permisosFalta = False

                #Faltas directas
                if request.POST.get("faltasDirectasSemana", False): #Checkeado
                    faltasDirectas = True
                elif request.POST.get("faltasDirectasSemana", True): #No checkeado
                    faltasDirectas = False

                #Horas extras
                if request.POST.get("horasExtrasSemana", False): #Checkeado
                    horasExtras = True
                elif request.POST.get("horasExtrasSemana", True): #No checkeado
                    horasExtras = False


                #lista de fechas!
                diferenciaDiasEntreFechas = fechaHastaParaComparar-fechaDesdeParaComparar
                diferenciaDiasEntreFechas = diferenciaDiasEntreFechas.days
                listaFechas = []
                listaFechasStr = []
                contadorFechas = 0
                for dia in range(diferenciaDiasEntreFechas+1):
                    contadorFechas = contadorFechas + 1
                    if contadorFechas == 1: #primer dia
                        listaFechas.append(fechaDesdeParaComparar)
                        
                        fechaDate = fechaDesdeParaComparar.date()
                        fechaChida = datetime.strftime(fechaDate,'%d-%m-%Y')
                        listaFechasStr.append(fechaChida)
                        
                    else:#Cualquier otro dia
                        numerito = contadorFechas - 1
                        fechaSiguiente = fechaDesdeParaComparar + timedelta(days=numerito)
                        if fechaSiguiente <= fechaHastaParaComparar:
                            listaFechas.append(fechaSiguiente)
                            
                            fechaDate = fechaSiguiente.date()
                            fechaChida = datetime.strftime(fechaDate,'%d-%m-%Y')
                            listaFechasStr.append(fechaChida)

                #PRIMERO, SACAR TODA LA LISTA DE EMPLEADOS CON ASISTENCIA EN OFICINA
                listaEmpleadosOficina = []
                
                consultaEmpleadosActivo = Empleados.objects.filter(activo = "A", correo__icontains = "@customco.com.mx")
                for empleado in consultaEmpleadosActivo:
                    idEmpleado = empleado.id_empleado
                    listaEmpleadosOficina.append(idEmpleado)

                #LISTAS DE ASISTENCIA DE LA OFICINA SOLAMENTE..
                listaAsistenciaEmpleadosOficina = [] 
                listaNombresEmpleadosOficina = []
                
                listaEmpleadosConAsistenciaPerfecta = []
                listaEmpleadosConRetardos = []
                listaEmpleadosConSalidasTempranas = []
                
                #Faltas
                listaEmpleadosConFaltasConPermiso = []
                listaEmpleadosConFaltaDirecta = []
                
                listaHorasExtrasOficina = []
                listaHorasExtrasForaneas = []

                #ASISTENCIA EN OFICINA, RECORRER POR EMPLEADO..
                for empleadoOficina in listaEmpleadosOficina:
                    idEmpleado = int(empleadoOficina)

                    #Info de empleado.
                    consultaEmpleado = Empleados.objects.filter(id_empleado = idEmpleado)
                    for datoEmpleado in consultaEmpleado:
                        nombreCompletoEmpleado = datoEmpleado.nombre + " "+ datoEmpleado.apellidos
                        idArea = datoEmpleado.id_area_id
                        consultaArea = Areas.objects.filter(id_area = idArea)
                        for datoArea in consultaArea:
                            nombreArea = datoArea.nombre
                            colorArea = datoArea.color
                    
                    listaNombresEmpleadosOficina.append([nombreCompletoEmpleado, nombreArea, colorArea])

                    asistenciaEmpleado = []
                    
                    asistenciaPerfecta = True
                    
                    empleadoConRetardo = False
                    infoRetardoEmpleado = []
                    numeroRetardosEmpleado = 0
                    numeroRetardosEmpleadoConPermiso = 0
                    
                    empleadoConSalidaTemprana = False
                    infoSalidaTemprana = []
                    numeroSalidasTempranasEmpleado = 0
                    numeroSalidasTEmpranasEmpleadoConPermiso = 0
                    
                    empleadoConFaltaConPermiso = False
                    infoFaltaEmpleadoConPermiso = []
                    numeroFaltasEmpleadoConPermiso = 0
                    
                    empleadoConFaltaDirecta = False
                    infoFaltaDirectaEmpleado = []
                    numeroFaltasDirectasEmpleado = 0
                    
                    empleadoTieneHorasExtrasEnOficina = False
                    infoHorasExtrasEmpleadoOficina = []
                    horasExtrasTotalesEmpleadoOficina = 0
                    
                    empleadoTieneHorasExtrasForaneas = False
                    infoHorasExtrasEmpleadoForaneas = []
                    horasExtrasTotalesEmpleadoForaneas = 0

                    #Hacer for que recorra cada una de las fechas de la lista
                    for fecha in listaFechas:
                        fechaAConsultar = fecha
                        

                        consultaEmpleadoFecha = Asistencia.objects.filter(fecha = fechaAConsultar, id_empleado_id = idEmpleado)
                        consultaEmpleadoFechaForanea = AsistenciaProyectoForaneo.objects.filter(fecha = fechaAConsultar, id_empleado_id = idEmpleado)
                        if consultaEmpleadoFecha:
                            for datosAsistenciaEmpleado in consultaEmpleadoFecha:
                                idAsistencia = datosAsistenciaEmpleado.id_asistencia
                                horaEntrada = datosAsistenciaEmpleado.hora_entrada
                                retardo= datosAsistenciaEmpleado.retardo
                                horaSalida = datosAsistenciaEmpleado.hora_salida
                                aTiempo = datosAsistenciaEmpleado.a_tiempo

                                #ENTRADA
                                if retardo == "NO":
                                    estatusRetardo = "Sin retardo"
                                else:
                                    #Consulta para ver incidencia 
                                    consultaIncidenciaLlegadaTardia = IncidenciaLlegadaTardia.objects.filter(id_asitencia_id = idAsistencia)
                                    if consultaIncidenciaLlegadaTardia:
                                        estatusRetardo = "Retardo, con permiso"
                                        asistenciaPerfecta = False
                                        empleadoConRetardo = True
                                        numeroRetardosEmpleadoConPermiso  = numeroRetardosEmpleadoConPermiso +1
                                        for dato in consultaIncidenciaLlegadaTardia:
                                            motivo = dato.motivo
                                        infoRetardoEmpleado.append([horaEntrada, fechaAConsultar, motivo])
                                    else:
                                        estatusRetardo = "Sin incidencia"
                                        asistenciaPerfecta = False
                                        empleadoConRetardo = True
                                        numeroRetardosEmpleado  = numeroRetardosEmpleado +1
                                        infoRetardoEmpleado.append([horaEntrada, fechaAConsultar, "SinMotivo"])
                                
                                #SALIDA
                                if horaSalida == "na":
                                    horaSalida = "No reportó salida"
                                    estatusSalida = "na"
                                    asistenciaPerfecta = False
                                else:
                                    if aTiempo == "SI":
                                        consultaIncidenciaSalidaPorFuera = IncidenciaSalidaFuera.objects.filter(id_asitencia_id = idAsistencia)
                                        if consultaIncidenciaSalidaPorFuera:
                                            estatusSalida = "Salida fuera"
                                            asistenciaPerfecta = False
                                        else:
                                            estatusSalida = "Salida a tiempo"
                                    else:
                                        consultaIncidenciaSalidaTemprana = IncidenciaSalidaTemprana.objects.filter(id_asitencia_id = idAsistencia)
                                        if consultaIncidenciaSalidaTemprana:
                                            estatusSalida = "Salida antes, con permiso"
                                            asistenciaPerfecta = False
                                            
                                            empleadoConSalidaTemprana = True
                                            numeroSalidasTEmpranasEmpleadoConPermiso = numeroSalidasTEmpranasEmpleadoConPermiso + 1
                                            
                                            for dato in consultaIncidenciaSalidaTemprana:
                                                motivo = dato.motivo
                                            
                                            infoSalidaTemprana.append([horaSalida, fechaAConsultar, motivo])
                                        else:
                                            estatusSalida = "Salida antes, sin permiso"
                                            asistenciaPerfecta = False
                                            
                                            empleadoConSalidaTemprana = True
                                            numeroSalidasTempranasEmpleado = numeroSalidasTempranasEmpleado + 1
                                            infoSalidaTemprana.append([horaSalida, fechaAConsultar, "SinPermiso"])


                                #Hora extra
                                consultaHorasExtras = HorasExtras.objects.filter(id_asitencia_id = idAsistencia)

                                if consultaHorasExtras:
                                    for horaExtra in consultaHorasExtras:
                                        numeroHorasExtras = horaExtra.numero_horas_extras
                                    estatusHorasExtras = str(numeroHorasExtras)
                                    
                                    empleadoTieneHorasExtrasEnOficina = True
                                    horasExtrasTotalesEmpleadoOficina = horasExtrasTotalesEmpleadoOficina + numeroHorasExtras
                                    infoHorasExtrasEmpleadoOficina.append([fechaAConsultar, horaSalida, estatusHorasExtras])
                                    
                                    
                                    
                                else:
                                    estatusHorasExtras = "na"

                            asistenciaEmpleado.append(["tieneAsistencia",horaEntrada,retardo,estatusRetardo, horaSalida, aTiempo, estatusSalida, estatusHorasExtras])
                        elif consultaEmpleadoFechaForanea:
                            for datosAsistenciaEmpleado in consultaEmpleadoFechaForanea:
                                idAsistencia = datosAsistenciaEmpleado.id_asistencia_proyecto_foraneo
                                horaEntrada = datosAsistenciaEmpleado.hora_entrada
                                horaSalida = datosAsistenciaEmpleado.hora_salida
                                proyecto = datosAsistenciaEmpleado.proyecto_interno_id
                                
                                if proyecto == None:
                                    proyecto = datosAsistenciaEmpleado.motivo
                                else:
                                    #Consulta de proyecto
                                    consultaProyecto = Proyectos.objects.filter(id_proyecto = proyecto)
                                    
                                    if consultaProyecto:
                                        for datoProyecto in consultaProyecto:
                                            numeroInternoProyecto = datoProyecto.numero_proyecto_interno
                                            nombreProyecto = datoProyecto.nombre_proyecto
                                            
                                    proyecto = "# "+numeroInternoProyecto+" - "+nombreProyecto

                                #Hora extra
                                consultaHorasExtras = HorasExtrasForaneas.objects.filter(id_asitencia_foraneas = idAsistencia)

                                if consultaHorasExtras:
                                    for horaExtra in consultaHorasExtras:
                                        numeroHorasExtras = horaExtra.numero_horas_extras
                                    estatusHorasExtras = str(numeroHorasExtras)
                                    
                                    empleadoTieneHorasExtrasForaneas = True
                                    horasExtrasTotalesEmpleadoForaneas = horasExtrasTotalesEmpleadoForaneas + numeroHorasExtras
                                    infoHorasExtrasEmpleadoForaneas.append([fechaAConsultar,horaEntrada, horaSalida, proyecto, estatusHorasExtras])
                                    
                                    
                                else:
                                    estatusHorasExtras = "na"

                            asistenciaEmpleado.append(["tieneAsistenciaForanea",horaEntrada, horaSalida,proyecto, estatusHorasExtras])
                        else:
                            #Verificar si hay algun permiso de falta o falta.
                            consultaPermisoFalta = PermisosAsistencia.objects.filter(fecha = fechaAConsultar, id_empleado_id = idEmpleado)

                            consultaFaltaDirecta = FaltasAsistencia.objects.filter(fecha = fechaAConsultar, id_empleado_id = idEmpleado)

                            if consultaPermisoFalta:
                                for datoPermisoFalta in consultaPermisoFalta:
                                    motivoPermiso = datoPermisoFalta.motivo
                                asistenciaEmpleado.append(["permisoFalta", motivoPermiso])
                                asistenciaPerfecta = False
                                
                                empleadoConFaltaConPermiso = True
                                numeroFaltasEmpleadoConPermiso = numeroFaltasEmpleadoConPermiso + 1
                                infoFaltaEmpleadoConPermiso.append([fechaAConsultar, motivoPermiso])
                                
                                
                            elif consultaFaltaDirecta:
                                for datoFalta in consultaFaltaDirecta:
                                    observaciones = datoFalta.observaciones
                                asistenciaEmpleado.append(["faltaDirecta", observaciones])
                                asistenciaPerfecta = False
                                
                                empleadoConFaltaDirecta = True
                                numeroFaltasDirectasEmpleado = numeroFaltasDirectasEmpleado + 1
                                infoFaltaDirectaEmpleado.append([fechaAConsultar, observaciones])
                            else:
                                asistenciaEmpleado.append(["nada", "nada", "nada", "nada", "nada","nada", "nada"])
                                
                    #Checar asistencia perfecta.
                    if asistenciaPerfecta == True:
                        listaEmpleadosConAsistenciaPerfecta.append([nombreCompletoEmpleado, nombreArea, colorArea])
                    
                    if empleadoConRetardo == True:
                        listaEmpleadosConRetardos.append([nombreCompletoEmpleado, nombreArea, colorArea, numeroRetardosEmpleado, numeroRetardosEmpleadoConPermiso, infoRetardoEmpleado])
                        
                    if empleadoConSalidaTemprana == True:
                        listaEmpleadosConSalidasTempranas.append([nombreCompletoEmpleado, nombreArea, colorArea,numeroSalidasTempranasEmpleado, numeroSalidasTEmpranasEmpleadoConPermiso,infoSalidaTemprana ])
                    
                    if empleadoConFaltaConPermiso == True:
                        listaEmpleadosConFaltasConPermiso.append([nombreCompletoEmpleado, nombreArea, colorArea, numeroFaltasEmpleadoConPermiso, infoFaltaEmpleadoConPermiso])
                    
                    if empleadoConFaltaDirecta == True:
                        listaEmpleadosConFaltaDirecta.append([nombreCompletoEmpleado, nombreArea, colorArea,numeroFaltasDirectasEmpleado,infoFaltaDirectaEmpleado])
                    
                    if empleadoTieneHorasExtrasEnOficina == True:
                        listaHorasExtrasOficina.append([nombreCompletoEmpleado, nombreArea, colorArea,horasExtrasTotalesEmpleadoOficina, infoHorasExtrasEmpleadoOficina])

                    if empleadoTieneHorasExtrasForaneas == True:
                        listaHorasExtrasForaneas.append([nombreCompletoEmpleado, nombreArea, colorArea, horasExtrasTotalesEmpleadoForaneas,infoHorasExtrasEmpleadoForaneas ])
                        
                   
                   
                    #Se agrega la lista de ese empleado a la lista de todos los empleados
                    listaAsistenciaEmpleadosOficina.append(asistenciaEmpleado)

                listaAsistenciaZipeada = zip(listaNombresEmpleadosOficina, listaAsistenciaEmpleadosOficina)
                    
                



                

        return render(request,"empleadosCustom/Asistencia/Asistencia/reportes/reporteSemanal.html",{"estaEnAsistencias":estaEnAsistencias,"estaEnReporteAsistencia":estaEnReporteAsistencia ,"id_admin":id_admin,"nombre":nombre,"apellidos":apellidos,"correo":correo,"nombreCompleto":nombreCompleto,"almacen":almacen,"foto":foto, "rh":rh,
                                                                                              "listaAsistenciaZipeada":listaAsistenciaZipeada, "fechaDesde":fechaDesde, "fechaHasta":fechaHasta, "listaFechas":listaFechas, "listaFechasStr":listaFechasStr,
                                                                                              "asistenciaPerfectaVer":asistenciaPerfectaVer, "listaEmpleadosConAsistenciaPerfecta":listaEmpleadosConAsistenciaPerfecta,
                                                                                              "retardos":retardos,"listaEmpleadosConRetardos":listaEmpleadosConRetardos,
                                                                                              "salidasAntes":salidasAntes, "listaEmpleadosConSalidasTempranas":listaEmpleadosConSalidasTempranas,
                                                                                              "permisosFalta":permisosFalta, "listaEmpleadosConFaltasConPermiso":listaEmpleadosConFaltasConPermiso,
                                                                                              "faltasDirectas":faltasDirectas, "listaEmpleadosConFaltaDirecta":listaEmpleadosConFaltaDirecta,
                                                                                              "horasExtras":horasExtras, "listaHorasExtrasOficina":listaHorasExtrasOficina,
                                                                                              "listaHorasExtrasForaneas":listaHorasExtrasForaneas})

    
    else:
        return redirect('/login/')
    
    
    
def reporteExcelAsistenciaSemanal(request):
    if "idSesion" in request.session:
        fechaDesde = request.POST["fechaDesde"]
        fechaHasta = request.POST["fechaHasta"]

        fechaDesdeParaComparar = datetime.strptime(fechaDesde, '%Y-%m-%d')
        fechaHastaParaComparar = datetime.strptime(fechaHasta, '%Y-%m-%d')

        columnas = ['Empleado', 'Departamento']
        
        #lista de fechas!
        diferenciaDiasEntreFechas = fechaHastaParaComparar-fechaDesdeParaComparar
        diferenciaDiasEntreFechas = diferenciaDiasEntreFechas.days
        listaFechas = []
        listaFechasStr = []
        contadorFechas = 0
        for dia in range(diferenciaDiasEntreFechas+1):
            contadorFechas = contadorFechas + 1
            if contadorFechas == 1: #primer dia
                listaFechas.append(fechaDesdeParaComparar)
                
                fechaDate = fechaDesdeParaComparar.date()
                fechaChida = datetime.strftime(fechaDate,'%d-%m-%Y')
                listaFechasStr.append(fechaChida)
                
            else:#Cualquier otro dia
                numerito = contadorFechas - 1
                fechaSiguiente = fechaDesdeParaComparar + timedelta(days=numerito)
                if fechaSiguiente <= fechaHastaParaComparar:
                    listaFechas.append(fechaSiguiente)
                    
                    fechaDate = fechaSiguiente.date()
                    fechaChida = datetime.strftime(fechaDate,'%d-%m-%Y')
                    listaFechasStr.append(fechaChida)
            columnas.append(fechaChida)

        #PRIMERO, SACAR TODA LA LISTA DE EMPLEADOS CON ASISTENCIA EN OFICINA
        listaEmpleadosOficina = []
        
        consultaEmpleadosActivo = Empleados.objects.filter(activo = "A", correo__icontains = "@customco.com.mx")
        for empleado in consultaEmpleadosActivo:
            idEmpleado = empleado.id_empleado
            listaEmpleadosOficina.append(idEmpleado)

        #LISTAS DE ASISTENCIA DE LA OFICINA SOLAMENTE..
        listaAsistenciaEmpleadosOficina = [] 
        listaFaltasConPermiso = []
        listaFaltasDirectas = []
        
        
        

        #ASISTENCIA EN OFICINA, RECORRER POR EMPLEADO..
        for empleadoOficina in listaEmpleadosOficina:
            idEmpleado = int(empleadoOficina)

            #Info de empleado.
            consultaEmpleado = Empleados.objects.filter(id_empleado = idEmpleado)
            for datoEmpleado in consultaEmpleado:
                idEmpleado = datoEmpleado.id_empleado
                nombreCompletoEmpleado = datoEmpleado.nombre + " "+ datoEmpleado.apellidos
                idArea = datoEmpleado.id_area_id
                consultaArea = Areas.objects.filter(id_area = idArea)
                for datoArea in consultaArea:
                    nombreArea = datoArea.nombre
            
            
            
            asistenciaEmpleado = []
            asistenciaEmpleado.append(nombreCompletoEmpleado)
            asistenciaEmpleado.append(nombreArea)
            
            
            
            #Hacer for que recorra cada una de las fechas de la lista
            
            contadorFecha = 1
            for fecha in listaFechas:
                fechaAConsultar = fecha
                

                consultaEmpleadoFecha = Asistencia.objects.filter(fecha = fechaAConsultar, id_empleado_id = idEmpleado)
                consultaEmpleadoFechaAsistenciaForanea = AsistenciaProyectoForaneo.objects.filter(fecha = fechaAConsultar, id_empleado_id = idEmpleado)
                
                if consultaEmpleadoFecha:
                    for datosAsistenciaEmpleado in consultaEmpleadoFecha:
                        idAsistencia = datosAsistenciaEmpleado.id_asistencia
                        horaEntrada = datosAsistenciaEmpleado.hora_entrada
                        retardo= datosAsistenciaEmpleado.retardo
                        horaSalida = datosAsistenciaEmpleado.hora_salida
                        aTiempo = datosAsistenciaEmpleado.a_tiempo

                        
                        
                        #ENTRADA
                        if retardo == "NO":
                            estatusRetardo = "Sin retardo"
                        else:
                            #Consulta para ver incidencia 
                            consultaIncidenciaLlegadaTardia = IncidenciaLlegadaTardia.objects.filter(id_asitencia_id = idAsistencia)
                            if consultaIncidenciaLlegadaTardia:
                                estatusRetardo = "Retardo, con permiso"
                                
                            else:
                                estatusRetardo = "Sin permiso"
                                
                        
                        #SALIDA
                        if horaSalida == "na":
                            horaSalida = "No reportó salida"
                            estatusSalida = "na"
                        else:
                            if aTiempo == "SI":
                                consultaIncidenciaSalidaPorFuera = IncidenciaSalidaFuera.objects.filter(id_asitencia_id = idAsistencia)
                                if consultaIncidenciaSalidaPorFuera:
                                    estatusSalida = "Salida a tiempo por fuera"
                                else:
                                    estatusSalida = "Salida a tiempo"
                            else:
                                consultaIncidenciaSalidaTemprana = IncidenciaSalidaTemprana.objects.filter(id_asitencia_id = idAsistencia)
                                if consultaIncidenciaSalidaTemprana:
                                    estatusSalida = "Salida antes, con permiso"
                                else:
                                    estatusSalida = "Salida antes, sin permiso"
                                   


                        #Hora extra
                        consultaHorasExtras = HorasExtras.objects.filter(id_asitencia_id = idAsistencia)

                        if consultaHorasExtras:
                            for horaExtra in consultaHorasExtras:
                                numeroHorasExtras = horaExtra.numero_horas_extras
                            estatusHorasExtras = str(numeroHorasExtras) +" horas"
                            
                        else:
                            estatusHorasExtras = "Sin horas extras"
                            
                        
                    asistenciaEmpleado.append("EN OFICINA \nHora Entrada: "+horaEntrada+" hrs \nRetardo: "+retardo+"\nHora Salida: "+horaSalida+" hrs \nSalida a tiempo: "+aTiempo+" \nEstatus Salida: "+estatusSalida+" \n Horas Extras: "+estatusHorasExtras)
                           
                
                #Ver si tiene asistencia foranea
                elif consultaEmpleadoFechaAsistenciaForanea:
                    for dato in consultaEmpleadoFechaAsistenciaForanea:
                        idAsistencia = dato.id_asistencia_proyecto_foraneo
                        horaEntrada = dato.hora_entrada
                        horaSalida = dato.hora_salida
                        proyecto = dato.proyecto_interno_id
                        
                        if proyecto == None:
                            proyecto = dato.motivo
                        else:
                            
                            #Consulta de proyecto
                            consultaProyecto = Proyectos.objects.filter(id_proyecto = proyecto)
                            
                            if consultaProyecto:
                                for datoProyecto in consultaProyecto:
                                    numeroInternoProyecto = datoProyecto.numero_proyecto_interno
                                    nombreProyecto = datoProyecto.nombre_proyecto
                                    
                            proyecto = "# "+numeroInternoProyecto+" - "+nombreProyecto
                                
                        
                        #Consulta de horas extras.
                        consultaHorasExtras = HorasExtrasForaneas.objects.filter(id_asitencia_foraneas_id = idAsistencia)
                        
                        estatusHorasExtras = ""
                        
                        if consultaHorasExtras:
                            for datoHoras in consultaHorasExtras:
                                horasExtras = datoHoras.numero_horas_extras

                            estatusHorasExtras = str(horasExtras)+ " horas extras"
                        else:
                            estatusHorasExtras = "Sin horas extras"
                            
                        
                        
                        asistenciaEmpleado.append("FORANEA \nHora Entrada: "+horaEntrada+"hrs \nHora Salida: "+horaSalida+" hrs \nProyecto interno: "+proyecto+" \n Horas Extras: "+estatusHorasExtras)
                
                else:
                    #Verificar si hay algun permiso de falta o falta.
                    consultaPermisoFalta = PermisosAsistencia.objects.filter(fecha = fechaAConsultar, id_empleado_id = idEmpleado)

                    consultaFaltaDirecta = FaltasAsistencia.objects.filter(fecha = fechaAConsultar, id_empleado_id = idEmpleado)

                    if consultaPermisoFalta:
                        for datoPermisoFalta in consultaPermisoFalta:
                            motivoPermiso = datoPermisoFalta.motivo
                            idPermiso = datoPermisoFalta.id_permiso_asistencia
                            
                        listaFaltasConPermiso.append([idPermiso, nombreCompletoEmpleado, nombreArea, fechaAConsultar,motivoPermiso])
                        
                        asistenciaEmpleado.append("PERMISO FALTA \nMotivo permiso: "+motivoPermiso)
                    
                        
                    elif consultaFaltaDirecta:
                        for datoFalta in consultaFaltaDirecta:
                            observaciones = datoFalta.observaciones
                            idFaltaDirecta = datoFalta.id_falta_asistencia
                            
                        listaFaltasDirectas.append([idFaltaDirecta, nombreCompletoEmpleado, nombreArea, fechaAConsultar,observaciones])
                            
                        asistenciaEmpleado.append("FALTA DIRECTA \nObservaciones: "+observaciones)
                    
                        
                    else:
                        asistenciaEmpleado.append("Nada registrado")
            
            listaAsistenciaEmpleadosOficina.append(asistenciaEmpleado)            
        
            
            
            
        
        #METODO PARA EXPORTAR A EXCEL.
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename=Reporte de asistencia semanal - '+str(datetime.today().strftime('%Y-%m-%d'))+'.xls'
        
        #creación de libro de excel
        libro = xlwt.Workbook(encoding='utf-8')
        hoja = libro.add_sheet('Asistencia Semanal')
        
        borders = xlwt.Borders()
        borders.left = xlwt.Borders.THIN
        borders.right = xlwt.Borders.THIN
        borders.top = xlwt.Borders.THIN
        borders.bottom = xlwt.Borders.THIN

        
        numero_fila = 0
        estilo_fuente = xlwt.XFStyle()
        estilo_fuente.font.bold = True
        
       
        for columna in range(len(columnas)):
            if columna == 0 or columna == 1:
                hoja.col(columna).width = 100 * 100
            else:
                hoja.col(columna).width = 100 * 70
            hoja.write(numero_fila, columna, columnas[columna], estilo_fuente)
        
            
        estilo_fuente = xlwt.XFStyle()
        estilo_fuente.alignment.wrap = 1 
        for asistencia in listaAsistenciaEmpleadosOficina:
            numero_fila+=1
            for columna in range(len(asistencia)):
                
                if "EN OFICINA" in asistencia[columna]:
                    # Crear patrón de relleno sólido y asignarle un color verde
                    pattern = xlwt.Pattern()
                    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
                    pattern.pattern_fore_colour = xlwt.Style.colour_map['light_green']

                    # Asignar el patrón de relleno al estilo
                    estilo_fuente.pattern = pattern
                    
                elif "FORANEA" in asistencia[columna]:
                    # Crear patrón de relleno sólido y asignarle un color verde
                    pattern = xlwt.Pattern()
                    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
                    pattern.pattern_fore_colour = xlwt.Style.colour_map['pale_blue']

                    # Asignar el patrón de relleno al estilo
                    estilo_fuente.pattern = pattern
                    
                elif "PERMISO FALTA" in asistencia[columna]:
                    # Crear patrón de relleno sólido y asignarle un color verde
                    pattern = xlwt.Pattern()
                    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
                    pattern.pattern_fore_colour = xlwt.Style.colour_map['light_yellow']

                    # Asignar el patrón de relleno al estilo
                    estilo_fuente.pattern = pattern
                    
                elif "FALTA DIRECTA" in asistencia[columna]:
                    # Crear patrón de relleno sólido y asignarle un color verde
                    pattern = xlwt.Pattern()
                    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
                    pattern.pattern_fore_colour = xlwt.Style.colour_map['red']

                    # Asignar el patrón de relleno al estilo
                    estilo_fuente.pattern = pattern
                    
                elif "Nada registrado" in asistencia[columna]:
                    # Crear patrón de relleno sólido y asignarle un color verde
                    pattern = xlwt.Pattern()
                    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
                    pattern.pattern_fore_colour = xlwt.Style.colour_map['gray25']

                    # Asignar el patrón de relleno al estilo
                    estilo_fuente.pattern = pattern
                    
                else:
                    estilo_fuente = xlwt.XFStyle()
                    estilo_fuente.alignment.wrap = 1 
                    
                estilo_fuente.borders = borders
                hoja.write(numero_fila, columna, str(asistencia[columna]), estilo_fuente)
        #Hoja de permisos de falta
        hojaPermisosFalta = libro.add_sheet('Permisos Falta')
        
        numero_fila = 0
        estilo_fuente = xlwt.XFStyle()
        estilo_fuente.font.bold = True
        
        columnas = ['Id permiso','Empleado', 'Departamento','Fecha', 'Motivo']
        for columna in range(len(columnas)):
            if columna == 0 or columna == 1:
                hojaPermisosFalta.col(columna).width = 100 * 100
            else:
                hojaPermisosFalta.col(columna).width = 100 * 70
                
            hojaPermisosFalta.write(numero_fila, columna, columnas[columna], estilo_fuente)
            
        
                
            
        estilo_fuente = xlwt.XFStyle()
        for permisito in listaFaltasConPermiso:
            numero_fila+=1
            for columna in range(len(permisito)):
                estilo_fuente.borders = borders
                
                hojaPermisosFalta.write(numero_fila, columna, str(permisito[columna]), estilo_fuente)

        #Hoja de faltas directas
        hojaFaltasDirectas = libro.add_sheet('Faltas directas')
        
        numero_fila = 0
        estilo_fuente = xlwt.XFStyle()
        estilo_fuente.font.bold = True
        
        columnas = ['Id permiso','Empleado', 'Departamento', 'Fecha', 'Observaciones']
        for columna in range(len(columnas)):
            if columna == 0 or columna == 1:
                hojaFaltasDirectas.col(columna).width = 100 * 100
            else:
                hojaFaltasDirectas.col(columna).width = 100 * 70
                
            hojaFaltasDirectas.write(numero_fila, columna, columnas[columna], estilo_fuente)
            
        
                
            
        estilo_fuente = xlwt.XFStyle()
        for faltita in listaFaltasDirectas:
            numero_fila+=1
            for columna in range(len(faltita)):
                estilo_fuente.borders = borders
                hojaFaltasDirectas.write(numero_fila, columna, str(faltita[columna]), estilo_fuente)
            


        
        libro.save(response)
        return response    

    else:
        return redirect('/login/')  
    



def reporteAsistenciaMensual(request):
    if "idSesion" in request.session:
        estaEnAsistencias = True
        estaEnReporteAsistencia = True

        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        if correo == "almacen01@customco.com.mx":
            almacen = True
        else:
            almacen = False

        if correo == "recursos.humanos@customco.com.mx":
            rh = True
        else:
            rh = False

        nombreCompleto = nombre + " " + apellidos
        
        foto = fotoAdmin(request)

        #Aqui se empieza

        if request.method == "POST":
            mesAElegir = request.POST["mesAElegir"]
            anio = request.POST["anio"]
            
            dias = 0
            
            arregloMesesCon30Dias = ["01","03","05","07","08","10","12"]
            arregloMesesCon31Dias = ["04","06","09","11"]
            
            
            
            if mesAElegir in arregloMesesCon30Dias:
                dias = "30"
            elif mesAElegir in arregloMesesCon31Dias:
                dias = "31"
            else:
                dias = "28"
            
            principioMes = str(anio)+"-"+str(mesAElegir)+"-01"
            finMes = str(anio)+"-"+str(mesAElegir)+"-"+dias
            

            fechaDesdeParaComparar = datetime.strptime(principioMes, '%Y-%m-%d')
            fechaHastaParaComparar = datetime.strptime(finMes, '%Y-%m-%d')
            



            #Asistencia perfecta
            if request.POST.get("asistenciaPerfectaMensual", False): #Checkeado
                asistenciaPerfectaVer = True
            elif request.POST.get("asistenciaPerfectaMensual", True): #No checkeado
                asistenciaPerfectaVer = False

            #Retardos
            if request.POST.get("retardosMensual", False): #Checkeado
                retardos = True
            elif request.POST.get("retardosMensual", True): #No checkeado
                retardos = False

            #Salidas tempranas
            if request.POST.get("salidasTempranasMensual", False): #Checkeado
                salidasAntes = True
            elif request.POST.get("salidasTempranasMensual", True): #No checkeado
                salidasAntes = False


            #Permisos de falta
            if request.POST.get("permisosFaltaMensual", False): #Checkeado
                permisosFalta = True
            elif request.POST.get("permisosFaltaMensual", True): #No checkeado
                permisosFalta = False

            #Faltas directas
            if request.POST.get("faltasDirectasMensual", False): #Checkeado
                faltasDirectas = True
            elif request.POST.get("faltasDirectasMensual", True): #No checkeado
                faltasDirectas = False

            #Horas extras
            if request.POST.get("horasExtrasMensual", False): #Checkeado
                horasExtras = True
            elif request.POST.get("horasExtrasMensual", True): #No checkeado
                horasExtras = False
                
            
            #Variables de contadores
            
            numeroRetardos = 0
            numeroSalidasTempranas = 0
            numeroPermisosFaltas = 0
            numeroFaltasDirectas = 0


            #lista de fechas!
            diferenciaDiasEntreFechas = fechaHastaParaComparar-fechaDesdeParaComparar
            diferenciaDiasEntreFechas = diferenciaDiasEntreFechas.days
            listaFechas = []
            listaFechasStr = []
            contadorFechas = 0
            for dia in range(diferenciaDiasEntreFechas+1):
                contadorFechas = contadorFechas + 1
                if contadorFechas == 1: #primer dia
                    listaFechas.append(fechaDesdeParaComparar)
                    
                    fechaDate = fechaDesdeParaComparar.date()
                    fechaChida = datetime.strftime(fechaDate,'%d-%m-%Y')
                    listaFechasStr.append(fechaChida)
                    
                else:#Cualquier otro dia
                    numerito = contadorFechas - 1
                    fechaSiguiente = fechaDesdeParaComparar + timedelta(days=numerito)
                    if fechaSiguiente <= fechaHastaParaComparar:
                        listaFechas.append(fechaSiguiente)
                        
                        fechaDate = fechaSiguiente.date()
                        fechaChida = datetime.strftime(fechaDate,'%d-%m-%Y')
                        listaFechasStr.append(fechaChida)

            #PRIMERO, SACAR TODA LA LISTA DE EMPLEADOS CON ASISTENCIA EN OFICINA
            listaEmpleadosOficina = []
            
            consultaEmpleadosActivo = Empleados.objects.filter(activo = "A", correo__icontains = "@customco.com.mx")
            for empleado in consultaEmpleadosActivo:
                idEmpleado = empleado.id_empleado
                listaEmpleadosOficina.append(idEmpleado)

            #LISTAS DE ASISTENCIA DE LA OFICINA SOLAMENTE..
            listaAsistenciaEmpleadosOficina = [] 
            listaNombresEmpleadosOficina = []
            
            listaEmpleadosConAsistenciaPerfecta = []
            listaEmpleadosConRetardos = []
            listaEmpleadosConSalidasTempranas = []
            
            #Faltas
            listaEmpleadosConFaltasConPermiso = []
            listaEmpleadosConFaltaDirecta = []
            
            listaHorasExtrasOficina = []
            listaHorasExtrasForaneas = []

            #ASISTENCIA EN OFICINA, RECORRER POR EMPLEADO..
            for empleadoOficina in listaEmpleadosOficina:
                idEmpleado = int(empleadoOficina)

                #Info de empleado.
                consultaEmpleado = Empleados.objects.filter(id_empleado = idEmpleado)
                for datoEmpleado in consultaEmpleado:
                    nombreCompletoEmpleado = datoEmpleado.nombre + " "+ datoEmpleado.apellidos
                    idArea = datoEmpleado.id_area_id
                    consultaArea = Areas.objects.filter(id_area = idArea)
                    for datoArea in consultaArea:
                        nombreArea = datoArea.nombre
                        colorArea = datoArea.color
                
                listaNombresEmpleadosOficina.append([nombreCompletoEmpleado, nombreArea, colorArea])

                asistenciaEmpleado = []
                
                asistenciaPerfecta = True
                
                empleadoConRetardo = False
                infoRetardoEmpleado = []
                numeroRetardosEmpleado = 0
                numeroRetardosEmpleadoConPermiso = 0
                
                empleadoConSalidaTemprana = False
                infoSalidaTemprana = []
                numeroSalidasTempranasEmpleado = 0
                numeroSalidasTEmpranasEmpleadoConPermiso = 0
                
                empleadoConFaltaConPermiso = False
                infoFaltaEmpleadoConPermiso = []
                numeroFaltasEmpleadoConPermiso = 0
                
                empleadoConFaltaDirecta = False
                infoFaltaDirectaEmpleado = []
                numeroFaltasDirectasEmpleado = 0
                
                empleadoTieneHorasExtrasEnOficina = False
                infoHorasExtrasEmpleadoOficina = []
                horasExtrasTotalesEmpleadoOficina = 0
                
                empleadoTieneHorasExtrasForaneas = False
                infoHorasExtrasEmpleadoForaneas = []
                horasExtrasTotalesEmpleadoForaneas = 0

                #Hacer for que recorra cada una de las fechas de la lista
                for fecha in listaFechas:
                    fechaAConsultar = fecha
                    

                    consultaEmpleadoFecha = Asistencia.objects.filter(fecha = fechaAConsultar, id_empleado_id = idEmpleado)
                    consultaEmpleadoFechaForanea = AsistenciaProyectoForaneo.objects.filter(fecha = fechaAConsultar, id_empleado_id = idEmpleado)
                    if consultaEmpleadoFecha:
                        for datosAsistenciaEmpleado in consultaEmpleadoFecha:
                            idAsistencia = datosAsistenciaEmpleado.id_asistencia
                            horaEntrada = datosAsistenciaEmpleado.hora_entrada
                            retardo= datosAsistenciaEmpleado.retardo
                            horaSalida = datosAsistenciaEmpleado.hora_salida
                            aTiempo = datosAsistenciaEmpleado.a_tiempo

                            #ENTRADA
                            if retardo == "NO":
                                estatusRetardo = "Sin retardo"
                            else:
                                #Consulta para ver incidencia 
                                consultaIncidenciaLlegadaTardia = IncidenciaLlegadaTardia.objects.filter(id_asitencia_id = idAsistencia)
                                if consultaIncidenciaLlegadaTardia:
                                    estatusRetardo = "Retardo, con permiso"
                                    asistenciaPerfecta = False
                                    empleadoConRetardo = True
                                    numeroRetardosEmpleadoConPermiso  = numeroRetardosEmpleadoConPermiso +1
                                    for dato in consultaIncidenciaLlegadaTardia:
                                        motivo = dato.motivo
                                    infoRetardoEmpleado.append([horaEntrada, fechaAConsultar, motivo])
                                    
                                    numeroRetardos = numeroRetardos+1
                                else:
                                    estatusRetardo = "Sin incidencia"
                                    asistenciaPerfecta = False
                                    empleadoConRetardo = True
                                    numeroRetardosEmpleado  = numeroRetardosEmpleado +1
                                    infoRetardoEmpleado.append([horaEntrada, fechaAConsultar, "SinMotivo"])
                                    
                                    numeroRetardos = numeroRetardos+1
                            
                            #SALIDA
                            if horaSalida == "na":
                                horaSalida = "No reportó salida"
                                estatusSalida = "na"
                                asistenciaPerfecta = False
                            else:
                                if aTiempo == "SI":
                                    consultaIncidenciaSalidaPorFuera = IncidenciaSalidaFuera.objects.filter(id_asitencia_id = idAsistencia)
                                    if consultaIncidenciaSalidaPorFuera:
                                        estatusSalida = "Salida fuera"
                                        asistenciaPerfecta = False
                                    else:
                                        estatusSalida = "Salida a tiempo"
                                else:
                                    consultaIncidenciaSalidaTemprana = IncidenciaSalidaTemprana.objects.filter(id_asitencia_id = idAsistencia)
                                    if consultaIncidenciaSalidaTemprana:
                                        estatusSalida = "Salida antes, con permiso"
                                        asistenciaPerfecta = False
                                        
                                        empleadoConSalidaTemprana = True
                                        numeroSalidasTEmpranasEmpleadoConPermiso = numeroSalidasTEmpranasEmpleadoConPermiso + 1
                                        
                                        for dato in consultaIncidenciaSalidaTemprana:
                                            motivo = dato.motivo
                                        
                                        infoSalidaTemprana.append([horaSalida, fechaAConsultar, motivo])
                                        
                                        numeroSalidasTempranas = numeroSalidasTempranas + 1
                                    else:
                                        estatusSalida = "Salida antes, sin permiso"
                                        asistenciaPerfecta = False
                                        
                                        empleadoConSalidaTemprana = True
                                        numeroSalidasTempranasEmpleado = numeroSalidasTempranasEmpleado + 1
                                        infoSalidaTemprana.append([horaSalida, fechaAConsultar, "SinPermiso"])
                                        
                                        numeroSalidasTempranas = numeroSalidasTempranas + 1


                            #Hora extra
                            consultaHorasExtras = HorasExtras.objects.filter(id_asitencia_id = idAsistencia)

                            if consultaHorasExtras:
                                for horaExtra in consultaHorasExtras:
                                    numeroHorasExtras = horaExtra.numero_horas_extras
                                estatusHorasExtras = str(numeroHorasExtras)
                                
                                empleadoTieneHorasExtrasEnOficina = True
                                horasExtrasTotalesEmpleadoOficina = horasExtrasTotalesEmpleadoOficina + numeroHorasExtras
                                infoHorasExtrasEmpleadoOficina.append([fechaAConsultar, horaSalida, estatusHorasExtras])
                                
                                
                                
                            else:
                                estatusHorasExtras = "na"

                        asistenciaEmpleado.append(["tieneAsistencia",horaEntrada,retardo,estatusRetardo, horaSalida, aTiempo, estatusSalida, estatusHorasExtras])
                    elif consultaEmpleadoFechaForanea:
                        for datosAsistenciaEmpleado in consultaEmpleadoFechaForanea:
                            idAsistencia = datosAsistenciaEmpleado.id_asistencia_proyecto_foraneo
                            horaEntrada = datosAsistenciaEmpleado.hora_entrada
                            horaSalida = datosAsistenciaEmpleado.hora_salida
                            proyecto = datosAsistenciaEmpleado.proyecto_interno_id
                            
                            if proyecto == None:
                                proyecto = datosAsistenciaEmpleado.motivo
                            else:
                                
                                #Consulta de proyecto
                                consultaProyecto = Proyectos.objects.filter(id_proyecto = proyecto)
                                
                                if consultaProyecto:
                                    for datoProyecto in consultaProyecto:
                                        numeroInternoProyecto = datoProyecto.numero_proyecto_interno
                                        nombreProyecto = datoProyecto.nombre_proyecto
                                        
                                proyecto = "# "+numeroInternoProyecto+" - "+nombreProyecto
                        

                            #Hora extra
                            consultaHorasExtras = HorasExtrasForaneas.objects.filter(id_asitencia_foraneas = idAsistencia)

                            if consultaHorasExtras:
                                for horaExtra in consultaHorasExtras:
                                    numeroHorasExtras = horaExtra.numero_horas_extras
                                estatusHorasExtras = str(numeroHorasExtras)
                                
                                empleadoTieneHorasExtrasForaneas = True
                                horasExtrasTotalesEmpleadoForaneas = horasExtrasTotalesEmpleadoForaneas + numeroHorasExtras
                                infoHorasExtrasEmpleadoForaneas.append([fechaAConsultar,horaEntrada, horaSalida, proyecto, estatusHorasExtras])
                                
                                
                            else:
                                estatusHorasExtras = "na"

                        asistenciaEmpleado.append(["tieneAsistenciaForanea",horaEntrada, horaSalida,proyecto, estatusHorasExtras])
                    else:
                        #Verificar si hay algun permiso de falta o falta.
                        consultaPermisoFalta = PermisosAsistencia.objects.filter(fecha = fechaAConsultar, id_empleado_id = idEmpleado)

                        consultaFaltaDirecta = FaltasAsistencia.objects.filter(fecha = fechaAConsultar, id_empleado_id = idEmpleado)

                        if consultaPermisoFalta:
                            for datoPermisoFalta in consultaPermisoFalta:
                                motivoPermiso = datoPermisoFalta.motivo
                            asistenciaEmpleado.append(["permisoFalta", motivoPermiso])
                            asistenciaPerfecta = False
                            
                            empleadoConFaltaConPermiso = True
                            numeroFaltasEmpleadoConPermiso = numeroFaltasEmpleadoConPermiso + 1
                            infoFaltaEmpleadoConPermiso.append([fechaAConsultar, motivoPermiso])
                            
                            numeroPermisosFaltas = numeroPermisosFaltas+1
                            
                            
                        elif consultaFaltaDirecta:
                            for datoFalta in consultaFaltaDirecta:
                                observaciones = datoFalta.observaciones
                            asistenciaEmpleado.append(["faltaDirecta", observaciones])
                            asistenciaPerfecta = False
                            
                            empleadoConFaltaDirecta = True
                            numeroFaltasDirectasEmpleado = numeroFaltasDirectasEmpleado + 1
                            infoFaltaDirectaEmpleado.append([fechaAConsultar, observaciones])
                            
                            numeroFaltasDirectas = numeroFaltasDirectas + 1
                        else:
                            asistenciaEmpleado.append(["nada", "nada", "nada", "nada", "nada","nada", "nada"])
                            
                #Checar asistencia perfecta.
                if asistenciaPerfecta == True:
                    listaEmpleadosConAsistenciaPerfecta.append([nombreCompletoEmpleado, nombreArea, colorArea])
                
                if empleadoConRetardo == True:
                    listaEmpleadosConRetardos.append([nombreCompletoEmpleado, nombreArea, colorArea, numeroRetardosEmpleado, numeroRetardosEmpleadoConPermiso, infoRetardoEmpleado])
                    
                if empleadoConSalidaTemprana == True:
                    listaEmpleadosConSalidasTempranas.append([nombreCompletoEmpleado, nombreArea, colorArea,numeroSalidasTempranasEmpleado, numeroSalidasTEmpranasEmpleadoConPermiso,infoSalidaTemprana ])
                
                if empleadoConFaltaConPermiso == True:
                    listaEmpleadosConFaltasConPermiso.append([nombreCompletoEmpleado, nombreArea, colorArea, numeroFaltasEmpleadoConPermiso, infoFaltaEmpleadoConPermiso])
                
                if empleadoConFaltaDirecta == True:
                    listaEmpleadosConFaltaDirecta.append([nombreCompletoEmpleado, nombreArea, colorArea,numeroFaltasDirectasEmpleado,infoFaltaDirectaEmpleado])
                
                if empleadoTieneHorasExtrasEnOficina == True:
                    listaHorasExtrasOficina.append([nombreCompletoEmpleado, nombreArea, colorArea,horasExtrasTotalesEmpleadoOficina, infoHorasExtrasEmpleadoOficina])

                if empleadoTieneHorasExtrasForaneas == True:
                    listaHorasExtrasForaneas.append([nombreCompletoEmpleado, nombreArea, colorArea, horasExtrasTotalesEmpleadoForaneas,infoHorasExtrasEmpleadoForaneas ])
                    
                
                
                #Se agrega la lista de ese empleado a la lista de todos los empleados
                listaAsistenciaEmpleadosOficina.append(asistenciaEmpleado)

            listaAsistenciaZipeada = zip(listaNombresEmpleadosOficina, listaAsistenciaEmpleadosOficina)
                
            

        return render(request,"empleadosCustom/Asistencia/Asistencia/reportes/reporteMensual.html",{"estaEnAsistencias":estaEnAsistencias,"estaEnReporteAsistencia":estaEnReporteAsistencia ,"id_admin":id_admin,"nombre":nombre,"apellidos":apellidos,"correo":correo,"nombreCompleto":nombreCompleto,"almacen":almacen,"foto":foto, "rh":rh,
                                                                                              "listaAsistenciaZipeada":listaAsistenciaZipeada, "principioMes":principioMes, "finMes":finMes, "listaFechas":listaFechas, "listaFechasStr":listaFechasStr,
                                                                                              "asistenciaPerfectaVer":asistenciaPerfectaVer, "listaEmpleadosConAsistenciaPerfecta":listaEmpleadosConAsistenciaPerfecta,
                                                                                              "retardos":retardos,"listaEmpleadosConRetardos":listaEmpleadosConRetardos,
                                                                                              "salidasAntes":salidasAntes, "listaEmpleadosConSalidasTempranas":listaEmpleadosConSalidasTempranas,
                                                                                              "permisosFalta":permisosFalta, "listaEmpleadosConFaltasConPermiso":listaEmpleadosConFaltasConPermiso,
                                                                                              "faltasDirectas":faltasDirectas, "listaEmpleadosConFaltaDirecta":listaEmpleadosConFaltaDirecta,
                                                                                              "horasExtras":horasExtras, "listaHorasExtrasOficina":listaHorasExtrasOficina,
                                                                                              "listaHorasExtrasForaneas":listaHorasExtrasForaneas,
                                                                                              "numeroRetardos":numeroRetardos, "numeroSalidasTempranas":numeroSalidasTempranas,
                                                                                              "numeroPermisosFaltas":numeroPermisosFaltas,
                                                                                              "numeroFaltasDirectas":numeroFaltasDirectas})

    
    else:
        return redirect('/login/')
    
    
    
    
def reporteAsistenciaAnual(request):
    if "idSesion" in request.session:
        estaEnAsistencias = True
        estaEnReporteAsistencia = True

        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        if correo == "almacen01@customco.com.mx":
            almacen = True
        else:
            almacen = False

        if correo == "recursos.humanos@customco.com.mx":
            rh = True
        else:
            rh = False

        nombreCompleto = nombre + " " + apellidos
        
        foto = fotoAdmin(request)

        #Aqui se empieza

        if request.method == "POST":
            anio = request.POST["anio"]
            
            
            principioDeAnio = str(anio)+"-01-01"
            finDeAnio = str(anio)+"-12-31"
            

            fechaDesdeParaComparar = datetime.strptime(principioDeAnio, '%Y-%m-%d')
            fechaHastaParaComparar = datetime.strptime(finDeAnio, '%Y-%m-%d')
            



            #Asistencia perfecta
            if request.POST.get("asistenciaPerfectaAnual", False): #Checkeado
                asistenciaPerfectaVer = True
            elif request.POST.get("asistenciaPerfectaAnual", True): #No checkeado
                asistenciaPerfectaVer = False

            #Retardos
            if request.POST.get("retardosAnual", False): #Checkeado
                retardos = True
            elif request.POST.get("retardosAnual", True): #No checkeado
                retardos = False

            #Salidas tempranas
            if request.POST.get("salidasTempranasAnual", False): #Checkeado
                salidasAntes = True
            elif request.POST.get("salidasTempranasAnual", True): #No checkeado
                salidasAntes = False


            #Permisos de falta
            if request.POST.get("permisosFaltaAnual", False): #Checkeado
                permisosFalta = True
            elif request.POST.get("permisosFaltaAnual", True): #No checkeado
                permisosFalta = False

            #Faltas directas
            if request.POST.get("faltasDirectasAnual", False): #Checkeado
                faltasDirectas = True
            elif request.POST.get("faltasDirectasAnual", True): #No checkeado
                faltasDirectas = False

            #Horas extras
            if request.POST.get("horasExtrasAnual", False): #Checkeado
                horasExtras = True
            elif request.POST.get("horasExtrasAnual", True): #No checkeado
                horasExtras = False
                
            
            #Variables de contadores
            
            numeroRetardos = 0
            numeroSalidasTempranas = 0
            numeroPermisosFaltas = 0
            numeroFaltasDirectas = 0


            #lista de fechas!
            diferenciaDiasEntreFechas = fechaHastaParaComparar-fechaDesdeParaComparar
            diferenciaDiasEntreFechas = diferenciaDiasEntreFechas.days
            listaFechas = []
            listaFechasStr = []
            contadorFechas = 0
            for dia in range(diferenciaDiasEntreFechas+1):
                contadorFechas = contadorFechas + 1
                if contadorFechas == 1: #primer dia
                    listaFechas.append(fechaDesdeParaComparar)
                    
                    fechaDate = fechaDesdeParaComparar.date()
                    fechaChida = datetime.strftime(fechaDate,'%d-%m-%Y')
                    listaFechasStr.append(fechaChida)
                    
                else:#Cualquier otro dia
                    numerito = contadorFechas - 1
                    fechaSiguiente = fechaDesdeParaComparar + timedelta(days=numerito)
                    if fechaSiguiente <= fechaHastaParaComparar:
                        listaFechas.append(fechaSiguiente)
                        
                        fechaDate = fechaSiguiente.date()
                        fechaChida = datetime.strftime(fechaDate,'%d-%m-%Y')
                        listaFechasStr.append(fechaChida)

            #PRIMERO, SACAR TODA LA LISTA DE EMPLEADOS CON ASISTENCIA EN OFICINA
            listaEmpleadosOficina = []
            
            consultaEmpleadosActivo = Empleados.objects.filter(activo = "A", correo__icontains = "@customco.com.mx")
            for empleado in consultaEmpleadosActivo:
                idEmpleado = empleado.id_empleado
                listaEmpleadosOficina.append(idEmpleado)

            #LISTAS DE ASISTENCIA DE LA OFICINA SOLAMENTE..
            listaAsistenciaEmpleadosOficina = [] 
            listaNombresEmpleadosOficina = []
            
            listaEmpleadosConAsistenciaPerfecta = []
            listaEmpleadosConRetardos = []
            listaEmpleadosConSalidasTempranas = []
            
            #Faltas
            listaEmpleadosConFaltasConPermiso = []
            listaEmpleadosConFaltaDirecta = []
            
            listaHorasExtrasOficina = []
            listaHorasExtrasForaneas = []

            #ASISTENCIA EN OFICINA, RECORRER POR EMPLEADO..
            for empleadoOficina in listaEmpleadosOficina:
                idEmpleado = int(empleadoOficina)

                #Info de empleado.
                consultaEmpleado = Empleados.objects.filter(id_empleado = idEmpleado)
                for datoEmpleado in consultaEmpleado:
                    nombreCompletoEmpleado = datoEmpleado.nombre + " "+ datoEmpleado.apellidos
                    idArea = datoEmpleado.id_area_id
                    consultaArea = Areas.objects.filter(id_area = idArea)
                    for datoArea in consultaArea:
                        nombreArea = datoArea.nombre
                        colorArea = datoArea.color
                
                listaNombresEmpleadosOficina.append([nombreCompletoEmpleado, nombreArea, colorArea])

                
                asistenciaPerfecta = True
                
                empleadoConRetardo = False
                infoRetardoEmpleado = []
                numeroRetardosEmpleado = 0
                numeroRetardosEmpleadoConPermiso = 0
                
                empleadoConSalidaTemprana = False
                infoSalidaTemprana = []
                numeroSalidasTempranasEmpleado = 0
                numeroSalidasTEmpranasEmpleadoConPermiso = 0
                
                empleadoConFaltaConPermiso = False
                infoFaltaEmpleadoConPermiso = []
                numeroFaltasEmpleadoConPermiso = 0
                
                empleadoConFaltaDirecta = False
                infoFaltaDirectaEmpleado = []
                numeroFaltasDirectasEmpleado = 0
                
                empleadoTieneHorasExtrasEnOficina = False
                infoHorasExtrasEmpleadoOficina = []
                horasExtrasTotalesEmpleadoOficina = 0
                
                empleadoTieneHorasExtrasForaneas = False
                infoHorasExtrasEmpleadoForaneas = []
                horasExtrasTotalesEmpleadoForaneas = 0

                #Hacer for que recorra cada una de las fechas de la lista
                for fecha in listaFechas:
                    fechaAConsultar = fecha
                    

                    consultaEmpleadoFecha = Asistencia.objects.filter(fecha = fechaAConsultar, id_empleado_id = idEmpleado)
                    consultaEmpleadoFechaForanea = AsistenciaProyectoForaneo.objects.filter(fecha = fechaAConsultar, id_empleado_id = idEmpleado)
                    if consultaEmpleadoFecha:
                        for datosAsistenciaEmpleado in consultaEmpleadoFecha:
                            idAsistencia = datosAsistenciaEmpleado.id_asistencia
                            horaEntrada = datosAsistenciaEmpleado.hora_entrada
                            retardo= datosAsistenciaEmpleado.retardo
                            horaSalida = datosAsistenciaEmpleado.hora_salida
                            aTiempo = datosAsistenciaEmpleado.a_tiempo

                            #ENTRADA
                            if retardo == "NO":
                                estatusRetardo = "Sin retardo"
                            else:
                                #Consulta para ver incidencia 
                                consultaIncidenciaLlegadaTardia = IncidenciaLlegadaTardia.objects.filter(id_asitencia_id = idAsistencia)
                                if consultaIncidenciaLlegadaTardia:
                                    estatusRetardo = "Retardo, con permiso"
                                    asistenciaPerfecta = False
                                    empleadoConRetardo = True
                                    numeroRetardosEmpleadoConPermiso  = numeroRetardosEmpleadoConPermiso +1
                                    for dato in consultaIncidenciaLlegadaTardia:
                                        motivo = dato.motivo
                                    infoRetardoEmpleado.append([horaEntrada, fechaAConsultar, motivo])
                                    
                                    numeroRetardos = numeroRetardos+1
                                else:
                                    estatusRetardo = "Sin incidencia"
                                    asistenciaPerfecta = False
                                    empleadoConRetardo = True
                                    numeroRetardosEmpleado  = numeroRetardosEmpleado +1
                                    infoRetardoEmpleado.append([horaEntrada, fechaAConsultar, "SinMotivo"])
                                    
                                    numeroRetardos = numeroRetardos+1
                            
                            #SALIDA
                            if horaSalida == "na":
                                horaSalida = "No reportó salida"
                                estatusSalida = "na"
                                asistenciaPerfecta = False
                            else:
                                if aTiempo == "SI":
                                    consultaIncidenciaSalidaPorFuera = IncidenciaSalidaFuera.objects.filter(id_asitencia_id = idAsistencia)
                                    if consultaIncidenciaSalidaPorFuera:
                                        estatusSalida = "Salida fuera"
                                        asistenciaPerfecta = False
                                    else:
                                        estatusSalida = "Salida a tiempo"
                                else:
                                    consultaIncidenciaSalidaTemprana = IncidenciaSalidaTemprana.objects.filter(id_asitencia_id = idAsistencia)
                                    if consultaIncidenciaSalidaTemprana:
                                        estatusSalida = "Salida antes, con permiso"
                                        asistenciaPerfecta = False
                                        
                                        empleadoConSalidaTemprana = True
                                        numeroSalidasTEmpranasEmpleadoConPermiso = numeroSalidasTEmpranasEmpleadoConPermiso + 1
                                        
                                        for dato in consultaIncidenciaSalidaTemprana:
                                            motivo = dato.motivo
                                        
                                        infoSalidaTemprana.append([horaSalida, fechaAConsultar, motivo])
                                        
                                        numeroSalidasTempranas = numeroSalidasTempranas + 1
                                    else:
                                        estatusSalida = "Salida antes, sin permiso"
                                        asistenciaPerfecta = False
                                        
                                        empleadoConSalidaTemprana = True
                                        numeroSalidasTempranasEmpleado = numeroSalidasTempranasEmpleado + 1
                                        infoSalidaTemprana.append([horaSalida, fechaAConsultar, "SinPermiso"])
                                        
                                        numeroSalidasTempranas = numeroSalidasTempranas + 1


                            #Hora extra
                            consultaHorasExtras = HorasExtras.objects.filter(id_asitencia_id = idAsistencia)

                            if consultaHorasExtras:
                                for horaExtra in consultaHorasExtras:
                                    numeroHorasExtras = horaExtra.numero_horas_extras
                                estatusHorasExtras = str(numeroHorasExtras)
                                
                                empleadoTieneHorasExtrasEnOficina = True
                                horasExtrasTotalesEmpleadoOficina = horasExtrasTotalesEmpleadoOficina + numeroHorasExtras
                                infoHorasExtrasEmpleadoOficina.append([fechaAConsultar, horaSalida, estatusHorasExtras])
                                
                                
                                
                            else:
                                estatusHorasExtras = "na"

                    elif consultaEmpleadoFechaForanea:
                        for datosAsistenciaEmpleado in consultaEmpleadoFechaForanea:
                            idAsistencia = datosAsistenciaEmpleado.id_asistencia_proyecto_foraneo
                            horaEntrada = datosAsistenciaEmpleado.hora_entrada
                            horaSalida = datosAsistenciaEmpleado.hora_salida
                            proyecto = datosAsistenciaEmpleado.proyecto_interno_id
                            
                            if proyecto == None:
                                proyecto = datosAsistenciaEmpleado.motivo
                            else:
                                #Consulta de proyecto
                                consultaProyecto = Proyectos.objects.filter(id_proyecto = proyecto)
                                
                                if consultaProyecto:
                                    for datoProyecto in consultaProyecto:
                                        numeroInternoProyecto = datoProyecto.numero_proyecto_interno
                                        nombreProyecto = datoProyecto.nombre_proyecto
                                        
                                proyecto = "# "+numeroInternoProyecto+" - "+nombreProyecto

                            #Hora extra
                            consultaHorasExtras = HorasExtrasForaneas.objects.filter(id_asitencia_foraneas = idAsistencia)

                            if consultaHorasExtras:
                                for horaExtra in consultaHorasExtras:
                                    numeroHorasExtras = horaExtra.numero_horas_extras
                                estatusHorasExtras = str(numeroHorasExtras)
                                
                                empleadoTieneHorasExtrasForaneas = True
                                horasExtrasTotalesEmpleadoForaneas = horasExtrasTotalesEmpleadoForaneas + numeroHorasExtras
                                infoHorasExtrasEmpleadoForaneas.append([fechaAConsultar,horaEntrada, horaSalida, proyecto, estatusHorasExtras])
                                
                                
                            else:
                                estatusHorasExtras = "na"

                    else:
                        #Verificar si hay algun permiso de falta o falta.
                        consultaPermisoFalta = PermisosAsistencia.objects.filter(fecha = fechaAConsultar, id_empleado_id = idEmpleado)

                        consultaFaltaDirecta = FaltasAsistencia.objects.filter(fecha = fechaAConsultar, id_empleado_id = idEmpleado)

                        if consultaPermisoFalta:
                            for datoPermisoFalta in consultaPermisoFalta:
                                motivoPermiso = datoPermisoFalta.motivo
                            asistenciaPerfecta = False
                            
                            empleadoConFaltaConPermiso = True
                            numeroFaltasEmpleadoConPermiso = numeroFaltasEmpleadoConPermiso + 1
                            infoFaltaEmpleadoConPermiso.append([fechaAConsultar, motivoPermiso])
                            
                            numeroPermisosFaltas = numeroPermisosFaltas+1
                            
                            
                        elif consultaFaltaDirecta:
                            for datoFalta in consultaFaltaDirecta:
                                observaciones = datoFalta.observaciones
                            asistenciaPerfecta = False
                            
                            empleadoConFaltaDirecta = True
                            numeroFaltasDirectasEmpleado = numeroFaltasDirectasEmpleado + 1
                            infoFaltaDirectaEmpleado.append([fechaAConsultar, observaciones])
                            
                            numeroFaltasDirectas = numeroFaltasDirectas + 1
                        
                            
                #Checar asistencia perfecta.
                if asistenciaPerfecta == True:
                    listaEmpleadosConAsistenciaPerfecta.append([nombreCompletoEmpleado, nombreArea, colorArea])
                
                if empleadoConRetardo == True:
                    listaEmpleadosConRetardos.append([nombreCompletoEmpleado, nombreArea, colorArea, numeroRetardosEmpleado, numeroRetardosEmpleadoConPermiso, infoRetardoEmpleado])
                    
                if empleadoConSalidaTemprana == True:
                    listaEmpleadosConSalidasTempranas.append([nombreCompletoEmpleado, nombreArea, colorArea,numeroSalidasTempranasEmpleado, numeroSalidasTEmpranasEmpleadoConPermiso,infoSalidaTemprana ])
                
                if empleadoConFaltaConPermiso == True:
                    listaEmpleadosConFaltasConPermiso.append([nombreCompletoEmpleado, nombreArea, colorArea, numeroFaltasEmpleadoConPermiso, infoFaltaEmpleadoConPermiso])
                
                if empleadoConFaltaDirecta == True:
                    listaEmpleadosConFaltaDirecta.append([nombreCompletoEmpleado, nombreArea, colorArea,numeroFaltasDirectasEmpleado,infoFaltaDirectaEmpleado])
                
                if empleadoTieneHorasExtrasEnOficina == True:
                    listaHorasExtrasOficina.append([nombreCompletoEmpleado, nombreArea, colorArea,horasExtrasTotalesEmpleadoOficina, infoHorasExtrasEmpleadoOficina])

                if empleadoTieneHorasExtrasForaneas == True:
                    listaHorasExtrasForaneas.append([nombreCompletoEmpleado, nombreArea, colorArea, horasExtrasTotalesEmpleadoForaneas,infoHorasExtrasEmpleadoForaneas ])
                    
                
                
               
                
            

        return render(request,"empleadosCustom/Asistencia/Asistencia/reportes/reporteAnual.html",{"estaEnAsistencias":estaEnAsistencias,"estaEnReporteAsistencia":estaEnReporteAsistencia ,"id_admin":id_admin,"nombre":nombre,"apellidos":apellidos,"correo":correo,"nombreCompleto":nombreCompleto,"almacen":almacen,"foto":foto, "rh":rh,
                                                                                              "anio":anio, "listaFechasStr":listaFechasStr,
                                                                                              "asistenciaPerfectaVer":asistenciaPerfectaVer, "listaEmpleadosConAsistenciaPerfecta":listaEmpleadosConAsistenciaPerfecta,
                                                                                              "retardos":retardos,"listaEmpleadosConRetardos":listaEmpleadosConRetardos,
                                                                                              "salidasAntes":salidasAntes, "listaEmpleadosConSalidasTempranas":listaEmpleadosConSalidasTempranas,
                                                                                              "permisosFalta":permisosFalta, "listaEmpleadosConFaltasConPermiso":listaEmpleadosConFaltasConPermiso,
                                                                                              "faltasDirectas":faltasDirectas, "listaEmpleadosConFaltaDirecta":listaEmpleadosConFaltaDirecta,
                                                                                              "horasExtras":horasExtras, "listaHorasExtrasOficina":listaHorasExtrasOficina,
                                                                                              "listaHorasExtrasForaneas":listaHorasExtrasForaneas,
                                                                                              "numeroRetardos":numeroRetardos, "numeroSalidasTempranas":numeroSalidasTempranas,
                                                                                              "numeroPermisosFaltas":numeroPermisosFaltas,
                                                                                              "numeroFaltasDirectas":numeroFaltasDirectas})

    
    else:
        return redirect('/login/')
    
    
def reporteAsistenciaEmpleado(request):
    if "idSesion" in request.session:
        estaEnAsistencias = True
        estaEnReporteAsistencia = True

        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        if correo == "almacen01@customco.com.mx":
            almacen = True
        else:
            almacen = False

        if correo == "recursos.humanos@customco.com.mx":
            rh = True
        else:
            rh = False

        nombreCompleto = nombre + " " + apellidos
        
        foto = fotoAdmin(request)

        #Aqui se empieza
        if request.method=="POST":
            idEmpleado = request.POST["idEmpleado"]
            
            #FECHASSSSS
            
            fechaDesde = request.POST["fechaDesde"]
            fechaHasta = request.POST["fechaHasta"]
            
            fechaDesdeParaComparar = datetime.strptime(fechaDesde, '%Y-%m-%d')
            fechaHastaParaComparar = datetime.strptime(fechaHasta, '%Y-%m-%d')
            
            #lista de fechas!
            diferenciaDiasEntreFechas = fechaHastaParaComparar-fechaDesdeParaComparar
            diferenciaDiasEntreFechas = diferenciaDiasEntreFechas.days
            listaFechas = []
            listaFechasStr = []
            locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
            contadorFechas = 0
            for dia in range(diferenciaDiasEntreFechas+1):
                contadorFechas = contadorFechas + 1
                if contadorFechas == 1: #primer dia
                    listaFechas.append(fechaDesdeParaComparar)
                    
                    fechaDate = fechaDesdeParaComparar.date()
                    fechaChida = datetime.strftime(fechaDate,'%d-%m-%Y')
                    diaPalabra = fechaDate.strftime("%A")
                    listaFechasStr.append([fechaChida, diaPalabra])
                    
                    
                else:#Cualquier otro dia
                    numerito = contadorFechas - 1
                    fechaSiguiente = fechaDesdeParaComparar + timedelta(days=numerito)
                    if fechaSiguiente <= fechaHastaParaComparar:
                        listaFechas.append(fechaSiguiente)
                        
                        fechaDate = fechaSiguiente.date()
                        fechaChida = datetime.strftime(fechaDate,'%d-%m-%Y')
                        diaPalabra = fechaDate.strftime("%A")
                        listaFechasStr.append([fechaChida, diaPalabra])
            
            
                                              
            

            consultaEmpleado = Empleados.objects.filter(id_empleado = idEmpleado)

            for datoEmpleado in consultaEmpleado:
                nombreEmpleado = datoEmpleado.nombre + " " + datoEmpleado.apellidos
                idArea = datoEmpleado.id_area_id
                imagenEmpleado = datoEmpleado.imagen_empleado
                puestoEmpleado = datoEmpleado.puesto

            
            consultaAreaEmpleado = Areas.objects.filter(id_area = idArea)
            horarioEmpleado = ""
            for datoArea in consultaAreaEmpleado:
                nombreDepartamentoEmpleado = datoArea.nombre
                colorDepartamentoEmpleado = datoArea.color
            if idArea == 9:
                if puestoEmpleado == "Jefatura de Soporte Técnico":
                    horarioEmpleado = "8:00 - 17:30 PM"
                else:
                    horarioEmpleado = "8:00 - 17:00 PM"
            else:
                horarioEmpleado = "8:00 - 17 :30 PM"
                
            #Checar asistencia en ese rango de fechas
            
            numeroDeRetardos = 0
            numeroDePermmisosLlegarTarde = 0
            numeroDeSalidasTempranas = 0
            numeroDePermisosSalidasTempranas = 0
            numeroPermisoFaltas = 0
            numeroFaltasDirectas = 0
            
            numeroHorasExtrasHtml = 0
            
            listaRetardos = []
            listaPermisosRetardos = []
            listaSalidasTempranas = []
            listaPermisosSalidasTempranas = []
            listaPermisosFatla = []
            listaFaltasDirectas = []
            listaHorasExtrasEmpleado = []
            
            listaAsistenciaEmpleado = []
            
            
            for fecha in listaFechas:
                fechaAConsultar = fecha
                
                consultaEmpleadoFecha = Asistencia.objects.filter(fecha = fechaAConsultar, id_empleado_id = idEmpleado)
                consultaEmpleadoFechaForanea = AsistenciaProyectoForaneo.objects.filter(fecha = fechaAConsultar, id_empleado_id = idEmpleado)
                
                #Consulta de asistencia en oficina
                if consultaEmpleadoFecha:
                    for datosAsistenciaEmpleado in consultaEmpleadoFecha:
                        idAsistencia = datosAsistenciaEmpleado.id_asistencia
                        horaEntrada = datosAsistenciaEmpleado.hora_entrada
                        retardo= datosAsistenciaEmpleado.retardo
                        horaSalida = datosAsistenciaEmpleado.hora_salida
                        aTiempo = datosAsistenciaEmpleado.a_tiempo

                        #ENTRADA
                        if retardo == "NO":
                            estatusRetardo = "Sin retardo"
                        else:
                            
                            #Consulta para ver incidencia 
                            consultaIncidenciaLlegadaTardia = IncidenciaLlegadaTardia.objects.filter(id_asitencia_id = idAsistencia)
                            if consultaIncidenciaLlegadaTardia:
                                
                                for datoIncidencia in consultaIncidenciaLlegadaTardia:
                                    motivo = datoIncidencia.motivo
                                
                                numeroDePermmisosLlegarTarde = numeroDePermmisosLlegarTarde+1
                                listaPermisosRetardos.append([fechaAConsultar, horaEntrada, motivo])
                                estatusRetardo = "Retardo con permiso"
                            else:
                                numeroDeRetardos = numeroDeRetardos + 1
                                listaRetardos.append([fechaAConsultar, horaEntrada])
                                estatusRetardo = "Retardo sin permiso"
                              
                        #SALIDA
                        if horaSalida == "na":
                            horaSalida = "No reportó salida"
                            estatusSalida = "na"
                        else:
                            if aTiempo == "SI":
                                consultaIncidenciaSalidaPorFuera = IncidenciaSalidaFuera.objects.filter(id_asitencia_id = idAsistencia)
                                if consultaIncidenciaSalidaPorFuera:
                                    estatusSalida = "Salida fuera"
                                else:
                                    estatusSalida = "Salida a tiempo"
                            else: #Salida a destiempo
                                consultaIncidenciaSalidaTemprana = IncidenciaSalidaTemprana.objects.filter(id_asitencia_id = idAsistencia)
                                if consultaIncidenciaSalidaTemprana:
                                    numeroDePermisosSalidasTempranas = numeroDePermisosSalidasTempranas + 1
                                    
                                    
                                    for dato in consultaIncidenciaSalidaTemprana:
                                        motivo = dato.motivo
                                    
                                    listaPermisosSalidasTempranas.append([fechaAConsultar, horaSalida, motivo])
                                    estatusSalida = "Salida temprana, con permiso"
                                else: #Salio temprano sin permiso
                                    numeroDeSalidasTempranas = numeroDeSalidasTempranas + 1
                                    listaSalidasTempranas.append([fechaAConsultar, horaSalida])
                                    estatusSalida = "Salida temprana, sin permiso"
                                    


                        #Hora extra
                        consultaHorasExtras = HorasExtras.objects.filter(id_asitencia_id = idAsistencia)

                        if consultaHorasExtras:
                            for horaExtra in consultaHorasExtras:
                                numeroHorasExtras = horaExtra.numero_horas_extras
                            estatusHorasExtras = str(numeroHorasExtras)
                            
                            
                            numeroHorasExtrasHtml = numeroHorasExtrasHtml + numeroHorasExtras
                            listaHorasExtrasEmpleado.append(["Oficina",fechaAConsultar, horaEntrada, horaSalida, estatusHorasExtras])
                        else:
                            estatusHorasExtras = "Sin horas extras"
                        
                        listaAsistenciaEmpleado.append(["Oficina",horaEntrada,retardo,estatusRetardo,horaSalida,estatusSalida,estatusHorasExtras])  
                            

                elif consultaEmpleadoFechaForanea:
                    for datosAsistenciaEmpleado in consultaEmpleadoFechaForanea:
                        idAsistencia = datosAsistenciaEmpleado.id_asistencia_proyecto_foraneo
                        horaEntrada = datosAsistenciaEmpleado.hora_entrada
                        horaSalida = datosAsistenciaEmpleado.hora_salida
                        proyecto = datosAsistenciaEmpleado.proyecto_interno_id
                        
                        if proyecto == None:
                            proyecto = datosAsistenciaEmpleado.motivo
                        else:
                            
                            #Consulta de proyecto
                            consultaProyecto = Proyectos.objects.filter(id_proyecto = proyecto)
                            
                            if consultaProyecto:
                                for datoProyecto in consultaProyecto:
                                    numeroInternoProyecto = datoProyecto.numero_proyecto_interno
                                    nombreProyecto = datoProyecto.nombre_proyecto
                                    
                            proyecto = "# "+numeroInternoProyecto+" - "+nombreProyecto

                        #Hora extra
                        consultaHorasExtras = HorasExtrasForaneas.objects.filter(id_asitencia_foraneas = idAsistencia)

                        if consultaHorasExtras:
                            for horaExtra in consultaHorasExtras:
                                numeroHorasExtras = horaExtra.numero_horas_extras
                            estatusHorasExtras = str(numeroHorasExtras)
                            
                            numeroHorasExtrasHtml = numeroHorasExtrasHtml + numeroHorasExtras
                            listaHorasExtrasEmpleado.append(["Foranea",fechaAConsultar, horaEntrada, horaSalida, estatusHorasExtras,proyecto])
                            
                        else:
                            estatusHorasExtras = "na"
                            
                        listaAsistenciaEmpleado.append(["Foranea",horaEntrada,horaSalida,proyecto,estatusHorasExtras])  
                            

                else:
                    #Verificar si hay algun permiso de falta o falta.
                    consultaPermisoFalta = PermisosAsistencia.objects.filter(fecha = fechaAConsultar, id_empleado_id = idEmpleado)

                    consultaFaltaDirecta = FaltasAsistencia.objects.filter(fecha = fechaAConsultar, id_empleado_id = idEmpleado)

                    if consultaPermisoFalta:
                        numeroPermisoFaltas = numeroPermisoFaltas + 1
                        
                        for datoPermisoFalta in consultaPermisoFalta:
                            motivoPermiso = datoPermisoFalta.motivo
                            
                        listaPermisosFatla.append([fechaAConsultar,motivoPermiso])
                        
                        listaAsistenciaEmpleado.append(["Permiso de Falta",motivoPermiso])  
                        
                    elif consultaFaltaDirecta:
                        numeroFaltasDirectas = numeroFaltasDirectas + 1
                        
                        for datoFalta in consultaFaltaDirecta:
                            observaciones = datoFalta.observaciones
                            
                        listaFaltasDirectas.append([fechaAConsultar,observaciones])
                        
                        listaAsistenciaEmpleado.append(["Falta directa",observaciones])  
                        
                    else:
                        listaAsistenciaEmpleado.append("NA")  
                
                    
            



        

        return render(request,"empleadosCustom/Asistencia/Asistencia/reportes/reporteAsistenciaEmpleado.html",{"estaEnAsistencias":estaEnAsistencias,"estaEnReporteAsistencia":estaEnReporteAsistencia ,"id_admin":id_admin,"nombre":nombre,"apellidos":apellidos,"correo":correo,"nombreCompleto":nombreCompleto,"almacen":almacen,"foto":foto, "rh":rh,
                                      "nombreEmpleado":nombreEmpleado,"nombreDepartamentoEmpleado":nombreDepartamentoEmpleado,"colorDepartamentoEmpleado":colorDepartamentoEmpleado,"imagenEmpleado":imagenEmpleado,"puestoEmpleado":puestoEmpleado,"horarioEmpleado":horarioEmpleado, "fechaDesde":fechaDesde, "fechaHasta":fechaHasta,
                                      "numeroDeRetardos":numeroDeRetardos,"numeroDePermmisosLlegarTarde":numeroDePermmisosLlegarTarde,
                                      "numeroDeSalidasTempranas":numeroDeSalidasTempranas,"numeroDePermisosSalidasTempranas":numeroDePermisosSalidasTempranas,
                                      "numeroPermisoFaltas":numeroPermisoFaltas, "numeroFaltasDirectas":numeroFaltasDirectas,
                                      "numeroHorasExtrasHtml":numeroHorasExtrasHtml, "listaRetardos":listaRetardos,
                                      "listaPermisosRetardos":listaPermisosRetardos,"listaSalidasTempranas":listaSalidasTempranas,
                                      "listaPermisosSalidasTempranas":listaPermisosSalidasTempranas,
                                      "listaPermisosFatla":listaPermisosFatla,"listaFaltasDirectas":listaFaltasDirectas,
                                      "listaHorasExtrasEmpleado":listaHorasExtrasEmpleado, "listaAsistenciaEmpleado":listaAsistenciaEmpleado,
                                      "listaFechasStr":listaFechasStr, "idEmpleado":idEmpleado})

    
    else:
        return redirect('/login/')
    
    
def reporteAsistenciaProyecto(request):
    if "idSesion" in request.session:
        estaEnAsistencias = True
        estaEnReporteAsistencia = True

        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        if correo == "almacen01@customco.com.mx":
            almacen = True
        else:
            almacen = False

        if correo == "recursos.humanos@customco.com.mx":
            rh = True
        else:
            rh = False

        nombreCompleto = nombre + " " + apellidos
        
        foto = fotoAdmin(request)

        #Aqui se empieza
        if request.method=="POST":
            proyecto = request.POST["proyecto"]
            
            



        

        return render(request,"empleadosCustom/Asistencia/Asistencia/reportes/reporteAsistenciaEmpleado.html",{"estaEnAsistencias":estaEnAsistencias,"estaEnReporteAsistencia":estaEnReporteAsistencia ,"id_admin":id_admin,"nombre":nombre,"apellidos":apellidos,"correo":correo,"nombreCompleto":nombreCompleto,"almacen":almacen,"foto":foto, "rh":rh})

    
    else:
        return redirect('/login/')
    
    
def verProyectos(request):
    if "idSesion" in request.session:
        estaEnProyectos = True
        estaEnVerProyectos = True

        id_admin=request.session["idSesion"]
        nombre = request.session['nombres']
        apellidos = request.session['apellidos']
        correo = request.session['correoSesion']
        if correo == "almacen01@customco.com.mx":
            almacen = True
        else:
            almacen = False

        if correo == "recursos.humanos@customco.com.mx":
            rh = True
        else:
            rh = False

        nombreCompleto = nombre + " " + apellidos
        
        foto = fotoAdmin(request)

        #Aqui se empieza
        
        #Consulta y lista de proyectos
        
        consultaProyectos = Proyectos.objects.all()
       
        if "proyectoRegistrado" in request.session:
           proyectoRegistrado = request.session["proyectoRegistrado"]
           del request.session["proyectoRegistrado"]
           
           return render(request,"empleadosCustom/Asistencia/Asistencia/verProyectos.html",{"estaEnProyectos":estaEnProyectos,"estaEnVerProyectos":estaEnVerProyectos ,"id_admin":id_admin,"nombre":nombre,"apellidos":apellidos,"correo":correo,"nombreCompleto":nombreCompleto,"almacen":almacen,"foto":foto, "rh":rh,
                                                                                            "proyectoRegistrado":proyectoRegistrado, "consultaProyectos":consultaProyectos})
           
        
        if "proyectoYaExiste" in request.session:
            proyectoYaExiste = request.session["proyectoYaExiste"]
            del request.session["proyectoYaExiste"]
            
            return render(request,"empleadosCustom/Asistencia/Asistencia/verProyectos.html",{"estaEnProyectos":estaEnProyectos,"estaEnVerProyectos":estaEnVerProyectos ,"id_admin":id_admin,"nombre":nombre,"apellidos":apellidos,"correo":correo,"nombreCompleto":nombreCompleto,"almacen":almacen,"foto":foto, "rh":rh,
                                                                                             "proyectoYaExiste":proyectoYaExiste,  "consultaProyectos":consultaProyectos})
            


        

        return render(request,"empleadosCustom/Asistencia/Asistencia/verProyectos.html",{"estaEnProyectos":estaEnProyectos,"estaEnVerProyectos":estaEnVerProyectos ,"id_admin":id_admin,"nombre":nombre,"apellidos":apellidos,"correo":correo,"nombreCompleto":nombreCompleto,"almacen":almacen,"foto":foto, "rh":rh,
                                                                                        "consultaProyectos":consultaProyectos})

    
    else:
        return redirect('/login/')
    
def agregarProyecto(request):
    if "idSesion" in request.session:
        if request.method == "POST":
            
            numeroProyectoInterno = request.POST["numeroProyectoInterno"]
            nombreProyecto = request.POST["nombreProyecto"]
            nombreCliente = request.POST["nombreCliente"]
            lugarProyecto = request.POST["lugarProyecto"]
            
            #Verificar que el numero de proyecto interno no esté dentro de los proyectos
            proyectoYaExiste = False
            
            consultaProyectos = Proyectos.objects.all()
            listaProyectos = []
            
            if consultaProyectos:
                for proyecto in consultaProyectos:
                    numProyectoConsultado = proyecto.numero_proyecto_interno
                    listaProyectos.append(numProyectoConsultado)
                if numeroProyectoInterno in listaProyectos:
                    proyectoYaExiste = True
                else:
                    proyectoYaExiste = True
            else:
                proyectoYaExiste = False
                
            if proyectoYaExiste == False:
                
                registroProyecto = Proyectos(numero_proyecto_interno = numeroProyectoInterno,
                                             nombre_proyecto = nombreProyecto,
                                             cliente = nombreCliente,
                                             lugar = lugarProyecto)
                
                registroProyecto.save()
                
                if registroProyecto:
                    request.session["proyectoRegistrado"] = "El proyecto "+numeroProyectoInterno+" se ha registrado correctamente!"
                
                    return redirect("/verProyectos/")
            else:
                request.session["proyectoYaExiste"] = "El proyecto "+numeroProyectoInterno+" ya existe en la Base de datos!"
                
                return redirect("/verProyectos/")
            
    
    else:
        return redirect('/login/')
    