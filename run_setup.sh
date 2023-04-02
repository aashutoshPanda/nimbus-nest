set -x
rm -rf env
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt

python manage.py migrate
python manage.py migrate --run-syncdb
python manage.py runserver