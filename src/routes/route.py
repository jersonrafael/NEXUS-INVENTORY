# START APP


# @app.route('/', methods=['GET'])
# def home():
    
#     find_cat = categorys.find()
#     alls_products = products.find()

#     #VALIDAR SI EL USUARIO ESTA LOGEADO
#     if 'username' in session:
#         statusLogin = True
#         return render_template('home.html', alls_products=alls_products,p_categorys=find_cat, messageLogin=statusLogin)
#     else:
#         statusLogin = False
#         return render_template('home.html', alls_products=alls_products,p_categorys=find_cat, messageLogin=statusLogin)



from app import app
@app.route('/', methods=['GET'])
def home():
    return 'Hola'