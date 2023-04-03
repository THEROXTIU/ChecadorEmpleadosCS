from os import truncate
from pyexpat import model
from unittest.util import _MAX_LENGTH
from django.db import models
from django.db.models.deletion import CASCADE
from django.forms import CharField, model_to_dict


# Create your models here.
class Areas (models.Model):
    id_area=models.AutoField(primary_key=True)
    nombre=models.CharField(max_length=80)
    color=models.CharField(max_length=80)

    def __str__(self):
        return str(self.id_area())

class Empleados (models.Model):
    id_empleado=models.AutoField(primary_key=True)
    nombre=models.CharField(max_length=80)
    apellidos=models.CharField(max_length=80)
    id_area=models.ForeignKey(Areas, on_delete=models.CASCADE)
    puesto=models.CharField(max_length=80)
    correo=models.EmailField(max_length=80)
    contraseña=models.CharField(max_length=40, null=True)
    imagen_empleado=models.ImageField(upload_to="empleados", null = True)
    activo=models.CharField(max_length=2)
    


    def __str__(self):
        return str(self.id_empleado())

class Equipos (models.Model):
    id_equipo=models.AutoField(primary_key=True)
    tipo=models.CharField(max_length=80)
    marca=models.CharField(max_length=80)
    modelo=models.CharField(max_length=80)
    color=models.CharField(max_length=80)
    imagen=models.ImageField(upload_to="imagenesequipos", null = True)
    pdf=models.FileField(upload_to='pdfequipos', null=True)
    memoriaram=models.CharField(max_length=80)
    procesador=models.CharField(max_length=80)
    sistemaoperativo=models.CharField(max_length=80)
    id_empleado=models.ForeignKey(Empleados, on_delete=models.CASCADE, null = True)
    estado=models.CharField(max_length=80)
    activo=models.CharField(max_length=2)
    modelocargador=models.CharField(max_length=80, null=True)
    fechaMant=models.DateField(null=True)

    def __str__(self):
        return self.id_equipo

class Mouses (models.Model):
    id_mouse = models.AutoField(primary_key=True)
    conexion = models.CharField(max_length=2)
    marca = models.CharField(max_length=30)
    modelo = models.CharField(max_length=30)
    estado = models.CharField(max_length=30)
    foto = models.ImageField(upload_to="mouses", null = True)
    id_equipo = models.ForeignKey(Equipos, on_delete=models.CASCADE, null=True)
    activo = models.CharField(max_length=2)

    def __str__(self):
        return self.id_mouse
    

class Mochilas (models.Model):
    id_mochila = models.AutoField(primary_key=True)
    marca = models.CharField(max_length=30)
    modelo = models.CharField(max_length=30)
    estado = models.CharField(max_length=30)
    foto = models.ImageField(upload_to="mochilas", null = True)
    id_empleado = models.ForeignKey(Empleados, on_delete=models.CASCADE, null=True)
    activo = models.CharField(max_length=2)

    def __str__(self):
        return self.id_mochila
    
class Celulares (models.Model):
    id_celular = models.AutoField(primary_key=True)
    marca = models.CharField(max_length=30)
    modelo = models.CharField(max_length=30)
    color = models.CharField(max_length=30)
    tipo_cargador = models.CharField(max_length=20, null=True)
    modelo_cargador = models.CharField(max_length=40, null=True)
    ram = models.IntegerField()
    numero_setie = models.CharField(max_length=40, null=True)
    numero_imei = models.CharField(max_length=40, null=True)
    telefono = models.CharField(max_length=10, null=True)
    fecha_contratacion_plan = models.DateField(null=True)
    meses_plan = models.IntegerField(null=True)
    en_plan = models.CharField(max_length=2, null=True)
    nombre_plan = models.CharField(max_length=40, null=True)
    compañia = models.CharField(max_length=30, null=True)
    foto = models.ImageField(upload_to="celulares", null = True)
    estado = models.CharField(max_length=30)
    id_empleado = models.ForeignKey(Empleados, on_delete=models.CASCADE, null=True)
    activo = models.CharField(max_length=2)

    def __str__(self):
        return self.id_celular

