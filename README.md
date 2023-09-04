# Django Birthday Greeter - Docker Deployment

Django Birthday Greeter is a Django-based application that automatically sends birthday greetings to your customers at their local time of 11:59 PM, regardless of their specified timezones. This README guide will help you understand how to deploy it using Docker containers.

## Technologies Used

Django Birthday Greeter relies on a variety of technologies and tools, each serving a specific purpose in the project:

- **Django**: The core framework for building the web application. Django manages customer registration, data storage, and the web interface.

- **Docker**: Utilized for containerization, Docker simplifies deployment, ensuring consistent environments across various setups.

- **Celery**: Employed for asynchronous task processing, Celery is responsible for scheduling and sending birthday greetings at the appropriate times.

- **Redis**: Serves as the message broker for Celery, facilitating communication between the application and the task queue.

- **PostgreSQL**: Used as the database management system, PostgreSQL stores customer data, including names, birthdates, and timezones.

- **SMTP/Email Service**: Responsible for sending personalized birthday emails to customers, creating a delightful experience.

- **Django Rest Framework (DRF)**: DRF provides a robust toolkit for creating web APIs, enabling seamless interactions with the application via API endpoints.

- **Pytz**: Pytz aids in efficiently managing timezones, ensuring accurate scheduling and delivery of birthday greetings based on customer-specific timezones.

## Purpose

The purpose of Django Birthday Greeter is to ensure that all of your customers receive personalized birthday wishes at their local midnight, creating a memorable and delightful experience. The bot sends wishes based on each customer's local time, making it suitable for a global customer base.

## How It Works

### 1. Customer Registration

- Customers register on the platform and provide their name, birthdate, and timezone.

### 2. Docker Containers

- Django Birthday Greeter is deployed using Docker containers, which simplify management and scalability.

### 3. Scheduled Task

- A scheduled task is configured to run daily at 11:55 PM server time within a Docker container. One can change the time at settings.

### 4. Task Execution

- When the task runs, it queries the database for customers whose birthdays match the current date.

### 5. Sending Wishes

- Birthday wishes are sent to all eligible customers at their local time of 11:59 PM, based on their specified timezones.

## Deployment

To set up Django Birthday Greeter using Docker, follow these steps:

1. Clone the repository: `git clone https://github.com/omariut/django-birthday-greeter.git`
2. Navigate to the project directory: `cd django-birthday-greeter`

### Build Docker Images

3. Build the Docker images for the Django app and Celery worker:

    ```docker-compose build```

### Configure Environment Variables

4. Configure your environment variables by creating a `.env` file in the project root directory. You can use the provided `.env.example` as a template.

### Run Docker Containers

5. Start the Docker containers:
    
    ```docker-compose up -d```

### Database Initialization

6. Initialize the database and apply migrations:

    ```docker-compose exec <your-container-name> python manage.py migrate```

7. Access the Django Birthday Greeter application at its deployment URL.

## Usage

- Customers can register and provide their birthdate through API.
- Birthday emails will be sent to all eligible customers at their local time of 11:59 PM each day.


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

