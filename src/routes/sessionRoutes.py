from flask import request,render_template,redirect,url_for,session
from app import app

import os
from dotenv import load_dotenv

load_dotenv()

#LOGIN
@app.route('/login', methods=['GET','POST'])
def login():
    info = ''
    if request.method == 'POST':
        req_data = request.form
        user_name = req_data['username']
        user_pass = req_data['userpass']
        useradmin = os.getenv("adminUser")
        useradminpass = os.getenv("adminPassWord")
        

        if user_name == useradmin:
            if user_pass == useradminpass:
                session['username'] = request.form['username']
                return redirect(url_for('home'))
                
            else:
                info = 'Contraseña incorrecta'
                return render_template('login.html', info=info)
        else:
            info = 'Datos incorrectos'
            return render_template('login.html', info=info)    
    return render_template('login.html', info=info)

#LOGOUT
@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('home'))