from django.shortcuts import render
from django.http import HttpResponse, FileResponse
import pandas as pd
import datetime
import os
import requests
import csv
import dotenv
from django.conf import settings
from cpquant.data import AlpacaDataClient


dotenv.load_dotenv()


def set_environment_variables(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                key, value = line.split(':', 1)
                #print(key)
                #print(value)
                os.environ[key] = value

# Specify the path to your environment variables file
env_file_path = 'vars.env'
set_environment_variables(env_file_path)

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

def about(request):
    return render(request, 'base/about.html')

def projects(request):
    return render(request, 'base/projects.html')

def contact(request):
    return render(request, 'base/contact.html')

def cpquant(request):
    return render(request, 'base/cpquant.html')

def startup_valuation(request):
    return render(request, 'base/startup-valuation.html')

def mts(request):
    return render(request, 'base/mts.html')

def submitb(request):
    print(request)
    if request.method == 'POST':
        data = request.POST
        stock = data.get('username')
        timeframe = data.get('password')
        start_ue = data.get('start')
        limit = data.get('limit')
        start = "20" + start_ue[-2:] + "-" + start_ue[0:2] + "-" + start_ue[3:5]

        client = AlpacaDataClient()
        bars = client.get_bars([ticker for ticker in stock.split(",")], timeframe, start, None, "raw", limit)
        for ticker in bars:
            df = bars[ticker]
            df.to_csv(ticker + ".csv")
            data = open(ticker + '.csv','r').read()
            print(data)
            resp = HttpResponse(data)
            os.remove(ticker + '.csv')
            resp['Content-Disposition'] = 'attachment;filename=' + ticker + '.csv'
            return resp
        
def submitt(request):
    print(request.POST)
    if request.method == 'POST':
        data = request.POST
        stock = data.get('username')
        start_ue = data.get('start')
        limit = data.get('limit')
        start = "20" + start_ue[-2:] + "-" + start_ue[0:2] + "-" + start_ue[3:5]

        client = AlpacaDataClient()
        trades = client.get_trades([ticker for ticker in stock.split(",")], start, None, limit)
        for ticker in trades:
            df = trades[ticker]
            df.to_csv(ticker + ".csv")
            data = open(ticker + '.csv','r').read()
            print(data)
            resp = HttpResponse(data)
            os.remove(ticker + '.csv')
            resp['Content-Disposition'] = 'attachment;filename=' + ticker + '.csv'
            return resp