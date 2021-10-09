from flask import Flask,render_template ,request
import pickle
import pandas as pd
import numpy as np
import json
import plotly
import plotly.graph_objects as go
import plotly.express as px

app = Flask(__name__)

model = pickle.load(open('model_new.sav','rb'))

dataset = pd.read_csv("Cleaned_Dataset.csv")
dataset.dropna(inplace = True)
metal_name = ''
output = ""
fig = px.line(dataset, x='Date', y='Gold' , markers=  True)
graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

fig2 = px.line(dataset, x='Date', y='Silver',markers=  True)
graphJSON2 = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)

fig3 = px.line(dataset, x='Date', y='Platinum',markers=  True)
graphJSON3 = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)

@app.route('/')
def index():
    return render_template('landingpage.html')

@app.route('/home')
def home():
    global type_metal
    type_metal =list(dataset.columns)
    # type_metal.insert(0,'Select the Company')

    type_metal.remove("Unnamed: 0")
    type_metal.remove("Date")
    type_metal.remove("Year")
    type_metal.remove("Month")
    type_metal.remove("Copper")
    type_metal.remove("Tin")
    type_metal.remove("Zinc")
    type_metal.remove("Date.1")
    type_metal.insert(0,'Select the Company')
 
    global Year 
    Year = sorted((dataset['Year'].unique()))
    Year.append(2022.0)
    Year.insert(0,'Select the Year')
    print(type(Year))
    global Month 
    Month = sorted(dataset['Month'].unique())
    print(Month)
    metal_name = ""
    Month.insert(0,'Select the Month')
    output = 0
    print(metal_name , "Hello")
    return render_template("index2.html" ,MetalName = metal_name, Metals = type_metal, Year = Year , Month = Month, graphJSON=graphJSON,graphJSON3=graphJSON3,graphJSON2=graphJSON2 , prediction= output )
   

@app.route('/predict' , methods=['POST'])
def predict():
    Metal_s = request.form.get('Metal')
    global metal_name
    metal_name = str(Metal_s)
    print(Metal_s)
    Year_s = request.form.get('Year')
    print(Year)
    Month_s = request.form.get('Month')
    print(Month)
    mapping = {"Gold" : 0, "Silver":1 , "Platinum":2}
    empty_array = np.empty((0, 2), int)
    empty_array = np.append(empty_array, np.array([[Year_s,Month_s]]), axis=0)
    prediction = model.predict(empty_array)
    global output
    output = str(prediction[0][mapping[Metal_s]])
    return render_template("index2.html" ,MetalName = metal_name, Metals = type_metal, Year = Year , Month = Month, graphJSON=graphJSON,graphJSON3=graphJSON3,graphJSON2=graphJSON2 , prediction= output)




if __name__ == '__main__':
    app.run(debug=True)

