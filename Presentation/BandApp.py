#!/usr/bin/python3

from flask import Flask, render_template, request, redirect, url_for
import mysql.connector, os, json

with open('/home/k-city/240-Database/Presentation/secrets.json', 'r') as secretFile:
    creds = json.load(secretFile)['mysqlCredentials']

app = Flask(__name__)

@app.route('/')
def default():
    return render_template('base.html')

@app.route('/performance-info', methods=['GET'])
def get_performance_info():
    PerformanceID = request.args.get('PerformanceID')
    SongID = request.args.get('SongID')
    # redirect to all Songs if no id was provided
    if PerformanceID is None:
        return redirect(url_for("get_performances"))

    connection = mysql.connector.connect(**creds)
    mycursor = connection.cursor()

    # update performance information if necessary
    performance_info = (
        request.args.get('PerformanceDate'),
        request.args.get('Length'),
        request.args.get('BandID'),
        PerformanceID
    )
    if not None in performance_info:
        mycursor.execute("UPDATE Performance set PerformanceDate=%s, Length=%s, BandID=%s where PerformanceID=%s", performance_info)
        connection.commit()

    # Add a new song to the performance
    add_performance_id = request.args.get('add_performance_id')
    if add_performance_id is not None:
        mycursor.execute("""INSERT into PerformanceSong (SongID, PerformanceID) values (%s, %s)""", (SongID, add_performance_id))
        connection.commit()

    # Adding a song to PerformanceSong
    if SongID is not None and PerformanceID is not None:
        mycursor.execute(
            "INSERT INTO PerformanceSong (SongID, PerformanceID) VALUES (%s, %s)",
            (SongID, PerformanceID)
        )
        connection.commit()



    # Remove a song from the performance
    remove_song_id = request.args.get('remove_song_id')
    if remove_song_id is not None:
        mycursor.execute("DELETE from PerformanceSong where SongID=%s and PerformanceID=%s", (remove_song_id, PerformanceID))
        connection.commit()

    # Retrieve basic information for the Performance
    mycursor.execute("SELECT BandName, YearFormed, PerformanceDate, Length, IncludesNonBandPerson, Performance.BandID from Performance join Band on Performance.BandID=Band.BandID where Performance.PerformanceID=%s", (PerformanceID,))
    try:
        BandName, YearFormed, PerformanceDate, Length, IncludesNonBandPerson, BandID = mycursor.fetchall()[0]
    except:
        return render_template("error.html", message="Error retrieving Performance - does it exist?")
    
    # Retrieve registered songs
    mycursor.execute("""SELECT Song.SongID, Title, Composer, Album from Song 
                     join PerformanceSong on PerformanceSong.SongID=Song.SongID 
                     join Performance on PerformanceSong.PerformanceID=Performance.PerformanceID
                     where Performance.PerformanceID=%s
                     order by Composer""", (PerformanceID,))
    registeredsongs = mycursor.fetchall()

    # Retrieve all songs (for adding to performance)
    mycursor.execute("""SELECT SongID, Title from Song 
                     WHERE SongID NOT IN (
                         SELECT SongID FROM PerformanceSong 
                         WHERE PerformanceID = %s
                     )""", (PerformanceID,))
    Songs = mycursor.fetchall()

    mycursor.close()
    connection.close()
    return render_template("performance-info.html",
                           PerformanceID=PerformanceID,
                           BandName=BandName,
                           YearFormed=YearFormed,
                           PerformanceDate=PerformanceDate,
                           Length=Length,
                           IncludesNonBandPerson=IncludesNonBandPerson,
                           BandID=BandID,
                           registered_Songs=registeredsongs,
                           Songs=Songs
                           )


