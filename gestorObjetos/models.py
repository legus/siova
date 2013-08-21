#encoding:utf-8
import os
import uuid
from django.db import models
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib import admin
import siova.lib.Archivos as mod_archivo
import siova.lib.Opciones as opc

class PalabraClave(models.Model):
    """
    Modelo que representa las palabras claves que se pueden asocia a cada :model:'gestorObjetos.EspecificacionLOM'
    """
    palabra_clave=models.CharField(help_text='Palabra que describe el Objeto', verbose_name="Palabra Clave", max_length=50, unique=True)
    class Meta:
        verbose_name = "Palabra Clave"
        verbose_name_plural = "Palabras Clave"
    def __unicode__(self):
        return self.palabra_clave

class Repositorio(models.Model):

    """
    Modelo que representa el repositorio, lugar donde se almacenan los :model:'gestorObjetos.Objeto'
    """
    """Campo que identifica al repositorio con un nombre"""
    nombre = models.CharField(help_text='Nombre que identifica al repositorio', verbose_name='Nombre del Repositorio', max_length=200,null=False,unique=True)
    """campo que permite determinar si el repositorio es visible para todos los usuarios o solo para aquellos autorizados"""
    publico = models.BooleanField(help_text='Marca para habilitar el repositorio al público', verbose_name='Público', default=True)
    """Relación hacia el :model:'Group' que puede observar los objetos"""
    grupos = models.ManyToManyField(Group,null=True,blank=True)

    def __unicode__(self):
        return self.nombre

class Autor (models.Model):
    """
    Modelo que permite representar a los autores del :model:'gestorObjetos.Objeto'
    """

    """Nombres del Autor del Objeto."""
    nombres = models.CharField(help_text="Nombres del Autor del Objeto.", verbose_name='Nombres', max_length=100, null=False)
    """Apellidos del Autor del Objeto."""
    apellidos = models.CharField(help_text="Apellidos del Autor del Objeto.", verbose_name='Apellidos', max_length=100, null=False)
    """Campo para el rol que representa el usuario en el objeto."""
    rol = models.CharField(help_text="Papel que juega en la creación del Objeto", verbose_name='Rol', max_length=100, default="Autor")
    class Meta:
        verbose_name_plural = "Autores"
    def __unicode__(self):
        return self.nombres+' '+self.apellidos

class AutorAdmin(admin.ModelAdmin):
    """
    Esta clase permite desplegar un conjunto de campos concatenados de un modelo, con el fin de mostrarlos así en el backend del administrador.
    """
    list_display = ('nombres', 'apellidos')
    list_display_links = ('nombres', 'apellidos')


class RutaCategoria(models.Model):
    """Modelo para la creación de las rutas taxonómica de categorías tomada de las
        áreas de conocimiento del ministerio de Educación nacional. cada categoría puede
        a su vez contener otras categorías"""

    """Nombre para la ruta de Categoría"""
    nombre_ruta=models.CharField(help_text="Nombre de la Categoría.", verbose_name='Categoría', max_length=150, null=False)
    """Relación a la :model:'gestorObjetos.RutaCategoria' para determinar si tiene una categoría padre"""
    cat_padre=models.ForeignKey('self', null=True, blank=True, related_name='+',verbose_name='Categoría Padre', help_text="Categoría que la contiene")
    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
    def __unicode__(self):
        return self.nombre_ruta
        #if self.cat_padre:
            #return ' | '.join([self.cat_padre.nombre_ruta,  self.nombre_ruta, ])
        #else:
            #return self.nombre_ruta
        
