import sqlite3
import requests
from flask import Flask, request,render_template
from datetime import date
from wtforms import Form, BooleanField, StringField, PasswordField, validators
import pandas as pd


app = Flask(__name__)

conn = sqlite3.connect("weatherlocation.db",check_same_thread=False)
cur = conn.cursor()
class Firstapp:
    def sql_query(zipcode,temperature,maximum_temperature,minimum_temperature,result,humidity,wind_speed,feels_like):
        try:
            today = date.today()
            in_date = today.strftime("%d/%m/%Y")
            cur.execute(f"INSERT INTO CurrentWeather (ZIPCODE,temp,maxtemp,temp_min,description,humidity,wind_speed,feels_like,date) VALUES('{zipcode}','{temperature}','{maximum_temperature}','{minimum_temperature}','{result}',{humidity},{wind_speed},{feels_like},'{in_date}');")
            conn.commit()
            return render_template('home.html')    
        except :
            print("error in query function")
            return render_template("home.html")


    @app.route("/operation", methods=['POST','GET'])
    def operation():
        try:            
            if request.method == "POST":
                task = request.form.get("operation", None)
                if task == "create":
                    return render_template("create.html")
                elif task == "insert":
                    return render_template("insert.html")
                elif task == "update":
                    return render_template("update.html")
                elif task=='delete':
                    return render_template("delete.html")
                else:
                    return render_template("apicall.html")
            return render_template("home.html")
        except:
            print("error in operation function")
            return render_template("home.html")


    @app.route("/create", methods=['POST','GET'])
    def create():
        try:
            zipcode = request.form.get('zipcode')
            city = request.form.get('City')
            state = request.form.get('State')
            zipcode_df = pd.read_sql_query("SELECT ZIPCODE FROM Weather",conn)
            print(zipcode_list)
            conn.commit()
            if zipcode in zipcode_list:
                message = "zipcode already exists, create new one "
            else:
                cur.execute(f"INSERT INTO weather (ZIPCODE,CITY,STATE) VALUES ('{zipcode}','{city}','{state}')")
                conn.commit()
                message ="entered data into database successfully" 
            return render_template("home.html",message = message)
        except:
            print("error in creating function")
            return render_template("home.html")

    @app.route("/delete", methods=['POST','GET'])
    def delete():
        try:
            zipcode = request.form.get('zipcode')
            zipcode_list = cur.execute("SELECT ZIPCODE FROM Weather")
            conn.commit()
            if zipcode in zipcode_list:
                cur.execute(f"DELETE FROM weather where ZIPCODE='{zipcode}'")
                conn.commit()
            else:
                print("zipcode doesnot exists, enter valid zipcode")
            return render_template("home.html")
        except:
            print("error in create function")
            return render_template("home.html")

    @app.route("/update", methods=['POST','GET'])
    def update():
        try:
            zipcode = request.form.get('zipcode')
            zipcode_list = cur.execute("SELECT ZIPCODE FROM Weather")
            conn.commit()
            if zipcode in zipcode_list:
                cur.execute(f"UPDATE weather SET ZIPCODE = '{zipcode}',CITY = '{city}',STATE ='{state}' where ZIPCODE='{zipcode}'")
                conn.commit()
                message = "update successful"
            else:
                message = "zipcode doesn't exists, enter valid zipcode to update(cannot change zipcode)"
            return render_template("home.html",message= message)
        except:
            print("error in create function")
            return render_template("home.html")

    @app.route('/')
    def home():
        return render_template("register.html",message ="Register Here")

    @app.route('/weather')
    def weather_city():
        try:
            API_key = 'b4012066f7bd668f5dbeef89d3f61fa1'
            zipcode_list = cur.execute("SELECT ZIPCODE FROM Weather")
            conn.commit()
            for zipcode in zipcode_list:
                url = f'http://api.openweathermap.org/data/2.5/weather?zip={zipcode},us&appid={API_key}'
                print(url)
                response = requests.get(url).json()
                forecast = response.get("weather",{})
                for i in forecast:
                    result = i['description']
                temperature = response.get('main', {}).get('temp')
                minimum_temperature = response.get('main',{}).get('temp_min')
                maximum_temperature = response.get('main',{}).get('temp_max')
                humidity = response.get('main',{}).get('humidity')
                wind_speed = response.get('wind',{}).get('speed')
                feels_like = response.get('main',{}).get('feels_like')
            return Firstapp.sql_query(zipcode=zipcode,temperature=temperature,maximum_temperature=maximum_temperature,minimum_temperature=minimum_temperature,result=result,humidity=humidity,wind_speed=wind_speed,feels_like=feels_like)
        except:
            print("error in api function")

    @app.route('/login', methods=['POST', 'GET'])
    def login():
        try:
            if request.method == 'POST':
                # access the data inside 
                username = request.form.get('username') 
                password = request.form.get('password')    
                df = pd.read_sql(f"SELECT username,password FROM login where username='{username}' and password = '{password}'",conn)
                print(df)
                conn.commit()
                if df is not None:
                    message = "Login Successful"
                    return render_template('home.html', message=message)
        except Exception as e:     
            message =  "Wrong username or password"
            print(e)
            return render_template('login.html', message=message)
 
    @app.route("/register", methods=['POST','GET'])
    def register():
        try:
            method = request.form.get('login')
            print(method)
            if method == 'Login':
                message ="Fill the details above"
                return render_template("login.html",message = message)
            else:
                username = request.form.get('username')
                password = request.form.get('password')

                
                df = pd.read_sql_query(f"SELECT * FROM login where username='{username}'",con=conn)
                print(df)

                if df is not None:
                    message = "username already exists, create new one "
                    return render_template("register.html",message = message)
                else:
                    cur.execute(f"INSERT INTO login (username,password) VALUES ('{username}','{password}')")
                    conn.commit() 
                    message = "registeration successful"
                    return render_template("login.html",message = message)
        except Exception as e:
            message ="error in registering"
            return render_template("register.html",message = e)


if __name__ == '__main__':
    app.run(debug=True)



