from connections.connection import db
from sqlalchemy import Column,Integer,String,ForeignKey


class Seat(db.Model):
    
    __table_args__ = {"schema":"Task_3_dbo"}
    __table_name__ = "seat"
    
    seat_no = Column(Integer,primary_key=True,autoincrement=True,nullable=False)
    seat_status = Column(String,nullable=False)
    
    user_id = Column(Integer,ForeignKey('Task_3_dbo.user.user_id'))
    
    