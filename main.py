from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import mysql.connector
import os
import datetime
from geopy.distance import geodesic
import numpy as np
import folium
from sklearn.cluster import OPTICS
from sklearn.preprocessing import StandardScaler
from flask_socketio import SocketIO, emit, join_room, leave_room
from engineio.payload import Payload
Payload.max_decode_packets = 200
from werkzeug.utils import secure_filename
from flask import request as flask_request


app = Flask(__name__, static_url_path='/static')
app.secret_key = 'abcdef'


socketio = SocketIO(app)

_users_in_room = {} # stores room wise user list
_room_of_sid = {} # stores room joined by an used
_name_of_sid = {} # stores display name of users


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    charset="utf8",
    database="pot"
)


@app.route('/',methods=['POST','GET'])
def index():

    
    return render_template('index.html')

@app.route('/cus_log',methods=['POST','GET'])
def cus_log():

    msg=""
    if flask_request.method == 'POST':
        username = flask_request.form['username']
        password = flask_request.form['password']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM po_customer WHERE username = %s AND password = %s', (username, password))
        account = cursor.fetchone()
        
        if account:
            session['username'] = username
            session['user_type'] = 'customer'
            msg="success"  
        else:
            msg="fail"
    
    return render_template('cus_log.html', msg=msg)

@app.route('/cus_reg',methods=['POST','GET'])
def cus_reg():

    msg=""
    if flask_request.method=='POST':
        name=flask_request.form['name']
        address=flask_request.form['address']
        mobile=flask_request.form['mobile']
        email=flask_request.form['email']
        latitude=flask_request.form['latitude']
        longitude=flask_request.form['longitude']
        
        username=flask_request.form['username']
        password=flask_request.form['password']
        now = datetime.datetime.now()
        r_date = now.strftime("%Y-%m-%d")
        
        mycursor = mydb.cursor()
        mycursor.execute("SELECT count(*) FROM po_customer where username=%s",(username, ))
        cnt = mycursor.fetchone()[0]
        if cnt==0:
            mycursor.execute("SELECT max(id)+1 FROM po_customer")
            maxid = mycursor.fetchone()[0]
            if maxid is None:
                maxid=1
            sql = "INSERT INTO po_customer(id, name, address, mobile, email, latitude, longitude, username, password, reg_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (maxid, name, address, mobile, email, latitude, longitude, username, password, r_date)
            mycursor.execute(sql, val)
            mydb.commit()
            msg="success"
        else:
            msg="fail"

    
    return render_template('cus_reg.html', msg=msg)


@app.route('/pot_log',methods=['POST','GET'])
def pot_log():

    msg=""
    if flask_request.method == 'POST':
        username = flask_request.form['username']
        password = flask_request.form['password']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM po_potter WHERE username = %s AND password = %s', (username, password))
        account = cursor.fetchone()
        
        if account:
            session['username'] = username
            session['user_type'] = 'potter'
            msg="success"  
        else:
            msg="fail"

    
    return render_template('pot_log.html', msg=msg)

@app.route('/pot_reg',methods=['POST','GET'])
def pot_reg():

    msg=""
    if flask_request.method=='POST':
        shop=flask_request.form['shop']
        name=flask_request.form['name']
        address=flask_request.form['address']
        mobile=flask_request.form['mobile']
        email=flask_request.form['email']
        latitude=flask_request.form['latitude']
        longitude=flask_request.form['longitude']
        
        username=flask_request.form['username']
        password=flask_request.form['password']
        now = datetime.datetime.now()
        r_date = now.strftime("%Y-%m-%d")
        
        mycursor = mydb.cursor()
        mycursor.execute("SELECT count(*) FROM po_potter where username=%s",(username, ))
        cnt = mycursor.fetchone()[0]
        if cnt==0:
            mycursor.execute("SELECT max(id)+1 FROM po_potter")
            maxid = mycursor.fetchone()[0]
            if maxid is None:
                maxid=1
            sql = "INSERT INTO po_potter(id, shop, name, address, mobile, email, latitude, longitude, username, password, reg_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (maxid, shop, name, address, mobile, email, latitude, longitude, username, password, r_date)
            mycursor.execute(sql, val)
            mydb.commit()
            msg="success"
        else:
            msg="fail"

    return render_template('pot_reg.html', msg=msg)

