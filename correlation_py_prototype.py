import re
import collections
import csv

data_path = '../netflix-prize-data/combined_data_1.txt'
film_names_path = '../netflix-prize-data/movie_titles.csv'

film_corrs_num = 200
max_read_films = 200

def main():
	ratings_dict = read_file()
	user_centric_dict = transform_input(ratings_dict)
	correlation_matrix = calculate_correlations(user_centric_dict)

	output_csv_with_names(correlation_matrix)


def calculate_correlations(user_centric_dict):

	correlation_matrix = [["" for x in range(film_corrs_num)] for y in range(film_corrs_num)]

	for film_1 in range(1, film_corrs_num):

		for film_2 in range(film_1+1, film_corrs_num):

			sum_x_times_y = 0
			sum_x = 0
			sum_y = 0
			sum_x_sq = 0
			sum_y_sq = 0

			for user_id in user_centric_dict:
				val_x = user_centric_dict[user_id].get(film_1, 0)
				val_y = user_centric_dict[user_id].get(film_2, 0)

				n = len(user_centric_dict)

				sum_x_times_y += val_x * val_y

				sum_x += val_x
				sum_y += val_y

				sum_x_sq += val_x * val_x
				sum_y_sq += val_y * val_y

			correlation_matrix[film_1][film_2] = round(
				( n * sum_x_times_y - sum_x * sum_y ) /
				( 
					( ( n * sum_x_sq - sum_x * sum_x ) ** 0.5 ) * 
					( ( n * sum_y_sq - sum_y * sum_y ) ** 0.5 )
				)
			, 3)

	return correlation_matrix

def transform_input(ratings_dict):

	user_centric_dict = collections.defaultdict(dict)

	for current_film_dict_id in ratings_dict:
		for user_id in ratings_dict[current_film_dict_id]:
			user_centric_dict[int(user_id)][current_film_dict_id] = 1 #int(ratings_dict[current_film_dict_id][user_id])

	return dict(user_centric_dict), len(ratings_dict)

def read_file():
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
	with open(film_names_path, 'rt') as csvfile:
		film_names = csv.reader(csvfile)

		for film_record in film_names:
			correlation_matrix[int(film_record[0])][0] = film_record[2]
			correlation_matrix[0][int(film_record[0])] = film_record[2]
			if int(film_record[0]) > len(correlation_matrix) - 2: break

	with open("correlationmatrix.csv", "wt") as f:
		writer = csv.writer(f, dialect='excel', delimiter=";")
		writer.writerows(correlation_matrix)

if __name__ == "__main__":
	main()

