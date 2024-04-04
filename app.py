from flask import Flask, request, render_template, redirect, url_for, flash
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Generate a random secret key for session management

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and file.filename.endswith('.txt'):
            content = file.read().decode("utf-8") 
            word_count = len(content.split())
            return render_template('index.html', word_count=word_count)
        else:
            flash('Invalid file type. Only .txt files are allowed.')
            return redirect(request.url)
    return render_template('index.html', word_count=None)

if __name__ == "__main__":
    app.run(debug=True)  # Set debug=False in production
