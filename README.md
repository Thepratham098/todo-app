# 🚀 Todo App (Docker + Flask + PostgreSQL)

A **full-stack Task Management Web Application** built using **Flask, PostgreSQL, and Docker**, featuring secure user authentication and a clean, modern UI inspired by Notion.

---

## 📌 Features

- 🔐 **User Authentication** (Register & Login)
- 📝 **Create, Update, Delete Tasks**
- ✅ **Mark Tasks as Completed**
- 👤 **User-Specific Task Management** (Data Isolation)
- 🔍 **Task Search Functionality**
- 🎨 **Clean Notion-Style UI** (Bootstrap-based)
- 🐳 **Fully Dockerized** (One-command setup)
- 🗄️ **PostgreSQL Integration**

---

## 🛠️ Tech Stack

| Layer            | Technology |
|------------------|-----------|
| Frontend         | HTML, CSS, Bootstrap |
| Backend          | Flask (Python) |
| Database         | PostgreSQL |
| Containerization | Docker, Docker Compose |
| Deployment       | Railway |

---

## ⚙️ Setup Instructions (Local)

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/todo-app.git
cd todo-app
2️⃣ Run Using Docker
docker compose up --build
3️⃣ Open in Browser
http://localhost:5000
🐳 Docker Services
Service	Description
web	Flask application
db	PostgreSQL database
🔑 Environment Variables (For Deployment)

Set the following variables in your deployment platform:

PGHOST=your-db-host
PGDATABASE=todo_db
PGUSER=postgres
PGPASSWORD=your-password
🚀 Deployment (Railway)

This project is deployed using Railway.

Steps:

Push your code to GitHub

Go to Railway and create a new project

Connect your GitHub repository

Add a PostgreSQL service

Configure environment variables

Deploy 🚀

📸 Screenshots (Optional)

Add screenshots here (Login Page, Dashboard, Task View, etc.)

📈 Future Improvements

🔔 Task reminders & notifications

📱 Mobile-first UI enhancements

📊 Task analytics dashboard

🌙 Dark mode support

🔐 OAuth (Google/GitHub login)

🤝 Contributing

Contributions are welcome!

# Fork the repository
# Create a new branch
git checkout -b feature/your-feature-name

# Commit your changes
git commit -m "Add your feature"

# Push to branch
git push origin feature/your-feature-name
📄 License

This project is licensed under the MIT License.

💡 Author

Prathamesh
💻 Passionate about building scalable and real-world applications
