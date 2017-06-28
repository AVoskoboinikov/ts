import tensorflow as tf

x1 = tf.constant([[1, 2]])
# x1 = tf.Variable(tf.random_normal([1,2]))

x2 = tf.constant([
	[7,2], 
	])
# x2 = tf.Variable(tf.random_normal([3,2]))

b = tf.constant([[3,3,3]])
# b = tf.Variable(tf.random_normal([1,2]))

sess = tf.Session()
sess.run(tf.global_variables_initializer())

x12 = tf.matmul(x1, tf.transpose(x2))

print(sess.run(x12))
# print(sess.run(x1))
# print(sess.run(tf.shape(x1)))
# print(sess.run(tf.shape(x2)))