class Teclados (models.Model):
    id_teclado = models.AutoField(primary_key=True)
    conexion = models.CharField(max_length=2)
    marca = models.CharField(max_length=30)
    modelo = models.CharField(max_length=30)
    estado = models.CharField(max_length=30)
    foto = models.ImageField(upload_to="teclados", null = True)
    id_equipo = models.ForeignKey(Equipos, on_delete=models.CASCADE, null=True)
    activo = models.CharField(max_length=2)

    def __str__(self):
        return self.id_teclado

class Monitores (models.Model):
    id_monitor = models.AutoField(primary_key=True)
    marca = models.CharField(max_length=30)
    modelo = models.CharField(max_length=30)
    estado = models.CharField(max_length=30)
    foto = models.ImageField(upload_to="monitores", null = True)
    id_equipo = models.ForeignKey(Equipos, on_delete=models.CASCADE, null=True)
    activo = models.CharField(max_length=2)

    def __str__(self):
        return self.id_monitor

class Telefonos (models.Model):
    id_telefono = models.AutoField(primary_key=True)
    id_empleado = models.ForeignKey(Empleados,  on_delete=models.CASCADE, null=True)
    conexion = models.CharField(max_length=2)
    marca = models.CharField(max_length=30)
    modelo = models.CharField(max_length=30)
    estado = models.CharField(max_length=30)
    foto = models.ImageField(upload_to="telefonos", null = True)
    extension = models.CharField(max_length=10, null=True)
    nodo = models.CharField(max_length=20, null=True)
    activo = models.CharField(max_length=2)

    def __str__(self):
        return self.id_telefono



class Renovacion_Equipos (models.Model):
    id_renov_equipo=models.AutoField(primary_key=True)
    id_equipo=models.ForeignKey(Equipos, on_delete=models.CASCADE)
    fecha_compra=models.DateField()
    fecha_renov=models.DateField()
    

     

class Carta (models.Model):
    id_carta=models.AutoField(primary_key=True)
    id_empleado=models.ForeignKey(Empleados, on_delete=models.CASCADE)
    id_equipo=models.ForeignKey(Equipos, on_delete=models.CASCADE)
    fecha=models.DateField()
    firma=models.ImageField(upload_to="firmas", null = True)
    
class CartaCelular (models.Model):
    id_carta_celular=models.AutoField(primary_key=True)
    id_empleado=models.ForeignKey(Empleados, on_delete=models.CASCADE)
    id_celular=models.ForeignKey(Celulares, on_delete=models.CASCADE)
    fecha=models.DateField()
    firma=models.ImageField(upload_to="firmasCartaCelular", null = True)
    


class Impresoras (models.Model):
    id_impresora=models.AutoField(primary_key=True)
    marca=models.CharField(max_length=80)
    modelo=models.CharField(max_length=80)
    numserie=models.CharField(max_length=80)
    imagen=models.ImageField(upload_to="impresoras", null = True)
    tipo=models.CharField(max_length=80)
    enred=models.CharField(max_length=2)
    ip=models.CharField(max_length=16, null=True)
    estado=models.CharField(max_length=80)
    activo=models.CharField(max_length=2)
    id_area=models.ForeignKey(Areas, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id_impresora)
    
class Renovacion_Impresoras (models.Model):
    id_renov_imp=models.AutoField(primary_key=True)
    id_impresora=models.ForeignKey(Impresoras,on_delete=CASCADE)
    fecha_compra=models.DateField()
    fecha_renov=models.DateField()

class Cartuchos (models.Model):
    id_cartucho=models.AutoField(primary_key=True)
    marca=models.CharField(max_length=80)
    modelo=models.CharField(max_length=80)
    cantidad=models.IntegerField()
    nuserie=models.CharField(max_length=10)
    color=models.CharField(max_length=80)
    imagenCartucho=models.ImageField(upload_to="cartuchos", null = True)
    id_impresora=models.ForeignKey(Impresoras, on_delete=models.CASCADE)

class CalendarioMantenimiento (models.Model):
    id_calmantenimiento=models.AutoField(primary_key=True)
    id_equipo=models.ForeignKey(Equipos, on_delete=models.CASCADE,null=True)
    id_impresora=models.ForeignKey(Impresoras, on_delete=models.CASCADE,null=True)
    operacion=models.CharField(max_length=200)
    fecha=models.DateField()
    observaciones=models.CharField(max_length=100)

