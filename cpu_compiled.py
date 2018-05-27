from __future__ import division
from numba import jit
import math

import numpy, threading, time
import execute_tests

@jit
def calculation_thread(user_centric_array_global_mem, correlation_matrix_global_mem, number_users, film_correlations_number):

	for film_1 in range(0, film_correlations_number):
		for film_2 in range(film_1, film_correlations_number):

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


def calculate_correlations(user_centric_array, film_correlations_number):

	number_users = len(user_centric_array)

	# CUDA stuff
	correlation_matrix_global_mem = numpy.zeros((film_correlations_number+1, film_correlations_number+1))

	# Start calculations
	calculation_thread(user_centric_array, correlation_matrix_global_mem, number_users, film_correlations_number)

	return correlation_matrix_global_mem


if __name__ == "__main__":
	execute_tests.launcher("cpu_compiled")


