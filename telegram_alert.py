import requests

# Replace with your actual bot token and chat ID
TELEGRAM_BOT_TOKEN = "7942412346:AAH6WHW7tKx7aJKCXtijDjvNoBhsBGUuABo"
TELEGRAM_CHAT_ID = "5652444161"  # Replace this after fetching actual chat ID

def send_report_via_telegram(report_path):
    url = f"https://api.telegram.org/bot7942412346:AAH6WHW7tKx7aJKCXtijDjvNoBhsBGUuABo/sendDocument"
    
    with open(report_path, 'rb') as file:
        files = {'document': file}
        data = {'chat_id': TELEGRAM_CHAT_ID}
        response = requests.post(url, data=data, files=files)
        
    if response.status_code == 200:
        print("✅ Report sent successfully via Telegram.")
    else:
        print(f"❌ Failed to send report. Error: {response.text}")

# Example usage
if __name__ == "__main__":
    report_file_path = r"C:\Users\megav\SecureVault\leak_report.csv"
    send_report_via_telegram(report_file_path)

