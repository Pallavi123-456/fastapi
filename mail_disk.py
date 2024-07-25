import psutil
from fastapi import FastAPI
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = FastAPI()


def bytes_to_gb(bytes_value):
    return round(bytes_value / (1024 ** 3))

SECRET_KEY = os.getenv('SECRET_KEY')
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USER = 'pallavipatil0713@gmail.com'  
EMAIL_PASSWORD = 'wkys nlir xkfn tzcl'  
EMAIL_SENDER = 'pallavipatil0713@gmail.com'  
EMAIL_RECIPIENT = 'pallavippatil2505@gmail.com' 



def send_email(subject, message):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECIPIENT
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    try:
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASSWORD)
        text = msg.as_string()
        server.sendmail(EMAIL_SENDER, EMAIL_RECIPIENT, text)
        server.quit()
        print('Email sent successfully!')
        return 'Email sent successfully'
    except smtplib.SMTPAuthenticationError as e:
        print(f'Failed to authenticate:{e}')   
        return 'Failed to authentication'
    except Exception as e:
        print(f'Failed to send email: {e}')
        return 'Failed to sent email'


@app.get("/disk-space")
def get_disk_space():
    disks = {}
    threshold_percent = 30
    for part in psutil.disk_partitions():
        if 'fixed' in part.opts or 'removable' in part.opts:
            usage = psutil.disk_usage(part.mountpoint)
            disks[part.device] = {
                "total": bytes_to_gb(usage.total),
                "used": bytes_to_gb(usage.used),
                "free": bytes_to_gb(usage.free),
                "percent": usage.percent
            }

       
            if usage.percent > threshold_percent:
                subject = f'Disk Space Alert: {part.device} exceeded {threshold_percent}% usage'
                message = f'Total: {bytes_to_gb(usage.total)} GB, Used: {bytes_to_gb(usage.used)} GB, Free: {bytes_to_gb(usage.free)} GB'
                status_msg = send_email(subject, message)

    return {"Disk Information":disks , "message": status_msg}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)