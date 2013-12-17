#encoding:utf-8	
from django.db import models
import siova.lib.Opciones as opc

class Grado(models.Model):
	"""
    Modelo que representa los grados escolares relacionados en los estándares de competencias
    """
	nominacion = models.CharField(help_text="Grado de escolaridad", verbose_name = 'Grado escolar', unique=True, max_length=3, choices=opc.get_grado(),default=opc.get_grado()[0][0])
	descripcion = models.TextField(help_text="Descripción del grado escolar", verbose_name='Descripción', blank=True)
	def __unicode__(self):
		return self.get_nominacion_display()

class Facultad(models.Model):
	"""
    Modelo que representa las Facultades de la institución a la que pertenecen los proyectos
    """
	nombre = models.CharField(help_text="Nombre de la facultad", verbose_name = 'Facultad', max_length=80, unique=True)
	class Meta:
		verbose_name_plural= "Facultades"
	def __unicode__(self):
		return self.nombre

class Programa(models.Model):
	"""
    Modelo que representa los programas académicos de la institución
    """
	nombre = models.CharField(help_text="Nombre del programa", verbose_name = 'programa', max_length=80, unique=True)
	modalidad = models.CharField(help_text="Modalidad del programa", verbose_name = 'Modalidad', max_length=3, choices=opc.get_modalidades(),default=opc.get_modalidades()[0][0])
	sede = models.CharField(help_text="Sede del programa", verbose_name = 'Sede', max_length=3, choices=opc.get_sedes(), default=opc.get_sedes()[0][0])
	facultad = models.ForeignKey(Facultad, help_text="Nombre de la facultad", verbose_name= 'Facultad', blank=False)
	def __unicode__(self):
		return self.nombre

class Factor_competencias(models.Model):
	"""
    Este Modelo representa los factores de los estándares de comptencias del Ministerio de educación Nacional
    """
	factor = models.CharField(help_text="Factor estándar básico de competencias", verbose_name = 'Factor competencias', max_length=80, unique=True)
	ruta_categoria = models.ForeignKey('gestorObjetos.RutaCategoria', blank=False, null=False, help_text="Área fundamental básica", verbose_name= 'Área básica')
	class Meta:
		verbose_name = "Factor competencias"
		verbose_name_plural= "Factores competencias"
	def __unicode__(self):
		return self.factor

class Enunciado(models.Model):
	"""
    Modelo que representa los enunciados que pueden o no pertenecer a cada :model:'gestorProyectos:Factor_competencias'
    """
	enunciado = models.TextField(help_text="Enunciado identificador para el factor de competencias", verbose_name = 'Enunciado')
	factor = models.ForeignKey(Factor_competencias, help_text="Factor de Competencias", verbose_name= 'Factor')
	class Meta:
		verbose_name = "Enunciado Identificador"
		verbose_name_plural= "Enunciados Identificadores"
		order_with_respect_to = 'factor'
	def __unicode__(self):
		return self.enunciado

class Indicador(models.Model):
	"""
    Modelo que representa los subprocesos de cada :model:'gestorProyectos:Enunciado' y/o :model:'gestorProyectos:Factor_competencias'
    """
	indicador = models.TextField(help_text="Indicador para el factor de competencias", verbose_name = 'indicador')
	factor = models.ForeignKey(Factor_competencias, blank=True, null=True, help_text="Factor de Competencias", verbose_name= 'Factor')
	enunciado = models.ForeignKey(Enunciado, blank=True, null=True, help_text="Enunciado del factor", verbose_name= 'Enunciado')
	grados = models.ManyToManyField(Grado, help_text="Grado de Escolaridad", verbose_name= 'Grado Escolar')
	class Meta:
		verbose_name = "Indicador de Competencia"
		verbose_name_plural= "Indicadores de Competencia"
		order_with_respect_to = 'factor'
	def __unicode__(self):
		return self.indicador

