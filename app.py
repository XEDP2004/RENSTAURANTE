from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
import database as db


template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(template_dir, 'src', 'templates')
app = Flask(__name__, template_folder= template_dir)
app.secret_key ="r1nc0npr0h1b1d02023r35taur4t3"

#Ruta de la aplicacion


@app.route('/', methods=['GET'])
def home():
   cursor = db.database.cursor()
   cursor.execute("SELECT * FROM users")
   myresult = cursor.fetchall()

    #Vamos a convertir los datos a diccionario

   insertObject = []
   columNames = [column[0] for column in cursor.description]
   for record in myresult:
      insertObject.append(dict(zip(columNames, record)))
   cursor.close()
   return render_template('index.html')




#CONTACTO CRUD

@app.route('/database', methods=['POST'])
def contacto():
   name= request.form['name']
   surname = request.form['surname']
   email = request.form['email']
   tel = request.form['tel']
   messenger = request.form['massenger']
   if name and surname and email and tel and messenger:
      cursor = db.database.cursor()
      sql = "INSERT INTO users (name,surname, email, tel, massenger) VALUES (%s, %s, %s, %s, %s)"
      data = (name, surname, email, tel, messenger)
      cursor.execute(sql, data)
      db.database.commit()
      return redirect(url_for('home', contacto='Gracias por contactarnos'))

@app.route('/database')
def database():
   cursor = db.database.cursor()
   cursor.execute("SELECT * FROM users")
   myresult = cursor.fetchall()

    #Vamos a convertir los datos a diccionario

   insertObject = []
   columNames = [column[0] for column in cursor.description]
   for record in myresult:
      insertObject.append(dict(zip(columNames, record)))
   cursor.close()
   return render_template('CRUD/database.html ', data=insertObject)

@app.route('/delete/<string:id>')
def delete(id):
    cursor = db.database.cursor()
    sql = "DELETE FROM users WHERE id=%s"
    data = (id,)
    cursor.execute(sql,data)
    db.database.commit()
    return redirect(url_for('database'))

@app.route('/edit/<string:id>', methods = ['POST'])
def edit(id):
   name = request.form['name']
   surname = request.form['surname']
   email= request.form['email']
   tel = request.form['tel']
   messenger = request.form['massenger']
   if name and surname and email and tel and messenger:
        cursor = db.database.cursor()
        sql = "UPDATE users SET name= %s, surname = %s, email = %s, tel=%s, massenger=%s WHERE id= %s"
        data = (name, surname, email, tel, messenger, id)
        cursor.execute(sql, data)
        db.database.commit()
   return redirect(url_for('database'))

# LOGIN


@app.route('/menu/', methods=["GET"])
def menu():
    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM singup")
    myresult = cursor.fetchall()

    # Convert data to a list of dictionaries
    user_data = []
    column_names = [column[0] for column in cursor.description]
    for record in myresult:
        user_data.append(dict(zip(column_names, record)))
    cursor.close()

    # Extract user names and surnames from the data and concatenate them
    user_names = [f"{user['name']} {user['surname']}" for user in user_data]

    return render_template('menu.html', user_names=user_names)

@app.route('/login')
def loginIngresar():
   return render_template('sitios/login.html')


@app.route('/login', methods=[ "POST"])
def login():
    email = request.form['email']
    password = request.form['password']

    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM singup WHERE email=%s AND password =%s",(email, password))
    user = cursor.fetchone()
    cursor.close()

    if user is not None:
       session['email'] = email
       session['id'] = user[0]
       return redirect(url_for('menu'))
    
    else:
       return render_template('sitios/login.html', error='Usuario o contraseña incorrecto')

   
#singup
@app.route('/singup')
def singup():
   cursor = db.database.cursor()
   cursor.execute("SELECT * FROM singup")
   myresult = cursor.fetchall()

    #Vamos a convertir los datos a diccionario

   insertObject = []
   columNames = [column[0] for column in cursor.description]
   for record in myresult:
      insertObject.append(dict(zip(columNames, record)))
   cursor.close()
   return render_template('sitios/singup.html')

@app.route('/databaseSingup', methods = ['POST'])
def databaseSingup():
   name = request.form['name']
   surname = request.form['surname']
   email = request.form['email']
   password = request.form['password']
   id = request.form['id']
   tel = request.form['tel']

   if not (name and surname and email and password and id and tel):
      flash('Todos los campos son obligatorios', 'error')
      return redirect(url_for('singup'))

   cursor = db.database.cursor()

   # Check if email or ID already exists
   cursor.execute("SELECT * FROM singup WHERE email=%s OR id=%s", (email, id))
   existing_user = cursor.fetchone()

   if existing_user:
      flash('Correo o ID ya existen. Intente con otra información.')
      return redirect(url_for('singup'))
   
   # Insert new user
   sql = "INSERT INTO singup (name, surname, email, password, id, tel) VALUES (%s, %s, %s, %s, %s, %s)"
   data = (name, surname, email, password, id, tel)
   cursor.execute(sql, data)
   db.database.commit()
   flash('Cuenta creada exitosamente', 'success')
   return redirect(url_for('menu'))

@app.route('/databaseSingup')
def singupDatabase():
   cursor = db.database.cursor()
   cursor.execute("SELECT * FROM singup")
   myresult = cursor.fetchall()

    #Vamos a convertir los datos a diccionario

   insertObject = []
   columNames = [column[0] for column in cursor.description]
   for record in myresult:
      insertObject.append(dict(zip(columNames, record)))
   cursor.close()
   return render_template('CRUD/databaseSingup.html ', data=insertObject)

@app.route('/deleteSingup/<string:id>')
def deleteSingup(id):
    cursor = db.database.cursor()
    sql = "DELETE FROM singup WHERE id=%s"
    data = (id,)
    cursor.execute(sql,data)
    db.database.commit()
    return redirect(url_for('singupDatabase'))

@app.route('/editSingup/<string:id>', methods = ['POST'])
def editSingup(id):
   name = request.form['name']
   surname = request.form['surname']
   email= request.form['email']
   password = request.form['password']
   tel = request.form['tel']
   
   if name and surname and email and password and  tel :
        cursor = db.database.cursor()
        sql = "UPDATE singup SET name= %s, surname = %s, email = %s, password=%s, tel=%s WHERE id= %s"
        data = (name, surname, email, password, tel, id)
        cursor.execute(sql, data)
        db.database.commit()
   return redirect(url_for('singupDatabase'))







if __name__ == '__main__':
   app.run(debug=True)