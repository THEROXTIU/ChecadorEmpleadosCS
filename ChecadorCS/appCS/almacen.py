#Librerías
from email.mime import text
from logging import info
import mimetypes
import os
import base64
from io  import BytesIO
from io import StringIO
from tkinter.tix import Tree
from typing import List

#Renderizado
from django.http import response
from django.http.response import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from reportlab import cmp
from django.views.generic import ListView
import json

#Importación de modelos
from appCS.models import Areas, Empleados, Equipos, Carta, Impresoras, Cartuchos, CalendarioMantenimiento, Programas, ProgramasArea, EquipoPrograma, Bitacora, Renovacion_Equipos, Renovacion_Impresoras, Preguntas, Encuestas, Respuestas, EncuestaEmpleadoResuelta, Mouses, Teclados, Monitores, HerramientasAlmacen, InstrumentosAlmacen, HerramientasAlmacenInactivas, PrestamosAlmacen, RequisicionCompraAlmacen, altasAlmacen, bajasAlmacen

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

def fotoAdmin(request):
    idadministrador=request.session["idSesion"]
    datosEmpleado = Empleados.objects.filter(id_empleado=idadministrador)
        
    for dato in datosEmpleado:
        foto = dato.imagen_empleado
        
    return foto

def solicitudesPendientesALM(request):
    
    #Si ya hay una sesión iniciada..
    if "idSesion" in request.session:
        
        
        estaEnAlmacen = True
        estaEnSolicitudesPendientes = True
        almacen = True
        administradordeVehiculos = True
        solicitantePrestamo = True


        id_admin=request.session["idSesion"]
        nombreini = request.session['nombres']
        apellidosini = request.session['apellidos']
        correo = request.session['correoSesion']

        if correo == "almacen01@customco.com.mx":
            almacen = True
        else:
            almacen=False


        foto = fotoAdmin(request)
        nombreCompleto = nombreini + " " + apellidosini #Blanca Yesenia Gaeta Talamantes
        
        solicitudesPendientes = PrestamosAlmacen.objects.filter(estatus="Pendiente")
        empleadosSolicitantes = []
        
        if solicitudesPendientes:
            for solicitud in solicitudesPendientes:
                
                #Herramientas
                herramientas = solicitud.id_herramientaInstrumento #Lista de herramientas 1,2
                arregloIndividualHerramientas = herramientas.split(",") #[1,2]
                
                codigos = []
                nombres = []
                descripciones = []
                for herramientaIndividual in arregloIndividualHerramientas:
                    
                    idHerramienta = int(herramientaIndividual)
                    
                    consultaHerramienta = HerramientasAlmacen.objects.filter(id_herramienta = idHerramienta)
                    
                    for dato in consultaHerramienta:
                        codigo = dato.codigo_herramienta
                        nombre = dato.nombre_herramienta
                        descripcion = dato.descripcion_herramienta
                    codigos.append(codigo)
                    nombres.append(nombre)
                    descripciones.append(descripciones)
                        
                
                # Cantidades
                cantidades = solicitud.cantidades_solicitadas
                arregloIndividualCantidades = cantidades.split(",")
                
                idEmpleadoSolicitante = solicitud.id_empleado_solicitante_id
                consultaEmpleado = Empleados.objects.filter(id_empleado = idEmpleadoSolicitante)
                for dato in consultaEmpleado:
                    nombreEmpleadoSolicitante = dato.nombre
                    apellidosEmpleadoSolicitante = dato.apellidos
                    
                    nombreCompletoEmpleadoSolicitante = nombreEmpleadoSolicitante + " " + apellidosEmpleadoSolicitante
                    empleadosSolicitantes.append(nombreCompletoEmpleadoSolicitante)
                
                
            arregloHerramientas = zip(codigos,nombres,descripciones, arregloIndividualCantidades)
            
            listaSolicitudesPendientes = zip(solicitudesPendientes,empleadosSolicitantes)
            

            if "prestamoEntregado" in request.session:
                prestamoEntregado = request.session["prestamoEntregado"]
                del request.session["prestamoEntregado"]
                return render(request, "empleadosCustom/almacen/solicitudesPendientes.html", {"solicitantePrestamo":solicitantePrestamo,"estaEnAlmacen":estaEnAlmacen,"estaEnSolicitudesPendientes":estaEnSolicitudesPendientes,"almacen":almacen,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo,
                                                                                        "arregloHerramientas":arregloHerramientas, "solicitudesPendientes":solicitudesPendientes, "listaSolicitudesPendientes":listaSolicitudesPendientes, "prestamoEntregado":prestamoEntregado, "almacen":almacen, "administradordeVehiculos":administradordeVehiculos})

            return render(request, "empleadosCustom/almacen/solicitudesPendientes.html", {"estaEnAlmacen":estaEnAlmacen,"estaEnSolicitudesPendientes":estaEnSolicitudesPendientes,"almacen":almacen,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo,
                                                                                        "arregloHerramientas":arregloHerramientas, "solicitudesPendientes":solicitudesPendientes, "listaSolicitudesPendientes":listaSolicitudesPendientes, "almacen":almacen, "administradordeVehiculos":administradordeVehiculos})
        else:
            sinPendientes = True
            if "prestamoEntregado" in request.session:
                prestamoEntregado = request.session["prestamoEntregado"]
                del request.session["prestamoEntregado"]    
                return render(request, "empleadosCustom/almacen/solicitudesPendientes.html", {"solicitantePrestamo":solicitantePrestamo,"estaEnAlmacen":estaEnAlmacen,"estaEnSolicitudesPendientes":estaEnSolicitudesPendientes,"almacen":almacen,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo,
                                                                                        "sinPendientes":sinPendientes,"prestamoEntregado":prestamoEntregado, "almacen":almacen, "administradordeVehiculos":administradordeVehiculos})
                
            return render(request, "empleadosCustom/almacen/solicitudesPendientes.html", {"solicitantePrestamo":solicitantePrestamo,"estaEnAlmacen":estaEnAlmacen,"estaEnSolicitudesPendientes":estaEnSolicitudesPendientes,"almacen":almacen,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo,
                                                                                        "sinPendientes":sinPendientes, "almacen":almacen, "administradordeVehiculos":administradordeVehiculos})
    #Si le da al inicio y no hay una sesión iniciada..
    else:
        return redirect('/login/') #redirecciona a url de inicio

def firmarPrestamo(request):
    
    #Si ya hay una sesión iniciada..
    if "idSesion" in request.session:
        
        
        estaEnAlmacen = True
        estaEnSolicitudesPendientes = True
        almacen = True
        solicitantePrestamo = True
        administradordeVehiculos = True


        id_admin=request.session["idSesion"]
        nombreini = request.session['nombres']
        apellidosini = request.session['apellidos']
        correo = request.session['correoSesion']
            
        foto = fotoAdmin(request)
        nombreCompleto = nombreini + " " + apellidosini #Blanca Yesenia Gaeta Talamantes
        
        if request.method == "POST":
            idPrestamoRecibido = request.POST['idPrestamo']
            
            infoPrestamo = PrestamosAlmacen.objects.filter(id_prestamo = idPrestamoRecibido)
            
            for dato in infoPrestamo:
                idEmpleadoSolicitante = dato.id_empleado_solicitante_id
                herramientasSolicitadas = dato.id_herramientaInstrumento
                cantidadesSolicitadas = dato.cantidades_solicitadas
                otro = dato.otro
            
            #Información de empleado
            consultaEmpleado = Empleados.objects.filter(id_empleado = idEmpleadoSolicitante)
            for datoEmpleado in consultaEmpleado:
                nombre = datoEmpleado.nombre
                apellidos = datoEmpleado.apellidos
                nombreCompletoEmpleadoSolicitante = nombre + " " + apellidos
                
                idArea = datoEmpleado.id_area_id
                consultaArea = Areas.objects.filter(id_area = idArea)
                for datoArea in consultaArea:
                    nombreDepartamento = datoArea.nombre
                    colorDepartamento = datoArea.color
                    
            #Información de herramientas
            arregloCantidadesHerramientas = cantidadesSolicitadas.split(",")
            herramientasAPrestar = []
            
            arregloIdsHerramientasAPrestar = herramientasSolicitadas.split(",")
            for idHerramienta in arregloIdsHerramientasAPrestar:
                consultaHerramienta = HerramientasAlmacen.objects.filter(id_herramienta = idHerramienta)
                
                for datoHerramienta in consultaHerramienta:
                    id_herramienta = datoHerramienta.id_herramienta
                    codigo_herramienta = datoHerramienta.codigo_herramienta
                    tipo_herramienta = datoHerramienta.tipo_herramienta
                    nombre_herramienta = datoHerramienta.nombre_herramienta
                    marca = datoHerramienta.marca
                    imagen = datoHerramienta.imagen_herramienta
                    descripcion_herramienta = datoHerramienta.descripcion_herramienta
                    unidad_herramienta = datoHerramienta.unidad
                    sku_herramienta = datoHerramienta.sku
                    cantidad_existencia = datoHerramienta.cantidad_existencia
                    
                herramientasAPrestar.append([id_herramienta, codigo_herramienta, tipo_herramienta,
                                             nombre_herramienta, marca, imagen, descripcion_herramienta,
                                             unidad_herramienta, sku_herramienta, cantidad_existencia])
            
            
            listaHerramientas = zip(herramientasAPrestar, arregloCantidadesHerramientas)
            
            return render(request, "empleadosCustom/almacen/firmarPrestamo.html", {"solicitantePrestamo":solicitantePrestamo,"estaEnAlmacen":estaEnAlmacen,"estaEnSolicitudesPendientes":estaEnSolicitudesPendientes,"almacen":almacen,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo, 
                                                                                   "infoPrestamo":infoPrestamo, "nombreCompletoEmpleadoSolicitante":nombreCompletoEmpleadoSolicitante,
                                                                                   "nombreDepartamento":nombreDepartamento, "colorDepartamento":colorDepartamento, "listaHerramientas":listaHerramientas, "otro":otro, "administradordeVehiculos":administradordeVehiculos})
    #Si le da al inicio y no hay una sesión iniciada..
    else:
        return redirect('/login/') #redirecciona a url de inicio
    
def firmarDevolucion(request):
    
    #Si ya hay una sesión iniciada..
    if "idSesion" in request.session:
        
        
        estaEnAlmacen = True
        estaEnSolicitudesMarcadas = True
        almacen = True
        solicitantePrestamo = True
        administradordeVehiculos = True


        id_admin=request.session["idSesion"]
        nombreini = request.session['nombres']
        apellidosini = request.session['apellidos']
        correo = request.session['correoSesion']
        foto = fotoAdmin(request)
        nombreCompleto = nombreini + " " + apellidosini #Blanca Yesenia Gaeta Talamantes
        
        
        if request.method == "POST":
            idPrestamoRecibido = request.POST['idPrestamo']
            herramientaBaja = False
        
        elif "idPrestamoActualizado" in request.session:
            idPrestamoRecibido =  request.session['idPrestamoActualizado']
            herramientaBaja =  request.session['herramientaActualizada']
            
        infoPrestamo = PrestamosAlmacen.objects.filter(id_prestamo = idPrestamoRecibido)
            
        for dato in infoPrestamo:
            idEmpleadoSolicitante = dato.id_empleado_solicitante_id
            herramientasSolicitadas = dato.id_herramientaInstrumento
            cantidadesSolicitadas = dato.cantidades_solicitadas
            otro = dato.otro
            
        #Información de empleado
        consultaEmpleado = Empleados.objects.filter(id_empleado = idEmpleadoSolicitante)
        for datoEmpleado in consultaEmpleado:
            nombre = datoEmpleado.nombre
            apellidos = datoEmpleado.apellidos
            nombreCompletoEmpleadoSolicitante = nombre + " " + apellidos
                
            idArea = datoEmpleado.id_area_id
            consultaArea = Areas.objects.filter(id_area = idArea)
            for datoArea in consultaArea:
                nombreDepartamento = datoArea.nombre
                colorDepartamento = datoArea.color
                    
        #Información de herramientas
        arregloCantidadesHerramientas = cantidadesSolicitadas.split(",")
        herramientasPrestadas = []
        herramientasPrestadasModalsBaja = []
            
        arregloIdsHerramientasAPrestar = herramientasSolicitadas.split(",")
        for idHerramienta in arregloIdsHerramientasAPrestar:
            consultaHerramienta = HerramientasAlmacen.objects.filter(id_herramienta = idHerramienta)
                
            for datoHerramienta in consultaHerramienta:
                id_herramienta = datoHerramienta.id_herramienta
                codigo_herramienta = datoHerramienta.codigo_herramienta
                tipo_herramienta = datoHerramienta.tipo_herramienta
                nombre_herramienta = datoHerramienta.nombre_herramienta
                marca = datoHerramienta.marca
                imagen = datoHerramienta.imagen_herramienta
                descripcion_herramienta = datoHerramienta.descripcion_herramienta
                unidad_herramienta = datoHerramienta.unidad
                sku_herramienta = datoHerramienta.sku
                cantidad_existencia = datoHerramienta.cantidad_existencia
                    
            herramientasPrestadas.append([id_herramienta, codigo_herramienta, tipo_herramienta,
                                             nombre_herramienta, marca, imagen, descripcion_herramienta,
                                             unidad_herramienta, sku_herramienta, cantidad_existencia])
            herramientasPrestadasModalsBaja.append([id_herramienta, codigo_herramienta, tipo_herramienta,
                                             nombre_herramienta, marca, imagen, descripcion_herramienta,
                                             unidad_herramienta, sku_herramienta, cantidad_existencia])
            
            
        listaHerramientas = zip(herramientasPrestadas, arregloCantidadesHerramientas)
            
        return render(request, "empleadosCustom/almacen/firmarDevolucion.html", {"solicitantePrestamo":solicitantePrestamo,"estaEnAlmacen":estaEnAlmacen,"estaEnSolicitudesMarcadas":estaEnSolicitudesMarcadas,"almacen":almacen,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo, 
                                                                                   "infoPrestamo":infoPrestamo, "nombreCompletoEmpleadoSolicitante":nombreCompletoEmpleadoSolicitante,
                                                                                   "nombreDepartamento":nombreDepartamento, "colorDepartamento":colorDepartamento, "listaHerramientas":listaHerramientas, "otro":otro, "herramientasPrestadasModalsBaja":herramientasPrestadasModalsBaja, "herramientaBaja":herramientaBaja, "administradordeVehiculos":administradordeVehiculos})
    #Si le da al inicio y no hay una sesión iniciada..
    else:
        return redirect('/login/') #redirecciona a url de inicio
    
    
    
def guardarEntrega(request):
    
    #Si ya hay una sesión iniciada..
    if "idSesion" in request.session:
        
        if request.method == "POST":
            idPrestamoGuardar = request.POST['idPrestamoGuardar']
            condicionesEntrega = request.POST['condicionesEntrega']
            canvasLargo = request.POST['canvasData']
            format, imgstr = canvasLargo.split(';base64,')
            ext = format.split('/')[-1]
            archivo = ContentFile(base64.b64decode(imgstr), name= "Prestamo"+str(idPrestamoGuardar) + '.' + ext)    
            
            fechaPrestamo = datetime.now()
            #actualizarRegistro
            
            actualizacionPrestamo = PrestamosAlmacen.objects.get(id_prestamo = idPrestamoGuardar)
            actualizacionPrestamo.fecha_prestamo = fechaPrestamo
            actualizacionPrestamo.firma_prestamo = archivo
            actualizacionPrestamo.condiciones = condicionesEntrega
            actualizacionPrestamo.estatus = "En prestamo"
            actualizacionPrestamo.save()
            
            if actualizacionPrestamo:
                #AQUI SE DEBEN DE DAR DE BAJA LAS CANTIDADES SELECCIONADAS
                consultaPrestamo = PrestamosAlmacen.objects.filter(id_prestamo = idPrestamoGuardar)
                for datos in consultaPrestamo:
                    idsHerramientas = datos.id_herramientaInstrumento
                    cantidadesHerramientas = datos.cantidades_solicitadas
                    idEmpleadoSolicitante = datos.id_empleado_solicitante_id
                    fecha_solicitud = datos.fecha_solicitud
                    proyecto = datos.proyecto_tarea
                    imagenFirmaEntrega = datos.firma_prestamo
                    
                arregloCantidadesHerramientas = cantidadesHerramientas.split(",")
                arregloIdsHerramientas = idsHerramientas.split(",")
                
                listaHerramientas = zip(arregloIdsHerramientas, arregloCantidadesHerramientas)
                
                arregloTablaHerramientasCorreo = []
                
                scriptHerramientasTelegram = ""
                    
                contadorHerramientas = 0


                for herramienta, cantidad in listaHerramientas:
                    contadorHerramientas = contadorHerramientas + 1
                    consultaHerramienta = HerramientasAlmacen.objects.filter(id_herramienta = herramienta)
                    for datoHerramienta in consultaHerramienta:
                        cantidadActualEnExistencia = datoHerramienta.cantidad_existencia
                        idHerramienta = datoHerramienta.id_herramienta
                        codigoHerramienta = datoHerramienta.codigo_herramienta
                        skuHerramienta = datoHerramienta.sku
                        nombreHerramienta = datoHerramienta.nombre_herramienta
                        marcaHerramienta = datoHerramienta.marca
                        if datoHerramienta.imagen_herramienta == None:
                            imagenHerramienta = "Sin imagen"
                        else: 
                            imagenHerramienta = datoHerramienta.imagen_herramienta
                        cantidadPrestada = str(cantidad)

                    if contadorHerramientas == 1:
                        scriptHerramientasTelegram = "\U0001F6E0 "+str(codigoHerramienta)+" - "+nombreHerramienta+". Cantidad entregada: "+str(cantidadPrestada)
                    else:
                        scriptHerramientasTelegram = scriptHerramientasTelegram+"\n \U0001F6E0 "+str(codigoHerramienta)+" - "+nombreHerramienta+". Cantidad solicitada: "+str(cantidadPrestada)
                    
                    
                    cantidadActualizada = cantidadActualEnExistencia - int(cantidad)
                    
                    actualizarExistenciaHerramienta = HerramientasAlmacen.objects.filter(id_herramienta = herramienta).update(cantidad_existencia = cantidadActualizada)
                    
                    arregloTablaHerramientasCorreo.append([idHerramienta,codigoHerramienta,skuHerramienta,nombreHerramienta,marcaHerramienta,imagenHerramienta,cantidadActualizada,cantidadPrestada])
                    
                if actualizarExistenciaHerramienta:
                
            
                    request.session['prestamoEntregado'] = "El prestamo "+ str(idPrestamoGuardar)+" ha sido entregado satisfactoriamente!"
                    
                    #Madar correo
                    datosEmpleadoSolicitante = Empleados.objects.filter(id_empleado=idEmpleadoSolicitante)
                    for dato in datosEmpleadoSolicitante:
                        nombreSolicitante= dato.nombre
                        apellidosSolicitante=dato.apellidos
                        correoSolicitante=dato.correo
                    
                    
                    asunto = "CS | Nueva entrega de préstamo a empleado."
                    plantilla = "empleadosCustom/almacen/correos/correoEntregaHerramienta.html"
                    
                    
                   
                    html_mensaje = render_to_string(plantilla, {"nombreSolicitante": nombreSolicitante, "apellidosSolicitante": apellidosSolicitante, "correoSolicitante": correoSolicitante,
                                                                "fecha_solicitud":fecha_solicitud,
                                                                "fecha_entrega":fechaPrestamo,
                                                                "proyecto":proyecto,
                                                                "imagenFirmaEntrega":imagenFirmaEntrega,
                                                                "idPrestamoEntregado":idPrestamoGuardar,
                                                                "arregloTablaHerramientasCorreo":arregloTablaHerramientasCorreo})
                    email_remitente = settings.EMAIL_HOST_USER
                    email_destino = ['sistemas@customco.com.mx']
                    mensaje = EmailMessage(asunto, html_mensaje, email_remitente, email_destino)
                    mensaje.content_subtype = 'html'
                    mensaje.send()

                    #Mandar notificación de telegram
                    try:
                        tokenTelegram = keysBotCustom.tokenBotPrestamos
                        botCustom = telepot.Bot(tokenTelegram)

                        idGrupoTelegram = keysBotCustom.idGrupo

                       

                        
                        mensaje = "\U0001274C ENTREGA DE HERRAMIENTA PRÉSTAMO #"+str(idPrestamoGuardar)+" \U0001274C \n Hola \U0001F44B! \n Se ha entregado la siguiente herramienta al empleado "+nombreSolicitante+" "+apellidosSolicitante+" : \n"+scriptHerramientasTelegram
                        botCustom.sendMessage(idGrupoTelegram,mensaje)
                    except:
                        print("An exception occurred")



                    return redirect("/solicitudesPendientesALM/")
            
    
    #Si le da al inicio y no hay una sesión iniciada..
    else:
        return redirect('/login/') #redirecciona a url de inicio

