"""External Captive Portal Web Server."""
import boto3
import requests
import json
import time as Time
from flask_cors import CORS
from boto3.dynamodb.conditions import Key, Attr
import pandas as pd
import plotly
import plotly.express as px
from flask import Flask, redirect, render_template, request, url_for


# Module Variables
global base_grant_url
global user_continue_url
global success_url


base_grant_url = "https://captive-portal.cxamerakidemo.io/index"
user_continue_url = "https://captive-portal.cxamerakidemo.io/success"
success_url = "https://captive-portal.cxamerakidemo.io/log"


app = Flask(__name__)
CORS(app, resources=r'/agenda/*')

# Flask micro-webservice URI endpoints
@app.route("/index", methods=["GET"])
def get_click():
    """Process GET requests to the /index URI; render the index.html page."""
    global base_grant_url
    global user_continue_url
    global success_url
    
    host = request.host_url
    base_grant_url = request.args.get('base_grant_url')
    user_continue_url = request.args.get('user_continue_url')
    node_mac = request.args.get('node_mac')
    client_ip = request.args.get('client_ip')
    client_mac = request.args.get('client_mac')
    success_url = host + "success"


    return render_template(
        "index.html",
        client_ip=client_ip,
        client_mac=client_mac,
        node_mac=node_mac,
        user_continue_url=user_continue_url,
        success_url=success_url,
    )


@app.route("/login", methods=["POST"])
def get_login():
    """Process POST requests to the /login URI; redirect to grant URL."""

    redirect_url = base_grant_url + '?continue_url=' + success_url
    #print(redirect_url)
    return redirect(redirect_url, code=302) # codigo 302 = page found 


@app.route("/success", methods=["GET"])
def get_success():
    """Process GET requests to the /success URI; render success.html."""
    global user_continue_url

    return render_template(
        "success.html",
        client_ip=client_ip,
        client_mac=client_mac,
        node_mac=node_mac,
        user_continue_url=user_continue_url,
        success_url=success_url,
    )

"""
@app.route("/log", methods=["GET","POST"])
def get_data():
    #Send data of the connected user to the template log.html
   
    return render_template("log.html")
"""



@app.route("/signup", methods=["GET","POST"])
def get_signup():
    """Process GET requests to the /signup URI; render the signup.html page."""
    global base_grant_url
    global user_continue_url
    global success_url
    
    host = request.host_url
    base_grant_url = request.args.get('base_grant_url')
    user_continue_url = request.args.get('user_continue_url')
    node_mac = request.args.get('node_mac')
    client_ip = request.args.get('client_ip')
    client_mac = request.args.get('client_mac')
    success_url = host + "success"


    return render_template(
        "signup.html",
        client_ip=client_ip,
        client_mac=client_mac,
        node_mac=node_mac,
        user_continue_url=user_continue_url,
        success_url=success_url,
    )


@app.route("/code", methods=["GET","POST"])
def get_code():
    
    return render_template("code.html")


@app.route("/log", methods=["POST", "GET"])
def get_cita():
    #Send data of the connected user to the template log.html
  
    return render_template("log.html")


