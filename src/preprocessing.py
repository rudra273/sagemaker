import os
import pandas as pd
from src.utils.helper import test_function

def load_data(data_path):
    """
    Load the preprocessed Iris dataset
    
    Args:
        data_path (str): Path to the preprocessed data file
    
    Returns:
        pandas.DataFrame: Loaded Iris dataset
    """

    # Read the preprocessed Iris dataset
    df_iris = pd.read_csv(data_path, header=None)
    test_function()
    
    return df_iris 
 



# Main execution block
if __name__ == "__main__":
    # Input and output paths from SageMaker Processing
    input_path = "/opt/ml/processing/input"
    output_path = "/opt/ml/processing/output"
    
    # Ensure output directory exists
    os.makedirs(output_path, exist_ok=True)
    
    # Find the input file (assuming there's only one)
    input_files = os.listdir(input_path)
    if not input_files:
        raise ValueError("No input files found in the input directory")
    
    
    input_file_path = os.path.join(input_path, input_files[0])
    output_file_path = os.path.join(output_path, "iris.csv")
    
    # Execute loading step
    print(f"Loading data from: {input_file_path}")
    processed_data = load_data(input_file_path)
    
    print(f"Saving processed data to: {output_file_path}")
    processed_data.to_csv(output_file_path, index=False, header=False)
    
    print("Processing complete!") 


# # Main execution block
# if __name__ == "__main__":
#     # Input and output paths from SageMaker Processing
#     input_path = "/opt/ml/processing/input"
#     output_path = "/opt/ml/processing/output"
    
#     # Ensure output directory exists
#     os.makedirs(output_path, exist_ok=True)
    
#     # Execute loading and concatenating step
#     processed_data = load_data(input_path)

#     # Save the concatenated DataFrame to a single CSV file
#     output_file_path = os.path.join(output_path, "iris_data.csv")
#     print(f"Saving data to: {output_file_path}")
    
#     processed_data.to_csv(output_file_path, index=False, header=False)  # Adjust header as needed
    
#     print("Processing complete!")