def guardarDevolucion(request):
    
    #Si ya hay una sesión iniciada..
    if "idSesion" in request.session:
        
        if request.method == "POST":
            idPrestamoGuardar = request.POST['idPrestamoGuardar']
            condicionesDevolucion = request.POST['condicionesEntrega']
            canvasLargo = request.POST['canvasData']
            format, imgstr = canvasLargo.split(';base64,')
            ext = format.split('/')[-1]
            archivo = ContentFile(base64.b64decode(imgstr), name= "Prestamo"+str(idPrestamoGuardar) + '.' + ext)    
            
            fechaDevolucion = datetime.now()
            #actualizarRegistro
            
            actualizacionPrestamo = PrestamosAlmacen.objects.get(id_prestamo = idPrestamoGuardar)
            actualizacionPrestamo.fecha_devolucion = fechaDevolucion
            actualizacionPrestamo.firma_devolucion = archivo
            actualizacionPrestamo.condiciones = condicionesDevolucion
            actualizacionPrestamo.estatus = "Devuelto"
            actualizacionPrestamo.save()
            
            if actualizacionPrestamo:
                #AQUI SE DEBEN DE DAR DE ALTA LAS CANTIDADES SELECCIONADAS
                consultaPrestamo = PrestamosAlmacen.objects.filter(id_prestamo = idPrestamoGuardar)
                for datos in consultaPrestamo:
                    idsHerramientas = datos.id_herramientaInstrumento
                    cantidadesHerramientas = datos.cantidades_solicitadas
                    idEmpleadoSolicitante = datos.id_empleado_solicitante_id
                    fecha_solicitud = datos.fecha_solicitud
                    fechaPrestamo = datos.fecha_prestamo
                    proyecto = datos.proyecto_tarea
                    imagenFirmaDevolucion = datos.fecha_devolucion
                    
                arregloCantidadesHerramientas = cantidadesHerramientas.split(",")
                arregloIdsHerramientas = idsHerramientas.split(",")
                
                listaHerramientas = zip(arregloIdsHerramientas, arregloCantidadesHerramientas)
                
                arregloTablaHerramientasCorreo = []
                
                scriptHerramientasTelegram = ""
                    
                contadorHerramientas = 0

                for herramienta, cantidad in listaHerramientas:
                    contadorHerramientas = contadorHerramientas + 1
                    consultaHerramienta = HerramientasAlmacen.objects.filter(id_herramienta = herramienta)
                    for datoHerramienta in consultaHerramienta:
                        cantidadActualEnExistencia = datoHerramienta.cantidad_existencia
                        idHerramienta = datoHerramienta.id_herramienta
                        codigoHerramienta = datoHerramienta.codigo_herramienta
                        skuHerramienta = datoHerramienta.sku
                        nombreHerramienta = datoHerramienta.nombre_herramienta
                        marcaHerramienta = datoHerramienta.marca
                        if datoHerramienta.imagen_herramienta == None:
                            imagenHerramienta = "Sin imagen"
                        else: 
                            imagenHerramienta = datoHerramienta.imagen_herramienta
                        cantidadDevuelta = str(cantidad)

                    if contadorHerramientas == 1:
                        scriptHerramientasTelegram = "\U0001F6E0 "+str(codigoHerramienta)+" - "+nombreHerramienta+". Cantidad devuelta: "+str(cantidadDevuelta)
                    else:
                        scriptHerramientasTelegram = scriptHerramientasTelegram+"\n \U0001F6E0 "+str(codigoHerramienta)+" - "+nombreHerramienta+". Cantidad devuelta: "+str(cantidadDevuelta)
                    
                    cantidadActualizada = cantidadActualEnExistencia + int(cantidad)
                    
                    actualizarExistenciaHerramienta = HerramientasAlmacen.objects.filter(id_herramienta = herramienta).update(cantidad_existencia = cantidadActualizada)
                    arregloTablaHerramientasCorreo.append([idHerramienta,codigoHerramienta,skuHerramienta,nombreHerramienta,marcaHerramienta,imagenHerramienta,cantidadActualizada,cantidadDevuelta])
                    
                if actualizarExistenciaHerramienta:
                
            
                    request.session['prestamoDevuelto'] = "El prestamo "+ str(idPrestamoGuardar)+" ha sido devuelto satisfactoriamente!"

                    datosEmpleadoSolicitante = Empleados.objects.filter(id_empleado=idEmpleadoSolicitante)
                    for dato in datosEmpleadoSolicitante:
                        nombreSolicitante= dato.nombre
                        apellidosSolicitante=dato.apellidos
                        correoSolicitante=dato.correo
                    
                    
                    asunto = "CS | Nueva devolución de préstamo a almacén."
                    plantilla = "empleadosCustom/almacen/correos/correoDevolucionHerramienta.html"
                    
                    
                   
                    html_mensaje = render_to_string(plantilla, {"nombreSolicitante": nombreSolicitante, "apellidosSolicitante": apellidosSolicitante, "correoSolicitante": correoSolicitante,
                                                                "fecha_solicitud":fecha_solicitud,
                                                                "fecha_entrega":fechaPrestamo,
                                                                "fecha_devolucion":fechaDevolucion,
                                                                "proyecto":proyecto,
                                                                "imagenFirmaEntrega":imagenFirmaDevolucion,
                                                                "idPrestamoEntregado":idPrestamoGuardar,
                                                                "arregloTablaHerramientasCorreo":arregloTablaHerramientasCorreo})
                    email_remitente = settings.EMAIL_HOST_USER
                    email_destino = ['sistemas@customco.com.mx']
                    mensaje = EmailMessage(asunto, html_mensaje, email_remitente, email_destino)
                    mensaje.content_subtype = 'html'
                    mensaje.send()

                    #Mandar notificación de telegram
                    try:
                        tokenTelegram = keysBotCustom.tokenBotPrestamos
                        botCustom = telepot.Bot(tokenTelegram)

                        idGrupoTelegram = keysBotCustom.idGrupo

                       

                        
                        mensaje = "\U0001274C DEVOLUCIÓN DE HERRAMIENTA PRÉSTAMO #"+str(idPrestamoGuardar)+" \U0001274C \n Hola \U0001F44B! \n Se ha devuelto la siguiente herramienta al almacen por el empleado "+nombreSolicitante+" "+apellidosSolicitante+" : \n"+scriptHerramientasTelegram
                        botCustom.sendMessage(idGrupoTelegram,mensaje)
                    except:
                        print("An exception occurred")
                    
                    return redirect("/solicitudesMarcadasALM/")
            
    
    #Si le da al inicio y no hay una sesión iniciada..
    else:
        return redirect('/login/') #redirecciona a url de inicio

def historialSolicitudesALM(request):
    
     #Si ya hay una sesión iniciada..
    if "idSesion" in request.session:
        
        
        estaEnAlmacen = True
        estaEnHistorialSolicitudes = True
        almacen = True
        solicitantePrestamo = True
        administradordeVehiculos = True


        id_admin=request.session["idSesion"]
        nombreini = request.session['nombres']
        apellidosini = request.session['apellidos']
        correo = request.session['correoSesion']
        foto = fotoAdmin(request)
        nombreCompleto = nombreini + " " + apellidosini #Blanca Yesenia Gaeta Talamantes
        
        prestamosDevueltos = PrestamosAlmacen.objects.filter(estatus="Devuelto")
        empleadosSolicitantes = []
        conDaño = []
        
        if prestamosDevueltos:
            for prestamoDevuelto in prestamosDevueltos:
                
                idPrestamoDevuelto = prestamoDevuelto.id_prestamo
                
                consultaPrestamoConDaño = HerramientasAlmacenInactivas.objects.filter(id_prestamo_id__id_prestamo = idPrestamoDevuelto)
                conDaños = ""
                #Si ese prestamo se entregó con algun daño..
                nombresHerramientasDañadas = []
                motivosDañados = []
                idsHerramientasDañadas = []
                if consultaPrestamoConDaño:
                    conDaños = "SI"
                    for daño in consultaPrestamoConDaño:
                        
                        idHerramientaDañada = daño.id_herramienta_id
                        motivo = daño.motivo_baja
                        
                        
                        idsHerramientasDañadas.append(idHerramientaDañada)
                        motivosDañados.append(motivo)
                        
                        consultaHerramienta = HerramientasAlmacen.objects.filter(id_herramienta = idHerramientaDañada)
                        for datoH in consultaHerramienta:
                            nombreHerramientaDañada = datoH.nombre_herramienta
                            
                        nombresHerramientasDañadas.append(nombreHerramientaDañada)
                    
                else: 
                    conDaños = "NO"
                    idsHerramientasDañadas.append("jijija")
                
                herramientasDañadas = zip(idsHerramientasDañadas, nombresHerramientasDañadas, motivosDañados)
                
                conDaño.append(conDaños)
                    
                
                #Herramientas
                herramientasDevueltas = prestamoDevuelto.id_herramientaInstrumento #Lista de herramientas 1,2
                arregloIndividualHerramientas = herramientasDevueltas.split(",") #[1,2]
                
                codigos = []
                nombres = []
                descripciones = []
                for herramientaIndividual in arregloIndividualHerramientas:
                    
                    idHerramienta = int(herramientaIndividual)
                    
                    consultaHerramienta = HerramientasAlmacen.objects.filter(id_herramienta = idHerramienta)
                    
                    for dato in consultaHerramienta:
                        codigo = dato.codigo_herramienta
                        nombre = dato.nombre_herramienta
                        descripcion = dato.descripcion_herramienta
                    codigos.append(codigo)
                    nombres.append(nombre)
                    descripciones.append(descripcion)
                        
                
                # Cantidades
                cantidades = prestamoDevuelto.cantidades_solicitadas
                arregloIndividualCantidades = cantidades.split(",")
                
                idEmpleadoSolicitante = prestamoDevuelto.id_empleado_solicitante_id
                consultaEmpleado = Empleados.objects.filter(id_empleado = idEmpleadoSolicitante)
                for dato in consultaEmpleado:
                    nombreEmpleadoSolicitante = dato.nombre
                    apellidosEmpleadoSolicitante = dato.apellidos
                    
                    nombreCompletoEmpleadoSolicitante = nombreEmpleadoSolicitante + " " + apellidosEmpleadoSolicitante
                    empleadosSolicitantes.append(nombreCompletoEmpleadoSolicitante)
                
                
            arregloHerramientas = zip(codigos,nombres,descripciones, arregloIndividualCantidades)
            
            listaSolicitudesPendientes = zip(prestamosDevueltos,empleadosSolicitantes, conDaño)
            

            
            return render(request, "empleadosCustom/almacen/historialSolicitudes.html", {"solicitantePrestamo":solicitantePrestamo,"estaEnAlmacen":estaEnAlmacen,"estaEnHistorialSolicitudes":estaEnHistorialSolicitudes,"almacen":almacen,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo,
                                                                                        "arregloHerramientas":arregloHerramientas, "solicitudesPendientes":prestamosDevueltos, "listaSolicitudesPendientes":listaSolicitudesPendientes, "herramientasDañadas":herramientasDañadas, "administradordeVehiculos":administradordeVehiculos})
        else:
            sinPendientes = True
                
            return render(request, "empleadosCustom/almacen/historialSolicitudes.html", {"solicitantePrestamo":solicitantePrestamo,"estaEnAlmacen":estaEnAlmacen,"estaEnHistorialSolicitudes":estaEnHistorialSolicitudes,"almacen":almacen,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo,
                                                                                        "sinPendientes":sinPendientes, "administradordeVehiculos":administradordeVehiculos})
    #Si le da al inicio y no hay una sesión iniciada..
    else:
        return redirect('/login/') #redirecciona a url de inicio

def solicitudesMarcadasALM(request):
    
    #Si ya hay una sesión iniciada..
    if "idSesion" in request.session:
        
        
        estaEnAlmacen = True
        estaEnSolicitudesMarcadas = True
        almacen = True
        solicitantePrestamo = True
        administradordeVehiculos = True


        id_admin=request.session["idSesion"]
        nombreini = request.session['nombres']
        apellidosini = request.session['apellidos']
        correo = request.session['correoSesion']
        foto = fotoAdmin(request)
        nombreCompleto = nombreini + " " + apellidosini #Blanca Yesenia Gaeta Talamantes
        
        prestamosRealizados = PrestamosAlmacen.objects.filter(estatus="En prestamo")
        empleadosPrestados = []
        
        if prestamosRealizados:
            for prestamo in prestamosRealizados:
                
                #Herramientas
                herramientas = prestamo.id_herramientaInstrumento #Lista de herramientas 1,2
                arregloIndividualHerramientas = herramientas.split(",") #[1,2]
                
                codigos = []
                nombres = []
                descripciones = []
                for herramientaIndividual in arregloIndividualHerramientas:
                    
                    idHerramienta = int(herramientaIndividual)
                    
                    consultaHerramienta = HerramientasAlmacen.objects.filter(id_herramienta = idHerramienta)
                    
                    for dato in consultaHerramienta:
                        codigo = dato.codigo_herramienta
                        nombre = dato.nombre_herramienta
                        descripcion = dato.descripcion_herramienta
                    codigos.append(codigo)
                    nombres.append(nombre)
                    descripciones.append(descripcion)
                        
                
                # Cantidades
                cantidades = prestamo.cantidades_solicitadas
                arregloIndividualCantidades = cantidades.split(",")
                
                idEmpleadoSolicitante = prestamo.id_empleado_solicitante_id
                consultaEmpleado = Empleados.objects.filter(id_empleado = idEmpleadoSolicitante)
                for dato in consultaEmpleado:
                    nombreEmpleadoSolicitante = dato.nombre
                    apellidosEmpleadoSolicitante = dato.apellidos
                    
                    nombreCompletoEmpleadoSolicitante = nombreEmpleadoSolicitante + " " + apellidosEmpleadoSolicitante
                    empleadosPrestados.append(nombreCompletoEmpleadoSolicitante)
                
                
            arregloHerramientas = zip(codigos,nombres,descripciones, arregloIndividualCantidades)
            
            listaPrestamosRealizados = zip(prestamosRealizados,empleadosPrestados)
            

            if "prestamoDevuelto" in request.session:
                prestamoEntregado = request.session["prestamoDevuelto"]
                del request.session["prestamoDevuelto"]
                return render(request, "empleadosCustom/almacen/solicitudesMarcadas.html", {"solicitantePrestamo":solicitantePrestamo,"estaEnAlmacen":estaEnAlmacen,"estaEnSolicitudesMarcadas":estaEnSolicitudesMarcadas,"almacen":almacen,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo,
                                                                                        "arregloHerramientas":arregloHerramientas, "prestamosRealizados":prestamosRealizados, "listaPrestamosRealizados":listaPrestamosRealizados, "prestamoEntregado":prestamoEntregado, "administradordeVehiculos":administradordeVehiculos})

            if "prestamoEntregadoParcial" in request.session:
                prestamoEntregado = request.session["prestamoEntregadoParcial"]
                del request.session["prestamoEntregadoParcial"]
                return render(request, "empleadosCustom/almacen/solicitudesMarcadas.html", {"solicitantePrestamo":solicitantePrestamo,"estaEnAlmacen":estaEnAlmacen,"estaEnSolicitudesMarcadas":estaEnSolicitudesMarcadas,"almacen":almacen,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo,
                                                                                        "arregloHerramientas":arregloHerramientas, "prestamosRealizados":prestamosRealizados, "listaPrestamosRealizados":listaPrestamosRealizados, "prestamoEntregado":prestamoEntregado, "administradordeVehiculos":administradordeVehiculos})
                
            return render(request, "empleadosCustom/almacen/solicitudesMarcadas.html", {"solicitantePrestamo":solicitantePrestamo,"estaEnAlmacen":estaEnAlmacen,"estaEnSolicitudesMarcadas":estaEnSolicitudesMarcadas,"almacen":almacen,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo,
                                                                                        "arregloHerramientas":arregloHerramientas, "prestamosRealizados":prestamosRealizados, "listaPrestamosRealizados":listaPrestamosRealizados, "administradordeVehiculos":administradordeVehiculos})
        else:
            sinPrestamos = True
            if "prestamoDevuelto" in request.session:
                prestamoEntregado = request.session["prestamoDevuelto"]
                del request.session["prestamoDevuelto"]    
                return render(request, "empleadosCustom/almacen/solicitudesMarcadas.html", {"solicitantePrestamo":solicitantePrestamo,"estaEnAlmacen":estaEnAlmacen,"estaEnSolicitudesMarcadas":estaEnSolicitudesMarcadas,"almacen":almacen,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo,
                                                                                        "sinPrestamos":sinPrestamos,"prestamoEntregado":prestamoEntregado, "administradordeVehiculos":administradordeVehiculos})
            if "prestamoEntregadoParcial" in request.session:
                prestamoEntregado = request.session["prestamoEntregadoParcial"]
                del request.session["prestamoEntregadoParcial"]    
                return render(request, "empleadosCustom/almacen/solicitudesMarcadas.html", {"solicitantePrestamo":solicitantePrestamo,"estaEnAlmacen":estaEnAlmacen,"estaEnSolicitudesMarcadas":estaEnSolicitudesMarcadas,"almacen":almacen,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo,
                                                                                        "sinPrestamos":sinPrestamos,"prestamoEntregado":prestamoEntregado, "administradordeVehiculos":administradordeVehiculos})
                
                
            return render(request, "empleadosCustom/almacen/solicitudesMarcadas.html", {"solicitantePrestamo":solicitantePrestamo,"estaEnAlmacen":estaEnAlmacen,"estaEnSolicitudesMarcadas":estaEnSolicitudesMarcadas,"almacen":almacen,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo,
                                                                                        "sinPrestamos":sinPrestamos, "administradordeVehiculos":administradordeVehiculos})
    #Si le da al inicio y no hay una sesión iniciada..
    else:
        return redirect('/login/') #redirecciona a url de inicio


    
