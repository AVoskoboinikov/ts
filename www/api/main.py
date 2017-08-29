import hug
import logging
# import simplejson
from predict import get_prediction
# from decimal import Decimal

@hug.get('/predict')
def predict(audusd, nzdusd):
	prediction = get_prediction(audusd, nzdusd)
	result = {'fisrst_class': repr(prediction[0]), 'second_class': repr(prediction[1])}

	# simplejson.dumps(result)
	logging.error(prediction[0])
	logging.error(prediction[1])

	return result