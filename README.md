# Telegram Shop Bot

Welcome to the Telegram Shop Bot! This bot serves as a virtual storefront on the Telegram platform, allowing users to browse and purchase items directly through the app.

## Getting Started

To get this bot up and running, follow these steps:

1. **Set up the environment**:
   - Rename the `env_dist` file to `.env`.
   - Fill in the `.env` file with your specific configurations such as the `BOT_TOKEN`, `DB_URL`, and other necessary parameters.

2. **Build and Run**:
   - Use Docker Compose to build and run the bot:
     ```sh
     docker-compose up -d
     ```

## File Structure Explanation

- `/.venv`: This directory holds the virtual environment where all the Python dependencies are installed.
  
- `/alembic`: A directory for Alembic, a lightweight database migration tool for usage with the SQLAlchemy Database Toolkit for Python.

- `/bot`: The main directory for the bot's source code.
  
  - `/db`: Contains SQLAlchemy models and database interaction layers.
    - `__init__.py`: Indicates that this directory is a Python package.
    - `base.py`: Base module for SQLAlchemy declarative base.
    - `database.py`: Contains the database session management and engine creation.
    - `models.py`: Defines the SQLAlchemy ORM models for your database tables.

  - `/handlers`: Telegram bot handlers for different types of updates.
    - `__init__.py`: Indicates that this directory is a Python package.
    - `callbacks.py`: Callback query handlers for inline button actions.
    - `commands.py`: Command handlers like `/start`, `/browse`, etc.

  - `/middlewares`: Middlewares to process updates before they reach handlers.
    - `__init__.py`: Indicates that this directory is a Python package.
    - `db.py`: Middleware for database session management in the context of web requests.

  - `__init__.py`: Indicates that this directory is a Python package.
  - `common.py`: Common utilities and helper functions.
  - `config_reader.py`: Configuration management to load environment variables.
  - `keyboards.py`: Keyboard layouts for Telegram's custom keyboards.
  - `ui_commands.py`: UI-related commands and bot interaction entry points.

- `/tests`: This directory should contain all of your test files. 
  - `test_models`.py: A test file specifically for testing your database models.

- `/venv`: Another virtual environment directory, possibly an artifact that should be checked if needed or removed.

- `/.gitignore`: The Git ignore file specifies intentionally untracked files to ignore.

- `/alembic.ini`: Configuration file for Alembic migrations.

- `/docker-compose.yml`: Docker Compose configuration to define and run multi-container Docker applications.

- `/Dockerfile`: Instructions for Docker to automatically build image configurations.

- `/env_dist`: A template for the environment variables file.

- `/test_env_dist`: A template for the test environment variables file.

- `/README.md`: The README file provides information about the bot and instructions on how to set it up.

- `/requirements.txt`: A list of Python package dependencies that the bot requires.

## Important Notes

- Remember to configure your `.env` file with the appropriate environment variables before starting the bot.
- Do not commit the `.env` file to your repository if it contains sensitive information. It should be added to your `.gitignore` file to prevent accidental exposure.
- For any changes or migrations needed to be done on the database, refer to the Alembic documentation and use the `alembic` command-line tool.

## Contributions

Contributions are welcome! If you have any suggestions or improvements, please feel free to fork the repository and submit a pull request.

Enjoy your Telegram Shop Bot!
