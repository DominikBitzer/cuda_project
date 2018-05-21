import data_read_write, numpy

import cProfile

film_correlations_number = 10

def main():
	user_centric_array = data_read_write.read_transformed_data(film_correlations_number)

	correlation_matrix = calculate_correlations(user_centric_array)

	data_read_write.output_csv_with_names(correlation_matrix)


def calculate_correlations(user_centric_array):
	correlation_matrix = numpy.zeros([film_correlations_number+1, film_correlations_number+1])

	number_users = len(user_centric_array)

	for film_1 in range(0, film_correlations_number):

		for film_2 in range(film_1, film_correlations_number):

			sum_x_times_y = 0
			sum_x = 0
			sum_y = 0
			sum_x_sq = 0
			sum_y_sq = 0

			for user_dict in user_centric_array:
				val_x = user_dict[film_1]
				val_y = user_dict[film_2]

				sum_x_times_y += val_x * val_y

				sum_x += val_x
				sum_y += val_y

				sum_x_sq += val_x * val_x
				sum_y_sq += val_y * val_y

			correlation_matrix[film_1+1][film_2+1] = round(
				( number_users * sum_x_times_y - sum_x * sum_y ) /
				( 
					( ( number_users * sum_x_sq - sum_x * sum_x ) ** 0.5 ) * 
					( ( number_users * sum_y_sq - sum_y * sum_y ) ** 0.5 )
				)
			, 3)

	return correlation_matrix


if __name__ == "__main__":
#	cProfile.run("main()")
	main()

