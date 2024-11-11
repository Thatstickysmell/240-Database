#!/usr/bin/python3

from flask import Flask, render_template, request
import mysql.connector, os
import json

app = Flask(__name__)

@app.route('/', methods=['GET'])
def showBand():
    with open('/home/k-city/240-Database/10-1-preparedStatements/secrets.json', 'r') as secretFile:
        creds = json.load(secretFile)['mysqlCredentials']
    
    connection = mysql.connector.connect(**creds)
    mycursor = connection.cursor()
    

    BandName = request.args.get('TheBandName')
    YearFormed = request.args.get('YearFormed')
    OriginCity = request.args.get('OriginCity')
    OriginState = request.args.get('OriginState')
        
    if BandName:
        mycursor.execute("INSERT INTO Band (BandName, YearFormed, OriginCity, OriginState) VALUES (%s, %s, %s, %s)", (BandName, YearFormed, OriginCity, OriginState))
        connection.commit()
    
    mycursor.execute("SELECT BandName, YearFormed, OriginCity, OriginState FROM Band")
    myresult = mycursor.fetchall()
    
    mycursor.close()
    connection.close()
    
    return render_template('TheBand.html', collection=myresult)

if __name__ == '__main__':
    app.run(port=8000, debug=True, host="0.0.0.0")