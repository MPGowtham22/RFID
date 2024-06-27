from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

Base = declarative_base()

class RFIDTag(Base):
    __tablename__ = 'rfid_tags'
    id = Column(Integer, primary_key=True)
    tag_id = Column(String(50), unique=True, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

engine = create_engine('sqlite:///rfid_data.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
import serial
from database_setup import RFIDTag, session

# Replace '/dev/ttyUSB0' with the appropriate port for your RFID reader
ser = serial.Serial('/dev/ttyUSB0', 9600)

def read_rfid():
    while True:
        tag_id = ser.readline().strip().decode('utf-8')
        print(f'Tag read: {tag_id}')

        # Store in the database
        new_tag = RFIDTag(tag_id=tag_id)
        session.add(new_tag)
        session.commit()

if __name__ == "__main__":
    read_rfid()
from flask import Flask, render_template
from database_setup import RFIDTag, session

app = Flask(__name__)

@app.route('/')
def index():
    tags = session.query(RFIDTag).all()
    return render_template('index.html', tags=tags)

if __name__ == "__main__":
    app.run(debug=True)
