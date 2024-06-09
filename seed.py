from app import db, create_app, bcrypt
from app.models import User, UserInfo, Agendamento
from datetime import date, time

app = create_app()

with app.app_context():
    # Limpar banco de dados
    db.drop_all()
    db.create_all()

    # Criar usuários de exemplo
    admin = User(
        nome='Admin User',
        email='admin@example.com',
        password=bcrypt.generate_password_hash('password123').decode('utf-8'),
        role='Administrador'
    )

    recepcionista = User(
        nome='Recepcionista User',
        email='recepcionista@example.com',
        password=bcrypt.generate_password_hash('password123').decode('utf-8'),
        role='Rececionista'
    )

    medico = User(
        nome='Médico User',
        email='medico@example.com',
        password=bcrypt.generate_password_hash('password123').decode('utf-8'),
        role='Médico'
    )

    tsdt = User(
        nome='TSDT User',
        email='tsdt@example.com',
        password=bcrypt.generate_password_hash('password123').decode('utf-8'),
        role='TSDT'
    )

    utente1 = User(
        nome='Utente 1',
        email='utente1@example.com',
        password=bcrypt.generate_password_hash('password123').decode('utf-8'),
        role='Utente'
    )

    utente2 = User(
        nome='Utente 2',
        email='utente2@example.com',
        password=bcrypt.generate_password_hash('password123').decode('utf-8'),
        role='Utente'
    )

    db.session.add(admin)
    db.session.add(recepcionista)
    db.session.add(medico)
    db.session.add(tsdt)
    db.session.add(utente1)
    db.session.add(utente2)
    db.session.commit()

    # Criar UserInfo para utentes
    utente1_info = UserInfo(
        user_id=utente1.id,
        cc_number='123456789',
        health_number='987654321',
        gender='M',
        birth_date=date(1990, 1, 1),
        weight=70.0,
        height=175.0,
        bmi=22.9
    )

    utente2_info = UserInfo(
        user_id=utente2.id,
        cc_number='987654321',
        health_number='123456789',
        gender='F',
        birth_date=date(1985, 5, 5),
        weight=60.0,
        height=165.0,
        bmi=22.0
    )

    db.session.add(utente1_info)
    db.session.add(utente2_info)
    db.session.commit()

    # Criar agendamentos de exemplo
    agendamento1 = Agendamento(
        user_id=utente1.id,
        tipo='Radiografia',
        data=date(2023, 6, 1),
        hora=time(10, 0),
        medico_id=medico.id
    )

    agendamento2 = Agendamento(
        user_id=utente2.id,
        tipo='Ultrassom',
        data=date(2023, 6, 2),
        hora=time(11, 0),
        medico_id=medico.id
    )

    db.session.add(agendamento1)
    db.session.add(agendamento2)
    db.session.commit()

    print("Dados de teste criados com sucesso!")
