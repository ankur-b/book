from flask import Flask, render_template,request
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
        c.execute("INSERT INTO users VALUES(?,?,?,?)",(fname,lname,email,passw))
        c.close()
        conn.close()
        return render_template('signin.html', error = None)
    c.close()
    conn.close()
    return render_template('signup.html', error = error)



@app.route('/signin')
def signin():
    return render_template("signin.html")

if __name__ == '__main__':
   app.run(debug = True)
