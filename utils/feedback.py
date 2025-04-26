import csv
import os
from datetime import datetime

def log_feedback(user_input, bot_response, feedback, log_file="feedback/feedback_log.csv"):
    file_exists = os.path.isfile(log_file)
    with open(log_file, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(["timestamp", "user_input", "bot_response", "feedback"])
        writer.writerow([datetime.now().isoformat(), user_input, bot_response, feedback])