@app.route('/song-info', methods=['GET'])
def get_song_info():
    SongID = request.args.get('SongID')
    
    # redirect to all songs if no id was provided
    if SongID is None:
        return redirect(url_for("get_songs"))

    connection = mysql.connector.connect(**creds)
    mycursor = connection.cursor()
    
    # check to see if the song needs to be updated
    new_Title = request.args.get('Title')
    new_Composer = request.args.get('Composer')
    new_Album = request.args.get('Album')
    if new_Title is not None and new_Composer is not None and new_Album:
        mycursor.execute("""UPDATE Song set Title=%s,Composer=%s, Album=%s where SongID=%s""", (new_Title, new_Composer, new_Album, SongID))
        connection.commit()

    # check to see if a Performance needs to be dropped
    drop_performancd_id = request.args.get('drop_performancd_id')
    if drop_performancd_id is not None:
        mycursor.execute("""DELETE from PerformanceSong where SongID=%s and PerformanceID=%s""", (SongID, drop_performancd_id))
        connection.commit()

    # check to see if a Performance needs to be added
    add_performance_id = request.args.get('add_performance_id')
    if add_performance_id is not None:
        mycursor.execute("""INSERT into PerformanceSong (SongID, PerformanceID) values (%s, %s)""", (SongID, add_performance_id))
        connection.commit()

    # retreve the song information from the database
    mycursor.execute("Select Title, Composer, Album from Song where SongID=%s", (SongID,))
    Title, Composer, Album = mycursor.fetchone()
    if Title is None or Composer is None:
        return """Error - unable to find song. <a href="/students">Return to the song list</a>"""
    
    # retrieve the songs's band from the database
    mycursor.execute("""SELECT PerformanceSong.PerformanceID, BandName, YearFormed, PerformanceDate, Length, Band.BandID from PerformanceSong
                         join Performance on Performance.PerformanceID=PerformanceSong.PerformanceID
                         join Band on Band.BandID=Performance.BandID
                         where PerformanceSong.SongID=%s""", (SongID,))
    registered_Performances = mycursor.fetchall()
    

    # retrieve a list of other bands the song can register for CHECK THIS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    mycursor.execute("""SELECT Performance.PerformanceID, BandName, YearFormed
                     from (
                         select PerformanceID as PerformanceID from Performance
                         except
                         select PerformanceID from PerformanceSong where SongID=%s) as remainingPerformances 
                     join Performance on remainingPerformances.PerformanceID=Performance.PerformanceID
                     join Band on Band.BandID=Performance.BandID""", (SongID,))
    all_performances = mycursor.fetchall()

    mycursor.close()
    connection.close()

    return render_template(
        "song_info.html", 
        SongID=SongID, 
        Title=Title, 
        Composer=Composer,
        Album=Album,
        registered_performances=registered_Performances,
        unregistered_performances=all_performances
        )

@app.route('/songs', methods=['GET'])
def get_songs():
    connection = mysql.connector.connect(**creds)
    mycursor = connection.cursor()

    # check to see if a new song needs to be added
    # new_SongID = request.args.get('new_SongID')
    new_Title = request.args.get('new_Title')
    new_Composer = request.args.get('new_Composer')
    new_Album = request.args.get('new_Album')
    if new_Title is not None and new_Composer is not None and new_Album:
        mycursor.execute("INSERT INTO Song (Title, Composer, Album) values (%s, %s, %s)", (new_Title, new_Composer, new_Album))
        connection.commit()

    # check to see if a song needs to be deleted
    delete_SongID = request.args.get('delete_SongID')
    if delete_SongID is not None:
        try:
            mycursor.execute("delete from Song where SongID=%s",(delete_SongID,))
            connection.commit()
        except:
            return render_template("error.html", message="Error deleting Song, perhaps this song is part of a performance")
        
    # retrieve all Songs
    mycursor.execute("SELECT SongID, Title, Composer, Album from Song")
    pageTitle = "Showing all Songs"
    allSongs = mycursor.fetchall()

    mycursor.close()
    connection.close()
    return render_template('songs.html', songList=allSongs, pageTitle=pageTitle)



@app.route('/performances', methods=['GET'])
def get_performances():
    connection = mysql.connector.connect(**creds)
    mycursor = connection.cursor()

    # check to see if a new Performance needs to be added
    new_performance_info = (
        #request.args.get('new_section_id'), 
       #request.args.get('new_BandID'), 
        request.args.get('new_PerformanceID'), 
        request.args.get('new_BandID'), 
        request.args.get('new_PerformanceDate'),
        request.args.get('new_Length'),
        request.args.get('new_IncludesNonBandPerson')
    )
    
    if not None in (new_performance_info):
        mycursor.execute("INSERT INTO Performance (PerformanceID, BandID, PerformanceDate, Length, IncludesNonBandPerson) values (%s, %s, %s, %s, %s)", new_performance_info)
        connection.commit()

    # check to see if a Performance needs to be deleted
    delete_PerformanceID = request.args.get('delete_PerformanceID')
    if delete_PerformanceID is not None:
        try:
            mycursor.execute("delete from Performance where PerformanceID=%s",(delete_PerformanceID,))
            connection.commit()
        except:
            return render_template("error.html", message="Error deleting Performance, perhaps there are students songs for it")

    # retrieve all performances
    mycursor.execute("SELECT Band.BandName, Performance.PerformanceID, Performance.BandID, Performance.PerformanceDate, Performance.Length, Performance.IncludesNonBandPerson from Performance join Band on Band.BandID=Performance.BandID")
    allPerformances = mycursor.fetchall()
    pageTitle = "Showing all Performances"
    # mycursor.execute("SELECT BandID, BandName, YearFormed from Band")
    # allBands = mycursor.fetchall()

    mycursor.close()
    connection.close()
    return render_template('performances.html', PerformanceList=allPerformances, pageTitle=pageTitle)

@app.route('/bands', methods=['GET'])
def get_bands():
    connection = mysql.connector.connect(**creds)
    mycursor = connection.cursor()

    # look to see if a new band should be added
    new_band_info = (
        # request.args.get('new_BandID'),
        request.args.get('new_BandName'),
        request.args.get('new_YearFormed'),
        request.args.get('new_OriginCity'),
        request.args.get('new_OriginState')
    )
    if not None in new_band_info:
        mycursor.execute("INSERT INTO Band (BandName, YearFormed, OriginCity, OriginState) values (%s, %s, %s, %s)", new_band_info)
        connection.commit()

    # look to see if a band should be deleted
    delete_BandID = request.args.get('delete_BandID')
    if delete_BandID is not None:
        try:
            mycursor.execute("DELETE from Band where BandID=%s", (delete_BandID,))
            connection.commit()
        except:
            return render_template("error.html", message="Error deleting Band, perhaps it has Performances")

    # retrieve a list of all Bands
    mycursor.execute("SELECT BandID, BandName, YearFormed, OriginCity, OriginState from Band")
    allBands = mycursor.fetchall()

    pageTitle = "Showing all Bands"

    mycursor.close()
    connection.close()
    return render_template('bands.html', allBands=allBands, pageTitle=pageTitle,)

@app.route('/band-info', methods=['GET'])
def get_band_info():
    TheBandID = request.args.get('BandID')
    
    # redirect to all bands if no id was provided
    if TheBandID is None:
        return redirect(url_for("get_bands"))

    connection = mysql.connector.connect(**creds)
    mycursor = connection.cursor()


    new_BandID = request.args.get('BandID')
    new_BandName = request.args.get('new_BandName')
    new_YearFormed = request.args.get('new_YearFormed')
    new_OriginCity = request.args.get('new_OriginCity')
    new_OriginState = request.args.get('new_OriginState')

    if new_BandID is None:
        return "Error, id not found"
    elif new_BandName is not None and new_YearFormed is not None:
        mycursor = connection.cursor()
        print("UPDATE Band set BandName=%s, YearFormed=%s, OriginCity=%s, OriginState=%s where BandID=%s", (new_BandName, new_YearFormed, new_OriginCity, new_OriginState, new_BandID))
        mycursor.execute("UPDATE Band set BandName=%s, YearFormed=%s, OriginCity=%s, OriginState=%s where BandID=%s", (new_BandName, new_YearFormed, new_OriginCity, new_OriginState, new_BandID))
        connection.commit()
        # mycursor.close()


    # retrieve Band information
    mycursor.execute("SELECT BandName, YearFormed, OriginCity, OriginState from Band where BandID=%s", (TheBandID,))
    try:
        new_BandName, new_YearFormed, new_OriginCity, new_OriginState = mycursor.fetchall()[0]
    except:
        return render_template("error.html", message="Error retrieving Band - perhaps it doesn't exist")
    
    # pageTitle = "Showing all Bands"
    # retrieve existing Performances of band
    mycursor.execute("SELECT PerformanceID, PerformanceDate, Length from Performance where BandID=%s", (TheBandID,))
    existingPerformances = mycursor.fetchall()
    
    mycursor.close()
    connection.close()

    return render_template("band-info.html",
                           BandID=TheBandID,
                           BandName=new_BandName,
                           YearFormed=new_YearFormed,
                           OriginCity=new_OriginCity,
                           OriginState=new_OriginState,
                           existingPerformances=existingPerformances
                           )

if __name__ == '__main__':
    app.run(port=8000, debug=True, host="0.0.0.0")