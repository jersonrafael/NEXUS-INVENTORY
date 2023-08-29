from flask_wtf import FlaskForm 
from wtforms import StringField,SubmitField,validators,FloatField,IntegerField,SelectField
from wtforms.validators import DataRequired


class agregar(FlaskForm):
    p_name = StringField(label=('Nombre de producto:'), validators=[DataRequired()])
    p_price = FloatField(label=('Precio de producto:'), validators=[DataRequired()])
    p_quantity = IntegerField(label=('Cantidad del producto:'), validators=[DataRequired()])
    p_description = StringField(label=('Descripcion del producto'), validators=[DataRequired()])
    category = SelectField(u'Programming Language', choices=[('cpp', 'C++'), ('py', 'Python'), ('text', 'Plain Text')])
    submit = SubmitField(label=('Submit'))