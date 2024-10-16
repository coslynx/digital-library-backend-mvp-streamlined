## docs/deployment.md

This file provides comprehensive deployment instructions for the Streamlined Digital Library Backend MVP, ensuring a seamless and efficient deployment process.

### 1.  Prerequisites

**Environment:**

- Python 3.9+
- PostgreSQL 13+
- Docker 20.10+

**Dependencies:**

- Make sure you have installed all dependencies listed in the `requirements.txt` file using `pip install -r requirements.txt`.

**Configuration:**

- Create a `.env` file and configure environment variables based on your deployment environment. Refer to `.env.example` for guidance.

### 2. Database Setup

1. **Create Database:** Use the `scripts/create_database.py` script to create the PostgreSQL database.
2. **Create Tables:** Run the `scripts/create_tables.py` script to create the database tables based on the models defined in `src/infrastructure/database/models`.
3. **Seed Database (Optional):** Execute the `scripts/seed_database.py` script to populate the database with initial data for testing or demonstration purposes.

### 3. Containerization and Deployment

1. **Build Docker Image:** Construct the Docker image using the `Dockerfile` in the project root.
2. **Docker Compose Setup:** Use the provided `docker-compose.yml` file to define the multi-container setup, including the application container and the PostgreSQL database container.
3. **Run Docker Compose:**  Start the application and database containers using `docker-compose up -d`.
4. **Apply Database Migrations:** Execute the Alembic migrations command within the container to ensure the latest database schema is applied: `docker-compose exec app python src/infrastructure/database/migrations/alembic/upgrade head`

### 4. Running the Application

- The application will be accessible at http://localhost:8000 by default. 
- If you need to adjust the port, you can modify the `ports` section in `docker-compose.yml`.
- The Docker Compose configuration automatically connects the application container to the PostgreSQL database container for seamless data access.

### 5.  Deployment to Production

- **Heroku Deployment:** For deployment to Heroku, follow these steps:
    1. **Create Heroku App:** Create a new Heroku app using the Heroku CLI: `heroku create <app-name>`.
    2. **Set Environment Variables:**  Set environment variables using the Heroku CLI:
        ```bash
        heroku config:set DATABASE_URL=your_database_url
        heroku config:set SECRET_KEY=your_secret_key
        ```
    3. **Deploy to Heroku:**  Push your code to Heroku: `git push heroku main`.
    4. **Run Database Migrations on Heroku:**  Execute the Alembic migrations command on Heroku: `heroku run python src/infrastructure/database/migrations/alembic/upgrade head`.
- **AWS Lambda with Zappa:** To deploy using Zappa, refer to the Zappa documentation for detailed instructions.
    - [https://www.zappa.io/](https://www.zappa.io/)
    - The `src/infrastructure/api/main.py` file acts as the main entry point for the FastAPI application, which can be deployed directly to AWS Lambda using Zappa.

### 6.  Monitoring and Logging

- **Prometheus:** Configure Prometheus to collect metrics from the application.
- **Grafana:** Use Grafana to visualize Prometheus metrics and create custom dashboards.
- **AWS CloudWatch (for AWS Lambda deployments):**  Utilize CloudWatch to monitor Lambda function performance, logs, and metrics.
- **Logging:**  The `src/utils/logger.py` file implements the logging system for the application, providing comprehensive logging functionality.

### 7. Security Considerations

- **Environment Variables:**  Use a secure `.env` file to store sensitive environment variables (e.g., database credentials, API keys).
- **Password Hashing:** The `src/domain/users/models/user.py` file implements password hashing using `passlib` for secure password management.
- **JWT Token Handling:**  The `src/utils/jwt_utils.py` file implements JWT token generation and verification for authentication.
- **Database Security:** Utilize the security features of PostgreSQL to protect data.
- **HTTPS Encryption:**  Ensure the application is deployed behind HTTPS for secure communication.

### 8.  Extensibility and Future-Proofing

- **Modular Design:** The codebase follows a modular architectural pattern, making it easier to add new features, extend functionality, and maintain the application.
- **Dependency Injection:** Utilize dependency injection in the FastAPI application to enhance testability and flexibility.
- **Code Style and Documentation:** Adhere to established coding standards, naming conventions, and documentation practices for better maintainability.
- **Containerization:** The use of Docker containers provides a consistent and portable deployment environment, making it easier to adapt to different environments and platforms.

### 9.  Additional Deployment Resources

- **Docker Documentation:** [https://docs.docker.com/](https://docs.docker.com/)
- **Docker Compose Documentation:** [https://docs.docker.com/compose/](https://docs.docker.com/compose/)
- **Heroku Documentation:** [https://devcenter.heroku.com/](https://devcenter.heroku.com/)
- **Zappa Documentation:** [https://www.zappa.io/](https://www.zappa.io/)
- **AWS Lambda Documentation:** [https://aws.amazon.com/lambda/](https://aws.amazon.com/lambda/)

### 10.  Continuous Integration and Deployment (CI/CD)

- **GitHub Actions:** Implement CI/CD pipelines using GitHub Actions to automate testing and deployment.

### 11.  Feedback and Improvements

- Please provide any feedback on these deployment instructions to help improve the process.


```