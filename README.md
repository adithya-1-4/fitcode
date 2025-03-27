# FitCode

A Flask Web Application for personalized home workouts.  
Languages: HTML, CSS, JavaScript, SQL, Python

## About

FitCode is a workout generation application that helps you create personalized workouts based on your fitness level and time availability. With gyms closed in many parts of the world due to COVID-19, FitCode provides a solution for maintaining fitness at home without equipment.

## Features

- **Register**: Create an account with username, password, and fitness level (beginner/intermediate/advanced)
- **Login**: Access your personalized workouts
- **Timer**: Track your workout intervals
- **Stopwatch**: Time your exercises
- **History**: View your past workouts
- **Change Level**: Adjust your fitness level as you progress
- **Workout Generator**: Generate customized workouts based on your preferences and time constraints

## How It Works

1. Log in to access the home page
2. Click "Let's Start Working Out" to begin
3. Enter how long you want your workout to be
4. Select which body areas you want to work on (arms, legs, abs, cardio)
5. Get a personalized workout based on your selections and fitness level
6. Use the built-in timer and stopwatch tools to track your workout

## Installation and Setup

1. Clone this repository:
   ```
   git clone <repository-url>
   cd fitcode
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Initialize the database:
   ```
   python init_db.py
   ```
   This step is crucial as it creates all the necessary tables and populates them with initial exercise data.

5. Run the application:
   ```
   python application.py
   ```

6. Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

7. Register a new account and start working out!

## Database Structure

- **users**: Stores user information including username, password hash, and fitness level
- **arms**, **legs**, **abs**, **cardio**: Tables containing exercise options for each category
- **workouts**: Stores user workout history with timestamps

## Technical Details

- Built with Flask web framework
- Uses SQLAlchemy for database management
- Styled with Bootstrap and custom CSS
- Uses JavaScript for timer and stopwatch functionality

## Troubleshooting

If you encounter database-related errors:
1. Delete the project.db file (if it exists)
2. Run `python init_db.py` to recreate the database
3. Restart the application

## Demo

![FitCode Demo](https://github.com/user-attachments/assets/74daf22e-eb15-4ae7-b5d0-72a00762196c)