class Programas (models.Model):
    id_programa=models.AutoField(primary_key=True)
    nombre_version=models.CharField(max_length=80)
    tipo=models.CharField(max_length=80)
    licencia=models.CharField(max_length=80)
    idioma=models.CharField(max_length=80)
    sistemaoperativo_arq=models.CharField(max_length=80)
    memoria_ram=models.CharField(max_length=80)
    procesador=models.CharField(max_length=80)
    imagenPrograma=models.ImageField(upload_to="programas", null = True)

    def __str__(self):
        return self.id_programa

class ProgramasArea (models.Model):
    id_area=models.ForeignKey(Areas, on_delete=models.CASCADE)
    id_programa=models.ForeignKey(Programas, on_delete=models.CASCADE)

class EquipoPrograma (models.Model):
    id_equipo=models.ForeignKey(Equipos, on_delete=models.CASCADE)
    id_programa=models.ForeignKey(Programas, on_delete=models.CASCADE)

class Bitacora (models.Model):
    id_empleado=models.ForeignKey(Empleados, on_delete=models.CASCADE)
    tabla=models.CharField(max_length=80)
    id_objeto=models.IntegerField()
    operacion=models.CharField(max_length=80)
    fecha_hora=models.DateTimeField()
    
class Encuestas (models.Model):
    id_encuesta = models.AutoField(primary_key=True)
    fecha_encuesta = models.DateField()
    nombre_encuesta = models.CharField(max_length=80)
    preguntas_multiples = models.CharField(max_length=80)
    preguntas_abiertas = models.CharField(max_length=80)
    def __str__(self):
        return self.id_encuesta
        
class Preguntas (models.Model):
    id_pregunta = models.AutoField(primary_key=True)
    id_encuesta = models.ForeignKey(Encuestas, on_delete=models.CASCADE)
    pregunta = models.TextField(max_length=500)
    tipo = models.CharField(max_length=3)
    clasificacion = models.CharField(max_length=100)
    def __str__(self):
        return self.id_pregunta
    

class Respuestas (models.Model):
    id_respuesta = models.AutoField(primary_key=True)
    id_pregunta = models.ForeignKey(Preguntas, on_delete=models.CASCADE)
    id_empleado = models.ForeignKey(Empleados, on_delete=models.CASCADE)
    respuesta = models.TextField(max_length=100)

  

class EncuestaEmpleadoResuelta (models.Model):
    id_empleado = id_empleado = models.ForeignKey(Empleados, on_delete=models.CASCADE)
    id_encuesta = models.ForeignKey(Encuestas, on_delete=models.CASCADE)

class DiscosDuros (models.Model):
    id_disco = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=30)
    marca = models.CharField(max_length=30)
    capacidad = models.IntegerField(null=True)
    dimension = models.CharField(max_length=20)
    alm_uso = models.IntegerField(null=True)
    alm_libre = models.IntegerField(null=True)
    estado = models.CharField(max_length=30)
    def __str__(self):
        return self.id_disco

class EmpleadosDiscosDuros (models.Model):
    id_empleado = models.ForeignKey(Empleados, on_delete=models.CASCADE)
    id_disco = models.ForeignKey(DiscosDuros, on_delete=models.CASCADE)
    fecha = models.DateField(null=True)

class MemoriasUSB (models.Model):
    id_usb = models.AutoField(primary_key=True)
    marca = models.CharField(max_length=30)
    modelo = models.CharField(max_length=30)
    capacidad = models.IntegerField()
    cantidadStock = models.IntegerField()
    def __str__(self):
        return self.id_usb


class PrestamosSistemas (models.Model):
    id_prestamo = models.AutoField(primary_key=True)
    id_empleado = models.ForeignKey(Empleados, on_delete=models.CASCADE)
    tabla = models.CharField(max_length=100, null=True)
    id_producto = models.CharField(max_length=4, null=True)
    otro = models.CharField(max_length=100, null=True)
    cantidad = models.IntegerField()
    fecha_prestamo = models.DateField()
    firma_entrega = models.ImageField(upload_to="firmasPrestamos", null = True)
    devolucion = models.CharField(max_length=1)
    fecha_entrega = models.DateField(null=True)
    condiciones = models.CharField(max_length=100, null=True)
    firma_devolucion = models.ImageField(upload_to="firmasPrestamos2", null = True)
    estatus = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.id_prestamo
    
