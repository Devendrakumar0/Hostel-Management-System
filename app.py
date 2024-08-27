from flask import Flask, render_template, request, session, redirect, url_for, flash, send_file
import pandas as pd
from flask_mail import *
import secrets
import os
from datetime import datetime
import smtplib
from email.message import EmailMessage
# import pywhatkit
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import secrets
from werkzeug.utils import secure_filename
import mysql.connector
from datetime import datetime
import os
from flask import render_template
from flask_socketio import SocketIO
import time
from flask_mail import Mail, Message
from flask import jsonify
import secrets
from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy




mydb = mysql.connector.connect(
    host="localhost", user="root", passwd="", database="hostel", charset='utf8', port=3306)
mycursor = mydb.cursor()

UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
 

# home page
@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/login')
# def login():
#     return render_template('login.html')

def generate_reset_token():
    return secrets.token_urlsafe(32)

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        studentemail = request.form['studentemail']
        password = request.form['password']
        sql = "select * from students where studentemail='%s' and password='%s'" % (
            studentemail, password)
        mycursor.execute(sql)
        results = mycursor.fetchall()
        if studentemail == 'management@gmail.com' and password == 'management':
            return render_template('students.html', msg="Login successfull")
        elif len(results) > 0:
            session['studentemail'] = studentemail
            print(session['studentemail'])
            return render_template('pay.html', msg="Login successfull")
        else:
            return render_template('login.html', error="Login Failed!!")
    return render_template('login.html')

# about page
@app.route('/about')
def about():
    return render_template('about.html')

# about page
@app.route('/gallery')
def gallery():
    return render_template('gallery.html')

#loading
# @app.route('/loading')
# def loading():
#     time.sleep(3)
#     return render_template('loading.html')

# manager login

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'www.devendrakumarpudi@gmail.com'
app.config['MAIL_PASSWORD'] = 'herr auni wyew xnqg'

mail = Mail(app)

@app.route("/management", methods=["POST", "GET"])
def management():
    if request.method == "POST":
        username = request.form['email']
        password = request.form['password']
        if username == 'management@gmail.com' and password == 'management':
            return render_template('managementhome.html', msg="Login successfull")
        else:
            return render_template('management.html', msg="Login Failed!!")
    return render_template('management.html')

#sudents 
@app.route("/students")
def students():
    return render_template('students.html')

# Add  students
@app.route("/addstudent", methods=["POST", "GET"])
def addstudent():
    profilepath = ""  # Initialize profilepath with a default value
    if request.method == "POST":
        studentname = request.form['studentname']
        studentemail = request.form['studentemail']
        Rollno = request.form['Rollno']
        year = request.form['year']
        sem = request.form['sem']
        branch = request.form['branch']
        password = request.form['password']
        password1 = request.form['Con_Password']
        contact = request.form['mobile']
        pcontact = request.form['pcontact']
        address = request.form['address']
        wifiname = request.form['wifiname']
        wifipassword = request.form['wifipassword']
        myfile = request.files['myfile']
        room_type = request.form['room_type']
        hostel_type = request.form['hostel_type']
        course = request.form['course']
        filename = myfile.filename  # Define filename here
        path = os.path.join("static/profiles/", filename)
        myfile.save(path)
        profilepath = "static/profiles/" + filename
        now = datetime.now()
        t = now.strftime("%H:%M:%S")
        current_date = datetime.now().date()
        print(current_date)
        print(t)
        if password == password1:
            sql = "select * from students where studentemail='%s' and password='%s'" % (
                studentemail, password)
            mycursor.execute(sql)
            data = mycursor.fetchall()
            print(data)
            if data == []:
                msg = Message('Aditya Hostels login Details', sender='www.devendrakumarpudi.com', recipients=[studentemail])
                msg.body = f"Hello {studentname},\n\nYour account has been successfully created with the following credentials:\n\nEmail: {studentemail}\nPassword: {password}\n\nPlease keep this information safe and do not share it with anyone.\n\nRegards,\nAditya Hostels"
                mail.send(msg)
                print(studentname, studentemail, password, address)
                sql = "insert into students(studentname,studentemail,Rollno,year,sem,branch,password,contact,pcontact,address,wifiname,wifipassword,Date,Time,profile,room_type,hostel_type,course)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                val = (studentname, studentemail, Rollno, year, sem, branch, password, contact,
                       pcontact, address, wifiname, wifipassword, current_date, t, profilepath, room_type, hostel_type, course)
                mycursor.execute(sql, val)
                mydb.commit()
                return render_template('addstudent.html', msg="data added successfully")
            else:
                flash('Details already Exist', "warning")
                return render_template('addstudent.html', msg="Details already Exist")
        else:
            msg = "Passwords do not match."
            flash(msg, "error")
            return render_template('addstudent.html')
    return render_template('addstudent.html')

# view added students
@app.route("/viewaddedstudents")
def viewaddedstudents():
    sql = "select * from students"
    data = pd.read_sql_query(sql, mydb)
    print(data)
    return render_template('viewaddedstudents.html', data=data)

#delete Student
@app.route('/deletestudent/<string:Rollno>')
def deletestudent(Rollno=''):
    try:
        # Delete the student from the allocation table using the roll number
        sql_delete_allocation = "DELETE FROM allocations WHERE Rollno = %s"
        mycursor.execute(sql_delete_allocation, (Rollno,))

        # Delete the student from the students table using the roll number
        sql_delete_student = "DELETE FROM students WHERE Rollno = %s"
        mycursor.execute(sql_delete_student, (Rollno,))

        mydb.commit()
        return redirect(url_for('viewaddedstudents'))
    except Exception as e:
        # If an error occurs, rollback the transaction and handle the error
        mydb.rollback()
        print("Error deleting student:", e)
        return "An error occurred while deleting the student."

# update student deatils
@app.route("/updatestudents/<int:id>", methods=["POST", "GET"])
def updatestudents(id=0):
    sql = "select * from students where id='%s'" % (id)
    mycursor.execute(sql)
    data = mycursor.fetchall()
    print(data)
    return render_template('updatestudents.html',id=data[0][0], data=data)

# update student deatils
@app.route('/updatedetails', methods=["POST", "GET"])
def updatedetails():
    if request.method == "POST":
        id = request.form['id']
        studentname = request.form['studentname']
        studentemail = request.form['studentemail']
        Rollno = request.form['Rollno']
        year = request.form['year']
        sem = request.form['sem']
        branch = request.form['branch']
        contact = request.form['mobile']
        pcontact = request.form['pcontact']
        address = request.form['address']
        wifiname = request.form['wifiname']
        wifipassword = request.form['wifipassword']
        myfile = request.files['myfile']
        filename = myfile.filename  # Define filename here
        path = os.path.join("static/profiles/", filename)
        myfile.save(path)
        profilepath = "static/profiles/" + filename  # Define filename here

        sql = "UPDATE students SET studentname=%s, studentemail=%s,Rollno=%s,year=%s,sem=%s,branch=%s, contact=%s,pcontact=%s, address=%s,wifiname=%s,wifipassword=%s,profile=%s WHERE id=%s"
        val = (studentname, studentemail, Rollno, year, sem, branch, contact,
               pcontact, address, wifiname, wifipassword, profilepath, id)
        mycursor.execute(sql, val)
        mydb.commit()
        return redirect(url_for('viewaddedstudents'))

