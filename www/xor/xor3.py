import tensorflow as tf
from tensorflow.python.ops import rnn, rnn_cell
from shutil import copyfile
import matplotlib.pyplot as plt
import time
import os
import numpy as np

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

fixture_data = [
    {'sample': [[[0, 0], [0, 1]]], 'label': [[0, 1]]},
    {'sample': [[[0, 1], [0, 1]]], 'label': [[1, 0]]},
    {'sample': [[[0, 1], [0, 0]]], 'label': [[0, 1]]},
    {'sample': [[[0, 0], [0, 0]]], 'label': [[1, 0]]},
]

def get_fixture_label_data(row_num):
    row_num = (row_num % len(fixture_data)) - 1
    return fixture_data[row_num]['sample'], fixture_data[row_num]['label']

def last_relevant(output, length):
    batch_size = tf.shape(output)[0]
    max_length = tf.shape(output)[1]
    out_size = int(output.get_shape()[2])
    index = tf.range(0, batch_size) * max_length + (length - 1)
    flat = tf.reshape(output, [-1, out_size])
    relevant = tf.gather(flat, index)
  
    return relevant





input_data = tf.placeholder(tf.float32, [None, 2, 2])

lstm_cell = rnn_cell.LSTMCell(2)
outputs, _ = rnn.dynamic_rnn(lstm_cell, input_data, dtype=tf.float32, sequence_length=[2])

output_W1 = tf.Variable(tf.random_uniform([2, 2], -1, 1))
output_b1 = tf.Variable(tf.random_uniform([2], 0.1, 0.2))

# output_W2 = tf.Variable(tf.zeros([2, 2]))
# output_b2 = tf.Variable(tf.zeros([2]))

# output_W3 = tf.Variable(tf.random_uniform([2, 1], -1, 1))
# output_b3 = tf.Variable(tf.zeros([1]))

# compute output for rirst layer
output1 = tf.add(tf.matmul(last_relevant(outputs, 2), output_W1), output_b1)

# # compute final prediction for step
# output2 = tf.add(tf.matmul(output1, output_W2), output_b2)

# output3 = tf.add(tf.matmul(output2, output_W3), output_b3)

final_output = output1
# final_output = tf.add(tf.matmul(output2, output_W3), output_b3)

# placeholder for correct output
correct_output = tf.placeholder(tf.float32, [1, 2])

correct_prediction = tf.equal(tf.argmax(correct_output, 1), tf.argmax(final_output, 1))

# compute error for step (classification error)
error = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=final_output, labels=correct_output))
# error = tf.reduce_mean(tf.square(final_output - correct_output))

# optimization for error
optimize = tf.train.AdamOptimizer().minimize(error)





# ########
# Training
# ########

train_iterations_count = 3000
train_epoch_count = 3

# initializr tensorflow session
sess = tf.Session()

# initialize variables
sess.run(tf.global_variables_initializer())

for epoch in range(train_epoch_count):
    result_a = []
    
    for i in range(train_iterations_count):
        input_value, output_value = get_fixture_label_data((i))

        network_output, error_v, is_correct, _ = sess.run(
            [final_output, error, correct_prediction, optimize],
            feed_dict = {input_data: input_value, correct_output: output_value}
        )

        # network_output = sess.run(
        #     [final_output],
        #     feed_dict = {input_data: input_value, correct_output: output_value}
        # )

        result_a.append(is_correct[0])

        # print current iteration number and error value
        print('Epoch:', epoch, 'Iteration:', (i+1))
        print('Input:', input_value)
        print('Error:', error_v)
        print('Correct:', is_correct)
        print('Real:', output_value, 'Predicted:', network_output, "\n\n")

accuracy = tf.reduce_mean(tf.cast(result_a, tf.float32))

print("####################", "\n")
print("Accuracy is:", sess.run(accuracy))
print("####################", "\n\n\n")