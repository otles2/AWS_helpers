# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.16.6
#   kernelspec:
#     display_name: conda_pytorch_p310
#     language: python
#     name: conda_pytorch_p310
# ---

# !getwd


# !cd /home/ec2-user/AWS_helpers


# +
import boto3
import sagemaker
from sagemaker import get_execution_role

# Initialize the SageMaker role, session, and s3 client
role = sagemaker.get_execution_role() # specifies your permissions to use AWS tools
session = sagemaker.Session() 
s3 = boto3.client('s3')

# -

import pandas as pd
# Define the S3 bucket and object key
bucket_name = 'zoteam-titanic'  # replace with your S3 bucket name

# Read the train data from S3
key = 'titanic_train.csv'  # replace with your object key
response = s3.get_object(Bucket=bucket_name, Key=key)
train_data = pd.read_csv(response['Body'])


# Read the test data from S3
key = 'titanic_test.csv'  # replace with your object key
response = s3.get_object(Bucket=bucket_name, Key=key)
test_data = pd.read_csv(response['Body'])


# check shape
print(train_data.shape)
print(test_data.shape)

# Inspect the first few rows of the DataFrame
train_data.head()

# +
# Define the S3 bucket and file location
key = "titanic_train.csv"  # Path to your file in the S3 bucket
local_file_path = "./titanic_train.csv"  # Local path to save the file

# Initialize the S3 client and download the file
s3.download_file(bucket_name, key, local_file_path)
# !ls

# +
# Initialize the total size counter
total_size_bytes = 0

# List and sum the size of all objects in the bucket
paginator = s3.get_paginator('list_objects_v2')
for page in paginator.paginate(Bucket=bucket_name):
    for obj in page.get('Contents', []):
        total_size_bytes += obj['Size']

# Convert the total size to gigabytes for cost estimation
total_size_gb = total_size_bytes / (1024 ** 3)
# print(f"Total size of bucket '{bucket_name}': {total_size_gb:.2f} GB") # can uncomment this if you want GB reported

# Convert the total size to megabytes for readability
total_size_mb = total_size_bytes / (1024 ** 2)
print(f"Total size of bucket '{bucket_name}': {total_size_mb:.2f} MB")
# -

# %cd /home/ec2-user/SageMaker/

# !git clone https://github.com/otles2/AWS_helpers.git


import AWS_helpers.helpers as helpers
helpers.get_s3_bucket_size(bucket_name)

# +
# AWS S3 Standard Storage pricing for US East (N. Virginia) region
# Pricing tiers as of November 1, 2024
first_50_tb_price_per_gb = 0.023  # per GB for the first 50 TB
next_450_tb_price_per_gb = 0.022  # per GB for the next 450 TB
over_500_tb_price_per_gb = 0.021  # per GB for storage over 500 TB

# Calculate the cost based on the size
if total_size_gb <= 50 * 1024:
    # Total size is within the first 50 TB
    cost = total_size_gb * first_50_tb_price_per_gb
elif total_size_gb <= 500 * 1024:
    # Total size is within the next 450 TB
    cost = (50 * 1024 * first_50_tb_price_per_gb) + \
           ((total_size_gb - 50 * 1024) * next_450_tb_price_per_gb)
else:
    # Total size is over 500 TB
    cost = (50 * 1024 * first_50_tb_price_per_gb) + \
           (450 * 1024 * next_450_tb_price_per_gb) + \
           ((total_size_gb - 500 * 1024) * over_500_tb_price_per_gb)

print(f"Estimated monthly storage cost: ${cost:.4f}")
print(f"Estimated annual storage cost: ${cost*12:.4f}")
# -

monthly_cost, storage_size_gb = helpers.calculate_s3_storage_cost(bucket_name)
print(f"Estimated monthly cost ({storage_size_gb:.4f} GB): ${monthly_cost:.5f}")
print(f"Estimated annual cost ({storage_size_gb:.4f} GB): ${monthly_cost*12:.5f}")

# +
# Define the S3 bucket name and the file paths
train_file_path = "results.txt" # assuming your file is in root directory of jupyter notebook (check file explorer tab)

# Upload the training file to a new folder called "results". You can also just place it in the bucket's root directory if you prefer (remove results/ in code below).
s3.upload_file(train_file_path, bucket_name, "results/results.txt")

print("Files uploaded successfully.")

# +
# Define the S3 bucket name and the file paths
train_file_path = "results.txt" # assuming your file is in root directory of jupyter notebook (check file explorer tab)

# Upload the training file to a new folder called "results". You can also just place it in the bucket's root directory if you prefer (remove results/ in code below).
s3.upload_file(train_file_path, bucket_name, "results/results.txt")

print("Files uploaded successfully.")

# +
import getpass

# Prompt for GitHub username and PAT securely
username = input("GitHub Username: ")
token = getpass.getpass("GitHub Personal Access Token (PAT): ")
# -

# !git config --global user.name "Zekai Otles"
# !git config --global user.email otles2@wisc.edu

# !pip install jupytext

# Adjust filename(s) if you used something different
# !jupytext --to py Interacting-with-S3.ipynb

# !git status


# !git status!

# !ls

# !git status

# !pwd

# !ls -a


