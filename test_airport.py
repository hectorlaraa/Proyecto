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
PlotAirports(airport_list)


# En test_airports.py, al final:
from airport import MapAirports

print("\n--- TEST: MapAirports (Google Earth) ---")


MapAirports(airport_list, "Mapa_Aeropuertos.kml")

print("Busca el archivo 'Mapa_Aeropuertos.kml' en tu carpeta y ábrelo con Google Earth.")