@app.route('/admin',methods=['POST','GET'])
def admin():

    msg=""
    if flask_request.method == 'POST':
        username = flask_request.form['username']
        password = flask_request.form['password']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM po_admin WHERE username = %s AND password = %s', (username, password))
        account = cursor.fetchone()
        
        if account:
            session['username'] = username
            session['user_type'] = 'admin'
            msg="success"  
        else:
            msg="fail"
 
    return render_template('admin.html', msg=msg)



###################################################################################################################

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/post', methods=['POST', 'GET'])
def post():
    if 'username' not in session or session.get('user_type') != 'potter':
        print("Please log in as a admin to access the page.", 'danger')
        return redirect(url_for('pot_log'))
    
    dt=""
    food_type=None
    post_id=None
    username = session.get('username')
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM po_potter WHERE username = %s", (username,))
    data = cursor.fetchone()
    cursor.close()
    name=data[1]
    address=data[3]
    mobile=data[4]
    longitude=data[10]
    latitude=data[11]
    
    msg=""
    nearby_users = []
    num_nearby_users = 0
    provider_coords = None  # Initialize with a default value
    if request.method=='POST':
        product_type=request.form['product_type']
        product=request.form['product']
        price=request.form['price']
        quantity=request.form['quantity']
        message=request.form['message']
        if 'image' in request.files:
            image = request.files['image']

            if image and allowed_file(image.filename):
                filename = secure_filename(image.filename)
                image_path = 'D:/pottery/static/uploads/' + filename
                image.save(image_path)
        
                now = datetime.datetime.now()
                post_date=now.strftime("%B %d, %Y")
                post_time=now.strftime("%I:%M %p")
        
                mycursor = mydb.cursor()
        
                mycursor.execute("SELECT max(id)+1 FROM post")
                maxid = mycursor.fetchone()[0]
                if maxid is None:
                    maxid=1
                sql = "INSERT INTO post(id, product_type, product, price, message, name, address, mobile, post_date, post_time, username, longitude, latitude, quantity, image) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                val = (maxid, product_type, product, price, message, name, address, mobile, post_date, post_time, username, longitude, latitude, quantity, filename)
                mycursor.execute(sql, val)
                mydb.commit()

                msg="success"

        

                try:
                    provider_cursor = mydb.cursor(dictionary=True)
                    provider_cursor.execute("SELECT * FROM po_potter WHERE username = %s", (username,))
                    provider_data = provider_cursor.fetchone()
                    provider_cursor.close()

                    # Extract provider coordinates
           
                    provider_coords = (provider_data['latitude'], provider_data['longitude'])

                    print("Provider Coordinates:", provider_coords)

                    # Fetch all users with valid latitude and longitude
                    user_cursor = mydb.cursor(dictionary=True)
                    user_cursor.execute("SELECT username, latitude, longitude FROM po_customer WHERE latitude IS NOT NULL AND longitude IS NOT NULL")
                    all_users = user_cursor.fetchall()
                    user_cursor.close()

                    for user in all_users:
                        user_coords = (user['latitude'], user['longitude'])
                        distance = geodesic(provider_coords, user_coords).kilometers


                        if distance < 100:  # Adjust the distance threshold as needed
                            user_details = get_user_details(user['username'])  # Fetch additional details
                            if user_details:
                                nearby_users.append({
                                    'username': user['username'],
                                    'latitude': user['latitude'],
                                    'longitude': user['longitude'],
                                    'user_details': user_details 
                                }) 

                    # Count the number of nearby users
                    num_nearby_users = len(nearby_users)

                except Exception as e:
                    print(f"An error occurred: {e}")
    

    return render_template('post.html', msg=msg, nearby_users=nearby_users, num_nearby_users=num_nearby_users, provider_coords=provider_coords, username=username)



