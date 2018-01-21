# gunicorn --workers=4 --bind 0.0.0.0:80 --worker-class=tornado main:__hug_wsgi__

# audUsd=1&audUsd=2&audUsd=3&audUsd=4&audUsd=5&audUsd=6&audUsd=7&audUsd=8&audUsd=9&audUsd=10&audUsd=11&audUsd=12&audUsd=13&audUsd=14&audUsd=15&audUsd=16&audUsd=17&audUsd=18&audUsd=19&audUsd=20&audUsd=21&audUsd=22&audUsd=23&audUsd=24&audUsd=25&audUsd=26&audUsd=27&audUsd=28&audUsd=29&audUsd=30&
# usdZar=1&usdZar=2&usdZar=3&usdZar=4&usdZar=5&usdZar=6&usdZar=7&usdZar=8&usdZar=9&usdZar=10&usdZar=11&usdZar=12&usdZar=13&usdZar=14&usdZar=15&usdZar=16&usdZar=17&usdZar=18&usdZar=19&usdZar=20&usdZar=21&usdZar=22&usdZar=23&usdZar=24&usdZar=25&usdZar=26&usdZar=27&usdZar=28&usdZar=29&usdZar=30&
# nzdUsd=1&nzdUsd=2&nzdUsd=3&nzdUsd=4&nzdUsd=5&nzdUsd=6&nzdUsd=7&nzdUsd=8&nzdUsd=9&nzdUsd=10&nzdUsd=11&nzdUsd=12&nzdUsd=13&nzdUsd=14&nzdUsd=15&nzdUsd=16&nzdUsd=17&nzdUsd=18&nzdUsd=19&nzdUsd=20&nzdUsd=21&nzdUsd=22&nzdUsd=23&nzdUsd=24&nzdUsd=25&nzdUsd=26&nzdUsd=27&nzdUsd=28&nzdUsd=29&nzdUsd=30&
# eurNzd=1&eurNzd=2&eurNzd=3&eurNzd=4&eurNzd=5&eurNzd=6&eurNzd=7&eurNzd=8&eurNzd=9&eurNzd=10&eurNzd=11&eurNzd=12&eurNzd=13&eurNzd=14&eurNzd=15&eurNzd=16&eurNzd=17&eurNzd=18&eurNzd=19&eurNzd=20&eurNzd=21&eurNzd=22&eurNzd=23&eurNzd=24&eurNzd=25&eurNzd=26&eurNzd=27&eurNzd=28&eurNzd=29&eurNzd=30&

import hug
# import logging
import numpy as np
import random

from advisers import adviserCorrelation

@hug.post('/predict')
# def predict(audUsd, usdZar, nzdUsd, eurNzd):
def predict(body):
	# logger = logging.getLogger(__name__)
	# logging.basicConfig()

	# logger.error(body['audusd'])
	# logger.error(body['usdzar'])
	# logger.error(body['nzdusd'])
	# logger.error(body['eurnzd'])
	# logger.error("\r\n\r\n\r\n")

	audUsdTicks = reversed([np.float32(i) for i in body['audusd']])
	audUsdTicks = np.reshape(audUsdTicks, (len(audUsdTicks)))

	usdZarTicks = reversed([np.float32(i) for i in body['usdzar']])
	usdZarTicks = np.reshape(usdZarTicks, (len(usdZarTicks)))

	nzdUsdTicks = reversed([np.float32(i) for i in body['nzdusd']])
	nzdUsdTicks = np.reshape(nzdUsdTicks, (len(nzdUsdTicks)))

	eurNzdTicks = reversed([np.float32(i) for i in body['eurnzd']])
	eurNzdTicks = np.reshape(eurNzdTicks, (len(eurNzdTicks)))

	result = adviserCorrelation(audUsdTicks, usdZarTicks, nzdUsdTicks, eurNzdTicks)
	
	if not result == 0:
		print("audUsdTicks")
		print(audUsdTicks)
		
		print("usdZarTicks")
		print(usdZarTicks)
		
		print("nzdUsdTicks")
		print(nzdUsdTicks)

		print("eurNzdTicks")
		print(eurNzdTicks)
	
	# result = random.randint(-1, 1)

	return result