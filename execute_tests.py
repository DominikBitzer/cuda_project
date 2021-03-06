import time, argparse
import data_read_write


film_correlations_number_default = 10

def launcher(implementation_version, film_correlations_number = 6):

	if implementation_version == "cpu_single":
		import cpu_single as correlation_container
	elif implementation_version == "cpu_compiled":
		import cpu_compiled as correlation_container
	elif implementation_version == "cpu_multi":
		import cpu_multi as correlation_container
	elif implementation_version == "cuda_1simple":
		import cuda_1simple as correlation_container
	elif implementation_version == "cuda_2multithread":
		import cuda_2multithread as correlation_container
	elif implementation_version == "cuda_mapped_test":
		import cuda_mapped_test as correlation_container

	user_centric_array = data_read_write.read_transformed_data(film_correlations_number)

	start_time = time.time()
	correlation_matrix = correlation_container.calculate_correlations(user_centric_array, film_correlations_number)
	print("Calculation of correlations of {} films with version \"{}\" took {} seconds.".format(film_correlations_number, implementation_version, time.time() - start_time))

	data_read_write.output_csv_with_names(correlation_matrix.round(decimals=4))



if __name__ == "__main__":

	parser = argparse.ArgumentParser("...")
	parser.add_argument("-i", "--implementation_version")
	parser.add_argument("-n", "--film_correlations_number", type = int, default = film_correlations_number_default)
	args = parser.parse_args()

	launcher(args.implementation_version, args.film_correlations_number)

