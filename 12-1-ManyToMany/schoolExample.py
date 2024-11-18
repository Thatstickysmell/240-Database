#!/usr/bin/python3

from flask import Flask, render_template, request, redirect, url_for
import mysql.connector, os, json

with open('secrets.json', 'r') as secretFile:
    creds = json.load(secretFile)['mysqlCredentials']

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/showBands', methods=['GET'])
def showBands():
    connection = mysql.connector.connect(**creds)
    mycursor = connection.cursor()
    # mycursor2 = connection.cursor()

    # If there is a section_id 'GET' variable, use this to refine the query
    ThePerformanceID = request.args.get('PerformanceID')
    if ThePerformanceID is not None:
        mycursor.execute("""SELECT Band.BandName, Performance.PerformanceDate, PerformanceSong.ArrangementType, Song.Title from Band
                         join Performance on Band.BandID=Performance.BandID
                         join PerformanceSong on Performance.PerformanceID=PerformanceSong.PerformanceID
                         join Song on PerformanceSong.SongID=Song.SongID
                         where Performance.PerformanceID=%s""", (ThePerformanceID,))
        myresult = mycursor.fetchall()
        if len(myresult) >= 1:
            TheBandName = myresult[0][3]
            TheBandPerformanceDate = myresult[0][1]
        else:
            TheBandName = TheBandPerformanceDate = "Unknown"
        pageTitle = f"Showing all students in section {ThePerformanceID}, {TheBandName} ({TheBandPerformanceDate})"
    else:
        mycursor.execute("SELECT BandID, BandName, YearFormed from Band")
        pageTitle = "Showing all Bands"
        myresult = mycursor.fetchall()

    mycursor.close()
    connection.close()
    return render_template('students.html', studentList=myresult, pageTitle=pageTitle)

@app.route('/showSongs', methods=['GET'])
def showSongs():
    connection = mysql.connector.connect(**creds)
    mycursor = connection.cursor()

    # If there is a student_id 'GET' variable, use this to refine the query
    TheSongID = request.args.get('SongID')
    if TheSongID is not None:
        # Check if the student is registering for a new class
        TheBandPlaysSong = request.args.get('BandPlaysSong')
        if TheBandPlaysSong is not None:
            mycursor.execute("""INSERT into PerformanceSong (PerformanceID, SongID) values (%s, %s)
                             """, (TheSongID, TheBandPlaysSong))
            connection.commit()

        mycursor.execute("""SELECT Song.Title, BandName, YearFormed, PerformanceDate, IncludesNonBandPerson
                         from Performance
                         join PerformanceSong on Performance.PerformanceID=PerformanceSong.PerformanceID
                         join Song on Song.SongID=PerformanceSong.SongID
                         join Band on Band.BandId=Performance.BandID
                         where Song.SongID=%s""", (TheSongID,))
        sections = mycursor.fetchall()
        print(sections)
        if len(sections) >= 1:
            PerformanceInfo = sections[0][3] and sections[0][4]
            mycursor.execute("""SELECT Song.SongID, BandName, YearFormed
                                FROM Song
                                Join Band on Band.BandID=Performance.PerformanceID
                                WHERE Performance.PerformanceID not in (
                                    SELECT PerformanceID
                                    from PerformanceSong
                                    where PerformanceSong.PerformanceID=%s
                                )
                             """, (TheSongID,))
            othersections = mycursor.fetchall()
            print(othersections)
        else:
            studentName = "Unknown"
            othersections = None
        pageTitle = f"Showing all sections for student: {studentName})"
    else:
        mycursor.execute("""SELECT section.id, course_name, course_code from section
                         join course on section.course_id=course.id""")
        pageTitle = "Showing all sections"
        sections = mycursor.fetchall()
        othersections = None

    mycursor.close()
    connection.close()
    print(f"{studentID=}")
    return render_template('sections.html', 
                           sectionList=sections, 
                           pageTitle=pageTitle, 
                           othersections=othersections, 
                           studentId=studentID 
                           )


if __name__ == '__main__':
    app.run(port=8000, debug=True, host="0.0.0.0")