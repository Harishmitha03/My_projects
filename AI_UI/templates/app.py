from flask import Flask, render_template, request, redirect, url_for, send_file
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pandas as pd
from fpdf import FPDF
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///resource_flow.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- Database Models ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    role = db.Column(db.String(20)) # 'Employee' or 'Manager'

class ResourceRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    category = db.Column(db.String(50))
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='Pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    resolution_date = db.Column(db.DateTime, nullable=True)

# --- Routes ---
@app.route('/')
def index():
    # Mocking a login for demo purposes
    requests = ResourceRequest.query.all()
    return render_template('dashboard.html', requests=requests)

@app.route('/submit', methods=['POST'])
def submit_request():
    new_req = ResourceRequest(
        user_id=1, # Default mock user
        category=request.form['category'],
        description=request.form['description']
    )
    db.session.add(new_req)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/update/<int:id>/<string:status>')
def update_status(id, status):
    req = ResourceRequest.query.get(id)
    req.status = status
    if status in ['Fulfilled', 'Rejected']:
        req.resolution_date = datetime.utcnow()
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/export/csv')
def export_csv():
    reqs = ResourceRequest.query.all()
    data = [{'ID': r.id, 'Category': r.category, 'Status': r.status, 'Date': r.created_at} for r in reqs]
    df = pd.DataFrame(data)
    df.to_csv('report.csv', index=False)
    return send_file('report.csv', as_attachment=True)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Create a mock manager if empty
        if not User.query.filter_by(username='admin').first():
            db.session.add(User(username='admin', role='Manager'))
            db.session.commit()
    app.run(debug=True)