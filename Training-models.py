# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.16.6
#   kernelspec:
#     display_name: conda_python3
#     language: python
#     name: conda_python3
# ---

# +
import getpass

# Prompt for GitHub username and PAT securely
username = input("GitHub Username: ")
token = getpass.getpass("GitHub Personal Access Token (PAT): ")
# -

# !git clone https://github.com/otles2/AWS_helpers.git

# %cd AWS_helpers

# !ls

# !git status

# !pwd

# !cp ../results.txt 
# !cp ../titanic_train.csv .
# !cp Interacting-with* .


# !ls

# !pwd

# !ls

# !cp ../results.txt .

# !ls

# !pwd

# !ls

# !git status

# !git add . # you may also add files one at a time, for further specificity over the associated commit message
# !git commit -m "Updates" # in general, your commit message should be more specific!

# !git push

# !git status

# !pwd

# !git pull

# !git status

# !git push

# !pip install jupytext

github_url='github.com/otles2/AWS_helpers'

# !git push https://{username}:{token}@{github_url} main

# !git pull

# !ls -a

# !vi .gitignore