def get_user_details(username):
    try:
        user_cursor = mydb.cursor(dictionary=True)
        user_cursor.execute("SELECT * FROM po_customer WHERE username = %s", (username,))
        user_details = user_cursor.fetchone()
        user_cursor.close()
        return user_details
    except Exception as e:
        print(f"An error occurred while fetching user details: {e}")
        return None



@app.route('/my_post', methods=['GET', 'POST'])
def my_post():
    if 'username' not in session or session.get('user_type') != 'potter':
        print("Please log in as a admin to access the page.", 'danger')
        return redirect(url_for('potter_log'))

    
    username=session.get('username')

    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM post where username = %s",(username,))
    data3 = cursor.fetchall()
    cursor.close()

    

    return render_template('my_post.html', post=data3)





@app.route('/view_post', methods=['POST', 'GET'])
def view_post():
    if 'username' not in session or session.get('user_type') != 'customer':
        print("Please log in as a admin to access the page.", 'danger')
        return redirect(url_for('cus_log'))

    
    username = session.get('username')
    msg=""

    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM po_customer where username = %s", (username,))
    data2 = cursor.fetchone()
    cursor.close()

    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM post")
    post2 = cursor.fetchall()
    cursor.close()

    
    act=flask_request.args.get("act")
    if act=="call":
        
        pid=flask_request.args.get("pid")
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM post WHERE id = %s", (pid,))
        da = cursor.fetchone()
        cursor.close()
        product=da[2]
        price=da[4]
        shop=da[5]
        contact=da[7]
        pot_username=da[10]

        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM po_customer where username = %s", (username,))
        dat = cursor.fetchone()
        name=dat[1]
        mobile=dat[3]
        cursor.close()
                
        now = datetime.datetime.now()
        req_date=now.strftime("%B %d, %Y")
        
        
        mycursor = mydb.cursor()
        mycursor.execute("SELECT max(id)+1 FROM request")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
        sql = "INSERT INTO request(id, product, price, shop, contact, pot_username, name, mobile, username, req_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (maxid, product, price, shop, contact, pot_username, name, mobile, username, req_date)
        mycursor.execute(sql, val)
        mydb.commit()
        msg="success"



    valid_posts = []
    try:
        cursor = mydb.cursor(dictionary=True)
        cursor.execute("SELECT latitude, longitude FROM po_customer WHERE username = %s", (username,))
        user_location = cursor.fetchone()
        cursor.close()
        

        user_coords = (user_location['latitude'], user_location['longitude'])
        cursor = mydb.cursor(dictionary=True)
        cursor.execute("SELECT * FROM post WHERE longitude IS NOT NULL AND latitude IS NOT NULL")
        posts = cursor.fetchall()

        # Filter posts based on distance
        valid_posts = []
        for post in posts:
            post_coords = (post['latitude'], post['longitude'])
            distance = geodesic(user_coords, post_coords).kilometers
            if distance <200:  # Change the distance threshold as needed
                valid_posts.append(post)

        cursor.close()

    except Exception as e:
        print(f"An error occurred: {e}")
    

    return render_template('view_post.html', data2=data2, msg=msg, post=post2)




@app.route('/quantity', methods=['GET', 'POST'])
def quantity():
    if 'username' not in session or session.get('user_type') != 'customer':
        print("Please log in as a admin to access the page.", 'danger')
        return redirect(url_for('cus_log'))


    pid=request.args.get('pid')
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM post where id=%s", (pid, ))
    post2 = cursor.fetchone()
    product=post2[2]
    price=post2[4]
    shop=post2[5]
    contact=post2[7]
    pro_username=post2[10]
    cursor.close()


    username=session.get('username')
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM po_customer where username=%s", (username, ))
    po = cursor.fetchone()
    name=po[1]
    mobile=po[3]
    email=po[4]
    cursor.close()


    if request.method=='POST':

        quantity=request.form['quantity']

        quantity = int(quantity)
        price = float(price)

        total=quantity*price
        
        now = datetime.datetime.now()
        r_date = now.strftime("%Y-%m-%d")
        
        mycursor = mydb.cursor()
        
        mycursor.execute("SELECT max(id)+1 FROM po_book")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
        sql = "INSERT INTO po_book(id, product, price, shop, contact, pro_username, name, mobile, email, reg_date, total, username) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (maxid, product, price, shop, contact, pro_username, name, mobile, email, r_date, total, username)
        mycursor.execute(sql, val)
        mydb.commit()
        msg="success"
        session['maxid'] = maxid
        return redirect(url_for('payment'))
        

    return render_template('quantity.html')




