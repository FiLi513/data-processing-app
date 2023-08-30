# Data Processing Application

This application reads JSON data from an AWS SQS Queue, masks sensitive data, and writes to a PostgreSQL database.

## Prerequisites

- Docker
- Docker Compose
- AWS CLI Local (`pip install awscli-local`)
- PostgreSQL Client (psql)

## Getting Started

1. Clone this repository to your local machine.
2. Set up the required dependencies as mentioned in the Prerequisites section.

## Configuration

1. AWS Credentials:
   - Configure AWS credentials for local testing using `aws configure` or environment variables.

2. Docker Compose:
   - Edit the `docker-compose.yml` file to suit your needs.

## Usage

1. Start the application:
docker-compose up
2. Read a message from the SQS Queue:
awslocal sqs receive-message --queue-url http://localhost:4566/000000000000/login-queue
3. Connect to the Postgres database and verify the table:
psql -d postgres -U postgres -p 5432 -h localhost -W
postgres=# select * from user_logins;
## Next Steps

This project has been designed to satisfy the exercise requirements within a limited timeframe. If more time were available, several enhancements could be considered:
- Implement error handling and retries for AWS service interactions.
- Add logging and monitoring to track application behavior.
- Include unit tests to ensure code reliability and correctness.
- Optimize database interactions for efficiency with larger datasets.
- Dockerize the application further for production deployment.

## Contributing

Contributions are welcome! If you find any issues or have improvements, feel free to submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

