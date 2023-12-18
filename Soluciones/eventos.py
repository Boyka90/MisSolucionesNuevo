
from Soluciones.models import paquetes, UsuarioPaq
import datetime

def actvivar_pqt():
    usu=UsuarioPaq.objects.all()
    for u in usu:
        pt=paquetes.objects.get(paqueteCod=str(u.paqueteMio))
        tiempo=u.fechaIni+datetime.timedelta(days=pt.paqueteDias)
        if tiempo>datetime.date.today() :
            usu=UsuarioPaq.objects.filter(paqueteMio_id=pt.paqueteID).update(activo=False)
