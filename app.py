from typing import List
from flask import Flask, render_template, request, flash, send_file, Response
import time
# import json to load JSON data to a python dictionary
import json
  
# urllib.request to make a request to api
import urllib.request
import requests
from urllib.error import URLError
  
app = Flask(__name__)



@app.route('/', methods =[ 'POST','GET'])
def weather():
    error = None
    if request.method == 'POST':
        city = request.form['city']
        if city == "":
            city = 'London'
    else:
        # for default name mathura
        city = 'London'
  
    # your API key will come here
    api = 'da67d9c34ac1b1b6d7bdb171d0a9fa17'
    url = 'https://api.openweathermap.org/data/2.5/weather?q=' + city + '&appid=' + api
    #city = city.replace()
    # source contain json data from api
    try:
        response = requests.get(url)
        source4 = response.json()
        print("status code:" + str(response.status_code))
        if response:
            print('Success!')
        elif 400 <= response.status_code <= 499:
            print('Client error.')
            return render_template('index.html', data = {"error":"City/Country not found."})
        elif 500 <= response.status_code <= 599:
            print("Server Error")
            return render_template('index.html', data = {"error":"The server couldn\'t fulfill the request."})
    except URLError as e:
        if hasattr(e, 'reason'):
            print('We failed to reach a server.')
            print('Reason: ', e.reason)
            return render_template('index.html', data = {"error":"We failed to reach a server."})
        elif hasattr(e, 'code'):
            print('The server couldn\'t fulfill the request.')
            print('Error code: ', e.code)
            return render_template('index.html', data = {"error":"The server couldn\'t fulfill the request."})
    else:   
        # converting JSON data to a dictionary
        print()
        lon, lat = str(source4['coord']['lon']), str(source4['coord']['lat'])
        url2 = 'https://api.openweathermap.org/data/2.5/onecall?lat='+ lat +'&lon='+lon+'&units=metric&exclude=current,minutely,hourly,alerts&appid=' + api
        list_of_data2 = requests.get(url2).json()
        data = {
            "country_code": str(source4['sys']['country']),
            "cityname":str(source4['name']),
            "weather":str(list_of_data2["daily"][0]['weather'][0]['description'])
            }
        for i in range(len(list_of_data2["daily"])):

                data["date" + str(i)] = str(time.strftime('%A, %d-%m-%Y', time.localtime(list_of_data2["daily"][i]['dt'])))
                data["day_temp" + str(i)]  = str(list_of_data2["daily"][i]['temp']['day'])
                data["night_temp" + str(i)] = str(list_of_data2["daily"][i]['temp']['night'])
                data["humidity" + str(i)] = str(list_of_data2["daily"][i]['humidity'])

        return render_template('index.html', data = data)


    
  
  
  
if __name__ == '__main__':
    app.run(debug = True)