class SoportesTecnicos (models.Model):
    id_soporte = models.AutoField(primary_key = True)
    id_empleado = models.ForeignKey(Empleados, on_delete=models.CASCADE)
    fecha_soporte = models.DateField()
    equipo_soporte = models.CharField(max_length=50, null=True)
    tabla = models.CharField(max_length=100)
    operacion = models.CharField(max_length=255)
    observaciones = models.CharField(max_length=250, null=True)
    resuelto_interno = models.CharField(max_length=2, null=True)
    resuelto_proveedor = models.CharField(max_length=50, null=True)
    
    def __str__(self):
        return self.id_soporte
    
    
class ImplementacionSoluciones (models.Model):
    id_implementacion = models.AutoField(primary_key = True)
    titulo_problema = models.CharField(max_length=250)
    descripcion = models.CharField(max_length=250)
    fecha_comienzo = models.DateField()
    fecha_terminada = models.DateField()
    resuelto = models.CharField(max_length=2)
    revisado = models.CharField(max_length=2)
    firma_direccion = models.ImageField(upload_to="firmasImplementaciones", null = True)
    comentarios_direccion =  models.CharField(max_length=250, null=True)
    
    
    def __str__(self):
        return self.id_implementacion


#ALMACEN
class PrestamosAlmacen (models.Model):
    id_prestamo = models.AutoField(primary_key=True)
    fecha_solicitud = models.DateField()
    fecha_requerimiento = models.DateField(null=True)
    id_empleado_solicitante = models.ForeignKey(Empleados, on_delete=models.CASCADE)
    proyecto_tarea = models.CharField(max_length = 100, null=True)
    observaciones = models.CharField(max_length=255)
    id_herramientaInstrumento = models.CharField(max_length=100, null=True)
    cantidades_solicitadas = models.CharField(max_length=100, null=True)
    otro = models.CharField(max_length=100, null=True)
    fecha_prestamo = models.DateField(null=True)
    firma_prestamo = models.ImageField(upload_to="firmasPrestamosAlmacen", null = True)
    fecha_devolucion = models.DateField(null=True)
    firma_devolucion = models.ImageField(upload_to="firmasDevolucionAlmacen", null = True)
    condiciones = models.CharField(max_length=100, null=True)
    estatus = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.id_prestamo
    
class HerramientasAlmacen (models.Model):
    id_herramienta = models.AutoField(primary_key=True)
    codigo_herramienta = models.CharField(max_length=6)
    tipo_herramienta = models.CharField(max_length=15, null=True)
    nombre_herramienta = models.CharField(max_length=100)
    nombre_corto = models.CharField(max_length=60, null=True)
    descripcion_herramienta = models.TextField()
    marca = models.CharField(max_length=50)
    unidad = models.CharField(max_length=50)
    sku = models.CharField(max_length=100)
    cantidad_existencia = models.IntegerField(null=True)
    stock = models.IntegerField(null=True)
    costo = models.FloatField(null=True)
    imagen_herramienta = models.ImageField(upload_to="imagenesHerramientas", null = True)
    estado_herramienta = models.CharField(max_length=2)
    motivo_estado = models.CharField(max_length=200)
    fecha_alta = models.DateField()
    orden_compra_evidence = models.CharField(max_length=30, null=True)
    proveedor = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.id_herramienta
    
    def json(self):
        return {
            'id_herramienta':    self.id_herramienta,
            'codigo': self.codigo_herramienta,
            'tipo_herramienta': self.tipo_herramienta,
            'nombre_herramienta': self.nombre_herramienta,
            'nombre_corto': self.nombre_corto,
            'descripcion_herramienta': self.descripcion_herramienta,
            'marca': self.marca,
            'unidad': self.unidad,
            'sku': self.sku,
            'cantidad_existencia': self.cantidad_existencia,
            'stock':self.stock,
            'costo':self.costo,
            'imagen_herramienta': str(self.imagen_herramienta),
            'estado_herramienta': self.estado_herramienta,
            'motivo_estado': self.motivo_estado,
            'fecha_alta': str(self.fecha_alta) 
        }
