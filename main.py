from flask import Flask, render_template,request,redirect,url_for,session
import sqlite3
import goodreads_api_client as gr
import goodreads
import os
import requests
from xml.etree import ElementTree
import shutil

current = ""
adminCh = False
DevKey = 'UvqPf2fGbH2YoWaetp1bA'

app = Flask(__name__)

app.secret_key = '\xf0\xa5\x9ewe6\x82RU\x8b\t\x0b\xb6\xcc\xf8\xb2\xdb\x02\x83\xab\x0f\x13\x15'

conn = sqlite3.connect("Users.db")
c = conn.cursor()

c.execute("CREATE TABLE IF NOT EXISTS users (first_name text NOT NULL,last_name text NOT NULL,email text PRIMARY KEY NOT NULL, password text NOT NULL, username text NOT NULL)")
c.close()
conn.close()

@app.route('/',methods=['GET', 'POST'])
def index():
    conn = sqlite3.connect("Users.db")
    c = conn.cursor()
    if request.method == 'POST':
        if request.form.get('first_name'):
            fname = request.form['first_name']
            lname = request.form['last_name']
            email = request.form['email']
            passw = request.form['password']
            cpass = request.form['cpassword']
            uname = request.form['username']
            t = (email.lower(),)
            c.execute("SELECT email FROM users WHERE email = ?", t)
            checkEmail = c.fetchone()
            if checkEmail != None:
                c.close()
                conn.close()
                return render_template('signup.html', error = "Email already in use")
            t = (uname.lower(),)
            c.execute("SELECT username FROM users WHERE username = ?", t)
            checkUser = c.fetchone()
            if checkUser != None:
                c.close()
                conn.close()
                return render_template('signup.html', error = "Username already in use")
            c.execute("INSERT INTO users VALUES(?,?,?,?,?)",(fname,lname,email,passw,uname))
            conn.commit()
            c.close()
            conn.close()
            return redirect(url_for('signin'))
        if request.form.get('searchB'):
            searchB = request.form['searchB']
            searchB = list(searchB.split())
            qu = 'https://www.goodreads.com/search/index.xml?key='+DevKey+'&q='
            for i in searchB:
                qu = qu + i + "+"
            qu = qu.rstrip("+")
            response = requests.get(qu)
            tree = ElementTree.fromstring(response.content)
            noBooks = (tree[1][2].text)
            print (noBooks)
            if int(noBooks) == 0:
                c.close()
                conn.close()
                return redirect(url_for('noResults'))
            totList = {}
            for i in range(int(noBooks)):
                title = tree[1][6][i][-1][1].text
                author = tree[1][6][i][-1][2][1].text
                imgurl = tree[1][6][i][-1][3].text
                simgurl = tree[1][6][i][-1][4].text
                dict = {}
                dict['title'] = title
                dict['author'] = author
                dict['imgurl'] = imgurl
                dict['simgurl'] = simgurl
                totList[i] = dict
            print (totList)
            searchB = ' '.join(searchB)
            session['listRes'] = totList
            return redirect(url_for('result', totList = totList, sear = searchB))
    c.close()
    conn.close()
    if current != '':
        return render_template('user.html', username = current)
    return render_template('signup.html', error = '')

@app.route('/signin' ,methods=['GET','POST'])
def signin():
    conn = sqlite3.connect("Users.db")
    c = conn.cursor()
    global current
    if request.method == 'POST':
        emai = request.form['email']
        passc = request.form['password']
        if emai == "ankur@ankurbarve.me" and passc == "abhi1234":
            c.close()
            conn.close()
            global adminCh
            adminCh = True
            return redirect(url_for('admin'))
        else:
            t = (emai.lower(),)
            c.execute("SELECT email, username, password FROM users WHERE email = ?",t)
            checkLogin = c.fetchone()
            if checkLogin == None:
                c.execute("SELECT email, username, password FROM users WHERE lower(username) = ?",t)
                checkLogin = c.fetchone()
                if checkLogin != None:
                    if checkLogin[2] == passc:
                        c.close()
                        conn.close()
                        current = checkLogin[1]
                        session['logged_in'] = True
                        session['username'] = checkLogin[0]
                        return redirect(url_for('index'))
                    else:
                        c.close()
                        conn.close()
                        return render_template('signin.html', error = "Username and password do not match.")
                c.close()
                conn.close()
                return render_template('signin.html', error = "Username or Email address doesn't exist. Signup first.")
            if checkLogin[2] == passc:
                c.close()
                conn.close()
                current = checkLogin[1]
                session['logged_in'] = True
                session['username'] = checkLogin[0]
                print (session['username'])
                return redirect(url_for('index'))
            c.close()
            conn.close()
            return render_template('signin.html', error = "Email and password do not match.")
    if current != '':
        c.close()
        conn.close()
        return redirect(url_for('index'))
    c.close()
    conn.close()
    return render_template('signin.html', error = '')

@app.route('/admin')
def admin():
    global admin
    if adminCh == True:
        return render_template('admin.html', username="admin")
    else:
        return redirect(url_for('signin'))

@app.route('/result', methods = ['GET'])
def result():
    if request.method == 'GET':
        listRes = session['listRes']
        sear = request.args['sear']
        print(type(listRes))
        print(listRes)
        return render_template('searchResults.html', sear = sear, listRes = listRes)

@app.route('/noResults')
def noResults():
    return render_template('noResults.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    session['logged_in'] = False
    global adminCh
    global current
    adminCh = False
    current = ''
    return redirect(url_for('signin'))

if __name__ == '__main__':
    app.run(debug = True)
