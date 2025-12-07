# VegiTrade Backend

Backend services for the VegiTrade application.

## Structure
- `api_service/`: FastAPI service for mobile app API
- `admin_service/`: Django admin panel

## Setup on Server

1. Install dependencies:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r api_service/requirements.txt
pip install -r admin_service/requirements.txt
```

2. Start services:
```bash
chmod +x start_server.sh
./start_server.sh
```

## Services
- FastAPI: `http://YOUR_SERVER:8000`
- Django Admin: `http://YOUR_SERVER:8001/admin`