class HerramientasAlmacenInactivas (models.Model):
    id_herramientaInactiva = models.AutoField(primary_key=True)
    id_herramienta = models.ForeignKey(HerramientasAlmacen, on_delete=models.CASCADE)
    id_prestamo = models.ForeignKey(PrestamosAlmacen, on_delete=models.CASCADE, null=True)
    motivo_baja = models.CharField(max_length=6)
    explicacion_baja = models.TextField()
    cantidad_baja = models.CharField(max_length=15, null=True)
    fecha_baja = models.DateField()
    enInventario = models.CharField(max_length=3, null=True)

    def __str__(self):
        return self.id_herramienta
    
class InstrumentosAlmacen (models.Model):
    id_instrumento = models.AutoField(primary_key=True)
    codigo_instrumento = models.CharField(max_length=6)
    nombre_instrumento = models.CharField(max_length=100)
    descripcion_instrumento = models.TextField()
    marca = models.CharField(max_length=50)
    unidad = models.CharField(max_length=50)
    sku = models.CharField(max_length=30)
    imagen_instrumento = models.ImageField(upload_to="imagenesInstrumentos", null = True)
    estado_instrumento = models.CharField(max_length=2)
    motivo_estado = models.CharField(max_length=200)
    fecha_alta = models.DateField()

    def __str__(self):
        return self.id_instrumento
    
class RequisicionCompraAlmacen (models.Model):
    id_requi = models.AutoField(primary_key=True)
    id_empleado_solicitante = models.ForeignKey(Empleados, on_delete=models.CASCADE, null=True)
    id_herramienta = models.ForeignKey(HerramientasAlmacen, on_delete=models.CASCADE, null=True)
    id_prestamo = models.ForeignKey(PrestamosAlmacen, on_delete=models.CASCADE, null=True)
    cantidad_requerida = models.IntegerField()
    fehca_requi = models.DateField()
    fehca_requiEntrada = models.DateField(null=True)
    estatus_requi = models.CharField(max_length=30)

    def __str__(self):
        return self.id_requi
    
class altasAlmacen (models.Model):
    id_alta = models.AutoField(primary_key=True)
    id_herramienta = models.ForeignKey(HerramientasAlmacen, on_delete=models.CASCADE, null=True)
    cantidad_agregar = models.CharField(max_length=200, null=True)
    stockActualizado = models.CharField(max_length=200, null=True)
    codigoActualizado = models.CharField(max_length=200, null=True)
    fecha_alta = models.DateField(null=True)
    orden_compra_evidence_act = models.CharField(max_length=200, null=True)
    proveedor_alta = models.CharField(max_length=200, null=True)
    estatus_alta = models.CharField(max_length=30)
    requi = models.CharField(max_length=30, null = True)
    

    def __str__(self):
        return self.id_alta

class bajasAlmacen (models.Model):
    id_baja = models.AutoField(primary_key=True)
    id_herramienta = models.ForeignKey(HerramientasAlmacen, on_delete=models.CASCADE)
    motivo_baja = models.CharField(max_length=10)
    explicacion_baja = models.TextField()
    cantidad_baja = models.IntegerField()
    fecha_solicitud_baja = models.DateField()
    estatus_baja = models.CharField(max_length=30)
    token = models.CharField(max_length=30)
    fecha_baja = models.DateField()
    

    def __str__(self):
        return self.id_alta
    
class Vehiculos (models.Model):
    id_vehiculo = models.AutoField(primary_key=True)
    codigo_vehiculo = models.CharField(max_length=10)
    marca_vehiculo = models.CharField(max_length=20)
    modelo_vehiculo = models.CharField(max_length=40)
    numero_serie_vehiculo = models.CharField(max_length=50)
    color_vehiculo = models.CharField(max_length=20)
    año_vehiculo = models.CharField(max_length=4)
    placa_vehiculo = models.CharField(max_length=15)
    transmision_vehiculo = models.CharField(max_length=12)
    responsable_actual = models.ForeignKey(Empleados, on_delete=models.CASCADE) 
    ultimo_km_registrado = models.IntegerField()
    status_vehiculo = models.CharField(max_length=20)
    motivo_status_vehiculo = models.CharField(max_length=255, null=True)
    fecha_alta_vehiculo = models.DateField()
    imagen_frontal_vehiculo=models.ImageField(upload_to="vehiculos", null = True)
    imagen_trasera_vehiculo=models.ImageField(upload_to="vehiculos", null = True)
    imagen_lateralIzquierda_vehiculo=models.ImageField(upload_to="vehiculos", null = True)
    imagen_lateralDerecha_vehiculo=models.ImageField(upload_to="vehiculos", null = True)
    
    
    def __str__(self):
        return self.id_vehiculo
    
