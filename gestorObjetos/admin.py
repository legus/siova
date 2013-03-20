from gestorObjetos.models import Objeto, Espec_lom, Repositorio, PalabraClave, Autor, RutaCategoria, UserProfile
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
 
admin.site.unregister(User)
 
class UserProfileInline(admin.StackedInline):
	model = UserProfile
 
class UserProfileAdmin(UserAdmin):
	inlines = [UserProfileInline]
 
admin.site.register(User, UserProfileAdmin)

admin.site.register(Objeto)
admin.site.register(Espec_lom)
admin.site.register(Repositorio)
admin.site.register(PalabraClave)
admin.site.register(Autor)
admin.site.register(RutaCategoria)