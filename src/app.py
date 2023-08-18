from flask import Flask, jsonify, request, json,redirect,url_for,session,send_from_directory
from bson.json_util import dumps
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId
from flask_cors import CORS
from flask import render_template
from markupsafe import escape
# from werkzeug import secure_filename
import os


uri = "mongodb+srv://jrrvgamer:jerson980@suplimax.gjezftg.mongodb.net/?retryWrites=true&w=majority"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

# from flask_login import LoginManager,login_required

# MONGODB CONNECTION
# client = MongoClient('mongodb://localhost:27017/')
db = client['suplimax']
products = db['products']
categorys = db['categorys']

# START APP
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
UPLOAD_FOLDER = './static/products/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# login_manager = LoginManager()

"""
    RUTA DE HOME
"""

#RUTA HOME
@app.route('/', methods=['GET'])
def home():
    find_cat = categorys.find()
    alls_products = products.find()

    #VALIDAR SI EL USUARIO ESTA LOGEADO
    if 'username' in session:
        statusLogin = True
        return render_template('home.html', alls_products=alls_products,p_categorys=find_cat, messageLogin=statusLogin)
    else:
        statusLogin = False
        return render_template('home.html', alls_products=alls_products,p_categorys=find_cat, messageLogin=statusLogin)

    # return render_template('home.html', alls_products=alls_products,p_categorys=find_cat)

"""
    RUTA DE BUSQUEDA
"""
#RUTA DE BUSQUEDA
@app.route('/search', methods=['POST'])
def searchP():
    req_data = request.form
    p_search = req_data['p_search']
    
    products_search = products.find_one({"p_name":p_search})

    if products_search is None:
        return f'No hay resultados'
    else:
        return f'busqueda {products_search}'

#RUTA BUSQUEDA POR CATEGORIAS
@app.route('/category/<category_id>')
def catSearch(category_id):
    find_cat = categorys.find_one({"_id":ObjectId(category_id)})
    all_products_cat = products.find({"cat_id": category_id})
    return render_template('categorys.html', name=find_cat,products_find=all_products_cat)


"""
    RUTA DE PRODUCTOS
"""

#RUTA VER PRODUCTO COMPLETO
@app.route('/product/<p_id>')
def moreInfo(p_id):
    p_fund = products.find_one({'_id': ObjectId(p_id)})
    cat_fund = categorys.find_one({'_id':ObjectId(p_fund['cat_id'])})
    return render_template('productInfo.html', p_fund=p_fund,cat_fund=cat_fund)

# DELETE A PRODUCT
@app.route('/del/<_id>', methods=['GET'])
def delete_product(_id):
    find_product = products.find_one({"_id": ObjectId(_id)})

    print(find_product)

    if find_product is None:
        return dumps({'message': 'No deleted that product dont exist'})
    else:
        del_product = products.delete_one({"_id": ObjectId(_id)})
        return redirect(url_for('proteccion'))

# EDIT A PRODUCT
@app.route('/edit/<_id>', methods=['GET','POST'])
def edit_product(_id):

    if request.method == 'GET':
        p = products.find_one({"_id": ObjectId(_id)})
        p_info = p['cat_id']
        p_cat = categorys.find_one({"_id": ObjectId(p_info)})
        p_cat_g = categorys.find()
        return render_template('modificar.html', p=p,p_cat=p_cat,p_cat_g=p_cat_g)
    else:
        pass

    if request.method == 'POST':
        req_data = request.form
        p_name = req_data['p_name']
        p_price = req_data['p_price']
        p_quantity = req_data['p_quantity']
        p_description = req_data['p_description']
        cat_id = req_data['cat_id']

        message = ''
        result = products.find_one({"_id": ObjectId(_id)})

        # Check if exist a document
        if result is None:
            message = "El producto no existe"
            p = products.find_one({"_id": ObjectId(_id)})
            return render_template('modificar.html', p=p, message=message)
        else:
            products.update_one({"_id": ObjectId(_id)}, {"$set": {"p_name": p_name, "p_price":p_price, "p_quantity":p_quantity, "p_description":p_description, 'cat_id':cat_id}})
            message = "Se han realizado los cambios con exito"
            p = products.find_one({"_id": ObjectId(_id)})
            p_info = p['cat_id']
            p_cat = categorys.find_one({"_id": ObjectId(p_info)})
            p_cat_g = categorys.find()
            return render_template('modificar.html', p=p, message=message,p_cat=p_cat,p_cat_g=p_cat_g)
            

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


