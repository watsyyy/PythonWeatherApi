import sqlite3, urllib2, datetime, json
from bottle import route, request, debug, run, template, static_file

import datetime
import json
import urllib2

places = {
            'Dublin' : [53.3498, -6.2603,1],
            'Belfast' : [54.5973, -5.9301,1],
            'Cork' : [51.8969, -8.4863,1],
            'Athlone' : [53.4239, -7.9407,1],
            'Limerick' : [52.6680, -8.6305,1],
            'Galway' : [53.2707, -9.0568,1],
            'Waterford' : [52.2993, -7.1101,1],
            'Donegal' : [54.6538, -8.1096,1],
            'Armagh' : [54.3503, -6.6528,1],
            'Derry' : [54.9966, -7.3086,1],
            'Coleraine' : [55.1326, -6.6646,1],
            'Tralee' : [52.2713, -9.6999,1],
            'Sligo' : [54.2766, -8.4761,1]
         }

## def retrieve_places():
 ##connect = sqlite3.connect('forecast.db')
## cursor = connect.cursor()
## cursor.execute("SELECT location, latitude, longtitude FROM forecast2")
 ##result = cursor.fetchall()
 ##cursor.close()
 ##connect.close()

def url_builder(endpoint, lat, lon):
     user_api = 'd3a38f619180926cc586af94ac8766d1'
     unit = 'metric'  # For Fahrenheit use imperial, for Celsius use metric, and the default is Kelvin.
     mode = 'json'
     return 'http://api.openweathermap.org/' + 'data/2.5/'+ endpoint + \
           '?mode=' + mode + \
           '&units=' + unit + \
           '&APPID=' + user_api + \
           '&lat=' + str(lat) + \
           '&lon=' + str(lon)

def fetch_data(full_api_url):
    url = urllib2.urlopen(full_api_url)
    output = url.read().decode('utf-8')
    return json.loads(output)

def time_converter(timestamp):
    return datetime.datetime.fromtimestamp(timestamp).strftime('%d %b %I:%M %p')

def makeDropDown():
 global places
 selectStr = "<select name='location'>"
 for place in places:
  selectStr = selectStr + "<option value='" + \
 place + "'>" + place + "</option>"
 selectStr = selectStr + "</select>"
 return selectStr



def convertCoordinates(lat, lon):
    mapWidth, mapHeight = 540, 700
    leftLon, rightLon = -10.663, -5.428
    topLat, bottomLat = 55.384, 51.427
    lonRange = abs(leftLon - rightLon)
    latRange = abs(topLat - bottomLat)
    result = []
    result.append(int(round(abs(mapWidth * \
                ((abs(leftLon) - abs(lon)) / lonRange)))))
    result.append(int(round(abs(mapHeight * \
                ((abs(topLat) - abs(lat)) / latRange)))))
    return result


def getForecastData():
    global places
    connect = sqlite3.connect('forecast.db')
    cursor = connect.cursor()
    cursor.execute("DELETE FROM forecasts")
    #for place in location:
     #   places[place[1]] = [place[2], place[3], place [4]]
    for place in places:
        json_data = fetch_data(url_builder('forecast', \
                        places[place][0], places[place][1]))
        for forecast in json_data['list']:
            temperature = int(round(forecast['main']['temp'],0))
            symbol = forecast['weather'][0]['icon']
            timestamp = forecast['dt']
            cursor.execute("INSERT INTO forecasts (location, \
                            temperature, symbol, timestamp) \
                            VALUES (?, ?, ?, ?)", \
                            (place, temperature, symbol, timestamp))
    connect.commit()


    cursor.execute("SELECT DISTINCT timestamp FROM forecasts \
                    ORDER BY timestamp ASC")
   
    timestamps = cursor.fetchall()
    mapData = []
    timestampData = []
    for timestamp in timestamps:
        cursor.execute("SELECT * FROM forecasts \
                        WHERE timestamp = ?", (timestamp[0],))
        allLocationData = cursor.fetchall()
        singleMapData = []
        for locationData in allLocationData:
            place = locationData[1]
            symbol = locationData[3]
            imageCoords = convertCoordinates(places[place][0],\
                                            places[place][1])
            symbolURL = "http://openweathermap.org/img/w/" + \
                        symbol + ".png"
            singleMapData.append([imageCoords[0], \
                imageCoords[1], symbolURL, locationData[2], \
                place])
        mapData.append(singleMapData)
        timestampData.append(time_converter(timestamp[0]))
    cursor.close()
    connect.close()
    return mapData, timestampData

@route('/images/<filename>')
def send_image(filename):
    return static_file(filename, root='./images/')

@route('/')
@route('/<id>')
def showMap(id=0):
    global mapData, timestampData
    id = int(id)
    prev = id - 1 if id > 0 else id
    next = id + 1 if id < len(mapData)-1 else \
            len(mapData)-1
    return template('showWeatherMap.tpl', \
                    mapData = mapData[id], \
                    timestampData = timestampData[id], \
                    prev = prev, next = next)

mapData, timestampData = getForecastData()

@route('/manage')
def manage():
    global places    
    return template('manage.tpl', places = places)
#global places, mapData, timestampData
   # if request.forms.get("updateLocations"):
        #connect = sqlite3.connect('forecast.db')
        #cursor = connect.cursor()

debug(True)
run(reloader=True)