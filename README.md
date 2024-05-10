# File-Task 


# Django REST API Documentation

This Django REST API provides endpoints for user authentication, file upload, file view, and user status change.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/akborhossain/File-Task.git
    ```
2. Create and activate a virtual environment:

    ```bash
    # Create a virtual environment
    python -m venv venv

    # Activate the virtual environment (Windows)
    .\venv\Scripts\activate

    # Activate the virtual environment (Mac/Linux)
    source venv/bin/activate
    ```
3. Navigate to the project directory:

    ```bash
    cd File-Task
    ```

4. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Configuration

1. Set up the database:

    I've configured the project to use SQLite database, so there's no need for additional setup. However, if you prefer to use a different database, you can modify the database settings in `settings.py` accordingly.

2. Perform migrations:
   If you've changed the database settings or models, you'll need to perform migrations using the following command:
    ```bash
    python manage.py migrate
    ```

3. Create a superuser for admin access:
    In the attached database, the superuser username is 'a' and the password is 'a'. You can create a new superuser or use this one for administrative tasks.
    ```bash
    python manage.py createsuperuser
    ```

4. Run the development server:

    ```bash
    python manage.py runserver
    ```

The API will be available at `http://localhost:8000/` or `http://127.0.0.1:8000/`.

## Endpoints

### User Registration

- Endpoint: `/signup/`
- Method: `POST`
- Description: Register a new user.
- Request Body:
    ```json
    {
        "username": "example_user",
        "email": "example@example.com",
        "password": "example_password"
    }
    ```
- Response:
    ```json
    {
        "message": "User registered successfully",
        "status": 201,
        "success": true
    }
    ```

### User Login

- Endpoint: `/login/`
- Method: `POST`
- Description: Authenticate user and provide access token.
- Request Body:
    ```json
    {
        "username": "example_user",
        "password": "example_password"
    }
    ```
- Response:
    ```json
    {
        "message": "Login successful",
        "access": "<access_token>"
    }
    ```

### File Upload API Endpoints

### 1. Create a New File

- **Endpoint:** `/file_up/`
- **Method:** `POST`
- **Description:** Upload a new file. Staff and Super user can create or upload file.
- **Request Body:** 
  - `title` : Title of the file.
  - `description` : Description of the file.
  - `uploaded_files`: The file to be uploaded.
- **Authorization:** Required (JWT token in header).
- **Response:** Details of the uploaded file.

### 2. Get List of Files

- **Endpoint:** `/file_up/`
- **Method:** `GET`
- **Description:** Retrieve a list of all files.
- **Parameters:**
  - `page` : Page number for pagination.
  - `limit` : Limit per page.
  - `created_by` (optional): created_by=True for get current user files.
- **Authorization:** Required (JWT token in header).
- **Response:** List of files with pagination details.

### 3. Get File Details

- **Endpoint:** `/file_up/<int:pk>/`
- **Method:** `GET`
- **Description:** Retrieve details of a specific file.
- **Parameters:** 
  - `pk`: ID of the file.
- **Authorization:** Required (JWT token in header).
- **Response:** Details of the specified file.

### 4. Update File Details

- **Endpoint:** `/file_up/<int:pk>/`
- **Method:** `PUT`
- **Description:** Update details of a specific file. Staff and Superuser can update the file info.
- **Parameters:** 
  - `pk`: ID of the file.
- **Request Body:** 
  - `title` (optional): Updated title of the file.
  - `description` (optional): Updated description of the file.
  - `uploaded_files` (optional): Updated file.
- **Authorization:** Required (JWT token in header).
- **Response:** Updated details of the specified file.

### 5. Delete a File

- **Endpoint:** `/file_up/<int:pk>/`
- **Method:** `DELETE`
- **Description:** Delete a specific file. Only super user can delete.
- **Parameters:** 
  - `pk`: ID of the file.
- **Authorization:** Required (JWT token in header).
- **Response:** Success message if the file is deleted successfully.

#### 6. Get List of Files by Anonymous User

- **Endpoint:** `/public_view/`
- **Method:** `GET`
- **Description:** Retrieve a list of all files.
- **Parameters:**
  - `page` (optional): Page number for pagination.
  - `limit` (optional): Limit per page.
- **Authorization:** Not required.
- **Response:** List of files with pagination details.

### 7. Get List of Files Details by Anonymous User

- **Endpoint:** `/public_view/<int:pk>/`
- **Method:** `GET`
- **Description:** Retrieve details of a specific file.
- **Parameters:** 
  - `pk`: ID of the file.
- **Authorization:** Not required.
- **Response:** Details of the specified file.

### User Status Change

- Endpoint: `/status_change/<int:pk>`
- Method: `PUT`
- Description: Change user status (staff or superuser). Staff can change any user staff status and super user can change any status.
- Parameters:
    - `pk`: User ID
- Request Body:
    ```json
    {
        "is_staff": true,
        "is_superuser": true
    }
    ```
- Authorization: JWT Token in header.
- Response: Updated user status.

## Authentication and Access Control

## Authentication

Authentication in this project is handled using JSON Web Tokens (JWT). When a user logs in or authenticates, they receive a JWT token which they can include in the headers of subsequent requests to authenticate themselves.

Example: Authorization: Bearer <access_token>


### Access Control

There are many way for access control (custom class permissions). Access control is managed using Django's default User model and its built-in permissions system. There are three types of users:

1. **Active User**: A regular user account. These users have basic access and permissions in the system. These user can only read permisions in this project.

2. **Staff User**: Staff users have additional permissions compared to regular users. They can perform certain administrative tasks. These users can read , write and update permisions in this project.

3. **Superuser**: Superusers have full control and access to the system. They can perform administrative tasks and have access to all features.
