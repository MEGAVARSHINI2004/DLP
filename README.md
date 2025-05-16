# 🛡️ SecureVault: A Python-Based Data Loss Prevention (DLP) System
SecureVault is a real-time Data Loss Prevention (DLP) solution developed in Python. It monitors and protects sensitive data across various channels, including file systems, clipboard, emails, and external devices. Leveraging machine learning and natural language processing techniques, SecureVault classifies data and enforces security policies to prevent unauthorized data exfiltration.

# 🚀 Features
## Real-Time File Monitoring
Detects access and modifications to sensitive documents.
Classifies files using ML/NLP and pattern matching.

## Clipboard & Screen Monitoring
Detects copy-paste actions involving confidential data (e.g., credit card numbers, passwords).
Alerts or blocks actions based on defined security policies.

## Email & Upload Monitoring
Analyzes outgoing emails for attachments and message content.
Blocks or alerts on suspected data leaks.

## External Drive Detection & Restriction
Detects and blocks sensitive data transfers to USB drives.
Applies write protection policies.

## Keyword and Regex-Based Detection
Utilizes custom keywords and regex patterns to detect PII, API keys, internal project names, etc.

## Behavioral Analysis
Detects unusual user activities, such as accessing a large number of files rapidly.
Triggers alerts for abnormal behavior.

## Security Policy Engine
Allows admin-defined rules: block, log, alert, quarantine.
Supports role-based policies for different departments.

## Dashboard & Reporting
Displays incidents, risk scores, and activity timelines.
Exports PDF/CSV logs for audit purposes.

# 🛠️ Tech Stack
Language: Python
GUI (Optional): Tkinter / PyQt for dashboard
## Data Monitoring:
watchdog for filesystem monitoring
psutil for process monitoring
pyshark for packet capture
pyperclip for clipboard access
## NLP/ML:
scikit-learn
spaCy
regex
nltk
Database: SQLite / PostgreSQL
## API Integration:
Telegram Bot for alert notifications

# 📦Installation
## Clone the Repository
git clone https://github.com/MEGAVARSHINI2004/SecureVault.git
cd SecureVault
## Create a Virtual Environment
On Windows: venv\Scripts\activate
## Install Dependencies
pip install -r requirements.txt


# 🚀 Usage
## Start the Application
python app.py
## Access the Dashboard
Open your web browser and navigate to http://127.0.0.1:5000.
## Login
Use the default admin credentials:
   Username: admin
   Password: admin123

# ⚙️ Configuration
Security Policies: Define and manage security policies in the config/policies.json file.
## Alert Notifications:
Telegram: Set up your Telegram Bot API token and chat ID in config/alerts.json.


# 📊 Dashboard
## The dashboard provides an intuitive interface to:
View real-time incidents and alerts.
Monitor risk scores and user activities.
Export logs in PDF or CSV formats for auditing purposes.


