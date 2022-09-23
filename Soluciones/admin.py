from django.contrib import admin
from Soluciones.models import mensajes,salas,UsuarioConcurso,concursos,correoValidacion, libros, soluciones, solucionadores, tematicas,paquetes,UsuarioPaq, QRPago,perfil,ProblemaPaq, comentarios
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
admin.site.register(concursos)
admin.site.register(UsuarioConcurso)
admin.site.register(salas)
admin.site.register(mensajes)
# Register your models here.
