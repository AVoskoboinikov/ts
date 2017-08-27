import tensorflow as tf
import os

w1 = tf.Variable(tf.random_normal(shape=[2]), name='w1')
w2 = tf.Variable(tf.random_normal(shape=[5]), name='w2')
saver = tf.train.Saver([w1,w2])
sess = tf.Session()
sess.run(tf.global_variables_initializer())
name = os.path.dirname(os.path.abspath(__file__)) + "/" + 'my_test_model'
saver.save(sess, name, global_step=1000)