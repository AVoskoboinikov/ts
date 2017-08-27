import tensorflow as tf

x1 = tf.constant([[1], [2]])
# x2 = tf.constant([3, 3, 3])
# final_output = tf.constant([ 0.000261774148, -0.000264855444])
# correct_output = tf.constant([0, 1])

# error = tf.reduce_mean(tf.nn.sparse_softmax_cross_entropy_with_logits(logits=final_output, labels=correct_output))
# error = tf.reduce_mean(( (correct_output * tf.log(final_output)) + ((1 - correct_output) * tf.log(1.0 - final_output)) ) * -1)
# error = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=final_output, labels=correct_output))

sess = tf.Session()
sess.run(tf.global_variables_initializer())

# final_output_v, correct_output_v = sess.run([final_output, correct_output])
# ev = sess.run([error], feed_dict = {final_output: final_output_v, correct_output: correct_output_v})
ev = sess.run(tf.reshape(x1, [1,2]))
print(ev)