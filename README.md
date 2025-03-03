# :seedling: Django Blog Project

## Overview

 This is a simple blog application developed using Django, designed to allow users to create, read, update, and delete posts. The application also supports user authentication, profile management, and commenting on posts. 

## Features

:one: **Home Page**: Displays the main index of the blog.

:two: **Post List**: View all blog posts and filter by category.

:three: **Post Detail**: View details of individual posts.
  
:four: **Create Post**: Functionality for authenticated users to create new blog posts.

:five: **Commenting System**: Users can comment on individual posts.

:six: **User Profiles**: Users can manage their profiles and edit their posts.

:seven: **Authentication**: User registration, login, logout, and password management features.

:eight: **Search Functionality**: Search for posts by keywords.

## URL Patterns

The application includes the following URL patterns:

- : Show the index page.
- `/posts/`: List all blog posts.
- `/posts/<category>/`: List posts filtered by a specific category.
- `/posts/detail/<pk>/`: Show the detail of a specific post by primary key (pk).
- `/tickets/`: View the tickets (if applicable).
- `/posts/<post_id>/comment/`: Add a comment to a specific post.
- `/create_post/`: Create a new post (requires authentication).
- `/search/`: Search for posts based on user input.
- `/profile/`: View user profile.
- `/profile/edit_post/<post_id>/`: Edit a specific post.
- `/profile/delete_post/<post_id>/`: Delete a specific post.
- `/profile/delete_image/<image_id>/`: Delete an image from the profile.
- `/login/`: User login page.
- `/logout/`: User logout functionality.
- `/password_change/`: Change the user's password.
- `/password_change/done/`: Confirmation page after password change.
- `/password_reset/`: Request a password reset.
- `/password_reset/done/`: Confirmation page after password reset request.
- `/password_reset/confirm/<uidb64>/<token>/`: Confirm the password reset.
- `/password_reset/complete/`: Completion page after password reset.
- `/register/`: User registration page.
- `/edit_account/`: Edit user account details.

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/yourproject.git
    cd yourproject
    ```

2. **Create a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Apply migrations**:
    ```bash
    python manage.py migrate
    ```

5. **Create a superuser** (optional):
    ```bash
    python manage.py createsuperuser
    ```

6. **Run the development server**:
    ```bash
    python manage.py runserver
    ```

7. **Access the application**: Open your web browser and navigate to `http://127.0.0.1:8000/`.

## Usage

- **User Registration**: Navigate to `/register/` to create a new account.
- **Login/Logout**: Users can log in at `/login/` and log out at `/logout/`.
- **Create and Manage Posts**: Authenticated users can create, edit, and delete posts from their profile page (`/profile/`).
- **Comment on Posts**: Visitors can leave comments on posts.
- **Search Posts**: Use the search functionality to find specific posts.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or report issues.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
