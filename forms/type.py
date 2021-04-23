from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class TypeForm(FlaskForm):
    name = StringField('Наименование типа товара', validators=[DataRequired()])
    description = StringField('Описание (кратко)', validators=[DataRequired()])
    submit = SubmitField('Добавить тип товара')
