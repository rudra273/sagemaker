import os
import numpy as np
import sagemaker
from sagemaker import get_execution_role
from sagemaker.sklearn.estimator import SKLearn
from sagemaker.serve import SchemaBuilder, ModelBuilder
from sagemaker.serve.mode.function_pointers import Mode
import mlflow
from mlflow import MlflowClient

def get_latest_model_source(model_name):
    """
    Retrieve the latest model source from MLflow registry
    
    Args:
        model_name (str): Name of the registered model
    
    Returns:
        str: Source path of the latest model version
    """
    mlflow.set_tracking_uri(os.getenv('MLFLOW_TRACKING_URI'))
    client = MlflowClient()
    
    # Get the latest version of the registered model
    registered_model = client.get_registered_model(name=model_name)
    return registered_model.latest_versions[0].source

def create_sagemaker_model(
    source_path, 
    role_arn, 
    sample_input, 
    sample_output
):
    """
    Create and deploy a SageMaker model
    
    Args:
        source_path (str): MLflow model source path
        role_arn (str): AWS IAM role ARN
        sample_input (np.ndarray): Sample input for schema building
        sample_output (int): Sample output for schema building
    
    Returns:
        sagemaker.predictor.Predictor: Deployed model predictor
    """
    # Create schema builder
    schema_builder = SchemaBuilder(
        sample_input=sample_input,
        sample_output=sample_output,
    )
    
    # Create model builder
    model_builder = ModelBuilder(
        mode=Mode.SAGEMAKER_ENDPOINT,
        schema_builder=schema_builder,
        role_arn=role_arn,
        model_metadata={"MLFLOW_MODEL_PATH": source_path},
    )
    
    # Build and deploy the model
    built_model = model_builder.build()
    predictor = built_model.deploy(
        initial_instance_count=1, 
        instance_type="ml.m5.large"
    )
    
    return predictor

def main():
    # Get SageMaker session and role
    sagemaker_session = sagemaker.Session()
    role = get_execution_role()
    
    # Sample input for model schema (replace with your actual sample)
    sklearn_input = np.array([1.0, 2.0, 3.0, 4.0]).reshape(1, -1)
    sklearn_output = 1
    
    # Get the latest model source from MLflow
    source_path = get_latest_model_source("sm-job-experiment-model")
    
    # Deploy the model
    predictor = create_sagemaker_model(
        source_path, 
        role, 
        sklearn_input, 
        sklearn_output
    )
    
    # Optional: Test the predictor
    prediction = predictor.predict(sklearn_input)
    print("Model prediction:", prediction)

if __name__ == '__main__':
    main()

    