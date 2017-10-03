from datetime import datetime
from datetime import timedelta
import sys
import re
import os


msje_ayuda = '''
Programa que bloquea sitios por determinada cantidad de tiempo

La lista de sitios a bloquear se encuentra en el archivo \"Páginas Web.txt\".

Uso: blqueador.py [hr][m][s]

Comandos:

    [hr]    Cantidad de horas en el temporizador
    [m]     Cantidad de minutos en el temporizador
    [s]     Cantidad de segundos en el temporizador


Ejemplos:

    bloqueador.py 3hr4m6s        Bloquea los sitios por 3 horas, 4 minutos y 6 segundos

    bloqueador.py 2hr            Bloquea los sitios por 2 horas

    bloqueador.py 30m50s         Bloquea los sitios por 30 minutos y 50 segundos
'''


# Función que parsea input de tiempo y lo transforma en un objecto timedelta
def syntax_tiempo(cadena_tiempo, patron_compilado):
    partes = patron_compilado.match(cadena_tiempo)
    if partes:
        partes = partes.groupdict()
        parametros_tiempo = {}
        for (nombre, parametros) in partes.items():
            if parametros:
                parametros_tiempo[nombre] = int(parametros)
        return timedelta(**parametros_tiempo)
    else:
        print(msje_ayuda)
        sys.exit()


# Función que devuelve un archivo a su estado original basándose en una copia temporal
def volver_original(original, copia):
    print("¡Ahora eres libre de nuevo!")
    with open(copia, "r") as temp:
        lineas = temp.readlines()
        with open(original, "w") as hosts_or:
            for linea in lineas:
                hosts_or.writelines(linea)
            hosts_or.close()
        temp.close()


# Clase que crea archivo temporales y los elimina
class Copia:
    def __init__(self, archivo):
        self.ruta = archivo
        self.archivo = os.path.basename(os.path.splitext(archivo)[0])
        self.copia = self.archivo + "_temp"

    def copiar(self):
        with open(self.ruta, "r") as original:
            with open(self.copia, "w") as copia:
                copia.writelines(original.readlines())
                copia.close()
            original.close()

    def eliminar(self):
        """Elimina la copia del archivo"""
        os.remove(self.copia)


def main():
    delta_tiempo = None
    # NOTE: Agregar detección de OS
    ruta_hosts = r"C:\Windows\System32\drivers\etc\hosts"
    redireccion = "127.0.0.1"
    # Hora de comienzo de script
    hora_com = datetime.now()
    patron_tiempo = re.compile(r"((?P<hours>\d+?)hr)?((?P<minutes>\d+?)m)?((?P<seconds>\d+)s)?")

    try:
        delta_tiempo = syntax_tiempo(sys.argv[1], patron_tiempo)

        print("Tiempo: ", delta_tiempo)
        hora_fin = hora_com + delta_tiempo

        hosts = Copia(ruta_hosts)
        hosts.copiar()

        # Añadir páginas al archivo 'hosts'
        with open("Páginas Web.txt", "r") as pag:
            paginas = [linea.rstrip("\n") for linea in pag.readlines()]
        with open(ruta_hosts, "a") as hosts_arch:
            for pagina in paginas:
                hosts_arch.write("\n{} {}".format(redireccion, pagina))

        # Checkear constantemente si ya se llegó a la hora final
        while True:
            if datetime.now() > hora_fin:
                volver_original(ruta_hosts, hosts.copia)
                return

    except KeyboardInterrupt:
        volver_original(ruta_hosts, hosts.copia)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(msje_ayuda)
        sys.exit()
    main()
