from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL



app = Flask(__name__)
app.secret_key = 'many random bytes'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'data'

mysql = MySQL(app)



@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM STUDENTS")
    data = cur.fetchall()
    cur.close()




    return render_template('index.html', students=data )



@app.route('/insert', methods = ['POST'])
def insert():

    if request.method == "POST":
        flash("Data Inserted Successfully")
        name = request.form['name']
        room = request.form['room']
        device = request.form['device']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO STUDENTS (name, room, device) VALUES (%s, %s, %s)", (name, room, device))
        mysql.connection.commit()
        return redirect(url_for('Index'))




@app.route('/delete/<string:sno_data>', methods = ['GET'])
def delete(sno_data):
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM STUDENTS WHERE sno=%s", (sno_data))
    mysql.connection.commit()
    return redirect(url_for('Index'))





@app.route('/update',methods=['POST','GET'])
def update ():

    if request.method == 'POST':
        sno_data = request.form['id']
        name = request.form['name']
        room = request.form['room']
        device = request.form['device']
        cur = mysql.connection.cursor()
        cur.execute("""
               UPDATE STUDENTS
               SET name=%s, room=%s, device=%s
               WHERE sno=%s
            """, (name, room, device, sno_data))
        flash("Data Updated Successfully")
        mysql.connection.commit()
        return redirect(url_for('Index'))




if __name__ == "__main__":
    app.run(debug=True)