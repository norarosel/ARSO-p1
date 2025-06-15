import subprocess
import sys
import logging
import pickle
import create

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def anadir_servidor(servidor, listaServidores):
	listaServidores.append(servidor)
	
def quitar_servidor(servidor, listaServidores):
	listaServidores.remove(servidor)

def mostrar_lista():
	with open("listaServidores.dat", "rb") as fich:
		lista = pickle.load(fich)
	return lista
	
def guardar_lista(listaServidores):
	
	with open("listaServidores.dat", "wb") as fich: #Esto necesario para acceder a la lista desde otros módulos, tiene que estar guardada, w sobreescribe
        	pickle.dump(listaServidores, fich)
        
