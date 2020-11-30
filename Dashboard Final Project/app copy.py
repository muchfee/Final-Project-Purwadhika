from flask import Flask, render_template, jsonify, request,url_for
import joblib
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import json
from flask_material import Material

app = Flask(__name__)
Material(app)
# home route
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/dataset')
def dataset():
    df = pd.read_csv('Data_Dashboard')
    return render_template('dataset.html',df_view = df.head(100))

@app.route('/graphic')
def graphic():
    return render_template('graphic.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if request.method == 'POST':
        T1 = request.form['t1'] 
        T2 = request.form['t2']
        Humidity = request.form['hum']
        wind_speed = request.form['wind_speed']
        weather_code = request.form['weather_code']
        Month = request.form['month']
        Day = request.form['day']
        Hour = request.form['hour']

        Hour = int(Hour)
        T1 = float(T1)
        T2  = float(T2)
        wind_speed = float(wind_speed)
        Humidity = float(Humidity)


        data = {            
            't1' : T1,
            't2' : T2,
            'hum' : Humidity,
            'wind_speed' : wind_speed,
            'weather_code': weather_code,
            'month' : Month,
            'day' : Day,
            'hour' : Hour,

        }


    df_predict = pd.DataFrame(data = data, index=[1])
    model = joblib.load('RandomForest Bikeshares Predictor')
    prediction = model.predict(df_predict)
    predict = round(prediction[0],0)
    print(prediction)

    return render_template('index.html', t1 =T1,t2= T2, hum= Humidity,
                wind_speed=wind_speed,
                weather_code=weather_code,
                month= Month,
                day=Day,
                hour=Hour,
                predict=predict)
    

    
if __name__ == "__main__":
    app.run(debug=True)
