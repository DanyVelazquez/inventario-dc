from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length
from .models import ESTADOS

class EquipoForm(FlaskForm):
    nombre = StringField("Nombre", validators=[DataRequired(), Length(max=100)])
    descripcion = TextAreaField("Descripción")
    modelo = StringField("Modelo", validators=[DataRequired(), Length(max=100)])
    numero de serie = StringField("Nº de Serial", validators=[DataRequired(), Length(max=64)])
    datacenter = StringField("Datacenter", validators=[DataRequired(), Length(max=50)])
    estado = SelectField("Estado", choices=[(e, e.capitalize()) for e in ESTADOS], validators=[DataRequired()])
    submit = SubmitField("Guardar")
