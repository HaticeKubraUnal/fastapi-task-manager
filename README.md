# FastAPI Task Manager

This project is a simple, full-stack To-Do List application built from scratch specifically to learn and practice FastAPI, modern backend architecture, and related technologies. Despite being a small learning project, it successfully implements relational database logic, RESTful API design, and authorization standards.
## 🚀 Features

* **Authentication:** Secure registration and login system using JWT (JSON Web Tokens) and password hashing (bcrypt).
* **Relational Database:** One-to-Many relationship (User-Task) implementation using SQLModel and SQLite.
* **Data Isolation:** A secure architecture ensuring users can only view, update, and manage their own tasks.
* **Full CRUD Operations:** Complete API endpoints for creating, reading, partially updating, and deleting tasks.
* **User Interface:** A responsive frontend integrated with the backend using HTML, CSS, and Vanilla JavaScript (Fetch API).
* **Professional Standards:** Secure environment variable management for secrets using Pydantic-Settings and `.env` files.

## 🛠️ Tech Stack

* **Backend:** FastAPI, Python
* **Database & ORM:** SQLite, SQLModel
* **Security:** PyJWT, Passlib (Bcrypt)
* **Frontend:** HTML5, CSS3, JavaScript

## ⚙️ Installation & Setup

Follow these steps to run the project locally on your machine.

**1. Clone the Repository:**
```bash
git clone [https://github.com/HaticeKubraUnal/fastapi-task-manager.git](https://github.com/HaticeKubraUnal/fastapi-task-manager.git)
cd fastapi-task-manager
```

**2. Install Dependencies:**
```bash
pip install fastapi[all] sqlmodel passlib[bcrypt] pyjwt pydantic-settings
```

**3. Set Up Environment Variables:**
Create a `.env` file in the root directory of the project and add your secure configuration:
```env
SECRET_KEY="your_super_secret_key_here"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**4. Run the Server:**
```bash
fastapi dev app/main.py
```

**5. Access the Application:**
* Web Interface: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
* API Documentation (Swagger UI): [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## 📸 Pictures From Project
<img img width="88%" alt="image" src="https://github.com/user-attachments/assets/e6719212-65a0-4050-9c96-637a21768686" />
<br>
<br>
<img width="891" height="646" alt="image" src="https://github.com/user-attachments/assets/92022887-5a39-4bd7-8d1b-9dd8a7adf904" />

