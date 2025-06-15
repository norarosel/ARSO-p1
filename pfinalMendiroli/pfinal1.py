import subprocess
import sys
import logging
import pickle
import time
import create
import stop
import delete
import start
import listFuncion
import lista

arg1 = sys.argv[1]
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

if arg1 == "create":
	create.crear()

if arg1 == "list":
	listFuncion.listar()

if arg1 == "start":
	start.arrancar()

if arg1 == "delete":
	delete.destruir()
	
if arg1 == "stop":
	stop.parar()
