from flask import Flask, render_template, request, redirect, session, url_for, jsonify, send_file
from database import init_db, create_user, validate_user, save_report, get_reports, is_duplicate, delete_report, get_report_image
from imghdr import what
import io

app = Flask(__name__)
app.secret_key = 'super-secret-key'
init_db()

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if create_user(username, password):
            return redirect('/login')
        else:
            return "Username already exists", 400
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if validate_user(username, password):
            session['username'] = username
            if username == "admin":
                return redirect('/admin')
            return redirect('/')
        else:
            return "Invalid credentials", 401
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/')
def index():
    if 'username' not in session:
        return redirect('/login')
    return render_template('index.html', username=session['username'])

@app.route('/report', methods=['POST'])
def report():
    if 'username' not in session:
        return jsonify({'status': 'unauthorized'}), 401

    lat = request.form.get('lat', type=float)
    lon = request.form.get('lon', type=float)
    description = request.form.get('description')
    issue_type = request.form.get('issue_type')
    image_file = request.files.get('image')

    image_blob = None
    if image_file:
        image_blob = image_file.read()

    if is_duplicate(lat, lon):
        return jsonify({'status': 'duplicate'}), 200

    save_report(lat, lon, description, issue_type, image_blob)
    return jsonify({'status': 'ok'}), 201

@app.route('/reports', methods=['GET'])
def reports():
    return jsonify(get_reports())

@app.route('/admin', methods=['GET'])
def admin():
    if 'username' not in session or session['username'] != 'admin':
        return redirect('/login')
    reports = get_reports()
    return render_template('admin.html',
                         username=session['username'],
                         reports=reports)
    
@app.route('/resolved', methods=['DELETE'])
def deleteReport():
    data = request.json
    unique_id = data.get('unique_id')
    delete_report(unique_id)
    return jsonify({'status': 'ok'}), 200

@app.route('/image/<unique_id>')
def get_image(unique_id):
    image_blob = get_report_image(unique_id)
    if image_blob:
        image_type = what(None, h=image_blob)
        mimetype = f'image/{image_type}' if image_type else 'application/octet-stream'
        return send_file(
            io.BytesIO(image_blob),
            mimetype=mimetype
        )
    return "Image not found", 404

if __name__ == '__main__':
    app.run(debug=True)