class documentacionVehiculos (models.Model):
    id_documentacion = models.AutoField(primary_key=True)
    vehiculo = models.ForeignKey(Vehiculos, on_delete=models.CASCADE)
    factura_vehiculo=models.FileField(upload_to='facturasVehiculos', null=True)
    tarjeta_circulacion=models.FileField(upload_to='tarjetasCirculacionVehiculos', null=True)
    pago_seguro=models.FileField(upload_to='segurosVehiculos', null=True)
    contrato_arrendamiento=models.FileField(upload_to='contratosArrendamientosVehiculos', null=True)
    
    
    def __str__(self):
        return self.id_documentacion
    
class tenenciasVehiculos (models.Model):
    id_tenencia = models.AutoField(primary_key=True)
    vehiculo = models.ForeignKey(Vehiculos, on_delete=models.CASCADE)
    agregado_por = models.ForeignKey(Empleados, on_delete=models.CASCADE)
    recibio_tenencia_vehiculo = models.FileField(upload_to='tenenciasvehiculo')
    ano_pagado = models.CharField(max_length=255, null = True)
    fecha_tenencia = models.DateField()
    placas_nuevas = models.CharField(max_length=2)
    referencia_pago_tenencia = models.CharField(max_length=20)
    monto_pagado_vehiculo = models.FloatField(max_length=30)
    
    
    def __str__(self):
        return self.id_tenencia

class serviciosVehiculos (models.Model):
    id_servicio = models.AutoField(primary_key=True)
    vehiculo = models.ForeignKey(Vehiculos, on_delete=models.CASCADE)
    fecha_servicios_vehiculo = models.DateField()
    tipo_servicio = models.CharField(max_length=20)
    servicios_realizados = models.CharField(max_length=255)
    kilometraje_preservicio = models.IntegerField()
    taller_servicio = models.CharField(max_length=50)
    monto_pagado = models.CharField(max_length=20)
    agregado_por = models.ForeignKey(Empleados, on_delete=models.CASCADE)
    factura_servicios = models.FileField(upload_to='facturasServiciosVehiculos', null=True)
    
    
    def __str__(self):
            return self.id_servicio

class alineacionyBalanceo (models.Model):
    id_alineacion_balanceo = models.AutoField(primary_key=True)
    id_vehiculo = models.ForeignKey(Vehiculos, on_delete=models.CASCADE)
    agregado_por = models.ForeignKey(Empleados, on_delete=models.CASCADE)
    alineacion_realizada = models.CharField(max_length=2)
    balanceo_realizado = models.CharField(max_length=2)
    cambio_llantas = models.CharField(max_length=255)
    numero_cambio_llantas = models.IntegerField(null = True)
    medida_llanta_nueva = models.CharField(max_length=255, null = True)
    marca_llanta_nueva= models.CharField(max_length=255, null = True)
    observaciones = models.CharField(max_length=255)
    monto_pagado = models.CharField(max_length=20, null = True)
    kilometraje_prealineacion= models.IntegerField()
    fecha_alineacion = models.DateField()
    factura_alineacion = models.FileField(upload_to='facturasalineacion', null=True)
    
    def __str__(self):
        return self.id_alineacion_balanceo


class reparacionVehiculo (models.Model):
    id_reparacion = models.AutoField(primary_key=True)
    id_vehiculo = models.ForeignKey(Vehiculos, on_delete=models.CASCADE)
    agregado_por = models.ForeignKey(Empleados, on_delete=models.CASCADE)
    fecha_reparacion = models.DateField()
    motivo_reparacion = models.CharField(max_length=25)
    descripcion_reparacion = models.CharField(max_length=255)
    taller_reparacion = models.CharField(max_length=100, null = True)
    costo_reparacion = models.FloatField()
    factura_reparacion = models.FileField(upload_to='facturaReparacion', null=True)
    
    def __str__(self):
        return self.id_reparacion

