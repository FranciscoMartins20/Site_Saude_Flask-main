from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    nome = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    
    info = db.relationship('UserInfo', back_populates='user', uselist=False)
    agendamentos = db.relationship('Agendamento', foreign_keys='Agendamento.user_id', back_populates='user')
    relatorios_medico = db.relationship('RelatorioRaioX', back_populates='medico', foreign_keys='RelatorioRaioX.medico_id')

    def __repr__(self):
        return f"User('{self.nome}', '{self.email}')"

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class UserInfo(db.Model):
    __tablename__ = 'UserInfo'
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), primary_key=True)
    cc_number = db.Column(db.String(20), nullable=False)
    health_number = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    height = db.Column(db.Float, nullable=False)
    bmi = db.Column(db.Float, nullable=False)

    user = db.relationship('User', back_populates='info')
    relatorios_paciente = db.relationship('RelatorioRaioX', back_populates='paciente', foreign_keys='RelatorioRaioX.paciente_id')

    def __repr__(self):
        return f"UserInfo('{self.cc_number}', '{self.health_number}', '{self.gender}', '{self.birth_date}', '{self.weight}', '{self.height}', '{self.bmi}')"

class Agendamento(db.Model):
    __tablename__ = 'agendamentos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    data = db.Column(db.Date, nullable=False)
    hora = db.Column(db.Time, nullable=False)
    medico_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    
    user = db.relationship('User', foreign_keys=[user_id], back_populates='agendamentos')
    medico = db.relationship('User', foreign_keys=[medico_id])

    def __repr__(self):
        return f"Agendamento('{self.tipo}', '{self.data}', '{self.hora}', '{self.user_id}', '{self.medico_id}')"

class RelatorioRaioX(db.Model):
    __tablename__ = 'relatorio_raiox'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tipo_exame = db.Column(db.String(100), nullable=False)
    data_exame = db.Column(db.Date, nullable=False)
    descricao = db.Column(db.String(255), nullable=False)
    imagem_url = db.Column(db.String(255), nullable=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('UserInfo.user_id'), nullable=False)
    medico_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)

    paciente = db.relationship('UserInfo', back_populates='relatorios_paciente', foreign_keys=[paciente_id])
    medico = db.relationship('User', back_populates='relatorios_medico', foreign_keys=[medico_id])
    resultados = db.relationship('Resultado', back_populates='relatorio', cascade="all, delete-orphan")

    def __repr__(self):
        return f"RelatorioRaioX('{self.tipo_exame}', '{self.data_exame}', '{self.descricao}')"

class Resultado(db.Model):
    __tablename__ = 'resultados'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    area_examinada = db.Column(db.String(100), nullable=False)
    resultado = db.Column(db.String(255), nullable=False)
    observacoes = db.Column(db.String(255), nullable=True)
    relatorio_id = db.Column(db.Integer, db.ForeignKey('relatorio_raiox.id'), nullable=False)

    relatorio = db.relationship('RelatorioRaioX', back_populates='resultados')

    def __repr__(self):
        return f"Resultado('{self.area_examinada}', '{self.resultado}', '{self.observacoes}')"
