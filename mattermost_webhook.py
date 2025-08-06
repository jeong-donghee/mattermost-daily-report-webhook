import requests
import schedule
import time
from datetime import datetime, timedelta

WEBHOOK_URL = "{MATTERMOST_WEBHOOK_URL}"

# 한글 요일
WEEKDAYS_KR = ["월", "화", "수", "목", "금", "토", "일"]

def send_message(text):
    payload = {"text": text}
    response = requests.post(WEBHOOK_URL, json=payload)
    if response.status_code != 200:
        print(f"❌ Error: {response.status_code}, {response.text}")
    else:
        print(f"✅ Sent: {text}")

def format_date_string(date: datetime):
    date_str = date.strftime("%m/%d")
    weekday = WEEKDAYS_KR[date.weekday()]
    return f"{date_str} ({weekday})"

def morning_plan():
    today = datetime.now()
    send_message(f"## 오늘의 계획 {format_date_string(today)}")

def evening_summary():
    today = datetime.now()
    send_message(f"## 어제의 진행 현황 {format_date_string(today)}")

# 평일만 실행
for day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']:
    getattr(schedule.every(), day).at("08:30").do(morning_plan)
    getattr(schedule.every(), day).at("17:30").do(evening_summary)

print("⏰ Mattermost scheduler started...")

while True:
    schedule.run_pending()
    time.sleep(1)
