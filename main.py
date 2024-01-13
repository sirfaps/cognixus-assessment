from flask import Flask, request, jsonify, redirect, url_for, session
import sqlite3
from flask_dance.contrib.github import make_github_blueprint, github
import os
from dotenv import load_dotenv
from auth_decorator import check_user_auth

# Allow to run on http
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

load_dotenv()
github_blueprint = make_github_blueprint(
    client_id=os.getenv('GITHUB_CLIENT_KEY'),
    client_secret=os.getenv('GITHUB_SECRET_KEY')
)

app.register_blueprint(github_blueprint, url_prefix='/github')

# Create tasks table (if not exists)
conn = sqlite3.connect('/app/database/todo.db')
cursor = conn.cursor()
cursor.executescript('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        description TEXT,
        status TEXT DEFAULT 'pending',
        user_id TEXT,
        FOREIGN KEY(user_id) REFERENCES users(clientID)
    );
    
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        userName TEXT,
        clientID TEXT UNIQUE  -- Ensures clientID is unique
    );
''')
conn.close()


@app.route('/login')
def github_login():
    if not github.authorized:
        return redirect(url_for('github.login'))
    return '<h1>Request failed!</h1>'


@app.route('/')
def welcome():
    if github.authorized:
        account_info = github.get('/user')
        account_info_json = account_info.json()

        user_id = os.getenv('GITHUB_SECRET_KEY')
        github_username = account_info_json.get('login')  # Fetch GitHub username

        # Establish a connection to the SQLite database
        conn = sqlite3.connect('/app/database/todo.db')
        cursor = conn.cursor()

        select_user_query = "SELECT * FROM users WHERE clientID = ?"
        cursor.execute(select_user_query, (user_id,))
        existing_user = cursor.fetchone()

        if existing_user is None:
            # If the user doesn't exist, insert the user into the users table
            insert_user_query = "INSERT INTO users (clientID, userName) VALUES (?, ?)"
            cursor.execute(insert_user_query, (user_id, github_username))
            conn.commit()
        else:
            # If the user exists, update the username
            update_user_query = "UPDATE users SET userName = ? WHERE clientID = ?"
            cursor.execute(update_user_query, (github_username, user_id))
            conn.commit()

        # Close the database connection
        conn.close()

        return 'Your Github name is {} <a href="{}"><button>List all the Tasks</button></a> or <a href="{}"><button>Logout</button></a>'.format(
            account_info_json['login'], url_for('get_task_endpoint'), url_for('github_logout'))
    else:
        return "Welcome! Please <a href='{}'><button>Login</button></a>".format(url_for('github.login'))


@app.route('/logout')
def github_logout():
    if github.authorized:
        try:
            # Clear the GitHub OAuth token from the session
            session.pop('github_oauth', None)

            # Clear other session data if needed
            # session.pop('other_data_key', None)

            # Clear the user session
            session.clear()

            # Successfully logged out
            return redirect(url_for('welcome'))  # Redirect to your homepage or login page
        except Exception as e:
            # Handling logout failure
            print(str(e))
            return "Logout failed due to an error."

    # Redirect to the login page if not logged in
    return redirect(url_for('github.login'))


@app.route('/tasks', methods=['GET'], endpoint='get_task_endpoint')
@check_user_auth
def list_all_tasks():
    try:
        # Extract user_id from .env
        user_id = os.getenv('GITHUB_SECRET_KEY')
        # Establish a connection to the SQLite database
        conn = sqlite3.connect('/app/database/todo.db')
        cursor = conn.cursor()

        # SQL SELECT command to retrieve tasks for a specific user_id
        # select_all_tasks = "SELECT * FROM tasks WHERE user_id = ?"        << this shows user's client_secret. which is confidential
        select_all_tasks = "SELECT id, description, status FROM tasks WHERE user_id = ?"

        # Execute the SQL command with the user_id parameter
        cursor.execute(select_all_tasks, (user_id,))  # Pass user_id as a tuple

        # Fetch all the rows returned by the query
        tasks = cursor.fetchall()

        # Close the database connection
        conn.close()

        # Return the retrieved tasks as JSON
        return jsonify({'tasks': tasks}), 200

    except Exception as e:
        # Handle exceptions and return an error message
        return jsonify({'error': str(e)}), 500


# Endpoint to add a new task
@app.route('/tasks', methods=['POST'], endpoint='add_task_endpoint')
@check_user_auth
def add_task():
    try:
        # Parse task details from the request body (JSON format)
        task_data = request.get_json()

        # Extract task details from the request
        task_description = task_data.get('description')
        status = task_data.get('status', 'pending')  # Default status is 'pending'
        user_id = os.getenv('GITHUB_SECRET_KEY')  # Replace with the actual user ID

        print(f"task_description: {task_description}")
        print(f"status: {status}")
        print(f"user_id: {user_id}")

        # SQL INSERT command to add a task
        insert_task_query = """
            INSERT INTO tasks (description, status, user_id)
            VALUES (?, ?, ?)
        """

        # Establish a connection to the SQLite database
        with sqlite3.connect('database/todo.db') as conn:
            cursor = conn.cursor()

            # Execute the SQL command with task details
            cursor.execute(insert_task_query, (task_description, status, user_id))

            # Get the ID of the last inserted row
            task_id = cursor.lastrowid

            # Commit changes to the database
            conn.commit()

            # Fetch the inserted task details
            select_task_query = """
                SELECT id, description, status, user_id
                FROM tasks
                WHERE id = ?
            """

            cursor.execute(select_task_query, (task_id,))
            inserted_task = cursor.fetchone()

        # Return the details of the inserted task in the response
        return jsonify({'message': 'Task added successfully', 'task': inserted_task}), 201

    except Exception as e:
        # Handle exceptions and return an error message
        return jsonify({'error': str(e)}), 500


# Endpoint to delete tasks by status
@app.route('/tasks', methods=['DELETE'], endpoint='del_task_endpoint')
@check_user_auth
def delete_tasks_by_status():
    try:
        # Establish a connection to the SQLite database
        conn = sqlite3.connect('/app/database/todo.db')
        cursor = conn.cursor()

        # Parse task details from the request body (JSON format)
        task_data = request.get_json()

        # Extract task status from the request body
        task_status = task_data.get('status')
        task_id = task_data.get('task_id')
        task_user = task_data.get('user_id')

        if task_status is not None:
            # SQL DELETE command to delete tasks by status
            delete_task_query = """
                DELETE FROM tasks WHERE status = ?
            """
            cursor.execute(delete_task_query, (task_status,))
        elif task_id is not None:
            # SQL DELETE command to delete tasks by task's ID
            delete_task_query = """
                DELETE FROM tasks WHERE id = ?
            """
            cursor.execute(delete_task_query, (task_id,))
        elif task_user is not None:
            # SQL DELETE command to delete tasks by user's ID
            delete_task_query = """
                DELETE FROM tasks WHERE user_id = ?
            """
            cursor.execute(delete_task_query, (task_user,))
        else:
            return jsonify({'error': "Please provide a status, user's ID or task's status"}), 400

        # Commit changes to the database
        conn.commit()

        # Close the database connection
        conn.close()

        # Return a success message
        return jsonify({'message': f'Tasks with status "{task_status}" deleted successfully'}), 200

    except Exception as e:
        # Handle exceptions, rollback changes, and return an error message
        if 'conn' in locals():
            conn.rollback()
            conn.close()
        return jsonify({'error': str(e)}), 500


@app.route('/tasks/complete', methods=['PATCH'], endpoint='comp_task_endpoint')
@check_user_auth
def mark_task_as_completed():
    try:
        task_data = request.get_json()
        taskID = task_data.get('taskID')

        if taskID is None:
            return jsonify({'error': 'TaskID is missing in the request payload'}), 400

        # Establish a connection to the SQLite database
        conn = sqlite3.connect('/app/database/todo.db')
        cursor = conn.cursor()

        # SQL UPDATE command to mark a task as completed
        update_task_query = """
            UPDATE tasks SET status = ? WHERE id = ?
        """

        # Execute the SQL command with the new status and task ID
        cursor.execute(update_task_query, ('completed', taskID))

        # Commit changes to the database
        conn.commit()

        # Close the database connection
        conn.close()

        # Return a success message
        return jsonify({'message': f'Task {taskID} marked as completed'}), 200

    except Exception as e:
        # Handle exceptions, rollback changes, and return an error message
        if 'conn' in locals():
            conn.rollback()
            conn.close()
        return jsonify({'error': str(e)}), 500


@app.route('/tasks/edit', methods=['PATCH'], endpoint='edit_task_endpoint')
@check_user_auth
def change_task_data():
    try:
        task_data = request.get_json()
        taskID = task_data.get('taskID')
        taskDesc = task_data.get('description')
        taskStatus = task_data.get('status')

        if taskID is None:
            return jsonify({'error': 'TaskID is missing in the request payload'}), 400

        # Establish a connection to the SQLite database
        conn = sqlite3.connect('/app/database/todo.db')
        cursor = conn.cursor()

        # SQL UPDATE command to mark a task as completed
        update_task_query = """
            UPDATE tasks SET description = ?, status = ? WHERE id = ?
        """

        # Execute the SQL command with the new status and task ID
        cursor.execute(update_task_query, (taskDesc, taskStatus, taskID))

        # Commit changes to the database
        conn.commit()

        # Close the database connection
        conn.close()

        # Return a success message
        return jsonify({'message': f'Task {taskID} has been updated'}), 200

    except Exception as e:
        # Handle exceptions, rollback changes, and return an error message
        if 'conn' in locals():
            conn.rollback()
            conn.close()
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