class EspecificacionLOM(models.Model):
    """
    Modelo que representa la especificación asociada a cada :model:'gestorObjetos.Objeto' en el sistema.
    """

    """Nombre para el objeto virtual de aprendizaje o recurso digital."""
    lc1_titulo=models.CharField(help_text='Nombre para el objeto', verbose_name='Título', max_length=200, unique=True, null=False)
    """Lenguaje primario o lenguajes predominante en el objeto y que se utiliza para comunicarse con el usuario."""
    lc1_idioma=models.CharField(help_text='Lenguaje predominante en el objeto', verbose_name='Idioma', max_length=2,choices=opc.get_idiomas(),default=opc.get_idiomas()[0][0])
    """Descripción Textual del contenido del objeto."""
    lc1_descripcion=models.TextField(help_text='Descripción Textual del contenido del objeto', verbose_name="Descripción", null=False)

    """Lugar, tiempo, cultura, geografía o región en la cual el objeto es aplicado."""
    lc1_cobertura=models.TextField(help_text='Lugar, tiempo, cultura, geografía o región en la cual el objeto es aplicado',
                                    verbose_name="Cobertura", null=True, blank=True)
    """
    Granularidad Funcional del objeto. N1: recursos digitales, N2:colección de recursos. ejp: lección,
    N3: Colección de lecciones. ejp: cursos, N4: ejp:conjunto de cursos.
    """
    lc1_nivel_agregacion=models.CharField(help_text='Granularidad Funcional del objeto.',
                                            verbose_name='Nivel de Agregación', max_length=2,choices=opc.get_nivel_agregacion(),default=opc.get_nivel_agregacion()[0][0])
    """La edición del objeto."""
    lc2_version=models.CharField(help_text='La edición del objeto', verbose_name="Versión", max_length=50, default="1.0")

    """Fecha en que el objeto es creado."""
    lc2_fecha=models.DateTimeField(help_text='Fecha en que el objeto es publicado', verbose_name="Fecha de Publicación", auto_now_add=True)
    
    """Tipo de Datos técnico, tipo MIME Types. http://www.iana.org/assignments/media-types/index.html.
    lc3_formato=models.CharField(help_text='Tipo de datos. Ejp: video/mpeg, text/html, image/jpg', verbose_name="Formato",
                                max_length=100, null=True, default="text/plain")
    
    Tamaño del objeto en megabytes.
    lc3_tamano=models.DecimalField(help_text='Tamaño del objeto en megabytes.',
                                    verbose_name="Tamaño", max_digits=50, decimal_places=2, null=False, default="10", editable=False)
    URL que se usa para acceder al Objeto
    lc3_ubicacion=models.URLField(max_length=300, null=True, default="url", editable=False)"""
    
    """Capacidades técnicas requeridas para usar este objeto."""
    lc3_requerimientos=models.TextField(help_text='Capacidades técnicas requeridas para usar este objeto',
                                    verbose_name="Requerimientos", null=True, blank=True)
    """Descripción de cómo instalar este objeto."""
    lc3_instrucciones=models.TextField(help_text='Descripción de cómo usar este objeto.', verbose_name="Instrucciones", null=True, blank=True)
    
    """Modo predominante del aprendizaje que aplica este objeto."""
    lc4_tipo_inter=models.CharField(help_text="Modo predominante del aprendizaje que aplica este objeto",
                                    verbose_name="Tipo de Interactividad", max_length=3,choices=opc.get_tipo_interactividad(),default=opc.get_tipo_interactividad()[1][0])
    """Tipo de recurso de aprendizaje."""
    lc4_tipo_rec=models.CharField(help_text="Tipo de recurso de aprendizaje.",
                                    verbose_name="Tipo de Recurso de Aprendizaje", max_length=50, null=True,choices=opc.get_tipo_recurso(),default=opc.get_tipo_recurso()[0][0])
    """Grado de interactividad que predomina en el objeto."""
    lc4_nivel_inter=models.CharField(help_text="Grado de interactividad que predomina en el objeto.",
                                    verbose_name="Nivel de Interactividad", max_length=3,choices=opc.get_nivel_interactividad(),default=opc.get_nivel_interactividad()[0][0])
    """Descripción de los Usarios para los cuales este objeto fue diseñado."""
    lc4_poblacion=models.TextField(help_text='Descripción de los Usuarios para los cuales este objeto fue diseñado.',
                                    verbose_name="Población", null=True, blank=True)
    """Principal ambiente en el cual este objeto es utilizado."""
    lc4_contexto=models.CharField(help_text="Principal ambiente en el cual este objeto es utilizado.",
                                    verbose_name="Contexto", max_length=4,choices=opc.get_contexto(),default=opc.get_contexto()[0][0], null=True, blank=True)
    """Comentarios sobre las condiciones de uso de este objeto."""
    lc5_derechos=models.TextField(help_text='Condiciones de uso de este objeto. Ejp: copyright, Creative Commons',
                                    verbose_name="Derechos de Uso", null=False)
    """Se proveen comentarios sobre el uso educativo del objeto."""
    lc6_uso_educativo=models.TextField(help_text='Anotación sobre el uso educativo del objeto',
                                    verbose_name="Uso Educativo", null=True, blank=True)
    class Meta:
        verbose_name = "Metadato"
        verbose_name_plural = "Metadatos"

    def __unicode__(self):
        return self.lc1_titulo


