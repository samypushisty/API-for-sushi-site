# Sushi Shop Backend Application

## Overview

This backend application is developed for educational purposes for a sushi shop website. The backend is built using the FastAPI framework, with a PostgreSQL database for data storage.

## Features

- **FastAPI**: A modern, fast (high-performance) web framework for building APIs with Python 3.7+.
- **PostgreSQL**: A powerful open-source object-relational database system used for managing data.
- **SQLAlchemy**: A SQL toolkit and Object-Relational Mapping (ORM) system that facilitates database interactions and relationships between tables.

## Authentication

- Upon user login, a JSON Web Token (JWT) is generated and stored in cookies.
- The token contains all necessary information about the user and is used for authentication during all operations on the website.
- The token has an expiration time, after which it becomes invalid and is automatically removed.

## Database Structure

The application features a well-defined database schema with relationships managed through SQLAlchemy. This allows for efficient data handling and interactions between different tables.

## Usage

1. **Installation**:
   - Clone the repository.
   - Install the required dependencies using:
     ```bash
     pip install -r requirements.txt
     ```
   - Set up the PostgreSQL database and configure the connection settings.

2. **Running the Application**:
   - Start the FastAPI application using Uvicorn:
     ```bash
     uvicorn main:app --reload
     ```

3. **Accessing the API**:
   - The API can be accessed at `http://localhost:8000`.

## Conclusion

This backend application serves as a project for understanding RESTful API development with FastAPI and PostgreSQL, emphasizing user authentication and database management through SQLAlchemy.
