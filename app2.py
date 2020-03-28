from flask import Flask, render_template, send_file
import os
import json
import xlwt
import ast
import pandas as pd
import Waze_Police_Scraper

app = Flask(__name__, static_folder='\\templates\\static')

def load():
    current_path = os.path.abspath(os.getcwd())
    f = open("data - its not the json data.txt", "r", encoding="utf-8")
    data_list = f.read()
    data_list = ast.literal_eval(data_list)
    return data_list, current_path

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
    data_list, current_path = load()
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
    data_list, current_path = load()
    if file_type == "json":
        file_name = "{}\\json\\POLICE {} {}.json".format(current_path, file_type.upper(), date)
        if directory_exist("json"):
            some_data = convert_data("json", data_list)
            f = open(file_name, "w+")
            f.write(str(some_data))
            f.close()
        else:
            os.mkdir("json")
            some_data = convert_data("json", data_list)
            f = open(file_name, "w+")
            f.write(str(some_data))
            f.close()
        return file_name, current_path
    elif file_type == "xls":
        file_name = '{}\\xls\\POLICE {} {}.xls'.format(current_path, file_type.upper(), date)
        if directory_exist("xls"):
            some_data = convert_data("xls", data_list)
            some_data.to_excel(file_name, index=True)
        else:
            os.mkdir("xls")
            some_data = convert_data("xls", data_list)
            some_data.to_excel(file_name, index=True)
        return file_name, current_path
    elif file_type == "csv":
        file_name = '{}\\csv\\POLICE {} {}.csv'.format(current_path, file_type.upper(), date)
        if directory_exist("csv"):
            some_data = convert_data("csv", data_list)
            pd.read_json(some_data).to_csv(file_name)
        else:
            os.mkdir("csv")
            some_data = convert_data("csv", data_list)
            pd.read_json(some_data).to_csv(file_name)
        return file_name, current_path


@app.route('/download/json')
def download_json():
    file_name, current_path = create_file("json")
    return """<div id="json"><h2>Downloaded {}</h2>
        <h2>Check {}</h2></div> <div class="main_page_button"><a href="/" target="_self"><button class='button_back'>Go Back</button></a></div> <style>#json {{text-align: center; color: #222; font-family: "Trebuchet MS"}} body {{background-image: url("https://i.ibb.co/6BKdvF0/Blur-2.png"); background-size: cover;}} .button_back {{color: #3854BD; background: transparent; border: 2px solid #3854BD; border-radius: 6px; padding: 16px 32px; text-align: center; font-size: 16px; margin: 4px 2px; transition-duration: 0.4s; cursor: pointer; text-decoration: none; -webkit-transition-duration: 0.4s; top:500px; position:absolute; right:1230px; top:170px;}} .buttons:hover {{background-color: #008CBA; color: white;}}</style>""".format(
        file_name.split("\\")[-1], current_path + "\\json")


@app.route('/download/xls')
def download_xls():
    file_name, current_path = create_file("xls")
    return """<div id="xls"><h2>Downloaded {}</h2>
        <h2>Check {}</h2></div> <div class="main_page_button"><a href="/" target="_self"><button class='button_back'>Go Back</button></a></div> <style>#xls {{text-align: center;, color: #222; font-family: "Trebuchet MS"}} body {{background-image: url("https://i.ibb.co/6BKdvF0/Blur-2.png"); background-size: cover;}} .button_back {{color: #3854BD; background: transparent; border: 2px solid #3854BD; border-radius: 6px; padding: 16px 32px; text-align: center; font-size: 16px; margin: 4px 2px; transition-duration: 0.4s; cursor: pointer; text-decoration: none; -webkit-transition-duration: 0.4s; top:500px; position:absolute; right:1230px; top:170px;}} .buttons:hover {{background-color: #008CBA; color: white;}}</style>""".format(
        file_name.split("\\")[-1], current_path + "\\xls")


@app.route('/download/csv')
def download_csv():
    file_name, current_path = create_file("csv")
    return """<div id="csv"><h2>Downloaded {}</h2>
        <h2>Check {}</h2></div> <div class="main_page_button"><a href="/" target="_self"><button class='button_back'>Go Back</button></a></div> <style>#csv {{text-align: center;, color: #222; font-family: "Trebuchet MS"}} body {{background-image: url("https://i.ibb.co/6BKdvF0/Blur-2.png"); background-size: cover;}} .button_back {{color: #3854BD; background: transparent; border: 2px solid #3854BD; border-radius: 6px; padding: 16px 32px; text-align: center; font-size: 16px; margin: 4px 2px; transition-duration: 0.4s; cursor: pointer; text-decoration: none; -webkit-transition-duration: 0.4s; top:500px; position:absolute; right:1230px; top:170px;}} .buttons:hover {{background-color: #008CBA; color: white;}}</style>""".format(
        file_name.split("\\")[-1], current_path + "\\csv")



if __name__ == "__main__":
    Waze_Police_Scraper.start_script()
    try:
        load()
        app.run()
    except KeyboardInterrupt:
        exit()