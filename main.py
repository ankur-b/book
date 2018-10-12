from flask import Flask, render_template,request,redirect,url_for,session
import sqlite3
import goodreads_api_client as gr
import goodreads
import os

current = ""

app = Flask(__name__)

app.secret_key = '\xf0\xa5\x9ewe6\x82RU\x8b\t\x0b\xb6\xcc\xf8\xb2\xdb"\x02\x83\xab\x0f\x13\x15'

conn = sqlite3.connect("Users.db")
c = conn.cursor()

c.execute("CREATE TABLE IF NOT EXISTS users (first_name text NOT NULL,last_name text NOT NULL,email text PRIMARY KEY NOT NULL, password text NOT NULL)")
c.close()
conn.close()

@app.route('/',methods=['GET', 'POST'])
def index():
    conn = sqlite3.connect("Users.db")
    c = conn.cursor()
    if request.method == 'POST':
        fname = request.form['first_name']
        lname = request.form['last_name']
        email = request.form['email']
        passw = request.form['password']
        cpass = request.form['cpassword']
        t = (email,)
        c.execute("SELECT email FROM users WHERE email = ?", t)
        checkEmail = c.fetchone()
        print (checkEmail)
        if checkEmail != None:
            c.close()
            conn.close()
            return render_template('signup.html', error = "Email already in use")
        c.execute("INSERT INTO users VALUES(?,?,?,?)",(fname,lname,email,passw))
        conn.commit()
        c.close()
        conn.close()
        return redirect(url_for('signin'))
    c.close()
    conn.close()
    if current != '':
        return render_template('user.html', username = current)
    return render_template('signup.html', error = '')

@app.route('/signin' ,methods=['GET','POST'])
def signin():
    conn = sqlite3.connect("Users.db")
    c = conn.cursor()
    if request.method == 'POST':
        emai = request.form['email']
        passc = request.form['password']
        if emai == "ankur@ankurbarve.me" and passc == "abhi1234":
            c.close()
            conn.close()
            return redirect(url_for('admin'))
        else:
            t = (emai,)
            c.execute("SELECT email, password FROM users WHERE email = ?", t)
            checkLogin = c.fetchone()
            if checkLogin == None:
                c.close()
                conn.close()
                return render_template('signin.html', error = "Email address doesn't exist. Signup first.")
            if checkLogin[1] == passc:
                c.close()
                conn.close()
                global current
                current = checkLogin[0]
                session['logged_in'] = True
                session['username'] = checkLogin[0]
                return redirect(url_for('index'))
            c.close()
            conn.close()
            return render_template('signin.html', error = "Email and password do not match.")
    c.close()
    conn.close()
    return render_template('signin.html', error = '')

@app.route('/admin')
def admin():
    return render_template('admin.html',username="admin")

@app.route('/books')
def books():
    return reduced_book

@app.route('/logout')
def logout():
    session.pop('username', None)
    global current
    current = ''
    return redirect(url_for('signin'))

if __name__ == '__main__':
  app.run(debug = True)