def verHerramientasALM(request):
    
    #Si ya hay una sesión iniciada..
    if "idSesion" in request.session:
        
        
        estaEnAlmacen = True
        estaEnVerHerramientas = True
        almacen = True
        solicitantePrestamo = True
        administradordeVehiculos = True


        id_admin=request.session["idSesion"]
        nombreini = request.session['nombres']
        apellidosini = request.session['apellidos']
        correo = request.session['correoSesion']
        foto = fotoAdmin(request)
        nombreCompleto = nombreini + " " + apellidosini #Blanca Yesenia Gaeta Talamantes
        
        registrosHerramientas = HerramientasAlmacen.objects.all()
        registrosHerramientasModal = HerramientasAlmacen.objects.all()
        registrosHerramientasModalBaja = HerramientasAlmacen.objects.all()
        
        #Herramientas dañadas
        registrosHerramientasDañadas = HerramientasAlmacenInactivas.objects.filter(enInventario = "Si")
        datosHerramientasDañadas = []
        for herramientaDañada in registrosHerramientasDañadas:
            id_herramienta = herramientaDañada.id_herramienta_id
            id_prestamo = herramientaDañada.id_prestamo
            #consulta a herramienta
            datosHerramienta = HerramientasAlmacen.objects.filter(id_herramienta = id_herramienta)
            
            for herramienta in datosHerramienta:
            
                tipo = herramienta.tipo_herramienta
                codigo = herramienta.codigo_herramienta
                nombre = herramienta.nombre_herramienta
                marca = herramienta.marca
                descripcion = herramienta.descripcion_herramienta
                
                if id_prestamo == None:
                    id_prestamo = "Sin prestamo"
                    nombreEmpleadoResponsable = "Dado de baja por almacén"
                else:
                    consultaPrestamo = PrestamosAlmacen.objects.filter(id_prestamo = id_prestamo)
                    for dato in consultaPrestamo:
                        idEmpleadoResponsable = dato.id_empleado_solicitante_id
                            
                    consultaEmpleado = Empleados.objects.filter(id_empleado = idEmpleadoResponsable)
                    for datoEmpleado in consultaEmpleado:
                        nombreEmpleadoResponsable = datoEmpleado.nombre
                    
            
            datosHerramientasDañadas.append([id_herramienta, tipo, codigo, nombre, marca, descripcion, id_prestamo, nombreEmpleadoResponsable])
        
        listaDañadas = zip(registrosHerramientasDañadas, datosHerramientasDañadas)    
        
        #Herramientas dañadas fuera del inventario
        registrosHerramientasDañadasFuera = HerramientasAlmacenInactivas.objects.filter(enInventario = "No")
        datosHerramientasDañadasFuera = []
        for herramientaDañadaFuera in registrosHerramientasDañadasFuera:
            id_herramienta = herramientaDañadaFuera.id_herramienta_id
            id_prestamo = herramientaDañadaFuera.id_prestamo
            #consulta a herramienta
            datosHerramienta = HerramientasAlmacen.objects.filter(id_herramienta = id_herramienta)
            
            for herramienta in datosHerramienta:
            
                tipo = herramienta.tipo_herramienta
                codigo = herramienta.codigo_herramienta
                nombre = herramienta.nombre_herramienta
                marca = herramienta.marca
                descripcion = herramienta.descripcion_herramienta
                
                if id_prestamo == None:
                    id_prestamo = "Sin prestamo"
                    nombreEmpleadoResponsable = "Dado de baja por almacén"
                else:
                    consultaPrestamo = PrestamosAlmacen.objects.filter(id_prestamo = id_prestamo)
                    for dato in consultaPrestamo:
                        idEmpleadoResponsable = dato.id_empleado_solicitante_id
                            
                    consultaEmpleado = Empleados.objects.filter(id_empleado = idEmpleadoResponsable)
                    for datoEmpleado in consultaEmpleado:
                        nombreEmpleadoResponsable = datoEmpleado.nombre
                    
            
            datosHerramientasDañadasFuera.append([id_herramienta, tipo, codigo, nombre, marca, descripcion, id_prestamo, nombreEmpleadoResponsable])
        
        listaDañadasFuera = zip(registrosHerramientasDañadasFuera, datosHerramientasDañadasFuera)  
    
        #Costos de herramientas
        costoTotalHerramienta = []
        herramientasDañadasXHerramienta = []
        herramientasEnPrestamo = []
        costoTotalDañoHerramienta = []
        prestamosDeHerramienta = []
        for herramienta in registrosHerramientas:
            cantidadExistencia = herramienta.cantidad_existencia
            costo = herramienta.costo
            
            idHerramienta = herramienta.id_herramienta
            consultaHerramientasDañadas = HerramientasAlmacenInactivas.objects.filter(id_herramienta_id__id_herramienta = idHerramienta, enInventario="Si")
            
            contadorHerramientasDañadas = 0
            for dañada in consultaHerramientasDañadas:
                contadorHerramientasDañadas = contadorHerramientasDañadas + 1
            
            totalExistenciaConDaños = cantidadExistencia + contadorHerramientasDañadas
            
            costoTotalDaño = costo * contadorHerramientasDañadas
            
           
            
            consultaPrestamos = PrestamosAlmacen.objects.filter(estatus = "En prestamo")
            contadorHerramientaEnPrestamo = 0
            for prestamo in consultaPrestamos:
                idsHerramientasPrestadas = prestamo.id_herramientaInstrumento
                cantidadesHerramientasPrestadas = prestamo.cantidades_solicitadas
                
                arregloIdsHerramientasPrestadas = idsHerramientasPrestadas.split(",")
                arregloCantidadesHerramientas = cantidadesHerramientasPrestadas.split(",")
                
                listaHerramientasEnPrestamo = zip(arregloIdsHerramientasPrestadas, arregloCantidadesHerramientas)
                
                for idH, cantidad in listaHerramientasEnPrestamo:
                    intidH = int(idH)
                    if intidH == idHerramienta:
                        contadorHerramientaEnPrestamo = contadorHerramientaEnPrestamo + int(cantidad)
                        
            if contadorHerramientaEnPrestamo == 0:
                costoTotalInventarioHerramienta = costo*totalExistenciaConDaños
            else:
                costoPrestados = costo*contadorHerramientaEnPrestamo
                costosTodos = costo*totalExistenciaConDaños
                costoTotalInventarioHerramienta = costoPrestados + costosTodos
            
            
            herramientasEnPrestamo.append(contadorHerramientaEnPrestamo)
            costoTotalHerramienta.append(costoTotalInventarioHerramienta)
            herramientasDañadasXHerramienta.append(contadorHerramientasDañadas)
            costoTotalDañoHerramienta.append(costoTotalDaño)
            
        
            #Prestamos de herramientas
            prestamosAlmacen = PrestamosAlmacen.objects.filter(estatus="En prestamo")
            prestamosHerramientaIndividual = []
            for prestamo in prestamosAlmacen:
                idsHerramientasPrestamo = prestamo.id_herramientaInstrumento
                idPrestamo = prestamo.id_prestamo
                idEmpleadoSolicitante = prestamo.id_empleado_solicitante_id
                
                consultaEmpleado = Empleados.objects.filter(id_empleado = idEmpleadoSolicitante)
                for dato in consultaEmpleado:
                    nombreEmpleado = dato.nombre
                
                arregloIdsHerramientasPrestamo = idsHerramientasPrestamo.split(",")
                for idf in arregloIdsHerramientasPrestamo:
                    intId = int(idf)
                    if intId == idHerramienta:
                        prestamosHerramientaIndividual.append([idPrestamo, nombreEmpleado])
                  
            
            prestamosDeHerramienta.append(prestamosHerramientaIndividual)
            
            
        
            
        listaHerramientas = zip(registrosHerramientas, costoTotalHerramienta, herramientasDañadasXHerramienta, herramientasEnPrestamo, costoTotalDañoHerramienta, prestamosDeHerramienta)

        registrosHerramientasModal = zip(registrosHerramientas,herramientasEnPrestamo)
        registrosHerramientasModalBaja = zip(registrosHerramientas,herramientasEnPrestamo)
        
        costoTotalTotal = 0
        for costototal in costoTotalHerramienta:
            costoTotalTotal = costoTotalTotal + costototal
        
        #Si una herramienta fue actualizada..
        if "herramientaActualizada" in request.session:
            herramientaAct = request.session['herramientaActualizada']
            del request.session['herramientaActualizada']
            return render(request, "empleadosCustom/almacen/verHerramientas.html", {"solicitantePrestamo":solicitantePrestamo,"estaEnAlmacen":estaEnAlmacen,"estaEnVerHerramientas":estaEnVerHerramientas,"almacen":almacen,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo, "registrosHerramientas":registrosHerramientas, "registrosHerramientasModal":registrosHerramientasModal, "registrosHerramientasModalBaja":registrosHerramientasModalBaja, "listaDañadas":listaDañadas,"listaDañadasFuera":listaDañadasFuera, "herramientaAct":herramientaAct, "listaHerramientas":listaHerramientas, "costoTotalTotal":costoTotalTotal, "administradordeVehiculos":administradordeVehiculos})
            
        if "herramientaDescontada" in request.session:
            herramientaDescontada = request.session['herramientaDescontada']
            del request.session['herramientaDescontada']
            return render(request, "empleadosCustom/almacen/verHerramientas.html", {"solicitantePrestamo":solicitantePrestamo,"estaEnAlmacen":estaEnAlmacen,"estaEnVerHerramientas":estaEnVerHerramientas,"almacen":almacen,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo, "registrosHerramientas":registrosHerramientas, "registrosHerramientasModal":registrosHerramientasModal, "registrosHerramientasModalBaja":registrosHerramientasModalBaja, "listaDañadas":listaDañadas,"listaDañadasFuera":listaDañadasFuera, "herramientaDescontada":herramientaDescontada, "listaHerramientas":listaHerramientas, "costoTotalTotal":costoTotalTotal, "administradordeVehiculos":administradordeVehiculos})
            
        if "herramientaDañadaEliminada" in request.session:
            herramientaDañadaEliminada = request.session['herramientaDañadaEliminada']
            del request.session['herramientaDañadaEliminada']
            return render(request, "empleadosCustom/almacen/verHerramientas.html", {"solicitantePrestamo":solicitantePrestamo,"estaEnAlmacen":estaEnAlmacen,"estaEnVerHerramientas":estaEnVerHerramientas,"almacen":almacen,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo, "registrosHerramientas":registrosHerramientas, "registrosHerramientasModal":registrosHerramientasModal, "registrosHerramientasModalBaja":registrosHerramientasModalBaja, "listaDañadas":listaDañadas,"listaDañadasFuera":listaDañadasFuera, "herramientaDañadaEliminada":herramientaDañadaEliminada, "listaHerramientas":listaHerramientas, "costoTotalTotal":costoTotalTotal, "administradordeVehiculos":administradordeVehiculos})
            
        

        return render(request, "empleadosCustom/almacen/verHerramientas.html", {"solicitantePrestamo":solicitantePrestamo,"estaEnAlmacen":estaEnAlmacen,"estaEnVerHerramientas":estaEnVerHerramientas,"almacen":almacen,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo, "registrosHerramientas":registrosHerramientas, "registrosHerramientasModalBaja":registrosHerramientasModalBaja, "registrosHerramientasModal":registrosHerramientasModal, "listaDañadas":listaDañadas,"listaDañadasFuera":listaDañadasFuera, "listaHerramientas":listaHerramientas, "costoTotalTotal":costoTotalTotal, "administradordeVehiculos":administradordeVehiculos})
    #Si le da al inicio y no hay una sesión iniciada..
    else:
        return redirect('/login/') #redirecciona a url de inicio


def agregarHerramientasALM(request):
    
    #Si ya hay una sesión iniciada..
    if "idSesion" in request.session:
        
        
        estaEnAlmacen = True
        estaEnAgregarHerramientas = True
        almacen = True
        solicitantePrestamo = True
        administradordeVehiculos = True


        id_admin=request.session["idSesion"]
        nombreini = request.session['nombres']
        apellidosini = request.session['apellidos']
        correo = request.session['correoSesion']
        foto = fotoAdmin(request)
        nombreCompleto = nombreini + " " + apellidosini #Blanca Yesenia Gaeta Talamantes

        ultimoCodigo = ""
        consultaDeHerramientas = HerramientasAlmacen.objects.all()
        
        if consultaDeHerramientas:
            for herramienta in consultaDeHerramientas:
                ultimoCodigo = herramienta.codigo_herramienta
            
        

        if request.method == "POST":
            tipoHerramienta = request.POST['tipoHerramienta']
            nombreHerramienta = request.POST['nombreHerramienta']
            marcaHerramienta = request.POST['marcaHerramienta']
            unidadMedida = request.POST['unidadMedida']
            descripcion = request.POST['descripcion']
            imagenHerramienta = request.FILES.get('imagenHerramienta')
            skuHerramienta = request.POST['skuHerramienta']
            cantidadHerramienta = request.POST['cantidadHerramienta']
            costoHerramienta = request.POST['costoHerramienta']
            
            proveedorHerramienta = request.POST['proveedorHerramienta']
            odcHerramienta = request.POST['odcHerramienta']
            codigoHerramienta = request.POST['codigoHerramienta']
            nombre_corto = request.POST['nombreCorto']
            
            if proveedorHerramienta == "":
                proveedorHerramienta = "Sin proveedor"
            
            if odcHerramienta == "":
                odcHerramienta == "Sin orden de compra"
                
            
            
            #Codigo de herramienta
            consultaHerramientas = HerramientasAlmacen.objects.all()
                
            #Si hay, sumar codigo
            if codigoHerramienta == "":
                if consultaHerramientas:
                    haguardado = False
                    for herramienta in consultaHerramientas:
                        if "HA" in herramienta.codigo_herramienta:
                            haguardado = True
                            codigo = herramienta.codigo_herramienta
                        else:
                            haguardado = False
                    
                    if haguardado:
                        
                        #el ultimo código
                        primerDigito = codigo[2]
                        segundoDigito = codigo[3]
                        tercerDigito = codigo[4]
                        cuartoDigito = codigo[5]
                            
                        numero = primerDigito+segundoDigito+tercerDigito+cuartoDigito
                        intNumero = int(numero)
                        codigoInt = intNumero + 1
                        codigo = "HA"+str(codigoInt)
                    else:
                        codigo = "HA1000"
                else:
                    codigo = "HA1000"
            else:
                codigo = codigoHerramienta
                
                # Registro de herramienta
            fechaAlta =  datetime.now()
                
            if imagenHerramienta:
                registroHerramienta = HerramientasAlmacen(codigo_herramienta = codigo,
                                                          tipo_herramienta = tipoHerramienta,
                                                          nombre_herramienta = nombreHerramienta,
                                                          nombre_corto = nombre_corto,
                                                          descripcion_herramienta = descripcion,
                                                          marca = marcaHerramienta,
                                                          unidad = unidadMedida,
                                                          sku = skuHerramienta,
                                                          imagen_herramienta = imagenHerramienta,
                                                          estado_herramienta = "F",
                                                          motivo_estado = "Es funcional, disponible para prestamo",
                                                          fecha_alta = fechaAlta, 
                                                          cantidad_existencia = cantidadHerramienta,
                                                          costo = costoHerramienta,
                                                          stock = cantidadHerramienta,
                                                          orden_compra_evidence = odcHerramienta,
                                                          proveedor = proveedorHerramienta)
            else:
                registroHerramienta = HerramientasAlmacen(codigo_herramienta = codigo,
                                                          tipo_herramienta = tipoHerramienta,
                                                          nombre_herramienta = nombreHerramienta,
                                                          nombre_corto = nombre_corto,
                                                          descripcion_herramienta = descripcion,
                                                          marca = marcaHerramienta,
                                                          unidad = unidadMedida,
                                                          sku = skuHerramienta,
                                                          estado_herramienta = "F",
                                                          motivo_estado = "Es funcional, disponible para prestamo",
                                                          fecha_alta = fechaAlta, 
                                                          cantidad_existencia = cantidadHerramienta,
                                                          costo = costoHerramienta,
                                                          stock = cantidadHerramienta,
                                                          orden_compra_evidence = odcHerramienta,
                                                          proveedor = proveedorHerramienta)
                
            registroHerramienta.save()
            if registroHerramienta:
                herramientaGuardada = "La herramienta " + nombreHerramienta + " ha sido guardada satisfactoriamente!"
                return render(request, "empleadosCustom/almacen/agregarHerramientas.html", {"estaEnAlmacen":estaEnAlmacen,"estaEnAgregarHerramientas":estaEnAgregarHerramientas,"almacen":almacen,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo, "herramientaGuardada":herramientaGuardada, "administradordeVehiculos":administradordeVehiculos})
        return render(request, "empleadosCustom/almacen/agregarHerramientas.html", {"solicitantePrestamo":solicitantePrestamo,"estaEnAlmacen":estaEnAlmacen,"estaEnAgregarHerramientas":estaEnAgregarHerramientas,"almacen":almacen,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo, "ultimoCodigo":ultimoCodigo, "administradordeVehiculos":administradordeVehiculos})
    #Si le da al inicio y no hay una sesión iniciada..
    else:
        return redirect('/login/') #redirecciona a url de inicio


