import tensorflow as tf
from tensorflow.python.ops import rnn, rnn_cell

# prepare for fixture reading
fixtures_files = tf.train.string_input_producer(["fixtures_1.csv"])
reader = tf.TextLineReader()
key, value = reader.read(fixtures_files)

record_defaults = [[1], [1], [1]]
col1, col2, col3 = tf.decode_csv(value, record_defaults=record_defaults)
input_data = tf.stack([[col1], [col2]])

# prepare nn model params
rnn_size = 32

x = tf.placeholder(tf.float32, [2, 1])
y = tf.placeholder(tf.float32)

# define nn model computational graph
def rnn_model(data):
	layer = {
		'weights': tf.Variable(tf.random_uniform([rnn_size, 1], -1, 1)),
		'biases': tf.Variable(tf.random_normal([]))
	}

	data = tf.split(data, 2, 0)

	lstm_cell = rnn_cell.BasicLSTMCell(rnn_size, state_is_tuple=True)
	outputs, _ = rnn.static_rnn(lstm_cell, data, dtype=tf.float32)

	output = tf.matmul(outputs[-1], layer['weights']) + layer['biases']

	return output

# define a way the nn trains
epochs_count = 2
iterations_count = 100000
validation_count = 10

def rnn_train(x):
	prediction = rnn_model(x)
	cost = tf.reduce_mean(tf.square(prediction - y))
	optimizer = tf.train.AdamOptimizer().minimize(cost)

	with tf.Session() as sess:
		# Start populating the filename queue.
		coord = tf.train.Coordinator()
		threads = tf.train.start_queue_runners(coord=coord)
		
		sess.run(tf.global_variables_initializer())

		for epoch in range(epochs_count):
			epoch_lost = 0
			
			for i in range(iterations_count - validation_count):
			    x1, x2 = sess.run([input_data, col3])
			    _, loss = sess.run([optimizer, cost], feed_dict={x:x1, y:x2})

			    if i % 1000 == 0:
			    	print 'Epoch', epoch + 1, 'Data set', i
			    # 	print input_data
			    # 	print sess.run(prediction, {x:input_data})

			    epoch_lost += loss

			for i in range(validation_count):
				x1, x2 = sess.run([input_data, col3])

				print "\n"
				print "Input is:", x1, "Label is:", x2
				print "Prediction is:", sess.run(prediction, {x:x1})
				print "\n"

			print 'Epoch', epoch + 1, 'is done'
			print 'Epoch lost is:', epoch_lost
			print '\n\n\n'

			sess.run(reader.reset())

		coord.request_stop()
  		coord.join(threads)

		print 'Done!'

rnn_train(x)