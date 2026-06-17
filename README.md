# KanMind Backend

A RESTful backend for **KanMind**, a Kanban-style project management tool.
It provides token-authenticated endpoints for managing boards, tasks and
comments, built with Django and the Django REST Framework.

---

## Features

- Token-based authentication (registration & login)
- Boards with an owner and members
- Tasks with status, priority, assignee and reviewer
- Dedicated lists for tasks **assigned to** or **reviewed by** the current user
- Comments on tasks
- Object-level permissions (owner / member / creator rules)

---

## Tech Stack

| Component  | Version                              |
| ---------- | ------------------------------------ |
| Language   | Python 3.12+ (required by Django 6)  |
| Framework  | Django 6.0.6                         |
| API        | Django REST Framework 3.17.1         |
| Database   | SQLite                               |
| Auth       | DRF Token Authentication             |

---

## Project Structure

```
kanmind_backend/
├── core/         # Project settings, root URL config, WSGI/ASGI
├── auth_app/     # Registration, login, email check
│   └── api/      # serializers.py, views.py, urls.py
├── kanban_app/   # Boards, tasks, comments
│   └── api/      # serializers.py, views.py, urls.py, permissions.py
├── manage.py
└── requirements.txt
```

---

## Getting Started

### Prerequisites

- Python 3.12 or newer
- `pip` and `venv`

### Installation

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd kanmind_backend
   ```

2. **Create and activate a virtual environment**

   ```bash
   python -m venv .venv
   ```

   Activate it — **Windows (PowerShell):**

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

   **macOS / Linux:**

   ```bash
   source .venv/bin/activate
   ```

3. **Install the dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Create a `.env` file** in the project root (it is git-ignored) with a
   Django secret key:

   ```
   SECRET_KEY=your-secret-key-here
   ```

   You can generate one with:

   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

5. **Apply the database migrations**

   ```bash
   python manage.py migrate
   ```

6. **(Optional) Create an admin user** to use the Django admin at `/admin/`:

   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**

   ```bash
   python manage.py runserver
   ```

   The API is now available at `http://127.0.0.1:8000/`.

---

## Authentication

The API uses **token authentication**. Register or log in to receive a token,
then send it with every authenticated request in the `Authorization` header:

```
Authorization: Token <your-token>
```

Registration and login responses both return:

```json
{
  "token": "...",
  "fullname": "Max Mustermann",
  "email": "max@example.com",
  "user_id": 1
}
```

---

## API Endpoints

Base path: `/api/`

### Authentication

| Method | Endpoint             | Description                       | Auth |
| ------ | -------------------- | --------------------------------- | ---- |
| POST   | `/registration/`     | Create a new user                 | No   |
| POST   | `/login/`            | Log in and obtain a token         | No   |
| GET    | `/email-check/`      | Check if an email exists (`?email=`) | Yes |

### Boards

| Method | Endpoint            | Description                          | Permission        |
| ------ | ------------------- | ------------------------------------ | ----------------- |
| GET    | `/boards/`          | List boards the user owns or joins   | Authenticated     |
| POST   | `/boards/`          | Create a board (creator = owner)     | Authenticated     |
| GET    | `/boards/{id}/`     | Board detail incl. members and tasks | Owner or member   |
| PATCH  | `/boards/{id}/`     | Update title / members               | Owner or member   |
| DELETE | `/boards/{id}/`     | Delete a board                       | Owner only        |

### Tasks

| Method | Endpoint                  | Description                       | Permission              |
| ------ | ------------------------- | --------------------------------- | ----------------------- |
| GET    | `/tasks/assigned-to-me/`  | Tasks where the user is assignee  | Authenticated           |
| GET    | `/tasks/reviewing/`       | Tasks where the user is reviewer  | Authenticated           |
| POST   | `/tasks/`                 | Create a task on a board          | Board member            |
| PATCH  | `/tasks/{id}/`            | Update a task (board is fixed)    | Board member            |
| DELETE | `/tasks/{id}/`            | Delete a task                     | Creator or board owner  |

### Comments

| Method | Endpoint                                | Description            | Permission     |
| ------ | --------------------------------------- | ---------------------- | -------------- |
| GET    | `/tasks/{task_id}/comments/`            | List a task's comments | Board member   |
| POST   | `/tasks/{task_id}/comments/`            | Add a comment          | Board member   |
| DELETE | `/tasks/{task_id}/comments/{id}/`       | Delete a comment       | Author only    |

---

## Conventions & Notes

- **User model:** The project uses Django's built-in `User`. The full name is
  stored in `first_name`, and `username` is set to the user's email.
- **Task `status`:** one of `to-do`, `in-progress`, `review`, `done`.
- **Task `priority`:** one of `low`, `medium`, `high`.
- **User short object** (e.g. `assignee`, `reviewer`, board `members`):
  `{ "id", "email", "fullname" }`, or `null`.
- **Comment `author`** is returned as the author's full name (a string).
- **Field-name quirk:** board *list* and *detail (GET)* responses use
  `owner_id`, while the board *update (PATCH)* response uses `owner_data` and
  `members_data`.
- `assignee` and `reviewer` must be members of the task's board.
