## docs/api.md

This file defines the API endpoints for the Streamlined Digital Library Backend MVP. It acts as the entry point for interacting with the library system via RESTful API calls.

### 1. File Purpose and Implementation Details:

- **Role:** This file serves as the core API interface for the backend system, exposing endpoints for various library operations.
- **Features:**
    - **Book Management:** 
        - Create new book entries (POST `/books`).
        - Retrieve book details (GET `/books/{book_id}`).
        - Update existing book entries (PUT `/books/{book_id}`).
        - Delete existing book entries (DELETE `/books/{book_id}`).
        - Search for books (GET `/books`) with optional query parameters (e.g., `title`, `author`, `isbn`).
    - **User Management:**
        - Register new users (POST `/users`).
        - Authenticate users (POST `/auth/token`).
        - Get current user information (GET `/users/me`).
        - Update user profiles (PUT `/users/me`).
        - Delete user accounts (DELETE `/users/me`).
- **Architectural Principles:**
    - **RESTful API Design:**  Follow RESTful principles for a consistent and predictable API structure.
    - **Dependency Injection:** Utilize FastAPI's dependency injection to decouple components and enhance testability.
- **User Stories:**
    - As a library staff member, I want to be able to add, edit, and remove books from the library catalog.
    - As a library patron, I want to search for books and view their details.
    - As a library user, I want to create an account and manage my profile information.
- **Pseudocode:**
    ```
    # Main API routes
    @app.post("/books")
    def create_book(book: BookCreate, db: Session = Depends(get_db), book_service: BookService = Depends()):
        # Validate book data
        # Create book in database using BookService
        # Return the created book

    @app.get("/books/{book_id}")
    def get_book_by_id(book_id: int, db: Session = Depends(get_db), book_service: BookService = Depends()):
        # Retrieve book from database using BookService
        # Return book details

    # Similar routes for update_book, delete_book, and search_books

    # User registration, login, and profile management routes 
    @app.post("/users")
    def register_user(user: UserCreate, db: Session = Depends(get_db), user_service: UserService = Depends()):
        # Validate user data
        # Register user using UserService
        # Return the created user

    @app.post("/auth/token")
    def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db), user_service: UserService = Depends()):
        # Authenticate user using UserService
        # Generate JWT token
        # Return the access token

    # Similar routes for get_current_user, update_user_profile, and delete_user
    ```
- **Performance Requirements:** 
    - Optimize for efficient data retrieval and response generation.
    - Consider caching mechanisms for frequently accessed data (e.g., popular books).
- **Inputs and Outputs:**
    - **Inputs:** API requests (POST, GET, PUT, DELETE) with appropriate data payloads.
    - **Outputs:**  API responses in JSON format, including:
        - Success status code (200, 201, 204) and data.
        - Error status code (400, 401, 403, 404, 500) and error message.

### 2. Required Dependencies and Import Statements:

- **Core Modules:**
    - `fastapi`: `from fastapi import FastAPI, HTTPException, Depends, APIRouter, status`
        - Version: `0.89.1` - Asynchronous web framework for building APIs.
    - `uvicorn`: `import uvicorn`
        - Version: `0.19.0` - ASGI server for running FastAPI applications.
    - `pydantic`: `from pydantic import BaseModel, validator`
        - Version: `1.10.4` - Data validation and parsing library.
    - `sqlalchemy`: `from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, ForeignKey`
        - Version: `1.4.43` - ORM for interacting with the PostgreSQL database.
    - `psycopg2`: `from sqlalchemy.ext.declarative import declarative_base`
        - Version: `2.9.6` - PostgreSQL adapter for SQLAlchemy.
- **Third-Party Packages:**
    - `python-multipart`: `from fastapi.responses import HTMLResponse, JSONResponse`
        - Version: `0.0.5` - File upload handling for FastAPI.
    - `jwt`: `from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm`
        - Version: `2.6.0` - JSON Web Token (JWT) library for authentication.
    - `passlib`: `from passlib.hash import bcrypt`
        - Version: `1.7.4` - Password hashing library for user security.
    - `alembic`: (Used for database migrations) - Not imported directly in this file.
    - `python-dotenv`: (Used for loading environment variables) - Not imported directly in this file.
    - `requests`: (Used for external API calls) - Not imported directly in this file. 
