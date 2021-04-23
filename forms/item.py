from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class ItemForm(FlaskForm):
    name = StringField('Наименование товара', validators=[DataRequired()])
    amount = IntegerField('Количество товара', validators=[DataRequired()])
    company = StringField('Компания (название)', validators=[DataRequired()])
    description = StringField('Описание (кратко)', validators=[DataRequired()])
    item_type = StringField('Тип товара', validators=[DataRequired()])
    submit = SubmitField('Добавить товар')
