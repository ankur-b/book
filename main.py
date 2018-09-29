from flask import Flask, render_template,request,redirect,url_for,session
import sqlite3

app = Flask(__name__)

conn = sqlite3.connect("Users.db")
c = conn.cursor()

c.execute("CREATE TABLE IF NOT EXISTS users (first_name text NOT NULL,last_name text NOT NULL,email text PRIMARY KEY NOT NULL, password text NOT NULL)")
c.close()
conn.close()

@app.route('/',methods=['GET', 'POST'])
def index():
    conn = sqlite3.connect("Users.db")
    c = conn.cursor()
    error = None
    if request.method == 'POST':
        fname = request.form['first_name']
        lname = request.form['last_name']
        email = request.form['email']
        passw = request.form['password']
        cpass = request.form['cpassword']
        if passw == cpass:
            c.execute("INSERT INTO users VALUES(?,?,?,?)",(fname,lname,email,passw))
            conn.commit()
            c.close()
            conn.close()
            return render_template('signin.html', error = None)
        else:
            c.close()
            conn.close()
            return render_template('signup.html', error = "Make Sure Your Password and Confirm is Equal")    
    c.close()
    conn.close()
    return render_template('signup.html')

@app.route('/signin' ,methods=['GET','POST'])
def signin():
    conn = sqlite3.connect("Users.db")
    c = conn.cursor()
    error = None
    if request.method == 'POST':
        print("hello worldcsxn l;")
        emai = request.form['email']
        passc = request.form['password']
        if emai == "ankur@ankurbarve.me" and passc == "abhi1234":
            return redirect(url_for('admin'))
        else:
            return redirect(url_for('user'))
    c.close()
    conn.close()
    return render_template('signin.html', error = error)

@app.route('/user')
def user():
    return render_template('user.html',username="allu")

@app.route('/admin')
def admin():
    return render_template('admin.html',username="admin")


if __name__ == '__main__':
   app.run(debug = True)
