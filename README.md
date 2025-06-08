
# 📚 Libramind Backend

A production-grade, modular, and scalable backend for a library management system, built using **FastAPI**, **PostgreSQL**, **SQLAlchemy**, and **Alembic**. It supports student and book management, issuance tracking, and enforces clean REST API design principles.

---

## 🚀 Features

- ✅ Modular folder structure with separation of concerns  
- ✅ FastAPI with automatic OpenAPI docs  
- ✅ PostgreSQL + SQLAlchemy ORM + Alembic migrations  
- ✅ Complete Book & Student management APIs  
- ✅ Book issuance and return logic with availability enforcement  
- ✅ Input validation with Pydantic  
- ✅ Consistent error handling and status codes  
- ✅ Docker and local development support  

---

## 🏗️ Tech Stack

| Layer       | Tool/Library               |
|-------------|----------------------------|
| Web Server  | FastAPI + Uvicorn          |
| Database    | PostgreSQL                 |
| ORM         | SQLAlchemy                 |
| Migrations  | Alembic                    |
| Validation  | Pydantic                   |
| Packaging   | Docker, Docker Compose     |
| Logging     | Python `logging` module    |

---

## 🧪 Sample API Usage

### ✅ Create a Student
```http
POST /students/
Content-Type: application/json

{
  "roll_number": "CS101",
  "name": "Alice"
}
```

---

### ✅ Create a Book
```http
POST /books/
Content-Type: application/json

{
  "title": "Clean Code",
  "author": "Robert C. Martin",
  "isbn": "9780132350884",
  "category": "Programming",
  "copies": 3
}
```

---

### ✅ Issue a Book
```http
POST /books/issue/
Content-Type: application/json

{
  "student_roll_number": "CS101",
  "book_id": 1,
  "days_for_issue": 7
}
```

---

### ✅ Return a Book
```http
POST /books/return/
Content-Type: application/json

{
  "student_roll_number": "CS101",
  "book_id": 1
}
```

---

### ✅ Get All Books
```http
GET /books/
```

---

## 🗃️ Database Schema Overview

### 📘 `books` Table
| Column    | Type     | Description                      |
|-----------|----------|----------------------------------|
| id        | Integer  | Primary key                      |
| title     | String   | Book title                       |
| author    | String   | Book author                      |
| isbn      | String   | Unique ISBN                      |
| category  | String   | Genre/category                   |
| copies    | Integer  | Available copies in the library  |

---

### 🧑‍🎓 `students` Table
| Column        | Type     | Description               |
|---------------|----------|---------------------------|
| id            | Integer  | Primary key               |
| name          | String   | Full name                 |
| roll_number   | String   | Unique student ID         |

---

### 🔗 `issued_books` Table
| Column             | Type     | Description                               |
|--------------------|----------|-------------------------------------------|
| id                 | Integer  | Primary key                               |
| book_id            | FK       | References `books.id`                     |
| student_id         | FK       | References `students.id`                  |
| issued_date        | Date     | Date the book was issued                  |
| due_date           | Date     | Date the book is expected to be returned  |
| returned_date      | Date     | Date the book was actually returned       |


---

## 🛠️ Setup Instructions

### 🧑‍💻 Local Development

1. **Clone the repository**
    ```bash
    git clone https://github.com/IVYLIFE/Libramind-backend
    cd LibraMind-backend
    ```

2. **Install dependencies**
    ```bash
    python -m venv .LibraMind
    source .LibraMind/bin/activate
    pip install -r requirements.txt
    ```

3. **If you have local PostgreSQL then ensure it's running**
   ```bash
    sudo su - postgres psql
    \i app/database/sql/db.sql
    \i app/database/sql/tables.sql
    psql -U skinnysky -h localhos -d libramind   
   ```
   [ Login to psql console as postgres user ] </br>
   [ Run the script to create DB and User/Role ] </br>
   [ Run the script to create tables and add records ] </br>
   [ Login to psql console with the created user ] </br></br>


4. **Configure `.env`** (based on `config.py`)
   ```
   DB_HOST=localhost
   DB_PORT=5432
   DB_USER=your_user
   DB_PASSWORD=your_password
   DB_NAME=libramind_db
   ```

5. **Run Alembic migrations** (optional, if using Alembic):
   ```bash
   alembic upgrade head
   ```

6. **Start the development server**
   ```bash
   fastapi dev app.py
   ```

---

### 🐳 Docker Setup
Only of there's no local PostgreSQL:

```bash
docker-compose up --build
```

This spins up:
- `fastapi-app`: your API
- `postgres`: PostgreSQL with preconfigured DB

---

## 🔐 Status Codes & Error Handling

