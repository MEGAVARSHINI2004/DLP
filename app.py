import os
import pandas as pd
from flask import Flask, render_template, request, send_file, redirect, url_for, session
from io import StringIO
from functools import wraps
from flask import Response 

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Change this for production!

REPORT_FILE = "leak_report.csv"

# Simple user store (for demo)
USERS = {
    "admin": "password123"
}

def load_report():
    if not os.path.exists(REPORT_FILE) or os.path.getsize(REPORT_FILE) == 0:
        return None
    try:
        df = pd.read_csv(REPORT_FILE, on_bad_lines='skip', quotechar='"')
        return df
    except Exception as e:
        print(f"Error loading report: {e}")
        return None

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if USERS.get(username) == password:
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error="Invalid username or password")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
    df = load_report()
    if df is None:
        return "No data available."

    source_filter = request.values.get('source', '').lower()
    type_filter = request.values.get('type', '').lower()
    date_filter = request.values.get('date', '')

    filtered_df = df

    if source_filter:
        filtered_df = filtered_df[filtered_df['Source'].str.lower().str.contains(source_filter)]
    if type_filter:
        filtered_df = filtered_df[filtered_df['Type'].str.lower().str.contains(type_filter)]
    if date_filter:
        filtered_df = filtered_df[filtered_df['Timestamp'].str.startswith(date_filter)]

    table_html = filtered_df.to_html(classes='table table-striped', index=False, escape=False)

    # Prepare data for charts
    chart_data_type = (
        filtered_df.groupby('Type')
        .size()
        .reset_index(name='Count')
        .rename(columns={'Type': 'Type', 'Count': 'Count'})
        .to_dict(orient='list')
    )
    chart_data_time = None
    try:
        filtered_df['Date'] = pd.to_datetime(filtered_df['Timestamp']).dt.date
        chart_data_time = (
            filtered_df.groupby('Date')
            .size()
            .reset_index(name='Count')
            .rename(columns={'Date': 'Date', 'Count': 'Count'})
            .to_dict(orient='list')
        )
    except Exception:
        chart_data_time = {'Date': [], 'Count': []}

    # Safety: Ensure keys exist
    if not chart_data_type or 'Type' not in chart_data_type or 'Count' not in chart_data_type:
        chart_data_type = {'Type': [], 'Count': []}
    if not chart_data_time or 'Date' not in chart_data_time or 'Count' not in chart_data_time:
        chart_data_time = {'Date': [], 'Count': []}

    return render_template(
        'table.html',
        table=table_html,
        source=source_filter,
        type=type_filter,
        date=date_filter,
        chart_data_type=chart_data_type,
        chart_data_time=chart_data_time
    )

@app.route('/export')
@login_required
def export():
    df = load_report()
    if df is None:
        return redirect(url_for('home'))

    csv_string = df.to_csv(index=False)

    # Return CSV as downloadable response
    return Response(
        csv_string,
        mimetype='text/csv',
        headers={"Content-disposition": "attachment; filename=leak_report_export.csv"}
    )
def start_dashboard():
    app.run(debug=False, port=5000)

if __name__ == "__main__":
    start_dashboard()