"""
#-------si funciona!
@app.route("/cita", methods=["POST", "GET"])
def get_cita_usr():
    #Send data of the connected user to the template log.html
    
    if request.method == "POST":
        results = request.form
        name = request.form["name"]
        name_ap = request.form["name_ap"]
        name_am = request.form["name_am"]
        email = request.form["user_email_address"]
        doctor = request.form["doctor"]
        fecha = request.form["date"]

        TABLE_NAME = 'portal-login'
        #connects with dynamodb instance and insert form data
        dynamodb_client = boto3.client('dynamodb',
        region_name="us-east-1")
        dynamodb = boto3.resource('dynamodb', region_name="us-east-1")

        table = dynamodb.Table(TABLE_NAME)

        table.put_item(
            Item={
                "name": name,
                "name_ap": name_ap,
                "name_am": name_am,
                "email": email,
                "doctor": doctor,
                "fecha": fecha,
                "user-id": email
            }
        )
        return redirect("/cita", code=302)


    TABLE_NAME = "portal-login"

    dynamodb_client = boto3.client('dynamodb',
    region_name="us-east-1")
    dynamodb = boto3.resource('dynamodb', region_name="us-east-1")

    table = dynamodb.Table(TABLE_NAME)
    #response = table.scan()
    
    response = table.query(
        KeyConditionExpression=Key('user-id').eq('tania_v_z@hotmail.com')
    )
    

    return render_template("cita.html", data=response)





@app.route("/cita", methods=["POST", "GET"])
def get_cita_usr():
    #Send data of the connected user to the template log.html
    
    #if request.method == "POST":
    results = request.form
    name = request.form["name"]
    name_ap = request.form["name_ap"]
    name_am = request.form["name_am"]
    email = request.form["user_email_address"]
    doctor = request.form["doctor"]
    fecha = request.form["date"]

    TABLE_NAME = 'portal-login'
    #connects with dynamodb instance and insert form data
    dynamodb_client = boto3.client('dynamodb',
    region_name="us-east-1")
    dynamodb = boto3.resource('dynamodb', region_name="us-east-1")

    table = dynamodb.Table(TABLE_NAME)

    table.put_item(
        Item={
            "name": name,
            "name_ap": name_ap,
            "name_am": name_am,
            "email": email,
            "doctor": doctor,
            "fecha": fecha,
            "user-id": email
        }
    )
    #return redirect("/cita", code=302)


    TABLE_NAME = "portal-login"

    dynamodb_client = boto3.client('dynamodb',
    region_name="us-east-1")
    dynamodb = boto3.resource('dynamodb', region_name="us-east-1")

    table = dynamodb.Table(TABLE_NAME)
    #response = table.scan()
    
    response = table.query(
        KeyConditionExpression=Key('user-id').eq(email)
    )
    

    return render_template("cita.html", data=response)


@app.route("/cita", methods=["POST", "GET"])
def get_cita_usr():
    #Send data of the connected user to the template log.html
    
    #if request.method == "POST":
    unique_key = str(Time.time())
    results = request.form
    name = request.form["name"]
    name_ap = request.form["name_ap"]
    name_am = request.form["name_am"]
    email = request.form["user_email_address"]
    doctor = request.form["doctor"]
    motive = request.form["motive"]
    fecha = request.form["date"]
    time = str(request.form["time"])

    TABLE_NAME = 'portal-login'
    #connects with dynamodb instance and insert form data
    dynamodb_client = boto3.client('dynamodb',
    region_name="us-east-1")
    dynamodb = boto3.resource('dynamodb', region_name="us-east-1")

    table = dynamodb.Table(TABLE_NAME)

    table.put_item(
        Item={
            "name": name,
            "name_ap": name_ap,
            "name_am": name_am,
            "email": email,
            "doctor": doctor,
            "fecha": fecha,
            "motive": motive,
            "time": time,
            "user-id": unique_key
        }
    )
    #return redirect("/cita", code=302)


    TABLE_NAME = "portal-login"

    dynamodb_client = boto3.client('dynamodb',
    region_name="us-east-1")
    dynamodb = boto3.resource('dynamodb', region_name="us-east-1")

    table = dynamodb.Table(TABLE_NAME)
    response = table.scan()

    return render_template("cita.html", data=response)
"""

"""
@app.route("/cita", methods=["POST", "GET"])
def get_cita_usr():
    #Send data of the connected user to the template log.html
    
    #if request.method == "POST":
    unique_key = str(Time.time())
    results = request.form
    name = request.form["name"]
    name_ap = request.form["name_ap"]
    name_am = request.form["name_am"]
    email = request.form["user_email_address"]
    doctor = request.form["doctor"]
    motive = request.form["motive"]
    fecha = request.form["date"]
    time = str(request.form["time"])

    TABLE_NAME = 'Appointment_Info'
    #connects with dynamodb instance and insert form data
    dynamodb_client = boto3.client('dynamodb',
    region_name="us-east-2")
    dynamodb = boto3.resource('dynamodb', region_name="us-east-2")

    table = dynamodb.Table(TABLE_NAME)

    table.put_item(
        Item={
            "date": fecha,
            "doctor_email": "officialbcm@gmail.com",
            "index": unique_key,
            "patient_email": email,
            "patient_f_surname": name_ap,
            "patient_name": name,
            "patient_s_surname": name_am,
            "patient_symptoms": motive,
            "time": time
        }
    )
    #api call to show patient information
    #redirect("/cita", code=302)
    response = api_call(email)
    return render_template("cita.html", data=response)

@app.route("/cita", methods=["GET"])
def api_call(email):
    url = "https://po7yuq5dw8.execute-api.us-east-1.amazonaws.com/Prod/paciente?email=" + email
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    #print(response.text)
    return response

"""