#blocks
@app.route("/blocks")
def blocks():
    return render_template('blocks.html')

# Add Blocks
@app.route("/addblocks", methods=["POST", "GET"])
def addblocks():
    profilepath = ""  # Initialize profilepath with a default value
    if request.method == "POST":
        hostel_type = request.form['hostel_type']
        roomnumber = request.form['roomnumber']
        blockname = request.form['blockname']
        wordenname = request.form['wordenname']
        wordernumber = request.form['wordernumber']
        wordenemail = request.form['wordenemail']

        # Check if the block already exists in the database
        # if block_exists(blockname):
        #     return render_template('addblocks.html', message='Block already exists.')

        # Check if the block is a boys block and the total boys blocks are less than 6
        # if hostel_type.lower() == 'boys' :and count_blocks('boys') >= 6
        #     return render_template('error.html', message='Cannot add more than 6 boys blocks.')

        # # Check if the block is a girls block and the total girls blocks are less than 3
        # elif hostel_type.lower() == 'girls' and count_blocks('girls') >= 3:
        #     return render_template('error.html', message='Cannot add more than 3 girls blocks.')

        # If the block is allowed, insert into the database
        if(hostel_type.lower() == 'girls' or hostel_type.lower() == 'boys'):
            sql = "INSERT INTO blocks(hostel_type, roomnumber, blockname, wordenname, wordernumber, wordenemail) VALUES (%s, %s, %s, %s, %s, %s)"
            val = (hostel_type, roomnumber, blockname,
                   wordenname, wordernumber, wordenemail)
            mycursor.execute(sql, val)
            mydb.commit()
            return render_template('addblocks.html', message='Block added successfully.')

    return render_template('addblocks.html')

# view Blocks
@app.route("/viewblocks")
def viewblocks():
    sql = "select * from blocks"
    data = pd.read_sql_query(sql, mydb)
    print(data)
    return render_template('viewblocks.html', data=data)

#view all boys blocks
@app.route("/viewallboysblocks")
def viewallboysblocks():
    sql = "select * from blocks where hostel_type ='boys'"
    data = pd.read_sql_query(sql, mydb)
    print(data)
    return render_template('viewallboysblocks.html', data=data)

#view B Block boys

# view Boys Blocks
@app.route("/viewboysblocks")
def viewboysblocks():
    sql = "select * from allocations where hostel_type='BOYS HOSTEL'"
    data = pd.read_sql_query(sql, mydb)
    print(data)
    return render_template('viewboysblocks.html', data=data)
#view A block boys
@app.route("/viewAblockboys")
def viewAblockboys():
    sql = "select * from allocations where blockname='Block A' and hostel_type='BOYS HOSTEL'"
    data = pd.read_sql_query(sql, mydb)
    print(data)
    return render_template('viewboysblocks.html', data=data)

#view B block boys
@app.route("/viewBblockboys")
def viewBblockboys():
    sql = "select * from allocations where blockname='Block B' and hostel_type='BOYS HOSTEL'"
    data = pd.read_sql_query(sql, mydb)
    print(data)
    return render_template('viewboysblocks.html', data=data)

#view C block boys
@app.route("/viewCblockboys")
def viewCblockboys():
    sql = "select * from allocations where blockname='Block C' and hostel_type='BOYS HOSTEL'"
    data = pd.read_sql_query(sql, mydb)
    print(data)
    return render_template('viewboysblocks.html', data=data)

#view D block boys
@app.route("/viewDblockboys")
def viewDblockboys():
    sql = "select * from allocations where blockname='Block D' and hostel_type='BOYS HOSTEL'"
    data = pd.read_sql_query(sql, mydb)
    print(data)
    return render_template('viewboysblocks.html', data=data)

#view E block boys
@app.route("/viewEblockboys")
def viewEblockboys():
    sql = "select * from allocations where blockname='Block E' and hostel_type='BOYS HOSTEL'"
    data = pd.read_sql_query(sql, mydb)
    print(data)
    return render_template('viewboysblocks.html', data=data)

#view F block boys
@app.route("/viewFblockboys")
def viewFblockboys():
    sql = "select * from allocations where blockname='Block F' and hostel_type='BOYS HOSTEL'"
    data = pd.read_sql_query(sql, mydb)
    print(data)
    return render_template('viewboysblocks.html', data=data)


# view all girls blocks
@app.route("/viewallgirlsblocks")
def viewallgirlsblocks():
    sql = "select * from blocks where hostel_type ='GIRLS HOSTEL'"
    data = pd.read_sql_query(sql, mydb)
    print(data)
    return render_template('viewallgirlsblocks.html', data=data)

# view Girls Blocks
@app.route("/viewgirlsblocks")
def viewgirlsblocks():
    sql = "select * from allocations where hostel_type ='GIRLS HOSTEL'"
    data = pd.read_sql_query(sql, mydb)
    print(data)
    return render_template('viewgirlsblocks.html', data=data)

# view A Girls Block
@app.route("/viewAgirlsblocks")
def viewAgirlsblocks():
    sql = "select * from allocations where hostel_type ='GIRLS HOSTEL' and blockname='Block A'"
    data = pd.read_sql_query(sql, mydb)
    print(data)
    return render_template('viewgirlsblocks.html', data=data)

# view B Girls Block
@app.route("/viewBgirlsblocks")
def viewBgirlsblocks():
    sql = "select * from allocations where hostel_type ='GIRLS HOSTEL' and blockname='Block B'"
    data = pd.read_sql_query(sql, mydb)
    print(data)
    return render_template('viewgirlsblocks.html', data=data)

# view C Girls Block
@app.route("/viewCgirlsblocks")
def viewCgirlsblocks():
    sql = "select * from allocations where hostel_type ='GIRLS HOSTEL' and blockname='Block C'"
    data = pd.read_sql_query(sql, mydb)
    print(data)
    return render_template('viewgirlsblocks.html', data=data)

#foodmenu
@app.route('/foodmenu')
def foodmenu():
    return render_template('foodmenu.html')


