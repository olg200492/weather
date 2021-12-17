from typing import List
from flask import Flask, render_template, request
import time
  
# import json to load JSON data to a python dictionary
import json
  
# urllib.request to make a request to api
import urllib.request
  
  
app = Flask(__name__)
  
@app.route('/', methods =['POST', 'GET'])
def weather():
    if request.method == 'POST':
        city = request.form['city']
        if city == "":
            city = 'mathura'
    else:
        # for default name mathura
        city = 'mathura'
  
    # your API key will come here
    api = 'da67d9c34ac1b1b6d7bdb171d0a9fa17'
    #lot = json.loads(urllib.request.urlopen('http://api.openweathermap.org/geo/1.0/direct?q='+city+'&limit=5&appid='+api).read())
    #print(lot)
    #lat , lon = str(lot[0]['lat']), str(lot[0]['lon'])
    # source contain json data from api
    source1 = urllib.request.urlopen('https://api.openweathermap.org/data/2.5/weather?q=' + city + '&appid=' + api).read()
    # converting JSON data to a dictionary
    list_of_data = json.loads(source1)
    lon, lat = str(list_of_data['coord']['lon']), str(list_of_data['coord']['lat'])
    source2 = urllib.request.urlopen('https://api.openweathermap.org/data/2.5/onecall?lat='+ lat +'&lon='+lon+'&units=metric&exclude=current,minutely,hourly,alerts&appid=' + api).read()
    print('https://api.openweathermap.org/data/2.5/onecall?lat='+ lat +'&lon='+lon+'&units=metric&exclude=current,minutely,hourly,alerts&appid=' + api)
    list_of_data2 = json.loads(source2)
    data = {
        "country_code": str(list_of_data['sys']['country']),
        "cityname":str(list_of_data['name'])
        }
    for i in range(len(list_of_data2["daily"])):
        
            data["date" + str(i)] = str(time.strftime('%A, %d-%m-%Y', time.localtime(list_of_data2["daily"][i]['dt'])))
            data["day_temp" + str(i)]  = str(list_of_data2["daily"][i]['temp']['day'])
            data["night_temp" + str(i)] = str(list_of_data2["daily"][i]['temp']['night'])
            data["humidity" + str(i)] = str(list_of_data2["daily"][i]['humidity'])
            
    
    # data for variable list_of_data
    #data = {
    #    "country_code": str(list_of_data['sys']['country']),
    #    "cityname":str(list_of_data['name']),
    #    "temp_cel": str(list_of_data['main']['temp']) + ' C',
    #    "humidity": str(list_of_data['main']['humidity']),
    #}
    #print(data)
    return render_template('index.html', data = data)
  
  
  
if __name__ == '__main__':
    app.run(debug = True)