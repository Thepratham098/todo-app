🚀 Todo App (Docker + Flask + PostgreSQL)
A full-stack Task Management Web Application built using Flask, PostgreSQL, and Docker, featuring user authentication and a clean, modern UI.
📌 Features
🔐 User Authentication (Login/Register)
📝 Create, Update, Delete Tasks
✅ Mark tasks as Completed
👤 User-specific task management (data isolation)
🎨 Clean Notion-style UI with Bootstrap
🔍 Task search functionality
🐳 Fully Dockerized (easy setup & deployment)
🗄️ PostgreSQL database integration
🛠️ Tech Stack
Frontend: HTML, CSS, Bootstrap
Backend: Flask (Python)
Database: PostgreSQL
Containerization: Docker & Docker Compose
Deployment: Railway
📂 Project Structure

todo-docker-app/
│
├── app/
│   ├── app.py
│   ├── templates/
│   │   ├── index.html
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── profile.html
│   │
│   ├── static/
│   │   ├── style.css
│   │
│   ├── requirements.txt
│
├── Dockerfile
├── docker-compose.yml
├── README.md
⚙️ Setup Instructions (Local)
1️⃣ Clone the repository
Bash
git clone https://github.com/your-username/todo-app.git
cd todo-app
2️⃣ Run using Docker
Bash
docker compose up --build
3️⃣ Open in browser

http://localhost:5000
🐳 Docker Services
web → Flask application
db → PostgreSQL database
🔑 Environment Variables (for deployment)

PGHOST=your-db-host
PGDATABASE=todo_db
PGUSER=postgres
PGPASSWORD=your-password
🚀 Deployment
This project is deployed using Railway.
Steps:
Push code to GitHub
Connect repo to Railway
Add PostgreSQL service
Configure environment variables
Deploy
