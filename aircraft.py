import matplotlib.pyplot as plt
import math

from airport import LoadAirports


class Aircraft:
    def __init__(self, aircraft, origin=None, arrival=None, airline=None, destination=None, departure=None):
        self.aircraft = aircraft
        self.origin = origin
        self.arrival = arrival
        self.airline = airline
        self.destination = destination
        self.departure = departure


# Definimos la función para cargar el archivo de llegadas.
def LoadArrivals(filename):
    arrivals = []  # Lista vacía para almacenar los objetos Aircraft
    try:  # Intentamos abrir el archivo, y si el programa no lo encuentra no avisa con un mensaje de error gracias al except.
        file = open(filename)  # Abrimos el archivo con el nombre recibido como argumento
        lines = file.readlines()  # Utiliizamos el readlines para leer todas las líneas y nos devuelve una lista.
        for i in range(1, len(lines)):
            parts = lines[i].split()  # Separamos cada línea en partes.
            if len(parts) == 4:  # Aqui comprobamos que cada línea tenga 4 partes.
                aircraft = parts[0]  # Asignamos cada parte a su variable correspondiente.
                origin = parts[1]
                arrival = parts[2]
                airline = parts[3]
                arrivals.append(Aircraft(aircraft, origin, arrival,
                                         airline))  # Utilizamos la función append para añadir el objeto a la lista vacía arrivals que habíamos creado.
    except FileNotFoundError:
        print("File not found")
    return arrivals  # Nos devuelve la lista de arrivals una vez esta ya haya pasado por todas las líneas del archivo.


def PlotArrivals(aircrafts,
                 ax):  # Definimos PlotArrivals que recibe la lista de aircrafts y el objeto ax para graficar.
    if not aircrafts:  # Aqui si la lista de aircrafts está vacía, el programa avisa con un mensaje de error y no intenta graficar nada.
        print("No aircrafts found")
        return
    arrivals = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22,
                23]  # Determinamos cada hora del día para graficar en el eje x.
    cantidad = [0] * 24
    for aircraft in aircrafts:  # Recorremos la lista de aircrafts, y por cada uno de ellos separamos la hora y los minutos de su llegada utilizando el split.
        hour, minutes = aircraft.arrival.split(":")  # Separamos la hora y los minutos utilizando el split.
        cantidad[int(hour)] = cantidad[
                                  int(hour)] + 1  # Utilizamos la hora para determinar en qué posición de la lista cantidad se encuentra, y sumamos 1 a esa posición cada vez que un avión llegue a esa hora.
    ax.bar(arrivals, cantidad,
           color='#1e9faa')  # Utilizamos el método bar para graficar un gráfico de barras, con las horas en el eje x y la cantidad de llegadas en el eje y. El color de las barras es #1e9faa.
    ax.set_xlabel('Hour')
    ax.set_ylabel('Vuelos')
    ax.set_title('Arrivals every hour')


def SaveFlights(aircrafts,
                filename):  # Definimos la función SaveFlights que recibe la lista de aircrafts y el nombre del archivo donde se guardarán los datos.
    if not aircrafts:  # Si la lista de aircrafts está vacía, el programa avisa con un mensaje de error y no intenta guardar nada.
        return -1

    f = open(filename,
             'w')  # Abrimos el archivo en modo escritura, lo que significa que si el archivo ya existe, se sobrescribirá.
    f.write(
        "Aircraft origin arrival airline\n")  # Escribimos la cabecera del archivo, con los nombres de las columnas separados por espacios.
    for aircraft in aircrafts:  # Aqui indicamos lo que hay que escribir por cada avión, utilizando el método write para escribir una línea por cada avión, con sus atributos separados por espacios.
        f.write(f"{aircraft.aircraft} {aircraft.origin} {aircraft.arrival} {aircraft.airline}\n")
    f.close()

    return 0


