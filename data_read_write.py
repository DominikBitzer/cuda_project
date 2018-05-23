import re, collections, csv, numpy

data_path = '../netflix-prize-data/combined_data_1.txt'
film_names_path = '../netflix-prize-data/movie_titles.csv'

correlation_matrix_output_path = 'correlationmatrix.csv'
transformed_data_path = 'user_centric_ratings.npy'

max_read_films = 200


def main():
	ratings_dict = read_original_netflix_file()
	user_centric_dict = transform_input(ratings_dict)
	write_transformed_data(user_centric_dict)


def transform_input(ratings_dict):
	user_centric_dict = collections.defaultdict(dict)

	for current_film_dict_id in ratings_dict:
		for user_id in ratings_dict[current_film_dict_id]:
			user_centric_dict[int(user_id)][current_film_dict_id] = 1 #int(ratings_dict[current_film_dict_id][user_id])

	return dict(user_centric_dict)


def write_transformed_data(user_centric_dict):
	ratings_matrix = numpy.zeros([len(user_centric_dict), max_read_films], dtype='int8') 

	for n_th_user_sequential, user_id in enumerate(user_centric_dict):
		for film_number_iterator in range(0, max_read_films):
			ratings_matrix[n_th_user_sequential][film_number_iterator] = user_centric_dict[user_id].get(film_number_iterator+1, 0)

	numpy.save(transformed_data_path, ratings_matrix)


def read_transformed_data(film_correlations_number):
	user_centric_array = numpy.load(transformed_data_path)

	return user_centric_array

def read_original_netflix_file():
	ratings_dict = {}
	rating_pattern = re.compile("^(\d{1,7}),([12345])")
	new_film_pattern = re.compile("^(\d{1,5}):")
	current_film = 0
	with open(data_path) as f:
		for line in f:
			my_match = rating_pattern.match(line)
			if my_match:
				rater_user_id = my_match.group(1)
				rating_score = my_match.group(2)
				ratings_dict[current_film][rater_user_id] = rating_score
			elif new_film_pattern.match(line):
				current_film += 1
				if current_film > max_read_films: break # TODO TESTING
				ratings_dict[current_film] = {}
			else:
				raise Exception("Couldn't match anything for string {}, done".format(line))

	return ratings_dict

def output_csv_with_names(correlation_matrix):
	correlation_matrix = [list(x) for x in correlation_matrix]
	
	with open(film_names_path, 'rt') as csvfile:
		film_names = csv.reader(csvfile)

		for film_record in film_names:
			correlation_matrix[int(film_record[0])][0] = film_record[2]
			correlation_matrix[0][int(film_record[0])] = film_record[2]
			if int(film_record[0]) > len(correlation_matrix) - 2: break

	with open(correlation_matrix_output_path, "wt") as f:
		writer = csv.writer(f, dialect='excel', delimiter=";")
		writer.writerows(correlation_matrix)


if __name__ == "__main__":
	main()

