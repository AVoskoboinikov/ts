import tensorflow as tf

# prepare for fixture reading
fixtures_files = tf.train.string_input_producer(["fixtures_1.csv", "fixtures_2.csv", "fixtures_3.csv"])
reader = tf.TextLineReader()
key, value = reader.read(fixtures_files)

record_defaults = [[1], [1], [1]]
col1, col2, col3 = tf.decode_csv(value, record_defaults=record_defaults)
features = tf.stack([col1, col2])

# prepare nn model params
n_nodes_hl1 = 300
n_nodes_hl2 = 200
n_nodes_hl3 = 300
n_nodes_otput = 1

x = tf.placeholder(tf.float32, [1, 2])
y = tf.placeholder(tf.float32)

# define nn model computational graph
def model_nn(data):

	hl_1 = {
		'weights': tf.Variable(tf.random_normal([n_nodes_hl1, 2])),
		'biases': tf.Variable(tf.random_normal([n_nodes_hl1]))
	}

	hl_2 = {
		'weights': tf.Variable(tf.random_normal([n_nodes_hl2, n_nodes_hl1])),
		'biases': tf.Variable(tf.random_normal([n_nodes_hl2]))
	}

	hl_3 = {
		'weights': tf.Variable(tf.random_normal([n_nodes_hl3, n_nodes_hl2])),
		'biases': tf.Variable(tf.random_normal([n_nodes_hl3]))
	}

	ol = {
		'weights': tf.Variable(tf.random_normal([n_nodes_otput, n_nodes_hl3])),
		'biases': tf.Variable(tf.random_normal([n_nodes_otput]))
	}

	hl_1_value = tf.add(tf.matmul(data, tf.transpose(hl_1['weights'])), hl_1['biases'])
	hl_1_value = tf.nn.relu(hl_1_value)

	hl_2_value = tf.add(tf.matmul(hl_1_value, tf.transpose(hl_2['weights'])), hl_2['biases'])
	hl_2_value = tf.nn.relu(hl_2_value)

	hl_3_value = tf.add(tf.matmul(hl_2_value, tf.transpose(hl_3['weights'])), hl_3['biases'])
	hl_3_value = tf.nn.relu(hl_3_value)

	ol_value = tf.add(tf.matmul(hl_3_value, tf.transpose(ol['weights'])), ol['biases'])

	return ol_value

# define a way the nn trains
def train_nn(x):
	prediction = model_nn(x)
	cost = tf.reduce_sum(tf.square(prediction - y))
	optimizer = tf.train.AdamOptimizer(0.002).minimize(cost)

	with tf.Session() as sess:
		# Start populating the filename queue.
		coord = tf.train.Coordinator()
		threads = tf.train.start_queue_runners(coord=coord)
		
		sess.run(tf.global_variables_initializer())

		for i in range(50):
		    input_data, label = sess.run([features, col3])
		    input_data = sess.run(tf.reshape(input_data, [1, 2]))

		    sess.run([optimizer, cost], feed_dict={x:input_data, y:label})

		    print 'Optimized for input set', i

		accuracy = sess.run(cost, {x:[[5, 3]], y:8})
		
		print 'Done!'
		print 'Accuracy is: ', accuracy

		x1 = sess.run(tf.constant([[5, 3]]))
		print 'Prediction is:', sess.run(prediction, feed_dict={x:x1})

train_nn(x)

