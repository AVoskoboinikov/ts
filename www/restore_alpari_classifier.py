import tensorflow as tf
import matplotlib.pyplot as plt
import os
import numpy as np
from random import shuffle

# #################
# Reading test data
# #################

fixture_file = 'alpari/AUDUSD-NZDUSD-1M.csv'
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

def get_fixture_label_data(row_num):
    row_num = (row_num % len(fixture_data)) - 1
    return fixture_data[row_num]['sample'], fixture_data[row_num]['label']






# ###########################################
# Setting path to model that will be restored
# ###########################################

model_id_to_restore = '1504123313'

path_to_model = os.path.join(
	os.path.dirname(os.path.abspath(__file__)), 
	'models',
	model_id_to_restore
	)

meta_file_path = os.path.join(
	path_to_model, 
	(model_id_to_restore + '.meta')
	)




# ####################################################
# Restoring graph and required plaveholders/operations
# ####################################################

sess = tf.Session()

saver = tf.train.import_meta_graph(meta_file_path)
saver.restore(sess, tf.train.latest_checkpoint(path_to_model))

graph = tf.get_default_graph()

input_data = graph.get_tensor_by_name("input_data:0")
final_output = graph.get_tensor_by_name("final_output:0")

correct_output = tf.placeholder(tf.float32, [1, classes_size])
correct_prediction = tf.equal(tf.argmax(correct_output, 1), tf.argmax(final_output, 1))




# ######################
# Testing restored model
# ######################

train_iterations_count = len(fixture_data) - 40000
test_iterations_count = 40000

network_results = []

first_class_correct = 0
first_class_wrong = 0
second_class_correct = 0
second_class_wrong = 0

ids = list(range(test_iterations_count))
shuffle(ids)

for i in range(test_iterations_count):
    input_value, output_value = get_fixture_label_data(train_iterations_count + ids[i])

    network_output, is_correct = sess.run(
        [final_output, correct_prediction],
        feed_dict = {input_data: input_value, correct_output: output_value}
    )

    if i % 1000 == 0:
        print("Done:", i)
        print(output_value)
        print(network_output)
        print("\n\n\n")

    network_results.append(is_correct[0])

    if is_correct[0] == True:
        
        # [1, 0]
        if output_value[0][0] == 1.0:
            first_class_correct += 1

        # [0, 1]
        if output_value[0][1] == 1.0:
            second_class_correct += 1

    if is_correct[0] == False:
        
        # [1, 0]
        if output_value[0][0] == 1.0:
            first_class_wrong += 1

        # [0, 1]
        if output_value[0][1] == 1.0:
            second_class_wrong += 1




test_accuracy = sess.run(tf.reduce_mean(tf.cast(network_results, tf.float32)))

print("####################", "\n")
print("Test accuracy is:", test_accuracy)
print("Amount of correct predictions that trend WILL NOT have difference for 10 points:", first_class_correct)
print("\n")
print("Amount of correct predictions that trend WILL have difference for 10 points:", second_class_correct)
print("\n")
print("Amount of wrong predictions that trend WILL have difference for 10 points:", first_class_wrong)
print("\n")
print("Amount of wrong predictions that trend WILL NOT have difference for 10 points:", second_class_wrong)
print("####################", "\n\n\n")