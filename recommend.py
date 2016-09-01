import requests
import sys


collected_movie_ids = []
watched_movie_ids = []
unwatched_movie_ids = []

watched_movies_data = {}
unwatched_movies_data = {}
actors = {}
directors = {}
sorted_actors_by_movie_number = []
sorted_directors_by_movie_number = []


def sort_by_length_of_movie_list(data_dict):
    return [el for el in reversed(sorted(data_dict.items(), key=lambda x: len(x[1])))]


def sort_and_print_actors():
    # Sorting the actors regarding their number of movies
    sorted_actors_by_movie_number = sort_by_length_of_movie_list(actors)
    # Printing Top 10 favourite ACTORS name with movie name
    print('Top 10 Favourite ACTORS:')
    print('------------------------')
    for ind, actor in enumerate(sorted_actors_by_movie_number[0:10]):
        print('{}) {}\nMovies: {}\n'.format(ind+1, actor[0], ', '.join(actor[1])))

    return sorted_actors_by_movie_number


def sort_and_print_directors():
    # Sorting the directors regarding their number of movies
    sorted_directors_by_movie_number = sort_by_length_of_movie_list(directors)
    # Printing Top 10 favourite ACTORS name with movie name
    print('Top 10 Favourite DIRECTORS:')
    print('---------------------------')
    for ind, director in enumerate(sorted_directors_by_movie_number[0:10]):
        print('{}) {}'.format(ind+1, director[0]))

    return sorted_directors_by_movie_number


def build_actors_list():
    for movie_id, movie_data in watched_movies_data.items():
        for movie_actor in movie_data['Actors']:
            if movie_actor in actors:
                actors[movie_actor].append(movie_data['Title'])
            else:
                actors[movie_actor] = [movie_data['Title']]


def build_directors_list():
    for movie_id, movie_data in watched_movies_data.items():
        for movie_director in movie_data['Directors']:
            if movie_director not in ['N/A']:
                if movie_director in directors:
                    directors[movie_director].append(movie_data['Title'])
                else:
                    directors[movie_director] = [movie_data['Title']]


def recommend_unwatched_movie():
    top_ten_actors = [actor[0] for actor in sorted_actors_by_movie_number[0:10]]
    top_ten_directors = [director[0] for director in sorted_directors_by_movie_number[0:10]]

    recommended_movie_by_actors = []
    for movie_id, movie_data in unwatched_movies_data.items():
        if len(set(movie_data['Actors']).intersection(set(top_ten_actors))) > 0:
            recommended_movie_by_actors.append(movie_data)

    print(recommended_movie_by_actors)
    print(len(recommended_movie_by_actors))

    recommended_movie_by_actors_and_directors = []
    for movie_data in recommended_movie_by_actors:
        if len(set(movie_data['Directors']).intersection(set(top_ten_directors))) > 0:
            recommended_movie_by_actors_and_directors.append(movie_data)

    print('')
    print('')
    print(recommended_movie_by_actors_and_directors)

def scrape_movie(movie_id):
    response = requests.get('http://www.omdbapi.com/?i={}&plot=short&r=json'.format(movie_id))

    # Printing progress bar
    sys.stdout.flush()
    sys.stdout.write('.')

    movie_data = response.json()
    movie_data['Actors'] = [el.strip() for el in movie_data['Actors'].split(',')]
    movie_data['Directors'] = [el.strip() for el in movie_data['Director'].split(',')]
    return movie_data


def scrap_movie_data():
    # Reading movie ids of watched movies
    with open('watched.txt') as watched_movie_ids_file:
        for movie_id in watched_movie_ids_file.readlines():
            watched_movie_ids.append(movie_id.strip())

    # Reading movie ids of collected movies
    with open('movies.txt') as collected_movie_ids_file:
        for movie_id in collected_movie_ids_file.readlines():
            collected_movie_ids.append(movie_id.strip())

    unwatched_movie_ids = list(set(collected_movie_ids) - set(watched_movie_ids))

    # scraping all the movie data from watched movies with OMDB API
    print('Scraping watched movie data:')
    for movie_id in watched_movie_ids:
        movie_data = scrape_movie(movie_id)
        watched_movies_data[movie_id] = movie_data
    print('')

    # scraping all the movie data from unwatched movies with OMDB API
    print('Scraping unwatched movie data:')
    for movie_id in unwatched_movie_ids:
        movie_data = scrape_movie(movie_id)
        unwatched_movies_data[movie_id] = movie_data
    print('')



if __name__ == '__main__':
    # Scraping all movie data
    print('')
    scrap_movie_data()

    # Building all needed data structures
    build_actors_list()
    build_directors_list()

    # Display all stuffs
    print('\n')
    sorted_actors_by_movie_number = sort_and_print_actors()
    sorted_directors_by_movie_number = sort_and_print_directors()
    print('')

    recommend_unwatched_movie()
