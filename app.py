from flask import Flask, request, render_template, redirect, url_for, flash, Markup
import os

app = Flask(__name__)
app.secret_key = 'verysecretkey'  # Hardcoded secret key (Vulnerability #1)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
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
    return render_template('index.html', word_count=None)

if __name__ == "__main__":
    app.run(debug=True)
