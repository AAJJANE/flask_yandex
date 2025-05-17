import datetime
from flask import Flask, render_template, request, redirect, make_response, abort, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_restful import Api
from data import __db_session as db_session

db_session.global_init("db/database.sqlite")

from forms import SelectionForm, LoginForm, ExtraLoginForm, RegisterForm, JobFormFactory

from data.users import User
from data.jobs import Jobs
from api import jobs as jobs_api
from api import users as users_api

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
api = Api(app)


@login_manager.user_loader
def load_user(user_id: id) -> User | None:
    return db_session.create_session().get(User, user_id)


@app.route('/')
def index():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    params = {
        'title': 'Works log',
        'jobs': jobs
    }
    return render_template('index.html', **params)


@app.route('/training/<prof>')
def training(prof: str):
    params = {
        'title': 'Тренировки в полёте',
        'prof': prof
    }
    return render_template('training.html', **params)


@app.route('/list_prof/<tag>')
def list_prof(tag: str):
    profs = '''инженер-исследователь
пилот
строитель
экзобиолог
врач
инженер по терраформированию
климатолог
специалист по радиационной защите
астрогеолог
гляциолог
инженер жизнеобеспечения
метеоролог
оператор марсохода
киберинженер
штурман
пилот дронов'''.splitlines()
    params = {
        'title': '',
        'profs': profs,
        'tag': tag
    }
    return render_template('list_prof.html', **params)


@app.route('/astronaut_selection', methods=['GET', 'POST'])
def astronaut_selection():
    form = SelectionForm()
    if form.validate_on_submit():
        return answer(form)
    return render_template('_base_form.html', title='Отбор астронавтов', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('_base_form.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('_base_form.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('_base_form.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('_base_form.html', title='Регистрация', form=form)


@app.route('/extra_login', methods=['GET', 'POST'])
def extra_login():
    form = ExtraLoginForm()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template('_base_form.html', title='Аварийный доступ', form=form)


@app.route('/answer')
@app.route('/auto_answer')
def _answer():
    return answer()


def answer(form=None):
    form = form or SelectionForm()
    data = {
        'title': 'Анкета',
        'surname': form.surname.data,
        'name': form.name.data,
        'education': form.selectEducation.data,
        'profession': form.prof.data or [None],
        'sex': form.sex.data,
        'motivation': form.description.data,
        'ready': form.access.data,
    }
    return render_template('auto_answer.html', **data)


@app.route('/jobs', methods=['GET', 'POST'])
@login_required
def add_news():
    if request.method == 'GET':
        return render_template('_base_form.html', title='Adding job', form=JobFormFactory()())
    db_sess = db_session.create_session()
    job = Jobs()
    form = JobFormFactory(db_sess)(request.form, obj=job)
    if form.validate() and request.method == 'POST':
        form.populate_obj(job)
        db_sess.merge(job)
        db_sess.commit()
        return redirect('/')
    return render_template('_base_form.html', title='Adding job', form=form)


@app.route('/jobs/<int:_id>', methods=['GET', 'POST'])
@login_required
def edit_news(_id):
    db_sess = db_session.create_session()
    job = db_sess.get(Jobs, _id)
    if job is None:
        abort(404)
    if not (job.team_leader_obj == current_user or current_user.is_admin()):
        abort(403)
    form = JobFormFactory(db_sess, "Save")(request.form, obj=job)
    if request.method == "GET":
        return render_template('_base_form.html', title='Editing job', form=form)
    if form.validate() and request.method == 'POST':
        form.populate_obj(job)
        db_sess.merge(job)
        db_sess.commit()
        return redirect('/')


@app.route('/jobs_delete/<int:_id>')
@login_required
def jobs_delete(_id):
    db_sess = db_session.create_session()
    job = db_sess.get(Jobs, _id)
    if job is None:
        abort(404)
    if job.team_leader_obj != current_user:
        abort(403)
    db_sess.delete(job)
    db_sess.commit()
    return redirect('/')


@app.errorhandler(404)
def not_found(error):
    print(error)
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(error):
    print(error)
    return make_response(jsonify({'error': 'Bad Request'}), 400)


if __name__ == '__main__':
    app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
    app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=365)
    app.register_blueprint(jobs_api.blueprint)
    app.register_blueprint(users_api.blueprint)
    app.run(port=8080, debug=True)
