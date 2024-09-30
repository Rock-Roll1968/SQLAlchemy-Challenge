 # Import the dependencies.
import numpy as np
import datetime as dt

#################################################
# Database Setup
#################################################
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Create engine using the `hawaii.sqlite` database file
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Declare a Base using `automap_base()`
Base = automap_base()

# Use the Base class to reflect the database tables
Base.prepare(autoload_with=engine, reflect=True)

# Assign the measurement class to a variable called `Measurement` and
# the station class to a variable called `Station`
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a session
session = Session()

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    return (
            f"Available Routes:<br/>"
            f"/api/v1.0/precipitation<br/>"
            f"/api/v1.0/stations<br/>"
            f"/api/v1.0/tobs<br/>"
            f"/api/v1.0/start_date<br/>"
            f"/api/v1.0/start_end_date"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    
    last_year_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= last_year_date).all()
    session.close()

    precip_data = {date: prcp for date, prcp in results}
    return jsonify(precip_data)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    
    results = session.query(Station.name).all()
    session.close()

    stations_list = [station[0] for station in results]
    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    last_year_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.date,Measurement.tobs).filter(Measurement.date >= last_year_date, Measurement.station == 'USC00519281').all()
    session.close()

    tobs_data = { date:tobs for date,tobs in results}
    return jsonify(tobs_data)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def date_range(start, end='2017-08-23'):
    session = Session(engine)

    min,avg,max = session.query(
        func.min(Measurement.tobs),
        func.avg(Measurement.tobs),
        func.max(Measurement.tobs)
     ).filter(
         (Measurement.date>=start) &
         (Measurement.date<=end)
    ).first()

    print(min,avg,max)
    
    return {'Min_temp':min, 'Max_temp':max, 'Avg_temp':avg, 'start_date':start, 'end_date':end}
    


if __name__ == "__main__":
    app.run(debug=True)