@app.route('/payment', methods=['GET', 'POST'])
def payment():
    if 'username' not in session or session.get('user_type') != 'customer':
        print("Please log in as a admin to access the page.", 'danger')
        return redirect(url_for('cus_log'))

    msg=""
    total=""

    maxid=session.get('maxid')
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM po_book where id=%s", (maxid, ))
    po = cursor.fetchone()
    total=po[10]
    
    if request.method=='POST':
        payment=request.form['payment']
        
        cursor = mydb.cursor()
        cursor.execute("update po_book set payment=%s where id=%s",(payment, maxid))
        mydb.commit()
        msg="success"


    return render_template('payment.html', maxid=maxid, msg=msg, total=total)




@app.route('/orders', methods=['GET', 'POST'])
def orders():
    if 'username' not in session or session.get('user_type') != 'customer':
        print("Please log in as a admin to access the page.", 'danger')
        return redirect(url_for('cus_log'))

    username=session.get('username')
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM po_book where username=%s", (username, ))
    po = cursor.fetchall()

    return render_template('orders.html', po_book=po)



@app.route('/requests2', methods=['GET', 'POST'])
def requests2():
    if 'username' not in session or session.get('user_type') != 'customer':
        print("Please log in as a admin to access the page.", 'danger')
        return redirect(url_for('cus_log'))

    username=session.get('username')
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM request where username=%s", (username, ))
    po = cursor.fetchall()

    return render_template('requests2.html', request=po)





@app.route('/view_req', methods=['GET', 'POST'])
def view_req():
    if 'username' not in session or session.get('user_type') != 'potter':
        print("Please log in as a admin to access the page.", 'danger')
        return redirect(url_for('pot_log'))

    username=session.get('username')
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM request where pot_username=%s", (username, ))
    po1 = cursor.fetchall()

    if flask_request.method=='POST':
        aid=flask_request.form['aid']
        date=flask_request.form['date']
        time=flask_request.form['time']
        cursor = mydb.cursor()
        cursor.execute("update request set date=%s, time=%s where id=%s",(date, time, aid))
        mydb.commit()

    return render_template('view_req.html', request=po1)



@app.route('/view_order', methods=['GET', 'POST'])
def view_order():
    if 'username' not in session or session.get('user_type') != 'potter':
        print("Please log in as a admin to access the page.", 'danger')
        return redirect(url_for('pot_log'))

    username=session.get('username')
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM po_book where pro_username=%s", (username, ))
    po2 = cursor.fetchall()

    
    act=flask_request.args.get("act")
    if act=="ok":
        oid=flask_request.args.get("oid")
        cursor = mydb.cursor()
        cursor.execute("update po_book set status=1 where id=%s",(oid,))
        mydb.commit()
        print("successfully accepted")
        
    if act=="pro":
        oid=flask_request.args.get("oid")
        cursor = mydb.cursor()
        cursor.execute("update po_book set status=2 where id=%s",(oid,))
        mydb.commit()
        print("your account will be rejected")

    if act=="de":
        oid=flask_request.args.get("oid")
        cursor = mydb.cursor()
        cursor.execute("update po_book set status=3 where id=%s",(oid,))
        mydb.commit()
        print("your account will be rejected")

    return render_template('view_order.html', po_book=po2)


@app.route('/pot_req', methods=['GET', 'POST'])
def pot_req():
   

    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM po_potter")
    po2 = cursor.fetchall()

    
    act=flask_request.args.get("act")
    if act=="ok":
        oid=flask_request.args.get("oid")
        cursor = mydb.cursor()
        cursor.execute("update po_potter set action=1 where id=%s",(oid,))
        mydb.commit()
        print("successfully accepted")
        
    if act=="no":
        oid=flask_request.args.get("oid")
        cursor = mydb.cursor()
        cursor.execute("update po_potter set action=2 where id=%s",(oid,))
        mydb.commit()
        print("your account will be rejected")

    

    return render_template('pot_req.html', po_potter=po2)




