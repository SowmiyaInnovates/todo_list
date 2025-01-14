


from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail, Message

app = Flask(__name__)

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_gmail_@gmail.com'
app.config['MAIL_PASSWORD'] = 'your_password_'

mail = Mail(app)

# To-Do list storage
tasks = []

@app.route('/')
def index():
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    task = request.form.get('task')
    if task:
        tasks.append(task)
    return redirect(url_for('index'))

@app.route('/delete/<int:task_index>', methods=['POST'])
def delete_task(task_index):
    if 0 <= task_index < len(tasks):
        tasks.pop(task_index)
    return redirect(url_for('index'))

@app.route('/send', methods=['POST'])
def send_email():
    recipient_email = request.form.get('email')
    if recipient_email:
        task_list = '\n'.join(tasks)
        msg = Message('Your To-Do List', sender='your-email@gmail.com', recipients=[recipient_email])
        msg.body = f"Here is your To-Do list:\n\n{task_list}"
        mail.send(msg)
        return "Email sent successfully!"
    return "Failed to send email. Please provide a valid email address."

if __name__ == '__main__':
    app.run(debug=True)
