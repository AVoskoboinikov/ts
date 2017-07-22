import tensorflow as tf
import csv
from tensorflow.python.ops import rnn, rnn_cell

rnn_size = 10
x = tf.placeholder(tf.float32, [10, 1])
y = tf.placeholder(tf.float32)

# define a way the nn trains
# batch_size = 10
epochs_count = 100
iterations_count = 1000
validation_count = 20

def get_data_ref(batch_size=1):
	columns_count = 11

	# prepare for fixture reading
	fixtures_files = tf.train.string_input_producer(["fixtures_1.csv"])
	reader = tf.TextLineReader()
	key, value = reader.read(fixtures_files)

	record_defaults = [[1.] for _ in range(columns_count)]
	columns = tf.decode_csv(value, record_defaults=record_defaults)
	label_data = tf.stack([[columns[i]] for i in range(columns_count-1)])
	feature_data = tf.stack([columns[-1]])

	if batch_size != 1:
		min_after_dequeue = 10000
		capacity = min_after_dequeue + 3 * batch_size
		label_data_batch, feature_data_batch = tf.train.batch([label_data, feature_data], batch_size=batch_size)

		return label_data_batch, feature_data_batch

	return label_data, feature_data

# def read_data(rows_count):
# 	columns_count = 11

# 	# prepare for fixture reading
# 	fixtures_files = tf.train.string_input_producer(["fixtures_1.csv"])
# 	reader = tf.TextLineReader()
# 	key, value = reader.read(fixtures_files)

# 	record_defaults = [[1.] for _ in range(columns_count)]
# 	columns = tf.decode_csv(value, record_defaults=record_defaults)
# 	label_data = tf.stack(columns[0:(columns_count-1)])
# 	feature_data = tf.stack([columns[-1]])

# 	labels = []
# 	features = []

# 	with tf.Session() as sess:
# 		sess.run(tf.global_variables_initializer())

# 		# Start populating the filename queue.
# 		coord = tf.train.Coordinator()
# 		threads = tf.train.start_queue_runners(coord=coord)

# 		for _ in range(rows_count):

# 			x1, x2 = sess.run([label_data, feature_data])

# 			labels.append(x1)
# 			features.append(x2)

# 		coord.request_stop()
# 		coord.join(threads)

# 	sess.close()

# 	return batched_label_data, batched_feature_data


def rnn_model(data):
	layer = {
		'weights': tf.Variable(tf.random_uniform([rnn_size, 1], -0.4, 0.4)),
		'biases': tf.Variable(tf.random_uniform([]))
	}

	data = tf.split(data, 10, 0)

	lstm_cell = rnn_cell.LSTMCell(rnn_size, state_is_tuple=True, activation=tf.nn.relu)
	outputs, _ = rnn.static_rnn(lstm_cell, data, dtype=tf.float32)

	output = tf.matmul(outputs[-1], layer['weights']) + layer['biases']

	return output

def rnn_train(x):
	train_data_count = iterations_count
	features, labels = get_data_ref(1)
	
	prediction = rnn_model(x)
	cost = tf.reduce_mean(tf.square(prediction - y))
	optimizer = tf.train.AdamOptimizer(0.0005).minimize(cost)
	# lossLogFile = open('loss.csv', 'wb')

	with tf.Session() as sess:
		sess.run(tf.global_variables_initializer())

		coord = tf.train.Coordinator()
		threads = tf.train.start_queue_runners(coord=coord)

		for epoch in range(epochs_count):
			epoch_lost = 0
			
			for i in range(0, (iterations_count - validation_count)):
				feature, label = sess.run([features, labels])
				_, loss = sess.run([optimizer, cost], feed_dict={x:feature, y:label})

				epoch_lost += loss

			if (epoch + 1) % epochs_count == 0:

				for i in range((iterations_count - validation_count), iterations_count):
					feature, label = sess.run([features, labels])

					print "\n"
					print "Input is:", feature, "Label is:", label
					print "Prediction is:", sess.run(prediction, {x:feature})
					print "\n"

			print 'Epoch', epoch + 1, 'is done'
			print 'Epoch lost is:', epoch_lost
			print '\n\n\n'

			# fixtureFile = csv.writer(lossLogFile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
			# fixtureFile.writerow([(epoch + 1), loss])

		coord.request_stop()
		coord.join(threads)

		print 'Done!'

rnn_train(x)