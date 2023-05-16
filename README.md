# Django Kafka (API's Service)
This project focuses on Kafka Integration which communicate with other microservice using event based communication.


## Tools and Technologies
        PostgresSQL
        Python3
        Django==3.24
        DRF
        Kafka


## Running the Project

To run the project, follow these steps:

1. Set up a virtual environment using the command: `python -m venv venv`
2. Activate the virtual environment.
3. Install the required packages by running: `pip install -r requirement.txt`
4. Migrate Database Schema: `python manage.py migrate`
5. Start the Django development server: `python manage.py runserver`
6. Access the website in your browser at: `http://localhost:8000/`


## Directory structure
    .
    |
    |-- common
    |-- djangokafka
    |   |-- settings
    |   |-- urls
    |-- common
    |   |-- urls
    |   |-- models
    |   |-- views
    |-- static
    |-- env-example
    |-- requirement.txt
    |-- manage.py

## Contributing

If you'd like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature: `git checkout -b feature-name`
3. Make your changes and commit them: `git commit -am 'Add some feature'`
4. Push the branch to your forked repository: `git push origin feature-name`
5. Open a pull request on GitHub.

Please ensure that your code follows the project's coding conventions and includes appropriate tests.