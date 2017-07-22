import tensorflow as tf
import csv

def get_data_ref(batch_size=1):
	columns_count = 11

	# prepare for fixture reading
	fixtures_files = tf.train.string_input_producer(["fixtures_1.csv"])
	reader = tf.TextLineReader()
	key, value = reader.read(fixtures_files)

	record_defaults = [[1.] for _ in range(columns_count)]
	columns = tf.decode_csv(value, record_defaults=record_defaults)
	label_data = tf.stack(columns[0:(columns_count-1)])
	feature_data = tf.stack([columns[-1]])

	if batch_size != 1:
		min_after_dequeue = 10000
		capacity = min_after_dequeue + 3 * batch_size
		# label_data_batch, feature_data_batch = tf.train.shuffle_batch(
		# 											[label_data, feature_data], 
		# 											batch_size=batch_size, 
		# 											capacity=capacity,
		# 											min_after_dequeue=min_after_dequeue
		# 										)

		label_data_batch, feature_data_batch = tf.train.batch(
													[label_data, feature_data], 
													batch_size=batch_size
												)


		return label_data_batch, feature_data_batch

	return label_data, feature_data

x_ref, y_ref = get_data_ref(3)

with tf.Session() as sess:
	coord = tf.train.Coordinator()
	threads = tf.train.start_queue_runners(coord=coord)

	for _ in range(3):
		x1, x2 = sess.run([x_ref, y_ref])

		print x1, "\n", x2, "\n\n\n\n"

	coord.request_stop()
	coord.join(threads)

sess.close()