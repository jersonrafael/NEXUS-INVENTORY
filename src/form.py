from flask_wtf import FlaskForm 
from wtforms import StringField,SubmitField,validators,FloatField,IntegerField,SelectField,FileField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileRequired
from wtforms import ValidationError

from conn import categorys

find_cat = categorys.find()

def validate_no_numbers(form, field):
    # Esta función verificará si el campo contiene números
    if any(char.isdigit() for char in field.data):
        raise ValidationError('Este campo no debe contener números')

class Producto(FlaskForm):
    p_name = StringField(label=('Nombre de producto:'), validators=[DataRequired(message='Campo obligatorio'), validate_no_numbers])
    p_price = FloatField(label=('Precio de producto en USD:'), validators=[DataRequired(message='Campo obligatorio')])
    p_quantity = IntegerField(label=('Cantidad del producto:'), validators=[DataRequired(message='Campo obligatorio')])
    p_description = StringField(label=('Descripcion del producto'), validators=[DataRequired(message='Campo obligatorio'), validate_no_numbers])
    category = SelectField(u'Categoria del producto', choices=[(x['_id'], x['cat_name']) for x in find_cat])
    ImagenProducto = FileField(validators=[FileRequired()])
    submit = SubmitField(label=('Submit'))


class EditProductForm(FlaskForm):
    p_name = StringField('Nombre de producto:', validators=[DataRequired(), validate_no_numbers])
    p_price = FloatField('Precio de producto:', validators=[DataRequired()])
    p_quantity = IntegerField('Cantidad del producto:', validators=[DataRequired()])
    p_description = StringField('Descripción del producto:', validators=[DataRequired()])
    category = SelectField('Categoría del producto', choices=[], validators=[DataRequired()])
    submit = SubmitField('Guardar Cambios')