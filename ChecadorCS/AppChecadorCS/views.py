from django.shortcuts import render,redirect
from datetime import datetime
from appCS.models import Empleados, Proyectos

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




        return render(request,"registro/registro.html",{"nombresEmpleado":nombresEmpleado,"consultaProyectos":consultaProyectos,"listaEmpleados":listaEmpleados})
    else:
        return redirect("/login/")

def salir(request):
    del request.session["sesionIniciada"]
    return redirect("/login/")

def entrada(request):
    if "sesionIniciada" in request.session:
        return render(request,"registro/entrada.html",{})
    else:
        return redirect("/login/")
