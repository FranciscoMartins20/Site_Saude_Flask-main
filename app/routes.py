from flask import Blueprint, jsonify, render_template, redirect, url_for, flash, session, request
from app import db, bcrypt
from app.models import User, UserInfo, Agendamento, RelatorioRaioX, Resultado
from app.forms import UserRegistrationForm, AdminCreateUserForm, LoginForm, UpdateUserForm, DeleteUserForm, AgendamentoForm, RelatorioForm
from functools import wraps
from datetime import time

main = Blueprint('main', __name__)

# Middleware de controle de acesso
def roles_required(*roles):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if 'user' not in session:
                flash('Por favor, faça login para acessar esta página.', 'warning')
                return redirect(url_for('main.login'))
            if session['user']['role'] not in roles:
                flash('Você não tem permissão para acessar esta página.', 'danger')
                return redirect(url_for('main.home'))
            return fn(*args, **kwargs)
        decorated_view.__name__ = fn.__name__
        return decorated_view
    return wrapper

# Rotas existentes
@main.route('/')
def home():
    user = session.get('user')
    return render_template('home.html', title='Home', user=user)

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = UserRegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(nome=form.nome.data, email=form.email.data, password=hashed_password, role='Utente')
        db.session.add(user)
        db.session.commit()
        flash('Sua conta foi criada! Agora pode fazer login', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', title='Registrar', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session['user'] = {'id': user.id, 'nome': user.nome, 'email': user.email, 'role': user.role}
            flash('Login realizado com sucesso!', 'success')
            if session['user']['role'] == 'Utente':
                return redirect(url_for('main.home'))
            else:
                return redirect(url_for('main.home'))
        else:
            flash('Login falhou. Verifique o nome de utilizador e a senha', 'danger')
    return render_template('login.html', title='Login', form=form)

@main.route('/logout')
def logout():
    session.pop('user', None)
    flash('Você saiu da sua conta.', 'success')
    return redirect(url_for('main.home'))

@main.route('/relatorio_raio_x')
@roles_required('Médico')
def relatorio_raio_x():
    return render_template('relatorio_raio_x.html')

@main.route('/create_agendamento', methods=['GET', 'POST'])
@roles_required('Administrador', 'Rececionista')
def create_agendamento():
    form = AgendamentoForm()
    form.utente.choices = [(user.id, user.nome) for user in User.query.filter_by(role='Utente').all()]
    form.medico.choices = [(user.id, user.nome) for user in User.query.filter_by(role='Médico').all()]

    if form.validate_on_submit():
        hora = time.fromisoformat(form.hora.data)
        
        # Verificar se já existe um agendamento para o mesmo médico na mesma data e hora
        existing_agendamento = Agendamento.query.filter_by(
            medico_id=form.medico.data,
            data=form.data.data,
            hora=hora
        ).first()
        
        if existing_agendamento:
            flash('O médico já tem um agendamento nesse horário.', 'danger')
            return redirect(url_for('main.create_agendamento'))
        
        agendamento = Agendamento(
            user_id=form.utente.data,
            tipo=form.tipo.data,
            data=form.data.data,
            hora=hora,
            medico_id=form.medico.data
        )
        db.session.add(agendamento)
        db.session.commit()
        flash('Agendamento criado com sucesso!', 'success')
        return redirect(url_for('main.agendamentos_list'))
    return render_template('agendamento.html', title='Agendamento de Exames de Radiologia', form=form)


@main.route('/agendamento/<int:agendamento_id>/edit', methods=['GET', 'POST'])
@roles_required('Administrador', 'Rececionista')
def edit_agendamento(agendamento_id):
    agendamento = Agendamento.query.get_or_404(agendamento_id)
    form = AgendamentoForm(obj=agendamento)
    form.utente.choices = [(user.id, user.nome) for user in User.query.filter_by(role='Utente').all()]
    form.medico.choices = [(user.id, user.nome) for user in User.query.filter_by(role='Médico').all()]
    
    if form.validate_on_submit():
        hora = time.fromisoformat(form.hora.data)  # Converte a string de hora para um objeto time
        agendamento.user_id = form.utente.data
        agendamento.tipo = form.tipo.data
        agendamento.data = form.data.data
        agendamento.hora = hora  # Use o objeto time
        agendamento.medico_id = form.medico.data
        db.session.commit()
        flash('Agendamento atualizado com sucesso!', 'success')
        return redirect(url_for('main.agendamentos_list'))
    
    return render_template('edit_agendamento.html', title='Editar Agendamento', form=form, agendamento=agendamento)

@main.route('/agendamentos')
@roles_required('Administrador', 'Rececionista')
def agendamentos_list():
    utente_alias = db.aliased(User)
    medico_alias = db.aliased(User)
    agendamentos = db.session.query(
        Agendamento.id, 
        utente_alias.nome.label('utente_nome'), 
        Agendamento.tipo, 
        Agendamento.data, 
        Agendamento.hora, 
        medico_alias.nome.label('medico_nome')
    ).join(utente_alias, Agendamento.user_id == utente_alias.id).join(medico_alias, Agendamento.medico_id == medico_alias.id).all()
    return render_template('agendamentos_list.html', agendamentos=agendamentos)


@main.route('/perfil')
@roles_required('Utente')
def perfil():
    user = session['user']
    agendamentos = Agendamento.query.filter_by(user_id=user['id']).all()
    historico_exames = [
        {'tipo': 'RX Tórax', 'data': '10/01/2023'},
        {'tipo': 'Tomografia Computadorizada', 'data': '05/08/2023'}
    ]
    return render_template('perfil.html', user=user, agendamentos=agendamentos, historico_exames=historico_exames)

@main.route('/dashboard')
@roles_required('Administrador', 'Rececionista', 'Médico', 'TSDT')
def dashboard():
    user = session['user']
    return render_template('dashboard.html', user=user)

@main.route('/userslist')
@roles_required('Administrador', 'Rececionista')
def users_list():
    if session['user']['role'] == 'Rececionista':
        users = db.session.query(User, UserInfo).outerjoin(UserInfo, User.id == UserInfo.user_id).filter(User.role == 'Utente').all()
    else:
        users = db.session.query(User, UserInfo).outerjoin(UserInfo, User.id == UserInfo.user_id).all()
    
    delete_form = DeleteUserForm()
    create_form = AdminCreateUserForm()
    return render_template('users_list.html', users=users, delete_form=delete_form, create_form=create_form)

@main.route('/user/<int:id>')
@roles_required('Administrador', 'Rececionista')
def user_detail(id):
    user = User.query.get_or_404(id)
    delete_form = DeleteUserForm()
    return render_template('user_detail.html', user=user, delete_form=delete_form)

@main.route('/user/<int:id>/edit', methods=['GET', 'POST'])
@roles_required('Administrador', 'Rececionista')
def edit_user(id):
    user = User.query.get_or_404(id)
    form = UpdateUserForm(obj=user)
    if form.validate_on_submit():
        try:
            user.nome = form.nome.data
            user.email = form.email.data
            user.role = form.role.data
            db.session.commit()

            if form.role.data == 'Utente':
                if user.info:
                    user.info.cc_number = form.cc_number.data
                    user.info.health_number = form.health_number.data
                    user.info.gender = form.gender.data
                    user.info.birth_date = form.birth_date.data
                    user.info.weight = form.weight.data
                    user.info.height = form.height.data
                    user.info.bmi = form.bmi.data
                else:
                    user_info = UserInfo(
                        user_id=user.id,
                        cc_number=form.cc_number.data,
                        health_number=form.health_number.data,
                        gender=form.gender.data,
                        birth_date=form.birth_date.data,
                        weight=form.weight.data,
                        height=form.height.data,
                        bmi=form.bmi.data
                    )
                    db.session.add(user_info)
                db.session.commit()

            flash('Os detalhes do usuário foram atualizados.', 'success')
            return redirect(url_for('main.users_list'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar os detalhes do usuário: {str(e)}', 'danger')
    if request.method == 'GET':
        form.nome.data = user.nome
        form.email.data = user.email
        form.role.data = user.role
        if user.role == 'Utente' and user.info:
            form.cc_number.data = user.info.cc_number
            form.health_number.data = user.info.health_number
            form.gender.data = user.info.gender
            form.birth_date.data = user.info.birth_date
            form.weight.data = user.info.weight
            form.height.data = user.info.height
            form.bmi.data = user.info.bmi
    return render_template('edit_user.html', form=form, user=user)

@main.route('/user/<int:id>/delete', methods=['POST'])
@roles_required('Administrador')
def delete_user(id):
    user = User.query.get_or_404(id)
    try:
        db.session.delete(user)
        db.session.commit()
        flash('Usuário deletado com sucesso.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao deletar o usuário: {str(e)}', 'danger')
    return redirect(url_for('main.users_list'))

@main.route('/create_user', methods=['GET', 'POST'])
@roles_required('Administrador', 'Rececionista')
def create_user():
    form = AdminCreateUserForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        role = form.role.data if session['user']['role'] == 'Administrador' else 'Utente'
        user = User(nome=form.nome.data, email=form.email.data, password=hashed_password, role=role)
        db.session.add(user)
        db.session.commit()

        if role == 'Utente':
            user_info = UserInfo(
                user_id=user.id,
                cc_number=form.cc_number.data,
                health_number=form.health_number.data,
                gender=form.gender.data,
                birth_date=form.birth_date.data,
                weight=form.weight.data,
                height=form.height.data,
                bmi=form.bmi.data
            )
            db.session.add(user_info)
            db.session.commit()

        flash('Usuário criado com sucesso!', 'success')
        return redirect(url_for('main.users_list'))
    return render_template('create_user.html', title='Adicionar Novo Usuário', form=form)

@main.route('/me')
@roles_required('Utente', 'Administrador', 'Rececionista', 'Médico', 'TSDT')
def me():
    user_id = session['user']['id']
    user = User.query.get_or_404(user_id)
    return render_template('perfil.html', user=user)

# Rotas para relatórios de Raio-X
@main.route('/relatorios')
@roles_required('Administrador', 'Médico')
def relatorios_list():
    relatorios = RelatorioRaioX.query.all()
    return render_template('relatorios_list.html', relatorios=relatorios)

@main.route('/relatorio/<int:id>')
@roles_required('Administrador', 'Médico')
def relatorio_detail(id):
    relatorio = RelatorioRaioX.query.get_or_404(id)
    return render_template('relatorio_detail.html', relatorio=relatorio)

@main.route('/create_relatorio', methods=['GET', 'POST'])
@roles_required('Administrador', 'Médico')
def create_relatorio():
    form = RelatorioForm()
    form.paciente.choices = [(user.user_id, user.user.nome) for user in UserInfo.query.all()]
    form.medico.choices = [(user.id, user.nome) for user in User.query.filter_by(role='Médico').all()]
    if form.validate_on_submit():
        relatorio = RelatorioRaioX(
            tipo_exame=form.tipo_exame.data,
            data_exame=form.data_exame.data,
            descricao=form.descricao.data,
            imagem_url=form.imagem_url.data,
            paciente_id=form.paciente.data,
            medico_id=form.medico.data
        )
        db.session.add(relatorio)
        db.session.commit()
        for resultado in form.resultados.entries:
            resultado_obj = Resultado(
                area_examinada=resultado.data['area_examinada'],
                resultado=resultado.data['resultado'],
                observacoes=resultado.data['observacoes'],
                relatorio_id=relatorio.id
            )
            db.session.add(resultado_obj)
        db.session.commit()
        flash('Relatório criado com sucesso!', 'success')
        return redirect(url_for('main.relatorios_list'))
    return render_template('create_relatorio.html', title='Adicionar Relatório de Raio-X', form=form)

@main.route('/relatorio/<int:id>/edit', methods=['GET', 'POST'])
@roles_required('Administrador', 'Médico')
def edit_relatorio(id):
    relatorio = RelatorioRaioX.query.get_or_404(id)
    form = RelatorioForm(obj=relatorio)
    form.paciente.choices = [(user.user_id, user.user.nome) for user in UserInfo.query.all()]
    form.medico.choices = [(user.id, user.nome) for user in User.query.filter_by(role='Médico').all()]
    if form.validate_on_submit():
        relatorio.tipo_exame = form.tipo_exame.data
        relatorio.data_exame = form.data_exame.data
        relatorio.descricao = form.descricao.data
        relatorio.imagem_url = form.imagem_url.data
        relatorio.paciente_id = form.paciente.data
        relatorio.medico_id = form.medico.data
        db.session.commit()
        # Update resultados
        for resultado in form.resultados.entries:
            resultado_obj = Resultado.query.get(resultado.data['id'])
            if resultado_obj:
                resultado_obj.area_examinada = resultado.data['area_examinada']
                resultado_obj.resultado = resultado.data['resultado']
                resultado_obj.observacoes = resultado.data['observacoes']
            else:
                resultado_obj = Resultado(
                    area_examinada=resultado.data['area_examinada'],
                    resultado=resultado.data['resultado'],
                    observacoes=resultado.data['observacoes'],
                    relatorio_id=relatorio.id
                )
                db.session.add(resultado_obj)
        db.session.commit()
        flash('Relatório atualizado com sucesso!', 'success')
        return redirect(url_for('main.relatorios_list'))
    return render_template('edit_relatorio.html', title='Editar Relatório de Raio-X', form=form, relatorio=relatorio)

@main.route('/relatorio/<int:id>/delete', methods=['POST'])
@roles_required('Administrador', 'Médico')
def delete_relatorio(id):
    relatorio = RelatorioRaioX.query.get_or_404(id)
    try:
        db.session.delete(relatorio)
        db.session.commit()
        flash('Relatório deletado com sucesso.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao deletar o relatório: {str(e)}', 'danger')
    return redirect(url_for('main.relatorios_list'))

@main.route('/relatorios/<int:user_id>')
@roles_required('Administrador', 'Médico')
def relatorios_by_user(user_id):
    relatorios = RelatorioRaioX.query.filter_by(paciente_id=user_id).all()
    return render_template('relatorios_list.html', relatorios=relatorios)

@main.route('/api/user/<int:user_id>/agendamentos', methods=['GET'])
@roles_required('Administrador', 'Médico')
def api_user_agendamentos(user_id):
    agendamentos = Agendamento.query.filter_by(user_id=user_id).all()
    agendamentos_data = [{
        'tipo': agendamento.tipo,
        'data': agendamento.data.strftime('%Y-%m-%d'),
        'descricao': f'{agendamento.tipo} agendado para {agendamento.data.strftime("%d/%m/%Y")} às {agendamento.hora.strftime("%H:%M")}'
    } for agendamento in agendamentos]
    return jsonify(agendamentos_data)
