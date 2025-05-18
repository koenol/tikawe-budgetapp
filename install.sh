if pip install flask; then
    echo "Flask installed."
else
    echo "Error: Could not execute pip install flask."
    read -p "Possible causes: Pip is not installed correctly."
fi

if [ -f schema.sql ]; then
    echo "schema.sql found"
else
    echo "Error: Could not locate schema.sql, unable to continue the installation."
    read -p "Possible solution: Try to create database manually by running python install.py or python3 install.py. If that does not solve the problem, contact the developer."
    exit 1
fi

if python install.py; then
    echo "Database created succesfully"
    exit 0
elif python3 install.py; then
    echo "Database created succesfully"
    exit 0
else
    echo "Error: Could not execute install.py using using python and python3."
    read -p "Possible causes: Python is not installed correctly or the install.py file is missing. Try manual installation. If that does not solve the problem, contact the developer." 
    exit 1
fi