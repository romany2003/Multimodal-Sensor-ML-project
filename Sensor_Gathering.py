import dash
from dash.dependencies import Output, Input
from dash import dcc, html, dcc
from datetime import datetime
import json
import plotly.graph_objs as go
from collections import deque
from flask import Flask, request
import csv
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt

server = Flask(__name__)
app = dash.Dash(__name__, server=server)

MAX_DATA_POINTS = 1000
UPDATE_FREQ_MS = 1000

time = deque(maxlen=MAX_DATA_POINTS)
accel_x = deque(maxlen=MAX_DATA_POINTS)
accel_y = deque(maxlen=MAX_DATA_POINTS)
accel_z = deque(maxlen=MAX_DATA_POINTS)

app.layout = html.Div(
	[
		dcc.Markdown(
			children="""
			# Live Sensor Readings
			Streamed from Sensor Logger: tszheichoi.com/sensorlogger
		"""
		),
		dcc.Graph(id="live_graph"),
		dcc.Interval(id="counter", interval=UPDATE_FREQ_MS),
	]
)


@app.callback(Output("live_graph", "figure"), Input("counter", "n_intervals"))
def update_graph(_counter):
	data = [
		go.Scatter(x=list(time), y=list(d), name=name)
		for d, name in zip([accel_x, accel_y, accel_z], ["X", "Y", "Z"])
	]

	graph = {
		"data": data,
		"layout": go.Layout(
			{
				"xaxis": {"type": "date"},
				"yaxis": {"title": "Acceleration ms<sup>-2</sup>"},
			}
		),
	}
	if (
		len(time) > 0
	):  #  cannot adjust plot ranges until there is at least one data point
		graph["layout"]["xaxis"]["range"] = [min(time), max(time)]
		graph["layout"]["yaxis"]["range"] = [
			min(accel_x + accel_y + accel_z),
			max(accel_x + accel_y + accel_z),
		]

	return graph


#Gyroscope
buffer_gyrx = []
buffer_gyry = []
buffer_gyrz = []

#Acceleration
buffer_accx = []
buffer_accy = []
buffer_accz = []
buffer_acct = []




@server.route("/data", methods=["POST"])
def data():  #get sensor data from app
	if str(request.method) == "POST":
		data = json.loads(request.data)
		print(len(data['payload']))

		#collecting gyroscope and accelerometer data 
		checklist = ["gyroscope","accelerometer"]
		i = 0
		j=0
		for d in data['payload']:
			i+=1
			if len(data['payload'])%i > 4 and len(checklist)==0:
				j+=4
				checklist = ["accelerometer","gyroscope"]

            #gyroscope
			if (
				d.get("name", None) == "gyroscope" and "gyroscope" in  checklist
			):
				checklist.remove("gyroscope")
				buffer_gyrx.append(d["values"]["x"])
				buffer_gyry.append(d["values"]["y"])
				buffer_gyrz.append(d["values"]["z"])
                
            #accel
			if (
				d.get("name", None) == "accelerometer"and "accelerometer" in  checklist
			): 

				checklist.remove("accelerometer")
				buffer_accx.append(d["values"]["x"])
				buffer_accy.append(d["values"]["y"])
				buffer_accz.append(d["values"]["z"])
				
                
				accel_x.append(d["values"]["x"])
				accel_y.append(d["values"]["y"])
				accel_z.append(d["values"]["z"])

		print("===>Added " + str(j) + " entries~")
		for s in checklist:
                # adding the data into the bufffer
			if s == "gyroscope":
				checklist.remove("gyroscope")
				buffer_gyrx.append(buffer_gyrx[-1] if buffer_gyrx else 0)
				buffer_gyry.append(buffer_gyry[-1] if buffer_gyry else 0)
				buffer_gyrz.append(buffer_gyrz[-1] if buffer_gyrz else 0)


			if s == "accelerometer":
				checklist.remove("accelerometer")
				buffer_accx.append(buffer_accx[-1] if buffer_accx else 0)
				buffer_accy.append(buffer_accy[-1] if buffer_accy else 0)
				buffer_accz.append(buffer_accz[-1] if buffer_accz else 0)

	
	
	return "success"


#outputting the extracted data into csv file.

if __name__ == "__main__":
	app.run_server(port=8000, host="0.0.0.0")
	
	current_time = datetime.now()

	data = {
		
		'acc_x': buffer_accx,
		'acc_y': buffer_accy,
		'acc_z': buffer_accz,
		'gyrx': buffer_gyrx,
		'gyry': buffer_gyry,
		'gyrz': buffer_gyrz
	}
 
	df = pd.DataFrame(data)
	df.to_csv("out.csv",index=False)
	print("ADDED " + str(len(buffer_acct)) + " entries!~")

