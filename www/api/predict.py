import tensorflow as tf
import os

def get_prediction(audusd, nzdusd):

	##############################################################
	# Restoring trained model
	##############################################################

	model_id_to_restore = '1504006754'

	path_to_model = os.path.join(
		os.path.dirname(os.path.abspath(__file__)),
	    '..',
		'models',
		model_id_to_restore
	)

	meta_file_path = os.path.join(
		path_to_model, 
		(model_id_to_restore + '.meta')
	)

	sess = tf.Session()

	saver = tf.train.import_meta_graph(meta_file_path)
	saver.restore(sess, tf.train.latest_checkpoint(path_to_model))

	graph = tf.get_default_graph()

	input_data = graph.get_tensor_by_name("input_data:0")
	final_output = graph.get_tensor_by_name("final_output:0")

	



	##############################################################
	# Converting audusd nzdusd to format required by input_data 
	# Must be matrix with shape 1 x 30 x 2
	##############################################################

	input_value = []
	data_length = 30

	for i in range(data_length):
		sample = [float(audusd[i]), float(nzdusd[i])]
		input_value.append(sample)

	input_value = [input_value]





	##############################################################
	# Making prediction
	##############################################################

	network_output = sess.run([final_output], feed_dict={input_data: input_value})

	return network_output[0][0]