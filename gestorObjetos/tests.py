#encoding:utf-8
from django.test import TestCase
from gestorObjetos.models import PalabraClave, Repositorio, Autor
from django.contrib.auth.models import Group, User
from django.test.client import Client

class loggingTest(TestCase):
	def setUp(self):
		self.client = Client()

	def test_logging(self):
		response = self.client.post('/ingresar/', {'username': 'admin', 'password': 'siova_virtual'})
		self.assertEqual(response.status_code,200)

	def test_logging_Autorizado(self):
		self.client.post('/ingresar/', {'username': 'admin', 'password': 'siova_virtual'})
		response = self.client.get('/privado/')
		self.assertEqual(response.status_code,200)
		
class PalabraClaveTest(TestCase):
    def setUp(self):
        """
        Prueba para la creación de palabras claves
        """
        self.p1 =  PalabraClave(palabra_clave='gato')

    def test_palabra_clave_exist(self):
    	self.assertTrue(self.p1)

class RepositorioTest(TestCase):
    def setUp(self):
        """
        Prueba para la creación de Repositorios
        """
        self.u1 = User('john', 'lennon@thebeatles.com', 'johnpassword')
        self.gr1 = Group('estudiantes')
        self.rep =  Repositorio(nombre='Licenciatura', publico=True)

    def test_repositorio_exist(self):
    	self.assertTrue(self.rep)

class AutorTest(TestCase):
    """
    Prueba para la creación de autores para el objeto.
    """
    def setUp(self):
        self.autor1 = Autor(nombres='Leidy', apellidos='Reyes', rol='Diseñador')

    def test_autor_exist(self):
        self.assertTrue(self.autor1)