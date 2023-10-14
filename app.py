from flask import Flask, request, render_template, send_file
import datetime
import os
import requests
import csv

app = Flask(__name__, static_url_path='', 
            static_folder='static', template_folder='templates')

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

@app.route('/')
def home():
    return render_template('./gui.html')

@app.route('/get_data', methods = ['GET'])
def get_data():
    return render_template('./data_form.html')

@app.route('/about', methods = ['GET'])
def about():
    return render_template('./about.html')

@app.route('/contact')
def contact():
    return render_template('./contact.html')

@app.route('/projects')
def projects():
    return render_template('./projects.html')

@app.route('/download', methods=['POST'])
def submit():
    if request.method == 'POST':
        stock = request.form.get('username')
        timeframe = request.form.get('password')
        limit = request.form.get('limit')
        print(stock)
        print(timeframe)
        print(limit)

        if int(limit) > 10000:
            limit = 10000

        base_url = "https://data.alpaca.markets/v2/stocks/trades?symbols="
        end_url = "&limit=" + limit

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


        tf_value = 0
        if timeframe == "T":
            tf_value = input("How many minutes? (1-59)")
        elif timeframe == "H":
            tf_value = input("How many hours? (1-23))")
        elif timeframe == "M":
            tf_value = input("How many months? (1,2,3,4,6,12)") 


        if tf_value == 0:
            tf_value = 1
        tf_url += str(tf_value) + timeframe 

        start = yesterday.strftime("%Y-%m-%dT%H%%3A%M%%3A%SZ")
        end = today.strftime("%Y-%m-%dT%H%%3A%M%%3A%SZ")
        print(start)
        print(end)
        base_url = base_url + "&start=" + start + "&end=" + end + end_url
        print(base_url)

        secret_key = os.environ.get("ALPACA_DATA_SECRET_KEY")
        print(secret_key)
        public_key = os.environ.get("ALPACA_DATA_PUBLIC_KEY")
        print("pk" + public_key)
        
        headers = {
            #"accept": "application/json",
            "APCA-API-KEY-ID": public_key,
            "APCA-API-SECRET-KEY": secret_key
        }

        response = requests.get(base_url, headers=headers)
        content = response.text
        print(content)
        csv_file_path = "./prices.csv"

        file = open(csv_file_path, mode="r+", newline="")
        csv_writer = csv.writer(file)

        temp_pair = []
        i = 0
        while i < len(content) - 2:
            #print(content[i])
            if content[i] == '"':
                if content[i+1] == 't':
                    i += 5
                    temp_time = ""
                    while content[i] != ',':
                        temp_time += content[i]
                        i += 1
                    temp_pair.append(temp_time)
                elif content[i+1] == 'p':
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

            #file.close()
        file.close()
        return send_file(csv_file_path, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)