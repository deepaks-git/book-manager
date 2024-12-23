# Book Management API

This is a RESTful API for managing books and user authentication using Flask. The API supports operations such as adding, updating, deleting, and filtering books, along with user registration and login.

## Live Demo
[Visit the Live Project](https://book-manager-2hyx.onrender.com/apidocs)

## Project Overview
This project demonstrates the following features:
- User authentication using JWT.
- CRUD operations for managing books.
- API documentation using Flasgger.
- SQLite database integration.
- Deployment-ready setup for Render.

## Technologies Used
- **Flask**: Python web framework.
- **Flask-JWT-Extended**: For handling authentication.
- **Flask-SQLAlchemy**: ORM for database operations.
- **Flasgger**: Automatically generate Swagger UI documentation.
- **SQLite**: Lightweight database.
- **Gunicorn**: WSGI server for running the application in production.

## Installation and Setup

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd <repository_folder>
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the database:
   ```bash
   python
   >>> from app import db
   >>> db.create_all()
   >>> exit()
   ```

5. Run the application:
   ```bash
   python app.py
   ```

6. Access the application at `http://localhost:3000`.

## Deployment

### Render Deployment Steps

1. Ensure your project folder contains:
   - `app.py` (your Flask application).
   - `requirements.txt` (generated using `pip freeze > requirements.txt`).
   - `runtime.txt` (specify Python version, e.g., `python-3.9.12`).
   - `Procfile` (contains `web: gunicorn app:app`).
   - `finalBook.db` (your SQLite database).

2. Push the project to GitHub.

3. Follow these steps on Render:
   - Log in to [Render](https://render.com).
   - Create a new Web Service.
   - Connect your GitHub repository.
   - Set the build and start commands.
   - Deploy the service.

4. Access your deployed API via the Render-provided URL.

## Features

### User Authentication
- **Register**: `/register`
- **Login**: `/login`

### Book Management
- **Add Book**: `/addBook`
- **Update Book**: `/updateBook/<id>`
- **Delete Book**: `/deleteBook/<id>`
- **View Books**: `/showBooks`
- **Sort Books**: `/books/sort`
- **Filter Books**: `/books/filter`

### API Documentation
- Swagger UI is available at `/apidocs` for testing and exploring endpoints interactively.

## Topics
`Flask` `REST API` `JWT` `SQLite` `Flasgger` `Gunicorn` `Render` `Swagger UI` `Book Management` `Authentication` `Python` `CRUD Operations`

---

Feel free to contribute or raise issues in the repository!
