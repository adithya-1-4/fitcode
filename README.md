Project: A Flask Web Application
Languages: HTML, CSS, Java Script, SQL, Python
Name of Project: FitCode

Inspiration:
Given the current climate due to Covid-19, people have been forced indoors. With
gyms closed in many parts of the world, people find it hard to find a way to expend
their energy. This is especially true in a country like India where it is extremely
hot in summer and people hardly feel like going outside for a walk or run.

Initially I started doing my own workouts at home when the lockdown started. But after sometime,
it became boring to try to come up with new workouts everyday. This happened when I was working on
the week 6 problem set. Then it occured to me that I could create a python program to output
a randomly ordered list of 12 exercises(20 minute workout), 3 from each of the categories: arms, legs, abs, cardio. I
used this for a while and then once a learnt web programming and flask, I realised that I could
turn my python program into a web application but one which is user friendly and adaptive to
the users requirements.

Features:
Register- Lets you register with username and password, along witha fitness level(beginner/intermediate/advanced),
stores all data in a SQL database. Checks all requirements for password and username.

Log In- Lets you login with username and password.

Timer: Provides the user with a user friendly timer so that user does not need to exit app for a timer.

Stopwatch: Provides user with a user friendly stopwatch, incase the user prefers a stopwatch over a timer.

History: Provides the user with access to workouts done in the past along with the date.

Change Level: This feature allows you to change your level of fitness to access more challenging workouts.

Log Out: User can log out to prevent others from using account or to log into a different account.

Working:
As soon as you login, you are taken to the home page, which has a button which lets you start
a workout.Click on it and you are taken to a page asking you how long you want your workout to be.After, you
enter this, there is page asking you what you want to work on using a checkbox form. The categories available are:
arms, legs, abs, and cardio. Once you submit this your workout is ready.
I have implemented an algorithm that will provide the user with a workout (according to categories selected) that
can be completed within the time limit and of appropriate difficulty.The algorithm accounts for breaks between
exercises and such.
The page that displays the workout also has a link to warmup page which provides the user with a list of warmuos from
which the user can choose.


Gif:


![Untitled](https://github.com/user-attachments/assets/74daf22e-eb15-4ae7-b5d0-72a00762196c)