class Objeto(models.Model):
    """
    Modelo que representa al objeto, ya sea un objeto virtual de aprendizaje o un recurso digital.
    """

    """campo que permite determinar si el objeto es visible en el :model:'gestorObjetos.Repositorio' asociado"""
    publicado = models.BooleanField(help_text='Marca para publicar en repositorio', verbose_name='Publicado', default=False)
    """Atributo que permite identificar si es un objeto virtual de aprendizaje o recurso digital"""
    tipo_obj = models.CharField(help_text='Tipo de Objeto', verbose_name='Tipo de Objeto', max_length=3,choices=opc.get_tipo_obj(),default=opc.get_tipo_obj()[1][0])

    """Atributo asociado a la clase :model:'django.core.files' que apunta a la ubicación física del objeto en el sistema de archivos."""
    archivo = models.FileField(help_text='Archivo a Subir', verbose_name='Archivo', upload_to=mod_archivo.get_file_path, storage=mod_archivo.get_file_storage())

    """Atributo que relaciona uno a uno el objeto con su respectiva especificación LOM"""
    espec_lom = models.OneToOneField(EspecificacionLOM, help_text='Metadatos para el objeto', verbose_name='Metadato')

    """Atributo que relaciona al objeto con un :model:'gestorObjetos.Repositorio'."""
    repositorio = models.ForeignKey(Repositorio,help_text='Repositorio donde se aloja el objeto')

    """Campo que representa la :model:'gestorObjetos.Categoria' o Ruta Taxonómica del :model:'gestorObjetos.Objeto'"""
    ruta_categoria=models.ForeignKey(RutaCategoria,help_text='Categoría o área de conocimiento')

    """Relación a los :model:'gestorObjetos.Autor' para definir los autores asociados al objeto"""
    autores=models.ManyToManyField(Autor,help_text='Personas autoras del objeto')

    """Relación a las :model:'gestorObjetos.PalabraClave' para definir etiquetas asociadas al objeto"""
    palabras_claves=models.ManyToManyField(PalabraClave,help_text='Palabras asociadas al objeto.')

    """Relación al :model:'User' para determinar el creador del objeto"""
    creador = models.ForeignKey(User, blank=True, null=True, default=1)

    def __unicode__(self):
        return self.espec_lom.lc1_titulo


class UserProfile(models.Model):
    """
    Clase UserProfile que premitirá extender las características del :model:'User'
    """

    """Adición de método para la relación del Usuario con un Rol que lo identifica en el sistema"""
    rol = models.CharField(help_text='Rol que identifica la participación del :model:"User" en el sistema',
                            verbose_name='Rol de Usuario', max_length=4, choices=opc.get_roles(), default=opc.get_roles()[0][0])
    """Adición de método para la relación con la :model:'gestorObjetos.RutaCategoria
    ruta_categoria = models.ForeignKey(RutaCategoria, null=True, blank=True)"""
    """relación directa al usuario"""
    user = models.ForeignKey(User, unique=True)

    class Meta:
        verbose_name = "Perfil de Usuario"
        verbose_name_plural = "Perfiles de Usuario"

    def __unicode__(self):
        return self.user.first_name

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
        

"""Adición de método para la relación del Usuario con un Rol que lo identifica en el sistema
User.add_to_class('rol', models.CharField(help_text='Rol que identifica la participación del :model:"User" en el sistema',
                                    verbose_name='Rol de Usuario', max_length=4, choices=opc.get_roles(), default=opc.get_roles()[0][0]))
Adición de método para la relación con la :model:'siova.RutaCategoria
User.add_to_class('ruta_categoria', models.ForeignKey(RutaCategoria, null=True, blank=True))"""