# Bloggy API: A Interactive blog app

This repository contains the backend API for **Bloggy: An Interactive Blog Application**. The API is built using Django Rest Framework and integrates with Firebase for authentication and real-time data management.

## Features

- **Blog Management**: APIs to create, retrieve, update, and delete blog posts.
- **User Profile Management**: APIs to manage user profiles.
- **Follow/Following System**: APIs to handle follow/unfollow actions and retrieve followers and followees.
- **Blog Views Count**: Track and update the view count for each blog post.
- **Firebase Integration**:
- **Authentication**: Secure API endpoints using Firebase Authentication.
- **Realtime Database**: Sync data with Firebase Realtime Database.

## Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/dpshah23/Bloggy-API.git
    cd bloggy-api
    ```

2. **Create a Virtual Environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set Up Firebase**:
   - Install `pyrebase` or any other Firebase package you are using.
   - Configure Firebase by adding your Firebase credentials in the project settings.

5. **Apply Migrations**:
    ```bash
    python manage.py migrate
    ```

6. **Run the Server**:
    ```bash
    python manage.py runserver
    ```


## Usage

- **Authentication**: Ensure your requests are authenticated using Firebase tokens.
- **Blog Operations**: Use the provided endpoints to create, view, update, and delete blogs.
- **Profile Management**: Manage user profiles through the relevant API endpoints.
- **Follow/Unfollow**: Implement follow and unfollow functionality using the provided API.
