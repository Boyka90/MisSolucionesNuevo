
from MySQLdb import _mysql

db=_mysql.connect(host="missoluciones2022.mysql.pythonanywhere-services.com",user="missoluciones202",password="Tamara2023",database="missoluciones202$misSoluciones2023")

def actvivar_pqt():
    db.query("UPDATE Soluciones_usuariopaq INNER JOIN Soluciones_paquetes ON Soluciones_usuariopaq.paqueteMio_id = Soluciones_paquetes.paqueteId SET Soluciones_usuariopaq.vencido = CASE WHEN DATE_ADD(Soluciones_usuariopaq.fechaIni, INTERVAL Soluciones_paquetes.paqueteDias DAY) < CURDATE() THEN 1 ELSE Soluciones_usuariopaq.vencido END")


actvivar_pqt()