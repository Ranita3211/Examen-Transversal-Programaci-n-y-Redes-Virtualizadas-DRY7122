import requests
import urllib.parse
import os

geocode_url = "https://graphhopper.com/api/1/geocode?"
route_url = "https://graphhopper.com/api/1/route?"
key = "4a4b6066-9eb0-4b53-9b2d-58ca88dc8bd9"  # Cambiar por tu API key si es necesario

transportes = {
    "auto": "car",
    "bicicleta": "bike",
    "a pie": "foot"
}

def geocoding(location, key):
    url = geocode_url + urllib.parse.urlencode({"q": location, "limit": "1", "key": key})
    respuesta = requests.get(url)
    datos = respuesta.json()
    estado = respuesta.status_code

    if estado == 200 and len(datos["hits"]) != 0:
        lat = datos["hits"][0]["point"]["lat"]
        lng = datos["hits"][0]["point"]["lng"]
        nombre = datos["hits"][0]["name"]
        pais = datos["hits"][0].get("country", "")
        estado_region = datos["hits"][0].get("state", "")
        direccion = f"{nombre}, {estado_region}, {pais}" if estado_region else f"{nombre}, {pais}"
    else:
        print("Error al buscar la ubicación:", location)
        lat, lng, direccion = None, None, location

    return estado, lat, lng, direccion

while True:
    os.system("clear" if os.name == "posix" else "cls")
    print("=======================================================")
    print("Medidor de distancias geograficas :)")
    print("=======================================================")
    print("Ingrese 's' en cualquier momento para salir")
    print("========================================================")
    print("Medios de transporte disponibles: auto, bicicleta, a pie")
    print("========================================================")
    
    medio = input("Seleccione el medio de transporte: ").lower()
    if medio == "s":
        break

    vehiculo = transportes.get(medio)

    origen = input("Ciudad de Origen: ")
    if origen.lower() == "s":
        break
    destino = input("Ciudad de Destino: ")
    if destino.lower() == "s":
        break

    estado1, lat1, lng1, dir1 = geocoding(origen, key)
    estado2, lat2, lng2, dir2 = geocoding(destino, key)

    if estado1 == 200 and estado2 == 200 and vehiculo is not None:
        puntos = f"&point={lat1}%2C{lng1}&point={lat2}%2C{lng2}"
        parametros = urllib.parse.urlencode({"vehicle": vehiculo, "key": key})
        ruta_url = route_url + parametros + puntos

        respuesta = requests.get(ruta_url)
        datos = respuesta.json()
        estado_ruta = respuesta.status_code

        if estado_ruta == 200:
            distancia_m = datos["paths"][0]["distance"]
            tiempo_ms = datos["paths"][0]["time"]

            km = distancia_m / 1000
            millas = km / 1.61
            seg = int(tiempo_ms / 1000 % 60)
            min = int(tiempo_ms / 1000 / 60 % 60)
            hr = int(tiempo_ms / 1000 / 60 / 60)

            print("\nRuta encontrada:")
            print("Desde:", dir1)
            print("Hasta:", dir2)
            print(f"Distancia: {km:.1f} km / {millas:.1f} millas")
            print(f"Duración estimada: {hr:02d}:{min:02d}:{seg:02d} (hr:min:ss)")
        else:
            print("Error al calcular la ruta:", datos.get("message", "Desconocido"))
    else:
        print("No se pudieron obtener las coordenadas para una o ambas ciudades, o el medio de transporte es inválido.")

    input("")