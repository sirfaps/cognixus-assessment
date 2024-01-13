# Backend API Project

This is a take-home project assessment given to me, where I need to create a TODO-list server where users can sign in using the GitHub platform, Add/Delete/List, and Mark tasks in the to-do list items.

In this project I am creating RESTful APIs using Python as the main language of choice, Flask as the framework, and docker to dockerize the whole project. 

## Directory Structure

- `/app`: Contains the main application code.
- `/database`: Contains the database file.

## Prerequisites
- Make sure your computer has Docker installed

## Setup Instructions
1. Clone the repository.
2. Set up environment variables [.env]([https://github.com/sirfaps/cognixus-assessment/edit/main/README.md#prerequisites](https://github.com/sirfaps/cognixus-assessment/tree/main?tab=readme-ov-file#setup-env))
3. Login to the system just by click the "Login button on the screen"![login server](https://github.com/sirfaps/cognixus-assessment/assets/82250418/400d323a-faf8-477f-98b6-37e78ebc4a75)
5. Setup session's cookies for cmd to work

## Setup .env
1. Login to your Github account, and go to the settings.
- ![Account Settings](https://github.com/sirfaps/cognixus-assessment/assets/82250418/53f2c894-b3ca-4154-bad7-5c199ddde4ce)
2. Scroll down and find "Developer settings"
- ![developer settings](https://github.com/sirfaps/cognixus-assessment/assets/82250418/6e30441d-2dc8-4ea8-8cc3-a131822dbe39)
3. Go to Oauth Apps and then click on New OAuth App to create a new OAuth App client.
- ![Screenshot_1](https://github.com/sirfaps/cognixus-assessment/assets/82250418/1eec9ba9-399a-4a9e-9694-dab0c93f786b)
4. Enter the Application name according to your liking. But for Homepage and Authorization callback URL, please fill in accordingly just in the picture provided. And then click on "Register application" below
- ![create oauth application](https://github.com/sirfaps/cognixus-assessment/assets/82250418/ee6c05df-7cce-4cd2-bf33-51d4ee19c13a)
5. Click on "Generate a new client secret button" and then copy both Client ID and Client secrets ID on your side.
- ![test](https://github.com/sirfaps/cognixus-assessment/assets/82250418/09a95038-79b8-4b06-85e4-282c8990562f)
6. And then be sure to scroll down and update the application!
- ![update application](https://github.com/sirfaps/cognixus-assessment/assets/82250418/082f8edc-7735-4e5d-baf6-701276290458)
7. Taking those two IDs you have just copied, please paste it into the following variables in .env file!
- ![Screenshot_2](https://github.com/sirfaps/cognixus-assessment/assets/82250418/09b7d6d0-f345-487e-a617-7cc338503c40)

- Rename `.env.example` to `.env` and set the required variables.

## Setup session's cookies for CMD API Calls
1. On your keyboard, press F12, go find "Application" as highlighted > Navigate to Cookies > Select session and copy the value below "Cookie Value"
- ![copy the session cookie](https://github.com/sirfaps/cognixus-assessment/assets/82250418/8845b55b-9750-472d-8329-51b611363404)
3. Once the value is copied, head to cookies.txt in the root folder of the project and replace the box with the value. 
> [!WARNING]
> PLEASE SURE TO SAVE THE FILE!!!
- ![cookie session](https://github.com/sirfaps/cognixus-assessment/assets/82250418/dad3b971-f0f1-4e73-9da7-39ccc64dec51)
- ![session](https://github.com/sirfaps/cognixus-assessment/assets/82250418/c59fbe58-c11e-42c5-b507-ceb30bdb4377)
4. Now you can head to CMD to cURL call the APIs of the system.


## APIs Instructions
1. Below is to call a API to **GET** all the tasks listed under the user
`curl -X GET http://localhost:5000/tasks --cookie cookies.txt`
2. Below is to call to **CREATE** a task in the todo list
`curl -X POST http://localhost:5000/tasks -H "Content-Type: application/json" -d "{\"description\": \"Go to grocery\", \"status\": \"not yet started\"}" --cookie cookies.txt`
3. Below is to **DELETE** data based on the status of the task
`curl -X DELETE http://localhost:5000/tasks -H "Content-Type: application/json" -d "{\"status\": \"completed\"}" --cookie cookies.txt`
4. Below is to **PATCH** a data and mark it as complete based on the task's ID
`curl -X PATCH http://localhost:5000/tasks/complete -H "Content-Type: application/json" -d "{\"taskID\": \"5\"}" --cookie cookies.txt`
5. Below is to **PATCH** a data and change its content(Description and status) based on the TaskID
`curl -X PATCH http://localhost:5000/tasks/edit -H "Content-Type: application/json" -d "{\"taskID\": \"5\", \"description\": \"Go to the gym\", \"status\": \"on going\"}" --cookie cookies.txt`


## Endpoints/API Documentation

- `/login`: Initiates GitHub login.
- `/tasks`: API endpoints for managing tasks.
  - GET: List all tasks.
  - POST: Add a new task.
  - DELETE: Delete tasks by status.
  - ...

## Database Schema

- `tasks`: Table for storing task information.
- `users`: Table for storing user information.
The following are the schema database of the system:
```
CREATE TABLE tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        description TEXT,
        status TEXT DEFAULT 'pending',
        user_id TEXT,
        FOREIGN KEY(user_id) REFERENCES users(clientID)
    );
CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        userName TEXT,
        clientID TEXT UNIQUE  -- Ensures clientID is unique
    );
```
![schema visual](https://github.com/sirfaps/cognixus-assessment/assets/82250418/ce33eb51-9c2c-4d98-a4f7-3cc672107891)


## Contributing Guidelines

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/new-feature`.
3. Make your changes.
4. Submit a pull request.

## Contact Information

For questions or issues, contact me at [brandonwcy2@gmail.com].
