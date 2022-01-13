# Vaccine checker

Python script using Selenium regularly run with Cron tabs to check the NHS website for eligibility of getting a covid vaccine with updates sent to Slack

Install version 89 of ChromeDriver: https://sites.google.com/chromium.org/driver/downloads?authuser=0

1. virtualenv .venv
2. source .venv/bin/activate
3. pip install -r requirements.txt 
3. run vaccine.py

Crontab to run regularly and notify when elgible to book