- **Internal Modules:**
    - `src.config.settings`: `from src.config.settings import settings`
        - Configuration settings for the application (e.g., database URL, secret key, logging levels).
    - `src.domain.books.models.book`: `from src.domain.books.models.book import Book`
        - Book data model.
    - `src.domain.users.models.user`: `from src.domain.users.models.user import User`
        - User data model.
    - `src.domain.books.repositories.book_repository`: `from src.domain.books.repositories.book_repository import BookRepository`
        - Book repository for database interactions.
    - `src.domain.users.repositories.user_repository`: `from src.domain.users.repositories.user_repository import UserRepository`
        - User repository for database interactions.
    - `src.domain.books.services.book_service`: `from src.domain.books.services.book_service import BookService`
        - Book service for business logic.
    - `src.domain.users.services.user_service`: `from src.domain.users.services.user_service import UserService`
        - User service for business logic.
    - `src.utils.exceptions`: `from src.utils.exceptions import AuthenticationError, UserNotFoundError, InvalidCredentialsError, BookNotFoundError, InvalidISBNError, DatabaseError`
        - Custom exceptions for error handling.
    - `src.utils.jwt_utils`: `from src.utils.jwt_utils import create_access_token, decode_token`
        - Utilities for JWT token operations.
    - `src.utils.logger`: `from src.utils.logger import Logger`
        - Logging utilities.
    - `src.infrastructure.api.dependencies.database`: `from src.infrastructure.api.dependencies.database import get_db`
        - Dependency injection for the SQLAlchemy database session. 
    - `src.infrastructure.api.dependencies.auth`: `from src.infrastructure.api.dependencies.auth import get_current_user, get_current_active_user`
        - Dependency injection for authentication middleware. 
- **Potential Conflicts:**  N/A

### 3. File Structure and Main Components:

