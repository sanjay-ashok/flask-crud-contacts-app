from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import os

# initializations
app = Flask(__name__)

# Mysql Connection
if os.environ.get('MYSQL_HOST'):
    app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST')
else:
    app.config['MYSQL_HOST'] = 'localhost'

if os.environ.get('MYSQL_USER'):
    app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER')
else:
    app.config['MYSQL_USER'] = 'root'

if os.environ.get('MYSQL_PASSWORD'):
    app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD')
else:
    app.config['MYSQL_PASSWORD'] = 'root'

if os.environ.get('MYSQL_DB'):
    app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB')
else:
    app.config['MYSQL_DB'] = 'flaskcrud'

mysql = MySQL(app)

# settings
app.secret_key = "mysecretkey"

# create contacts table
with app.app_context():
    stmt = "SHOW TABLES LIKE 'contacts';"
    cur = mysql.connection.cursor()
    cur.execute(stmt)
    result = cur.fetchone()
    if result:
        pass
    else:
        cur.execute('create table contacts( id int NOT NULL AUTO_INCREMENT, fullname varchar(255), phone varchar(255), email varchar(255), PRIMARY KEY (id));')
    cur.close()

# routes
@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts')
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', contacts = data)

@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO contacts (fullname, phone, email) VALUES (%s,%s,%s)", (fullname, phone, email))
        mysql.connection.commit()
        flash('Contact Added successfully')
        return redirect(url_for('Index'))

@app.route('/edit/<id>', methods = ['POST', 'GET'])
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts WHERE id = %s', (id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit-contact.html', contact = data[0])

@app.route('/update/<id>', methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE contacts
            SET fullname = %s,
                email = %s,
                phone = %s
            WHERE id = %s
        """, (fullname, email, phone, id))
        flash('Contact Updated Successfully')
        mysql.connection.commit()
        return redirect(url_for('Index'))

@app.route('/delete/<string:id>', methods = ['POST','GET'])
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contacts WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Contact Removed Successfully')
    return redirect(url_for('Index'))

# starting the app
if __name__ == "__main__":
    app.run(port=3000, debug=True, host='0.0.0.0')
