#encoding:utf-8
import os
import uuid
from django.core.files.storage import FileSystemStorage

def get_file_path(instance, filename):
	"""
	Método que especifica la codificación para el nombre del archivo que se almacenará en el servidor.
	"""

	"""Se separa la cadena que representa el archivo."""
	ext = filename.split('.')[-1]
	"""
	puedo hacer una combinación para el nombre del archivo como quiera especificarlo... instance.tipo_obj
	Se ha agregado una codificación extra antes de la extensión con el fin de identificar el objeto subido por su nombre
	esta codificación extra está relacionada con el primary key del speclom asociado a la instancia del objeto que se sube.
	"""
	filename="%s_%s.%s" % (uuid.uuid4(), instance.espec_lom.pk, ext) #Se une la nueva codificación del nombre con la extensión.
	return os.path.join('objetos', filename) #Se devuelve el nuevo nombre como un ruta relativa.

def get_file_storage():
	"""
	método que permite especificar el lugar donde serán almacenados los archivos.

	...puede faltar un parámetro denominado base_url que literalmente permite:
	URL that serves the files stored at this location. If omitted, it will default to the value of your MEDIA_URL setting.
	"""
	fs = FileSystemStorage(location='/')
	return fs