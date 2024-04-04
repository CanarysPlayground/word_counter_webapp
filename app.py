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
