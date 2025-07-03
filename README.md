
Photo Adventures

📸 About the Project

Photo Adventures is a web-based platform where users can share their photography experiences through blog posts. The project is built using Django, integrating cloud storage for image hosting, user authentication, social sharing, and an interactive commenting system.

🚀 Features

User Authentication: Secure login and signup using Django AllAuth.

CRUD Functionality: Users can create, edit, and delete blog posts.

Image Uploads: Cloudinary integration for seamless image storage.

Like & Comment System: Users can interact with posts through likes and comments.

Tagging & Categories: Posts can be categorized and tagged for better discoverability.

Social Sharing: Users can share their posts on social media.

Admin Dashboard: A Django-admin panel for managing content.

Custom 404 Page: Enhanced user experience with a friendly error page.

🛠️ Tech Stack

Backend: Django, Django REST Framework

Frontend: Bootstrap, JavaScript

Database: PostgreSQL

Hosting & Deployment: Gunicorn, Heroku

Cloud Storage: Cloudinary

Authentication: OAuth with Django AllAuth

📦 Installation & Setup

Prerequisites

Python 3.x

PostgreSQL

Virtual Environment (venv or pipenv)

Installation Steps

Clone the repository:

git clone https://github.com/harshh-0304 /photo-adventures.git
cd photo-adventures

Create a virtual environment & activate it:

python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

Install dependencies:

pip install -r requirements.txt

Set up environment variables:
Create a .env file and configure:

SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=your-postgres-url
CLOUDINARY_URL=your-cloudinary-url

Apply migrations:

python manage.py migrate

Create a superuser (optional for admin access):

python manage.py createsuperuser

Run the server:

python manage.py runserver

🔍 Testing

Run the following command to execute tests:

python manage.py test

🚀 Deployment

This project is configured for deployment on Heroku.

Install Heroku CLI and login:

heroku login

Create a Heroku app and push the code:

heroku create your-app-name
git push heroku main

Set up environment variables:

heroku config:set SECRET_KEY=your-secret-key
heroku config:set DATABASE_URL=your-postgres-url

Run migrations on Heroku:

heroku run python manage.py migrate

📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

🤝 Contributing

Fork the repository.

Create a feature branch (git checkout -b feature-branch).

Commit your changes (git commit -m 'Add some feature').

Push to the branch (git push origin feature-branch).

Create a pull request.

📧 Contact

For any questions or feedback, reach out at harshjadav332004@gmail.com.

