# movie-freak
A small movie recommendation system using OMDB API's

## Please run the below commands in terminal
$ virtualenv -p python3 movie-freak-env

$ cd movie-freak-env

$ source bin/activate

$ git clone https://github.com/tanvirrazin/movie-freak.git

$ cd movie-freak

$ pip install -r requirements.txt

$ python recommend.py

## Description
1) At first all the movie-ids in `watched.txt` and `movies.txt` files were read, differentiated watched and unwatched movies and scraped all the movie data using the OMDB API and kept in two different lists (one for watched-movies and one for unwatched-movies).

2) From watched-movie list, extracted all distinct Actors (identified by name) and Directors (identified by name) and kept in two different dictionaries with the list of the movie name, in which the Actor or the Directors were involved.

3) Sorted each of the dictionaries for actors and directors based on the number of watched-movies they were involved in.

4) Printed top 10 Actors and top 10 Directors names.

5) Extracted all the unwatched-movies, in which top 10 actors were involved.

6) Extracted all the unwatched-movies, in which top 10 directors were involved.

7) Made union of those movies, and shown the first 10 movies from that set.