```python
# src/infrastructure/api/v1/routes/books.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.domain.books.models.book import Book
from src.domain.books.services.book_service import BookService
from src.infrastructure.api.dependencies.database import get_db
from src.utils.exceptions import BookNotFoundError, InvalidISBNError

router = APIRouter(
    prefix="/books",
    tags=["Books"],
)

@router.post("/", response_model=Book, status_code=status.HTTP_201_CREATED)
async def create_book(book: BookCreate, db: Session = Depends(get_db), book_service: BookService = Depends()):
    """
    Creates a new book entry in the database.

    Args:
        book: Book object containing the new book data.
        db: SQLAlchemy database session.
        book_service: BookService instance for handling business logic.

    Returns:
        Book: The newly created book object.

    Raises:
        HTTPException: If an error occurs during book creation (e.g., invalid ISBN, duplicate book).
    """
    try:
        new_book = book_service.create_book(db, book)
        return new_book
    except InvalidISBNError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except HTTPException as e:
        raise e

@router.get("/", response_model=list[Book], status_code=status.HTTP_200_OK)
async def get_all_books(db: Session = Depends(get_db), book_service: BookService = Depends()):
    """
    Retrieves all books from the database.

    Args:
        db: SQLAlchemy database session.
        book_service: BookService instance for handling business logic.

    Returns:
        list[Book]: A list of all book objects.

    Raises:
        HTTPException: If an error occurs during book retrieval.
    """
    try:
        all_books = book_service.get_all_books(db)
        return all_books
    except HTTPException as e:
        raise e

@router.get("/{book_id}", response_model=Book, status_code=status.HTTP_200_OK)
async def get_book_by_id(book_id: int, db: Session = Depends(get_db), book_service: BookService = Depends()):
    """
    Retrieves a book by its ID.

    Args:
        book_id: The ID of the book to retrieve.
        db: SQLAlchemy database session.
        book_service: BookService instance for handling business logic.

    Returns:
        Book: The retrieved book object.

    Raises:
        HTTPException: If no book is found with the given ID or if an error occurs during retrieval.
    """
    try:
        book = book_service.get_book_by_id(db, book_id)
        return book
    except BookNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except HTTPException as e:
        raise e

@router.put("/{book_id}", response_model=Book, status_code=status.HTTP_200_OK)
async def update_book(book_id: int, book: BookUpdate, db: Session = Depends(get_db), book_service: BookService = Depends()):
    """
    Updates an existing book in the database.

    Args:
        book_id: The ID of the book to update.
        book: Book object containing the updated book data.
        db: SQLAlchemy database session.
        book_service: BookService instance for handling business logic.

    Returns:
        Book: The updated book object.

    Raises:
        HTTPException: If no book is found with the given ID or if an error occurs during update.
    """
    try:
        updated_book = book_service.update_book(db, book_id, book)
        return updated_book
    except BookNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except InvalidISBNError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except HTTPException as e:
        raise e

@router.delete("/{book_id}", response_model=bool, status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int, db: Session = Depends(get_db), book_service: BookService = Depends()):
    """
    Deletes a book from the database.

    Args:
        book_id: The ID of the book to delete.
        db: SQLAlchemy database session.
        book_service: BookService instance for handling business logic.

    Returns:
        bool: True if the book was deleted successfully, False otherwise.

    Raises:
        HTTPException: If no book is found with the given ID or if an error occurs during deletion.
    """
    try:
        deleted = book_service.delete_book(db, book_id)
        return deleted
    except BookNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except HTTPException as e:
        raise e

# Search Books Endpoint 
@router.get("/", response_model=list[Book], status_code=status.HTTP_200_OK)
async def search_books(
    title: str = None,
    author: str = None,
    isbn: str = None,
    db: Session = Depends(get_db),
    book_service: BookService = Depends(),
):
    """
    Searches for books based on title, author, or ISBN.

    Args:
        title: (Optional) Book title to search for.
        author: (Optional) Book author to search for.
        isbn: (Optional) Book ISBN to search for.
        db: SQLAlchemy database session.
        book_service: BookService instance for handling business logic.

    Returns:
        list[Book]: A list of matching books.

    Raises:
        HTTPException: If an error occurs during the search.
    """
    try:
        books = book_service.search_books(db, title=title, author=author, isbn=isbn)
        return books
    except HTTPException as e:
        raise e

# ... (User Authentication, Registration, Profile Management API Routes)

```

### 4. Data Management and State Handling:

- **Data Flow:** Data flows through a layered architecture.
    - **API Request:** Clients (e.g., web applications) send API requests to endpoints defined in this file.
    - **Controller:**  Routes delegate the requests to the `books_controller.py` or `users_controller.py` for processing.
    - **Service:** Controllers call methods in the `BookService` or `UserService` to perform business logic.
    - **Repository:** Services utilize repositories (`BookRepository`, `UserRepository`) to interact with the database.
    - **Database:** The PostgreSQL database stores and manages data, ensuring consistent data access across components.
    - **API Response:**  The controller generates responses based on the results and sends them back through the FastAPI routes to the client.
- **Local State:**  Minimal, primarily for caching or temporary data storage within functions or classes.
- **Caching:**  Not implemented in this file, but consider caching frequently accessed book data in a future iteration (e.g., using Redis or Memcached).
- **Shared State:** The database (PostgreSQL) acts as the central repository for shared state.
- **Data Validation and Sanitization:**
    - Validate all user input to prevent attacks like SQL injection and cross-site scripting (XSS).
    - Use Pydantic models to validate incoming API requests and ensure data integrity.
    - Sanitize user input using a library like `bleach` or implement custom sanitization logic.
    - Implement robust password hashing using `passlib` (version 1.7.4) for user passwords.

### 5. API Interactions and Network Requests:

