import subprocess
import sys
import time
import lista
import logging
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

def arrancar():

	subprocess.run(["lxc","start","lb"])
	subprocess.run(["lxc","start","cl"])

	answer = input("¿Desea arrancar todos los servidores? (y/n):")
	if answer == "y":
		subprocess.run(["lxc","start","--all"])
		subprocess.run(["sleep", "5"]) #Esperamos para no mostrar el bash antes de haber arrancado
		servidores = lista.mostrar_lista() #Para el bash
		log.info("Hemos arrancado todos los servidores.")
		for servidor in servidores:
			subprocess.Popen(["xterm", "-e", "lxc", "exec", servidor, "bash"]) #Muestra la consola de la mv, usamos Popen porque es asíncrona y no bloquea
	if answer == "n":
		nombre_servidor = input("Introduzca el nombre del servidor que quieras arrancar:")
		subprocess.run(["lxc", "start", nombre_servidor])
		subprocess.run(["sleep", "5"])
		log.info("Hemos arrancado el servidor.")
		subprocess.Popen(["xterm", "-e", "lxc", "exec", nombre_servidor, "bash"])
