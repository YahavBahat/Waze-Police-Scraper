from flask import Flask, render_template, send_file
import os
import json
import xlwt
import ast
import pandas as pd

app = Flask(__name__, static_folder='\\templates\\static')

f = open("C:\\Users\\Yahav Bahat\\Downloads\\ghgh.txt", "r", encoding="utf-8")
data_list = f.read()
data_list = ast.literal_eval(data_list)

file_types = ("json", "xls", "csv")

@app.route('/r')
def get_file_date():  # read config
    f = open("config.config", "r")
    date = f.read()
    date = date.replace(":", ";")  # Special characters in windows
    return date
    

@app.route('/')
def hello():
    return render_template('iframe.html')


@app.route('/map.html')
def main():
    return render_template('map.html')


@app.route('/GitHub-Mark-120px-plus.png')
def picture():
    return send_file("templates\\static\\images\\GitHub-Mark-120px-plus.png")


def directory_exist(file_type):
    return os.path.isdir('./{}'.format(file_type))


def convert_data(file_type, data_list):
    if file_type == "json":
        return data_list
    elif file_type == "xls":
        data = data_list[0]
        data = json.dumps(data)
        df = pd.read_json(data)
        return df
    elif file_type == "csv":
        data = data_list[0]
        data = json.dumps(data)
        return data


def create_file(file_type):
    date = get_file_date()
    if file_type == "json":
        file_name = "{}\\POLICE {} {}.json".format(file_type, file_type.upper(), date)
        some_data = convert_data("json", data_list)
        f = open(file_name, "w+")
        f.write(str(some_data))
        f.close()
        return file_name
    elif file_type == "xls":
        file_name = '{}\\POLICE {} {}.xls'.format(file_type, file_type.upper(), date)
        some_data = convert_data("xls", data_list)
        some_data.to_excel(file_name, index=True)
        return file_name
    elif file_type == "csv":
        file_name = '{}\\POLICE {} {}.csv'.format(file_type, file_type.upper(), date)
        some_data = convert_data("csv", data_list)
        pd.read_json(some_data).to_csv(file_name)
        return file_name


@app.route('/download/json')
def download_json():
    if directory_exist(file_types[0]):  # returns True, than directory exist
        file_name = create_file("json")
    else:
        os.mkdir("json")
        file_name = create_file("json")
    return """<div id="json"><h2>Downloaded {}</h2>
        <h2>Check Waze_Police_Scraper\{}</h2></div> <div class="main_page_button"><a href="/" target="_self"><button class='button_back'>Go Back</button></a></div> <style>#json {{text-align: center; color: #222; font-family: "Trebuchet MS"}} body {{background-image: url("https://i.ibb.co/6BKdvF0/Blur-2.png"); background-size: cover;}} .button_back {{color: #3854BD; background: transparent; border: 2px solid #3854BD; border-radius: 6px; padding: 16px 32px; text-align: center; font-size: 16px; margin: 4px 2px; transition-duration: 0.4s; cursor: pointer; text-decoration: none; -webkit-transition-duration: 0.4s; top:500px; position:absolute; right:1230px; top:170px;}} .buttons:hover {{background-color: #008CBA; color: white;}}</style>""".format(
        file_name, file_name.split(".")[1])


@app.route('/download/xls')
def download_xls():
    if directory_exist(file_types[1]):
        file_name = create_file("xls")
    else:
        os.mkdir("xls")
        file_name = create_file("xls")
    return """<div id="xls"><h2>Downloaded {}</h2>
        <h2>Check Waze_Police_Scraper\{}</h2></div> <div class="main_page_button"><a href="/" target="_self"><button class='button_back'>Go Back</button></a></div> <style>#xls {{text-align: center;, color: #222; font-family: "Trebuchet MS"}} body {{background-image: url("https://i.ibb.co/6BKdvF0/Blur-2.png"); background-size: cover;}} .button_back {{color: #3854BD; background: transparent; border: 2px solid #3854BD; border-radius: 6px; padding: 16px 32px; text-align: center; font-size: 16px; margin: 4px 2px; transition-duration: 0.4s; cursor: pointer; text-decoration: none; -webkit-transition-duration: 0.4s; top:500px; position:absolute; right:1230px; top:170px;}} .buttons:hover {{background-color: #008CBA; color: white;}}</style>""".format(
        file_name, file_name.split(".")[1])


@app.route('/download/csv')
def download_csv():
    if directory_exist(file_types[2]):
        file_name = create_file("csv")
    else:
        os.mkdir("csv")
        file_name = create_file("csv")
    return """<div id="csv"><h2>Downloaded {}</h2>
        <h2>Check Waze_Police_Scraper\{}</h2></div> <div class="main_page_button"><a href="/" target="_self"><button class='button_back'>Go Back</button></a></div> <style>#csv {{text-align: center;, color: #222; font-family: "Trebuchet MS"}} body {{background-image: url("https://i.ibb.co/6BKdvF0/Blur-2.png"); background-size: cover;}} .button_back {{color: #3854BD; background: transparent; border: 2px solid #3854BD; border-radius: 6px; padding: 16px 32px; text-align: center; font-size: 16px; margin: 4px 2px; transition-duration: 0.4s; cursor: pointer; text-decoration: none; -webkit-transition-duration: 0.4s; top:500px; position:absolute; right:1230px; top:170px;}} .buttons:hover {{background-color: #008CBA; color: white;}}</style>""".format(
        file_name, file_name.split(".")[1])



if __name__ == "__main__":
    Waze_Police_Scraper.start_script()
    try:
        app.run()
    except KeyboardInterrupt:
        exit()

