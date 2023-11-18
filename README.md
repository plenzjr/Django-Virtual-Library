# Virtual Library Project

![Tests](https://img.shields.io/github/actions/workflow/status/paulogil2010/Django-Virtual-Library/django-tests.yml?label=Tests)
![Contributors](https://img.shields.io/github/contributors/paulogil2010/Django-Virtual-Library?color=green)




## Description
Virtual Library is a Django-based web application designed to manage a digital library. It allows users to browse, review, and manage a collection of books, authors, and publishers.

## Features
- User authentication and registration.
- CRUD operations for managing books, authors, publishers, and book reviews.
- Advanced search and filtering capabilities.
- Integration with external APIs for fetching book and author details.
- Secure and scalable architecture.

## Technologies
- Django & Django Rest Framework
- PostgreSQL
- Docker & Docker Compose
- Pytest for testing
- GitHub Actions for CI/CD
- Swagger for API documentation

## Local Setup
To set up the Virtual Library on your local machine, follow these steps:

### Prerequisites
- Python 3.9
- Docker and Docker Compose
- Git (for cloning the repository)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/virtual-library.git
   cd virtual-library
   ```

2. Set up a virtual environment and activate it:

   ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies
   ```bash
    pip install -r requirements.txt
    ```

4. Run the Docker container for the PostgreSQL database
   ```bash
    docker-compose up -d
    ```

5. Apply the database migrations:

   ```bash
    python manage.py migrate
    ```

6. Load fixture into your database:
   ```bash
    python manage.py loaddata users
    python manage.py loaddata authors
    python manage.py loaddata publishers
    python manage.py loaddata categories
    python manage.py loaddata books
    python manage.py loaddata book_reviews
    ```



6. Start the Django development server:

   ```bash
    python manage.py runserver
    ```

7. The application should now be running at http://localhost:8000/

### Testing

Run the tests using Pytest:

```bash
pytest
```

### API Documentation

- Swagger UI for the API documentation at http://localhost:8000/swagger/
- Swagger Redoc for the API documentation at http://localhost:8000/redoc/

### Contributing

Contributions to Virtual Library are welcome. Please follow these steps to contribute:

1. Fork the repository.
2. Create a new feature branch (git checkout -b feature/your-feature).
3. Make your changes and commit (git commit -am 'Add some feature').
4. Push to the branch (git push origin feature/your-feature).
5. Open a pull request.

## Contact

- [LinkedIn](https://www.linkedin.com/in/plenzjr)
- [Email](mailto:paulogil2010@gmail.com)

### License
Distributed under the MIT License. See [LICENSE](LICENSE) for more information.
