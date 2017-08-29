import tensorflow as tf
from tensorflow.python.ops import rnn, rnn_cell
from shutil import copyfile
import time
import os
import numpy as np

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# id for current model
current_run_id = str(int(time.time()))

fixture_file = 'alpari/AUDUSD-NZDUSD-1M-last-year.csv'
fixture_data = []
fixture_size = 30
fixture_elems = 2
classes_size = 2

with open(fixture_file) as source:
    for row in source:
        row = row.strip().split(',')
        row = [float(item) for item in row]
        labels = [row[-classes_size:]]
        samples = [np.reshape(row[:-classes_size], [fixture_size, fixture_elems])]
        
        fixture_data.append({'sample': samples, 'label': labels})

# need a function to produce input data here 
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

def last_relevant_no_batches(output):
    return [output[-1][-1]]

def logResults(line):
    logFile = 'logs/alpari_classifier.log'
    file = open(logFile, 'a')
    file.write(line)


# ###############################################
# Describe LSTM model and tensorflow update graph
# ###############################################

# global init params
lstm_size = classes_size

# placeholder for input data
input_data = tf.placeholder(tf.float32, [None, fixture_size, fixture_elems], name="input_data")

# the LSTM Cell initialization
lstm_cell = rnn_cell.LSTMCell(lstm_size)

# passing input data to LSTM cell and get prediction and changed state
lstm_output, _ = rnn.dynamic_rnn(lstm_cell, input_data, dtype=tf.float32, sequence_length=[fixture_size])
last_relevant_output = last_relevant_no_batches(lstm_output)

# init first perceptron layer - weights and biases
output_W1 = tf.Variable(tf.random_uniform([lstm_size, classes_size], -1, 1), name="output_W1")
output_b1 = tf.Variable(tf.random_uniform([classes_size], -1, 1), name="output_b1")

# compute output for first layer
final_output = tf.add(tf.matmul(last_relevant_output, output_W1), output_b1, name="final_output")

# placeholder for correct output
correct_output = tf.placeholder(tf.float32, [1, classes_size])
correct_prediction = tf.equal(tf.argmax(correct_output, 1), tf.argmax(final_output, 1))

# compute error for step (classification error)
error = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=final_output, labels=correct_output))

# optimization for error
# optimize = tf.train.AdamOptimizer(0.00000001).minimize(error)
optimize = tf.train.AdamOptimizer(0.00005).minimize(error)





# ########
# Training
# ########

train_iterations_count = len(fixture_data) - 100000
train_epoch_count = 1

# initializr tensorflow session
sess = tf.Session()

# initialize variables
sess.run(tf.global_variables_initializer())

# initialize save object to save the model
saver = tf.train.Saver()

for epoch in range(train_epoch_count):
    epoch_results = []

    for i in range(train_iterations_count):
        # here should be function to retreive train data
        input_value, output_value = get_fixture_label_data((i+1))

        network_output, error_value, is_correct, _ = sess.run(
            [final_output, error, correct_prediction, optimize],
            feed_dict = {input_data: input_value, correct_output: output_value}
        )

        epoch_results.append(is_correct[0])

        if (i+1) % 1000 == 0:
            # print current iteration number and error value
            print('Epoch:', epoch, 'Iteration:', (i+1))
            # print('Error:', error_value)
            print('Current accuracy:', sess.run(tf.reduce_mean(tf.cast(epoch_results, tf.float32))))
            # print('Real:', output_value, 'Predicted:', network_output, "\n\n")

        # if error_value < 0.1:
        #     print('Epoch:', epoch, 'Iteration:', (i+1))
        #     print('Error:', error_value)
        #     print('Correct:', is_correct)
        #     print('Real:', output_value, 'Predicted:', network_output, "\n\n")
        
        # save all outputs so we can calculate accuracy
        

    train_accuracy = sess.run(tf.reduce_mean(tf.cast(epoch_results, tf.float32)))

    print("####################", "\n")
    print("Train accuracy is:", train_accuracy)
    print("####################", "\n\n\n")




# ############
# Saving model
# ############


# creating a directory to save model
model_dir = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'models',
    current_run_id
    )

if not os.path.exists(model_dir):
    os.makedirs(model_dir)

# saving current model to file
saver.save(sess, os.path.join(model_dir, current_run_id))

# copy this file to dir with current_run_id as name
copyfile(os.path.abspath(__file__), os.path.join(model_dir, current_run_id + '.py'))







# #######
# Testing
# #######

test_iterations_count = 100000

epoch_results = []

for i in range(test_iterations_count):
    # here should be function to retreive test data
    input_value, output_value = get_fixture_label_data(train_iterations_count + i)

    network_output, is_correct = sess.run(
        [final_output, correct_prediction],
        feed_dict = {input_data: input_value, correct_output: output_value}
    )

    if is_correct == True:
        print("Prediction is:", network_output)

    epoch_results.append(is_correct[0])
    
test_accuracy = sess.run(tf.reduce_mean(tf.cast(epoch_results, tf.float32)))

print("####################", "\n")
print("Test accuracy is:", test_accuracy)
print("####################", "\n\n\n")

result = 'Model: {0:10} Train accuracy: {1:5} Test accuracy: {2:5} \n\r'.format(current_run_id, train_accuracy, test_accuracy)
logResults(result)


# # for i in {1..20}; do python -u lstm_gen.py; done