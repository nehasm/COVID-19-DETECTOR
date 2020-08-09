from flask import Flask, request, jsonify, render_template 
from flask_sqlalchemy import SQLAlchemy
# from flask_marshmallow import Marshmallow
from datetime import datetime
import os
import dialogflow
import requests
import json
from flask_cors import CORS
import pickle
app = Flask(__name__)
CORS(app)
file = open('model.pkl', 'rb')

clf = pickle.load(file) 

file.close()

ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Neha@1999@localhost/covidbot'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://uqianwfqzecdxe:c2c975e5f8769049fe55e7ecec00b691f3da890abb91bd03570219d3babc81d2@ec2-52-204-20-42.compute-1.amazonaws.com:5432/d1rqcnqhfltfds'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Covidbot(db.Model):

    __tablename__ = "surveydata"

    time = db.Column(db.String(200),primary_key=True)
    name = db.Column(db.String(200),nullable=False)
    age = db.Column(db.String(500),nullable=False)
    tired = db.Column(db.String(1000),nullable=False)
    cold = db.Column(db.String(1000),nullable=False)
    fever = db.Column(db.String(1000),nullable=False)
    sgroupone = db.Column(db.String(500),nullable=False)
    sgrouptwo = db.Column(db.String(500),nullable=False)
    temp = db.Column(db.String(500),nullable=False)
    bp = db.Column(db.Text(),nullable=False)
    sother = db.Column(db.Text(),nullable=False)
    test = db.Column(db.Text(),nullable=False)
    ncovid = db.Column(db.String(),nullable=False)
    numcovid = db.Column(db.String(),nullable=False)

    def __init__(self,time,name,age,tired,cold,fever,sgroupone,sgrouptwo,temp,bp,sother,test,ncovid,numcovid):
        self.time = time
        self.name = name
        self.age = age
        self.tired = tired 
        self.cold = cold 
        self.fever = fever
        self.sgroupone = sgroupone
        self.sgrouptwo = sgrouptwo
        self.temp = temp
        self.bp = bp
        self.sother = sother
        self.test = test
        self.ncovid = ncovid
        self.numcovid = numcovid
        
@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json(silent=True)
    endtext = "Thank you for giving your valuable time and interacting with me"
    if data['queryResult']['fulfillmentText'] == endtext:
        global time,age,tired,cold,fever,sgroupone,sgrouptwo,temp,ncovid
        now = datetime.now()
        time = now.strftime("%d/%m/%Y %H:%M:%S")
        name = data['queryResult']['parameters']["person"][0]["name"]
        age = data['queryResult']['parameters']['age'][0]['amount']
        age = str(age)
        tired = data['queryResult']['parameters']["tired"][0]
        cold = data['queryResult']['parameters']['cold'][0]
        fever = data['queryResult']['parameters']['fever'][0]
        sgroupone = data['queryResult']['parameters']["sgroupone"][0]
        sgroupone = str(sgroupone)
        sgrouptwo = data['queryResult']['parameters']["sgrouptwo"][0]
        sgrouptwo = str(sgrouptwo)
        temp = data['queryResult']['parameters']['temp'][0]['amount']
        temp = str(temp)
        bp = data['queryResult']['parameters']['bp'][0]
        sother = data['queryResult']['parameters']["sother"][0]
        test = data['queryResult']['parameters']["test"][0]
        ncovid = data['queryResult']['parameters']['ncovid'][0]
        numcovid = data['queryResult']['parameters']['numcovid'][0]
        numcovid = str(numcovid)
        # new_entry = Covidbot(time, name, age, tired, cold, fever, sgroupone, sgrouptwo, temp, bp, sother, test, ncovid, numcovid)
        # db.session.add(new_entry)
        # db.session.commit()
    return  "hello"

def detect_intent_texts(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    if text:
        text_input = dialogflow.types.TextInput(
            text=text, language_code=language_code)
        query_input = dialogflow.types.QueryInput(text=text_input)
        response = session_client.detect_intent(
            session=session, query_input=query_input)
        return response.query_result.fulfillment_text

@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.form['message']
    project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
    fulfillment_text = detect_intent_texts(project_id, "unique", message, 'en')
    # if fulfillment_text == "":
    #     fulfillment_text = "i am null"
    response_text = { "message":  fulfillment_text }
    return jsonify(response_text)

@app.route('/detector')
def detector():
    try:
        int(float(age))
    except:
        return render_template("error.html")
    # time,age,tired,cold,fever,sgroupone,sgrouptwo,temp,ncovid
    Age=int(float(age))
    Fever = int(float(temp))
    if tired=="yes":
        Bodypain=1
    else:
        Bodypain=0
    if cold=="yes":
        Runny_nose=1
    else:
        Runny_nose=0
    Sgrouptwo = str(int(float(sgrouptwo)))
    if "1" in sgrouptwo:
        Difficulty_in_breathing=1
    else:
        Difficulty_in_breathing=0
    Sgroupone=str(int(float(sgroupone)))
    if "1" in sgroupone:
        Nasal_congestion=1
    else:
        Nasal_congestion=0
    if "2" in sgroupone:
        Sore_throat=1
    else:
        Sore_throat=0
    if ncovid=="yes":
        Contact_with_covid_patient=1
    else:
        Contact_with_covid_patient=0
    test_symptoms = [[Age,Fever,Bodypain,Runny_nose,Difficulty_in_breathing,Nasal_congestion,Sore_throat,Contact_with_covid_patient]]
    infProb = clf.predict_proba(test_symptoms)[0][1]
    intt=round(infProb * 100)
    age,temp,tired,cold,sgrouptwo,sgroupone,ncovid="","","","","","",""
    return render_template("detect.html",inf=intt)

# run Flask app
if __name__ == "__main__":
    app.run()