import requests
import sys


watched_movies_data = []
actors = {}
directors = {}


def sort_by_length_of_movie_list(data_dict):
    return sorted(data_dict.items(), key=lambda x: len(x[1]))


def sort_and_print_actors():
    # Sorting the actors regarding their number of movies
    sorted_actors_by_movie_number = sort_by_length_of_movie_list(actors)
    # Printing Top 10 favourite ACTORS name with movie name
    print('Top 10 Favourite ACTORS:')
    print('------------------------')
    for ind, actor in enumerate(sorted_actors_by_movie_number[-1:-11:-1]):
        print('{}) {}\nMovies: {}\n'.format(ind+1, actor[0], ', '.join(actor[1])))


def sort_and_print_directors():
    # Sorting the directors regarding their number of movies
    sorted_directors_by_movie_number = sort_by_length_of_movie_list(directors)
    # Printing Top 10 favourite ACTORS name with movie name
    print('Top 10 Favourite DIRECTORS:')
    print('---------------------------')
    for ind, director in enumerate(sorted_directors_by_movie_number[-1:-11:-1]):
        print('{}) {}'.format(ind+1, director[0]))


def build_actors_list():
    for movie_data in watched_movies_data:
        movie_actors = [el.strip() for el in movie_data['Actors'].split(',')]
        for movie_actor in movie_actors:
            if movie_actor in actors:
                actors[movie_actor].append(movie_data['Title'])
            else:
                actors[movie_actor] = [movie_data['Title']]


def build_directors_list():
    for movie_data in watched_movies_data:
        movie_directors = [el.strip() for el in movie_data['Director'].split(',')]
        for movie_director in movie_directors:
            if movie_director not in ['N/A']:
                if movie_director in directors:
                    directors[movie_director].append(movie_data['Title'])
                else:
                    directors[movie_director] = [movie_data['Title']]


def scrap_movie_data():
    with open('watched.txt') as collected_movie_ids:

        # scraping all the movie data from collected movies with OMDB API
        movie_count = 0
        for movie_id in collected_movie_ids.readlines():
            movie_id = movie_id.strip()

            response = requests.get('http://www.omdbapi.com/?i={}&plot=short&r=json'.format(movie_id))
            watched_movies_data.append(response.json())

            # Printing progress bar
            sys.stdout.flush()
            sys.stdout.write('.')
            movie_count += 1
        print('{} movie-data were scraped'.format(movie_count))


if __name__ == '__main__':
    # Scraping all movie data
    scrap_movie_data()

    # Building all needed data structures
    build_actors_list()
    build_directors_list()

    # Display all stuffs
    print('\n')
    sort_and_print_actors()
    sort_and_print_directors()
    print('')
