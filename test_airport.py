from airport import *
airport = Airport ("LEBL", 41.297445, 2.0832941)
SetSchengen(airport)
PrintAirport (airport)

airport_list = LoadAirports("Airports.txt")
print(f"Loaded {len(airport_list)} airports.")

for a in airport_list:
    SetSchengen(a)
nuevo = Airport("nasa", 41.90, 2.76) # Gerona

res1 = AddAirport(airport_list, nuevo)


print(f"List size after adding PRUEBA: {len(airport_list)}")

codigo_a_borrar = "EBAW"
resultado = RemoveAirport(airport_list, codigo_a_borrar)


result = SaveSchengenAirports(airport_list, "Schengen_Airports.txt")
if result == 0:
    print("Successfully saved Schengen airports to file.")



# En test_airports.py, al final:
from airport import MapAirports

print("\n--- TEST: MapAirports (Google Earth) ---")


MapAirports(airport_list, "Mapa_Aeropuertos.kml")

print("Busca el archivo 'Mapa_Aeropuertos.kml' en tu carpeta y ábrelo con Google Earth.")

# Importamos las funciones necesarias de airport.py
from airport import LoadAirports, CrearListaExamen


def ProbarExamen():
    # 1. Cargamos la lista completa de aeropuertos desde el archivo
    # Asegúrate de que "Airports.txt" esté en la misma carpeta
    ruta_archivo = "Airports.txt"
    lista_completa = LoadAirports(ruta_archivo)

    print(f"Total de aeropuertos cargados: {len(lista_completa)}")
    print("-" * 30)

    # 2. Llamamos a la función del examen
    lista_filtrada = CrearListaExamen(lista_completa)

    # 3. Mostramos los resultados
    print(f"Aeropuertos que cumplen las condiciones del examen:")
    print(f"(Latitud N+Par y Longitud E+Impar)")
    print("-" * 30)

    if len(lista_filtrada) == 0:
        print("No se encontró ningún aeropuerto que cumpla los requisitos.")
    else:
        i = 0
        while i < len(lista_filtrada):
            aero = lista_filtrada[i]
            # Suponiendo que tu objeto tiene un atributo .Name o .ICAO
            # Si es una lista de strings, usa solo: print(aero)
            print(f"- {aero.ICAO}: Lat {aero.lat_str}, Lon {aero.lon_str}")
            i = i + 1

    print("-" * 30)
    print(f"Total encontrados: {len(lista_filtrada)}")


# Ejecutamos la prueba
if __name__ == "__main__":
    ProbarExamen()