class Parametro(models.Model):
	"""
	Modelo que representa los parámetros de validación pedagógica
	"""
	nombre = models.CharField(help_text="Nombre del parámetro de validación", verbose_name="Parámetro de Validación", max_length=80)
	descripcion = models.TextField(help_text="Descripción del parámetro de validación", verbose_name = 'Descripción')
	tipo = models.CharField(help_text="Tipo parámetro de validación", verbose_name="Asociados a", max_length=4, choices=opc.get_tipo_p(), default=opc.get_tipo_p()[0][0])
	ponderacion = models.DecimalField(help_text="Valor porcentual de ponderación del parámetro", verbose_name="Ponderación Porcentual", max_digits=4, decimal_places=2)
	class Meta:
		verbose_name = "Parámetro"
		verbose_name_plural= "Parámetros"
	def __unicode__(self):
		return self.nombre

class OperacionMental(models.Model):
	"""
	Modelo que representa las operaciones mentales básicas las cuales pueden ser asociadas a los proyectos académicos
	"""
	operacion = models.CharField(help_text="Operación mental básica", verbose_name = 'Operación Mental', max_length=80, unique=True)
	descripcion = models.TextField(help_text="Descripción de la Operación mental básica", verbose_name = 'Descripción')
	class Meta:
		verbose_name = "Operación Mental"
		verbose_name_plural= "Operaciones Mentales"
	def __unicode__(self):
		return self.operacion

class Proyecto(models.Model):
	"""
	Modelo que representa los proyectos académicos
	"""
	"""Se incluye el campo título pero se debe llenar con la misma información el campo título de la especificación lom del objeto asociado con este proyecto"""
	titulo = models.CharField(max_length=200, unique=True, null=False)
	fecha = models.DateTimeField(help_text='Fecha en que el Proyecto es aprobado', verbose_name="Fecha de aprobación")
	fase = models.CharField(help_text="Movimiento de fase automático", max_length=2, choices=opc.get_fase(), default=opc.get_fase()[0][0])
	programa = models.ForeignKey(Programa, help_text='Programa académico al que pertenece el proyecto', verbose_name='Programa')
	indicadores = models.ManyToManyField(Indicador, blank=True, null=True, help_text="Relacione el/los Indicador (es) de comptencia", verbose_name= 'Indicador de Competencia')
	parametros = models.ManyToManyField(Parametro, through="Validacion", blank=True, null=True)
	operaciones = models.ManyToManyField(OperacionMental, blank=True, null=True, help_text="Relacione la/las Operación (es) Mental (es) básica (s) para el proyecto", verbose_name= 'Operaciones Mentales')
	calificacion = models.CharField(help_text="Calificación final del proyecto", max_length=1, choices=opc.get_calif(), default=opc.get_calif()[0][0])
	nota = models.DecimalField(help_text="Nota numérica de la validación del proyecto", verbose_name="Nota Porcentual", max_digits=4, decimal_places=2)
	def __unicode__(self):
		return self.titulo


class Validacion(models.Model):
	"""
	Modelo que rompe la relación muchos a muchos entre :model:'gestorProyectos:Proyecto' y :model:'gestorProyectos:Parametro' para representar la validación pedagógica de los proyectos
	"""
	proyecto = models.ForeignKey(Proyecto)
	parametro = models.ForeignKey(Parametro)
	fecha = models.DateField(auto_now_add=True)
	valoracion = models.CharField(verbose_name = 'Valoración', max_length=4, choices=opc.get_valoracion(), default=opc.get_valoracion()[0][0])
	#valoracion = models.DecimalField(verbose_name = 'Valoración', max_digits=4, decimal_places=2, choices=opc.get_valoracion(), default=opc.get_valoracion()[0][0])
	observaciones =  models.TextField(blank=True, help_text="Opcional", verbose_name = 'Observaciones')
	class Meta:
		verbose_name = "Validación"
		verbose_name_plural= "Validaciones"
	def __unicode__(self):
		return self.parametro.nombre
