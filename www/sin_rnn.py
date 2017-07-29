import tensorflow as tf
import csv
from tensorflow.python.ops import rnn, rnn_cell

rnn_size = 11
x = tf.placeholder(tf.float32, [None, 1, 1])
y = tf.placeholder(tf.float32)

batch_size = 10
epochs_count = 1000
iterations_count = 10000/batch_size
validation_count = 100/batch_size
# state = tf.zeros([batch_size, 1])

def get_data_ref(batch_size=1):
	columns_count = 2

	# prepare for fixture reading
	fixtures_files = tf.train.string_input_producer(["fixtures_1.csv"])
	reader = tf.TextLineReader()
	key, value = reader.read(fixtures_files)

	record_defaults = [[1.] for _ in range(columns_count)]
	columns = tf.decode_csv(value, record_defaults=record_defaults)
	label_data = tf.stack([[columns[i]] for i in range(columns_count-1)])
	feature_data = tf.stack([columns[-1]])

	if batch_size != -1:
		min_after_dequeue = 10000
		capacity = min_after_dequeue + 3 * batch_size
		label_data_batch, feature_data_batch = tf.train.batch([label_data, feature_data], batch_size=batch_size)

		return label_data_batch, feature_data_batch

	return label_data, feature_data

def last_relevant(output, length):
  batch_size = tf.shape(output)[0]
  max_length = tf.shape(output)[1]
  out_size = int(output.get_shape()[2])
  index = tf.range(0, batch_size) * max_length + (length - 1)
  flat = tf.reshape(output, [-1, out_size])
  relevant = tf.gather(flat, index)
  
  return relevant

def rnn_model(data):
	feature_columns_count = 1

	layer = {
		'weights': tf.Variable(tf.random_uniform([rnn_size, 1], -1, 1)),
		'biases': tf.Variable(tf.random_uniform([1]))
	}

	length = [feature_columns_count for _ in range(batch_size)]
	lstm_cell = rnn_cell.LSTMCell(rnn_size)
	# state = tf.zeros([batch_size, rnn_size])

	outputs, _ = rnn.dynamic_rnn(lstm_cell, data, dtype=tf.float32, sequence_length=length)
	# outputs, _ = lstm_cell(data, state)
	output = tf.matmul(last_relevant(outputs, feature_columns_count), layer['weights']) + layer['biases']

	return output

def rnn_train(x):
	train_data_count = iterations_count
	features, labels = get_data_ref(batch_size)
	
	prediction = rnn_model(x)
	cost = tf.reduce_mean(tf.square(prediction - y))
	optimizer = tf.train.AdamOptimizer(0.00005).minimize(cost)

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

			if (epoch + 1) % 10 == 0:

				for i in range((iterations_count - validation_count), iterations_count):
					feature, label = sess.run([features, labels])

					print "\n"
					print "Label is:", label
					print "Prediction is:", sess.run(prediction, {x:feature})
					print "\n"

			print 'Epoch', epoch + 1, 'is done'
			print 'Epoch lost is:', epoch_lost
			print '\n\n\n'

		coord.request_stop()
		coord.join(threads)

		print 'Done!'

rnn_train(x)