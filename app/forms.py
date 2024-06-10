from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, HiddenField, SubmitField, DateField, FloatField,TimeField
from wtforms.validators import DataRequired, Email, EqualTo, Optional, ValidationError
from .models import User

class UserRegistrationForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmar Senha', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=[
        ('Administrador', 'Administrador'),
        ('Rececionista', 'Rececionista'),
        ('Médico', 'Médico'),
        ('TSDT', 'TSDT'),
        ('Utente', 'Utente')
    ], validators=[DataRequired()])
    submit = SubmitField('Registrar')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email já está em uso. Escolha um diferente.')

class AdminCreateUserForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmar Senha', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=[
        ('Administrador', 'Administrador'),
        ('Rececionista', 'Rececionista'),
        ('Médico', 'Médico'),
        ('TSDT', 'TSDT'),
        ('Utente', 'Utente')
    ], validators=[DataRequired()])
    
    # Campos extras para Utente
    cc_number = StringField('Número do Cartão de Cidadão', validators=[Optional()])
    health_number = StringField('Número de Utente de Saúde', validators=[Optional()])
    gender = SelectField('Género', choices=[('M', 'Masculino'), ('F', 'Feminino')], validators=[Optional()])
    birth_date = DateField('Data de Nascimento', format='%Y-%m-%d', validators=[Optional()])
    weight = FloatField('Peso', validators=[Optional()])
    height = FloatField('Altura', validators=[Optional()])
    bmi = FloatField('IMC', validators=[Optional()])

    submit = SubmitField('Criar Usuário')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email já está em uso. Escolha um diferente.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class UpdateUserForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    role = SelectField('Role', choices=[
        ('Administrador', 'Administrador'),
        ('Rececionista', 'Rececionista'),
        ('Médico', 'Médico'),
        ('TSDT', 'TSDT'),
        ('Utente', 'Utente')
    ], validators=[DataRequired()])

    # Campos extras para Utente
    cc_number = StringField('Número do Cartão de Cidadão')
    health_number = StringField('Número de Utente de Saúde')
    gender = SelectField('Género', choices=[('M', 'Masculino'), ('F', 'Feminino')])
    birth_date = DateField('Data de Nascimento', format='%Y-%m-%d')
    weight = FloatField('Peso')
    height = FloatField('Altura')
    bmi = FloatField('IMC')

    submit = SubmitField('Atualizar')


class AgendamentoForm(FlaskForm):
    utente = SelectField('Utente', coerce=int, validators=[DataRequired()])
    tipo = SelectField('Tipo de Exame', choices=[
        ('radiografia', 'Radiografia'),
        ('ultrassom', 'Ecografia'),
        ('tomografia', 'TAC'),
        ('ressonancia', 'Ressonância Magnética')
    ], validators=[DataRequired()])
    data = DateField('Data do Exame', format='%Y-%m-%d', validators=[DataRequired()])
    hora = SelectField('Hora', choices=[(f'{h:02}:00', f'{h:02}:00') for h in range(9, 19)], validators=[DataRequired()])
    medico = SelectField('Médico', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Agendar')



class DeleteUserForm(FlaskForm):
    submit = SubmitField('Deletar')
