from connections.connection import db
from sqlalchemy import Column,Integer,String
from sqlalchemy.orm import relationship

class User(db.Model):
    
    __table_args__ = {"schema":"Task_3_dbo"}
    __table_name__ = "user"
    
    user_id = Column(Integer,primary_key=True,autoincrement=True,nullable=False)
    public_id = Column(String,nullable=False)
    user_name = Column(String(255),nullable=False)
    user_email = Column(String(255),nullable=False)
    user_password = Column(String(255),nullable=False)
    
    seats_id = relationship("Seat",backref="owner",lazy='dynamic')
    booking_id = relationship("Booking",backref="owner1",lazy='dynamic')
    

    
    