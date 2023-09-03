from bson import ObjectId

from flask import render_template,request,redirect,url_for,session
from app import app

from conn import products,categorys

#INVENTORY
@app.route('/inventario', methods=['GET'])
def inventario():

    if 'username' in session:
        get_products = products.find()
        return render_template('inventario.html', p=get_products)
    else:
        return 'Oops Parece que no tienes permiso para hacer eso'

# GET ALL CATEGORYS PROTEGIDAS
@app.route('/categoriasAdmin', methods=['GET'])
def categoriasAdmin():

    if 'username' in session:
        all_categorys = categorys.find()
        return render_template('categorias.html', all_categorys=all_categorys)
    else:
        return 'Oops Parece que no tienes permiso para hacer eso'

#ADD CATEGORY
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
        
#DELETE CATEGORY
@app.route('/del_categoria/<_id>', methods=['GET'])
def delete_category(_id):
    if 'username' in session:
        valid_cat = categorys.find_one({'_id': ObjectId(_id)})
        products_find= products.find_one({'cat_id': _id})

        if valid_cat is not None:
            categorys.delete_one({'_id': ObjectId(_id)})
            products.delete_one({'cat_id': _id})
            message = 'Categoria eliminada'
            return redirect(url_for('categoriasAdmin'))
        else:
            message = 'Esta categoria no existe'
            return redirect(url_for('categoriasAdmin'))
    else:
        return 'Oops no puedes hacer eso'