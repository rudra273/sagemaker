import logging
import numpy as np
import json
from sagemaker import get_execution_role
from sagemaker.predictor import Predictor
from sagemaker.session import Session
from sagemaker.base_serializers import NumpySerializer 

# Set logging level to debug to capture detailed logs
logging.basicConfig(level=logging.DEBUG)
endpoint = 'sagemaker-scikit-learn-2024-12-26-12-53-06-171'

# Example: Using an existing endpoint and setting up a predictor
predictor = Predictor(endpoint_name=endpoint, sagemaker_session=Session())

# Your data (example input data as a NumPy array)
sklearn_input = np.array([4.0, 8.0, 6.0, 3.0]).reshape(1, -1)

# Convert NumPy array to list (as JSON doesn't support NumPy arrays directly)
sklearn_input_list = sklearn_input.tolist()

# Set the serializer to JSON
predictor.serializer = NumpySerializer()

# Triggering prediction, logging will capture the request details
response = predictor.predict(sklearn_input_list)

# Log the response (for debugging and verification)
logging.debug("Prediction response: %s", response)

print(response) 