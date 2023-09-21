from flask import flash, render_template, redirect, url_for,request
# from werkzeug import secure_filename
from app import app

from bson import ObjectId
from conn import products,categorys

from cloud import cloudinary

from form import Producto,EditProductForm

import os

from priceBs import obtenerUsd

priceVes = obtenerUsd()
# 
priceVes = priceVes.replace(',', '.')
#SEE ALL INFO OF THE PRODUCT
@app.route('/product/<p_id>')
def moreInfo(p_id):
    p_fund = products.find_one({'_id': ObjectId(p_id)})
    idCat = p_fund['cat_id']
    cat_fund = categorys.find_one({'_id':ObjectId(idCat)})
    return render_template('productInfo.html', p_fund=p_fund,cat_fund=cat_fund,bcv=priceVes)

# DELETE A PRODUCT
@app.route('/del/<_id>', methods=['GET'])
def delete_product(_id):
    find_product = products.find_one({"_id": ObjectId(_id)})
    image = find_product['file_name']
    print(image)
    if find_product is None:
        return render_template('error.html')
    else:
        del_product = products.delete_one({"_id": ObjectId(_id)})
        cloudinary.uploader.destroy(image)
        return redirect(url_for('inventario'))
    
# EDIT A PRODUCT
@app.route('/edit/<_id>', methods=['GET', 'POST'])
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

        file = request.files['ImagenProducto']
        filen = file.filename

        message = ''
        result = products.find_one({"_id": ObjectId(_id)})

        # Check if exist a document with the same data
        if result is None:
            message = "El producto no existe"
            p = products.find_one({"_id": ObjectId(_id)})
            return render_template('modificar.html', p=p, message=message)
        else:
            products.update_one({"_id": ObjectId(_id)}, {"$set": {"p_name": p_name, "p_price":p_price, "priceVes": int(p_price) * float(priceVes),"p_quantity":p_quantity, "p_description":p_description, 'cat_id':cat_id, 'file_name':filen}})
            cloudinary.uploader.upload(file, public_id=filen)
            message = "Se han realizado los cambios con exito"
            p = products.find_one({"_id": ObjectId(_id)})
            p_info = p['cat_id']
            p_cat = categorys.find_one({"_id": ObjectId(p_info)})
            p_cat_g = categorys.find()
            return render_template('modificar.html', p=p, message=message,p_cat=p_cat,p_cat_g=p_cat_g,bcv=priceVes)

            

#ADD PRODUCT
@app.route('/agregar_producto', methods=['GET','POST'])
def add_product():
    form = Producto()
    if request.method == 'GET':
        message = ''
        find_cat = categorys.find()
        return render_template('agg_productos.html',message=message,find_cat=find_cat, form=form, bcv=priceVes)
    else:
        pass 
    
    if request.method == 'POST':
        req_data = request.form
        p_name = req_data['p_name'].capitalize()
        p_price = req_data['p_price'].capitalize()
        p_quantity = req_data['p_quantity'].capitalize()
        p_description = req_data['p_description'].capitalize()
        cat_id = req_data['category']

        file = request.files['ImagenProducto']
        filen = file.filename
        if form.validate_on_submit(): 
            product_data = {"p_name": p_name, "p_price": p_price,"priceVes": int(p_price) * float(priceVes), "p_quantity": p_quantity,"p_description": p_description, "cat_id":cat_id, 'file_name':filen}
            result = products.find_one({"p_name": p_name})
            if result is not None:
                message = 'El producto ya existe'
                find_cat = categorys.find()
                return render_template('agg_productos.html',message=message, find_cat=find_cat,form=form,bcv=priceVes)
            else:
                find_cat = categorys.find()
                products.insert_one(product_data)
                cloudinary.uploader.upload(file, public_id=filen)
                message = 'Producto agregado'
                return render_template('agg_productos.html',message=message,find_cat=find_cat,form=form,bcv=priceVes)
        message = 'Error al agregar el producto revisa que los campos este correctos'
        return render_template('agg_productos.html',message=message,form=form)