"""

@app.route("/cita", methods=["POST", "GET"])
def get_cita_usr():
    #Send data of the connected user to the template log.html
  
    if request.method == "POST":
        unique_key = str(Time.time())
        results = request.form
        name = request.form["name"]
        name_ap = request.form["name_ap"]
        name_am = request.form["name_am"]
        email = request.form["user_email_address"]
        doctor = request.form["doctor"]
        motive = request.form["motive"]
        fecha = request.form["date"]
        time = str(request.form["time"])

        TABLE_NAME = 'Appointment_Info'
        #connects with dynamodb instance and insert form data
        dynamodb_client = boto3.client('dynamodb',
        region_name="us-east-2")
        dynamodb = boto3.resource('dynamodb', region_name="us-east-2")
        table = dynamodb.Table(TABLE_NAME)
        table.put_item(
            Item={
                "date": fecha,
                "doctor_email": "officialbcm@gmail.com",
                "index": unique_key,
                "patient_email": email,
                "patient_f_surname": name_ap,
                "patient_name": name,
                "patient_s_surname": name_am,
                "patient_symptoms": motive,
                "time": time
            }
        )
        return redirect(url_for('api_call', correo = email))

    else:
        return render_template("log.html")
 
"""
"""
@app.route("/cita", methods=["POST", "GET"])
def get_cita_usr():
    #Send data of the connected user to the template log.html
  
    #if request.method == "POST":
    unique_key = str(Time.time())
    results = request.form
    name = request.form["name"]
    name_ap = request.form["name_ap"]
    name_am = request.form["name_am"]
    email = request.form["user_email_address"]
    doctor = request.form["doctor"]
    motive = request.form["motive"]
    fecha = request.form["date"]
    time = str(request.form["time"])

    TABLE_NAME = 'Appointment_Info'
    #connects with dynamodb instance and insert form data
    dynamodb_client = boto3.client('dynamodb',
    region_name="us-east-2")
    dynamodb = boto3.resource('dynamodb', region_name="us-east-2")
    table = dynamodb.Table(TABLE_NAME)
    table.put_item(
        Item={
            "date": fecha,
            "doctor_email": "officialbcm@gmail.com",
            "index": unique_key,
            "patient_email": email,
            "patient_f_surname": name_ap,
            "patient_name": name,
            "patient_s_surname": name_am,
            "patient_symptoms": motive,
            "time": time
        }
    )
    return redirect(url_for('api_call',correo = email))
    #else:
    #return render_template("log.html")

"""

@app.route("/cita", methods=["POST", "GET"])
def get_cita_usr():
    #Send data of the connected user to the template log.html
    print("sbvdncbjnf svbn jdv nmsdjnvm, cjmn ,sgvfcxjmn ,dsfvcxnjmk ,jdenhfmvs ,cdfeknjmlsvc ,")
    if request.method == "POST":
        unique_key = str(Time.time())

        name = request.form["name"]
        name_ap = request.form["name_ap"]
        name_am = request.form["name_am"]
        email = request.form["user_email_address"]
        doctor = request.form["doctor"]
        motive = request.form["motive"]
        fecha = request.form["date"]
        time = str(request.form["time"])
        Item={
                "date": fecha,
                "doctor_email": "officialbcm@gmail.com",
                "index": unique_key,
                "patient_email": email,
                "patient_f_surname": name_ap,
                "patient_name": name,
                "patient_s_surname": name_am,
                "patient_symptoms": motive,
                "time": time
            }
        print(Item)
        TABLE_NAME = 'Appointment_Info'
        #connects with dynamodb instance and insert form data
        dynamodb_client = boto3.client('dynamodb',
        region_name="us-east-2")
        dynamodb = boto3.resource('dynamodb', region_name="us-east-2")
        table = dynamodb.Table(TABLE_NAME)
        table.put_item(
            Item=Item
        )
        return redirect(url_for('api_call',correo = email))
    else:
        unique_key = str(Time.time())

        name = request.args.get("name")
        name_ap = request.args.get("name_ap")
        name_am = request.args.get("name_am")

        #email = request.args.get("user_email_address")
        email="tania@test.com"
        doctor = request.args.get("doctor")
        motive = request.args.get("motive")
        fecha = request.args.get("date")
        time = str(request.args.get("time"))
        Item={
                "date": fecha,
                "doctor_email": "officialbcm@gmail.com",
                "index": unique_key,
                "patient_email": email,
                "patient_f_surname": name_ap,
                "patient_name": name,
                "patient_s_surname": name_am,
                "patient_symptoms": motive,
                "time": time
            }
        print(Item)
        TABLE_NAME = 'Appointment_Info'
        #connects with dynamodb instance and insert form data
        dynamodb_client = boto3.client('dynamodb',
        region_name="us-east-2")
        dynamodb = boto3.resource('dynamodb', region_name="us-east-2")
        table = dynamodb.Table(TABLE_NAME)
        table.put_item(
            Item=Item
        )
        return redirect(url_for('api_call',correo = email))