# Add food menu
@app.route("/addfoodtypes", methods=["POST", "GET"])
def addfoodtypes():
    print("**************")
    if request.method == "POST":
        foodtypes = request.form['foodtypes']
        session['foodtypes'] = foodtypes
        print(session['foodtypes'])
        if foodtypes == "1":  # Tiffin
            print("&&&&&&&&&&")
            foodmenu = request.form['foodmenu']
            session['foodmenu'] = foodmenu
            print(session['foodmenu'])
            foodname = request.form['foodname']
            aboutfood = request.form['aboutfood']
            ingredients = request.form['ingredients']
            myfile = request.files['myfile']
            filename = myfile.filename
            path = os.path.join("static/profiles/", filename)
            myfile.save(path)
            profilepath = "static/profiles/" + filename
            status = 'pending'
            now = datetime.now()
            t = now.strftime("%H:%M:%S")
            current_date = datetime.now().date()
            print(current_date)
            print(t)
            sql = "INSERT INTO foodtypes(Foodid,FoodType, Foodname, AboutFood,ingredients, FoodImage, Date, Time,status) VALUES (%s, %s, %s, %s, %s, %s, %s,%s,%s)"
            val = (foodtypes, foodmenu, foodname, aboutfood,
                   ingredients, profilepath, current_date, t, status)
            mycursor.execute(sql, val)
            mydb.commit()
            flash("Tiffin Item added successfully", "success")
        elif foodtypes == "2":  # Lunch
            foodmenu = request.form['foodmenu']
            session['foodmenu'] = foodmenu
            print(session['foodmenu'])
            foodname = request.form['foodname']
            aboutfood = request.form['aboutfood']
            ingredients = request.form['ingredients']
            myfile = request.files['myfile']
            filename = myfile.filename
            path = os.path.join("static/profiles/", filename)
            myfile.save(path)
            profilepath = "static/profiles/" + filename
            status = 'pending'
            now = datetime.now()
            t = now.strftime("%H:%M:%S")
            current_date = datetime.now().date()
            print(current_date)
            print(t)
            sql = "INSERT INTO foodtypes(Foodid,FoodType, Foodname, AboutFood,ingredients, FoodImage, Date, Time,status) VALUES (%s, %s, %s, %s, %s, %s, %s,%s,%s)"
            val = (foodtypes, foodmenu, foodname, aboutfood,
                   ingredients, profilepath, current_date, t, status)
            mycursor.execute(sql, val)
            mydb.commit()
            flash("Lunch Item added successfully", "success")
        elif foodtypes == "3":  # Snacks
            foodmenu = request.form['foodmenu']
            session['foodmenu'] = foodmenu
            print(session['foodmenu'])
            foodname = request.form['foodname']
            aboutfood = request.form['aboutfood']
            ingredients = request.form['ingredients']
            myfile = request.files['myfile']
            filename = myfile.filename
            path = os.path.join("static/profiles/", filename)
            myfile.save(path)
            profilepath = "static/profiles/" + filename
            status = 'pending'
            now = datetime.now()
            t = now.strftime("%H:%M:%S")
            current_date = datetime.now().date()
            print(current_date)
            print(t)
            sql = "INSERT INTO foodtypes(Foodid,FoodType, Foodname, AboutFood,ingredients, FoodImage, Date, Time,status) VALUES (%s, %s, %s, %s, %s, %s, %s,%s,%s)"
            val = (foodtypes, foodmenu, foodname, aboutfood,
                   ingredients, profilepath, current_date, t, status)
            mycursor.execute(sql, val)
            mydb.commit()
            flash("Snacks Item added successfully", "success")
        elif foodtypes == "4":  # Dinner
            foodmenu = request.form['foodmenu']
            session['foodmenu'] = foodmenu
            print(session['foodmenu'])
            foodname = request.form['foodname']
            aboutfood = request.form['aboutfood']
            ingredients = request.form['ingredients']
            myfile = request.files['myfile']
            filename = myfile.filename
            path = os.path.join("static/profiles/", filename)
            myfile.save(path)
            profilepath = "static/profiles/" + filename
            status = 'pending'
            now = datetime.now()
            t = now.strftime("%H:%M:%S")
            current_date = datetime.now().date()
            print(current_date)
            print(t)
            sql = "INSERT INTO foodtypes(Foodid,FoodType, Foodname, AboutFood,ingredients, FoodImage, Date, Time,status) VALUES (%s, %s, %s, %s, %s, %s, %s,%s,%s)"
            val = (foodtypes, foodmenu, foodname, aboutfood,
                   ingredients, profilepath, current_date, t, status)
            mycursor.execute(sql, val)
            mydb.commit()
            flash("Dinner Item added successfully", "success")
        else:
            flash("Invalid food type selected", "error")
        return redirect(url_for("addfoodtypes"))
    return render_template("foodtypes.html")

#View food menu After adding
@app.route("/viewfood")
def viewfood():
    sql = "SELECT * FROM foodtypes"
    data = pd.read_sql_query(sql, mydb)
    print(data)
    return render_template("viewfood.html", cols=data.columns.values, rows=data.values.tolist())

@app.route('/delete/<id>')
def delete(id=0):
    sql = "delete from foodtypes where id='%s' " % (id)
    mycursor.execute(sql)
    mydb.commit()
    return redirect(url_for('viewfood'))

@app.route('/deleteallocation/<int:id>')
def deleteallocation(id=0):
    sql = "delete from allocations where id='%s' " %(id)
    mycursor.execute(sql)
    mydb.commit()
    return redirect(url_for('manageboysblocks'))
    

@app.route('/allocation')
def allocation():
    return render_template('allocation.html')

#allocate the room for the student
@app.route('/allocate_students', methods=["POST", "GET"])
def allocate_students():
    sql = "SELECT * FROM students"
    mycursor.execute(sql)
    data = mycursor.fetchall()
    print(data)
    studentemail =data[0][2]
    print(studentemail)
    sql1 = "SELECT * FROM blocks"
    mycursor.execute(sql1)
    data1 = mycursor.fetchall()
    print(data1)
    if request.method == "POST":
        Rollno = request.form['Rollno']
        sql = "SELECT * FROM students WHERE Rollno = %s"
        mycursor.execute(sql, (Rollno,))
        student_data = mycursor.fetchone()
        print(student_data)
        studentname = student_data[1]
        studentemail = student_data[2]
        course = student_data[20]
        Year = student_data[4]
        branch = student_data[6]
        print((Rollno, studentname, studentemail, Year, branch))
        Room_type = request.form['room_type']
        roomnumber = request.form['roomnumber']
        blockname = request.form['blockname']
        wordenname = request.form['wordenname']
        hostel_type = request.form['hostel_type']
        print((Rollno, studentname, studentemail, Year, branch, roomnumber,
              blockname, wordenname, hostel_type, Room_type))
        mycursor.nextset()
        sql = "SELECT * FROM allocations WHERE Rollno = %s"
        mycursor.execute(sql, (Rollno,))
        existing_data = mycursor.fetchone()

        if existing_data:
            print(f"Student with Rollno {Rollno} already allocated.")
        else:
            sql = "INSERT INTO allocations(Rollno, studentname, studentemail, Year, branch, roomnumber, blockname, wordenname, room_type, hostel_type, course) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (Rollno, studentname, studentemail, Year, branch, roomnumber,
                    blockname, wordenname, Room_type, hostel_type, course)
            mycursor.execute(sql, val)
            mydb.commit()
            print(f"Data for Rollno {Rollno} inserted successfully.")

    return render_template('roomallocate.html', data=data, data1=data1)

