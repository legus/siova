#encoding:utf-8
from decimal import Decimal
"""
Funciones para el manejo de las opciones
"""

def get_idiomas():
	ESP = 'sp'
	ENG = 'en'
	FRA = 'fr'
	ITA = 'it'
	JAP = 'ja'
	POR = 'pt'
	RUS = 'ru'
	SUI = 'sv'
	ALE = 'de'
	CHI = 'zh'

	IDIOMA_CHOICES = (
		(ESP, 'Español'),
		(ENG, 'Inglés'),
		(FRA, 'Francés'),
		(ITA, 'Italiano'),
		(JAP, 'Japonés'),
		(POR, 'Portugués'),
		(RUS, 'Ruso'),
		(SUI, 'Suizo'),
		(ALE, 'Alemán'),
		(CHI, 'Chino'),
	)
	return IDIOMA_CHOICES

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

def get_tipo_recurso():
	LEC = 'plain/text'
	WEB = 'application/xhtml'
	PDF = 'application/pdf'
	ZIP = 'application/zip'
	IMG = 'image/jpeg'
	AUD = 'audio/mpeg'
	MPG = 'video/mpeg'
	MP4 = 'video/mp4'
	WMV = 'video/x-ms-wmv'
	QUT = 'video/quicktime'
	FLV = 'video/x-flv'
	ANI = 'application/x-shockwave-flash'
	TIPO_RECURSO_CHOICES = (
		(LEC, 'Lectura'),
		(WEB, 'Página Web'),
		(PDF, 'Lectura/PDF'),
		(ZIP, 'Empaquetado'),
		(IMG, 'Imagen/Gráfico/Illustración'),
		(AUD, 'Audio'),
		(MPG, 'Video/mpg'),
		(MP4, 'Video/mp4'),
		(WMV, 'Video/wmv'),
		(QUT, 'Video/mov'),
		(FLV, 'Video/flv'),
		(ANI, 'Animación'),
	)
	return TIPO_RECURSO_CHOICES

def get_roles():
	REST = 'rest'
	RDOC = 'rdoc'
	RADM = 'radm'
	RCAT = 'rcat'
	RREV = 'rrev'
	ROLE_CHOICES = (
		(REST, 'Estudiante'),
		(RDOC, 'Docente'),
		(RADM, 'Administrador'),
		(RCAT, 'Catalogador'),
		(RREV, 'Revisor'),
	)
	return ROLE_CHOICES

def get_modalidades():
	MPRE = 'mpr'
	MSEM = 'mse'
	MDIS = 'mdi'
	MVIR = 'mvi'
	MODALIDADES_CHOICES = (
		(MPRE, 'Presencial'),
		(MSEM, 'Semi presencial'),
		(MDIS, 'A Distancia'),
		(MVIR, 'Virtual'),
	)
	return MODALIDADES_CHOICES

def get_sedes():
	SSAN = 'ssa'
	SCHI = 'sch'
	SYOP = 'syo'
	SSER = 'sse'
	SEDES_CHOICES = (
		(SSAN, 'San Gil'),
		(SCHI, 'Chiquinquirá'),
		(SYOP, 'Yopal'),
		(SSER, 'Seres'),
	)
	return SEDES_CHOICES

def get_grado():
	GPRI = 'gpr'
	GSEG = 'gse'
	GTER = 'gte'
	GCUA = 'gcu'
	GQUI = 'gqu'
	GRADOS_CHOICES = (
		(GPRI, 'Primero'),
		(GSEG, 'Segundo'),
		(GTER, 'Tercero'),
		(GCUA, 'Cuarto'),
		(GQUI, 'Quinto'),
	)
	return GRADOS_CHOICES

def get_fase():
	F1 = 'f1'
	F2 = 'f2'
	F3 = 'f3'
	FASES_CHOICES = (
		(F1, 'Fase 1'),
		(F2, 'Fase 2'),
		(F3, 'Fase 3'),
	)
	return FASES_CHOICES

def get_tipo_p():
	ACONT = 'acon'
	AENF = 'aenf'
	AEVA = 'aeva'
	AINT = 'aint'
	APOS = 'apos'
	TIPO_P_CHOICES = (
		(ACONT, 'Contenido en Relación con los estándares'),
		(AENF, 'Enfoque Cognitivo'),
		(AEVA, 'Evaluación'),
		(AINT, 'Intercomunicación Estudiante-Material'),
		(APOS, 'Posibilidades metodológicas'),
	)
	return TIPO_P_CHOICES

def get_valoracion():
	VNUL = '0.0'
	VTOT = '10.0'
	VMED = '7.0'
	VESC = '5.0'
	VNOC = '2.5'
	VALORACION_CHOICES = (
		(VNUL, 'Sin Calificar'),
		(VTOT, 'Totalmente'),
		(VMED, 'Medianamente'),
		(VESC, 'Escasamente'),
		(VNOC, 'No Cumple'),
	)
	return VALORACION_CHOICES

def get_valoracion_decimal():
	VNUL = Decimal('0.0')
	VTOT = Decimal('10.0')
	VMED = Decimal('7.0')
	VESC = Decimal('5.0')
	VNOC = Decimal('2.5')
	VALORACION_CHOICES = (
		(VNUL, 'Sin Calificar'),
		(VTOT, 'Totalmente'),
		(VMED, 'Medianamente'),
		(VESC, 'Escasamente'),
		(VNOC, 'No Cumple'),
	)
	return VALORACION_CHOICES

def get_calif():
	NUL = 's'
	APR = 'a'
	REP = 'r'
	CALIFICACION_CHOICES = (
		(NUL, 'Sin calificar'),
		(APR, 'Clasificado'),
		(REP, 'No Clasificado'),
	)
	return CALIFICACION_CHOICES

def get_umbral_calificacion():
	UMBRAL=Decimal('7.0')
	return UMBRAL