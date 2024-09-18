import datetime
from lib2to3.fixes.fix_input import context

from flask import Blueprint, jsonify, render_template, request
from flask_login import login_required
import uuid
# Models
from models.MovieModel import MovieModel
# Entities
from models.entities.Movie import Movie
# DB Connection
from database.db import get_connection

main = Blueprint('movie_blueprint', __name__)

def get_number_of_coupons_redeemed_so_far():
    connection = get_connection()
    with connection.cursor() as cursor:
        cursor.execute("""SELECT COUNT(*) AS total_rows FROM cupones;""")
        redeemed_coups = cursor.fetchone()[0]
        print(redeemed_coups)
    return redeemed_coups


@main.route('/')
@login_required
def get_movies():
    try:
        movies = MovieModel.get_movies()
        return jsonify(movies)
        #return render_template('index.html')
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@main.route('/<id>')
@login_required
def get_movie(id):
    try:
        movie = MovieModel.get_movie(id)
        if movie != None:
            return jsonify(movie)
        else:
            return jsonify({}), 404
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


@main.route('/add', methods=['GET', 'POST'])
@login_required
def add_movie():
    tiendas = [
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
                return jsonify(movie.id_tienda)
            else:
                return jsonify({'message': "Error on insert"}), 500

        except Exception as ex:
            return jsonify({'message': str(ex)}), 500

    return render_template(
            "index.html",
            tiendas=tiendas,
            cupones_canjeados=get_number_of_coupons_redeemed_so_far()
        )
