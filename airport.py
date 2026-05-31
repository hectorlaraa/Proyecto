class Airport:  #Definimos la clase Airport con sus atributos ICAO, latitude, longitude y schengen.
    def __init__(self, ICAO, latitude, longitude):
        self.ICAO = ICAO
        self.latitude = latitude
        self.longitude = longitude
        self.schengen = False


def IsSchengenAirport(code):    #Definimos una función que recibe un código ICAO y devuelve si x aeropuerto es Schengen o no combrobando el prefijo de este.
    schengen_prefixes = ['LO', 'EB', 'LK', 'LC', 'EK', 'EE', 'EF', 'LF', 'ED', 'ET', 'LG', 'EH', 'LH', 'BI', 'LI', 'EV',
                        'EY', 'EL', 'LM', 'EN', 'EP', 'LP', 'LZ', 'LJ', 'LE', 'ES', 'LS']
    encontrado = False
    prefix = str(code[0:2]) #Aquí indicamos donde se encuentra el prefijo del código ICAO, que es lo que nos interesa para determinar si el aeropuerto es Schengen o no.

    for i in schengen_prefixes: #Recorremos la lista de prefijos Schengen y comprobamos si el prefijo del código ICAO coincide con alguno de ellos. Si es así, encontramos el aeropuerto y devolvemos True. Si el prefijo es una cadena vacía, significa que el código ICAO no tiene un formato válido, por lo que devolvemos False.
        if prefix == i:
            encontrado = True
        if prefix == "":
            encontrado = False

    return encontrado


def SetSchengen(airport):
    airport.schengen = IsSchengenAirport(airport.ICAO)


def PrintAirport(airport):  #Definimos una función que recibe un objeto Airport y muestra su información por pantalla.
    print(f"ICAO: {airport.ICAO}")
    print(f"Coordinates: {airport.latitude}, {airport.longitude}")
    print(f"Schengen: {airport.schengen}")


def LoadAirports(filename): #Definimos una función para cargar el archivo de los aeropuertos.
    f = open(filename, 'r')
    airports = []
    f.readline()  # Saltamos la cabecera

    for linea in f:
        # 1. Limpiamos espacios invisibles y dividimos la línea
        linea = linea.strip()
        parts = linea.split()

        # 2. Solo intentamos leer si hay exactamente 3 partes (ICAO, LAT, LON)
        if len(parts) == 3:
            try:
                code = parts[0]
                lat_str = parts[1]
                lon_str = parts[2]

                # --- Lógica de Latitud ---
                if "." in lat_str:
                    lat = float(lat_str)
                else:
                    # Si no hay punto, recortamos según el formato NDDMMSS
                    lat = int(lat_str[1:3]) + int(lat_str[3:5]) / 60 + int(lat_str[5:7]) / 3600
                    if lat_str[0] == 'S': lat = -lat

                # --- Lógica de Longitud ---
                if "." in lon_str:
                    lon = float(lon_str)
                else:
                    # Si no hay punto, recortamos según el formato EDDDMMSS
                    lon = int(lon_str[1:4]) + int(lon_str[4:6]) / 60 + int(lon_str[6:8]) / 3600
                    if lon_str[0] == 'W': lon = -lon

                # 3. Añadimos el aeropuerto si todo ha ido bien
                a = Airport(code, lat, lon)
                airports.append(a)

            except:
                # Si una línea está mal formada, el programa la ignora y sigue
                print(f"Aviso: Saltando línea corrupta en el archivo.")


    f.close()
    return airports


def SaveSchengenAirports(airports, filename):   #Definimos una función que recibe la lista de aeropuertos y solo guarda en otro archivo aquellos que sean schengen.
    if len(airports) == 0:
        return " Error, no hay nada"

    f = open(filename, 'w') #Abrimos el archivo en modo escritura, lo que significa que si el archivo ya existe, se sobrescribirá. Si no existe, se creará uno nuevo.
    f.write("CODE LAT LON")

    for a in airports:
        if a.schengen == True:
            linea = a.ICAO + " " + str(a.latitude) + " " + str(a.longitude) + "\n"
            f.write(linea)
    return 0