def PlotAirlines(aircrafts,
                 ax):  # Definimos la función PlotAirlines que recibe la lista de aircrafts y el objeto ax para graficar.
    if not aircrafts:  # Si la lista de aircrafts está vacía, el programa avisa con un mensaje de error y no intenta graficar nada.
        print("No aircrafts found")
        return
    cont = {}
    for i in range(
            len(aircrafts)):  # Recorremos la lista de aircrafts utilizando un bucle for, y por cada avión obtenemos su aerolínea utilizando el atributo airline.
        aircraft = aircrafts[i]
        airline = aircraft.airline  # Obtenemos la aerolínea del avión utilizando el atributo airline.
        if airline not in cont:  # Sumamos 1 a la cantidad de vuelos de esa aerolínea en el diccionario cont, que tiene como clave el nombre de la aerolínea y como valor la cantidad de vuelos. Si la aerolínea no está en el diccionario, la añadimos con un valor inicial de 0.
            cont[airline] = 0
        cont[airline] = cont[airline] + 1
        # Ordenamos el diccionario por valores de mayor a menor y nos quedamos con los 10 primeros
    top10 = dict(sorted(cont.items(), key=lambda x: x[1], reverse=True)[:10])

        # Dibujamos el gráfico pasándole las claves, los valores y el color todo dentro del mismo paréntesis
    ax.bar(top10.keys(), top10.values(), color='#32612d')
    ax.set_xlabel('Airlines')
    ax.set_ylabel('Flights')
    ax.set_title('Flights every airline')
    ax.tick_params(axis='x',
                   rotation=90)  # Rotamos las etiquetas del eje x para que se vean mejor, ya que pueden ser muchas aerolíneas y sus nombres pueden ser largos.


def PlotFlightsType(aircrafts,
                    ax):  # Definimos una función para graficar la cantidad de vuelos que llegan desde países Schengen y no Schengen, utilizando un gráfico de barras. Recibe la lista de aircrafts y el objeto ax para graficar.
    if not aircrafts:
        print("No aircrafts found")
        return
    schengencode = ["LO", 'EB', 'LK', 'LC', 'EK', 'EE', 'EF', 'LF', 'ED', 'ET', 'LG', 'EH', 'LH', 'BI', 'LI', 'EV',
                    'EY', 'EL', 'LM', 'EN', 'EP', 'LP', 'LZ', 'LJ', 'LE', 'ES', 'LS']  # Indicamos los códigos ICAO
    schengen = 0  # Mantenemos un contador para los vuelos Schengen y otro para los no Schengen, ambos inicializados a 0.
    noschengen = 0
    for aircraft in aircrafts:  # Recorremos la lista de aircrafts utilizando un bucle for, y por cada avión obtenemos su origen utilizando el atributo origin. Luego, comprobamos si los dos primeros caracteres del código ICAO del origen están en la lista de códigos Schengen. Si es así, sumamos 1 al contador de vuelos Schengen, y si no, sumamos 1 al contador de vuelos no Schengen.
        if aircraft.origin[:2] in schengencode:
            schengen = schengen + 1
        else:
            noschengen = noschengen + 1
    ax.bar(["Schengen", "No Schengen"], [schengen, noschengen], color=["#8f1fcf",
                                                                       "#e57d90"])  # Graficamos la cantidad de aeropuertos schengen y no schengen utilizando el método bar, con las etiquetas "Schengen" y "No Schengen" en el eje x, y la cantidad de vuelos en el eje y. El color de las barras es #8f1fcf para Schengen y #e57d90 para No Schengen.
    ax.set_xlabel('Type')
    ax.set_ylabel('Flights')
    ax.set_title('Flights schengen/No schengen')


