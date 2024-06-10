from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField, DateField, FloatField, TextAreaField, FieldList, FormField
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

# Formulário para resultados
class ResultadoForm(FlaskForm):
    area_examinada = StringField('Área Examinada', validators=[DataRequired()])
    resultado = StringField('Resultado', validators=[DataRequired()])
    observacoes = StringField('Observações')

# Formulário para relatório de Raio-X
class RelatorioForm(FlaskForm):
    tipo_exame = StringField('Tipo de Exame', validators=[DataRequired()])
    data_exame = DateField('Data do Exame', format='%Y-%m-%d', validators=[DataRequired()])
    descricao = TextAreaField('Descrição', validators=[DataRequired()])
    imagem_url = StringField('URL da Imagem')
    paciente = SelectField('Paciente', validators=[DataRequired()], coerce=int)
    medico = SelectField('Médico', validators=[DataRequired()], coerce=int)
    resultados = FieldList(FormField(ResultadoForm), min_entries=1, max_entries=10)
    submit = SubmitField('Salvar Relatório')
