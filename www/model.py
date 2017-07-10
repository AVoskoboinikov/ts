import tensorflow as tf

# prepare for fixture reading
fixtures_files = tf.train.string_input_producer(["fixtures_1.csv"])
reader = tf.TextLineReader()
key, value = reader.read(fixtures_files)

record_defaults = [[1], [1], [1]]
col1, col2, col3 = tf.decode_csv(value, record_defaults=record_defaults)
features = tf.stack([[col1, col2]])

# prepare nn model params
n_nodes_hl1 = 300
# n_nodes_hl2 = 200
# n_nodes_hl3 = 300
n_nodes_otput = 1

x = tf.placeholder(tf.float32, [1, 2])
y = tf.placeholder(tf.float32)

# define nn model computational graph
def model_nn(data):

	hl_1 = {
		# 'weights': tf.Variable(tf.random_normal([n_nodes_hl1, 2])),
		'weights': tf.Variable(tf.random_uniform([2, n_nodes_hl1], -1, 1)),
		'biases': tf.Variable(tf.random_normal([n_nodes_hl1]))
	}

	# hl_2 = {
	# 	# 'weights': tf.Variable(tf.random_normal([n_nodes_hl2, n_nodes_hl1])),
	# 	'weights': tf.Variable(tf.random_uniform([n_nodes_hl1, n_nodes_hl2], -1, 1)),
	# 	'biases': tf.Variable(tf.random_normal([n_nodes_hl2]))
	# }

	# hl_3 = {
	# 	# 'weights': tf.Variable(tf.random_normal([n_nodes_hl3, n_nodes_hl2])),
	# 	'weights': tf.Variable(tf.random_uniform([n_nodes_hl2, n_nodes_hl3], -1, 1)),
	# 	'biases': tf.Variable(tf.random_normal([n_nodes_hl3]))
	# }

	ol = {
		# 'weights': tf.Variable(tf.random_normal([n_nodes_otput, n_nodes_hl3])),
		'weights': tf.Variable(tf.random_uniform([n_nodes_hl1, n_nodes_otput], -1, 1)),
		'biases': tf.Variable(tf.random_normal([n_nodes_otput]))
	}

	# hl_1_value = tf.add(tf.matmul(data, tf.transpose(hl_1['weights'])), hl_1['biases'])
	hl_1_value = tf.add(tf.matmul(data, hl_1['weights']), hl_1['biases'])
	hl_1_value = tf.nn.relu(hl_1_value)

	# hl_2_value = tf.add(tf.matmul(hl_1_value, tf.transpose(hl_2['weights'])), hl_2['biases'])
	# hl_2_value = tf.add(tf.matmul(hl_1_value, hl_2['weights']), hl_2['biases'])
	# hl_2_value = tf.nn.relu(hl_2_value)

	# # hl_3_value = tf.add(tf.matmul(hl_2_value, tf.transpose(hl_3['weights'])), hl_3['biases'])
	# hl_3_value = tf.add(tf.matmul(hl_2_value, hl_3['weights']), hl_3['biases'])
	# hl_3_value = tf.nn.relu(hl_3_value)

	# ol_value = tf.add(tf.matmul(hl_3_value, tf.transpose(ol['weights'])), ol['biases'])
	ol_value = tf.add(tf.matmul(hl_1_value, ol['weights']), ol['biases'])

	return ol_value

# define a way the nn trains
epochs_count = 20
iterations_count = 100000

def train_nn(x):
	prediction = model_nn(x)
	cost = tf.reduce_mean(tf.square(prediction - y))
	optimizer = tf.train.AdamOptimizer(0.0000005).minimize(cost)

	with tf.Session() as sess:
		# Start populating the filename queue.
		coord = tf.train.Coordinator()
		threads = tf.train.start_queue_runners(coord=coord)
		
		sess.run(tf.global_variables_initializer())

		for epoch in range(epochs_count):
			epoch_lost = 0
			
			for i in range(iterations_count):
			    input_data, label = sess.run([features, col3])

			    _, loss = sess.run([optimizer, cost], feed_dict={x:input_data, y:label})

			    if i % 1000 == 0:
			    	print 'Epoch', epoch + 1, 'Data set', i
			    	print input_data
			    	print sess.run(prediction, {x:input_data})
			    	# print 'Loss is:', loss

			    epoch_lost += loss

			print 'Epoch', epoch, 'is done'
			print 'Epoch lost is:', epoch_lost
			print '\n\n\n'

			sess.run(reader.reset())

		coord.request_stop()
  		coord.join(threads)
		
		print 'Done!'
		# print 'Prediction 1 is:', sess.run(prediction, {x:test_x1})
		# print 'Prediction 2 is:', sess.run(prediction, {x:test_x2})
		# print 'Prediction 3 is:', sess.run(prediction, {x:test_x3})
		# print 'Prediction 4 is:', sess.run(prediction, {x:test_x4})
		# print 'Loss is:', sess.run(cost, feed_dict={x:test_x, y:test_y})

train_nn(x)

