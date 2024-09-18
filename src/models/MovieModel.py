from database.db import get_connection
from .entities.Movie import Movie


class MovieModel():
    @classmethod
    def get_movies(self):
        try:
            connection = get_connection()
            movies = []

            with connection.cursor() as cursor:
                cursor.execute("SELECT id_tienda, fechahora_canje FROM cupones ORDER BY fechahora_canje ASC")
                resultset = cursor.fetchall()

                for row in resultset:
                    movie = Movie(row[0], row[1])
                    movies.append(movie.to_JSON())

            connection.close()
            return movies
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_movie(self, id_tienda):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute("SELECT id_tienda, fechahora_canje FROM cupones WHERE id_tienda = ? ORDER BY fechahora_canje ASC", (id_tienda,))
                row = cursor.fetchone()

                movie = None
                if row != None:
                    movie = Movie(row[0], row[1])
                    movie = movie.to_JSON()

            connection.close()
            return movie
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def add_movie(self, movie):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute("""INSERT INTO cupones (id_tienda, fechahora_canje) 
                                VALUES (?, ?)""", (movie.id_tienda, movie.fechahora_canje))
                affected_rows = cursor.rowcount
                connection.commit()

            connection.close()
            print("movie was added")
            return affected_rows
        except Exception as ex:
            raise Exception(ex)