@app.route('/get_student_details', methods=["POST"])
def get_student_details():
    if request.method == "POST":
        Rollno = request.form.get('Rollno')

        # Fetch student details from the database based on the selected rollno
        sql = "SELECT * FROM students WHERE Rollno = %s"
        mycursor.execute(sql, (Rollno,))
        student_data = mycursor.fetchone()

        if student_data:
            # Assuming the structure of student_data is (rollno, studentname, email, Year, branch, ...)
            response = {
                'studentname': student_data[1],
                'course' : student_data[20],
                'year': student_data[4],
                'branch': student_data[6],
                'hostel_type': student_data[18],
                'room_type': student_data[17],
                'studentemail' : student_data[2]
                # Add more fields as needed
            }
            return jsonify(response)

    # Handle invalid requests or errors
    return jsonify({'error': 'Invalid request'})

# manage allocation for student
@app.route("/manageallocation")
def manageallocation():
    sql = "SELECT * FROM allocations"
    data = pd.read_sql_query(sql, mydb)
    print(data)
    return render_template("manageallocation.html", data=data)

#View and manage boys block
@app.route("/manageboysblocks")
def manageboysblocks():
    sql = "select * from allocations where hostel_type ='BOYS HOSTEL'"
    data = pd.read_sql_query(sql, mydb)
    print(data)
    return render_template('manageboysblocks.html', data=data)

# Search Boys block with rollno
@app.route("/Searchblocks",methods=['POST','GET'])
def Searchblocks():
    if request.method=='POST':
        Rollno=request.form['Rollno']
        try:
            sql = "select * from allocations where Rollno='%s' " %(Rollno)
            print(sql)
	        # cursor.execute(sql)
            # mycursor.execute(sql)
            # results=mycursor.fetchall()
            # mydb.commit()
            # mydb.close()
            results=pd.read_sql_query(sql,mydb)
            results["action"]=""
            print(results)
            # result=results.drop(["user","dualaccess","dualaccessownerid","status"],axis=1)
            return render_template("viewboysblocks.html",data=results.values.tolist())
        except:
            return render_template("viewboysblocks.html",msg="not found")
    return render_template("viewboysblocks.html")

#update manage boys block
@app.route("/updatemanageboy/<int:id>", methods=["POST", "GET"])
def updatemanageboy(id=0):
    print(id)
    sql = "select * from allocations where id='%s'" % (id)
    mycursor.execute(sql)
    data = mycursor.fetchall()
    print(data)
    print("**************")
    sql1 = "SELECT * FROM blocks"
    mycursor.execute(sql1)
    data1 = mycursor.fetchall()
    print(data1)
    return render_template('updatemanageboys.html',id=data[0][0], data=data,data1=data1)

#update back
@app.route('/updateback', methods=['POST', 'GET'])
def updateback():
    sql = "select * from allocations"
    mycursor.execute(sql)
    data = mycursor.fetchall()
    print(data)
    print("*****")
    sql1 = "SELECT * FROM blocks"
    mycursor.execute(sql1)
    data1 = mycursor.fetchall()
    print(data1)
    if request.method == "POST":
        id = request.form['id']
        Rollno = request.form['Rollno']
        studentname = request.form['studentname']
        studentemail = request.form['studentemail']
        Year = request.form['Year']
        branch = request.form['branch']
        hostel_type = request.form['hostel_type']
        roomnumber = request.form['roomnumber']
        blockname = request.form['blockname']
        wordenname = request.form['wordenname']
        print(id, Rollno, studentname, Year, branch,
              hostel_type, roomnumber, blockname, wordenname)
        sql = "update allocations set Rollno='%s',studentname='%s',studentemail='%s',Year='%s',branch='%s',roomnumber='%s',blockname='%s',wordenname='%s',hostel_type='%s' where id='%s'" % (
             Rollno, studentname,studentemail, Year, branch, roomnumber,
              blockname, wordenname, hostel_type, id)
        mycursor.execute(sql)
        mydb.commit()
        return redirect('manageboysblocks')
    return render_template('updatemanageboys.html', data=data,data1=data1)


@app.route('/paypayment/<int:id>', methods=['POST', 'GET'])
def paypayment(id=0):
    sql = "select * from allocations where id='%s'" % (id)
    mycursor.execute(sql)
    data = mycursor.fetchall()
    print(data)
    # sql = "select * from allocations"
    # mycursor.execute(sql)
    # data1 = mycursor.fetchall()
    # print(data1)
    return render_template("paypayment.html",data=data)

#montly fee paymnet
@app.route('/paypaymentback', methods=['POST', 'GET'])
def paypaymentback():
    sql = "select * from allocations"
    # paypayment where studentemail='%s'"%session['studentemail']   
    mycursor.execute(sql)
    data = mycursor.fetchall()
    print(data)
    if request.method == 'POST':
        id = request.form['id']
        Rollno = request.form['Rollno']
        studentname = request.form['studentname']
        studentemail = request.form['studentemail']
        hostelfee = float(request.form['hostelfee'])
        currentbill = float(request.form['currentbill'])
        total_amount = hostelfee + currentbill

        # Insert the payment details into the database
        insert_sql = "INSERT INTO paypayment (Rollno,studentname,studentemail,hostelfee, currentbill, total_amount, Date) VALUES (%s, %s, %s,%s, %s, %s, %s)"
        insert_val = (Rollno,studentname,studentemail,hostelfee, currentbill, total_amount, datetime.now().date())
        data = mycursor.execute(insert_sql, insert_val)
        mydb.commit()
        print(data)
        flash("Payment Details added successfully", 'success')
        return redirect('manageboysblocks')
    return render_template('paypayment.html', data=data)


#View and manage girls block
@app.route("/managegirlsblocks")
def managegirlsblocks():
    sql = "select * from allocations where hostel_type ='GIRLS HOSTEL'"
    data = pd.read_sql_query(sql, mydb)
    print(data)
    return render_template('managegirlsblocks.html', data=data)

