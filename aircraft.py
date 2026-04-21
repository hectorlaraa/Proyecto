import matplotlib.pyplot as plt
import math

from airport import LoadAirports

class Aircraft:
    def __init__(self, aircraft, origin, arrival, airline):
        self.aircraft = aircraft
        self.origin = origin
        self.arrival = arrival
        self.airline = airline

def LoadArrivals (filename):
    arrivals = []
    try:
        file = open(filename)
        lines = file.readlines()
        for i in range(1, len(lines)):
            parts = lines[i].split()
            if len(parts) == 4:
                aircraft = parts[0]
                origin = parts[1]
                arrival = parts[2]
                airline = parts[3]
                arrivals.append(Aircraft(aircraft, origin, arrival, airline))
    except FileNotFoundError:
        print("File not found")
    return arrivals

def PlotArrivals (aircrafts,ax):
    if not aircrafts:
        print("No aircrafts found")
        return
    arrivals = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
    cantidad = [0]*24
    for aircraft in aircrafts:
        hour,minute = aircraft.arrival.split(":")
        cantidad[int(hour)] = cantidad[int(hour)] + 1
    ax.bar(arrivals, cantidad, color='#1e9faa')
    ax.set_xlabel('Hour')
    ax.set_ylabel('Vuelos')
    ax.set_title('Arrivals every hour')



def SaveFlights (aircrafts, filename):
    if not aircrafts:
        return
    f = open(filename, 'w')
    f.write("Aircraft origin  arrival airline\n")
    for aircraft in aircrafts:
        f.write(f"{aircraft.aircraft} {aircraft.origin} {aircraft.arrival} {aircraft.airline}\n")
    f.close()


def PlotAirlines (aircrafts,ax):
    if not aircrafts:
        print("No aircrafts found")
        return
    cont = {}
    for i in range(len(aircrafts)):
        aircraft = aircrafts[i]
        airline = aircraft.airline
        if airline not in cont:
            cont[airline] = 0
        cont[airline] = cont[airline] + 1
    ax.bar(cont.keys(), cont.values(), color='#32612d')
    ax.set_xlabel('Airlines')
    ax.set_ylabel('Flights')
    ax.set_title('Flights every airline')



def PlotFlightsType (aircrafts,ax):
    if not aircrafts:
        print("No aircrafts found")
        return
    schengencode = ["LO", 'EB', 'LK', 'LC', 'EK', 'EE', 'EF', 'LF', 'ED', 'ET', 'LG', 'EH', 'LH', 'BI', 'LI', 'EV', 'EY', 'EL', 'LM', 'EN', 'EP', 'LP', 'LZ', 'LJ', 'LE', 'ES', 'LS']
    schengen = 0
    noschengen = 0
    for aircraft in aircrafts:
        if aircraft.origin[:2] in schengencode:
            schengen = schengen + 1
        else:
            noschengen = noschengen + 1
    ax.bar(["Schengen", "No Schengen"], [schengen, noschengen], color=["#8f1fcf", "#e57d90"])
    ax.set_xlabel('Type')
    ax.set_ylabel('Flights')
    ax.set_title('Flights schengen/No schengen')



def MapFlights(aircrafts, filename="flights.kml"):
    if not aircrafts:
        print("No aircrafts found")
        return
    schengencode = ["LO", 'EB', 'LK', 'LC', 'EK', 'EE', 'EF', 'LF', 'ED', 'ET', 'LG', 'EH', 'LH', 'BI', 'LI', 'EV', 'EY', 'EL', 'LM', 'EN', 'EP', 'LP', 'LZ', 'LJ', 'LE', 'ES', 'LS', 'GC']
    LEBLlat = 41.297445
    LEBLlon = 2.0832941
    airports = LoadAirports("Airports.txt")
    airport_dict = {}
    for a in range(len(airports)):
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


def LongDistanceArrivals(aircrafts):
    if not aircrafts:
        print("No aircrafts found")
        return []
    LEBLlat = 41.297445
    LEBLlon = 2.0832941
    R = 6371
    airports = LoadAirports("Airports.txt")
    airport_dict = {}
    for a in airports:
        airport_dict[a.ICAO] = a
    result = []
    for aircraft in aircrafts:
        if aircraft.origin in airport_dict:
            origin_airport = airport_dict[aircraft.origin]
            lat1 = math.radians(origin_airport.latitude)
            lon1 = math.radians(origin_airport.longitude)
            lat2 = math.radians(LEBLlat)
            lon2 = math.radians(LEBLlon)
            a = math.sin((lat2-lat1)/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin((lon2-lon1)/2)**2
            distance = R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
            if distance > 2000:
                result.append(aircraft)
    return result


