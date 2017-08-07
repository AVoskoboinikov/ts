from numpy import array, sin, cos, pi
from random import random
from random import randint
import tensorflow as tf
from tensorflow.python.ops import rnn, rnn_cell
import matplotlib.pyplot as plt
import time

fixture_file = 'alpari/test1.csv'
fixture_data = []
fixture_size = 23

with open(fixture_file) as source:
    [fixture_data.append(row.strip().split(',')) for row in source]

# need a function to produce input data here 
def get_fixture_label_data(row_num):
    row_num = (row_num % len(fixture_data)) - 1
    
    return [fixture_data[row_num][0:fixture_size]], [[fixture_data[row_num][-1]]]





# ###############################################
# Describe LSTM model and tensorflow update graph
# ###############################################

# global init params
lstm_size = 50
input_size = fixture_size

# placeholder for input data
input_layer = tf.placeholder(tf.float32, [1, input_size])

# the LSTM Cell initialization
lstm_layer = rnn_cell.LSTMCell(lstm_size)

# default state is zero
# state has two variables because LSTM actualy has two states - cell state and hidden state
lstm_state_c = tf.Variable(tf.zeros([1, lstm_size]))
lstm_state_h = tf.Variable(tf.zeros([1, lstm_size]))

# now we need express it as one value
lstm_state = (lstm_state_c, lstm_state_h)

# passing input data to LSTM cell and get prediction and changed state
lstm_output, lstm_state_output = lstm_layer(input_layer, lstm_state, scope='LSTM1')

# we need to update both cell and hidden states
update_lstm_c_state = lstm_state_c.assign(lstm_state_output[0])
update_lstm_h_state = lstm_state_h.assign(lstm_state_output[1])

# in case we need to reset states to zero we need run this updates
reset_lstm_c_state = lstm_state_c.assign(tf.zeros([1, lstm_size]))
reset_lstm_h_state = lstm_state_h.assign(tf.zeros([1, lstm_size]))

# init output layer - weights and biases
output_W = tf.Variable(tf.random_uniform([lstm_size, 1], -1, 1))
output_b = tf.Variable(tf.random_uniform([1], -1, 1))

# compute final prediction for step
final_output = tf.matmul(lstm_output, output_W) + output_b

# placeholder for correct output
correct_output = tf.placeholder(tf.float32, [1, 1])

# compute error for step
error = tf.reduce_mean(tf.square(final_output - correct_output))

# optimization for error
optimize = tf.train.AdamOptimizer(0.0000001).minimize(error)





# ########
# Training
# ########

train_iterations_count = 110000
train_epoch_count = 1

# initializr tensorflow session
sess = tf.Session()

# initialize variables
sess.run(tf.global_variables_initializer())

for epoch in range(train_epoch_count):
    actual_output_collection = []
    network_output_collection = []
    x_axis = []

    # reset both cell and hidden states, so the test data will not be influenced with trained one
    sess.run(reset_lstm_c_state)
    sess.run(reset_lstm_h_state)
    
    for i in range(train_iterations_count):
        # here should be function to retreive train data
        input_value, output_value = get_fixture_label_data((i+1))

        # print(input_value, output_value)
        _, _, _, network_output, error_value = sess.run(
            [update_lstm_c_state, update_lstm_h_state, optimize, final_output,  error],
            feed_dict = {input_layer: input_value, correct_output: output_value}
        )

        # in case we need reset state we can run this
        # this will reset both cell and hidden states per each 1100 iteration
        # if (i+1) % len(fixture_data) == 0:
            # sess.run([reset_lstm_c_state, reset_lstm_h_state])

        # print current iteration number and error value
        # print('Epoch:',epoch, 'Iteration:', (i+1), 'Error:', error_value, "\n\n")
        
        # save all outputs so we can plot them later on graph
        actual_output_collection.append(output_value[0][0])
        network_output_collection.append(network_output[0][0])

        # this will be x-axis in future graph
        x_axis.append(i)

# # add predicted outputs with red color and real otputs with blue color
# plt.plot(
#     x_axis, network_output_collection, 'r-', 
#     x_axis, actual_output_collection, 'b-'
# )

# # shows graph
# plt.show()






# #######
# Testing
# #######

test_iterations_count = 4000

# this will move window with input data to the right, so the testing data will not follow the trained data
# for i in range(200):
    # here should be function to retreive test data
    # get_fixture_label_data()
 
# # reset both cell and hidden states, so the test data will not be influenced with trained one
# sess.run(reset_lstm_c_state)
# sess.run(reset_lstm_h_state)

actual_output_collection = []
network_output_collection = []
x_axis = [] 
 
for i in range(test_iterations_count):
    # here should be function to retreive test data
    input_value, output_value = get_fixture_label_data(train_iterations_count + i + 1)

    _, _, network_output = sess.run(
        [update_lstm_c_state, update_lstm_h_state, final_output],
        feed_dict = {input_layer: input_value, correct_output: output_value}
    )
 
    actual_output_collection.append(float(output_value[0][0]))
    network_output_collection.append(network_output[0][0])
    x_axis.append(i)
 
plt.plot(
    x_axis, network_output_collection, 'r-', 
    x_axis, actual_output_collection, 'b-'
)
# plt.show()

# save plot to file
id = str(int(time.time()))
plotFileName = id + '.png'
plt.savefig('plots/' + plotFileName)