def AddAirport(airports, new_airport):  #Definimos una función que recibe la lista de aeropuerto y uno nuevo, si no lo encuentra en la lista lo añade, pero si ya existe, no lo añade y devuelve un código de error (-1).
    encontrado = False
    i = 0
    num_airports = len(airports)

    while i < num_airports and not encontrado:  #La lógica que sigue el programa para determinar si el aeropuerto ya existe en la lista es recorrer la lista de aeropuertos y comparar el código ICAO de cada aeropuerto con el código ICAO del nuevo aeropuerto. Si encuentra una coincidencia, significa que el aeropuerto ya existe en la lista y se establece la variable "encontrado" como True. Si no encuentra ninguna coincidencia después de recorrer toda la lista, entonces "encontrado" permanece como False, lo que indica que el nuevo aeropuerto no está en la lista y puede ser añadido.
        if airports[i].ICAO == new_airport.ICAO:
            encontrado = True
        else:
            i = i + 1

    if encontrado == False:  #Solo añade el aeropuerto en caso de no encontrarlo en la lista.
        airports.append(new_airport)
        return 0


def RemoveAirport(airport_list, code):  #Al igual que la función anterior, esta función recibe la lista de aeropuertos y el código del cual queremos eliminar, si lo encuentra lo elimina si no, nos avisa.
    encontrado = False
    i = 0
    n = len(airport_list)

    while i < n and not encontrado: #Mientras no lo encuentre sigue buscando en la lista.
        if airport_list[i].ICAO == code:
            encontrado = True
        else:
            i = i + 1

    if encontrado: #Si encuentra el aeropuerto, lo elimina desplazando todos los elementos posteriores una posición hacia la izquierda y elimina el último elemento.

        while i < n - 1:
            airport_list[i] = airport_list[i + 1]
            i = i + 1

        aeros = []
        for j in range(n - 1):
            aeros.append(airport_list[j])

        airport_list.clear()
        for item in aeros:
            airport_list.append(item)

        return 0
    else:
        return -1





def PlotAirports(airports, ax): #Definimos una función que recibe la lista de aeropuertos y un objeto ax que utilizaremos para crear el gráfico.

    schengen = 0    #Mantenemos cuenta de la cantidad de aeropuertos Schengen y No Schengen para luego representarlos en el gráfico.
    no_schengen = 0

    for a in airports:  #Aqui recorre la lista airports y dependiendo de si es Schengen o no, va sumando a la variable correspondiente.
        if a.schengen == True:
            schengen = schengen + 1
        else:
            no_schengen = no_schengen + 1

#Representamos el gráfico de barras con los datos obtenidos.
    labels = ['Airports']
    ax.bar(labels, [schengen], label='Schengen', color='steelblue')

    ax.bar(labels, [no_schengen], bottom=[schengen], label='No Schengen', color='lightcoral')

    ax.set_xlabel('Count')
    ax.set_title('Schengen airports')
    ax.legend()

def MapAirports(airports, filename="airports.kml"): #Definimos una función que nos generará un archivo KML para indicarnos donde se encuentra cada aeropuerto en el mapa.
    f = open(filename, 'w')

    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
    f.write('<Document>\n')
    f.write('  <name>Airports Map</name>\n')

    for a in airports:

        if a.schengen == True:  #Aquí indicamos si el aeropuerto es Schengen o no asignandole colores diferentes.
            color = "ff0000ff"
        else:
            color = "ffff0000"
#Guía visual para ver donde se encuentra x aeropuerto en el mapa.
        f.write('  <Placemark>\n')
        f.write('    <name>' + a.ICAO + '</name>\n')
        f.write('    <Style>\n')
        f.write('      <IconStyle>\n')
        f.write('        <color>' + color + '</color>\n')
        f.write('      </IconStyle>\n')
        f.write('    </Style>\n')
        f.write('    <Point>\n')
#Indicamos las coordenadas de cada aeropuerto, utilizando la longitud y latitud de cada uno.
        f.write('      <coordinates>' + str(a.longitude) + ',' + str(a.latitude) + ',0</coordinates>\n')
        f.write('    </Point>\n')
        f.write('  </Placemark>\n')

    f.write('</Document>\n')
    f.write('</kml>\n')
    f.close()
    print(f"Archivo {filename} generado. Ábrelo con Google Earth.")