#Herramientas
def solicitarHerramientas(request):
    
    #Si ya hay una sesión iniciada..
    if "idSesion" in request.session:
        
        
        estaEnSolicitarHerramienta = True
        solicitantePrestamo = True


        id_admin=request.session["idSesion"]
        nombreini = request.session['nombres']
        apellidosini = request.session['apellidos']
        correo = request.session['correoSesion']

        consultaEmpleado = Empleados.objects.filter(id_empleado = id_admin)
        for datoEmpleado in consultaEmpleado:
            area = datoEmpleado.id_area_id

        if area == 1 or area ==5 or area == 7 or area == 8 or area == 9 or area == 10:
            solicitantePrestamo = True
            if area == 5:
                administradordeVehiculos = True
            else:
                administradordeVehiculos = False
        else:
            solicitantePrestamo = False
            administradordeVehiculos = False

        if correo == "almacen01@customco.com.mx":
            almacen = True
        else:
            almacen = False
        foto = fotoAdmin(request)
        nombreCompleto = nombreini + " " + apellidosini #Blanca Yesenia Gaeta Talamantes
        
        fechaHoy = datetime.now()
        
        
        data = [i.json() for i in HerramientasAlmacen.objects.filter(cantidad_existencia__range = (1,10000))]
        consulta = HerramientasAlmacen.objects.filter(cantidad_existencia__range = (1,10000))
       
        
        
        #Mandar prestamos de cada herramienta
        consulta2 = HerramientasAlmacen.objects.filter(cantidad_existencia__range = (1,10000))
        datosPrestamosPorHerramienta = []
        datosHerramientasRequisicion = []
        
        for herramienta in consulta2:
            idHerramienta = herramienta.id_herramienta
            
            prestamos = PrestamosAlmacen.objects.filter(estatus = "En prestamo")
            prestamosHerramientaIndividual = []
            for prestamo in prestamos:
                idPrestamito = prestamo.id_prestamo
                idsHerramientas = prestamo.id_herramientaInstrumento
                cantidadesHerramientas = prestamo.cantidades_solicitadas
                solicitante = prestamo.id_empleado_solicitante_id 
                consultaSolicitante = Empleados.objects.filter(id_empleado = solicitante)
                for datoEmpleado in consultaSolicitante:
                    nombreSolicitante = datoEmpleado.nombre
                
                arregloIds = idsHerramientas.split(",")
                arregloCantidades = cantidadesHerramientas.split(",")
                
                listaHerramientasEnPrestamo = zip(arregloIds, arregloCantidades)
                
                for idH, cantidad in listaHerramientasEnPrestamo:
                    
                    intidh = int(idH)
                    if idHerramienta == intidh:
                        prestamosHerramientaIndividual.append([idPrestamito, nombreSolicitante, cantidad ])
            
            datosPrestamosPorHerramienta.append(prestamosHerramientaIndividual)
                
        consultaHerramientasTabla = zip(consulta2, datosPrestamosPorHerramienta)
            
        consultaFunciones = HerramientasAlmacen.objects.all()
        
        if request.method == "POST":
            
            fecha_solicitud = datetime.now()
            fecha_requerido = request.POST['fecha_requerido']
            fecha_separada = fecha_requerido.split("/") #29   06    2018            2018     29   06
            fecha_normal_requerido = fecha_separada[2] + "-" + fecha_separada[0] + "-" + fecha_separada[1]
            
            proyecto = request.POST['proyecto']
            notas = request.POST['notas']
            cantidadHerramientasSolicitadas = request.POST['cantidadHerramientasSolicitadas']
            otrasHerramientas = request.POST['otrasHerramientas']
            
            if otrasHerramientas == "":
                otrasHerramientas = "No se solicitan otras herramientas"
            
            arregloCantidades = []
            arregloCantidadesRequi = []
            names = []
            names2 = []
            
            arregloIdsHerramientas = cantidadHerramientasSolicitadas.split(",")
            
            idPregunta = "id"
            cantidadSolicitar = "cantidadSolicitar"
            cantidadSolicitarRequi = "cantidadSolicitarRequi"
            for idherramienta in arregloIdsHerramientas:      # 1 2
                stringHerramienta = str(idherramienta)
                nameIdDeHerramienta = idPregunta + stringHerramienta
                nameCantidadASolicitar = cantidadSolicitar + stringHerramienta
                nameCantidadSolicitarRequi = cantidadSolicitarRequi + stringHerramienta #cantidadSolicitarRequi1   #cantidadSolicitarRequi2
                
                #Obtener valores que se mandaron
                idHerramientaMandado = request.POST[nameIdDeHerramienta]
                cantidadSolicitadaMandada = request.POST[nameCantidadASolicitar]
                arregloCantidades.append(cantidadSolicitadaMandada)
                
                cantidadSolicitadaRequiMandada = request.POST[nameCantidadSolicitarRequi]
                arregloCantidadesRequi.append(cantidadSolicitadaRequiMandada)

            stringCantidadesAGuardarEnBD = ""
            contadorCantidades = 0
            for cantidad in arregloCantidades:
                contadorCantidades = contadorCantidades + 1
                if contadorCantidades == 1:
                    stringCantidadesAGuardarEnBD = str(cantidad)
                else:
                    stringCantidadesAGuardarEnBD += "," + str(cantidad)
                    
            
            listaHerramientasRequi = zip(arregloIdsHerramientas, arregloCantidadesRequi)
            listaHErramientasSolicitadas = zip(arregloIdsHerramientas, arregloCantidades)
            
                    
            
            registroSolicitudPrestamo = PrestamosAlmacen(fecha_solicitud = fecha_solicitud,
                                                         fecha_requerimiento = fecha_normal_requerido,
                                                         id_empleado_solicitante = Empleados.objects.get(id_empleado = id_admin),
                                                         proyecto_tarea = proyecto,
                                                         otro = otrasHerramientas,
                                                         observaciones = notas,
                                                         id_herramientaInstrumento = cantidadHerramientasSolicitadas,
                                                         cantidades_solicitadas = stringCantidadesAGuardarEnBD,
                                                         estatus = "Pendiente")
            registroSolicitudPrestamo.save()
            
            registrosPrestamos = PrestamosAlmacen.objects.filter(estatus="Pendiente")
            arrayIdsPrestamos = []
            
            for prest in registrosPrestamos:
                idPrestPendiente = prest.id_prestamo
                arrayIdsPrestamos.append(idPrestPendiente)
                
            ultimoID = 0
            for idd in arrayIdsPrestamos:
                idInt = int(idd)
                ultimoID = idInt
            
            
            for herramientaRequi, cantidadRequi in listaHerramientasRequi:
                
                #Si es 0, no guarda la requi!
                if cantidadRequi == "0":
                    nada = True
                else: #Se guarda la requi
                    nada = False
                    registroRequi = RequisicionCompraAlmacen(id_empleado_solicitante = Empleados.objects.get(id_empleado = id_admin),
                                                             id_herramienta = HerramientasAlmacen.objects.get(id_herramienta = herramientaRequi),
                                                             id_prestamo = PrestamosAlmacen.objects.get(id_prestamo = ultimoID),
                                                             cantidad_requerida = cantidadRequi,
                                                             fehca_requi = fecha_solicitud,
                                                             estatus_requi = "Pendiente")
                    registroRequi.save()
                    
                    consultaHerramientaRequerida = HerramientasAlmacen.objects.filter(id_herramienta = herramientaRequi)
                    for dato in consultaHerramientaRequerida:
                        nombreHerramientaRequerida = dato.nombre_herramienta
                        sku_herramientaRequerida = dato.sku
                        codigo = dato.codigo_herramienta
                        if dato.imagen_herramienta == None:
                            imagen = "sin imagen"
                        else:
                            imagen = dato.imagen_herramienta
                        marca = dato.marca
                        proveedor = dato.proveedor
                        ordenCompra = dato.orden_compra_evidence
                    
                    datosHerramientasRequisicion.append([herramientaRequi,nombreHerramientaRequerida,codigo,sku_herramientaRequerida,imagen, cantidadRequi, marca, proveedor,ordenCompra])
                    
                    
                    
            if nada == False:         
                request.session['solicitudGuardada'] = "La solicitud ha sigo guardada con exito! Se ha mandado la requisición de herramientas por correo!"
            else:
                request.session['solicitudGuardada'] = "La solicitud ha sigo guardada con exito!"
            
            #CORREO ELECTRÓNICO
            datosEmpleadoSolicitante = Empleados.objects.filter(id_empleado=id_admin)
            strUltimoPrestamo = PrestamosAlmacen.objects.count()
            ultimoPrestamo = str(strUltimoPrestamo)
            for dato in datosEmpleadoSolicitante:
                nombreSolicitante= dato.nombre
                apellidosSolicitante=dato.apellidos
                correoSolicitante=dato.correo
            
            if nada == False:    
                asunto = "CS | Nueva solicitud de préstamo de herramienta con Requisición de compra."
            else:
                asunto = "CS | Nueva solicitud de préstamo de herramienta."
            plantilla = "empleadosCustom/almacen/correos/correoSolicitud.html"
            
            if nada == False:
                html_mensaje = render_to_string(plantilla, {"nombreSolicitante": nombreSolicitante, "apellidosSolicitante": apellidosSolicitante, "correoSolicitante": correoSolicitante,
                                                        "fecha_solicitud":fecha_solicitud,
                                                        "fecha_normal_requerido":fecha_normal_requerido,
                                                        "proyecto":proyecto,
                                                        "ultimoPrestamo":ultimoPrestamo, "datosHerramientasRequisicion":datosHerramientasRequisicion })
            else:
                html_mensaje = render_to_string(plantilla, {"nombreSolicitante": nombreSolicitante, "apellidosSolicitante": apellidosSolicitante, "correoSolicitante": correoSolicitante,
                                                        "fecha_solicitud":fecha_solicitud,
                                                        "fecha_normal_requerido":fecha_normal_requerido,
                                                        "proyecto":proyecto,
                                                        "ultimoPrestamo":ultimoPrestamo})
            email_remitente = settings.EMAIL_HOST_USER
            email_destino = ['sistemas@customco.com.mx']
            mensaje = EmailMessage(asunto, html_mensaje, email_remitente, email_destino)
            mensaje.content_subtype = 'html'
            mensaje.send()

            #Mandar notificación de telegram
            try:
                tokenTelegram = keysBotCustom.tokenBotPrestamos
                botCustom = telepot.Bot(tokenTelegram)

                idGrupoTelegram = keysBotCustom.idGrupo

                scriptHerramientasTelegram = ""
                    
                contadorHerramientas = 0
                for herramienta, cantidadSolicitada in listaHErramientasSolicitadas:
                    contadorHerramientas = contadorHerramientas + 1
                    idHerramienta = herramienta
                    cantidad = cantidadSolicitada

                    consultaHerramienta = HerramientasAlmacen.objects.filter(id_herramienta = idHerramienta)
                    for dato in consultaHerramienta:
                        nombreHerramienta= dato.nombre_herramienta
                        codigo = dato.codigo_herramienta

                    if contadorHerramientas == 1:
                        scriptHerramientasTelegram = "\U0001F6E0 "+str(codigo)+" - "+nombreHerramienta+". Cantidad solicitada: "+str(cantidad)
                    else:
                        scriptHerramientasTelegram = scriptHerramientasTelegram+"\n \U0001F6E0 "+str(codigo)+" - "+nombreHerramienta+". Cantidad solicitada: "+str(cantidad)
                    


                
                mensaje = "\U0001F4D1 SOLICITUD DE PRÉSTAMO #"+str(ultimoID)+" \U0001F4D1 \n Hola \U0001F44B! \n El empleado "+nombreSolicitante+" ha generado una solicitud de préstamo de las siguientes herramientas para el proyecto "+proyecto+": \n\n"+scriptHerramientasTelegram
                botCustom.sendMessage(idGrupoTelegram,mensaje)
            except:
                print("An exception occurred")
            
            
            return redirect('/verMisPrestamos/')

        consultaEmpleado = Empleados.objects.filter(id_empleado = id_admin)
        for datoEmpleado in consultaEmpleado:
            area = datoEmpleado.id_area_id
        if area == 1 or area ==5 or area == 7 or area == 8 or area == 9 or area == 10:
            if area == 5:
                solicitantePrestamo = True
                administradordeVehiculos = True
            else:
                solicitantePrestamo = True
                administradordeVehiculos = False

        else:
            solicitantePrestamo = False
            administradordeVehiculos = False


        return render(request, "empleadosCustom/almacen/empleados/solicitudHerramientas.html", {"solicitantePrestamo":solicitantePrestamo,"estaEnSolicitarHerramienta":estaEnSolicitarHerramienta,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo,
                                                                                                "fechaHoy":fechaHoy, "context":json.dumps(data), "HerramientasAlmacen":consulta, "consulta2":consultaHerramientasTabla, "consultaFunciones":consultaFunciones, "almacen":almacen, "solicitantePrestamo":solicitantePrestamo, "administradordeVehiculos":administradordeVehiculos})
    #Si le da al inicio y no hay una sesión iniciada..
    else:
        return redirect('/login/') #redirecciona a url de inicio

def verMisPrestamos(request):
    
    #Si ya hay una sesión iniciada..
    if "idSesion" in request.session:
        
        
        estaEnVerMisPrestamos = True
        solicitantePrestamo = True


        id_admin=request.session["idSesion"]
        nombreini = request.session['nombres']
        apellidosini = request.session['apellidos']
        correo = request.session['correoSesion']
        
        consultaEmpleado = Empleados.objects.filter(id_empleado = id_admin)
        for datoEmpleado in consultaEmpleado:
            area = datoEmpleado.id_area_id

        if area == 1 or area ==5 or area == 7 or area == 8 or area == 9 or area == 10:
            solicitantePrestamo = True
            if area == 5:
                administradordeVehiculos = True
            else:
                administradordeVehiculos = False
        else:
            solicitantePrestamo = False
            administradordeVehiculos = False

        if correo == "almacen01@customco.com.mx":
            almacen = True
        else:
            almacen = False


        foto = fotoAdmin(request)
        nombreCompleto = nombreini + " " + apellidosini #Blanca Yesenia Gaeta Talamantes
        
        
        
        # PRESTAMOS PENDIENTES- ----------------------------------------------------------------------------------------------------------------------------
        solicitudesPendientes = PrestamosAlmacen.objects.filter(id_empleado_solicitante_id__id_empleado = id_admin, estatus="Pendiente")
        prestamosEntregados = PrestamosAlmacen.objects.filter(id_empleado_solicitante_id__id_empleado = id_admin, estatus="En prestamo")
        prestamosDevueltos = PrestamosAlmacen.objects.filter(id_empleado_solicitante_id__id_empleado = id_admin, estatus="Devuelto")
        
        empleado = Empleados.objects.filter(id_empleado = id_admin)
        for dato in empleado:
            area = dato.id_area_id
           
        if area == 5: 
            administradordeVehiculos = True 
                
        
        #Pendientes
        arregloHerramientas = []
        codigos = []
        nombres = []
        descripciones = []
        
        #Entregados 
        arregloHerramientasEntregadas = []
        codigosHerramientasEntregadas = []
        nombresHerramientasEntregadas = []
        descripcionesHerramientasEntregadas = []
        
        #Pendientes
        conDaño = []
        nombresHerramientasDañadas = []
        motivosDañados = []
        idsHerramientasDañadas = []
        codigosDevueltos = []
        nombresDevueltos = []
        descripcionesDevueltos = []
        
        listaPrestamosDevueltos = ""
        herramientasDañadas = ""
        arregloHerramientasDevueltas = []
        
        
        if solicitudesPendientes:
            
            for solicitud in solicitudesPendientes:
                
                #Herramientas
                herramientas = solicitud.id_herramientaInstrumento
                arregloIndividualHerramientas = herramientas.split(",") #[1,2]
                
                
                for herramientaIndividual in arregloIndividualHerramientas:
                    
                    idHerramienta = int(herramientaIndividual)
                    
                    consultaHerramienta = HerramientasAlmacen.objects.filter(id_herramienta = idHerramienta)
                    
                    for dato in consultaHerramienta:
                        codigo = dato.codigo_herramienta
                        nombre = dato.nombre_herramienta
                        descripcion = dato.descripcion_herramienta
                    codigos.append(codigo)
                    nombres.append(nombre)
                    descripciones.append(descripcion)
                        
                
                # Cantidades
                cantidades = solicitud.cantidades_solicitadas
                arregloIndividualCantidades = cantidades.split(",")
                
            arregloHerramientas = zip(codigos,nombres,descripciones, arregloIndividualCantidades)
        
        
            
        
        if prestamosEntregados:
            
            for entrega in prestamosEntregados:
                
                #Herramientas
                herramientasEntregadas = entrega.id_herramientaInstrumento
                arregloIndividualHerramientasEntregadas = herramientasEntregadas.split(",") #[1,2]
                
                
                for herramientaIndividualEntregada in arregloIndividualHerramientasEntregadas:
                    
                    idHerramientaEntregada = int(herramientaIndividualEntregada)
                    
                    consultaHerramientaEntregada = HerramientasAlmacen.objects.filter(id_herramienta = idHerramientaEntregada)
                    
                    for datoE in consultaHerramientaEntregada:
                        codigoE = datoE.codigo_herramienta
                        nombreE = datoE.nombre_herramienta
                        descripcionE = datoE.descripcion_herramienta
                    codigosHerramientasEntregadas.append(codigoE)
                    nombresHerramientasEntregadas.append(nombreE)
                    descripcionesHerramientasEntregadas.append(descripcionE)
                        
                
                # Cantidades
                cantidadesEntregadas = entrega.cantidades_solicitadas
                arregloIndividualCantidadesEntregadas = cantidadesEntregadas.split(",")
                
            arregloHerramientasEntregadas = zip(codigosHerramientasEntregadas,nombresHerramientasEntregadas,descripcionesHerramientasEntregadas, arregloIndividualCantidadesEntregadas)
        
        
        
        
        
        if prestamosDevueltos:
            for prestamoDevuelto in prestamosDevueltos:
                
                idPrestamoDevuelto = prestamoDevuelto.id_prestamo
                
                consultaPrestamoConDaño = HerramientasAlmacenInactivas.objects.filter(id_prestamo_id__id_prestamo = idPrestamoDevuelto)
                conDaños = ""
                #Si ese prestamo se entregó con algun daño..
                
                if consultaPrestamoConDaño:
                    conDaños = "SI"
                    for daño in consultaPrestamoConDaño:
                        
                        idHerramientaDañada = daño.id_herramienta_id
                        motivo = daño.motivo_baja
                        
                        
                        idsHerramientasDañadas.append(idHerramientaDañada)
                        motivosDañados.append(motivo)
                        
                        consultaHerramienta = HerramientasAlmacen.objects.filter(id_herramienta = idHerramientaDañada)
                        for datoH in consultaHerramienta:
                            nombreHerramientaDañada = datoH.nombre_herramienta
                            
                        nombresHerramientasDañadas.append(nombreHerramientaDañada)
                    
                else: 
                    conDaños = "NO"
                    idsHerramientasDañadas.append("jijija")
                
                
                
                conDaño.append(conDaños)
                    
                
                #Herramientas
                herramientasDevueltas = prestamoDevuelto.id_herramientaInstrumento #Lista de herramientas 1,2
                arregloIndividualHerramientas = herramientasDevueltas.split(",") #[1,2]
                
                for herramientaIndividual in arregloIndividualHerramientas:
                    
                    idHerramienta = int(herramientaIndividual)
                    
                    consultaHerramienta = HerramientasAlmacen.objects.filter(id_herramienta = idHerramienta)
                    
                    for dato in consultaHerramienta:
                        codigo = dato.codigo_herramienta
                        nombre = dato.nombre_herramienta
                        descripcion = dato.descripcion_herramienta
                    codigosDevueltos.append(codigo)
                    nombresDevueltos.append(nombre)
                    descripcionesDevueltos.append(descripcion)
                        
                
                # Cantidades
                cantidades = prestamoDevuelto.cantidades_solicitadas
                arregloIndividualCantidades = cantidades.split(",")
                
                
                
                arregloHerramientasDevueltas = zip(codigosDevueltos,nombresDevueltos,descripcionesDevueltos, arregloIndividualCantidades)
            
            listaPrestamosDevueltos = zip(prestamosDevueltos, conDaño)
            
            herramientasDañadas = zip(idsHerramientasDañadas, nombresHerramientasDañadas, motivosDañados)
            
            

        if 'solicitudGuardada' in request.session:
            solicitudGuardada = request.session['solicitudGuardada']
            del request.session['solicitudGuardada']

            if administradordeVehiculos:
                return render(request, "empleadosCustom/almacen/empleados/verMisPrestamos.html", {"solicitantePrestamo":solicitantePrestamo,"estaEnVerMisPrestamos":estaEnVerMisPrestamos,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo,
                                                                                      "solicitudesPendientes":solicitudesPendientes, "arregloHerramientas":arregloHerramientas,
                                                                                      "prestamosEntregados":prestamosEntregados, "arregloHerramientasEntregadas":arregloHerramientasEntregadas,
                                                                                      "listaPrestamosDevueltos":listaPrestamosDevueltos, "herramientasDañadas":herramientasDañadas, "arregloHerramientasDevueltas":arregloHerramientasDevueltas, "solicitudGuardada":solicitudGuardada, "administradordeVehiculos":administradordeVehiculos,"almacen":almacen})


            return render(request, "empleadosCustom/almacen/empleados/verMisPrestamos.html", {"solicitantePrestamo":solicitantePrestamo,"estaEnVerMisPrestamos":estaEnVerMisPrestamos,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo,
                                                                                      "solicitudesPendientes":solicitudesPendientes, "arregloHerramientas":arregloHerramientas,
                                                                                      "prestamosEntregados":prestamosEntregados, "arregloHerramientasEntregadas":arregloHerramientasEntregadas,
                                                                                      "listaPrestamosDevueltos":listaPrestamosDevueltos, "herramientasDañadas":herramientasDañadas, "arregloHerramientasDevueltas":arregloHerramientasDevueltas, "solicitudGuardada":solicitudGuardada,"almacen":almacen})

        if administradordeVehiculos:
            return render(request, "empleadosCustom/almacen/empleados/verMisPrestamos.html", {"solicitantePrestamo":solicitantePrestamo,"estaEnVerMisPrestamos":estaEnVerMisPrestamos,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo,
                                                                                      "solicitudesPendientes":solicitudesPendientes, "arregloHerramientas":arregloHerramientas,
                                                                                      "prestamosEntregados":prestamosEntregados, "arregloHerramientasEntregadas":arregloHerramientasEntregadas,
                                                                                      "listaPrestamosDevueltos":listaPrestamosDevueltos, "herramientasDañadas":herramientasDañadas, "arregloHerramientasDevueltas":arregloHerramientasDevueltas, "administradordeVehiculos":administradordeVehiculos,"almacen":almacen})
            
        return render(request, "empleadosCustom/almacen/empleados/verMisPrestamos.html", {"solicitantePrestamo":solicitantePrestamo,"estaEnVerMisPrestamos":estaEnVerMisPrestamos,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo,
                                                                                      "solicitudesPendientes":solicitudesPendientes, "arregloHerramientas":arregloHerramientas,
                                                                                      "prestamosEntregados":prestamosEntregados, "arregloHerramientasEntregadas":arregloHerramientasEntregadas,
                                                                                      "listaPrestamosDevueltos":listaPrestamosDevueltos, "herramientasDañadas":herramientasDañadas, "arregloHerramientasDevueltas":arregloHerramientasDevueltas,"almacen":almacen})
        
        
            
            
        
    #Si le da al inicio y no hay una sesión iniciada..
    else:
        return redirect('/login/') #redirecciona a url de inicio

