from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def auto_migrate():
    
    from models.users import User
    from models.seats import Seat
    from models.bookings import Booking

    
    db.create_all()
    db.session.commit()
    