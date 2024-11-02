from flask import Flask, render_template, request

app = Flask(__name__)



@app.route('/')
def index():
	return render_template("GetTheBand.html")



@app.route('/TheBand.html', methods=['GET'])
def renderTableGet():
    TheBandName = request.args.get('YearFormed')
    YearFormed = request.args.get('OriginCity')
    OriginCity = request.args.get('TheBandName')
    OriginState = request.args.get('OriginState')
    output = render_template('TheBand.html', TheBandName=TheBandName, YearFormed=YearFormed, OriginCity=OriginCity, OriginState=OriginState)
    return output 


	


if __name__ == '__main__':
	app.run(port=8000, debug=True, host="0.0.0.0")