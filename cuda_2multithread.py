from __future__ import division
from numba import cuda, float32
import math

import numpy, threading, time
import execute_tests


@cuda.jit
def calculation_thread(user_centric_array_global_mem, correlation_matrix_global_mem, number_users, film_correlations_number):

	find_my_position = cuda.grid(1)

	for film_1 in range(0, film_correlations_number):
		for film_2 in range(film_1, film_correlations_number):
			if find_my_position > 0:
				find_my_position -= 1
				continue

			sum_x_times_y = 0
			sum_x = 0
			sum_y = 0
			sum_x_sq = 0
			sum_y_sq = 0

			for i in range(number_users):

				val_x = user_centric_array_global_mem[i][film_1]
				val_y = user_centric_array_global_mem[i][film_2]

				sum_x_times_y += val_x * val_y

				sum_x += val_x
				sum_y += val_y

				sum_x_sq += val_x * val_x
				sum_y_sq += val_y * val_y

			correlation_matrix_global_mem[film_1+1][film_2+1] = (
					( number_users * sum_x_times_y - sum_x * sum_y ) /
					( 
						( ( number_users * sum_x_sq - sum_x * sum_x ) ** 0.5 ) * 
						( ( number_users * sum_y_sq - sum_y * sum_y ) ** 0.5 )
					)
				)

			return


def calculate_correlations(user_centric_array, film_correlations_number):

	number_users = len(user_centric_array)

	# CUDA stuff
	user_centric_array_global_mem = cuda.to_device(user_centric_array)
	correlation_matrix_global_mem = cuda.device_array((film_correlations_number+1, film_correlations_number+1))

	threadsperblock = 8
	correlation_fields_to_fill = sum(range(film_correlations_number+1))
	blockspergrid = math.ceil(correlation_fields_to_fill / threadsperblock)

	# Start calculations
	calculation_thread[blockspergrid, threadsperblock](user_centric_array_global_mem, correlation_matrix_global_mem, number_users, film_correlations_number)

	correlation_matrix_results = correlation_matrix_global_mem.copy_to_host()

	return correlation_matrix_results


if __name__ == "__main__":
	execute_tests.launcher("cuda_2multithread")


