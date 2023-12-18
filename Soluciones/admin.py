from django.contrib import admin
from Soluciones.models import temaLibro,PagoEnZona,correoValidacion, libros, soluciones, solucionadores, tematicas,paquetes,UsuarioPaq, QRPago,perfil,ProblemaPaq, comentarios
admin.site.register(libros)
admin.site.register(soluciones)
admin.site.register(solucionadores)
admin.site.register(tematicas)
admin.site.register(paquetes)
admin.site.register(UsuarioPaq)
admin.site.register(QRPago)
admin.site.register(perfil)
admin.site.register(ProblemaPaq)
admin.site.register(comentarios)
admin.site.register(correoValidacion)
admin.site.register(temaLibro)
admin.site.register(PagoEnZona)

# Register your models here.