def MapFlights(aircrafts,
               filename="flights.kml"):  # Definimos la función MapFLights que recibe la lista de aircrafts y el nombre del archivo donde se guardará el mapa en formato KML. Esta función crea un mapa con las rutas de los vuelos, utilizando líneas verdes para los vuelos Schengen y líneas azules para los vuelos no Schengen.
    if not aircrafts:  # Si la lsita aircrafts está vacía, el programa avisa con un mensaje de error y no intenta crear el mapa.
        print("No aircrafts found")
        return -1
    schengencode = ["LO", 'EB', 'LK', 'LC', 'EK', 'EE', 'EF', 'LF', 'ED', 'ET', 'LG', 'EH', 'LH', 'BI', 'LI', 'EV',
                    'EY', 'EL', 'LM', 'EN', 'EP', 'LP', 'LZ', 'LJ', 'LE', 'ES', 'LS', 'GC']
    LEBLlat = 41.297445  # Indicamos las coordenadas de LEBL que utilizaremos como aeropuerto principal.
    LEBLlon = 2.0832941
    airports = LoadAirports("Airports.txt")  # De aqui carga la información de los aeropuertos
    airport_dict = {}
    for a in range(len(airports)):  # Aquí introducimos el programa para que se genere el archivo KML.
        airport_dict[airports[a].ICAO] = airports[a]
    f = open(filename, "w")
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
    f.write('<Document>\n')
    for aircraft in aircrafts:
        if aircraft.origin in airport_dict:
            origin_airport = airport_dict[aircraft.origin]
            f.write('<Placemark>\n')
            f.write('<name>Route ' + aircraft.origin + '-LEBL</name>\n')
            f.write('<Style><LineStyle>\n')
            f.write('<color>ff00ff00</color>\n' if aircraft.origin[:2] in schengencode else '<color>ff0000ff</color>\n')
            f.write('</LineStyle></Style>\n')
            f.write('<LineString>\n')
            f.write('<coordinates>\n')
            f.write(str(origin_airport.longitude) + ',' + str(origin_airport.latitude) + ',0\n')
            f.write(str(LEBLlon) + ',' + str(LEBLlat) + ',0\n')
            f.write('</coordinates>\n')
            f.write('</LineString>\n')
            f.write('</Placemark>\n')
    f.write('</Document>\n')
    f.write('</kml>\n')
    f.close()

    return 0


