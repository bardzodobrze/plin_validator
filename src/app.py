import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_wtf.csrf import CSRFProtect, generate_csrf
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from config import config

# Models:
from models.ModelUser import ModelUser
from models.MovieModel import MovieModel

# Entities:
from models.entities.User import User
from models.entities.Movie import Movie

# DB connection
from database.db import get_connection

app = Flask(__name__)
#csrf = CSRFProtect()
#csrf_token = generate_csrf()
login_manager_app = LoginManager(app)


def get_number_of_coupons_redeemed_so_far():
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute("""SELECT COUNT(*) AS total_rows FROM cupones;""")
        redeemed_coups = cursor.fetchone()[0]
        print(redeemed_coups)
    return redeemed_coups


@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(id)

@app.route('/')
@login_required
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # print(request.form['username'])
        # print(request.form['password'])
        user = User(0, request.form['username'], request.form['password'])
        logged_user = ModelUser.login(user)
        if logged_user != None:
            if logged_user.password:
                login_user(logged_user)
                return redirect(url_for('add_movie'))
            else:
                flash("Invalid password...")
                return render_template('auth/login.html')
        else:
            flash("User not found...")
            return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')


@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_movie():
    tiendas = [
        '',
        '18600 - BENAVIDES MIRAFLORES',
        '18601 - CHORRILLOS',
        '18602 - SAN JUAN DE MIRAFLORES',
        '18603 - MAGDALENA',
        '18604 - SUCRE',
        '18605 - SAN BORJA',
        '18606 - FAUCETT',
        '18607 - LA MARINA',
        '18608 - SAN JUAN DE LURIGANCHO',
        '18609 - CONSTRUCTORES',
        '18610 - BENAVIDES SURCO',
        '18611 - MOLICENTRO',
        '18612 - CORPAC',
        '18614 - LOS OLIVOS',
        '18615 - EL POLO',
        '18616 - PROCERES',
        '18617 - RAUL FERRERO',
        '18618 - COMANDANTE ESPINAR',
        '18619 - LINCE',
        '18620 - CALLAO',
        '18621 - SAN LUIS',
        '18622 - SAN MARTIN',
        '18623 - LA VICTORIA',
        '18624 - BARRANCO',
        '18625 - COMAS'
    ]

    if request.method == 'POST':
        try:
            id_tienda = request.form.get('tiendas').split()[0]
            fechahora_canje = datetime.datetime.now()
            movie = Movie(id_tienda, fechahora_canje)

            affected_rows = MovieModel.add_movie(movie)

            if affected_rows == 1:
                render_template('index.html')
            else:
                return jsonify({'message': "Error on insert"}), 500

        except Exception as ex:
            return jsonify({'message': str(ex)}), 500

    return render_template(
            "index.html",
            tiendas=tiendas,
            cupones_canjeados=get_number_of_coupons_redeemed_so_far()
        )


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/home')
@login_required
def home():
    return render_template('index.html')


def status_401(error):
    return redirect(url_for('login'))


def status_404(error):
    return "<h1>Página no encontrada</h1>", 404


if __name__ == '__main__':
    app.config.from_object(config['development'])

    # Blueprints
    # app.register_blueprint(Movie.main, url_prefix='/api/movies')

    app.register_error_handler(404, status_404)
    app.register_error_handler(401, status_401)
    app.run()