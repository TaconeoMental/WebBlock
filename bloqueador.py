from datetime import datetime
from datetime import timedelta
from sys import argv
import re
import os


msje_ayuda = '''
Programa que bloquea sitios por determinada cantidad de tiempo

blqueador.py [hr][m][s]

Comandos:

    [hr]    Cantidad de horas en el temporizador
    [m]     Cantidad de segundos en el temporizador
    [s]     Cantidad de segundos en el temporizador

La lista de sitios 
Ejemplos:
 
    bloqueador.py 3hr4m6s        Bloquea los sitios por 3 horas, 4 minutos y 6 segundos 

    bloqueador.py 2hr            Bloquea los sitios por 2 horas

    bloqueador.py 30m50s         Bloquea los sitios por 30 minutos y 50 segundos
'''


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
        raise SyntaxError

class Copia:
    def __init__(self, archivo):
        self.archivo = os.path.basename(os.path.splitext(archivo)[0])
        self.copia = self.archivo + "_temp"

    def copiar(self):

        with open(self.archivo, "r") as original:
            with open(self.copia, "w") as copia:
                copia.writelines(original.readlines())
                copia.close()
            original.close()

    def eliminar(self):
        os.remove(self.copia)


def main():

    delta_tiempo = None

    ruta_hosts = r"C:\Windows\System32\drivers\etc\hosts"

    redireccion = "127.0.0.1"

    hora_com = datetime.now()

    patron_tiempo = re.compile(r"((?P<hours>\d+?)hr)?((?P<minutes>\d+?)m)?((?P<seconds>\d+?)s)+")

    if len(argv) > 1:

        if argv[1] != "--help":

            # delta_tiempo = syntax_tiempo(argv[1], patron_tiempo)
            # if delta_tiempo == "0:00:00":
            #     print("Ejecuta el comando \"python bloqueador.py --help\" para obtener ayuda.")
            # else:
            try:
                tiempo_delta = delta_tiempo = syntax_tiempo(argv[1], patron_tiempo)
            except Exception as e:
                print("Ejecuta el comando \"python bloqueador.py --help\" para obtener ayuda.")
                exit()

            print(delta_tiempo)
            hora_fin = hora_com + delta_tiempo

            hosts = Copia(ruta_hosts)
            hosts.copiar()

            ##### Añadir Páginas #####
            with open("Páginas Web.txt", "r") as pag:
                paginas = [linea.rstrip("\n") for linea in pag.readlines()]
                pag.close()
            with open(ruta_hosts, "a") as hosts_arch:
                for pagina in paginas:
                    hosts_arch.write("\n{} {}".format(redireccion, pagina))
                hosts_arch.close()



            while True:
                if datetime.now() > hora_fin:
                    # Desbloquear sitios
                    print("wena prro")
                    with open(hosts.copia, "r") as temp:
                        lineas = temp.readlines()
                        with open(ruta_hosts, "w") as hosts_or:
                            for linea in lineas:
                                hosts_or.writelines(linea)
                            hosts_or.close()
                        temp.close()

                    hosts.eliminar()
                    break

        elif argv[1] == "--help":
            print(msje_ayuda)

        else:
            print("Ejecuta el comando \"python bloqueador.py --help\" para obtener ayuda.")

    else:
        print("Ejecuta el comando \"python bloqueador.py --help\" para obtener ayuda.")

if __name__ == '__main__':
    main()