def LongDistanceArrivals(
        aircrafts):  # Definimos una función para determinar los vuelos que llegan a una distancia superior a 2000km de LEBL
    if not aircrafts:  # Si la lista de aircrafts está vacía, el programa avisa con un mensaje de error y no intenta determinar los vuelos de larga distancia.
        print("No aircrafts found")
        return []
    LEBLlat = 41.297445  # Coordenadas LEBL
    LEBLlon = 2.0832941
    R = 6371  # Radio de la Tierra en km
    airports = LoadAirports(
        "Airports.txt")  # Aquí carga la información de los aeropuertos que utilizaremos para determinar la distancia.
    airport_dict = {}
    for a in airports:
        airport_dict[a.ICAO] = a
    result = []
    for aircraft in aircrafts:
        if aircraft.origin in airport_dict:  # Utilizamos la función de Haversine para determinar la distancia entre ambos aeropuertos.
            origin_airport = airport_dict[aircraft.origin]
            lat1 = math.radians(origin_airport.latitude)
            lon1 = math.radians(origin_airport.longitude)
            lat2 = math.radians(LEBLlat)
            lon2 = math.radians(LEBLlon)
            a = math.sin((lat2 - lat1) / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin((lon2 - lon1) / 2) ** 2
            distance = R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
            if distance > 2000:
                result.append(aircraft)
    return result


def LoadDepartures(filename):  # Definimos la función que carga el archivo de salidas.
    departures = []  # Creamos una lista vacía para almacenar los objetos Aircraft de las salidas.
    try:
        file = open(filename,
                    'r')  # Intentamos abrir el archivo, pero si no lo encuentra, gracias al except, el programa nos avisa
        lines = file.readlines()
        file.close()

        for i in range(1,
                       len(lines)):  # Recorremos el archivo línia por línea, gracias al readlines ya que nos ha devuelto una lista con strings.
            parts = lines[i].split()  # Separamos cada línea aplicando el método split.
            if len(parts) == 4:  # Comprobamos que cada línea esté bien formada.
                aircraft = parts[0]  # Asignamos cada parte con su variable correspondiente.
                destination = parts[1]
                departure = parts[2]
                airline = parts[3]

                departures.append(
                    Aircraft(aircraft, origin=None, arrival=None, airline=airline, destination=destination,
                             departure=departure))  # Aqui utilizando el appen añadimos a departures el objeto Aircraft creado con los datos de la línea del archivo.
    except FileNotFoundError:
        print("File not found")
        return [], -1

    return departures, 0


def time_to_minutes(
        time_str):  # Función auxiliar para convertir una hora en formato "HH:MM" a minutos totales desde medianoche, lo que facilita las comparaciones de tiempo.
    if not time_str: return 0
    h, m = map(int, time_str.split(':'))
    return h * 60 + m


def MergeMovements(arrivals, departures):
    if not arrivals or not departures:
        return [], -1  # Código de error si alguna lista está vacía

    merged_list = []
    used_arrivals = set()  # Para no reutilizar la misma llegada dos veces

    # Clonamos y ordenamos cronológicamente para asegurar emparejamientos lógicos
    arr_sorted = sorted(arrivals, key=lambda a: time_to_minutes(a.arrival))
    dep_sorted = sorted(departures, key=lambda d: time_to_minutes(d.departure))

    for dep in dep_sorted:
        matched_arr = None
        for arr in arr_sorted:
            # Buscamos que coincida el ID, que la llegada no se haya fusionado ya,
            # y que la llegada sea ANTERIOR a la salida.
            if arr not in used_arrivals and arr.aircraft == dep.aircraft:
                if time_to_minutes(arr.arrival) < time_to_minutes(dep.departure):
                    matched_arr = arr
                    break  # Encontramos la llegada correspondiente a esta salida

        if matched_arr:
            # Fusionamos los datos en una nueva estructura Aircraft
            merged_aircraft = Aircraft(
                aircraft=dep.aircraft,
                origin=matched_arr.origin,
                arrival=matched_arr.arrival,
                airline=dep.airline,
                destination=dep.destination,
                departure=dep.departure
            )
            merged_list.append(merged_aircraft)
            used_arrivals.add(matched_arr)  # Marcamos la llegada como utilizada
        else:
            # Si no hay llegada previa compatible, es un avión que pasó la noche (night aircraft)
            merged_list.append(dep)

    # Finalmente, añadimos los aviones que llegaron pero no han despegado aún
    for arr in arr_sorted:
        if arr not in used_arrivals:
            merged_list.append(arr)

    return merged_list, 0


def NightAircraft(aircrafts):
    if not aircrafts:
        return [], -1  # Código de error si la lista está vacía

    night_list = []
    for a in aircrafts:
        # Si origin/arrival es None pero destination/departure tiene datos
        if a.arrival is None and a.departure is not None:
            night_list.append(a)

    return night_list, 0


def GetStatusAtTime(aircrafts, current_mins):
    '''
    Calcula el estado del aeropuerto en un minuto exacto del día.
    '''
    en_tierra = 0
    llegadas_hoy = 0
    salidas_hoy = 0
    ultimo_movimiento = "Ninguno"
    min_diff = 9999  # Para buscar el evento más cercano a la hora actual

    # Función auxiliar rápida para pasar la hora ("08:30") a minutos (510)
    def to_mins(t_str):
        if not t_str or t_str == "" or t_str == "None": return -1
        try:
            h, m = map(int, t_str.split(':'))
            return h * 60 + m
        except:
            return -1

    for a in aircrafts:
        arr = to_mins(getattr(a, 'arrival', None))
        dep = to_mins(getattr(a, 'departure', None))

        # Contamos aterrizajes y despegues hasta esta hora
        if 0 <= arr <= current_mins:
            llegadas_hoy += 1
        if 0 <= dep <= current_mins:
            salidas_hoy += 1

        # ¿El avión está aparcado en el aeropuerto en este preciso minuto?
        esta_en_tierra = False
        if arr >= 0 and dep >= 0:
            if arr <= current_mins < dep:
                esta_en_tierra = True
        elif arr >= 0 and dep == -1:  # Llegó y no sale hoy
            if arr <= current_mins:
                esta_en_tierra = True
        elif arr == -1 and dep >= 0:  # Durmió en el aeropuerto y sale hoy
            if current_mins < dep:
                esta_en_tierra = True

        if esta_en_tierra:
            en_tierra += 1

        # Buscamos qué fue lo último que pasó (el evento más cercano hacia atrás)
        if 0 <= arr <= current_mins and (current_mins - arr) < min_diff:
            min_diff = current_mins - arr
            ultimo_movimiento = f"{a.aircraft} aterrizó a las {a.arrival}"

        if 0 <= dep <= current_mins and (current_mins - dep) < min_diff:
            min_diff = current_mins - dep
            ultimo_movimiento = f"{a.aircraft} despegó a las {a.departure}"

    return en_tierra, llegadas_hoy, salidas_hoy, ultimo_movimiento