#!/usr/bin/python3

from flask import Flask, render_template, request, redirect, url_for
import mysql.connector, os, json

with open('/home/k-city/240-Database/CRUD_for_Band_Table/secrets.json', 'r') as secretFile:
    creds = json.load(secretFile)['mysqlCredentials']

connection = mysql.connector.connect(**creds)

app = Flask(__name__)

@app.route('/', methods=['GET'])
def showBand():
    mycursor = connection.cursor()

    # If there is a name and desc 'GET' variable, insert the new value into the database
    BandName = request.args.get('TheBandName')
    YearFormed = request.args.get('YearFormed')
    OriginCity = request.args.get('OriginCity')
    OriginState = request.args.get('OriginState')
    
    if BandName is not None and YearFormed is not None:
        mycursor.execute("INSERT into Band (BandName, YearFormed) values (%s, %s)", (BandName, YearFormed))
        connection.commit()
    elif request.args.get('delete') == 'true':
        deleteID = request.args.get('BandID')
        mycursor.execute("DELETE from Band where BandID=%s", (deleteID,))
        connection.commit()

    # Fetch the current values of the speaker table
    mycursor.execute("SELECT BandName, YearFormed, OriginCity, OriginState, BandID FROM Band")
    myresult = mycursor.fetchall()
    mycursor.close()
    return render_template('TheBand.html', collection=myresult)

@app.route("/UpdateTheBand")
def updateBand():
    BandID = request.args.get('BandID')
    BandName = request.args.get('TheBandName')
    YearFormed = request.args.get('YearFormed')
    
    if BandID is None:
        return "Error, id not found"
    elif BandName is not None and YearFormed is not None:
        mycursor = connection.cursor()
        mycursor.execute("UPDATE Band set BandName=%s, YearFormed=%s where BandID=%s", (BandName, YearFormed, BandID))
        mycursor.close()
        connection.commit()
        return redirect(url_for('showBand'))


    mycursor = connection.cursor()
    mycursor.execute("select BandName, YearFormed from Band where BandID=%s;", (BandID,))
    existingBandName, existingYearFormed = mycursor.fetchone()
    mycursor.close()
    return render_template('TheBand.html', BandID=BandID, existingBandName=existingBandName, existingYearFormed=existingYearFormed)


if __name__ == '__main__':
    app.run(port=8000, debug=True, host="0.0.0.0")