def actualizarCantidadesHerramientasAlmacen(request):
    #Si ya hay una sesión iniciada..
    if "idSesion" in request.session:
        
        if request.method == "POST":
            idHerramientaActualizar = request.POST['idHerramientaActualizar']
            cantidadHerramientaActualizar = request.POST['cantidadHerramientaActualizar']
            cantidadHerramientaActualizarStock = request.POST['cantidadHerramientaActualizarStock']
            codigoHerramientaActualizar = request.POST['codigoHerramientaActualizar']
            intCantidadHerramientaActualizar = int(cantidadHerramientaActualizar)
            intStockActualizado = int(cantidadHerramientaActualizarStock)
            
            fachaSolicitud = datetime.now()
            
            odcActualizada = request.POST['odcActualizada']
            proveedorHerramientaActualizada = request.POST['proveedorHerramientaActualizada']
            
            consultaHerramienta = HerramientasAlmacen.objects.filter(id_herramienta = idHerramientaActualizar)
            for datoHerramienta in consultaHerramienta:
                    existenciaActual = datoHerramienta.cantidad_existencia
                    stockActual = datoHerramienta.stock
                    codigoActual = datoHerramienta.codigo_herramienta
                    odcActual = datoHerramienta.orden_compra_evidence
                    proveedorActual = datoHerramienta.proveedor
                    
            sumaExistencia = int(existenciaActual)+int(cantidadHerramientaActualizar)
            if sumaExistencia > stockActual:
                    actualizacionHerramienta = HerramientasAlmacen.objects.filter(id_herramienta = idHerramientaActualizar).update(
                        cantidad_existencia = sumaExistencia,
                        stock = sumaExistencia,
                        codigo_herramienta = codigoHerramientaActualizar,
                        orden_compra_evidence = odcActualizada,
                        proveedor = proveedorHerramientaActualizada
                    )
            else:
                actualizacionHerramienta = HerramientasAlmacen.objects.filter(id_herramienta = idHerramientaActualizar).update(
                        cantidad_existencia = sumaExistencia,
                        stock = intStockActualizado,
                        codigo_herramienta = codigoHerramientaActualizar,
                        orden_compra_evidence = odcActualizada,
                        proveedor = proveedorHerramientaActualizada
                )
            
            #Actualizar cantidad
           
            
            if actualizacionHerramienta:
                
                contadorActualizaciones = 0
                actualizaciones = altasAlmacen.objects.all()
                for actualizacion in actualizaciones:
                    contadorActualizaciones = actualizacion.id_alta
                
                contadorActualizaciones = contadorActualizaciones+1
                
                #Mandar correo a dani..
                asunto = "CS | Nueva actualización de herramienta. Numero "+str(contadorActualizaciones)
                plantilla = "empleadosCustom/almacen/correos/correoSolicitudAlta.html"
                
                
                existenciaBool = False
                stockBool = False
                codigoBool = False
                odcBool = False
                proveedorBool = False
                
                mensajeExistencia = ""
                mensajeStock = ""
                mensajeCodigo = ""
                mensajeODC = ""
                mensajeProveedor = ""
                
                ultimaSolicitud = 0
                consultaSolicitudes = altasAlmacen.objects.all()
                for solicitudes in consultaSolicitudes:
                    ultimaSolicitud = solicitudes.id_alta
               
                #Actualizacion Herramienta
                sumaExistencia = existenciaActual + intCantidadHerramientaActualizar
                
                if intCantidadHerramientaActualizar == 0:
                    existenciaBool = False
                    mensajeExistencia = "No se actualizarán cantidades en existencia."
                else:
                    existenciaBool = True
                    suma = existenciaActual+intCantidadHerramientaActualizar
                    mensajeExistencia = "Se actualizaron las cantidades de "+str(existenciaActual)+ " a "+str(suma) + " unidades. (Se agregaron "+str(intCantidadHerramientaActualizar)+" unidades)"
            
                if intStockActualizado == stockActual:
                    stockBool = False
                    if sumaExistencia > stockActual:
                        mensajeStock = "Se actualizó el stock de "+str(sumaExistencia-intCantidadHerramientaActualizar) + " a "+str(sumaExistencia) + " unidades."
                        
                    else:
                        mensajeStock  ="No se actualizará la cantidad en Stock."
                else:
                    stockBool = True
                    mensajeStock = "Se actualizó el stock de "+str(stockActual) + " a "+str(intStockActualizado) + " unidades."
                    
                if codigoHerramientaActualizar == codigoActual:
                    codigoBool = False
                    mensajeCodigo = "No se actualizará el código de la herramienta."
                else:
                    codigoBool = True
                    mensajeCodigo = "Se actualizó el código de la herramienta de "+str(codigoActual)+ " a "+ str(codigoHerramientaActualizar)
                    
                if odcActualizada == odcActual:
                    odcBool = False
                    mensajeODC = "No se actualizará la ODC ligada en evidence."
                else:
                    odcBool = True
                    mensajeODC = "Se actualizó la última ODC en Evidence de esta herramienta: "+str(odcActualizada)
                    
                if proveedorHerramientaActualizada == proveedorActual:
                    proveedorBool = False
                    mensajeProveedor = "No se actualizará el proveedor de esta herramienta."
                else:
                    proveedorBool = True
                    mensajeProveedor = "Se actualizó al proveedor: "+str(proveedorHerramientaActualizada)
                
                
                
                html_mensaje = render_to_string(plantilla, {"ultimaSolicitud":ultimaSolicitud,"fecha_solicitud_actualizacion":fachaSolicitud,
                                                            "consultaHerramienta":consultaHerramienta,
                                                            "existenciaBool":existenciaBool, "mensajeExistencia":mensajeExistencia,
                                                            "stockBool":stockBool,"mensajeStock":mensajeStock,
                                                            "codigoBool":codigoBool, "mensajeCodigo":mensajeCodigo,
                                                            "odcBool":odcBool,"mensajeODC":mensajeODC,
                                                            "proveedorBool":proveedorBool, "mensajeProveedor":mensajeProveedor})
                email_remitente = settings.EMAIL_HOST_USER
                email_destino = ['sistemas@customco.com.mx']
                mensaje = EmailMessage(asunto, html_mensaje, email_remitente, email_destino)
                mensaje.content_subtype = 'html'
                mensaje.send()
                
                alta = altasAlmacen(id_herramienta = HerramientasAlmacen.objects.get(id_herramienta = idHerramientaActualizar),
                                                  cantidad_agregar = mensajeExistencia,
                                                  stockActualizado = mensajeStock,
                                                  codigoActualizado = mensajeCodigo,
                                                  fecha_alta = fachaSolicitud,
                                                  orden_compra_evidence_act = mensajeODC,
                                                  proveedor_alta = mensajeProveedor,
                                                  estatus_alta = "Realizada",
                                                  requi = "Sin requisición ligada")
                alta.save()

                

                
                
                request.session['herramientaActualizada'] = "Se ha realizado la actualización! Correo electrónico mandado a Jefe de Logistica y compras."
                
                return redirect('/verHerramientasALM/')
    #Si le da al inicio y no hay una sesión iniciada..
    else:
        return redirect('/login/') #redirecciona a url de inicio
    
def bajaHerramientaAlmacen(request):
    #Si ya hay una sesión iniciada..
    
    if "idSesion" in request.session:
        id_admin=request.session["idSesion"]
        
        if request.method == "POST":
            idHerramientaBaja = request.POST['idHerramientaBaja']
            motivoBaja = request.POST['motivoBaja']
            explicacion = request.POST['explicacion']
            
            bajita = ""
            if motivoBaja == "E":
                bajita = "Extravío"
            elif motivoBaja == "D":
                bajita = "Dañado"
            
            consultaHerramienta = HerramientasAlmacen.objects.filter(id_herramienta = idHerramientaBaja)
            
            for dato in consultaHerramienta:
                cantidadExistenteActual = dato.cantidad_existencia
                nombreHerramienta = dato.nombre_herramienta
                codigoInternoSistema = dato.codigo_herramienta
                tipo = dato.tipo_herramienta
                marca = dato.marca
                descripcion = dato.descripcion_herramienta
                sku = dato.sku
                if dato.imagen_herramienta == None:
                    imagenHerramienta = "Sin imagen"
                else:
                    imagenHerramienta = dato.imagen_herramienta
                proveedor = dato.proveedor
                odcEvidence = dato.orden_compra_evidence
                
                
                
            intCantidadExistenciaActual = int(cantidadExistenteActual)
            
            
            restaCantidad = intCantidadExistenciaActual - 1
            fechaBaja = datetime.now()
            #Actualizar cantidad
            actualizacion = HerramientasAlmacen.objects.filter(id_herramienta = idHerramientaBaja).update(cantidad_existencia = restaCantidad)
            
            #Registro de baja 
            if bajita == "Extravío":
                registroDeBaja = HerramientasAlmacenInactivas(id_herramienta = HerramientasAlmacen.objects.get(id_herramienta = idHerramientaBaja), motivo_baja = motivoBaja, explicacion_baja = explicacion, 
                                                          cantidad_baja = "1", fecha_baja = fechaBaja, enInventario = "No")
            else:
                registroDeBaja = HerramientasAlmacenInactivas(id_herramienta = HerramientasAlmacen.objects.get(id_herramienta = idHerramientaBaja), motivo_baja = motivoBaja, explicacion_baja = explicacion, 
                                                          cantidad_baja = "1", fecha_baja = fechaBaja, enInventario = "Si")
            registroDeBaja.save()
            if actualizacion and registroDeBaja:
                #Hacer Requisición de compra de esa herramienta
                registroRequi = RequisicionCompraAlmacen(id_empleado_solicitante = Empleados.objects.get(id_empleado = id_admin),
                                                         id_herramienta = HerramientasAlmacen.objects.get(id_herramienta = idHerramientaBaja),
                                                         cantidad_requerida = 1, fehca_requi = fechaBaja, estatus_requi = "Pendiente")
                registroRequi.save()
                request.session['herramientaActualizada'] = "La herramienta " + nombreHerramienta + " ha sido dada de baja satisfactoriamente! Se ha mandado un correo con la solicitud de requisición de compra!"
                
                #MANDAR CORREO DE SOLICITUD DE REQUISICIÓN DE COMPRA
                
                    
                asunto = "CS | Solicitud de requisición de compra de herramienta"
                plantilla = "empleadosCustom/almacen/correos/correoBajaHerramienta.html"
                html_mensaje = render_to_string(plantilla, {"idHerramientaDañada":idHerramientaBaja,
                                                            "codigoHerramientaDañada":codigoInternoSistema,
                                                            "skuHerramientaDañada":sku,
                                                            "tipoHerramientaDañada":tipo,
                                                            "nombreHerramientaDañada":nombreHerramienta,
                                                            "marcaHerramientaDañada":marca,
                                                            "descripcionHerramientaDañada":descripcion,
                                                            "restaCantidad":restaCantidad,
                                                            "motivoDañoHerramientaDañada":bajita,
                                                            "explicacionDañoHerramientaDañada":explicacion,
                                                            "imagenHerramientaDañada":imagenHerramienta,
                                                            "proveedor":proveedor,
                                                            "odcEvidence":odcEvidence
                                                            })
                email_remitente = settings.EMAIL_HOST_USER
                email_destino = ['sistemas@customco.com.mx']
                mensaje = EmailMessage(asunto, html_mensaje, email_remitente, email_destino)
                mensaje.content_subtype = 'html'
                mensaje.send()

                #Mandar notificación de telegram
                try:
                    tokenTelegram = keysBotCustom.tokenBotPrestamos
                    botCustom = telepot.Bot(tokenTelegram)

                    idGrupoTelegram = keysBotCustom.idGrupo

                    
                    mensaje = "\U0001274C BAJA DE HERRAMIENTA #"+str(codigoInternoSistema)+" \U0001274C \n Hola \U0001F44B! \n Se ha dado de baja la herramientas : \n"+codigoInternoSistema+" - "+nombreHerramienta+ " por "+bajita
                    botCustom.sendMessage(idGrupoTelegram,mensaje)
                except:
                    print("An exception occurred")
            
                
                
                return redirect('/verHerramientasALM/')
    #Si le da al inicio y no hay una sesión iniciada..
    else:
        return redirect('/login/') #redirecciona a url de inicio
    
def bajaHerramientaAlmacenPrestamo(request):
    #Si ya hay una sesión iniciada..
    if "idSesion" in request.session:
        
        if request.method == "POST":
            idPrestamoConDaño = request.POST['idPrestamo']
            idHerramientaBaja = request.POST['idHerramientaBaja']
            intIdHerramientaBaja = int(idHerramientaBaja)
            motivoBaja = request.POST['motivoBaja']
            explicacion = request.POST['explicacion']
            
            fechaBaja = datetime.now()
            
            #Sacar nombre de herramienta
            consultaHerramienta = HerramientasAlmacen.objects.filter(id_herramienta = idHerramientaBaja)
            for datoH in consultaHerramienta:
                nombreHerramienta = datoH.nombre_herramienta
                codigoHerramienta = datoH.codigo_herramienta
            
            #Restar cantidad del prestamo, no de la existencia actual en almacén, ya que aun no se devuelve
            consultaPrestamo = PrestamosAlmacen.objects.filter(id_prestamo = idPrestamoConDaño)
            
            for dato in consultaPrestamo:
                idsHerramientas = dato.id_herramientaInstrumento
                empleado = dato.id_empleado_solicitante_id
                cantidadesHerramientas = dato.cantidades_solicitadas

            #Consula empleado
            consultaEmpleado = Empleados.objects.filter(id_empleado = empleado)
            for datoEmpleado in consultaEmpleado:
                nombreEmpleado = datoEmpleado.nombre
                apellidoEmpleado = datoEmpleado.apellidos

            nombreCompletoEmpleadoPrestamo = nombreEmpleado + " " + apellidoEmpleado
                
            #Arreglos ya separados
            arregloCantidades = cantidadesHerramientas.split(",")
            arregloIdsHerramientas = idsHerramientas.split(",")
            listaHerramientasCantidades = zip(arregloIdsHerramientas, arregloCantidades)
            
            posicionArreglo = 0
            for herramienta,cantidad in listaHerramientasCantidades:
                posicionArreglo = posicionArreglo + 1
                if herramienta == idHerramientaBaja:  #No entra a esta condicion ???
                    nuevaCantidadPrestada = int(cantidad) - 1
                    arregloCantidades[posicionArreglo-1] = nuevaCantidadPrestada
                    #Ya esta actualizado en el arreglo.. falta actualizar en la BD
                    
            stringCantidadesActualizar = ""
            contadorCantidades = 0
            for cantidad in arregloCantidades:
                contadorCantidades = contadorCantidades + 1
                if contadorCantidades == 1:
                    stringCantidadesActualizar = str(cantidad)
                else:
                    stringCantidadesActualizar += ","+str(cantidad)
                    
            #String de cantidades realizado
            
            #Actualizar string de cantidades
            actualizacionPrestamo = PrestamosAlmacen.objects.filter(id_prestamo = idPrestamoConDaño).update(cantidades_solicitadas = stringCantidadesActualizar)
            
            
            #Registro de baja 
            registroDeBaja = HerramientasAlmacenInactivas(id_herramienta = HerramientasAlmacen.objects.get(id_herramienta = idHerramientaBaja), motivo_baja = motivoBaja, explicacion_baja = explicacion, 
                                                          cantidad_baja = "1", fecha_baja = fechaBaja, id_prestamo = PrestamosAlmacen.objects.get(id_prestamo = idPrestamoConDaño))
            registroDeBaja.save()
            
            if actualizacionPrestamo and registroDeBaja:
                
                #MANDAR CORREO PARA REQUISICIOOON DE ESE EQUIPO QUE SE DIO DE BAJAAAAAA..
                
                
                request.session['idPrestamoActualizado'] = idPrestamoConDaño
                request.session['herramientaActualizada'] = "La herramienta " + nombreHerramienta + " ha sido dada de baja satisfactoriamente!"

                #Mandar notificación de telegram
                try:
                    tokenTelegram = keysBotCustom.tokenBotPrestamos
                    botCustom = telepot.Bot(tokenTelegram)

                    idGrupoTelegram = keysBotCustom.idGrupo

                    
                    mensaje = "\U0001274C BAJA DE HERRAMIENTA #"+str(codigoHerramienta)+" \U0001274C \n Hola \U0001F44B! \n Se ha dado de baja la herramienta: \n"+codigoHerramienta+" - "+nombreHerramienta+ " por "+motivoBaja+"\n Prestamo #"+str(idPrestamoConDaño)+" encargado: "+nombreCompletoEmpleadoPrestamo
                    botCustom.sendMessage(idGrupoTelegram,mensaje)
                except:
                    print("An exception occurred")
                    
                
                return redirect('/firmarDevolucion/')
    #Si le da al inicio y no hay una sesión iniciada..
    else:
        return redirect('/login/') #redirecciona a url de inicio
    

