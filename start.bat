@echo off
echo [Flask 서버 실행 중... http://127.0.0.1:5000/ ]
set FLASK_APP=app.py
set FLASK_ENV=development
python -m flask run
pause