@app.route("/agenda/<correo>", methods=["GET"])
def api_call(correo):
    url = "https://po7yuq5dw8.execute-api.us-east-1.amazonaws.com/Prod/paciente?email=" + correo
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    datos=response.json()['Items']
    #dat=datos['Items']
    
    return render_template("agenda.html", data=datos)


"""
@app.route("/dashboard")
def dashboard():
    TABLE_NAME = "InfoSensors"
    
    dynamodb_client = boto3.client('dynamodb',
    region_name="us-east-1")
    dynamodb = boto3.resource('dynamodb', region_name="us-east-1")

    table = dynamodb.Table(TABLE_NAME)

    response = table.scan()


    return render_template("dashboard.html", data=response)

"""
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/dashboard2")
def dashTemp():
    temperatura=[]
    TABLE_NAME = "InfoSensors"
    dynamodb_client = boto3.client('dynamodb',
    region_name="us-east-1")
    dynamodb = boto3.resource('dynamodb', region_name="us-east-1")
    table = dynamodb.Table(TABLE_NAME)
    response = table.scan(FilterExpression=Attr('idSensor').eq('Temp C1'))
    data=response['Items']

    for item in response['Items']:
        print(item)
        for val in item['temperature']:
            print(val)
            temperatura.append(val)  
    df = pd.DataFrame(temperatura)
    fig = px.line(df, x="ts", y="sensorValue", title="Sensor Temp C1 temperature")
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return render_template("dashboard2.html", graphJSON=graphJSON)

@app.route("/dashboard3")
def dashHum():
    humedad=[]
    TABLE_NAME = "InfoSensors"
    dynamodb_client = boto3.client('dynamodb',
    region_name="us-east-1")
    dynamodb = boto3.resource('dynamodb', region_name="us-east-1")
    table = dynamodb.Table(TABLE_NAME)
    response = table.scan(FilterExpression=Attr('idSensor').eq('Temp C1'))
    #data=response['Items']
    for item in response['Items']:
        #print(item)
        for val in item['humidity']:
            #print(val)
            humedad.append(val) 

    df = pd.DataFrame(humedad)
    fig = px.line(df, x="ts", y="sensorValue", title="Sensor Temp C1 humidity")
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return render_template("dashboard3.html", graphJSON=graphJSON)

@app.route("/dashboard4")
def dashTempS2():
    temperatura=[]
    TABLE_NAME = "InfoSensors"
    dynamodb_client = boto3.client('dynamodb',
    region_name="us-east-1")
    dynamodb = boto3.resource('dynamodb', region_name="us-east-1")
    table = dynamodb.Table(TABLE_NAME)
    response = table.scan(FilterExpression=Attr('idSensor').eq('TempE1'))
    #data=response['Items']
    for item in response['Items']:
        #print(item)
        for val in item['temperature']:
            #print(val)
            temperatura.append(val) 

    df = pd.DataFrame(temperatura)
    fig = px.line(df, x="ts", y="sensorValue", title="Sensor TempE1 Temperature")
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return render_template("dashboard4.html", graphJSON=graphJSON)

@app.route("/dashboard5")
def dashHumS3():
    humedad=[]
    TABLE_NAME = "InfoSensors"
    dynamodb_client = boto3.client('dynamodb',
    region_name="us-east-1")
    dynamodb = boto3.resource('dynamodb', region_name="us-east-1")
    table = dynamodb.Table(TABLE_NAME)
    response = table.scan(FilterExpression=Attr('idSensor').eq('TempE1'))
    #data=response['Items']
    for item in response['Items']:
        #print(item)
        for val in item['humidity']:
            #print(val)
            humedad.append(val) 

    df = pd.DataFrame(humedad)
    fig = px.line(df, x="ts", y="sensorValue", title="Sensor TempE1 humidity")
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return render_template("dashboard5.html", graphJSON=graphJSON)

@app.route("/dashboard6")
def door():
    puerta=[]
    TABLE_NAME = "InfoSensors"
    dynamodb_client = boto3.client('dynamodb',
    region_name="us-east-1")
    dynamodb = boto3.resource('dynamodb', region_name="us-east-1")
    table = dynamodb.Table(TABLE_NAME)
    response = table.scan(FilterExpression=Attr('idSensor').eq('Puerta Principal'))
    print(response['Items'])

    for item in response['Items']:
    #print(item)
        for val in item['door']:
            #print(val)
            puerta.append(val) 

    df = pd.DataFrame(puerta)
    fig = px.line(df, x="ts", y="sensorValue", title="Door Activity")
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)



    return render_template("dashboard6.html", graphJSON=graphJSON)







# If this script is the main script being executed, start the web server.
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)