import datetime
import uuid
from functools import wraps
import jwt
from connections.connection import db
from flask import current_app as app
from flask import jsonify , make_response, request
from werkzeug.security import check_password_hash, generate_password_hash
from models.users import User
from models.seats import Seat
from models.bookings import Booking


app.config['SECRET_KEY'] = 'thisissecret'


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        
        token = None
                
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
            
        if not token:
            return jsonify({'msg': "Token is Missing..!!!!"}),300
        
        try:
            data = jwt.decode(token,app.config['SECRET_KEY'],algorithms=['HS256'])           
            
        except:
            return jsonify({'msg' : "Token is Invalid"}),404     
        
        return f(*args, **kwargs)
    
    return decorated


@app.route('/seatbookings/<public_id>', methods = ['GET','POST','PUT','DELETE'])
@token_required
def booking(public_id):
    
    # GET REQUEST
    if request.method == 'GET':
        
        user_data = User.query.filter_by(public_id=public_id).first()
    
        output = []
        data = {}
            
        data['user_id'] = user_data.user_id
        data['user_public_id'] = user_data.public_id
        data['user_name'] = user_data.user_name        
        data['user_email'] = user_data.user_email
        data['user_password'] = user_data.user_password     
        
        ticket_list = []
        seat_list = []
        
        for seat in user_data.seats_id:
            seat_d = {}
            # data['seat_no'] = seat.seat_no
            seat_no = seat.seat_no
            # data['seat_status'] = seat.seat_status
            seat_status = seat.seat_status
            
            seat_d['seat_no'] = seat_no
            seat_d['seat_status'] = seat_status
            seat_list.append(seat_d)
            
            data['seat'] = seat_list
            
            for booking in user_data.booking_id:
                
                ticket = {}
                
                booking_id = booking.booking_id
                booking_date = booking.booking_date
                booking_payment = booking.booking_payment
                booking_status = booking.booking_status
                
                ticket['booking_id'] = booking_id
                ticket['booking_date'] = booking_date
                ticket['booking_payment'] = booking_payment
                ticket['booking_status'] = booking_status

            
            ticket_list.append(ticket)            
           
            data['tickets'] = ticket_list
           
        output.append(data)   
            
        return jsonify({"Data":output}),200
    
    # POST REQUEST  
    if request.method == 'POST':       
        
        data = request.get_json()
        
        for x in data:
            if x == 'user_id':
                
                hashed_password = generate_password_hash(data['user_password'], method='sha256')
            
                new_user = User(user_id=data['user_id'],public_id=str(uuid.uuid4()),user_name=data['user_name'],user_password=hashed_password,user_email=data['user_email'])
                db.session.add(new_user)
                db.session.commit()
                
                return jsonify({'msg' : 'Data Created Successfully...!!!'})         
                
            elif x == 'seat_no':
                
                seat_data = Seat.query.filter_by(seat_no=data['seat_no']).first()
                
                if not seat_data:
                    
                    user_data = db.session.query(User).filter_by(public_id=public_id).first()
                    
                    seat_info = Seat(seat_no=data['seat_no'],seat_status="Booked",owner=user_data)
                    db.session.add(seat_info)
                    db.session.commit()
                    
                    b_date = data['booking_date']
                    d_date = data['departure_date']
                    
                    booking_info = Booking(booking_id=str(uuid.uuid4()),booking_date=datetime.datetime.strptime(b_date, "%d/%m/%y"),departure_date=datetime.datetime.strptime(d_date, "%d/%m/%y"), booking_payment=data['booking_payment'],booking_status="Booked",owner1=user_data)
                    db.session.add(booking_info)
                    db.session.commit()                    
                
                    return jsonify({'msg' : 'Data Created Successfully...!!!'})
                
                if seat_data:
                    return jsonify({"msg":"Sorry, Seat is already booked. Please Try for Another Seat"})
                
                if Seat.query.count() > 10:
                    return jsonify({"msg":"Sorry, All Seats are Booked...!!!"}),
                    
    
    #PUT REQUEST
    if request.method == 'PUT':
        
        data = request.get_json()       
            
        user_data = db.session.query(User).filter_by(public_id=public_id).first()
        
        for seat in user_data.seats_id:
            if seat.seat_no == data['seat_no']:
                
                for booking in user_data.booking_id:
                    if booking.booking_id == data['booking_id']:
                        current_date = data['booking_date']
                        booking.booking_date = datetime.datetime.strptime(current_date, "%d/%m/%y")
                
                        try:                
                            db.session.commit()
                        except Exception as e:
                            print('Exception: {}'.format(e))
                            
        return jsonify({'msg' : 'Data updated Successfully..!!!!'}),200


    # DELETE REQUEST    
    if request.method == 'DELETE':
        
        data = request.get_json()
    
        user_data = User.query.filter_by(public_id=public_id).first()
    
        for seat in user_data.seats_id:
            for booking in user_data.booking_id:
                
                db.session.delete(seat)                
                db.session.commit()
                db.session.delete(booking)
                db.session.commit()    
        
        return jsonify({'msg' : 'Data Deleted Successfully..!!!!'}),200
    
# To make user Login
    
@app.route('/seatbookings/login')
def login():
    
    auth = request.authorization       
        
    if not auth or not auth.username or not auth.password:
        return make_response('Could Not Verify',401,{'WWW-Authenticate' : 'Basic realm = "Login required"'})    

    user = User.query.filter_by(user_name=auth.username).first()
        
    if not user:
        return make_response('Could Not Verify',401,{'WWW-Authenticate' : 'Basic realm = "Login required"'}),300   
        
    if check_password_hash(user.user_password,auth.password):            
                    
        payload = {
                "username" : auth.username,
                'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=10),
                "public_id" : user.public_id    
                }
            
        secret = app.config['SECRET_KEY']
            
        token = jwt.encode(payload,secret)
            
        return jsonify({'token' : token})        
    
    return make_response('Could Not Verify',401,{'WWW-Authenticate' : 'Basic realm = "Login required"'}),300