from django.contrib import admin
from .models import (TiposUsuarios,
                     Plataformas,
                     Empresas,
                     EmpresasUsuarios,)

# Register your models here.

admin.site.register(TiposUsuarios)
admin.site.register(Plataformas)
admin.site.register(Empresas)
admin.site.register(EmpresasUsuarios)
