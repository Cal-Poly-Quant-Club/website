from django.shortcuts import render
from django.http import HttpResponse, FileResponse
import datetime
import os
import requests
import csv

# Create your views here.

def base(request):
    return render(request, 'base/base.html')


def page1(request):
    return render(request, 'base/page1.html')

def page2(request):
    context = {}
    context['hello'] = 'Hello World!'
    return render(request, 'base/page2.html', context)

def get_data(request):
    return render(request, 'base/get_data.html')

def trades(request):
    return render(request, 'base/trades.html')

def bars(request):
    return render(request, 'base/bars.html')

def submitb(request):
    if request.method == 'POST':
        stock = request.form.get('username')
        timeframe = request.form.get('password')
        start_ue = request.form.get('start')
        limit = request.form.get('limit')
    
        base_url = "https://data.alpaca.markets/v2/stocks/bars?symbols="

        st_list = stock.split(",")
        for st in st_list:
            for i in range(len(st) - 1):
                print(f"st: {st}, i: {i}")
                if st[i] == " ":
                    if i == 0:
                        st = st[1:]
                    elif i == (len(st) - 1):
                        st = st[0:-1]
                    else:
                        print("Invalid input.")
                        raise(ValueError)
            base_url = base_url + st + "%2C"
        base_url = base_url[0:-3]

        monday = datetime.datetime(2023, 7, 3)
        days = {
            0: "Monday",
            1: "Tuesday",
            2: "Wednesday",
            3: "Thursday",
            4: "Friday",
            5: "Saturday",
            6: "Sunday"
        }
        today = datetime.datetime.now()
        yesterday = today - datetime.timedelta(days=1)
        diff = today - monday
        dotw_val = diff.days % 7
        dotw = days[dotw_val]
        print(dotw)
        if dotw == "Saturday":
            today = today - datetime.timedelta(days=1)
            yesterday = today - datetime.timedelta(days=1)
        elif dotw == "Sunday":
            today = today - datetime.timedelta(days=2)
            yesterday = today - datetime.timedelta(days=1)

        if timeframe[-1] != 'T' and timeframe[-1] != 'M' and timeframe[-1] != 'W' and timeframe[-1] != 'H' and timeframe[-1] != 'D':
            return render(request, "base/invalid_tf.html")
        else:
            base_url += "&timeframe=" + timeframe

        csv_file_path = "./prices.csv"
        file = open(csv_file_path, mode="r+", newline="")
        file.truncate(0)
        csv_writer = csv.writer(file)
        #start = "2017-01-03T00%3A00%3A00Z"
        start = "20" + start_ue[-2:] + "-" + start_ue[0:2] + "-" + start_ue[3:5] + "T00%3A00%3A00Z"
        end = today.strftime("%Y-%m-%dT%H%%3A%M%%3A%SZ")
        print(start)
        print(end)
        if int(limit) <= 10000:
            end_url = "&limit=" + limit
        else:
            end_url = "&limit=" + str(10000)
        full_url = base_url + "&start=" + start + "&end=" + end + end_url
        print(full_url)

        j = 0
        while j < int(limit):

            secret_key = os.environ.get("ALPACA_DATA_SECRET_KEY")
            print(secret_key)
            public_key = os.environ.get("ALPACA_DATA_PUBLIC_KEY")
            print("pk" + public_key)
            
            headers = {
                #"accept": "application/json",
                "APCA-API-KEY-ID": public_key,
                "APCA-API-SECRET-KEY": secret_key
            }

            response = requests.get(full_url, headers=headers)
            content = response.text
            if content[12:29] == "invalid timeframe":
                return render(request, "bars/invalid_tf.html")
            print(content)

            
            
            temp_pair = []
            first_time = start
            i = 0
            while i < len(content) - 2:
                print(content[i])
                if content[i] == '"':
                    if content[i+1] == 't':
                        i += 5
                        temp_time = ""
                        while content[i] != ',':
                            temp_time += content[i]
                            i += 1
                        temp_pair.append(temp_time)
                        first_time = temp_time
                    elif content[i+1] == 'c':
                        i += 4
                        temp_price = ""
                        while content[i] != ',':
                            temp_price += content[i]
                            i += 1
                        temp_pair.append(temp_price)
                        print(temp_pair)
                        csv_writer.writerow(temp_pair)
                        temp_pair = []
                    
                i += 1
            print(full_url)
            if not first_time == None:
                #print("FINAL TIME " + first_time)
                k = 0
                while k < (len(first_time) - 1):
                    print(first_time[k])
                    if first_time[k] == ':':
                        first_time = first_time[:k] + "%3A" + first_time[k+1:]
                        k += 3
                    elif first_time[k] == '.':
                        print("DECIMAL")
                        first_time = first_time[:k] + "Z"
                        k = len(first_time) - 1
                    else:
                        k += 1
                #print("first TIME " + first_time)
                start = first_time
                if int(limit) <= 10000:
                    end_url = "&limit=" + limit
                else:
                    end_url = "&limit=" + str(10000)
                full_url = base_url + "&start=" + start + "&end=" + end + end_url
            print(full_url)
            j += 10000
        file.close()
        response = FileResponse(csv_file_path)
        return response