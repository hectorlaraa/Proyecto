class Airport:
    def __init__(self, ICAO, latitude, longitude):
        self.ICAO = ICAO
        self.latitude = latitude
        self.longitude = longitude
        self.schengen = False


def IsSchengenAirport(code):
    schengen_prefixes = ['LO', 'EB', 'LK', 'LC', 'EK', 'EE', 'EF', 'LF', 'ED', 'ET', 'LG', 'EH', 'LH', 'BI', 'LI', 'EV',
                         'EY', 'EL', 'LM', 'EN', 'EP', 'LP', 'LZ', 'LJ', 'LE', 'ES', 'LS']
    encontrado = False
    prefix = str(code[0:2])

    for i in schengen_prefixes:
        if prefix == i:
            encontrado = True
        if prefix == "":
            encontrado = False

    return encontrado


def SetSchengen(airport):
    airport.schengen = IsSchengenAirport(airport.ICAO)


def PrintAirport(airport):
    print(f"ICAO: {airport.ICAO}")
    print(f"Coordinates: {airport.latitude}, {airport.longitude}")
    print(f"Schengen: {airport.schengen}")


def LoadAirports(filename):
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


def SaveSchengenAirports(airports, filename):
    if len(airports) == 0:
        return " Error, no hay nafda"

    f = open(filename, 'w')
    f.write("CODE LAT LON")

    for a in airports:
        if a.schengen == True:
            linea = a.ICAO + " " + str(a.latitude) + " " + str(a.longitude) + "\n"
            f.write(linea)
    return 0


def AddAirport(airports, new_airport):
    encontrado = False
    i = 0
    num_airports = len(airports)

    while i < num_airports and not encontrado:
        if airports[i].ICAO == new_airport.ICAO:
            encontrado = True
        else:
            i = i + 1

    # 3. Conditional Statement: Solo añadimos si NO se encontró
    if encontrado == False:
        airports.append(new_airport)
        return 0


def RemoveAirport(airport_list, code):
    encontrado = False
    i = 0
    n = len(airport_list)

    while i < n and not encontrado:
        if airport_list[i].ICAO == code:
            encontrado = True
        else:
            i = i + 1

    if encontrado:

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





def PlotAirports(airports, ax):

    n_schengen = 0
    n_no_schengen = 0

    for a in airports:
        if a.schengen == True:
            n_schengen = n_schengen + 1
        else:
            n_no_schengen = n_no_schengen + 1


    labels = ['Airports']
    ax.bar(labels, [n_schengen], label='Schengen', color='steelblue')

    ax.bar(labels, [n_no_schengen], bottom=[n_schengen], label='No Schengen', color='lightcoral')

    ax.set_xlabel('Count')
    ax.set_title('Schengen airports')
    ax.legend()

def MapAirports(airports, filename="airports.kml"):
    f = open(filename, 'w')

    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
    f.write('<Document>\n')
    f.write('  <name>Airports Map</name>\n')

    for a in airports:

        if a.schengen == True:
            color = "ff0000ff"
        else:
            color = "ffff0000"

        # 4. Escribimos la "chincheta" (Placemark) para cada aeropuerto
        f.write('  <Placemark>\n')
        f.write('    <name>' + a.ICAO + '</name>\n')
        f.write('    <Style>\n')
        f.write('      <IconStyle>\n')
        f.write('        <color>' + color + '</color>\n')
        f.write('      </IconStyle>\n')
        f.write('    </Style>\n')
        f.write('    <Point>\n')

        f.write('      <coordinates>' + str(a.longitude) + ',' + str(a.latitude) + ',0</coordinates>\n')
        f.write('    </Point>\n')
        f.write('  </Placemark>\n')

    f.write('</Document>\n')
    f.write('</kml>\n')
    f.close()
    print(f"Archivo {filename} generado. Ábrelo con Google Earth.")