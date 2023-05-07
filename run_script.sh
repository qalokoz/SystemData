#!/bin/bash

# Set up the virtual environment and install dependencies
cd /path/to/project
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Define the Python script to run
script_path="/service1"

# Run the Python script
python $script_path

# Deactivate the virtual environment
deactivate

# add this to cron
0 9 * * * /bin/bash /path/to/run_script.sh