- `200 OK` – Successful GET/POST
- `201 Created` – Resource created
- `400 Bad Request` – Validation failure or missing input
- `404 Not Found` – Resource not found
- `409 Conflict` – Book already issued, no copies left, etc.
- `422 Unprocessable Entity` – Schema validation error

Custom exception handlers are used for meaningful error messages via:
```python
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
```

---

## 📎 Example `.env` File

```env
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=libramind_db
```

---

## 📖 API Documentation

Once running, visit:

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## Sample API Usage

NOTE : For Complete API Documentation Refer to Swagger UI Docs

1. **List all books**

    ```bash
    curl -X GET "http://localhost:8000/books"
    ```
</br>

2. **Add a new book**

    ```bash
    curl -X POST "http://localhost:8000/books" \
    -H "Content-Type: application/json" \
    -d '{"title":"New Book","author":"Author","isbn":"1234567890123","category":"Fiction","copies":5}'
    ```
</br>

3. **Issue a book to a student**

    ```bash
    curl -X POST "http://localhost:8000/books/15" \
    -H "Content-Type: application/json" \
    -d '{"student_id":"CS101","duration_days":7}'
    ```
</br>


4. **List all students**

    ```bash
    curl -X GET "http://localhost:8000/students"
    ```
</br>


5. **Add a new student**

    ```bash
    curl -X POST "http://localhost:8000/students" \
    -H "Content-Type: application/json" \
    -d '{"name":"Jane Doe","roll_number":"CS150","department":"CS","semester":2,"phone":"9876543210","email":"jane.doe@example.com"}'
    ```
</br>


6. **Get a student by identifier**

    ```bash
    curl -X GET "http://localhost:8000/students/CS101"
    ```
</br>


7. **List books issued to a student**

    ```bash
    curl -X GET "http://localhost:8000/students/CS101/books"
    ```
</br>


8. **Return a book**
    ```bash
    curl -X PATCH "http://localhost:8000/students/CS101/books/15"
    ```
</br>
</br>


## 📚 Libramind - Overdue Reminder System

This subsystem handles **automated overdue tracking and email remainder** in the Libramind backend, using **Celery + Redis + SendGrid**.

---

### 🚀 Architecture Overview

### 🔧 Components:
- **Celery**: Background task queue.
- **Redis**: Broker for Celery (used to queue and manage tasks).
- **Brevo (Sendinblue)**: Email delivery provider (used to send remainder).
- **Scheduler**: Runs periodic tasks (using Celery Beat or custom logic).
- **Email Utility:** Sends reminder emails using SMTP.
- **Database:** Uses `issued_books` table for due/return tracking.
</br>

---

## 🧠 System Design

1. **Periodic Celery task** runs daily.
2. It identifies:
   - Issued books where `returned_date IS NULL`
   - And `due_date <= today + 5`
3. For each qualifying record:
   - An email is queued using **Brevo (Sendinblue)**.
4. If sending fails:
   - Celery retries the task automatically.

---
</br>


## 📬 Email Reminder Flow

- Subject: `"Library Reminder: Book Due Soon"`
- Body includes:
  - Book title
  - Due date
  - Days remaining
  - Instructions to return

---
</br>


## 🛠️ Setup Instructions

### 1. Install Python Packages

```bash
pip install celery[redis] redis
```

### 2. Start Redis Server

```bash
docker run -d -p 6379:6379 redis
```

### 3. Set Environment Variables in `.env`

```env
REDIS_URL=redis://localhost:6379/0
SMTP_SERVER=smtp-relay.brevo.com
SMTP_PORT=587
SMTP_USERNAME=your_verified_email@example.com
SMTP_PASSPASSWORD=your_brevo_api_key
SMTP_FROM_EMAIL=library@example.com

```

### 4. Run Celery Worker

```bash
celery -A app.celery_worker.celery_app worker --loglevel=info
```

### 5. Trigger the Daily Reminder Task

(Manual call for testing)

```bash
celery -A app.celery_worker.celery_app call app.scheduler.daily_tasks.send_daily_remainder
```


## ✅ Key Features

- Safe to use in production
- Decouples reminder logic from API
- Daily automated email triggers
- Duplicate-proof: one reminder per student-book per day
- Easily extendable to SMS/WhatsApp

---

## 📈 Future Enhancements

- Dashboard for admins to track email history
- Custom schedule intervals (every 12h, etc.)

---

> This module ensures overdue tracking and notifications are **fully automated, reliable, and scalable**.


## 👤 Author

**HIMANSHU** — Backend developer

</br>

## ✅ Next Steps / Enhancements

- Add authentication (JWT + roles)
- Testing with `pytest`

</br>


## 📝 License

MIT License (or update as per your preference)
