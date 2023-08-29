from app import app

#ROUTE ERROR HANDLER
@app.errorhandler(404)
def page_not_found(e):
    return 'La pagina no existe'