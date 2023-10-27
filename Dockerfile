from python:latest
copy . .
workdir .
env FLASK_APP=app \
FLASK_ENV=development \
PORT=4000
run pip install flask hashids ;  python init_db.py
cmd python app.py