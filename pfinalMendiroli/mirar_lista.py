import pickle
with open("listaServidores.dat", "rb") as f:
    datos = pickle.load(f)

print(datos)
