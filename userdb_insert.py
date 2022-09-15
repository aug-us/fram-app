import sqlite3
import flask
import pickle
from flask import Flask, render_template, request
import os
conn=sqlite3.connect('fram.db')
cursor=conn.cursor()
#creating instance of the class
app=Flask(__name__)
#to tell flask what url shoud trigger the function index()
@app.route('/')
def index():
    return flask.render_template('ind.htm')
#prediction function
@app.route('/highrisk')
@app.route('/lowrisk')
#@app.route('/sam')
@app.route('/result',methods = ['POST','GET']) 
def result():
    if request.method == 'POST':
        gender= request.form['gender']
        age=request.form['age']
        cigsPerDay=request.form['cigsPerDay']
        prevalentHyp=request.form['prevalentHyp']
        diabetes=request.form['diabetes']
        totChol=request.form['totChol']
        sysBP= request.form['sysBP']
        BMI=request.form['BMI']
        heartRate=request.form['heartRate']
        glucose=request.form['glucose']
        to_predict_list=[gender,age, cigsPerDay,prevalentHyp, diabetes,totChol, sysBP, BMI, heartRate, glucose]
        to_predict_list=[to_predict_list]#to covert ino 2D array
        loaded_model = pickle.load(open("heart_df.pkl","rb")) #unpickling the model
        result = loaded_model.predict(to_predict_list)
        if int(result)==1:
            #to insert user entry into database
            #cursor.execute("INSERT INTO User_entry (gender, age, cigsPerDay, prevalentHyp, diabetes,totChol, sysBP, BMI, heartRate, glucose, HeartRisk) VALUES(?,?,?,?,?,?,?,?,?,?,?)",(gender, age, cigsPerDay, prevalentHyp, diabetes,totChol, sysBP, BMI, heartRate, glucose, 1))
            #cursor.execute("COMMIT")
            #display the ouput
            return render_template('highrisk.htm')
            #return render_template('high.htm')
        else:
            #cursor.execute("INSERT INTO User_entry (gender, age, cigsPerDay, prevalentHyp, diabetes,totChol, sysBP, BMI, heartRate, glucose, HeartRisk) VALUES(?,?,?,?,?,?,?,?,?,?,?)",(gender, age, cigsPerDay, prevalentHyp, diabetes,totChol, sysBP, BMI, heartRate, glucose, 0))
            #cursor.execute("COMMIT")
            return render_template('lowrisk.htm')
@app.route("/riskpatients",methods=['POST'])
def riskpatients():
    if(request.form["submit"]=='HEALTH INSURANCE POLICIES'):
        return render_template("insurance.htm")
    elif(request.form["submit"]=="CARDIOLOGISTS IN CHENNAI"):
        return render_template("doctors.htm")
    else:
        pass
if __name__ == '__main__':
   port = int(os.environ.get("PORT", 2000))
   app.run(host='0.0.0.0',debug=True, port=port)
    
    
    
    
    
    
    
    
    
    
    