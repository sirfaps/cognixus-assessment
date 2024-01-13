# Backend API Project

This is a take-home project assessment given to me, where I need to create a TODO-list server where users can sign in using the GitHub platform, Add/Delete/List, and Mark tasks in the to-do list items.

In this project I am creating RESTful APIs using Python as the main language of choice, Flask as the framework, and docker to dockerize the whole project. 

## Directory Structure

- `/app`: Contains the main application code.
- `/database`: Contains the database file.

## Prerequisites
- Make sure your computer has Docker installed
- SQLite3 installed on your computer

## Setup Instructions
1. [Clone the repository and Setup](#clone-and-setup-the-system)
2. Set up environment variables [.env](#setup-env)
3. Login to the system just by clicking the "Login button on the screen"</br>
![login server](https://github.com/sirfaps/cognixus-assessment/assets/82250418/400d323a-faf8-477f-98b6-37e78ebc4a75)
4. [Setup session's cookies for cmd to work](#setup-session-cookies-for-cmd-api-calls)

## Clone and setup the system
1. In your IDE, go to terminal and type in `git clone https://github.com/sirfaps/cognixus-assessment.git` to clone this code repository</br> 
And then go to the root folder of the project </br>
![Screenshot_3](https://github.com/sirfaps/cognixus-assessment/assets/82250418/7f1b7002-252a-40d5-b6ca-abf3a282371c)
>[!WARNING]
> Besure to have docker install on the system or else this step will fail

2. Next, type `docker-compose build` into the terminal and docker should start processing </br>
![image](https://github.com/sirfaps/cognixus-assessment/assets/82250418/0587fe3d-87da-4a3f-b7b8-0e18bda36755)

3. To start the server just simply type in `docker-compose up` into the terminal and it should start
![image](https://github.com/sirfaps/cognixus-assessment/assets/82250418/e3312504-756b-4c30-a1f0-c4ae982cdc4a)

4. To stop service, besure to just key into your keyboard with a combination in the following `Ctrl + C`

## Setup .env

1. Login to your Github account, and go to the settings.</br>
![Account Settings](https://github.com/sirfaps/cognixus-assessment/assets/82250418/53f2c894-b3ca-4154-bad7-5c199ddde4ce)
2. Scroll down and find "Developer settings"</br>
![developer settings](https://github.com/sirfaps/cognixus-assessment/assets/82250418/6e30441d-2dc8-4ea8-8cc3-a131822dbe39)
3. Go to Oauth Apps and then click on New OAuth App to create a new OAuth App client.</br>
![Screenshot_1](https://github.com/sirfaps/cognixus-assessment/assets/82250418/1eec9ba9-399a-4a9e-9694-dab0c93f786b)
4. Enter the Application name according to your liking. But for Homepage and Authorization callback URL, please fill in accordingly just in the picture provided. And then click on "Register application" below</br>
![create oauth application](https://github.com/sirfaps/cognixus-assessment/assets/82250418/ee6c05df-7cce-4cd2-bf33-51d4ee19c13a)
5. Click on "Generate a new client secret button" and then copy both Client ID and Client secrets ID on your side.</br>
![test](https://github.com/sirfaps/cognixus-assessment/assets/82250418/09a95038-79b8-4b06-85e4-282c8990562f)
6. And then be sure to scroll down and update the application!</br>
![update application](https://github.com/sirfaps/cognixus-assessment/assets/82250418/082f8edc-7735-4e5d-baf6-701276290458)
7. Taking those two IDs you have just copied, please paste it into the following variables in .env file!</br>
![Screenshot_2](https://github.com/sirfaps/cognixus-assessment/assets/82250418/09b7d6d0-f345-487e-a617-7cc338503c40)

## Setup Session Cookies for CMD API Calls
1. On your keyboard, press F12, go find "Application" as highlighted > Navigate to Cookies > Select session and copy the value below "Cookie Value"</br>
![copy the session cookie](https://github.com/sirfaps/cognixus-assessment/assets/82250418/8845b55b-9750-472d-8329-51b611363404)
3. Once the value is copied, head to cookies.txt in the root folder of the project and replace the box with the value. 
> [!WARNING]
> PLEASE SURE TO SAVE THE FILE!!!

</br>

![cookie session](https://github.com/sirfaps/cognixus-assessment/assets/82250418/dad3b971-f0f1-4e73-9da7-39ccc64dec51)
</br>
![session](https://github.com/sirfaps/cognixus-assessment/assets/82250418/c59fbe58-c11e-42c5-b507-ceb30bdb4377)
4. Now you can head to CMD to cURL call the APIs of the system.
> [!NOTE]
> The reason why you need to manually add in the session's value is because when you call other APIs, you need call using `curl` commands in the CMD. Because you cannot login the Github platform using the cmd (Only via browser) and, also the code has a added security that only users that are **LOGGED IN** are able to call those APIs. So saving that cookie essentially make it so that you can CMD to call APIs endpoint that need user authorization.

## Endpoints/API Documentation
- `/login`: Initiates GitHub login.
- `/tasks`: API endpoints for managing tasks.
  - GET: List all tasks based on the user.
  - POST: Add a new task.
  - DELETE: Delete tasks by status.
- `/tasks/complete`
  - PATCH(Mark as complete): Mark status as complete based on the task's ID
- `/tasks/edit`
  - PATCH(Edit Task): Change description and status based ont he task's ID

## APIs Instructions
1. Below is to call a API to **GET** all the tasks listed under the user
`curl -X GET http://localhost:5000/tasks --cookie cookies.txt`</br>
2. Below is to call to **CREATE** a task in the todo list
`curl -X POST http://localhost:5000/tasks -H "Content-Type: application/json" -d "{\"description\": \"Go to grocery\", \"status\": \"not yet started\"}" --cookie cookies.txt`</br>
3. Below is to **DELETE** data based on the status of the task
`curl -X DELETE http://localhost:5000/tasks -H "Content-Type: application/json" -d "{\"status\": \"completed\"}" --cookie cookies.txt`</br>
4. Below is to **PATCH** a data and mark it as complete based on the task's ID
`curl -X PATCH http://localhost:5000/tasks/complete -H "Content-Type: application/json" -d "{\"taskID\": \"5\"}" --cookie cookies.txt`</br>
5. Below is to **PATCH** a data and change its content(Description and status) based on the TaskID
`curl -X PATCH http://localhost:5000/tasks/edit -H "Content-Type: application/json" -d "{\"taskID\": \"5\", \"description\": \"Go to the gym\", \"status\": \"on going\"}" --cookie cookies.txt`</br>

> [!NOTE]
> The `--cookie cookies.txt` are the cookies needed to call the API's that need user authorization. If "Unauthorized" message pops up when calling APIs endpoint, it is maybe due to cookies.txt not set properly.
> [!TIP]
> If you're not sure how to read the json parameter, here are few examples:

`"{\"taskID\": \"5\", \"description\": \"Go to the gym\", \"status\": \"on going\"}"`
is equivalent to
```
{
    "taskID" : 5,
    "description": "Go to the gym",
    "status": "on going"
}
```

</br>

`"{\"description\": \"Go to grocery\", \"status\": \"not yet started\"}"`
is equivalent to
```
{
    "description": "Go to grocery",
    "status": "not yet started"
}
```

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

## Basic Instructions use SQLite3
1. Using CMD, cd into the database (rootfolder/database)
- ![image](https://github.com/sirfaps/cognixus-assessment/assets/82250418/5b20a940-d4d6-430c-80ab-b489b47c87b5)
2. type in `sqlite3` to initiate the SQLite3 database and typein `.open todo.db` to open the todo database
- ![image](https://github.com/sirfaps/cognixus-assessment/assets/82250418/251bb9be-d42d-4832-9d1b-6f9c88383e94)
3. You can also type in `.tables` or `.schema` to check if the database is fully loaded in
- ![image](https://github.com/sirfaps/cognixus-assessment/assets/82250418/53bac3bc-3d51-4f6f-8d5b-98894dd92f20)
4. With that, you can start using normal SQL syntax to check data on the tables

## Contributing Guidelines

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/new-feature`.
3. Make your changes.
4. Submit a pull request.

## Contact Information

For questions or issues, contact me at [brandonwcy2@gmail.com].
