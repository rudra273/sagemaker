import argparse
import os
import joblib
import pandas as pd
import mlflow
from sklearn import tree
from utils.helper import test_function
test_function()

def train(train_data, max_leaf_nodes=-1):
    """
    Train a decision tree classifier
    
    Args:
        train_data (pd.DataFrame): Training data with first column as target
        max_leaf_nodes (int, optional): Maximum number of leaf nodes. Defaults to -1.
    
    Returns:
        sklearn.tree.DecisionTreeClassifier: Trained model
    """
    # Separate features and target
    train_y = train_data.iloc[:, 0]
    train_X = train_data.iloc[:, 1:]
    
    # Train decision tree classifier
    clf = tree.DecisionTreeClassifier(max_leaf_nodes=max_leaf_nodes)
    clf = clf.fit(train_X, train_y)
    
    return clf

def main():
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--max_leaf_nodes', type=int, default=-1)

    parser.add_argument('--output-data-dir', type=str, default=os.environ.get('SM_OUTPUT_DATA_DIR', '/opt/ml/output'))
    parser.add_argument('--model-dir', type=str, default=os.environ.get('SM_MODEL_DIR', '/opt/ml/model'))
    # parser.add_argument('--train', type=str, default=os.environ.get('SM_CHANNEL_TRAIN', './data'))
    parser.add_argument('--train', type=str, default=os.environ.get('SM_CHANNEL_TRAIN', '/opt/ml/input/data/train'))
    
    args = parser.parse_args()
    
    # Read input files 
    input_files = [
        os.path.join(args.train, file) 
        for file in os.listdir(args.train) 
        if os.path.isfile(os.path.join(args.train, file))
    ]

    print(f"Input files: {input_files}") 
    
    if not input_files:
        raise ValueError('No input files found in the training directory')
    
    # Read and concatenate data
    raw_data = [pd.read_csv(file, header=None, engine="python") for file in input_files]
    train_data = pd.concat(raw_data)

    print(f"Training data shape: {train_data.shape}")
    
    # Set MLflow tracking URI (if needed)
    tracking_uri = os.environ.get('MLFLOW_TRACKING_URI')
    if tracking_uri:
        mlflow.set_tracking_uri(tracking_uri)

    print(tracking_uri)
    
    # Enable MLflow autologging
    mlflow.autolog()

    print("Autologging enabled") 
    
    # Train the model
    with mlflow.start_run():
        clf = train(train_data, args.max_leaf_nodes)
        
        # Save the model
        joblib.dump(clf, os.path.join(args.model_dir, "model.joblib"))
        
        # Register the model with MLflow
        mlflow.sklearn.log_model(
            sk_model=clf, 
            artifact_path="model", 
            registered_model_name="sm-job-experiment-model"
        )



if __name__ == '__main__':
    main()
