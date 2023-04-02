Team Members: [Ashutosh Panda](https://github.com/aashutoshPanda) &amp; [Pratik Chaudhary](https://github.com/pratik0204)

- WEBSITE HOSTED: https://nimbus-nest.netlify.app
- BACKEND-HOSTED: https://nimbus-nest-drf.onrender.com

Make sure you have [python3](https://www.python.org/downloads/) and [git](https://git-scm.com/) installed on your local machine.

## Getting Started

Setup project environment-

```bash
$ sudo apt-get update -y
$ sudo apt-get install python3-pip -y
$ sudo apt-get install python3-venv -y
$ sudo apt-get install libpq-dev -y

$ git clone https://github.com/aashutoshPanda/nimbus-nest.git
$ cd nimbus-nest

$ python3 -m venv env
$ source env/bin/activate
$ pip3 install -r requirements.txt

$ python manage.py migrate
$ python manage.py migrate --run-syncdb
$ python manage.py runserver
```

Create super user
```bash
$ python manage.py createsuperuser
```

## Frontend
You can cd into the client folder, and follow the readme there.

## Contributing
We love contributions, so please feel free to add issues fix bugs, improve things, provide documentation and make a PR.
