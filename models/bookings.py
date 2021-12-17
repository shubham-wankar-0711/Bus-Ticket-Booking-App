from datetime import datetime

from sqlalchemy.sql.sqltypes import DateTime
from connections.connection import db
from sqlalchemy import Column,Integer,String,ForeignKey,DateTime


class Booking(db.Model):
    
    __table_args__ = {"schema":"Task_3_dbo"}
    __table_name__ = "booking"
    
    booking_id = Column(String,primary_key=True,nullable=False)
    booking_date = Column(DateTime,nullable=False)
    departure_date = Column(DateTime,nullable=False)
    booking_payment = Column(Integer,nullable=False)
    booking_status = Column(String(255),nullable=False)
    
    user_id = Column(Integer,ForeignKey('Task_3_dbo.user.user_id'))
    
    
    
    