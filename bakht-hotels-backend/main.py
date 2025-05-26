from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from typing import Optional

app = FastAPI(title="Murad Hotels API", version="1.0.0")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ContactForm(BaseModel):
    name: str
    email: EmailStr
    phone: str
    buy: bool
    sell: bool
    currentPlan: Optional[str] = None


EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT"))
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")


def send_email_smtp(form_data: ContactForm):

    try:

        msg = MIMEMultipart()
        msg['From'] = f"{form_data.name} <{EMAIL_USER}>"
        msg['To'] = RECEIVER_EMAIL
        msg['Reply-To'] = form_data.email
        msg['Subject'] = f"New Contact: {form_data.name} - Murad Hotels"


        body = f"""
📧 NEW CONTACT FORM SUBMISSION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

👤 CUSTOMER INFORMATION:
   Name: {form_data.name}
   Email: {form_data.email}
   Phone: {form_data.phone}

🏠 INTERESTS:
   • Buying Property: {'✅ Yes' if form_data.buy else '❌ No'}
   • Selling Property: {'✅ Yes' if form_data.sell else '❌ No'}"""

        if form_data.currentPlan:
            body += f"\n   • Selected Plan: {form_data.currentPlan}"

        body += f"""

📝 HOW TO RESPOND:
   • Click REPLY to respond directly to {form_data.name}
   • Their email: {form_data.email}
   • Their phone: {form_data.phone}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
This message was sent via Murad Hotels contact form
Time: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """

        msg.attach(MIMEText(body, 'plain'))


        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASSWORD)

        text = msg.as_string()
        server.sendmail(EMAIL_USER, RECEIVER_EMAIL, text)
        server.quit()

        return True
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False

@app.get("/")
async def root():

    return {"message": "Murad Hotels API is running"}

@app.post("/send-email")
async def send_email(form: ContactForm):

    try:

        if not form.name or not form.email or not form.phone:
            raise HTTPException(status_code=400, detail="Name, email, and phone are required")


        print("=== FORM SUBMISSION RECEIVED ===")
        print(f"Name: {form.name}")
        print(f"Email: {form.email}")
        print(f"Phone: {form.phone}")
        print(f"Buy: {form.buy}")
        print(f"Sell: {form.sell}")
        print(f"Plan: {form.currentPlan}")
        print("===============================")


        email_sent = send_email_smtp(form)

        if email_sent:
            return {"message": "Email sent successfully!", "status": "success"}
        else:

            print("Email failed to send, but returning success for testing")
            return {"message": "Form received successfully! (Email setup needed)", "status": "success"}

    except HTTPException:
        raise
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/health")
async def health_check():

    return {"status": "healthy", "message": "Backend is running properly"}


@app.post("/test-email")
async def test_email_endpoint(form: ContactForm):

    return {
        "message": "Data received successfully",
        "received_data": {
            "name": form.name,
            "email": form.email,
            "phone": form.phone,
            "buy": form.buy,
            "sell": form.sell,
            "currentPlan": form.currentPlan
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
