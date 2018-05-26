import numpy, threading, time
import execute_tests

class calculation_thread (threading.Thread):
	def __init__(self, film_1, film_2, user_centric_array, correlation_matrix, number_users):
		threading.Thread.__init__(self)
		self.film_1 = film_1
		self.film_2 = film_2
		self.user_centric_array = user_centric_array
		self.correlation_matrix = correlation_matrix
		self.number_users = number_users
	def run(self):
		sum_x_times_y = 0
		sum_x = 0
		sum_y = 0
		sum_x_sq = 0
		sum_y_sq = 0

		for user_line in self.user_centric_array:

			val_x = user_line[self.film_1]
			val_y = user_line[self.film_2]

			sum_x_times_y += val_x * val_y

			sum_x += val_x
			sum_y += val_y

			sum_x_sq += val_x * val_x
			sum_y_sq += val_y * val_y

		self.correlation_matrix[self.film_1+1][self.film_2+1] = round(
			( self.number_users * sum_x_times_y - sum_x * sum_y ) /
			( 
				( ( self.number_users * sum_x_sq - sum_x * sum_x ) ** 0.5 ) * 
				( ( self.number_users * sum_y_sq - sum_y * sum_y ) ** 0.5 )
			)
		, 3)


def calculate_correlations(user_centric_array, film_correlations_number):
	correlation_matrix = numpy.zeros([film_correlations_number+1, film_correlations_number+1])

	number_users = len(user_centric_array)

	started_threads = []

	for film_1 in range(0, film_correlations_number):
		for film_2 in range(film_1, film_correlations_number):
			spawned_thread = calculation_thread(film_1, film_2, user_centric_array, correlation_matrix, number_users).start()
			started_threads.append(spawned_thread)

			while threading.activeCount() > 100:
				time.sleep(0.01)

	while threading.activeCount() > 1:
		time.sleep(0.01)

	return correlation_matrix


if __name__ == "__main__":
	execute_tests.launcher("cpu_multi")


