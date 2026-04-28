#!/bin/bash
cd "$(dirname "$0")"

echo "Starting Error Lookup App..."

# Check if virtual environment exists, if not create it
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate the virtual environment
source .venv/bin/activate

# Install requirements
echo "Checking dependencies..."
pip install -r requirements.txt > /dev/null 2>&1

# Run the Streamlit app
echo "Launching Streamlit..."
streamlit run app.py
