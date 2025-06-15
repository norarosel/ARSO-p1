import subprocess
import sys
import time
import lista
import logging
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

def parar():

	answer = input("¿Desea parar todos los servidores? (y/n):")
	if answer == "y":
		subprocess.run(["lxc","stop","--all"])
		log.info("Hemos parado todos los servidores.")
	if answer == "n":
		nombre_servidor = input("Introduzca el nombre del servidor que quieras parar:")
		subprocess.run(["lxc", "stop", nombre_servidor])
		log.info("Hemos parado el servidor.")
