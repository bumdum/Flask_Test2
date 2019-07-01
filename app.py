import os

#import pandas as pd
#import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Flask, jsonify, g, request, render_template
from flask_sqlalchemy import SQLAlchemy

import json
import sqlite3
app = Flask(__name__, template_folder='templates')

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/f1_database.sqlite"
db = SQLAlchemy(app)
Base = automap_base()
Base.prepare(db.engine, reflect=True)

f1_data = Base.classes.data
f1_lap_data = Base.classes.lap_data
f1_pit_data = Base.classes.pit_data

@app.route("/")
def home():
    g.races = db.session.query(f1_data.raceId, f1_data.race_name).distinct().filter_by(year = '2017').all()
    return render_template("index.html")

@app.route("/data")
def index():
    sel = [
        f1_data.index,
        f1_data.race_name,
        f1_data.resultId,
        f1_data.raceId,
        f1_data.driverId,
        f1_data.circuitId,
        f1_data.constructorId,
        f1_data.grid,
        f1_data.position,
        f1_data.positionText,
        f1_data.positionOrder,
        f1_data.points,
        f1_data.laps,
        f1_data.time_x,
        f1_data.milliseconds,
        f1_data.fastestLap,
        f1_data.rank,
        f1_data.fastestLapTime,
        f1_data.fastestLapSpeed,
        f1_data.statusId,
        f1_data.year,
        f1_data.round,
        f1_data.date,
        f1_data.RaceName,
        f1_data.driverRef,
        f1_data.dob,
        f1_data.driver_number,
        f1_data.driver_nationality,
        f1_data.team_name,
        f1_data.team_nationality,
        f1_data.circuit_name,
        f1_data.circuit_location,
        f1_data.circuit_country,
        f1_data.circuit_lat,
        f1_data.circuit_lng,
        f1_data.status
    ]

    results = db.session.query(*sel).all()


    f1_list = []
    for result in results:
        f1_dict = {}
        f1_dict ["race_name"] = result[1]
        f1_dict["resuldID"] = result[2]
        f1_dict["raceId"] = result[3]
        f1_dict["driverId"] = result[4]
        f1_dict["circuitId"] = result[5]
        f1_dict["constructorId"] = result[6]
        f1_dict["grid"] = result[7]
        f1_dict["position"] = result[8]
        f1_dict["positionText"] = result[9]
        f1_dict["positionOrder"] = result[10]
        f1_dict["points"] = result[11]
        f1_dict["laps"] = result[12]
        f1_dict["time"] = result[13]
        f1_dict["milliseconds"] = result[14]
        f1_dict["fastestLap"] = result[15]
        f1_dict["rank"] = result[16]
        f1_dict["fastestLapTime"] = result[17]
        f1_dict["fastestLapSpeed"] = result[18]
        f1_dict["statusId"] = result[19]
        f1_dict["year"] = result[20]
        f1_dict["round"] = result[21]
        f1_dict["date"] = result[22]
        f1_dict["RaceName"] = result[23]
        f1_dict["driverRef"] = result[24]
        f1_dict["dob"] = result[25]
        f1_dict["driver_number"] = result[26]
        f1_dict["driver_nationality"] = result[27]
        f1_dict["team_name"] = result[28]
        f1_dict["team_nationality"] = result[29]
        f1_dict["circuit_name"] = result[30]
        f1_dict["circuit_location"] = result[31]
        f1_dict["circuit_country"] = result[32]
        f1_dict["circuit_lat"] = result[33]
        f1_dict["circuit_lng"] = result[34]
        f1_dict["status"] = result[35]

        f1_list.append(f1_dict)


    return jsonify(f1_list)


@app.route("/lap_data")
def laps():
    sel = [
        f1_lap_data.index,
        f1_lap_data.raceId,
        f1_lap_data.driverId,
        f1_lap_data.lap,
        f1_lap_data.position,
        f1_lap_data.lap_time,
        f1_lap_data.lap_milliseconds,
        f1_lap_data.RaceName,
        f1_lap_data.driverRef
    ] 

    results = db.session.query(*sel).all()

    lap_list = []
    for result in results:
        lap_dict = {}
        lap_dict["raceId"] = result[1]
        lap_dict["driverId"] = result[2]
        lap_dict["lap"] = result[3]
        lap_dict["position"] = result[4]
        lap_dict["lap_time"] = result[5]
        lap_dict["lap_milliseconds"] = result[6]
        lap_dict["RaceName"] = result[7]
        lap_dict["driverRef"] = result[8]
        lap_list.append(lap_dict)

    return jsonify(lap_list)


@app.route("/pit_data")
def pit():
    sel = [
        f1_pit_data.index,
        f1_pit_data.raceId,
        f1_pit_data.driverId,
        f1_pit_data.pit_stop_number,
        f1_pit_data.Pit_lap,
        f1_pit_data.pit_timestamp,
        f1_pit_data.pit_duration,
        f1_pit_data.pit_milliseconds,
        f1_pit_data.RaceName,
        f1_pit_data.driverRef,
    ]
    
    results = db.session.query(*sel).all()

    pit_list = []
    for result in results:
        pit_dict = {}
        pit_dict["raceId"] = result[1]
        pit_dict["driverId"] = result[2]
        pit_dict["pit_stop_number"] = result[3]
        pit_dict["Pit_lap"] = result[4]
        pit_dict["pit_timestamp"] = result[5]
        pit_dict["pit_duration"] = result[6]
        pit_dict["pit_milliseconds"] = result[7]
        pit_dict["RaceName"] = result[8]
        pit_dict["driverRef"] = result[9]
        pit_list.append(pit_dict)

    return jsonify(pit_list)


@app.route("/get_fastest_laps")
def fastestlaps():
    raceId = request.args.get('a', 0, type=int)
    results = db.session.query(f1_lap_data.driverRef, f1_lap_data.lap_time).filter_by(raceId = raceId).order_by(position).limit(3).all()
    return jsonify([dict(zip(tuple ('nt') ,i)) for i in results])


if __name__ == "__main__":
    app.run(debug=True)