#AGREAGAR PRODUCTO
@app.route('/agregar_producto', methods=['GET','POST'])
def add_product():

    if request.method == 'GET':
        message = ''
        find_cat = categorys.find()
        return render_template('agg_productos.html',message=message,find_cat=find_cat)
    else:
        pass 
    
    if request.method == 'POST':
        req_data = request.form
        p_name = req_data['p_name'].capitalize()
        p_price = req_data['p_price'].capitalize()
        p_quantity = req_data['p_quantity'].capitalize()
        p_description = req_data['p_description'].capitalize()
        cat_id = req_data['_id']

        file = request.files['file']
        filen = file.filename

        # if filen == '':
        #     message = 'Selecciona una imagen para el producto'
        #     find_cat = categorys.find()
        #     return render_template('agg_productos.html',message=message, find_cat=find_cat)
        # else:
        #     file.save(os.path.join(app.config['UPLOAD_FOLDER'], filen))
        #     pass

        # url_for('static', filename='imagen.jpg')
        priceVes = None

        # if priceVes == None:
        #     priceVes = '0'
        # else:
        #     pass
        product_data = {"p_name": p_name, "p_price": p_price, "priceVes": priceVes, "p_quantity": p_quantity,
                        "p_description": p_description, "cat_id":cat_id, 'file_name':filen}

        # Check if exist a document with the same name
        result = products.find_one({"p_name": p_name})
        if result is not None:
            # exist='El producto ya existe'
            # return render_template('form.html')
            message = 'El producto ya existe'
            find_cat = categorys.find()
            return render_template('agg_productos.html',message=message, find_cat=find_cat)
        else:
            if p_name and p_description and p_price and p_quantity and filen != '':
                products.insert_one(product_data)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filen))
                message = 'Producto agregado'
                return render_template('agg_productos.html',message=message)
            else:
                find_cat = categorys.find()
                message = 'Producto no agregado revisa que todos los campos esten correctos'
                product_data = {"p_name": p_name, "p_price": p_price, "priceVes": priceVes, "p_quantity": p_quantity,
                        "p_description": p_description, "cat_id":cat_id, 'file_name':filen}
                return render_template('agg_productos.html',message=message, product_data=product_data, find_cat=find_cat)


"""
    RUTA DE VALIDACIONES
"""

#MANEJADOR DE ERRORES
@app.errorhandler(404)
def page_not_found(e):
    return 'La pagina no existe'

"""
    RUTAS LOGIN
"""

#RUTA LOGIN
@app.route('/login', methods=['GET','POST'])
def login():
    info = ''
    if request.method == 'POST':
        req_data = request.form
        user_name = req_data['username']
        user_pass = req_data['userpass']
        useradmin = 'Jerson'
        useradminpass = "12345678"
        

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

#RUTA LOGOUT
@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('home'))


"""
    RUTAS PROTEGIDAS
"""

#INVENTARIO PROTEGIDO
@app.route('/inventario', methods=['GET'])
def proteccion():

    if 'username' in session:
        get_products = products.find()
        return render_template('inventario.html', p=get_products)
    else:
        return 'Oops Parece que no tienes permiso para hacer eso'


"""
    RUTAS CATEGORIAS
"""

#AGREGAR CATEGORIAS PROTEGIDA
@app.route('/add_category', methods=['GET','POST'])
def add_category():

    if 'username' in session:
        if request.method == "GET":
            return render_template('agg_categorias.html')
        else:
            pass

        if request.method == 'POST':
            req_data = request.form
            cat_name = req_data['cat_name'].capitalize()
        
            if cat_name != '':
                product_cat = {'cat_name':cat_name}
                # Check if exist a document with the same name
                result = categorys.find_one({"cat_name": cat_name})
                if result is not None:
                    message = 'La categoria ya existe'
                    return render_template('agg_categorias.html', message=message)
                else:
                    insert_cat = categorys.insert_one(product_cat)
                    message = 'Categoria Agregada'
                    return render_template('agg_categorias.html', message=message)
            else:
                message = 'La categoria no puede estar vacia'
                return render_template('agg_categorias.html', message=message)
        else:
            return 'Oops No puedes hacer eso'

#ELIMINAR CATEGORIA PROTEGIDA
@app.route('/del_categoria/<_id>', methods=['GET'])
def delete_category(_id):
    if 'username' in session:
        valid_cat = categorys.find_one({'_id': ObjectId(_id)})
        products_find= products.find_one({'cat_id': _id})

        if valid_cat is not None:
            categorys.delete_one({'_id': ObjectId(_id)})
            products.delete_one({'cat_id': _id})
            message = 'Categoria eliminada'
            return redirect(url_for('get_all_categorys'))
        else:
            message = 'Esta categoria no existe'
            return redirect(url_for('get_all_categorys'))
    else:
        return 'Oops no puedes hacer eso'

# GET ALL CATEGORYS PROTEGIDAS
@app.route('/categorias', methods=['GET'])
def get_all_categorys():

    if 'username' in session:
        all_categorys = categorys.find()
        return render_template('categorias.html', all_categorys=all_categorys)
    else:
        return 'Oops Parece que no tienes permiso para hacer eso'

#EDITAR CATEGORIA
@app.route('/edit_category/<_id>', methods=['GET','POST'])
def edit_category(_id):
    if 'username' in session:
        if request.method == 'POST':
            req_data = request.form
            cat_name = req_data['cat_name']

            if req_data is not None:
                categorys.update_one({'_id': ObjectId(_id)}, {'$set': {'cat_name': cat_name}})
                valid_cat = categorys.find_one({'_id': ObjectId(_id)})
                message = 'Categoria modificada'
                return render_template('editar_categoria.html', message=message,valid_cat=valid_cat)
            else:
                valid_cat = categorys.find_one({'_id': ObjectId(_id)})
                message = "That category don't exist"
                return render_template('editar_categoria.html', message=message,valid_cat=valid_cat)
        else:
            pass

        if request.method == 'GET':
            valid_cat = categorys.find_one({'_id': ObjectId(_id)})
            return render_template('editar_categoria.html', valid_cat=valid_cat)
        else:
            pass
    else:
        return 'Oops parece que no tienes permiso para hacer esto'

@app.route('/styles/<path:path>')
def send_css(path):
    return send_from_directory('css', path)

# RUN APP
if __name__ == "__main__":
    app.run(host='192.168.1.42',port=5000, debug=True)
    # app.run()
# debug=True
# 



