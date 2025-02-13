#!/bin/bash

# Exit script on any error
set -e

# Initialize conda in the script (to ensure proper shell environment setup)
eval "$(conda shell.bash hook)"

# Activate the virtual environment (if applicable)
conda activate ./.conda

# Run Streamlit in the background
echo "Starting Streamlit..."
streamlit run ./translation/yttranscriber.py &

# Run Django development server
echo "Starting Django server..."
python manage.py runserver

# Keep the terminal open (optional)
wait
