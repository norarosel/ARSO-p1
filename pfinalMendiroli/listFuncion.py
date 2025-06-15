import subprocess
import sys
import logging
import pickle
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def listar():
	subprocess.run(["lxc", "list"]) 
