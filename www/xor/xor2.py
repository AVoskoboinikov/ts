import tensorflow as tf
from tensorflow.python.ops import rnn, rnn_cell
from shutil import copyfile
import matplotlib.pyplot as plt
import time
import os
import numpy as np

fixture_data = [
    {'sample': [[1, 0]], 'label': [[0, 1]]},
    {'sample': [[0, 0]], 'label': [[1, 0]]},
    {'sample': [[0, 1]], 'label': [[0, 1]]},
    {'sample': [[1, 1]], 'label': [[1, 0]]},
]

fixture_size = 2
fixture_elems = 2
label_classes = 2

def get_fixture_label_data(row_num):
    row_num = (row_num % len(fixture_data)) - 1
    return fixture_data[row_num]['sample'], fixture_data[row_num]['label']

# ###############################################
# Describe LSTM model and tensorflow update graph
# ###############################################

input_data = tf.placeholder(tf.float32, [1, 2])

output_W1 = tf.Variable(tf.random_uniform([2, 2], -1, 1))
output_b1 = tf.Variable(tf.zeros([2]))

# init second perceptron layer - weights and biases
output_W2 = tf.Variable(tf.random_uniform([2, 2], -1, 1))
output_b2 = tf.Variable(tf.zeros([2]))

# compute output for rirst layer
output1 = tf.nn.relu(tf.add(tf.matmul(input_data, output_W1), output_b1))

# # compute final prediction for step
final_output = tf.add(tf.matmul(output1, output_W2), output_b2)

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

train_iterations_count = 10000
train_epoch_count = 10

# initializr tensorflow session
sess = tf.Session()

# initialize variables
sess.run(tf.global_variables_initializer())

for epoch in range(train_epoch_count):
    
    for i in range(train_iterations_count):
        input_value, output_value = get_fixture_label_data((i+1))

        network_output, error_v, is_correct, _ = sess.run(
            [final_output, error, correct_prediction, optimize],
            feed_dict = {input_data: input_value, correct_output: output_value}
        )

        # print current iteration number and error value
        print('Epoch:', epoch, 'Iteration:', (i+1))
        print('Input:', input_value)
        print('Error:', error_v)
        print('Correct:', is_correct)
        print('Real:', output_value, 'Predicted:', network_output, "\n\n")
