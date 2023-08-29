from flask import render_template
from app import app

from bson import ObjectId
from conn import categorys,products

#SEE THE CATEGORYS
@app.route('/category/<category_id>')
def catSearch(category_id):
    find_cat = categorys.find_one({"_id":ObjectId(category_id)})
    all_products_cat = products.find({"cat_id": category_id})
    return render_template('categorys.html', name=find_cat,products_find=all_products_cat)