import tensorflow as tf
import csv
from tensorflow.python.ops import rnn, rnn_cell

x1 = tf.Variable(tf.random_uniform([3, 10, 1], -1, 1))
x2 = tf.Variable(tf.random_uniform([10, 1], -1, 1))

# def calc(data):
# 	data = tf.transpose(data, [1,0,2])
# 	data = tf.reshape(data, [-1, 1])
# 	data = tf.split(data, 10, 0)

# 	# data = tf.reshape(data, (-1, 10))
# 	# data = tf.split(data, 3, 0)

# 	lstm_cell = rnn_cell.LSTMCell(10, state_is_tuple=True, activation=tf.nn.relu)
# 	outputs, _ = rnn.static_rnn(lstm_cell, data, dtype=tf.float32)

# 	return outputs[-1]

# def run(x):
# 	o1 = calc(x)

# 	with tf.Session() as sess:
# 		sess.run(tf.global_variables_initializer())	

# 		o1v = sess.run(o1, feed_dict={x1:sess.run(x1)})

# 		# print sess.run(x1)
# 		print
# 		print o1v
# 		# print
# 		# print tf.shape(o1v)


# run(x1)

with tf.Session() as sess:
		sess.run(tf.global_variables_initializer())	
		
		x1s = x1
		x1s = tf.transpose(x1, [1,0,2])
		x1s = tf.reshape(x1s, [-1, 1])
		x1s = tf.split(x1s, 10, 0)

		print sess.run(x1)
		print
		print sess.run(x1s)
		print sess.run(tf.shape(x1s))

		print "\n\n\n"

		x2s = tf.split(x2, 10, 0)
		print sess.run(x2)
		print
		print sess.run(x2s)
		print sess.run(tf.shape(x2s))