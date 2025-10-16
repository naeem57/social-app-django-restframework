🧠 Social App (Django)

A simple social media web application built using Django and Django REST Framework (DRF).
Users can register, log in, create posts, follow others, and interact with posts in real-time using WebSockets.

🚀 Features

🔐 User authentication (JWT)

👤 Create and update user profiles

📝 Create, update, and delete posts

❤️ Like and comment on posts

💬 Real-time chat using Django Channels

🕵️ Search users and posts

📸 Upload media (images/videos)

⚙️ Admin panel for managing users and posts

🛠️ Tech Stack

Backend: Django, Django REST Framework

Real-Time: Django Channels, Redis

Database: PostgreSQL (or SQLite for local testing)

Auth: JWT Authentication

Media Handling: Cloudinary or local storage

⚙️ Installation & Setup
1️⃣ Clone the Repository
git clone https://github.com/yourusername/social-app-django.git
cd social-app-django

2️⃣ Create Virtual Environment
python -m venv venv
venv\Scripts\activate  # (On Windows)
# OR
source venv/bin/activate  # (On macOS/Linux)

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Apply Migrations
python manage.py makemigrations
python manage.py migrate

5️⃣ Run Server
python manage.py runserver


Now visit → http://127.0.0.1:8000/

🔑 API Endpoints
Method	Endpoint	Description
POST	/api/register/	Register new user
POST	/api/login/	Login and get JWT token
GET	/api/user/	Get logged-in user info
POST	/api/posts/	Create post
GET	/api/posts/	Get all posts
PUT	/api/posts/<id>/	Update post
DELETE	/api/posts/<id>/	Delete post