# Search Boys block with rollno
@app.route("/Searchgilesblocks",methods=['POST','GET'])
def Searchgilesblocks():
    if request.method=='POST':
        Rollno=request.form['Rollno']
        try:
            sql = "select * from allocations where Rollno='%s' " %(Rollno)
            print(sql)
            # cur,db = mydb()
            results=pd.read_sql_query(sql,db)
            # cur.close()
            # db.commit()
            # db.close()
            results["action"]=""
            # x = results.drop(["Files"], axis=1)
            # print(x)
            # result=results.drop(["user","dualaccess","dualaccessownerid","status"],axis=1)
            print(results)
    #         return render_template("SearchgirlsDisplay.html", col_name=results.columns.values,row_val=results.values.tolist())
    #     except:
    #         return render_template("viewgirlsblocks.html",msg="not found")
    # return render_template("viewgirlsblocks.html")
            return render_template("viewgirlsblocks.html",data=results.values.tolist())
        except:
            return render_template("viewboysblocks.html",msg="not found")
    return render_template("viewgirlsblocks.html")

#update manage boys block
@app.route("/updatemanagegirls/<int:id>", methods=["POST", "GET"])
def updatemanagegirls(id=0):
    print(id)
    sql = "select * from allocations where id='%s'" % (id)
    mycursor.execute(sql)
    data = mycursor.fetchall()
    print(data)
    print("**************")
    sql1 = "SELECT * FROM blocks"
    mycursor.execute(sql1)
    data1 = mycursor.fetchall()
    print(data1)
    return render_template('updatemanagegirls.html',id=data[0][0], data=data,data1=data1)

#update back
@app.route('/updatebackgirls', methods=['POST', 'GET'])
def updatebackgirls():
    sql = "select * from allocations"
    mycursor.execute(sql)
    data = mycursor.fetchall()
    print(data)
    print("*****")
    sql1 = "SELECT * FROM blocks"
    mycursor.execute(sql1)
    data1 = mycursor.fetchall()
    print(data1)
    if request.method == "POST":
        id = request.form['id']
        Rollno = request.form['Rollno']
        studentname = request.form['studentname']
        studentemail = request.form['studentemail']
        Year = request.form['Year']
        branch = request.form['branch']
        Block = request.form['Block']
        # Blocknumber = request.form['Blocknumber']
        Blockname = request.form['Blockname']
        wordenname = request.form['wordenname']
        print(id, Rollno, studentname, Year, branch,
              Block, Blockname, wordenname)
        sql = "update allocations set Rollno='%s',studentname='%s',studentemail='%s',Year='%s',branch='%s',Block='%s',Blockname='%s',wordenname='%s' where id='%s'" % (
             Rollno, studentname,studentemail, Year, branch,
              Block, Blockname, wordenname, id)
        mycursor.execute(sql)
        mydb.commit()
        return redirect('managegirlsblocks')
    return render_template('updatemanagegirls.html', data=data,data1=data1)


@app.route('/paypaymentgirls/<int:id>', methods=['POST', 'GET'])
def paypaymentgirls(id=0):
    sql = "select * from allocations where id='%s'" % (id)
    mycursor.execute(sql)
    data = mycursor.fetchall()
    print(data)
    # sql = "select * from allocations"
    # mycursor.execute(sql)
    # data1 = mycursor.fetchall()
    # print(data1)
    return render_template("paypaymentgirls.html",data=data)

#montly fee paymnet
@app.route('/paypaymentbackgirls', methods=['POST', 'GET'])
def paypaymentbackgirls():
    sql = "select * from allocations"
    mycursor.execute(sql)
    data = mycursor.fetchall()
    print(data)
    if request.method == 'POST':
        id = request.form['id']
        Rollno = request.form['Rollno']
        studentname = request.form['studentname']
        studentemail = request.form['studentemail']
        hostelfee = float(request.form['hostelfee'])
        currentbill = float(request.form['currentbill'])
        total_amount = hostelfee + currentbill

        # Insert the payment details into the database
        insert_sql = "INSERT INTO paypayment (Rollno,studentname,studentemail,hostelfee, currentbill, total_amount, Date) VALUES (%s, %s, %s,%s, %s, %s, %s)"
        insert_val = (Rollno,studentname,studentemail,hostelfee, currentbill, total_amount, datetime.now().date())
        data = mycursor.execute(insert_sql, insert_val)
        mydb.commit()
        print(data)
        flash("Payment Details added successfully", 'success')
        return redirect('managegirlsblocks')
    return render_template('paypaymentbackgirls.html', data=data)

# studen login page
@app.route("/student", methods=["POST", "GET"])
def student():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        sql = "select * from students where email='%s' and password='%s'" % (
            email, password)
        mycursor.execute(sql)
        results = mycursor.fetchall()

        if len(results) > 0:
            session['studentemail'] = email
            print(session['studentemail'])
            return render_template('profile.html', msg="Login successfull")
        else:
            return render_template('student.html', msg="Login failed")
    return render_template('student.html')

# studemt  home page and view profile
@app.route('/profile')
def profile():
    sql = "select * from students where studentemail='" + session['studentemail'] + "'"
    data = pd.read_sql_query(sql, mydb)
    print(data)
    return render_template('profile.html', cols=data.columns.values, rows=data.values.tolist())

#View all the food deatils
@app.route("/allfoodviewfood")
def allfoodviewfood():

    return render_template("allfoodviewfood.html")

#view tiffine
@app.route('/tiffine')
def tiffine():
    sql = "select * from foodtypes where Foodid='1'"
    data = pd.read_sql_query(sql, mydb)
    return render_template("tiffine.html", cols=data.columns.values, rows=data.values.tolist())

# View lunch
@app.route('/Lunch')
def Lunch():
    sql = "select * from foodtypes where Foodid='2'"
    data = pd.read_sql_query(sql, mydb)
    return render_template("Lunch.html", cols=data.columns.values, rows=data.values.tolist())

#view snacks
@app.route('/Snacks')
def Snacks():
    sql = "select * from foodtypes where Foodid='3'"
    data = pd.read_sql_query(sql, mydb)
    return render_template("Snacks.html", cols=data.columns.values, rows=data.values.tolist())

#view dinner
@app.route('/Dinner')
def Dinner():
    sql = "select * from foodtypes where Foodid='4'"
    data = pd.read_sql_query(sql, mydb)
    return render_template("Dinner.html", cols=data.columns.values, rows=data.values.tolist())

@app.route('/pay')
def pay():
    return render_template("pay.html")

@app.route('/payment')
def payment():
    sql = "select * from paypayment where stuemail='%s'"%session['studentemail'] 
    mycursor.execute(sql)
    data = mycursor.fetchall()
    print(data)
    return render_template("payment.html", data=data)