- **Google Books API (External API - Not Implemented in this file):**
    - **Endpoint:**  [https://www.googleapis.com/books/v1/volumes](https://www.googleapis.com/books/v1/volumes)
    - **HTTP Method:** GET
    - **Request Payload:** Query parameters (e.g., `q`, `isbn`, `title`) to search for books.
    - **Response Scenarios:** 
        - **Success:**  Returns a JSON object containing book details (title, author, ISBN, cover image, etc.).
        - **Error:** Returns an HTTP error code and message (e.g., 404 Not Found, 400 Bad Request).
    - **Error Handling:** Implement error handling to catch HTTP errors (e.g., `requests.exceptions.RequestException`). 
        - Log error messages and details.
        - Return appropriate error responses to the client.
        - Implement retries (with exponential backoff) for transient network errors.
    - **Authentication:** Requires an API key (stored securely in the `.env` file). 
    - **Rate Limiting:** Implement rate limiting to prevent exceeding the API's usage limits.

### 6. Error Handling, Logging, and Debugging:

- **Error Handling:**
    - **Error Types:** 
        - `InvalidISBNError`:  Raised when an invalid ISBN format is provided.
        - `BookNotFoundError`: Raised when a book is not found.
        - `UserNotFoundError`:  Raised when a user is not found.
        - `InvalidCredentialsError`:  Raised when the provided credentials are incorrect.
        - `DatabaseError`:  Raised when a database error occurs.
    - **Error Messages and Codes:**
        - Use descriptive error messages and appropriate HTTP status codes for API responses (e.g., 400 Bad Request, 401 Unauthorized, 404 Not Found, 500 Internal Server Error).
    - **Error Handling:**
        - **Logging:** Log all errors (using the `Logger` class from `src/utils/logger.py`) to capture error details for debugging and monitoring. 
        - **API Responses:** Return appropriate error responses (including HTTP status codes) to the client.
- **Logging:**
    - **Information:** Log the following information for debugging and monitoring:
        - Timestamp
        - Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        - Module name (e.g., `src.infrastructure.api.v1.routes.books`)
        - Error messages and stack traces
        - API request details (method, endpoint, request payload)
    - **Sensitive Data:**  
        - Avoid logging sensitive information directly in logs (e.g., passwords, API keys).
        - Use string masking or redacting to protect sensitive data.
- **Debugging:**
    - **Debug Flags:** Use environment variables (e.g., `DEBUG=True` in the `.env` file) to enable or disable debug logging.
    - **Console Outputs:**  Use `print` statements or logging at the `DEBUG` level to output helpful debugging information.

### 7. Performance Optimization Techniques:

- **Potential Bottlenecks:**
    - **Database Queries:** Inefficient database queries can significantly impact performance.
    - **API Requests:**  Excessive API requests (especially if not rate-limited) can lead to performance issues.
- **Optimization Strategies:**
    - **Database Query Optimization:** 
        - **Indexes:** Create indexes on frequently queried fields (e.g., `isbn`, `title`, `author`) in the PostgreSQL database.
        - **Prepared Statements:**  Use prepared statements with SQLAlchemy to improve query efficiency.
        - **Query Optimization Techniques:** Analyze query plans to identify areas for improvement.
    - **API Request Optimization:**
        - **Rate Limiting:** Implement rate limiting to prevent exceeding the API's usage limits.
        - **Caching:** Cache API responses to reduce the number of requests (e.g., using `cachetools` or `Redis`).
- **Performance Benchmarks and Metrics:**
    - Measure API request latency and database query execution time.

### 8. Security Measures and Data Protection:

- **Security Considerations:**
    - **Authentication:**  Protect sensitive endpoints with JWT authentication (using the `jwt` library) and secure key management (using the `.env` file).
    - **Authorization:** Use role-based access control (e.g., `staff` and `patron` roles) to restrict access to specific resources.
    - **Input Validation:** Validate all user input using Pydantic models to prevent attacks like SQL injection and cross-site scripting (XSS).
    - **Data Sanitization:**  Sanitize user input using a library like `bleach` or implement custom sanitization logic to remove potentially malicious content.
    - **Password Hashing:**  Implement robust password hashing using `passlib` (version 1.7.4) for user passwords.
- **Input Validation and Sanitization:**
    - **Book Data:** 
        - **ISBN:** Validate ISBN format using a regex or a dedicated library (e.g., `isbnlib`).
        - **Title, Author, Description:**  Sanitize text fields using a library like `bleach` or implement custom sanitization logic.
    - **User Data:**
        - **Username:**  Validate username format.
        - **Email:**  Validate email address format.
        - **Password:**  Ensure the password meets minimum length and complexity requirements.
        - **Sanitization:**  Sanitize all user-provided text fields using `bleach` or a similar library.
- **Data Encryption and Hashing:**
    - **Passwords:**  Hash passwords securely using `passlib` (version 1.7.4) with a strong algorithm (e.g., `bcrypt`).

### 9. Integration with Other MVP Components:

- **Interacting Components:**
    - `src/infrastructure/api/main.py`:  The FastAPI application instance.
    - `src/domain/books/models/book.py`:  Book data model.
    - `src/domain/users/models/user.py`: User data model.
    - `src/domain/books/repositories/book_repository.py`: Book repository for database interactions.
    - `src/domain/users/repositories/user_repository.py`: User repository for database interactions.
    - `src/domain/books/services/book_service.py`: Book service for business logic.
    - `src/domain/users/services/user_service.py`: User service for business logic.
    - `src/utils/exceptions.py`:  Custom exceptions for error handling.
    - `src/utils/jwt_utils.py`: Utilities for JWT token operations.
    - `src/infrastructure/api/dependencies/database.py`:  Dependency injection for the database session.
    - `src/infrastructure/api/dependencies/auth.py`:  Dependency injection for authentication middleware.
- **Interactions:**
    - **Data Flow:** Data flows through a layered architecture.
    - **Control Flow:** 
        - This file defines routes that delegate requests to controllers.
        - Controllers call services, which in turn use repositories to interact with the database. 
    - **Shared Resources:** 
        - The database (PostgreSQL) is a shared resource.
        - The SQLAlchemy engine (created in `src/infrastructure/database/engine.py`) is shared for database connections.
    - **Global State:**  Global state (e.g., configuration settings) is managed through environment variables (`src/config/settings.py`) and potentially through a global configuration object.
- **Loose Coupling:** 
    - Utilize interfaces or abstract classes to decouple components, promoting modularity and flexibility.
    - Employ dependency injection to inject dependencies dynamically, improving testability and reducing tight coupling.

### 10. Scalability and Future-Proofing:

- **Scalability Considerations:**
    - **Horizontal Scaling:**  Consider using a load balancer to distribute traffic across multiple instances of the application. 
    - **Database Scaling:** Utilize PostgreSQL's scaling features (e.g., replication, read replicas) to handle increasing data volumes.
    - **Caching:**  Implement caching for frequently accessed data (e.g., popular books) to improve performance.
- **Extensible Code:**
    - **Interfaces and Abstract Classes:**  Define interfaces or abstract classes to create clear contracts for different components, enabling easier extension.
    - **Strategy Pattern:** Implement the Strategy pattern to swap out algorithms or behaviors for specific functionalities, allowing for easy customization.
    - **Dependency Injection:** Employ dependency injection to inject dependencies dynamically. 
- **Configuration Options:**  Use environment variables (e.g., `DATABASE_URL`, `SECRET_KEY`) in the `.env` file to configure settings that can vary across different environments.
- **Future Features:**
    - **E-book Lending:**  Add API endpoints for managing e-book loans.
    - **Personalized Recommendations:**  Implement API endpoints for retrieving personalized book recommendations.
    - **Advanced Search:** Add API endpoints for supporting more complex search filters.

### 11. Monorepo-Specific Integration:

- **Monorepo Structure:**  This file is located in the `src/infrastructure/api/v1/routes` directory within the monorepo structure.
- **Workspace-Specific Configurations:**  Not applicable, as the project is not using a monorepo structure.
- **Shared Libraries and Components:** 
    - Import modules like `src.domain.books.models.book`, `src.domain.users.models.user`, `src.domain.books.repositories.book_repository`, `src.domain.users.repositories.user_repository`, `src.domain.books.services.book_service`, `src.domain.users.services.user_service`, `src.utils.exceptions`, `src.utils.jwt_utils`, `src.infrastructure.api.dependencies.database`, `src.infrastructure.api.dependencies/auth` for seamless integration with other parts of the application.

### 12. Cross-Package Communication and Data Flow:

- **Cross-Package Interactions:** 
    - Interactions occur between this file and other packages within the application, primarily through data flow (e.g., passing book or user data) and control flow (e.g., calling functions in services).
- **Cross-Package APIs:**  Not applicable.
- **Shared State Management:** Not applicable.

### 13. Testing and Quality Assurance:

- **Unit Tests:** 
    - Create unit tests for individual functions and methods in this file. 
    - Test cases should include valid inputs, invalid inputs, edge cases, and error scenarios. 
    - Use the `pytest` framework for writing tests.
- **Integration Tests:** 
    - Test all API endpoints to ensure they are correctly integrated and handle requests and responses.
    -  Use the `TestClient` from the `fastapi.testclient` library to interact with the API endpoints for integration testing.
    - Use mocking libraries (e.g., `unittest.mock`) to mock dependencies or external services for testing. 
- **Performance and Load Tests:**
    - Conduct performance and load testing using tools like `Locust` or `JMeter` to simulate high user loads.
    -  Measure performance metrics (e.g., request latency, database query time) to identify potential bottlenecks.
- **Code Coverage:** 
    - Use code coverage tools (e.g., `coverage`) to track the percentage of code covered by tests.
    -  Aim for high code coverage (ideally 80% or higher) to ensure that most of the codebase is thoroughly tested.
- **Linting and Code Formatting:**
    - Use the `flake8` linter to enforce code style and identify potential code quality issues.
    -  Use a code formatter (e.g., `black`) to automatically format code for consistency.
- **Documentation:**
    - Add clear and concise comments to explain complex logic and design decisions.
    -  Use docstrings to provide a detailed description of each class, function, and method. 
    -  Generate comprehensive API documentation using tools like Swagger or Postman.

### 15. API/Route Specific Instructions:

**Book Management:**

- **Create Book (POST `/books`)**
    - **Request Body:** 
        ```json
        {
          "title": "The Hitchhiker's Guide to the Galaxy",
          "author": "Douglas Adams",
          "isbn": "9780345391803",
          "description": "A humorous science fiction novel...",
          "publication_date": "1979-10-12",
          "language": "English",
          "genre": "Science Fiction",
          "cover_image": "https://example.com/cover.jpg"
        }
        ```
    - **Response (Success):**
        ```json
        {
          "id": 1,
          "title": "The Hitchhiker's Guide to the Galaxy",
          "author": "Douglas Adams",
          "isbn": "9780345391803",
          "description": "A humorous science fiction novel...",
          "publication_date": "1979-10-12",
          "language": "English",
          "genre": "Science Fiction",
          "cover_image": "https://example.com/cover.jpg"
        }
        ```
    - **Response (Error):**
        - **Invalid ISBN:**  Status code 400, Error message: "Invalid ISBN format".
        - **Duplicate Book:** Status code 400, Error message: "Book with this ISBN already exists".
    - **Validation:**
        - Validate the `isbn` field using a regex or a dedicated library.
        - Ensure the `title` and `author` fields are not empty.
    - **Authentication:**  Requires authentication (JWT token).
    - **Logging:**  Log the request and response, including the book data.
    - **Caching:** Not implemented in this file.
- **Get Book by ID (GET `/books/{book_id}`)**
    - **Request Parameters:** `book_id` (integer)
    - **Response (Success):**  
        ```json
        {
          "id": 1,
          "title": "The Hitchhiker's Guide to the Galaxy",
          "author": "Douglas Adams",
          "isbn": "9780345391803",
          "description": "A humorous science fiction novel...",
          "publication_date": "1979-10-12",
          "language": "English",
          "genre": "Science Fiction",
          "cover_image": "https://example.com/cover.jpg"
        }
        ```
    - **Response (Error):**
        - **Book Not Found:**  Status code 404, Error message: "Book with ID {book_id} not found".
    - **Validation:**  N/A
    - **Authentication:** Requires authentication (JWT token).
    - **Logging:**  Log the request and response, including the book ID and retrieved data.
    - **Caching:** Not implemented in this file. 
- **Update Book (PUT `/books/{book_id}`)**
    - **Request Parameters:** `book_id` (integer)
    - **Request Body:**  
        ```json
        {
          "title": "The Hitchhiker's Guide to the Galaxy",
          "author": "Douglas Adams",
          "isbn": "9780345391803",
          "description": "A humorous science fiction novel...",
          "publication_date": "1979-10-12",
          "language": "English",
          "genre": "Science Fiction",
          "cover_image": "https://example.com/cover.jpg"
        }
        ```
    - **Response (Success):** 
        ```json
        {
          "id": 1,
          "title": "The Hitchhiker's Guide to the Galaxy",
          "author": "Douglas Adams",
          "isbn": "9780345391803",
          "description": "A humorous science fiction novel...",
          "publication_date": "1979-10-12",
          "language": "English",
          "genre": "Science Fiction",
          "cover_image": "https://example.com/cover.jpg"
        }
        ```
    - **Response (Error):** 
        - **Book Not Found:**  Status code 404, Error message: "Book with ID {book_id} not found".
        - **Invalid ISBN:** Status code 400, Error message: "Invalid ISBN format".
    - **Validation:** 
        - Validate the `isbn` field using a regex or a dedicated library.
    - **Authentication:** Requires authentication (JWT token).
    - **Logging:** Log the request and response, including the book ID, updated data, and returned data.
    - **Caching:** Not implemented in this file.
- **Delete Book (DELETE `/books/{book_id}`)**
    - **Request Parameters:** `book_id` (integer)
    - **Response (Success):** Status code 204 (No Content).
    - **Response (Error):**
        - **Book Not Found:** Status code 404, Error message: "Book with ID {book_id} not found".
    - **Validation:** N/A
    - **Authentication:** Requires authentication (JWT token).
    - **Logging:** Log the request and response, including the book ID.
    - **Caching:** Not implemented in this file.

**Search Books (GET `/books`)**

- **Request Parameters:** 
    - `title`: (Optional) Search for books with this title.
    - `author`: (Optional) Search for books by this author.
    - `isbn`: (Optional) Search for books with this ISBN.
- **Response (Success):**
    ```json
    [
      {
        "id": 1,
        "title": "The Hitchhiker's Guide to the Galaxy",
        "author": "Douglas Adams",
        "isbn": "9780345391803",
        "description": "A humorous science fiction novel...",
        "publication_date": "1979-10-12",
        "language": "English",
        "genre": "Science Fiction",
        "cover_image": "https://example.com/cover.jpg"
      },
      {
        "id": 2,
        "title": "Pride and Prejudice",
        "author": "Jane Austen",
        "isbn": "9780141439518",
        "description": "A classic romantic novel...",
        "publication_date": "1813-01-28",
        "language": "English",
        "genre": "Romance",
        "cover_image": "https://example.com/cover.jpg"
      }
    ]
    ```
- **Response (Error):** 
    - **Error During Search:** Status code 500, Error message: "Error searching for books".
- **Validation:** N/A
- **Authentication:**  Requires authentication (JWT token).
- **Logging:** Log the request and response, including the search criteria and results.
- **Caching:**  Consider caching search results in a future iteration (e.g., using Redis).

**User Management:**

- **Register User (POST `/users`)**
    - **Request Body:**
        ```json
        {
          "username": "johndoe",
          "email": "johndoe@example.com",
          "password": "password123" 
        }
        ```
    - **Response (Success):**
        ```json
        {
          "id": 1,
          "username": "johndoe",