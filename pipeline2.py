import os
import sagemaker
from sagemaker.workflow.pipeline import Pipeline
from sagemaker.workflow.steps import ProcessingStep, TrainingStep
from sagemaker.processing import ProcessingInput, ProcessingOutput
from sagemaker.workflow.pipeline_context import PipelineSession
from sagemaker.processing import ScriptProcessor
from sagemaker.estimator import Estimator


def create_sagemaker_pipeline(
    role, 
    sagemaker_session, 
    input_data_uri, 
    outout_data_uri,
    processing_instance_type='ml.t3.medium',
    training_instance_type='ml.c4.xlarge'
):
    """
    Create a SageMaker Pipeline using existing preprocessing and training scripts
    """
    # Create a pipeline session
    pipeline_session = PipelineSession()

    image_uri = "750573229682.dkr.ecr.us-east-1.amazonaws.com/custom-sagemaker-image:latest"

    script_processor = ScriptProcessor(
    
    image_uri=image_uri,
    command=["python3"],  # Command to run your script inside the container
    role=role,
    instance_type=processing_instance_type,
    instance_count=1,
    sagemaker_session=pipeline_session
    )


    processing_step = ProcessingStep(
        name='PreprocessIrisData',
        processor=script_processor,
        inputs=[
            ProcessingInput(
                source=input_data_uri, 
                destination='/opt/ml/processing/input'
            )
        ],
        outputs=[
            ProcessingOutput(
                source='/opt/ml/processing/output',
                destination=outout_data_uri,
                output_name='ProcessedData'
            )
        ],
        code='src/preprocessing.py' 
    )
    

    custom_estimator = Estimator(
        image_uri=image_uri,
        entry_point='train.py',
        source_dir='src', 
        role=role,
        instance_type=training_instance_type, 
        instance_count=1,
        framework_version='1.2-1',
        hyperparameters={
            'max_leaf_nodes': 30
        },
        sagemaker_session=pipeline_session,
        environment={
            'MLFLOW_TRACKING_ARN': os.getenv('MLFLOW_TRACKING_ARN', '')
        }  
    
    )
    
    training_step = TrainingStep(
        name='TrainIrisModel',
        # estimator=sklearn_estimator,
        estimator=custom_estimator, # Use the custom estimator,
        inputs={
            'train': processing_step.properties.ProcessingOutputConfig.Outputs['ProcessedData'].S3Output.S3Uri
        },
        depends_on=[processing_step]
    )
    
    # Create Pipeline
    pipeline = Pipeline(
        name='iris-mlflow-pipeline',
        steps=[processing_step, training_step],
        sagemaker_session=pipeline_session
    )
    
    return pipeline

def main():
    # Initialize SageMaker session and get role
    sagemaker_session = sagemaker.Session()
    
    role = 'arn:aws:iam::750573229682:role/service-role/AmazonSageMaker-ExecutionRole-20241211T150457' 
    
    # S3 URI for input data
    input_data_uri = "s3://mlflow-sagemaker-us-east-1-750573229682/iris-dataset/"

    # S3 URI for output data
    outout_data_uri = "s3://mlflow-sagemaker-us-east-1-750573229682/iris-output/"

    # Create pipeline
    pipeline = create_sagemaker_pipeline(
        role, 
        sagemaker_session, 
        input_data_uri,
        outout_data_uri
    )
    
    # Upsert pipeline
    pipeline.upsert(role_arn=role)
    
    # Execute the pipeline
    execution = pipeline.start()
    
    # Wait for the pipeline to finish
    execution.wait()
    
    print("Pipeline execution completed.")
    print("Pipeline Execution Status:", execution.describe()['PipelineExecutionStatus'])

if __name__ == '__main__':
    main()

