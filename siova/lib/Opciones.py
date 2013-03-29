#encoding:utf-8
"""
Funciones para el manejo de las opciones
"""

def get_tipo_obj():
	OVA = 'ova'
	RECURSO = 'rda'
	TIPO_OBJ_CHOICES = (
		(OVA, 'Objeto Virtual de Aprendizaje'),
		(RECURSO, 'Recurso Digital'),
	)
	return TIPO_OBJ_CHOICES

def get_nivel_agregacion():
    N1 = 'N1'
    N2 = 'N2'
    N3 = 'N3'
    N4 = 'N4'
    NIVEL_AGREGACION_CHOICES = (
        (N1, 'Recursos Digitales'),
        (N2, 'Colección de Recursos'),
        (N3, 'Colección de Lecciones'),
        (N4, 'Colección de Cursos'),
    )
    return NIVEL_AGREGACION_CHOICES


def get_tipo_interactividad():
	ACTIVO = 'act'
	EXPOSITIVO = 'exp'
	TIPO_INTERACTIVIDAD_CHOICES = (
		(ACTIVO, 'Activo'),
		(EXPOSITIVO, 'Expositivo'),
	)
	return TIPO_INTERACTIVIDAD_CHOICES

def get_contexto():
	C1 = 'EPre'
	C2 = 'EBas'
	C3 = 'EMed'
	C4 = 'ESup'
	C5 = 'ETra'
	CONTEXTO_CHOICES = ((C1, 'Educación Preescolar'),
		(C2, 'Educación Básica'),
		(C3, 'Educación Media'),
		(C4, 'Educación Superior'),
		(C5, 'Educación para el Trabajo'),)
	return CONTEXTO_CHOICES

def get_nivel_interactividad():
	MUYBAJO = 'mba'
	BAJO = 'baj'
	MEDIO = 'med'
	ALTO = 'alt'
	MUYALTO = 'mal'
	NIVEL_INTERACTIVIDAD_CHOICES = (
		(MUYBAJO, 'Muy Bajo'),
		(BAJO, 'Bajo'),
		(MEDIO, 'Medio'),
		(ALTO, 'Alto'),
		(MUYALTO, 'Muy Alto'),
	)
	return NIVEL_INTERACTIVIDAD_CHOICES

def get_roles():
	REST = 'rest'
	RDOC = 'rdoc'
	RADM = 'radm'
	RVIS = 'rvis'
	RREV = 'rrev'
	ROLE_CHOICES = (
		(REST, 'Estudiante'),
		(RDOC, 'Docente'),
		(RADM, 'Administrador'),
		(RVIS, 'Visitante'),
		(RREV, 'Revisor'),
	)
	return ROLE_CHOICES