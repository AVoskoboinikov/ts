import tensorflow as tf
import matplotlib.pyplot as plt
import os

# #################
# Reading test data
# #################

fixture_file = 'alpari/test1.csv'
fixture_data = []
fixture_size = 23

with open(fixture_file) as source:
	[fixture_data.append(row.strip().split(',')) for row in source]

def get_fixture_label_data(row_num):
	row_num = (row_num % len(fixture_data)) - 1

	return [fixture_data[row_num][0:fixture_size]], [[fixture_data[row_num][-1]]]






# ###########################################
# Setting path to model that will be restored
# ###########################################

model_id_to_restore = '1502223003'

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
update_lstm_c_state = graph.get_tensor_by_name("update_lstm_c_state:0")
update_lstm_h_state = graph.get_tensor_by_name("update_lstm_h_state:0")
final_output = graph.get_tensor_by_name("final_output:0")




# ######################
# Testing restored model
# ######################

test_data_lag = 110000
test_data_size = 4000

actual_output_collection = []
network_output_collection = []
x_axis = []

for i in range(test_data_size):
    input_value, output_value = get_fixture_label_data(test_data_lag + i + 1)

    _, _, network_output = sess.run(
        [update_lstm_c_state, update_lstm_h_state, final_output],
        feed_dict = {input_data: input_value}
    )
 
    actual_output_collection.append(float(output_value[0][0]))
    network_output_collection.append(network_output[0][0])
    x_axis.append(i)
 
plt.plot(
    x_axis, network_output_collection, 'r-', 
    x_axis, actual_output_collection, 'b-'
)
plt.show()