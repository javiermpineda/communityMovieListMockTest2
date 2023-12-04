import requests
from flask import Flask, request, jsonify, render_template, redirect, url_for
from movie_crud import MovieCRUD
from database import init_db
from datetime import datetime

app = Flask(__name__)
crud = MovieCRUD()

@app.route('/')
def index():
    movies = crud.get_all_movies()
    return render_template('index.html', movies=movies)

@app.route('/add_movie', methods=['GET', 'POST'])
def add_movie():
    if request.method == 'POST':
        try:
            data = {
                'movie_id': request.form['movie_id'],
                'title': request.form['title'],
                'image_url': request.form['image_url'],
                'updated': datetime.now(),
                'url_streaming': request.form['url_streaming']
            }
            crud.create(data)
        except ValueError as e:
            return str(e), 400  # Return the error message with a 400 Bad Request status

        return redirect(url_for('index'))

    return render_template('add_movie.html')

@app.route('/view_movie/<string:movie_id>')
def view_movie(movie_id):
    movie = crud.read(movie_id)
    if movie:
        return render_template('view_movie.html', movie=movie)
    return 'Movie not found', 404

@app.route('/delete_movie/<string:movie_id>', methods=['POST'])
def delete_movie(movie_id):
    crud.delete(movie_id)
    return redirect(url_for('index'))

@app.route('/search_movie', methods=['GET', 'POST'])
def search_movie():
    movies = None
    if request.method == 'POST':
        search_term = request.form['search_term']
        url = "https://utelly-tv-shows-and-movies-availability-v1.p.rapidapi.com/lookup"
        querystring = {"term": search_term, "country": "ca"}
        headers = {
            "X-RapidAPI-Key": "2226a5ffcbmsh41e5138dc667816p1a05f8jsn125f54b44b23",
            "X-RapidAPI-Host": "utelly-tv-shows-and-movies-availability-v1.p.rapidapi.com"
        }
        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()
        movies = data.get('results', [])

    return render_template('search_movie.html', movies=movies)

@app.route('/add_movie_from_search', methods=['POST'])
def add_movie_from_search():
    try:
        # Extract and process form data
        data = {
            'movie_id': request.form['movie_id'],
            'title': request.form['name'],
            'image_url': request.form['picture'],
            'updated': datetime.now(),  # Make sure to format correctly
            'url_streaming': 'example_streaming_url'  # Update as needed
        }
        crud.create(data)
        # Redirect to the index page after successful data processing
        return redirect(url_for('index'))

    except Exception as e:
        # Handle exceptions, maybe log the error or notify the user
        print("Error:", e)
        # Redirect or show an error message
        return redirect(url_for('index'))  # Redirect to the index or error page




if __name__ == '__main__':
    init_db()  # Initialize the database
    app.run(debug=True)
