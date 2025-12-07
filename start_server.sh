#!/bin/bash

# 1. Setup Virtual Environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate

# 2. Install Dependencies
echo "Installing dependencies..."
pip install -r api_service/requirements.txt
pip install -r admin_service/requirements.txt

# 3. Start Services
echo "Starting FastAPI on 0.0.0.0:8000..."
cd api_service
nohup uvicorn main:app --host 0.0.0.0 --port 8000 > ../api.log 2>&1 &
cd ..

echo "Starting Django on 0.0.0.0:8001..."
cd admin_service
nohup python manage.py runserver 0.0.0.0:8001 > ../admin.log 2>&1 &
cd ..

echo "Services started! Check api.log and admin.log for output."
