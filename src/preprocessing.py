# import os
# import pandas as pd

# from utils.helper import test_function  
# test_function() 

# # # print('helloo') 

# def load_data(data_path):
#     """
#     Load the preprocessed Iris dataset
    
#     Args:
#         data_path (str): Path to the preprocessed data file
    
#     Returns:
#         pandas.DataFrame: Loaded Iris dataset
#     """

#     # Read the preprocessed Iris dataset
#     df_iris = pd.read_csv(data_path, header=None)    
#     return df_iris 
 

# # Main execution block
# if __name__ == "__main__":
#     # Input and output paths from SageMaker Processing
#     input_path = "/opt/ml/processing/input"
#     output_path = "/opt/ml/processing/output"
    
#     # Ensure output directory exists
#     os.makedirs(output_path, exist_ok=True)
    
#     # Find the input file (assuming there's only one)
#     input_files = os.listdir(input_path)
#     if not input_files:
#         raise ValueError("No input files found in the input directory")
    
#     # input_file_path = os.path.join(input_path, input_files[0])

#     input_file_path = os.path.join(input_path, 'iris.csv') 
#     output_file_path = os.path.join(output_path, "iris.csv") 
    
#     # Execute loading step
#     print(f"Loading data from: {input_file_path}")
#     processed_data = load_data(input_file_path)
    
#     print(f"Saving processed data to: {output_file_path}")
#     processed_data.to_csv(output_file_path, index=False, header=False)
    
#     print("Processing complete!") 


import os
import pandas as pd
import csv

from utils.helper import test_function
test_function()

def load_data(data_path):
    """
    Load the Iris dataset while preserving the exact number format
    
    Args:
        data_path (str): Path to the preprocessed data file
    
    Returns:
        list: List of rows with preserved number formatting
    """
    # Read the data as strings to preserve the exact formatting
    with open(data_path, 'r') as file:
        csv_reader = csv.reader(file)
        data = list(csv_reader)
    return data

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
    
    input_file_path = os.path.join(input_path, 'iris.csv')
    output_file_path = os.path.join(output_path, "preprocessed_iris.csv") 
    
    # Execute loading step
    print(f"Loading data from: {input_file_path}")
    processed_data = load_data(input_file_path)
    
    print(f"Saving processed data to: {output_file_path}")
    # Write the data exactly as read
    with open(output_file_path, 'w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerows(processed_data)
    
    print("Processing complete!") 