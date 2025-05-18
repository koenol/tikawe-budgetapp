if python install.py; then
    exit 0
elif python3 install.py; then
    exit 0
else
    echo "Error: Could not execute install.py using using python and python3."
    read -p "Possible causes: Python is not installed correctly or the install.py file is missing. Try manual installation. If that does not solve the problem, contact the developer." 
    exit 1
fi