#payment
@app.route('/paymentback', methods=['POST', 'GET'])
def paymentback():
    sql = "select * from paypayment where studentemail='%s'"%session['studentemail']
    mycursor.execute(sql)
    data = mycursor.fetchall()
    print(data)
    if not data:
        return render_template("paymentn.html")
    if request.method == 'POST':
        id = request.form['id']
        Rollno = request.form['Rollno']
        studentname = request.form['studentname']
        studentemail = request.form['studentemail']
        hostelfee = request.form['hostelfee']
        currentbill = request.form['currentbill']
        totalamount = request.form['totalamount']
        Cardname = request.form['cardname']
        Cardnumber = request.form['cardnumber']
        expmonth = request.form['expmonth']
        cvv = request.form['cvv']
        # Get current date and time
        now = datetime.now()
        t = now.strftime("%H:%M:%S")
        current_date = now.date()
        status = 'pending'
        # Check if an entry for the current month already exists
        existing_entry_sql = "SELECT * FROM payment WHERE Rollno = %s AND MONTH(Date) = %s"
        existing_entry_val = (Rollno, current_date.month)
        mycursor.execute(existing_entry_sql, existing_entry_val)
        existing_entry = mycursor.fetchone()

        if existing_entry:
            # Entry for the current month already exists, handle accordingly
            flash("Payment for this month already Done. You cannot make another payment for the same month.", 'error')
        else:
            # Insert the new payment entry
            insert_sql = "INSERT INTO payment(Rollno, studentname, studentemail, totalamount, Cardname, Cardnumber, expmonth, cvv, Date, Time, hostelfee, currentbill, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            insert_val = (Rollno, studentname, studentemail, totalamount, Cardname, Cardnumber, expmonth, cvv, current_date, t, hostelfee, currentbill, status)
            mycursor.execute(insert_sql, insert_val)
            
            update_sql = "UPDATE paypayment SET status='Paid' WHERE studentemail=%s"
            update_val = (session['studentemail'],)
            mycursor.execute(update_sql, update_val)
            
            update_sql1 = "UPDATE payment SET status='Paid' WHERE studentemail=%s"
            update_val1 = (session['studentemail'],)
            mycursor.execute(update_sql1, update_val1)
            mydb.commit()
            flash("Payment successfully recorded for the current month.", 'success')

    return render_template("payment.html",data=data)

#view payment
@app.route("/viewpayment")
def viewpayment():
    sql = "select * from payment where studentemail='%s'"%(session['studentemail'])
    mycursor.execute(sql)
    data = mycursor.fetchall()
    print(data)
    print("*********")
    return render_template("viewpayment.html", data=data)

#view students payments
@app.route("/viewstudentspayments")
def viewstudentspayments():
    # SQL query to select payment information and hostel_type
    sql = """
    SELECT pp.*, s.hostel_type
    FROM paypayment pp
    JOIN students s ON pp.studentemail = s.studentemail
    """
    # Execute the query and fetch data
    mycursor.execute(sql)
    data = mycursor.fetchall()

    # Convert the fetched data to a pandas DataFrame
    df = pd.DataFrame(data, columns=['id', 'Rollno', 'studentname', 'studentemail', 'hostelfee', 'currentbill', 'total_amount', 'Date', 'status', 'hostel_type'])

    # Print the DataFrame for debugging
    print(df)

    # Pass the DataFrame to the template
    return render_template("viewstudentspayments.html", data=df)

#receipt template
@app.route("/receipt_template")
def receipt_template():
    sql = "select * from payment where studentemail='%s'"%(session['studentemail'])
    mycursor.execute(sql)
    data = mycursor.fetchall()
    print(data)
    return render_template("receipt_template.html", data=data)
    
#outpass request
@app.route('/outpass', methods=['POST', 'GET'])
def outpass():
    pcontact = None
    roomnumber = None
    if request.method == 'POST':
        studentemail = session['studentemail']
        outdate = request.form['outdate']
        outtime = request.form['outtime']
        reason = request.form['reason']
        pcontact = request.form['pcontact']
        destination = request.form['destination']
        roomnumber = request.form['roomnumber']
        
        # Convert the input date string to a datetime object
        # outdate_datetime = datetime.strptime(outdate, '%Y-%m-%d')
        
        # Query to fetch parent number from students table
        student_query = "SELECT pcontact FROM students WHERE studentemail = %s"
        mycursor.execute(student_query, (studentemail,))
        pcontact = mycursor.fetchone()[0]
        
        # Query to fetch room number from allocations table
        allocation_query = "SELECT roomnumber FROM allocations WHERE studentemail = %s"
        mycursor.execute(allocation_query, (studentemail,))
        roomnumber = mycursor.fetchone()[0] 

        # Check if a record with the same email and date already exists
        existing_entry_sql = "SELECT * FROM outpass WHERE studentemail = %s AND outdate = %s"
        existing_entry_val = (studentemail, outdate)
        mycursor.execute(existing_entry_sql, existing_entry_val)
        existing_entry = mycursor.fetchone()
        
        if existing_entry:
            flash("Out pass request already exists for this date.", 'error')
        else:
            # Insert the new outpass entry
            insert_sql = "INSERT INTO outpass(studentemail, outdate, outtime, reason, pcontact, Date, Time, destination, roomnumber) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            insert_val = (studentemail, outdate, outtime, reason, pcontact,
                          datetime.now().date(), datetime.now().strftime("%H:%M:%S"), destination, roomnumber)
            mycursor.execute(insert_sql, insert_val)
            mydb.commit()
            flash("Out pass Request has been sent to admin", 'success')

    return render_template("outpass.html", pcontact=pcontact, roomnumber=roomnumber)

# View all the student by students
@app.route('/viewalocationstudent')
def viewalocationstudent():
    try:
        cursor = mydb.cursor(dictionary=True)
        student_email = session['studentemail']
        cursor.execute("SELECT roomnumber, hostel_type FROM allocations WHERE studentemail = %s", (student_email,))
        room_info = cursor.fetchone()
        if room_info:
            room_number = room_info['roomnumber']
            hostel_type = room_info['hostel_type']
            sql = "SELECT * FROM allocations WHERE roomnumber = %s AND hostel_type = %s"
            cursor.execute(sql, (room_number, hostel_type))
            student_details = cursor.fetchall()
            print(student_details)
            return render_template('viewalocationstudent.html', student_details=student_details)
        else:
            return "No room allocated for the student."
    except Exception as e:
        # Handle exceptions appropriately (e.g., database errors)
        print("Error:", e)
        return "An error occurred while processing your request."
    finally:
        # Close the cursor and database connection
        cursor.close()
    