def excelInventario(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Inventario Herramientas Almacén '+str(datetime.today().strftime('%Y-%m-%d'))+'.xls'
    
    #creación de libro de excel
    libro = xlwt.Workbook(encoding='utf-8')
    hoja = libro.add_sheet('Reporte de existencias')
    
    numero_fila = 0
    estilo_fuente = xlwt.XFStyle()
    estilo_fuente.font.bold = True
    
    columnas = ['Id Herramienta','Código Herramienta', 'Nombre herramienta', 'Descripción', 'Marca', 'Unidad','Tipo','Categoria/Nombre corto', 'SKU','Fecha de alta en CS','Cantidad en préstamos','Cantidad en existencia','Cantidad Dañadas en inventario','Total Cantidades','Stock','Costo unitario','Costo Total Activo','Costo Total Inventario físico','Cantidad Extraviadas','Cantidad Dañadas Fuera del inventario', 'Costo Pérdida', 'Costo Real total (Costo total Activo - Costo Total pérdida) ', 'Proveedor', 'ODC Evidence ligada' ]
    for campo in range(len(columnas)):
        hoja.write(numero_fila, campo, columnas[campo], estilo_fuente)
        
    todasLasHerramientas = HerramientasAlmacen.objects.all()
    
    arrayHerramientas = []
    for herramienta in todasLasHerramientas:
        idHerramienta = herramienta.id_herramienta
        codigoHerramienta = herramienta.codigo_herramienta,
        nombreHerramienta = herramienta.nombre_herramienta
        nombreCorto = herramienta.nombre_corto
        descripcionHerramienta = herramienta.descripcion_herramienta,
        marca = herramienta.marca
        unidad = herramienta.unidad
        tipo = herramienta.tipo_herramienta
        sku = herramienta.sku
        fecha_alta = herramienta.fecha_alta
        stock = herramienta.stock
        existencias = herramienta.cantidad_existencia
        costo_unitario = herramienta.costo
        proveedor = herramienta.proveedor
        ordenCompra = herramienta.orden_compra_evidence
        
        #CantidadPrestamos ya esta..
        contadorHerramientasEnPrestamo = 0
        consultaPrestamosDeHerramienta = PrestamosAlmacen.objects.filter(estatus="En prestamo")
        for dato in consultaPrestamosDeHerramienta:
            idsHerramientas = dato.id_herramientaInstrumento
            cantidadesHerramientas = dato.cantidades_solicitadas
            
            arregloIdsHerramientas = idsHerramientas.split(",")
            arregloCantidadesHerramientas = cantidadesHerramientas.split(",")
            
            listaHerramientasEnPrestamo = zip(arregloIdsHerramientas,arregloCantidadesHerramientas)
            
            for idhhh, cantidad in listaHerramientasEnPrestamo:
                idH = int(idhhh)
                can = int(cantidad)
                if idH == idHerramienta:
                    contadorHerramientasEnPrestamo = contadorHerramientasEnPrestamo + can
        
        #cantidad dañadas en inventario
        cantidadHerramientasDañadas = 0
        consultaHerramientasDañadas = HerramientasAlmacenInactivas.objects.filter(id_herramienta_id__id_herramienta = idHerramienta, motivo_baja="D", enInventario="Si")
        
        for herramientaDañada in consultaHerramientasDañadas:
            cantidadHerramientasDañadas = cantidadHerramientasDañadas + 1
            
        #Total cantidades
        totalCantidades = existencias + cantidadHerramientasDañadas
        
        #cantidad extraviadas
        cantidadHerramientasExtraviadas = 0
        consultaHerramientasExtraviadas = HerramientasAlmacenInactivas.objects.filter(id_herramienta_id__id_herramienta = idHerramienta, motivo_baja="E")
        
        for herramientaExtraviada in consultaHerramientasExtraviadas:
            cantidadHerramientasExtraviadas = cantidadHerramientasExtraviadas + 1
            
         #cantidad dañadas en inventario
        cantidadHerramientasDañadasNoInventariadas = 0
        consultaHerramientasDañadasNoInventariadas = HerramientasAlmacenInactivas.objects.filter(id_herramienta_id__id_herramienta = idHerramienta, motivo_baja="D", enInventario="No")
        
        for herramientaDañadaNoInventariada in consultaHerramientasDañadasNoInventariadas:
            cantidadHerramientasDañadasNoInventariadas = cantidadHerramientasDañadasNoInventariadas + 1
            
        #costo total
        #Costo de total de herramientas en existencia, más herramientas en prestamo, mas dañadas
        
        sumaHerramientas = existencias + contadorHerramientasEnPrestamo + cantidadHerramientasDañadas
        costoTotal = float(sumaHerramientas) * costo_unitario
        
        costoTotalDaño = cantidadHerramientasDañadas
        
        #costo total daño
        costoTotalDaño = float(cantidadHerramientasDañadas) * costo_unitario
        #costo total extravio
        costoTotalExtravio = float(cantidadHerramientasExtraviadas) * costo_unitario
        
        costoTotalDañoNoInventariado = float(cantidadHerramientasDañadasNoInventariadas)* costo_unitario
        #costo perdida
        costoTotalPerdida = costoTotalDaño + costoTotalExtravio + costoTotalDañoNoInventariado
       
        
        sumaActivo = existencias + contadorHerramientasEnPrestamo
        costoTotalActivo = float(sumaActivo) * costo_unitario
         #costo real total
        costoRealTotal = costoTotalActivo - costoTotalPerdida
        
        
        arrayHerramientas.append([idHerramienta, codigoHerramienta, nombreHerramienta, descripcionHerramienta, marca, unidad, tipo,nombreCorto, sku, fecha_alta,contadorHerramientasEnPrestamo, existencias,cantidadHerramientasDañadas, totalCantidades,stock,costo_unitario,costoTotalActivo,costoTotal, cantidadHerramientasExtraviadas,cantidadHerramientasDañadasNoInventariadas, costoTotalPerdida, costoRealTotal, proveedor, ordenCompra ])
        
        
            
        
    estilo_fuente = xlwt.XFStyle()
    for herramienta in arrayHerramientas:
        numero_fila+=1
        for columna in range(len(herramienta)):
            hoja.write(numero_fila, columna, str(herramienta[columna]), estilo_fuente)
        
    
    
    
        
    libro.save(response)
    return response    


def excelInventarioHerramientas(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Inventario Cíclico Herramientas Almacén '+str(datetime.today().strftime('%Y-%m-%d'))+'.xls'
    
    #creación de libro de excel
    libro = xlwt.Workbook(encoding='utf-8')
    hoja = libro.add_sheet('Reporte de existencias')
    
    numero_fila = 0
    estilo_fuente = xlwt.XFStyle()
    estilo_fuente.font.bold = True
    
    columnas = ['Id Herramienta','Código Herramienta', 'Nombre herramienta', 'Marca', 'Tipo','Categoria/Nombre corto', 'SKU','Stock','Cantidad en existencia Almacén','Cantidad Dañadas','Total Cantidades','Total Cantidades Contadas','¿Con faltante?','Diferencia', 'Total Cantidades en prestamo']
    for campo in range(len(columnas)):
        hoja.write(numero_fila, campo, columnas[campo], estilo_fuente)
        
    todasLasHerramientas = HerramientasAlmacen.objects.all()
    
    arrayHerramientas = []
    for herramienta in todasLasHerramientas:
        idHerramienta = herramienta.id_herramienta
        codigoHerramienta = herramienta.codigo_herramienta
        nombreHerramienta = herramienta.nombre_herramienta
        nombreCorto = herramienta.nombre_corto
        marca = herramienta.marca
        tipo = herramienta.tipo_herramienta
        sku = herramienta.sku
        stock = herramienta.stock
        existencias = herramienta.cantidad_existencia
        
        
        #CantidadPrestamos ya esta..
        contadorHerramientasEnPrestamo = 0
        consultaPrestamosDeHerramienta = PrestamosAlmacen.objects.filter(estatus="En prestamo")
        for dato in consultaPrestamosDeHerramienta:
            idsHerramientas = dato.id_herramientaInstrumento
            cantidadesHerramientas = dato.cantidades_solicitadas
            
            arregloIdsHerramientas = idsHerramientas.split(",")
            arregloCantidadesHerramientas = cantidadesHerramientas.split(",")
            
            listaHerramientasEnPrestamo = zip(arregloIdsHerramientas,arregloCantidadesHerramientas)
            
            for idhhh, cantidad in listaHerramientasEnPrestamo:
                idH = int(idhhh)
                can = int(cantidad)
                if idH == idHerramienta:
                    contadorHerramientasEnPrestamo = contadorHerramientasEnPrestamo + can
        
        #cantidad dañadas
        cantidadHerramientasDañadas = 0
        consultaHerramientasDañadas = HerramientasAlmacenInactivas.objects.filter(id_herramienta_id__id_herramienta = idHerramienta, motivo_baja="D")
        
        for herramientaDañada in consultaHerramientasDañadas:
            cantidadHerramientasDañadas = cantidadHerramientasDañadas + 1
            
        #Total cantidades
        totalCantidades = existencias + cantidadHerramientasDañadas
        
       
        
        arrayHerramientas.append([idHerramienta, codigoHerramienta, nombreHerramienta, marca,  tipo,nombreCorto, sku, stock, existencias,cantidadHerramientasDañadas, totalCantidades, "", "", "", contadorHerramientasEnPrestamo])
        
        
            
        
    estilo_fuente = xlwt.XFStyle()
    for herramienta in arrayHerramientas:
        numero_fila+=1
        for columna in range(len(herramienta)):
            hoja.write(numero_fila, columna, str(herramienta[columna]), estilo_fuente)
        
    
    
    
        
    libro.save(response)
    return response 


def devolucionParcial(request):
    
    #Si ya hay una sesión iniciada..
    if "idSesion" in request.session:
        
        
        estaEnAlmacen = True
        estaEnSolicitudesMarcadas = True
        almacen = True
        solicitantePrestamo = True
        administradordeVehiculos = True


        id_admin=request.session["idSesion"]
        nombreini = request.session['nombres']
        apellidosini = request.session['apellidos']
        correo = request.session['correoSesion']
        foto = fotoAdmin(request)
        nombreCompleto = nombreini + " " + apellidosini #Blanca Yesenia Gaeta Talamantes
        
        
        if request.method == "POST":
            idPrestamoRecibido = request.POST['idPrestamo']
        
       
        infoPrestamo = PrestamosAlmacen.objects.filter(id_prestamo = idPrestamoRecibido)
            
        for dato in infoPrestamo:
            idEmpleadoSolicitante = dato.id_empleado_solicitante_id
            herramientasSolicitadas = dato.id_herramientaInstrumento
            cantidadesSolicitadas = dato.cantidades_solicitadas
            otro = dato.otro
            
        #Información de empleado
        consultaEmpleado = Empleados.objects.filter(id_empleado = idEmpleadoSolicitante)
        for datoEmpleado in consultaEmpleado:
            nombre = datoEmpleado.nombre
            apellidos = datoEmpleado.apellidos
            nombreCompletoEmpleadoSolicitante = nombre + " " + apellidos
                
            idArea = datoEmpleado.id_area_id
            consultaArea = Areas.objects.filter(id_area = idArea)
            for datoArea in consultaArea:
                nombreDepartamento = datoArea.nombre
                colorDepartamento = datoArea.color
                    
        #Información de herramientas
        arregloCantidadesHerramientas = cantidadesSolicitadas.split(",")
        herramientasPrestadas = []
        herramientasPrestadasModalsBaja = []
            
        arregloIdsHerramientasAPrestar = herramientasSolicitadas.split(",")
        for idHerramienta in arregloIdsHerramientasAPrestar:
            consultaHerramienta = HerramientasAlmacen.objects.filter(id_herramienta = idHerramienta)
                
            for datoHerramienta in consultaHerramienta:
                id_herramienta = datoHerramienta.id_herramienta
                codigo_herramienta = datoHerramienta.codigo_herramienta
                tipo_herramienta = datoHerramienta.tipo_herramienta
                nombre_herramienta = datoHerramienta.nombre_herramienta
                marca = datoHerramienta.marca
                imagen = datoHerramienta.imagen_herramienta
                descripcion_herramienta = datoHerramienta.descripcion_herramienta
                unidad_herramienta = datoHerramienta.unidad
                sku_herramienta = datoHerramienta.sku
                cantidad_existencia = datoHerramienta.cantidad_existencia
                    
            herramientasPrestadas.append([id_herramienta, codigo_herramienta, tipo_herramienta,
                                             nombre_herramienta, marca, imagen, descripcion_herramienta,
                                             unidad_herramienta, sku_herramienta, cantidad_existencia])
            herramientasPrestadasModalsBaja.append([id_herramienta, codigo_herramienta, tipo_herramienta,
                                             nombre_herramienta, marca, imagen, descripcion_herramienta,
                                             unidad_herramienta, sku_herramienta, cantidad_existencia])
            
            
        listaHerramientas = zip(herramientasPrestadas, arregloCantidadesHerramientas)
            
        return render(request, "empleadosCustom/almacen/devolucionParcial.html", {"solicitantePrestamo":solicitantePrestamo,"estaEnAlmacen":estaEnAlmacen,"estaEnSolicitudesMarcadas":estaEnSolicitudesMarcadas,"almacen":almacen,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo, 
                                                                                   "infoPrestamo":infoPrestamo, "nombreCompletoEmpleadoSolicitante":nombreCompletoEmpleadoSolicitante,
                                                                                   "nombreDepartamento":nombreDepartamento, "colorDepartamento":colorDepartamento, "listaHerramientas":listaHerramientas, "otro":otro, "herramientasPrestadasModalsBaja":herramientasPrestadasModalsBaja, "administradordeVehiculos":administradordeVehiculos})
    #Si le da al inicio y no hay una sesión iniciada..
    else:
        return redirect('/login/') #redirecciona a url de inicio
    
    
    
def guardarDevolucionParcial(request):
    
    #Si ya hay una sesión iniciada..
    if "idSesion" in request.session:
        
        if request.method == "POST":
            idPrestamoGuardar = request.POST['idPrestamoGuardar']
            condicionesEntrega = request.POST['condicionesEntrega']
            
            name= "cantidadDevolver"
            
            consultaPrestamo = PrestamosAlmacen.objects.filter(id_prestamo = idPrestamoGuardar)
            
            for datos in consultaPrestamo:
                idsHerramientas = datos.id_herramientaInstrumento
                cantidades = datos.cantidades_solicitadas
            
            arregloIdsHerramientas = idsHerramientas.split(",")
            arregloCantidades = cantidades.split(",")
            
            cantidadesParcialmenteEntregadas = []
            
            for idh in arregloIdsHerramientas:
                stridh = str(idh)
                nameCantidadDevolver = name + stridh #cantidadDevolver1, 2.. 6. 9..
                
                cantidadActualizadaHerramientaIndividual = request.POST[nameCantidadDevolver]
                cantidadesParcialmenteEntregadas.append(cantidadActualizadaHerramientaIndividual)
                
            nuevasCantidades = []
            
            listaHerramientas = zip(arregloIdsHerramientas,arregloCantidades, cantidadesParcialmenteEntregadas)
            
            for herramienta, cantidad, cantidadParcialmenteEntregada in listaHerramientas:
                intHerramienta = int(herramienta)
                intCantidad = int(cantidad)
                intCantidadEntregada = int(cantidadParcialmenteEntregada)
                
                resta = intCantidad - intCantidadEntregada
                nuevasCantidades.append(resta)
                
                #Suma de cantidades
                consultaHerramienta = HerramientasAlmacen.objects.filter(id_herramienta = intHerramienta)
                for dato in consultaHerramienta:
                    existenciaActual = dato.cantidad_existencia
                existenciaActualizada = existenciaActual + intCantidadEntregada
                actualizacionCantidadHerramienta = HerramientasAlmacen.objects.filter(id_herramienta = intHerramienta).update(cantidad_existencia = existenciaActualizada)
                
            stringNuevasCantidades = ""
            contadorCantidadesNuevas = 0
            for cantidadNueva in nuevasCantidades:
                contadorCantidadesNuevas = contadorCantidadesNuevas + 1
                if contadorCantidadesNuevas == 1:
                    stringNuevasCantidades = str(cantidadNueva)
                else:
                    stringNuevasCantidades = stringNuevasCantidades+","+str(cantidadNueva)
                
            
            #actualizarRegistro
            
            actualizacionPrestamo = PrestamosAlmacen.objects.get(id_prestamo = idPrestamoGuardar)
            actualizacionPrestamo.cantidades_solicitadas = stringNuevasCantidades
            actualizacionPrestamo.condiciones = condicionesEntrega
            actualizacionPrestamo.save()
            
            if actualizacionPrestamo:
                #AQUI SE DEBEN DE DAR DE BAJA LAS CANTIDADES SELECCIONADAS
                request.session['prestamoEntregadoParcial'] = "El prestamo "+ str(idPrestamoGuardar)+" ha sido entregado parcialmente satisfactoriamente!"
                
                #Mandar notificación de telegram
                try:
                    tokenTelegram = keysBotCustom.tokenBotPrestamos
                    botCustom = telepot.Bot(tokenTelegram)

                    idGrupoTelegram = keysBotCustom.idGrupo

                    
                    mensaje = "\U0001274C DEVOLUCIÓN PARCIAL DE HERRAMIENTA, PRESTAMO #"+str(idPrestamoGuardar)+" \U0001274C \n Hola \U0001F44B! \n El empleado ha regesado parcialmente herramienta del préstamo: \n"+codigoHerramienta+" - "+nombreHerramienta+ " por "+motivoBaja+"\n Prestamo #"+str(idPrestamoConDaño)+" encargado: "+nombreCompletoEmpleadoPrestamo
                    botCustom.sendMessage(idGrupoTelegram,mensaje)
                except:
                    print("An exception occurred")


                return redirect("/solicitudesMarcadasALM/")

                
            
    
    #Si le da al inicio y no hay una sesión iniciada..
    else:
        return redirect('/login/') #redirecciona a url de inicio
    
    
 
def verRequisicionesHerramientas(request):
    
    #Si ya hay una sesión iniciada..
    if "idSesion" in request.session:
        
        
        estaEnAlmacen = True
        estaEnVerRequisicionesHerramientas = True
        almacen = True
        solicitantePrestamo = True
        administradordeVehiculos = True


        id_admin=request.session["idSesion"]
        nombreini = request.session['nombres']
        apellidosini = request.session['apellidos']
        correo = request.session['correoSesion']
        foto = fotoAdmin(request)
        nombreCompleto = nombreini + " " + apellidosini #Blanca Yesenia Gaeta Talamantes
        
        #Consulta a tabla de requis
        
        consultaRequisicionesPendientes = RequisicionCompraAlmacen.objects.filter(estatus_requi="Pendiente")
        consultaRequisicionesSaldadas = RequisicionCompraAlmacen.objects.filter(estatus_requi="Saldada")
        
        #informacion de empleado
        infoEmpleadoPendiente = []
        infoEmpleadoSaldada = []
        
        #información de herramienta
        infoHerramientaPendiente = []
        infoHerramientaSaldada = []
        
        #Informacion de prestamo
        infoPrestamoPendiente = []
        infoPrestamoPendienteBooleano = []
        infoPrestamoSaldada = []
        infoPrestamoPendienteBooleanoSaldada = []
        
        # Requis pendientes
        for requiPendiente in consultaRequisicionesPendientes:
            idEmpleadoSolicitante = requiPendiente.id_empleado_solicitante_id
            idHerramientaSolicitada = requiPendiente.id_herramienta_id
            idPrestamo = requiPendiente.id_prestamo_id
            
            #infoEmpleado 
            consultaEmpleado = Empleados.objects.filter(id_empleado = idEmpleadoSolicitante)
            for dato in consultaEmpleado:
                nombreEmpleado = dato.nombre
                apellidosEmpleado = dato.apellidos
                idArea = dato.id_area_id
                
                consultaArea = Areas.objects.filter(id_area = idArea)
                for datoArea in consultaArea:
                    nombreArea = datoArea.nombre
                    colorArea = datoArea.color
            nombreCompletoEmpleado = nombreEmpleado + " " + apellidosEmpleado
                    
            infoEmpleadoPendiente.append([nombreCompletoEmpleado, nombreArea, colorArea])
            
            #infoHerramienta
            consultaHerramienta = HerramientasAlmacen.objects.filter(id_herramienta = idHerramientaSolicitada)
            for datoHerramienta in consultaHerramienta:
                idHerramienta = datoHerramienta.id_herramienta
                nombreHerramienta = datoHerramienta.nombre_herramienta
                codigoHerramienta = datoHerramienta.codigo_herramienta
                skuHerramienta = datoHerramienta.sku
                proveedorHerramienta = datoHerramienta.proveedor
                odcHerramienta = datoHerramienta.orden_compra_evidence
                if datoHerramienta.imagen_herramienta == None:
                    imagenHerramienta = "Sin imagen"
                else:
                    imagenHerramienta = datoHerramienta.imagen_herramienta
                existencia = datoHerramienta.cantidad_existencia
                stockNecesario = datoHerramienta.stock
                costounitario = datoHerramienta.costo
                
                cantidadPrestamos = 0
                
                consultaPrestamos = PrestamosAlmacen.objects.filter(estatus="En prestamo")
                for prestamo in consultaPrestamos:
                    idsHerramientas = prestamo.id_herramientaInstrumento
                    cantidadesHerramientas = prestamo.cantidades_solicitadas
                    
                    arregloIdsHerramientas = idsHerramientas.split(",")
                    arregloCantidadesHerramientas = cantidadesHerramientas.split(",")
                    
                    listaHerramientasxPrestamo = zip(arregloIdsHerramientas, arregloCantidadesHerramientas)
                    
                    for herramienta, cantidad in listaHerramientasxPrestamo:
                        intIdHerramienta = int(herramienta)
                        intCantidad = int(cantidad)
                        
                        if idHerramienta == intIdHerramienta:
                            cantidadPrestamos = cantidadPrestamos + intCantidad
            infoHerramientaPendiente.append([idHerramienta, nombreHerramienta, codigoHerramienta, skuHerramienta,proveedorHerramienta,odcHerramienta, imagenHerramienta,existencia, cantidadPrestamos, stockNecesario, costounitario])
            
            #infoPrestamo
            conPrestamo = False
            if idPrestamo == None:
                infoPrestamoPendiente.append("Sin prestamo")
                infoPrestamoPendienteBooleano.append(conPrestamo)
            else:
                conPrestamo = True
                consultaPrestamo = PrestamosAlmacen.objects.filter(id_prestamo = idPrestamo)
                for datoPrestamo in consultaPrestamo:
                    idDelPrestamo = datoPrestamo.id_prestamo
                    proyecto = datoPrestamo.proyecto_tarea
                
                infoPrestamoPendienteBooleano.append(conPrestamo)
                infoPrestamoPendiente.append([idDelPrestamo, proyecto])
                
                
        
        # Requis Saldadas
        for requiSaldada in consultaRequisicionesSaldadas:
            idEmpleadoSolicitante = requiSaldada.id_empleado_solicitante_id
            idHerramientaSolicitada = requiSaldada.id_herramienta_id
            idPrestamo = requiSaldada.id_prestamo_id
            
            #infoEmpleado 
            consultaEmpleado = Empleados.objects.filter(id_empleado = idEmpleadoSolicitante)
            for dato in consultaEmpleado:
                nombreEmpleado = dato.nombre
                apellidosEmpleado = dato.apellidos
                idArea = dato.id_area_id
                
                consultaArea = Areas.objects.filter(id_area = idArea)
                for datoArea in consultaArea:
                    nombreArea = datoArea.nombre
                    colorArea = datoArea.color
            nombreCompletoEmpleado = nombreEmpleado + " " + apellidosEmpleado
                    
            infoEmpleadoSaldada.append([nombreCompletoEmpleado, nombreArea, colorArea])
            
            #infoHerramienta
            consultaHerramienta = HerramientasAlmacen.objects.filter(id_herramienta = idHerramientaSolicitada)
            for datoHerramienta in consultaHerramienta:
                idHerramienta = datoHerramienta.id_herramienta
                nombreHerramienta = datoHerramienta.nombre_herramienta
                codigoHerramienta = datoHerramienta.codigo_herramienta
                skuHerramienta = datoHerramienta.sku
                proveedorHerramienta = datoHerramienta.proveedor
                odcHerramienta = datoHerramienta.orden_compra_evidence
                if datoHerramienta.imagen_herramienta == None:
                    imagenHerramienta = "Sin imagen"
                else:
                    imagenHerramienta = datoHerramienta.imagen_herramienta
                existencia = datoHerramienta.cantidad_existencia
                stockNecesario = datoHerramienta.stock
                costounitario = datoHerramienta.costo
                
                cantidadPrestamos = 0
                
                consultaPrestamos = PrestamosAlmacen.objects.filter(estatus="En prestamo")
                for prestamo in consultaPrestamos:
                    idsHerramientas = prestamo.id_herramientaInstrumento
                    cantidadesHerramientas = prestamo.cantidades_solicitadas
                    
                    arregloIdsHerramientas = idsHerramientas.split(",")
                    arregloCantidadesHerramientas = cantidadesHerramientas.split(",")
                    
                    listaHerramientasxPrestamo = zip(arregloIdsHerramientas, arregloCantidadesHerramientas)
                    
                    for herramienta, cantidad in listaHerramientasxPrestamo:
                        intIdHerramienta = int(herramienta)
                        intCantidad = int(cantidad)
                        
                        if idHerramienta == intIdHerramienta:
                            cantidadPrestamos = cantidadPrestamos + intCantidad
            infoHerramientaSaldada.append([idHerramienta, nombreHerramienta, codigoHerramienta, skuHerramienta,proveedorHerramienta,odcHerramienta, imagenHerramienta,existencia, cantidadPrestamos, stockNecesario, costounitario])
            
            #infoPrestamo
            conPrestamo = False
            if idPrestamo == None:
                infoPrestamoSaldada.append("Sin prestamo")
                infoPrestamoPendienteBooleanoSaldada.append(conPrestamo)
            else:
                conPrestamo = True
                consultaPrestamo = PrestamosAlmacen.objects.filter(id_prestamo = idPrestamo)
                for datoPrestamo in consultaPrestamo:
                    idDelPrestamo = datoPrestamo.id_prestamo
                    proyecto = datoPrestamo.proyecto_tarea
                
                infoPrestamoPendienteBooleanoSaldada.append(conPrestamo)
                infoPrestamoSaldada.append([idDelPrestamo, proyecto])
        
                
        #Listtas de prestamos pendientes    
        listaPrestamosPendientes = zip(consultaRequisicionesPendientes, infoEmpleadoPendiente, infoHerramientaPendiente, infoPrestamoPendiente, infoPrestamoPendienteBooleano)
        listaPrestamosPendientesModalEntrada = zip(consultaRequisicionesPendientes, infoEmpleadoPendiente, infoHerramientaPendiente, infoPrestamoPendiente, infoPrestamoPendienteBooleano)
                
        #Listas de requis Saldadas
        listaRequisSaldadas = zip(consultaRequisicionesSaldadas, infoEmpleadoSaldada, infoHerramientaSaldada, infoPrestamoSaldada, infoPrestamoPendienteBooleanoSaldada)
            
            
        if 'herramientaEntrada' in request.session:
            herramientaEntrada = request.session['herramientaEntrada']
            del request.session['herramientaEntrada']
            return render(request, "empleadosCustom/almacen/requis/verRequisicionesHerramientas.html", {"solicitantePrestamo":solicitantePrestamo,"estaEnAlmacen":estaEnAlmacen,"estaEnVerRequisicionesHerramientas":estaEnVerRequisicionesHerramientas,"almacen":almacen,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo,
                                                                                                    "listaPrestamosPendientes":listaPrestamosPendientes, "listaPrestamosPendientesModalEntrada":listaPrestamosPendientesModalEntrada, "listaRequisSaldadas":listaRequisSaldadas, "herramientaEntrada":herramientaEntrada, "administradordeVehiculos":administradordeVehiculos})

        return render(request, "empleadosCustom/almacen/requis/verRequisicionesHerramientas.html", {"solicitantePrestamo":solicitantePrestamo,"estaEnAlmacen":estaEnAlmacen,"estaEnVerRequisicionesHerramientas":estaEnVerRequisicionesHerramientas,"almacen":almacen,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo,
                                                                                                    "listaPrestamosPendientes":listaPrestamosPendientes, "listaPrestamosPendientesModalEntrada":listaPrestamosPendientesModalEntrada, "listaRequisSaldadas":listaRequisSaldadas, "administradordeVehiculos":administradordeVehiculos})
    #Si le da al inicio y no hay una sesión iniciada..
    else:
        return redirect('/login/') #redirecciona a url de inicio
    
    

def entradaHerramientaPorRequi(request):
    #Si ya hay una sesión iniciada..
    
    if "idSesion" in request.session:
        id_admin=request.session["idSesion"]
        
        if request.method == "POST":
            idHerramientaEntrada = request.POST['idHerramientaActualizar']
            idRequi = request.POST['idRequi']
            cantidadHerramientaEntrada = request.POST['cantidadHerramientaEntrada']
            proveedorEntrada = request.POST['proveedorEntrada']
            odcEntrada = request.POST['odcEntrada']
            
            consultaHerramienta = HerramientasAlmacen.objects.filter(id_herramienta = idHerramientaEntrada)
            for dato in consultaHerramienta:
                existenciaActual = dato.cantidad_existencia
                odcActual = dato.orden_compra_evidence
                proveedorActual = dato.proveedor
                stockActual = dato.stock
                codigoHerramientaActualizar = dato.codigo_herramienta
                odcActual = dato.orden_compra_evidence
                proveedorActual = dato.proveedor
            
            existenciaActualizada = int(existenciaActual) + int(cantidadHerramientaEntrada)
            
            if stockActual < existenciaActualizada:
            
                actualizacionHerramienta = HerramientasAlmacen.objects.filter(id_herramienta = idHerramientaEntrada).update(cantidad_existencia = existenciaActualizada,
                                                                                                                        proveedor = proveedorEntrada, orden_compra_evidence = odcEntrada, stock = existenciaActualizada)
            else:
            
                actualizacionHerramienta = HerramientasAlmacen.objects.filter(id_herramienta = idHerramientaEntrada).update(cantidad_existencia = existenciaActualizada,
                                                                                                                        proveedor = proveedorEntrada, orden_compra_evidence = odcEntrada)
            
            if actualizacionHerramienta:
                fechaEntrada = datetime.now()
                #Actualizar requi a saldada
                actualizacionRequi = RequisicionCompraAlmacen.objects.filter(id_requi = idRequi).update(estatus_requi = "Saldada")
                actRequi = RequisicionCompraAlmacen.objects.get(id_requi = idRequi)
                actRequi.fehca_requiEntrada = fechaEntrada
                actRequi.save()
                
                fecha = datetime.now()
                
               
                
                #Guardar alta y mandar correo
                existenciaBool = False
            
                odcBool = False
                proveedorBool = False
                
                mensajeExistencia = ""
                mensajeODC = ""
                mensajeProveedor = ""
                
                ultimaSolicitud = 0
                consultaSolicitudes = altasAlmacen.objects.all()
                for solicitudes in consultaSolicitudes:
                    ultimaSolicitud = solicitudes.id_alta
               
                
                if existenciaActualizada == 0:
                    existenciaBool = False
                    mensajeExistencia = "No se actualizarán cantidades en existencia."
                else:
                    existenciaBool = True
                    mensajeExistencia = "Se actualizaron las cantidades de "+str(existenciaActual)+ " a "+str(existenciaActualizada) + " unidades. (Se agregarán "+str(cantidadHerramientaEntrada)+" unidades)"
            
                if odcEntrada == odcActual:
                    odcBool = False
                    mensajeODC = "No se actualizará la ODC ligada en evidence."
                else:
                    odcBool = True
                    mensajeODC = "Se actualizó la última ODC en Evidence de esta herramienta: "+str(odcEntrada)
                    
                if proveedorEntrada == proveedorActual:
                    proveedorBool = False
                    mensajeProveedor = "No se actualizará el proveedor de esta herramienta."
                else:
                    proveedorBool = True
                    mensajeProveedor = "Se actualizó al proveedor: "+str(proveedorEntrada)
                
                
                stockBool = False
                codigoBool = False
                mensajeStock = "No se actualizará la cantidad en Stock."
                mensajeCodigo = "No se actualizará el código de la herramienta."
                if stockActual < existenciaActualizada:
                    stockBool = True
                    mensajeStock = "Se actualizó el stock de "+str(stockActual) + " a "+str(existenciaActualizada) + " unidades."
                
                fecha = datetime.now()
                contadorActualizaciones = 0
                actualizaciones = altasAlmacen.objects.all()
                for actualizacion in actualizaciones:
                    contadorActualizaciones = actualizacion.id_alta
                
                contadorActualizaciones = contadorActualizaciones+1
                
                porRequi = True
                idRequi = str(idRequi)
                
                asunto = "CS | Nueva actualización de herramienta. Numero "+str(contadorActualizaciones)
                plantilla = "empleadosCustom/almacen/correos/correoSolicitudAlta.html"
                html_mensaje = render_to_string(plantilla, {"ultimaSolicitud":ultimaSolicitud,"fecha_solicitud_actualizacion":fecha,
                                                            "consultaHerramienta":consultaHerramienta,
                                                            "existenciaBool":existenciaBool, "mensajeExistencia":mensajeExistencia,
                                                            "stockBool":stockBool,"mensajeStock":mensajeStock,
                                                            "codigoBool":codigoBool, "mensajeCodigo":mensajeCodigo,
                                                            "odcBool":odcBool,"mensajeODC":mensajeODC,
                                                            "proveedorBool":proveedorBool, "mensajeProveedor":mensajeProveedor, "porRequi":porRequi, "idRequi":idRequi})
                email_remitente = settings.EMAIL_HOST_USER
                email_destino = ['sistemas@customco.com.mx']
                mensaje = EmailMessage(asunto, html_mensaje, email_remitente, email_destino)
                mensaje.content_subtype = 'html'
                mensaje.send()
                
                
               
                alta = altasAlmacen(id_herramienta = HerramientasAlmacen.objects.get(id_herramienta = idHerramientaEntrada),
                                                  cantidad_agregar = mensajeExistencia,
                                                  stockActualizado = mensajeStock,
                                                  codigoActualizado = mensajeCodigo,
                                                  fecha_alta = fecha,
                                                  orden_compra_evidence_act = mensajeODC,
                                                  proveedor_alta = mensajeProveedor,
                                                  estatus_alta = "Realizada",
                                                  requi = str(idRequi))
                alta.save()
                
                
                
                
                request.session['herramientaEntrada'] = "Se le ha dado entrada a la requisición "+str(idRequi)+" satisfactoriamente!"
                
                
                return redirect('/verRequisicionesHerramientas/')
    #Si le da al inicio y no hay una sesión iniciada..
    else:
        return redirect('/login/') #redirecciona a url de inicio
    
def descontarDeInventario(request):
    #Si ya hay una sesión iniciada..
    
    if "idSesion" in request.session:
        
        
        if request.method == "POST":
            idHerramientaADescontarInventario = request.POST['idHerramientaADescontarInventario']
            
            
            consultaBajaHerramienta = HerramientasAlmacenInactivas.objects.filter(id_herramientaInactiva = idHerramientaADescontarInventario).update(enInventario = "No")

            if consultaBajaHerramienta:
                request.session['herramientaDescontada'] = "Se ha descontado la herramienta dañada del inventario satisfactoriamente!"
                
                
                return redirect('/verHerramientasALM/')
    #Si le da al inicio y no hay una sesión iniciada..
    else:
        return redirect('/login/') #redirecciona a url de inicio
    
    
    
    
#PDF COSTOS ALMACEN
def pdfCostosAlmacén(request):
    if "idSesion" in request.session:
            
        #crear el http response con pdf
        respuesta = HttpResponse(content_type='application/pdf')
        respuesta['Content-Disposition'] = 'attachment; filename=Reporte Costos Herramientas Almacen '+str(datetime.today().strftime('%Y-%m-%d'))+'.pdf'
        #Crear objeto PDF 
        buffer =BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        base_dir = str(settings.BASE_DIR) #C:\Users\AuxSistemas\Desktop\CS Escritorio\Custom-System\djangoCS
        #nombre de empresa
        logo = base_dir+'/static/images/logoCustom.PNG'   
        c.drawImage(logo, 40,700,120,70, preserveAspectRatio=True)
            
        c.setFont('Helvetica-Bold', 12)
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
        c.setFillColor(color_guinda)
            
        c.setFont('Helvetica-Bold', 12)
        c.drawString(410,750, "REPORTE DE COSTOS")
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
        c.setFont('Helvetica-Bold', 18)
            
        c.drawString(100,660, 'Reporte de costos de herramienta de almacén')
        c.setFont('Helvetica-Bold', 15)
        c.drawString(50,620, 'Tabla de totales')
        
        #obtener datos de area
        
        datosAreas= Areas.objects.all()
        cantidad_empleados = []
        
        for area in datosAreas:
            id_area_una = area.id_area
            areaInt = int(id_area_una)
            
            empleadosEnArea = Empleados.objects.filter(id_area_id__id_area = areaInt)
            
            numero_empleados = 0
            for empleado in empleadosEnArea:
                numero_empleados+=1
            
            cantidad_empleados.append(numero_empleados)
            
        listaAreas = zip(datosAreas, cantidad_empleados)
        #header de tabla
        styles = getSampleStyleSheet()
        styleBH =styles["Normal"]
        styleBH.alignment = TA_CENTER
        styleBH.fontSize = 10
        
        
        h1 = Paragraph('''Herramientas en almacén''', styleBH)
        h2 = Paragraph('''Herramientas en préstamo''', styleBH)
        h3 = Paragraph('''Herramientas Activas (en almacén + prestadas)''', styleBH)
        h4 = Paragraph('''Herramientas Dañadas (siguen en inventario físico)''', styleBH)
        h5 = Paragraph('''Herramientas Dañadas inactivas (fuera de inventario)''', styleBH)
        h6 = Paragraph('''Herramientas Extraviadas (fuera de inventario)''', styleBH)
        filasTabla=[]
        filasTabla.append([h1, h2, h3, h4, h5, h6])
        #Tabla
        styleN = styles["BodyText"]
        styleN.alignment = TA_CENTER
        styleN.fontSize = 7
        
        high = 545
        
        cantidadHerramientasAlmacen = 0
        cantidadHerramientasAlmacenStr = ""
        
        
        cantidadHerramientasEnPrestamo = 0
        cantidadHerramientasEnPrestamoStr = ""
        
        cantidadHerramientasActivas = 0
        cantidadHerramientasActivasStr = ""
        
        cantidadHerramientasDañadas = 0
        cantidadHerramientasDañadasStr = ""
        
        cantidadHerramientasDañadasInactivas = 0
        cantidadHerramientasDañadasInactivasStr = ""
        
        cantidadHerramientasExtraviadas = 0
        cantidadHerramientasExtraviadasStr = ""
        
        #Cantidad Herramientas Almacén
        consultaHerramientas = HerramientasAlmacen.objects.all()
        costoTotalHerramientasActivas = 0
        stringCostoTotalHerramientasActivas = ""
        
        for herramienta in consultaHerramientas:
            cantidadHerramienta = herramienta.cantidad_existencia
            costoHerramienta = herramienta.costo
            
            costoTotalHerramienta = float(cantidadHerramienta) * costoHerramienta
            
            costoTotalHerramientasActivas = costoTotalHerramientasActivas + costoTotalHerramienta
            
            cantidadHerramientasAlmacen = cantidadHerramientasAlmacen + int(cantidadHerramienta)
        
        cantidadHerramientasAlmacenStr = str(cantidadHerramientasAlmacen) + " unidades"
        
        
        #CantidadHerramientasEnPrestamo
        consultaPrestamosAlmacen = PrestamosAlmacen.objects.filter(estatus="En prestamo")
        costoTotalHerramientasEnPrestamo = 0
        for prestamo in consultaPrestamosAlmacen:
            cantidades = prestamo.cantidades_solicitadas
            idsHerramientas = prestamo.id_herramientaInstrumento
            sumaCantidades = 0
            arregloCantidades = cantidades.split(",")
            arregloIdsHerramienta = idsHerramientas.split(",")
            
            lista = zip(arregloIdsHerramienta, arregloCantidades)
            costoHerramientasEnPrestamo = 0
            for idH, cantidad in lista:
                
                intCantidad = int(cantidad)
                intid = int(idH)
                sumaCantidades = sumaCantidades + intCantidad
                
                consultaHerramienta = HerramientasAlmacen.objects.filter(id_herramienta = intid)
                for datoHerramienta in consultaHerramienta:
                    costoHerramienta = datoHerramienta.costo
                costoTotalHerramienta = costoHerramienta * float(intCantidad)
                costoHerramientasEnPrestamo = costoHerramientasEnPrestamo + costoTotalHerramienta
                
            cantidadHerramientasEnPrestamo = cantidadHerramientasEnPrestamo + sumaCantidades
            costoTotalHerramientasEnPrestamo = costoTotalHerramientasEnPrestamo + costoHerramientasEnPrestamo
        cantidadHerramientasEnPrestamoStr = str(cantidadHerramientasEnPrestamo) + " unidades"
        
        sumaCostosActivos = costoTotalHerramientasActivas + costoTotalHerramientasEnPrestamo
        stringCostoTotalHerramientasActivas = str(sumaCostosActivos)
        
        #Herramientas Activas
        cantidadHerramientasActivas = cantidadHerramientasAlmacen + cantidadHerramientasEnPrestamo
        cantidadHerramientasActivasStr = str(cantidadHerramientasActivas) + " unidades"
            
        #Herramientas Dañadas en inventario
        consultaDañadasInventario = HerramientasAlmacenInactivas.objects.filter(motivo_baja = "D", enInventario = "Si")
        costoTotalHerramientasDañadasEnInventario = 0
        costoTotalHerramientasDañadasEnInventarioStr = ""
        for x in consultaDañadasInventario:
            cantidadHerramientasDañadas = cantidadHerramientasDañadas + 1
            idHerramienta = x.id_herramienta_id
            
            consultaHerramienta = HerramientasAlmacen.objects.filter(id_herramienta = idHerramienta)
            for datoHerramienta in consultaHerramienta:
                costo=datoHerramienta.costo
            costoTotalHerramientasDañadasEnInventario = costoTotalHerramientasDañadasEnInventario + costo
        cantidadHerramientasDañadasStr = str(cantidadHerramientasDañadas) + " unidades"
        costoTotalHerramientasDañadasEnInventarioStr = str(costoTotalHerramientasDañadasEnInventario)
        
        costoTotalInventarioFísico = costoTotalHerramientasActivas + costoTotalHerramientasDañadasEnInventario
        
        #Herramientas Dañadas que ya no estan en el inventario
        consultaDañadasInventarioNo = HerramientasAlmacenInactivas.objects.filter(motivo_baja = "D", enInventario = "No")
        costoTotalHerramientasDañadasNoInventario = 0
        for x in consultaDañadasInventarioNo:
            cantidadHerramientasDañadasInactivas = cantidadHerramientasDañadasInactivas + 1
            idHerramienta = x.id_herramienta_id
            
            consultaHerramienta = HerramientasAlmacen.objects.filter(id_herramienta = idHerramienta)
            for datoHerramienta in consultaHerramienta:
                costo=datoHerramienta.costo
            costoTotalHerramientasDañadasNoInventario = costoTotalHerramientasDañadasEnInventario + costo
        cantidadHerramientasDañadasInactivasStr = str(cantidadHerramientasDañadasInactivas) + " unidades"
        
        #Herramientas Extraviadas
        consultaExtraviadas = HerramientasAlmacenInactivas.objects.filter(motivo_baja = "E", enInventario = "No")
        costoTotalHerramientasExtraviadas = 0
        for x in consultaExtraviadas:
            cantidadHerramientasExtraviadas = cantidadHerramientasExtraviadas + 1
            idHerramienta = x.id_herramienta_id
            
            consultaHerramienta = HerramientasAlmacen.objects.filter(id_herramienta = idHerramienta)
            for datoHerramienta in consultaHerramienta:
                costo=datoHerramienta.costo
            costoTotalHerramientasExtraviadas = costoTotalHerramientasDañadasEnInventario + costo
        cantidadHerramientasExtraviadasStr = str(cantidadHerramientasExtraviadas) + " unidades"
        
        #Costo total perdida
        costoTotalPerdida = costoTotalHerramientasDañadasEnInventario + costoTotalHerramientasDañadasNoInventario + costoTotalHerramientasExtraviadas
        
        #costo total total
        costoTotalTotal = sumaCostosActivos + costoTotalPerdida
        
        
        
        totalUnidadesPerdida = cantidadHerramientasDañadas + cantidadHerramientasDañadasInactivas + cantidadHerramientasExtraviadas
        sumaUnidades = cantidadHerramientasActivas+ totalUnidadesPerdida
        multiplicacion = totalUnidadesPerdida * 100
        resultado = totalUnidadesPerdida / sumaUnidades
        resultadoMasChido = resultado*100
        
        resultadoConDos = round(resultadoMasChido,2)
        fila = [cantidadHerramientasAlmacenStr, cantidadHerramientasEnPrestamoStr, cantidadHerramientasActivasStr,cantidadHerramientasDañadasStr,cantidadHerramientasDañadasInactivasStr,cantidadHerramientasExtraviadasStr ]
        filasTabla.append(fila)
            
        #escribir tabla
        width, height = letter
        tabla = Table(filasTabla, colWidths=[3 * cm, 3 * cm, 3 * cm, 3 * cm, 3 * cm, 3 * cm])
        tabla.setStyle(TableStyle([
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BACKGROUND', (0, 0), (-1, 0), '#FF9800'),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ]))
        
        
        tabla.wrapOn(c, width, height)
        tabla.drawOn(c, 50, high)
        
        colorVerde = "#4CAF50"
        color_negro="#030305"
        color_guinda="#B03A2E"
        color_rojo = "#F44336"
        color_gris = "#607D8B"
        
        c.setFont('Helvetica-Bold', 13)
        c.drawString(100,500, 'Costo Total Herramientas Activas ('+cantidadHerramientasActivasStr+') :')
        c.setFillColor(colorVerde)
        c.drawString(135,475, '$'+stringCostoTotalHerramientasActivas+' MXN.')
        c.setFillColor(color_negro)
        
        c.drawString(100,450, 'Costo Total Herramientas Dañadas en inventario ('+cantidadHerramientasDañadasStr+') :')
        c.setFillColor(color_rojo)
        c.drawString(135,425, '+ $'+costoTotalHerramientasDañadasEnInventarioStr+' MXN.')
        c.setFillColor(color_negro)
        c.setFont('Helvetica-Bold', 10)
        c.drawString(280,425, 'Costo Total Inventario Físico: $'+str(costoTotalInventarioFísico)+' MXN.')
        c.setFont('Helvetica-Bold', 13)
        c.drawString(100,395, 'Costo Total Herramientas Dañadas fuera de inventario ('+cantidadHerramientasDañadasInactivasStr+') :')
        c.setFillColor(color_rojo)
        c.drawString(135,370, '+ $'+str(costoTotalHerramientasDañadasNoInventario)+' MXN.')
        c.setFillColor(color_negro)
        
        c.drawString(100,340, 'Costo Total Herramientas extraviadas ('+cantidadHerramientasExtraviadasStr+') :')
        c.setFillColor(color_rojo)
        c.drawString(135,315, '+ $'+str(costoTotalHerramientasExtraviadas)+' MXN.')
        
        c.setFillColor(color_negro)
        
        c.setFont('Helvetica-Bold', 15)
        c.drawString(100,285, 'Costo Total Pérdida :')
        c.setFillColor(color_rojo)
        c.drawString(135,260, '= $'+str(costoTotalPerdida)+' MXN.')
        
        c.setFillColor(color_negro)
        
        c.drawString(30,220, 'Costo Total de herramientas')
        c.drawString(30,195, '(activas, dañadas y extraviadas) :')
        c.setFillColor(color_gris)
        c.drawString(35,170, '$'+stringCostoTotalHerramientasActivas+' + $'+str(costoTotalPerdida)+'')
        c.drawString(35,145, '= $'+str(costoTotalTotal)+' MXN.')
        c.setFillColor(color_negro)
        
        c.drawString(100,90, 'Del 100% de herramientas, el '+str(resultadoConDos)+'% es pérdida de las mismas.')
        
        
        
        #grafico de pastel
        b = Drawing()
        pie = Pie()
        pie.x = 0
        pie.y = 0
        pie.height = 160
        pie.width = 160
        pie.data = [totalUnidadesPerdida, cantidadHerramientasActivas ]
        strContestadas = str(totalUnidadesPerdida) + " unidades Perdidas"
        strFaltantes = str(cantidadHerramientasActivas) + " unidades Activas"
        pie.labels = [strContestadas, strFaltantes]
        pie.slices.strokeWidth = 0.5
        pie.slices[1].popout = 10
        pie.slices[0].fillColor= colors.HexColor("#F44336")
        pie.slices[1].fillColor=colors.HexColor("#4CAF50")
        b.add(pie)
        x,y = 380,130 
        renderPDF.draw(b, c, x, y, showBoundary=False)
        
        c.setFillColor(color_negro)
        #linea guinda
        
        c.setFillColor(color_guinda)
        c.setStrokeColor(color_guinda)
        c.line(40,60,560,60)
        
        
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
    else:
        return redirect('/login/') #redirecciona a url de inicio
    

def listaAltasAlmacen(request):
    
    #Si ya hay una sesión iniciada..
    if "idSesion" in request.session:
        
        
        estaEnAlmacen = True
        estaEnAltasAlmacen = True
        almacen = True
        solicitantePrestamo = True
        administradordeVehiculos = True


        id_admin=request.session["idSesion"]
        nombreini = request.session['nombres']
        apellidosini = request.session['apellidos']
        correo = request.session['correoSesion']
        foto = fotoAdmin(request)
        nombreCompleto = nombreini + " " + apellidosini #Blanca Yesenia Gaeta Talamantes
        
        arrayHerramientasPendientes = []
        altasPendientes = altasAlmacen.objects.filter(estatus_alta = "Realizada")
        
        boolCambioCantidad = []
        cambioCantidad = []
        
        boolCambioCodigo = []
        cambioCodigo = []
        
        boolCambioStock = []
        cambioStock = []
        
        boolCambioODC = []
        cambioODC = []
        
        boolCambioProveedor = []
        cambioProveedor = []
        
        for altaPendiente in altasPendientes:
            idHerramienta = altaPendiente.id_herramienta_id
            consultaHerramienta = HerramientasAlmacen.objects.filter(id_herramienta = idHerramienta)
            
            #Datos de herramienta
            for datoHerramienta in consultaHerramienta:
                codigoActual = datoHerramienta.codigo_herramienta
                skuActual = datoHerramienta.sku
                nombreActual = datoHerramienta.nombre_herramienta
                nombreCorto = datoHerramienta.nombre_corto
                imagen = datoHerramienta.imagen_herramienta
                existenciaActual = datoHerramienta.cantidad_existencia
                stockActual = datoHerramienta.stock
                odcActual = datoHerramienta.orden_compra_evidence
                proveedorActual = datoHerramienta.proveedor
             
            arrayHerramientasPendientes.append([codigoActual,skuActual,nombreActual,nombreCorto,imagen,existenciaActual,stockActual,proveedorActual]) 
            
            
            #Cantidades
            cantidadActualizar = altaPendiente.cantidad_agregar
            if cantidadActualizar == 0:
                boolCambioCantidad.append("No actualizar cantidad")
                cambioCantidad.append("No actualizar cantidad")
            else:
                boolCambioCantidad.append("Actualizar cantidad")
                cambioCantidad.append(cantidadActualizar)
                
            #Codigo
            codigoActualizar = altaPendiente.codigoActualizado
            if codigoActualizar == codigoActual:
                boolCambioCodigo.append("No actualizar codigo")
                cambioCodigo.append("No actualizar codigo")
            else:
                boolCambioCodigo.append("Actualizar codigo")
                cambioCodigo.append(codigoActualizar)
                
            #Stock
            stockActualizar = altaPendiente.stockActualizado
            if stockActualizar == stockActual:
                boolCambioStock.append("No actualizar stock")
                cambioStock.append("No actualizar stock")
            else:
                boolCambioStock.append("Actualizar stock")
                cambioStock.append(stockActualizar)
                
            #ODC
            odcActualizar = altaPendiente.orden_compra_evidence_act
            if odcActualizar == odcActual:
                boolCambioODC.append("No actualizar odc")
                cambioODC.append("No actualizar odc")
            else:
                boolCambioODC.append("Actualizar odc")
                cambioODC.append(odcActualizar)
            
            #Proveedor
            proveedorActualizar = altaPendiente.proveedor_alta
            if proveedorActualizar == proveedorActual:
                boolCambioProveedor.append("No actualizar proveedor")
                cambioProveedor.append("No actualizar proveedor")
            else:
                boolCambioProveedor.append("Actualizar proveedor")
                cambioProveedor.append(proveedorActualizar)
                
        listaAltasPendientes = zip(altasPendientes,arrayHerramientasPendientes)
            
            
        
            
                
              
            
        
        
        

        return render(request, "empleadosCustom/almacen/altasbajas/altasAlmacen.html", {"solicitantePrestamo":solicitantePrestamo,"estaEnAlmacen":estaEnAlmacen,"estaEnAltasAlmacen":estaEnAltasAlmacen,"almacen":almacen,"id_admin":id_admin, "nombreCompleto":nombreCompleto, "foto":foto, "correo":correo, "listaAltasPendientes":listaAltasPendientes, "administradordeVehiculos":administradordeVehiculos})
    #Si le da al inicio y no hay una sesión iniciada..
    else:
        return redirect('/login/') #redirecciona a url de inicio
    
def excelInventarioHerramientasCategoria(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Inventario Cíclico Herramientas Almacen x Categoria '+str(datetime.today().strftime('%Y-%m-%d'))+'.xls'
    
    #creación de libro de excel
    libro = xlwt.Workbook(encoding='utf-8')
    hoja = libro.add_sheet('Reporte de categorias')
    
    numero_fila = 0
    estilo_fuente = xlwt.XFStyle()
    estilo_fuente.font.bold = True
    
    columnas = ['Número Categoría','Nombre Categoría', 'Cantidad En Existencia','Cantidad Dañada en inventario','Cantidad Total en inventario','Cantidad contada','Sobrante/Faltante','Cuántas unidades?', 'Cantidad en Préstamo','Cantidad Dañada Fuera de inventario', 'Cantidades extraviadas fuera de inventario']
    for campo in range(len(columnas)):
        hoja.write(numero_fila, campo, columnas[campo], estilo_fuente)
        
    categorias = ["Martillo", "Llave Perica", "Llave Inglesa", "Llave Torx", "Llave Allen", "Llave medida","Multimetro"]
    todasLasHerramientas = HerramientasAlmacen.objects.all()
    
    arrayExcel = []
    arrayNumeroCategoria = []
    nombreCategoria = []
    arrayCantidadesCategoria = []
    arrayDañadasEnInventario = []
    totalesInventarioCategoria = []
    totalesEnPrestamo = []
    totalesDañadasFuera = []
    totalesExtraviadas = []
    
    numCategoria = 0
    for categoria in categorias:
        numCategoria = numCategoria + 1
        nombreCategoria = categoria
        
        totalEnInventario = 0
        contadorProductosEnCategoriaInventarioFisicoDisponible = 0
        contadorProductosDañadosEnInventario = 0
        contadorHerramientaEnPrestamo = 0 
        contadorProductosDañadosFueraInventario = 0
        contadorHerramientasExtraviadas = 0
        consultaHerramientasCategoria = HerramientasAlmacen.objects.filter(nombre_corto = categoria)
        
        for herramienta in consultaHerramientasCategoria: 
            cantidadEnExistenciaActualInventario = herramienta.cantidad_existencia
            contadorProductosEnCategoriaInventarioFisicoDisponible = contadorProductosEnCategoriaInventarioFisicoDisponible + cantidadEnExistenciaActualInventario
            idHerramienta = herramienta.id_herramienta
            
            
            consultaHerramientasDañadasEnInventario = HerramientasAlmacenInactivas.objects.filter(id_herramienta_id__id_herramienta = idHerramienta, enInventario = "Si", motivo_baja = "D")
            numeroDañosHerramienta = 0
            for daño in consultaHerramientasDañadasEnInventario:
                numeroDañosHerramienta = numeroDañosHerramienta + 1
            contadorProductosDañadosEnInventario = contadorProductosDañadosEnInventario + numeroDañosHerramienta
            
            #numero de prestamos
            consultaPrestamos = PrestamosAlmacen.objects.filter(estatus = "En prestamo")
            contadorHerramientaEnPrestamo = 0
            for prestamo in consultaPrestamos:
                idsHerramientasPrestadas = prestamo.id_herramientaInstrumento
                cantidadesHerramientasPrestadas = prestamo.cantidades_solicitadas
                
                arregloIdsHerramientasPrestadas = idsHerramientasPrestadas.split(",")
                arregloCantidadesHerramientas = cantidadesHerramientasPrestadas.split(",")
                
                listaHerramientasEnPrestamo = zip(arregloIdsHerramientasPrestadas, arregloCantidadesHerramientas)
                
                for idH, cantidad in listaHerramientasEnPrestamo:
                    intidH = int(idH)
                    if intidH == idHerramienta:
                        contadorHerramientaEnPrestamo = contadorHerramientaEnPrestamo + int(cantidad)

            #Herramientas dañadas fuera de inventario
            consultaHerramientasDañadasFueraInventario = HerramientasAlmacenInactivas.objects.filter(id_herramienta_id__id_herramienta = idHerramienta, enInventario = "No", motivo_baja = "D")
            numeroDañosHerramientaFueraAlmacen = 0
            for daño in consultaHerramientasDañadasFueraInventario:
                numeroDañosHerramientaFueraAlmacen = numeroDañosHerramientaFueraAlmacen + 1
            contadorProductosDañadosFueraInventario = contadorProductosDañadosFueraInventario + numeroDañosHerramientaFueraAlmacen
        
            #Herramientas extraviadas
            consultaHerramientasExtraviadas = HerramientasAlmacenInactivas.objects.filter(id_herramienta_id__id_herramienta = idHerramienta, enInventario = "No", motivo_baja = "E")
            numeroDañosHerramientaExtraviadas = 0
            for daño in consultaHerramientasExtraviadas:
                numeroDañosHerramientaExtraviadas = numeroDañosHerramientaExtraviadas + 1
            contadorHerramientasExtraviadas = contadorHerramientasExtraviadas + numeroDañosHerramientaExtraviadas
        
        
        totalEnInventario = int(contadorProductosEnCategoriaInventarioFisicoDisponible) + int(contadorProductosDañadosEnInventario)
            
        arrayCantidadesCategoria.append(contadorProductosEnCategoriaInventarioFisicoDisponible)
        arrayDañadasEnInventario.append(contadorProductosDañadosEnInventario)
        totalesInventarioCategoria.append(totalEnInventario)
        totalesEnPrestamo.append(contadorHerramientaEnPrestamo)
        totalesDañadasFuera.append(contadorProductosDañadosFueraInventario)
        totalesExtraviadas.append(contadorHerramientasExtraviadas)
        
        arrayExcel.append([numCategoria, nombreCategoria,contadorProductosEnCategoriaInventarioFisicoDisponible,
                           contadorProductosDañadosEnInventario,totalEnInventario, "", "","",
                           contadorHerramientaEnPrestamo,contadorProductosDañadosFueraInventario,
                           contadorHerramientasExtraviadas])
            
        
    estilo_fuente = xlwt.XFStyle()
    for categoria in arrayExcel:
        numero_fila+=1
        for columna in range(len(categoria)):
            hoja.write(numero_fila, columna, str(categoria[columna]), estilo_fuente)
        
    
    
    
        
    libro.save(response)
    return response 

def quitarPerdida(request):
    #Si ya hay una sesión iniciada..
    
    if "idSesion" in request.session:
        
        
        if request.method == "POST":
            idHerramientaAEliminarDaño = request.POST['idDañoEliminar']
            
            
            herramientaDañadaBorrada = HerramientasAlmacenInactivas.objects.get(id_herramientaInactiva = idHerramientaAEliminarDaño)
            herramientaDañadaBorrada.delete()
            if herramientaDañadaBorrada:
                request.session['herramientaDañadaEliminada'] = "Se ha eliminado el daño y ya no se contará en cuenta!"
                
                
                return redirect('/verHerramientasALM/')
    #Si le da al inicio y no hay una sesión iniciada..
    else:
        return redirect('/login/') #redirecciona a url de inicio
    