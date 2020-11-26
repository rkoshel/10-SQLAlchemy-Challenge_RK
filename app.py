import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify



engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

measurement = Base.classes.measurement
station = Base.classes.station

app = Flask(__name__)


@app.route("/")
def welcome():
    """List available API routes"""
    return(
        f"Available Routes:<br/>"
        f"/precipitation<br/>"
        f"/stations<br/>"
        f"/tobs<br/>"
        

        
    )

@app.route("/precipitation")
def precipitation():
    #create session and query precipation and date data
    session = Session(engine)

    results = session.query(measurement.date, measurement.prcp).all()

    session.close()

    #create dictionary from row data and append to a list
    precip = []
    for date, prcp in results:
        precip_dict = {}
        precip_dict["date"] = date
        precip_dict["prcp"] = prcp
        precip.append(precip_dict)
    
    return jsonify(precip)

@app.route("/stations")
def stations():
    #create session to pull station information
    session = Session(engine)
    
    results2 = session.query(station.station).all()

    session.close()

#create dictionary from row data and append to a list
    stations = []
    for row in results2:
        station_dict = {}
        station_dict["station"] = row
        stations.append(station_dict)

    return jsonify(stations)

@app.route("/tobs")
def tobs():
    #create session to pull last year of data for most active station
    session = Session(engine)
    
    one_year_ago = dt.date(2017, 8, 23) - dt.timedelta(days = 365)

    results3 = session.query(measurement.date, measurement.tobs).\
        filter(measurement.date >= one_year_ago).\
        filter(measurement.station =='USC00519281').all()

    session.close()

    #create dictionary from row data and append to a list
    tobs_list = []
    for date, tobs in results3:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        tobs_list.append(tobs_dict)
    
    return jsonify(tobs_list)



if __name__ == '__main__':
    app.run(debug=True)