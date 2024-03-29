Team Members: [Ashutosh Panda](https://github.com/aashutoshPanda) &amp; [Pratik Chaudhary](https://github.com/pratik0204)

- WEBSITE HOSTED: https://nimbus-nest.netlify.app
- BACKEND-HOSTED: https://nimbus-nest-drf.onrender.com

<p align="center">
  <a href="https://ibb.co/2cyxSwk">
    <img src="https://i.ibb.co/HGV6C0H/Screenshot-from-2021-05-19-14-43-17.png" alt="Vicara Preview" border="0">
  </a>
</p>

Make sure you have [python3](https://www.python.org/downloads/) and [git](https://git-scm.com/) installed on your local machine.

### Features

1. Upload & Download - files and folders with Drag & Drop

- Also you can upload with a downloadable url
- Folders are downloaded as zip

2. Mark your files or Folders as favourite for quick access

3. Trash - Upon deletion your valuables in trash, you can also permanently delete from there

4. Share files & folders with your peers with a shareable url!

- All the files shared with you will be present in 'Shared with Me' section

5. Admin panel to allocate max disk space for a user

- Initially all users are provided with 100 MB of storage
- Storage can be upgraded to any limit - We store our files in AWS S3

6. Google OAuth for quick and easy logins

7. Move folders and files across the drive

8. File preview directly in the drive for images, PDFs, etc.

9. Tour of the platform for new users, you can also get a tour with the 'HELP' button at the top-right corner.

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

## Backend Maintenance

Backend is hosted on - https://dashboard.render.com/d/dpg-clqnopie9h4c73ao5fp0-a

1. Free Postgres DB expires in 90 days [today 10 DEC - next expiry 10 MARCH]
2. Make new postgres DB on render.com
3. Copy the external DB url and update `DATABASE_URL` in the backend service ENV VARS and save changes
4. Use clear build cache and re-deploy option to get the latest changes
5. Shell access is present only for paid services, the DB is fresh we need to apply migrations and create super-user etc..
6. Clone the project, remove old env and create a new one

```
rm -rf env
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

7. and in the .env file add the DATABASE_URL as the external URL of postgres from render.com

For super-user provide the same username and password as provided in env file / ENV VARS in render.com

```
python manage.py makemigrations
python manage.py migrate
python manage.py migrate --run-syncdb
python manage.py createsuperuser
```

7. Now the /admin should work in the deployed backend, login and follow these for oauth setup - https://iamashutoshpanda.medium.com/google-login-with-django-react-part-2-2dc41b499861

8. Go to deploy section and clear cache and deploy site.
