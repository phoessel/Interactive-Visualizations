import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func

from flask import (
    Flask,
    render_template,
    jsonify)


engine = create_engine("sqlite:///belly_button_biodiversity.sqlite")

session = Session(engine)

inspector = inspect(engine)

results = inspector.get_table_names()
print(results)

#inspect samples data
columns = inspector.get_columns('samples_metadata')
for column in columns:
    print(column["name"], column["type"])

#inspect OTU data
columns = inspector.get_columns('otu')
for column in columns:
    print(column["name"], column["type"])

Base = automap_base()

Base.prepare(engine, reflect=True)

Main_data = Base.classes.samples_metadata
sample_data = Base.classes.samples
bacteria_data = Base.classes.otu

fulldata = session.query(Main_data).limit(5).all()
for x in fulldata:
    print(x)
#print(fulldata)


app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome!"
    return render_template('index.html')

@app.route('/names')
def names():
    engine = create_engine("sqlite:///belly_button_biodiversity.sqlite")

    session = Session(engine)

    inspector = inspect(engine)

    Base = automap_base()

    Base.prepare(engine, reflect=True)

    Main_data = Base.classes.samples_metadata
    sample_data = Base.classes.samples
    bacteria_data = Base.classes.otu

    names = session.query(Main_data).limit(5).all()
    names_list = []
    for name in names:
        #print(name.SAMPLEID)
        names_list.append(name.SAMPLEID)

    return jsonify(names_list)

@app.route('/otu')
def otu():
    engine = create_engine("sqlite:///belly_button_biodiversity.sqlite")

    session = Session(engine)

    inspector = inspect(engine)

    Base = automap_base()

    Base.prepare(engine, reflect=True)

    Main_data = Base.classes.samples_metadata
    sample_data = Base.classes.samples
    bacteria_data = Base.classes.otu

    OTU_desc = session.query(bacteria_data).limit(5).all()

    otu_list = []
    for x in OTU_desc:
        #print(x.lowest_taxonomic_unit_found)
        otu_list.append(x.lowest_taxonomic_unit_found)
    return jsonify(otu_list)
    

@app.route('/metadata/<sample>')
def sample(sample):

    engine = create_engine("sqlite:///belly_button_biodiversity.sqlite")

    session = Session(engine)

    inspector = inspect(engine)

    Base = automap_base()

    Base.prepare(engine, reflect=True)

    Main_data = Base.classes.samples_metadata
    sample_data = Base.classes.samples
    bacteria_data = Base.classes.otu
  
    fulldata = session.query(Main_data).all()
    print(fulldata)
    sample_data=[]
    for x in fulldata:
        if x.SAMPLEID == sample:
            sample_data.append({
                "AGE": x.AGE,
                "BBTYPE": x.BBTYPE,
                "ETHNICITY": x.ETHNICITY,
                "GENDER": x.GENDER,
                "LOCATION": x.LOCATION,
                "SAMPLEID": x.SAMPLEID
            })
    return jsonify(sample_data)


if __name__ == "__main__":
    app.run(debug=True)