class cambiosVehiculares (models.Model):
    id_cambio_vehiculo = models.AutoField(primary_key=True)
    id_vehiculo = models.ForeignKey(Vehiculos, on_delete=models.CASCADE)
    fecha_cambio = models.DateField()
    encargado_anterior_y_nuevo = models.CharField(max_length=10, null = True)
    kilometraje_camibo = models.IntegerField()
    observaciones = models.CharField(max_length=255, null = True)
    daños = models.CharField(max_length=255, null = True)
    firma_encargado_anterior = models.ImageField(upload_to="firmaCambioVehiculoAnterior", null = True)
    firma_encargado_nuevo = models.ImageField(upload_to="firmaCambioVehiculoNuevo", null = True)
    agregado_por = models.ForeignKey(Empleados, on_delete=models.CASCADE, null = True)
    
    def __str__(self):
        return self.id_cambio_vehiculo

class asignacionesVehiculares (models.Model):
    id_asignacion_vehiculo = models.AutoField(primary_key=True)
    id_vehiculo = models.ForeignKey(Vehiculos, on_delete=models.CASCADE)
    fecha_asignacion = models.DateField()
    encargado_asignado_y_agregadopor = models.CharField(max_length=10, null = True)
    kilometraje_asignacion = models.IntegerField()
    observaciones = models.CharField(max_length=255, null = True)
    daños = models.CharField(max_length=255, null = True)
    firma_encargado_asignado = models.ImageField(upload_to="firmaAsignacionVehiculos", null = True)
    firma_empleado_agregadopor = models.ImageField(upload_to="firmaEmpleadoAgregadoPorAsignacion", null = True)
    
    
    def __str__(self):
        return self.id_asignacion_vehiculo


class EvaluacionesDesempeno(models.Model):
    id_evaluacion_desempeno = models.AutoField(primary_key=True)
    periodo_evaluacion = models.CharField(max_length=10)
    nombre_evaluacion = models.CharField(max_length=40)
    creado_por = models.ForeignKey(Empleados, on_delete=models.CASCADE, null = True)
    estatus_general = models.CharField(max_length=15)
    estatus_evaluadores = models.CharField(max_length=15, null = True)
    
    def __str__(self):
        return self.id_evaluacion_desempeno

class IndicadorEvaluador(models.Model):
    id_indicador_evaluador = models.AutoField(primary_key=True)
    fecha_creacion = models.DateField()
    evaluacion_desempeno = models.ForeignKey(EvaluacionesDesempeno, on_delete=models.CASCADE)
    empleado_evaluador = models.ForeignKey(Empleados, on_delete=models.CASCADE, null = True)
    estatus_general = models.CharField(max_length=20)
    empleados_evaluados = models.CharField(max_length=255)
    estatus_empleados_evaluador = models.CharField(max_length=255)
    agregado_por = models.CharField(max_length=3) #Llave foranea extra

    def __str__(self):
        return self.id_indicador_evaluador

class ResultadosDesempeno(models.Model):
    id_resultado_desempeno = models.AutoField(primary_key=True)
    indicador_evaluador = models.ForeignKey(IndicadorEvaluador, on_delete=models.CASCADE)
    id_empleado_evaluado = models.ForeignKey(Empleados, on_delete=models.CASCADE)
    resultado_preguntas = models.CharField(max_length=255)
    estatus_resultado_preguntas = models.CharField(max_length=255)
    estatus_resultado = models.CharField(max_length=50)
    fecha_terminacion = models.DateField(null = True)

    def __str__(self):
        return self.id_resultado_desempeno

class EmpleadosCara(models.Model):
    id_empleado_cara = models.AutoField(primary_key=True)
    id_empleado = models.ForeignKey(Empleados, on_delete= CASCADE)
    cara_registrada = models.CharField(max_length=2)
    cara_activa = models.CharField(max_length=2)

    def __str__(self):
        return self.id_empleado_cara

class Asistencia(models.Model):
    id_asistencia = models.AutoField(primary_key=True)
    id_empleado = models.ForeignKey(Empleados, on_delete= CASCADE, null = True)
    fecha = models.DateField(null = True)
    hora_entrada = models.CharField(max_length=8, null = True)
    retardo = models.CharField(max_length=2, null = True)
    hora_salida = models.CharField(max_length=8, null = True)
    a_tiempo = models.CharField(max_length=2, null = True)

    def __str__(self):
        return str(self.id_asistencia)
    
