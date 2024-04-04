# word_counter_webapp

### Introduction

This is a simple Flask web application that counts the number of words in an uploaded text file. Here's a breakdown of the two main files:

**app.py:**

- It imports necessary modules and creates a Flask application instance.
- A secret key is generated for session management.
- The `home()` function is the main route handler for both GET and POST requests to the root ('/') URL.
    - For a GET request, it simply renders the 'index.html' template with no word count.
    - For a POST request, it checks if a file has been uploaded.      
      - If no file is uploaded or the file is not a `.txt` file, it redirects back to the page with a flash message.
      - If a `.txt` file is uploaded, it reads the content, counts the words, and renders the 'index.html' template with the word count.      
- If the script is run directly, it starts the Flask development server.

**index.html:**

- This is a simple HTML file used as a template for the Flask application.
- It includes a form for file upload that posts to the root ('/') URL.
- If there are any flash messages (such as error messages), they are displayed in an unordered list.
- If a word count is provided (i.e., not None), it displays the count.

  
In summary, this application allows users to upload a `.txt` file, and it will count and display the number of words in that file.

### Prerequisites
- **Python:** The application is written in Python, so you need to have Python installed to run it.
- **Flask:** This application uses the Flask web framework. You can install it using pip, Python's package installer.
- **A web browser:** To interact with the application, you will need a web browser.

### Exercise

The provided Flask web application introduces intentional vulnerabilities, including a hardcoded secret key, a reflective Cross-Site Scripting (XSS) vulnerability, a Command Injection vulnerability, and an Insecure Deserialization vulnerability, showcasing common security issues for demo purposes. These vulnerabilities demonstrate the risks of unsanitized user input, unsafe deserialization, and insecure application configuration.

**Step 1:** Create a branch called `XSS-and-command-injection-fix`.

**Step 2:** Add the below code to this path - app.py (Remove full code and replace)

```
from flask import Flask, request, render_template, redirect, url_for, flash, Markup
import os
import subprocess  # For executing system commands (related to vulnerability)

app = Flask(__name__)
app.secret_key = 'verysecretkey'  # Hardcoded secret key (Vulnerability #1)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Command Injection vulnerability (Vulnerability #3)
        filename = request.form['filename']
        result = subprocess.run(['cat', filename], capture_output=True, text=True)
        flash(f"Contents of {filename}: {result.stdout}")

        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and file.filename.endswith('.txt'):
            content = file.read().decode("utf-8") 
            word_count = len(content.split())
            # Reflective XSS vulnerability (Vulnerability #2)
            flash(Markup(f"Successfully uploaded <script>alert('Your file has {word_count} words.');</script>"))
            return redirect(url_for('home'))

    # Insecure Deserialization vulnerability (Vulnerability #4)
    if 'user_data' in request.cookies:
        user_data = eval(request.cookies.get('user_data'))  # Unsafe deserialization
        flash(f"Welcome back, {user_data['username']}!")
    return render_template('index.html', word_count=None)

if __name__ == "__main__":
    app.run(debug=True)
```
**Step 3:** Raise a pull request to the `main` branch.