@app.route('/ad_or', methods=['GET', 'POST'])
def ad_or():
    

    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM po_book")
    po2 = cursor.fetchall()

    
    

    return render_template('ad_or.html', po_book=po2)



###################################################################################################################




@app.route("/call", methods=["GET", "POST"])
def call():

    aid=request.args.get("aid")
    if request.method == "POST":
        room_id = request.form['room_id']
        cursor = mydb.cursor()
        cursor.execute("update request set link=%s where id=%s",(room_id, aid))
        mydb.commit()
        
        return redirect(url_for("entry_checkpoint", room_id=room_id, aid=aid))

    return render_template("call.html")

@app.route("/room/<string:room_id>/")
def enter_room(room_id):
    act=request.args.get("act")
    
    
    if room_id not in session:
        return redirect(url_for("entry_checkpoint", room_id=room_id))
    
    return render_template("chatroom.html", room_id=room_id, display_name=session[room_id]["name"], mute_audio=session[room_id]["mute_audio"], mute_video=session[room_id]["mute_video"])

@app.route("/room/<string:room_id>/checkpoint/", methods=["GET", "POST"])
def entry_checkpoint(room_id):
    

    username=""
    
    if request.method == "POST":
        mute_audio = request.form['mute_audio']
        mute_video = request.form['mute_video']
        session[room_id] = {"name": username, "mute_audio":mute_audio, "mute_video":mute_video}
        return redirect(url_for("enter_room", room_id=room_id))

    return render_template("chatroom_checkpoint.html", room_id=room_id)

@socketio.on("connect")
def on_connect():
    sid = request.sid
    print("New socket connected ", sid)
    

@socketio.on("join-room")
def on_join_room(data):
    sid = request.sid
    room_id = data["room_id"]
    display_name = session[room_id]["name"]
    
    # register sid to the room
    join_room(room_id)
    _room_of_sid[sid] = room_id
    _name_of_sid[sid] = display_name
    
    # broadcast to others in the room
    print("[{}] New member joined: {}<{}>".format(room_id, display_name, sid))
    emit("user-connect", {"sid": sid, "name": display_name}, broadcast=True, include_self=False, room=room_id)
    
    # add to user list maintained on server
    if room_id not in _users_in_room:
        _users_in_room[room_id] = [sid]
        emit("user-list", {"my_id": sid}) # send own id only
    else:
        usrlist = {u_id:_name_of_sid[u_id] for u_id in _users_in_room[room_id]}
        emit("user-list", {"list": usrlist, "my_id": sid}) # send list of existing users to the new member
        _users_in_room[room_id].append(sid) # add new member to user list maintained on server

    print("\nusers: ", _users_in_room, "\n")


@socketio.on("disconnect")
def on_disconnect():
    sid = request.sid
    room_id = _room_of_sid[sid]
    display_name = _name_of_sid[sid]

    print("[{}] Member left: {}<{}>".format(room_id, display_name, sid))
    emit("user-disconnect", {"sid": sid}, broadcast=True, include_self=False, room=room_id)

    _users_in_room[room_id].remove(sid)
    if len(_users_in_room[room_id]) == 0:
        _users_in_room.pop(room_id)

    _room_of_sid.pop(sid)
    _name_of_sid.pop(sid)

    print("\nusers: ", _users_in_room, "\n")


@socketio.on("data")
def on_data(data):
    sender_sid = data['sender_id']
    target_sid = data['target_id']
    if sender_sid != request.sid:
        print("[Not supposed to happen!] request.sid and sender_id don't match!!!")

    if data["type"] != "new-ice-candidate":
        print('{} message from {} to {}'.format(data["type"], sender_sid, target_sid))
    socketio.emit('data', data, room=target_sid)


@app.route('/logout')
def logout():
    
    session.clear()
    print("Logged out successfully", 'success')
    return redirect(url_for('index'))



if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)