class IncidenciaLlegadaTardia(models.Model):
    id_incidencia_llegada_tardia = models.AutoField(primary_key=True)
    id_asitencia = models.ForeignKey(Asistencia, on_delete=CASCADE)
    fecha = models.DateField(null = True)
    hora_entrada = models.CharField(max_length=8, null = True)
    motivo = models.CharField(max_length=255)

    def __str__(self):
        return self.id_incidencia_llegada_tardia

class IncidenciaSalidaTemprana(models.Model):
    id_incidencia_salida_temprana = models.AutoField(primary_key=True)
    id_asitencia = models.ForeignKey(Asistencia, on_delete=CASCADE)
    fecha = models.DateField(null = True)
    hora_salida = models.CharField(max_length=8, null = True)
    motivo = models.CharField(max_length=255)

    def __str__(self):
        return self.id_incidencia_salida_temprana
    
class IncidenciaSalidaFuera(models.Model):
    id_incidencia_salida_fuera = models.AutoField(primary_key=True)
    id_asitencia = models.ForeignKey(Asistencia, on_delete=CASCADE)
    fecha = models.DateField(null = True)
    hora_salida = models.CharField(max_length=8, null = True)
    motivo = models.CharField(max_length=255)

    def __str__(self):
        return self.id_incidencia_salida_fuera
    
class PermisosAsistencia(models.Model):
    id_permiso_asistencia = models.AutoField(primary_key=True)
    id_empleado = models.ForeignKey(Empleados, on_delete= CASCADE, null = True)
    fecha = models.DateField(null = True)
    motivo = models.CharField(max_length=255)

    def __str__(self):
        return self.id_permiso_asistencia
    
class FaltasAsistencia(models.Model):
    id_falta_asistencia = models.AutoField(primary_key=True)
    id_empleado = models.ForeignKey(Empleados, on_delete= CASCADE, null = True)
    fecha = models.DateField(null = True)
    observaciones = models.CharField(max_length=255)

    def __str__(self):
        return self.id_falta_asistencia
    
class HorasExtras(models.Model):
    id_horas_extras = models.AutoField(primary_key=True)
    id_asitencia = models.ForeignKey(Asistencia, on_delete=CASCADE)
    numero_horas_extras = models.IntegerField()

    def __str__(self):
        return self.id_horas_extras
    

class Proyectos(models.Model):
    id_proyecto = models.AutoField(primary_key=True)
    numero_proyecto_interno = models.CharField(max_length=255)
    nombre_proyecto = models.CharField(max_length=255)
    cliente = models.CharField(max_length=255)
    lugar = models.CharField(max_length=255)

    def __str__(self):
        return self.id_proyecto
    
    
class AsistenciaProyectoForaneo(models.Model):
    id_asistencia_proyecto_foraneo = models.AutoField(primary_key=True)
    id_empleado = models.ForeignKey(Empleados, on_delete= CASCADE, null = True)
    personal_externo = models.CharField(max_length=255, null=True)
    fecha_entrada = models.DateField(null = True)
    hora_entrada = models.CharField(max_length=8, null = True)
    fecha_salida = models.DateField(null = True)
    hora_salida = models.CharField(max_length=8, null = True)
    proyecto_interno = models.ForeignKey(Proyectos, on_delete= CASCADE, null = True)
    motivo = models.CharField(max_length=255, null = True)
    actividad_realizada = models.CharField(max_length=255, null = True)
    actividades_realizadas = models.CharField(max_length=255, null = True)

    def __str__(self):
        return str(self.id_asistencia_proyecto_foraneo)
    
class HorasExtrasForaneas(models.Model):
    id_horas_extras_foraneas = models.AutoField(primary_key=True)
    id_asitencia_foraneas = models.ForeignKey(AsistenciaProyectoForaneo, on_delete=CASCADE)
    numero_horas_extras = models.IntegerField()

    def __str__(self):
        return self.id_horas_extras_foraneas

class RelacionNFCEmpleado(models.Model):
    id_relacion = models.AutoField(primary_key=True)
    id_empleado = models.ForeignKey(Empleados, on_delete=CASCADE)
    uid_nfc = models.CharField(max_length=255)

    def __str__(self):
        return self.id_relacion
    

    

    

