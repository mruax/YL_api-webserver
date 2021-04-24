from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class CompanyForm(FlaskForm):
    name = StringField('Название компании', validators=[DataRequired()])
    address = StringField('Адрес', validators=[DataRequired()])
    phone_number = StringField('Номер телефона',
                               validators=[DataRequired()])
    post_address = IntegerField('Почтовый индекс',
                                validators=[DataRequired()])
    description = StringField('Описание', validators=[DataRequired()])
    INN = IntegerField('Идентификационный номер налогоплательщика (ИНН) - 12 '
                       'цифр',
                       validators=[DataRequired()])
    KPP = IntegerField('Код причины постановки на учет (КПП) - 1-50 цифр',
                       validators=[DataRequired()])
    ORGN = IntegerField('Основной государственный регистрационный номер (ОРГН)'
                        ' - 13 цифр', validators=[DataRequired()])
    OKPO = IntegerField('Общероссийский классификатор предприятий и '
                        'организаций (ОКПО) - 10 цифр',
                        validators=[DataRequired()])
    submit = SubmitField('Зарегистрировать компанию')
