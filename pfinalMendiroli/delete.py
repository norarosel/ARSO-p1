import subprocess
import sys
import logging
import pickle
import time
import lista
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def destruir(): 
	listaServidores = lista.mostrar_lista()
	logger.debug(f"listaServidores contiene: {listaServidores}") #Para ver qué teníamos en la lista antes de borrar

	answer = input("¿Desea borrar todos los servidores y elementos de comunicación? (y/n):")
	
	if answer == "y":
		for servidor in listaServidores:
			subprocess.run(["lxc","stop",servidor])
			subprocess.run(["lxc","delete",servidor])
			#lista.quitar_servidor(servidor, listaServidores) lo hemos quitado porque no se puede modificar una lista que estamos iterando
			logger.info("Servidor " + str(servidor) + " destruido." )
		listaServidores = list()
		lista.guardar_lista(listaServidores) #Borramos la lista guardando una vacía, porque hemos elegido borrar todos los servidores
		subprocess.run(["lxc","stop","lb"])
		subprocess.run(["lxc","stop","cl"])		
		subprocess.run(["lxc","delete","lb"])
		subprocess.run(["lxc","delete","cl"])
		#subprocess.run(["lxc","network","delete","lxdbr0"]) no se puede borrar
		subprocess.run(["lxc","network","delete","lxdbr1"])
		logger.info("Se han borrado todos los componentes de comunicación")
		

	if answer == "n":
    		nombre_servidor = input("Introduzca el nombre del servidor que quieras borrar:")
    		subprocess.run(["lxc", "stop", nombre_servidor, "--force"])
    		subprocess.run(["lxc","delete",nombre_servidor])
    		logger.info("Servidor " + str(nombre_servidor) + " destruido." )
    		lista.quitar_servidor(nombre_servidor, listaServidores)
	lista.guardar_lista (listaServidores)	  
		
		