#add feedback
@app.route('/feedback', methods=['POST', 'GET'])
def feedback():
    if request.method == 'POST':
        email = session['stuemail']
        feedback = request.form['feedback']
        reason = request.form['reason']
        # Convert the input date string to a datetime object

        insert_sql = "INSERT INTO feedback(email, feedback,reason, Date, Time) VALUES (%s,%s, %s, %s,%s)"
        insert_val = (email, feedback, reason, datetime.now(
        ).date(), datetime.now().strftime("%H:%M:%S"))
        mycursor.execute(insert_sql, insert_val)
        mydb.commit()
        flash("Feed back sent successfully", 'success')

    return render_template("feedback.html")

#raise a compalint
@app.route('/raisecomplaint', methods=['POST', 'GET'])
def raisecomplaint():
    profilepath = ""
    if request.method == 'POST':
        email = session['studentemail']
        complaint = request.form['complaint']
        description = request.form['description']
        roomnumber =request.form['roomnumber']
        myfile = request.files['myfile']
        filename = myfile.filename  # Define filename here
        path = os.path.join("static/complaint images/", filename)
        myfile.save(path)
        profilepath = "static/complaint images/" + filename
        insert_sql = "INSERT INTO complaints(email, complaint, description, roomnumber, image, Date, Time) VALUES (%s, %s, %s, %s, %s, %s,%s)"
        insert_val = (email, complaint, description, roomnumber, profilepath, datetime.now(
        ).date(), datetime.now().strftime("%H:%M:%S"),)
        mycursor.execute(insert_sql, insert_val)
        mydb.commit()
        flash("Complaint raised successfully", 'success')

    return render_template("raisecomplaint.html")

#view other details
@app.route('/otherdeatils')
def otherdeatils():
    return render_template("otherdeatils.html")

#view feed back by management
@app.route("/viewfeedback")
def viewfeedback():
    sql = "SELECT * FROM feedback"
    data = pd.read_sql_query(sql, mydb)
    print(data)
    return render_template("viewfeedback.html", data=data)

#view complaints
@app.route("/viewcomplaints")
def viewcomplaints():
    sql = "SELECT * FROM complaints"
    data = pd.read_sql_query(sql, mydb)
    print(data)
    return render_template("viewcomplaints.html", data=data)

#view raised complaints
@app.route("/viewraisedcomplaints")
def viewraisedcomplaints():
    sql = "SELECT * FROM complaints where email='%s'" % session['studentemail']
    data = pd.read_sql_query(sql, mydb)
    print(data)
    return render_template("viewraisedcomplaints.html", data=data)

@app.route("/update_complaint_status", methods=["POST"])
def update_complaint_status():
    # Get the complaint ID and action taken from the form submitted
    complaint_id = request.form.get("complaint_id")
    action_taken = request.form.get("action_taken")
    action_taken = action_taken.strip("'")
    complaint_id = complaint_id.strip("'")
    # Update the action_taken field in the complaints table
    sql = "UPDATE complaints SET action_taken= %s WHERE complaint_id= %s"
    cursor = mydb.cursor()
    cursor.execute(sql, (action_taken, complaint_id))
    mydb.commit()
    cursor.close()
    # Redirect the user back to the viewraisedcomplaints route after updating
    return redirect("/viewraisedcomplaints")



@app.route("/complaint_statistics")
def complaint_statistics():
    complaint_sql = """
    SELECT complaint, COUNT(complaint) AS count
    FROM complaints
    GROUP BY complaint
    """
    complaint_data = pd.read_sql_query(complaint_sql, mydb)

    action_taken_sql = """
    SELECT complaint, action_taken, COUNT(*) AS count
    FROM complaints
    GROUP BY complaint, action_taken
    """
    action_taken_data = pd.read_sql_query(action_taken_sql, mydb)

    complaint_chart_data = {
        'labels': complaint_data['complaint'].tolist(),
        'counts': complaint_data['count'].tolist()
    }

    action_taken_chart_data = { 'labels': complaint_data['complaint'].tolist(), 'yes': [int(x) for x in action_taken_data['count'][action_taken_data['action_taken'] == 'yes'].tolist()], 'no': [int(x) for x in action_taken_data['count'][action_taken_data['action_taken'] == 'no'].tolist()] }

    for i in range(len(action_taken_data)):
        complaint_index = action_taken_data['complaint'][i]

        if action_taken_data['action_taken'][i] == 'Yes':
            action_taken_chart_data['yes'][complaint_data['complaint'].tolist().index(complaint_index)] += action_taken_data['count'][i]
        elif action_taken_data['action_taken'][i] == 'No':
            action_taken_chart_data['no'][complaint_data['complaint'].tolist().index(complaint_index)] += action_taken_data['count'][i]

    return render_template("complaint_statistics.html", complaint_chart_data=complaint_chart_data, action_taken_chart_data=action_taken_chart_data)



#view optpass request
@app.route("/viewoutpass")
def viewoutpass():
    outpass_sql = "SELECT * FROM outpass"
    outpass_data = pd.read_sql_query(outpass_sql, mydb)
    students_sql = "SELECT studentemail FROM students"
    students_data = pd.read_sql_query(students_sql, mydb)
    
    merged_data = pd.merge(outpass_data, students_data, on='studentemail', how='inner')
    print(merged_data)
    return render_template("viewoutpass.html", data=merged_data)


#accept for outpass
@app.route("/accept/<id>")
def accept(id=0):
    print(id)
    sql = "select  * from outpass where id='%s'" % (id)
    mycursor.execute(sql)
    dc = mycursor.fetchall()
    print(dc)
    email = dc[0][1]
    print("*********")
    print(email)
    otp = "Your Outpass Request is accepted and this is your secret Key :"
    mail_content = 'Your Outpass request is Accepted  by Admin for out pass  and email is:' + email + ' '
    sender_address = 'www.devendrakumarpudi@gmail.com'
    # sender_address = 'www.devendrakumarpudi@gmail.com'
    #tojh crvj vtot iufp
    sender_pass = 'cbxv mofh nfzm oahh'
    receiver_address = email
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'Aditya Hostels'
    message.attach(MIMEText(mail_content, 'plain'))
    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.starttls()
    session.login(sender_address, sender_pass)
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    sql = "update outpass set status='Approve' where id='%s'" % (id)
    mycursor.execute(sql)
    mydb.commit()    
    return redirect(url_for('viewoutpass'))


@app.route("/rejected/<id>")
def rejected(id=0):
    print(id)
    sql = "select  * from outpass where id='%s'" % (id)
    mycursor.execute(sql)
    dc = mycursor.fetchall()
    print(dc)
    
    email = dc[0][1]

    print(email)
    print("********")
    otp = "Your Outpass Request is Rejected and this is your secret Key :"
    # skey = secrets.token_hex(4)
    # print("secret key", skey)
    mail_content = 'Your Outpass request is Rejected  by Admin and email is:' + email + ' '
    sender_address = 'www.devendrakumarpudi@gmail.com'
    sender_pass = 'cbxv mofh nfzm oahh'
    receiver_address = email
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'Hostel Management system'
    message.attach(MIMEText(mail_content, 'plain'))
    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.starttls()
    session.login(sender_address, sender_pass)
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()

    sql = "update outpass set status='Rejected' where id='%s'" % (id)
    mycursor.execute(sql)
    mydb.commit()

    return redirect(url_for('viewoutpass'))


