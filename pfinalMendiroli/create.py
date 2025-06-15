import sys
import subprocess
import logging
import pickle
import lista
import time

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

def imagen():
	subprocess.run(["lxc","image","import","/mnt/vnx/repo/arso/ubuntu2004.tar.gz","--alias","ubuntu2004"])
	
def create_bridges():
	subprocess.run(["lxc", "network", "create", "lxdbr1","ipv4.address=134.3.1.1/24" ,"ipv4.nat=true"])
	subprocess.run(["lxc", "network", "set", "lxdbr0", "ipv4.address=134.3.0.1/24", "ipv4.nat=true"])
	subprocess.run(["lxc", "network", "set", "lxdbr0", "ipv6.nat", "false"])
	subprocess.run(["lxc", "network", "set", "lxdbr0", "ipv6.address", "none"])
	subprocess.run(["lxc", "network", "set", "lxdbr1", "ipv6.nat", "false"])
	subprocess.run(["lxc", "network", "set", "lxdbr1", "ipv6.address", "none"])
	
def create_cl():
	subprocess.run(["lxc", "init","ubuntu2004","cl"])
	subprocess.run(["lxc","network","attach","lxdbr1","cl","eth0"])
	subprocess.run(["lxc","config","device","set","cl","eth0","ipv4.address","134.3.1.25"]) #Se conecta a eth0 porque solo tiene una conexión, pero al 134.3.1 del bridge1 (no eth1)
	
def create_lb():
	subprocess.run(["lxc", "init","ubuntu2004","lb"])
	subprocess.run(["lxc","network","attach","lxdbr0","lb","eth0"])
	subprocess.run(["lxc","config","device","set","lb","eth0","ipv4.address","134.3.0.10"])
	subprocess.run(["lxc","network","attach","lxdbr1","lb","eth1"])
	subprocess.run(["lxc","config","device","set","lb","eth1","ipv4.address","134.3.1.10"])
	subprocess.run(["lxc", "start", "lb"]) #Primero hay que arrancar, sino instance is not running
	eth1_in = False
	while not eth1_in:
		time.sleep(3)
		subprocess.call(["lxc", "file", "push", "50-cloud-init-lb.yaml", "lb/etc/netplan/50-cloud-init-lb.yaml"])
		time.sleep(2)
		respuesta = subprocess.run(["lxc", "exec", "lb", "--", "cat", "/etc/netplan/50-cloud-init-lb.yaml"], stdout=subprocess.PIPE) 
		eth1_in = "eth1" in respuesta.stdout.decode("utf-8")
	subprocess.run(["lxc", "restart", "lb"])
	#subprocess.call(["lxc", "exec", "lb", "--", "shutdown", "-r", "now"])
	subprocess.run(["lxc", "stop", "lb", "--force"])
	
def create_contenedor(nombre_contenedor, num_contenedor):
	subprocess.run(["lxc", "init","ubuntu2004", nombre_contenedor])
	subprocess.run(["lxc","network","attach","lxdbr0", nombre_contenedor,"eth0"])
	subprocess.run(["lxc","config","device","set",nombre_contenedor,"eth0","ipv4.address","134.3.0.1"+num_contenedor])
	

def crear():
	listaServidores=lista.mostrar_lista() #Se tiene que hacer esto para que coja la lista (que debe estar vacía por delete), y para que acumule servidores
	log.debug(f"La variable listaServidores contiene: {listaServidores}")
	imagen()
	create_bridges()
	if (len(sys.argv)==3): ##Confirma si se han pasado 3 parámetros en el mensaje (python3 orden num)
		numServidores = len(listaServidores)
		arg2 = sys.argv[2]
		suma = numServidores + int(arg2)
		if numServidores == 0:
		
			if (int(arg2) < 1) or (int(arg2) > 5):
				log.warning("El numero de parámetros no está entre 1 y 5.")	
			else:
				for i in range(1, int(arg2) +1):
					nombre_contenedor = "s"+str(i) 
					num_contenedor = str(i)
					create_contenedor(nombre_contenedor, num_contenedor)
					lista.anadir_servidor(nombre_contenedor, listaServidores)
					
				create_cl()
				create_lb()
				log.info("Hemos creado "+str(arg2) +" servidores")
				
		else:
			if (int(arg2) < 1) or (suma > 5): #Esto es para hacer create 3 y luego create 2 
				log.warning("Se ha alcanzado el número máximo de servidores.")	
			else:
				for i in range(numServidores+1, suma+1):
					nombre_contenedor = "s"+str(i) 
					num_contenedor = str(i)
					create_contenedor(nombre_contenedor, num_contenedor)
					lista.anadir_servidor(nombre_contenedor, listaServidores)
					
				create_cl()
				create_lb()
				log.info("Hemos creado "+str(arg2) +" servidores")
		
	elif (len(sys.argv)==2): ##Si sólo ha pasado 2 parámetros
		answer = input("¿Desea crear un servidor en específico? Tenga en cuenta que no puede elegir n si ya existen servidores (y/n):")
		if answer == "y": ##Crea un servidor en específico
			nombre_contenedor = input("Introduzca el nombre del servidor que quieras crear, tenga en cuenta que no puede elegir uno que ya esté creado (debe acabar en un número):")
			num_contenedor= nombre_contenedor[-1]
			create_contenedor(nombre_contenedor,num_contenedor)
			lista.anadir_servidor(nombre_contenedor, listaServidores)
			create_cl()
			create_lb()
    			
		elif answer == "n": #Crea 2 servidores por defecto si no se especifica
			argumento_pordefecto=2
			for i in range(1, argumento_pordefecto +1):	
				nombre_contenedor = "s"+str(i) 
				num_contenedor = str(i)
				create_contenedor(nombre_contenedor, num_contenedor)
				lista.anadir_servidor(nombre_contenedor, listaServidores)
			create_cl()
			create_lb()
			log.info("Hemos creado "+ str(argumento_pordefecto)+" servidores por defecto.")
	else:
		log.warning("Número de parámetros incorrecto.")
	log.debug(f"La variable listaServidores contiene: {listaServidores}")
	lista.guardar_lista(listaServidores)	


	
