import os
import sagemaker
from sagemaker.workflow.pipeline import Pipeline
from sagemaker.workflow.steps import ProcessingStep, TrainingStep
from sagemaker.workflow.model_step import ModelStep
from sagemaker.processing import Processor, ProcessingInput, ProcessingOutput
from sagemaker.sklearn.processing import SKLearnProcessor
from sagemaker.sklearn.estimator import SKLearn
from sagemaker.model import Model
from sagemaker.workflow.pipeline_context import PipelineSession

def create_sagemaker_pipeline(
    role, 
    sagemaker_session, 
    input_data_uri, 
    processing_instance_type='ml.c4.xlarge',
    training_instance_type='ml.c4.xlarge' 
):
    """
    Create a SageMaker Pipeline for MLflow model training and deployment
    
    Args:
        role (str): AWS IAM role ARN
        sagemaker_session (sagemaker.session.Session): SageMaker session
        input_data_uri (str): S3 URI for input data
        processing_instance_type (str, optional): Instance type for preprocessing
        training_instance_type (str, optional): Instance type for training
    
    Returns:
        sagemaker.workflow.pipeline.Pipeline: Configured SageMaker Pipeline
    """
    # Create a pipeline session
    pipeline_session = PipelineSession()
    
    # Preprocessing Step
    sklearn_processor = SKLearnProcessor(
        framework_version='1.0-1',
        role=role,
        instance_type=processing_instance_type,
        instance_count=1,
        sagemaker_session=pipeline_session
    )
    
    processing_step = ProcessingStep(
        name='PreprocessIrisData',
        processor=sklearn_processor,
        inputs=[
            ProcessingInput(
                source=input_data_uri, 
                destination='/opt/ml/processing/input'
            )
        ],
        outputs=[
            ProcessingOutput(
                source='/opt/ml/processing/output',
                destination=f'{input_data_uri}/processed'
            )
        ],
        code='src/preprocessing.py'
    )
    
    # Training Step
    sklearn_estimator = SKLearn(
        entry_point='src/train.py',
        role=role,
        instance_type=training_instance_type,
        framework_version='1.0-1',
        hyperparameters={
            'max_leaf_nodes': 30
        },
        sagemaker_session=pipeline_session
    )
    
    training_step = TrainingStep(
        name='TrainIrisModel',
        estimator=sklearn_estimator,
        inputs={
            'train': processing_step.properties.ProcessingOutputConfig.Outputs['ProcessingOutput'].S3Output.S3Uri
        }
    )
    
    # Model Registration and Deployment Step
    model = Model(
        image_uri=sklearn_estimator.training_image_uri(),
        model_data=training_step.properties.ModelArtifacts.S3ModelArtifacts,
        role=role,
        sagemaker_session=pipeline_session
    )
    
    model_step = ModelStep(
        name='RegisterAndDeployModel',
        step_args=model.register(
            content_types=['text/csv'],
            response_types=['text/csv'],
            inference_instances=['ml.m5.large'],
            transform_instances=['ml.m5.large'],
            model_package_group_name='IrisModelPackageGroup'
        )
    )
    
    # Create Pipeline
    pipeline = Pipeline(
        name='iris-mlflow-pipeline',
        steps=[processing_step, training_step, model_step],
        sagemaker_session=pipeline_session
    )
    
    return pipeline

def main():
    # Initialize SageMaker session and get role
    sagemaker_session = sagemaker.Session()
    # role = sagemaker.get_execution_role()
    role = 'arn:aws:iam::750573229682:role/sagemaker_execution_role' 
    
    # S3 URI for input data (replace with your actual S3 bucket)
    input_data_uri = 's3://mlflow-sagemaker-us-east-1-750573229682/iris-dataset'
    
    # Create and submit pipeline
    pipeline = create_sagemaker_pipeline(
        role, 
        sagemaker_session, 
        input_data_uri
    )
    
    # Upsert pipeline
    pipeline.upsert(role_arn=role)
    
    print("Pipeline created successfully!")

if __name__ == '__main__':
    main()