@app.route('/updatedback', methods=["POST", "GET"])
def updatedback():
    if request.method == "POST":
        id = request.form['id']
        studentname = request.form['studentname']
        studentemail = request.form['stduentemail']
        Rollno = request.form['Rollno']
        year = request.form['year']
        sem = request.form['sem']
        branch = request.form['branch']
        contact = request.form['mobile']
        pcontact = request.form['pcontact']
        address = request.form['address']
        wifiname = request.form['wifiname']
        wifipassword = request.form['wifipassword']
        myfile = request.files['myfile']
        filename = myfile.filename  # Define filename here
        path = os.path.join("static/profiles/", filename)
        myfile.save(path)
        profilepath = "static/profiles/" + filename  # Define filename here

        sql = "UPDATE students SET studentname=%s, studentemail=%s,Rollno=%s,year=%s,sem=%s,branch=%s, contact=%s,pcontact=%s, address=%s,wifiname=%s,wifipassword=%s,profile=%s WHERE id=%s"
        val = (studentname, studentemail, Rollno, year, sem, branch, contact,
               pcontact, address, wifiname, wifipassword, profilepath, id)
        mycursor.execute(sql, val)
        mydb.commit()
        return redirect(url_for('viewaddedstudents'))



@app.route('/eventcalendar')
def eventcalendar():
    # sql = "SELECT * FROM events"
    # data = pd.read_sql_query(sql, mydb)
    # return render_template('eventcalendar.html', events=data.to_dict(orient='records'))
     return render_template('eventcalendar.html')


@app.route('/get_events')
def get_events():
    sql = "SELECT * FROM events"
    mycursor.execute(sql)
    events = mycursor.fetchall()
    event_list = []
    for event in events:
        event_dict = {
            'event_id': event[0],  # Assuming id is the first column in your events table
            'eventname': event[1],  # Assuming eventname is the second column
            'Date': event[2]  # Assuming Date is the third column
            # Add 'end' property if you have end date/time for events
        }
        event_list.append(event_dict)
    return jsonify(event_list)

@app.route('/add_event', methods=['GET', 'POST'])
def add_event():
    if request.method == 'POST':
        eventname = request.form['eventname']
        Date = request.form['Date']
        sql = "INSERT INTO events(eventname, Date) VALUES (%s, %s)"
        val = (eventname, Date)
        mycursor.execute(sql, val)
        mydb.commit()
        return jsonify({'message': 'Event added successfully'})
    else:
        return render_template('calendar.html')  # Render form for adding event


@app.route('/delete_event/<int:event_id>', methods=['POST'])
def delete_event(event_id):
    sql = "DELETE FROM events WHERE event_id = %s"
    val = (event_id,)
    mycursor.execute(sql, val)
    mydb.commit()
    return jsonify({'message': 'Event deleted successfully'})



# Assume you have a function to check if the block exists


# def block_exists(block_number):
#     # Your logic to check if the block exists in the database
#     # You may perform a database query or use any other method

#     # For example, let's assume mycursor is your database cursor
#     mycursor.execute(
#         "SELECT * FROM Blocks WHERE Blocknumber = %s", (block_number,))
#     result = mycursor.fetchone()

#     return result is not None


























def generate_token():
    return secrets.token_hex(16)





# forgot password 
@app.route("/forgotpassword", methods=['POST', 'GET'])
def forgotpassword():
    if request.method == 'POST':
        studentemail = request.form['studentemail']
        # Check if the email exists in the students table
        mycursor.execute("SELECT * FROM students WHERE studentemail = %s", (studentemail,))
        result = mycursor.fetchone()
        if result:
            token = generate_token()
            # Store the token in the database for the user
            mycursor.execute("UPDATE students SET reset_token = %s WHERE studentemail = %s", (token, studentemail))
            mydb.commit()
            msg = Message('Password Reset', sender='your_email@example.com', recipients=[studentemail])
            msg.body = f"Hello {result[1]},\n\nTo reset your password, please click the following link: {url_for('reset_password', token=token, _external=True)}\n\nIf you didn't request this, please ignore this email."
            mail.send(msg)
            flash('An email with instructions to reset your password has been sent.', 'info')
            return redirect(url_for('login'))
        else:
            flash('Email address not found.', 'error')
    return render_template('forgotpassword.html')



# Route for the password reset page
@app.route('/resetpassword/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if request.method == 'POST':
        new_password = request.form['new_password']
        # Check if the token is valid for the provided email address
        studentemail = request.form['studentemail']
        mycursor.execute("SELECT * FROM students WHERE studentemail = %s AND reset_token = %s", (studentemail, token))
        result = mycursor.fetchone()
        if result:
            # Update the password for the user in the database
            mycursor.execute("UPDATE students SET password = %s, reset_token = NULL WHERE studentemail = %s", (new_password, studentemail))
            mydb.commit()
            flash('Your password has been reset successfully.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Invalid or expired token.', 'error')
    # Pass the token to the template for the form action
    return render_template('resetpassword.html', token=token)

# update password 


@app.route("/updatepassword", methods=['POST', 'GET'])
def updatepassword():
    if request.method == "POST":
        form = request.form
        email = session['sforgotemail']
        password = form['password']
        confirmpassword = form['confirmpassword']
        if password == confirmpassword:
            sql = "select * from students where email='%s'" % (email)
            mycursor.execute(sql)
            data = mycursor.fetchall()
            mydb.commit()
            if data:
                sql = "update students set password='%s' where email='%s'" % (
                    password, session['sforgotemail'])
                mycursor.execute(sql)
                mydb.commit()
                flash("Password Updated Successfully", "success")
                return redirect(url_for("student"))
        else:
            return render_template("student.html")





















    




# @app.route("/managegirlsblocks")
# def managegirlsblocks():
#     sql = "select * from allocations where Block='girls'"
#     data = pd.read_sql_query(sql, mydb)
#     print(data)
#     return render_template('managegirlsblocks.html', data=data)


# @app.route("/Searchblocks",methods=["POST","GET"])
# def Searchblocks():
#     if request.method=="POST":
#         searchrollno = request.form['search']
#         newsql = "SELECT * FROM allocations WHERE Rollno='%s'" % (searchrollno)
#         data = pd.read_sql_query(newsql,mydb)
#         return render_template('viewmanagegirls.html', data=data)
#     return redirect("managegirlsblocks")


if __name__ == "__main__":
    app.run(debug=True)
