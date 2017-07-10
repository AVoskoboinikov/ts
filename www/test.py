import tensorflow as tf

x1 = tf.constant([[1],[2]])
data = tf.split(x1, 2, 0)
# x2 = tf.constant([[2, 2, 2]])

# w1 = tf.Variable(tf.random_uniform([3], -1, 1))
# b1 = tf.Variable(tf.random_uniform([3], -1, 1))

sess = tf.Session()
sess.run(tf.global_variables_initializer())

print(sess.run(x1))
print(sess.run(tf.shape(x1)))
print(sess.run(data))
# print
# print(sess.run(x2))
# print(sess.run(tf.shape(x2)))
# print
# print(sess.run(x2*x1))
# print(sess.run(tf.matmul(x2,x1)))
# print(sess.run(w1))
# print(sess.run(b1))
# print 

# y = x1 * w1
# print(sess.run(y))
# print(sess.run(y + b1))