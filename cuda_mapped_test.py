from __future__ import division
from numba import cuda, float32
import math

import numpy, threading, time
import execute_tests

@cuda.jit('void(int8[:,:], float64[:,:], int32, int32)')
def calculation_thread(user_centric_array_global_mem, correlation_matrix_global_mem, number_users, film_correlations_number):

	find_my_position = cuda.grid(1)

	film_1 = 0
	while film_1 < film_correlations_number:

		film_2 = film_1
		while film_2 < film_correlations_number:

			if find_my_position > 0:
				find_my_position -= 1
				film_2 += 1
				continue

			sum_x_times_y = 0
			sum_x = 0
			sum_y = 0
			sum_x_sq = 0
			sum_y_sq = 0

			user_id = 0
			while user_id < number_users:
				user_id += 1

				val_x = user_centric_array_global_mem[user_id, film_1]
				val_y = user_centric_array_global_mem[user_id, film_2]

				sum_x_times_y += val_x * val_y

				sum_x += val_x
				sum_y += val_y

				sum_x_sq += val_x * val_x
				sum_y_sq += val_y * val_y

			correlation_matrix_global_mem[film_1+1, film_2+1] = 5

#			correlation_matrix_global_mem[film_1+1, film_2+1] = (
#					( number_users * sum_x_times_y - sum_x * sum_y ) /
#					( 
#						( ( number_users * sum_x_sq - sum_x * sum_x ) ** 0.5 ) * 
#						( ( number_users * sum_y_sq - sum_y * sum_y ) ** 0.5 )
#					)
#				)

#			correlation_matrix_global_mem[film_1+1, film_2+1] = (
#					( number_users * sum_x_times_y - sum_x * sum_y ) /
#					( 
#						( ( number_users * sum_x_sq - sum_x * sum_x ) ** 0.5 ) * 
#						( ( number_users * sum_y_sq - sum_y * sum_y ) ** 0.5 )
#					)
#				)

			return

		film_1 += 1



def calculate_correlations(user_centric_array, film_correlations_number):

	number_users = len(user_centric_array)

	# CUDA stuff

	stream = cuda.stream()

	with stream.auto_synchronize():

		threadsperblock = 8
		correlation_fields_to_fill = sum(range(film_correlations_number+1))
		blockspergrid = math.ceil(correlation_fields_to_fill / threadsperblock)

		user_centric_array_global_mem = cuda.to_device(user_centric_array, stream=stream)
		correlation_matrix_global_mem = cuda.mapped_array((film_correlations_number+1, film_correlations_number+1), dtype='float64')

		y = numpy.ones((1,1), dtype='float64')
		yc = cuda.to_device(y, stream=stream)

		# Start calculations
		calculation_thread[blockspergrid, threadsperblock](user_centric_array_global_mem, correlation_matrix_global_mem, int(number_users), int(film_correlations_number))



	print(correlation_matrix_global_mem)
	return correlation_matrix_global_mem



if __name__ == "__main__":
	execute_tests.launcher("cuda_mapped_test")

