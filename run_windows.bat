@echo off
echo Starting Error Lookup App...

:: Check if virtual environment exists, if not create it
if not exist ".venv\" (
    echo Creating virtual environment...
    python -m venv .venv
)

:: Activate the virtual environment
call .venv\Scripts\activate.bat

:: Install requirements
echo Checking dependencies...
pip install -r requirements.txt > nul 2>&1

:: Run the Streamlit app
echo Launching Streamlit...
streamlit run app.py

pause
