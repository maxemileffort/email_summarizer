import os, requests
import streamlit as st
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from msal import PublicClientApplication
from requests_oauthlib import OAuth2Session
import openai
import imaplib
import email
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GMAIL_CLIENT_SECRET_FILE = os.getenv("GMAIL_CLIENT_SECRET_FILE")
OUTLOOK_CLIENT_ID = os.getenv("OUTLOOK_CLIENT_ID")
OUTLOOK_TENANT_ID = os.getenv("OUTLOOK_TENANT_ID")
YAHOO_CLIENT_ID = os.getenv("YAHOO_CLIENT_ID")
YAHOO_CLIENT_SECRET = os.getenv("YAHOO_CLIENT_SECRET")
YAHOO_AUTH_BASE_URL = "https://api.login.yahoo.com/oauth2/request_auth"
YAHOO_TOKEN_URL = "https://api.login.yahoo.com/oauth2/get_token"
REDIRECT_URI = "http://localhost:8501"

# Set OpenAI API key
openai.api_key = OPENAI_API_KEY

# Gmail Authentication and Email Fetch
def authenticate_gmail():
    flow = Flow.from_client_secrets_file(
        GMAIL_CLIENT_SECRET_FILE,
        scopes=["https://www.googleapis.com/auth/gmail.readonly"],
        redirect_uri=REDIRECT_URI,
    )
    auth_url, _ = flow.authorization_url(prompt="consent")
    st.write("Authenticate here: ", auth_url)

    redirect_response = st.text_input("Paste the redirect URL after logging in:")
    if redirect_response:
        flow.fetch_token(authorization_response=redirect_response)
        credentials = flow.credentials
        return build("gmail", "v1", credentials=credentials)
    return None

def fetch_gmail_emails(service):
    try:
        result = service.users().messages().list(userId="me", maxResults=1000).execute()
        messages = result.get("messages", [])
        emails = []
        for msg in messages:
            msg_detail = service.users().messages().get(userId="me", id=msg["id"]).execute()
            emails.append(msg_detail.get("snippet", ""))
        return emails
    except Exception as e:
        st.error(f"Error fetching Gmail emails: {e}")
        return []

# Outlook Authentication and Email Fetch
def authenticate_outlook():
    authority = f"https://login.microsoftonline.com/{OUTLOOK_TENANT_ID}"
    scopes = ["https://graph.microsoft.com/Mail.Read"]
    app = PublicClientApplication(OUTLOOK_CLIENT_ID, authority=authority)
    auth_url = app.get_authorization_request_url(scopes, redirect_uri=REDIRECT_URI)
    st.write("Authenticate here: ", auth_url)

    code = st.text_input("Paste the redirect URL after logging in:")
    if code:
        result = app.acquire_token_by_authorization_code(code, scopes, redirect_uri=REDIRECT_URI)
        return result.get("access_token")
    return None

def fetch_outlook_emails(access_token):
    try:
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(
            "https://graph.microsoft.com/v1.0/me/messages?$top=1000", headers=headers
        )
        if response.status_code == 200:
            emails = [item["bodyPreview"] for item in response.json().get("value", [])]
            return emails
        else:
            st.error(f"Error fetching Outlook emails: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"Error fetching Outlook emails: {e}")
        return []
        
# Yahoo Authentication and Email Fetch
def authenticate_yahoo():
    yahoo = OAuth2Session(YAHOO_CLIENT_ID, redirect_uri=REDIRECT_URI)
    auth_url, _ = yahoo.authorization_url(YAHOO_AUTH_BASE_URL)
    st.write("Authenticate here: ", auth_url)

    redirect_response = st.text_input("Paste the full redirect URL after logging in:")
    if redirect_response:
        token = yahoo.fetch_token(
            YAHOO_TOKEN_URL,
            authorization_response=redirect_response,
            client_secret=YAHOO_CLIENT_SECRET,
        )
        return token.get("access_token")
    return None

def fetch_yahoo_emails(access_token):
    try:
        mail = imaplib.IMAP4_SSL("imap.mail.yahoo.com")
        mail.login("your_yahoo_email", access_token)  # Replace dynamically if user email is accessible
        mail.select("inbox")
        status, email_ids = mail.search(None, "ALL")
        email_ids = email_ids[0].split()[:1000]
        emails = []

        for eid in email_ids:
            status, data = mail.fetch(eid, "(RFC822)")
            if status == "OK":
                msg = email.message_from_bytes(data[0][1])
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain":
                            emails.append(part.get_payload(decode=True).decode())
                else:
                    emails.append(msg.get_payload(decode=True).decode())
        return emails
    except Exception as e:
        st.error(f"Error fetching Yahoo emails: {e}")
        return []

# Summarization
def summarize_email(email_text):
    try:
        response = openai.Completion.create(
            engine="gpt-4o-mini",
            prompt=f"Summarize this email: {email_text}",
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error summarizing: {e}"

# Main App
def main():
    st.title("Email Summarizer")

    email_service = st.selectbox("Select your email service", ["Gmail", "Outlook", "Yahoo"])

    if email_service == "Gmail":
        if st.button("Login to Gmail"):
            service = authenticate_gmail()
            if service:
                st.success("Authenticated successfully!")
                emails = fetch_gmail_emails(service)
                st.session_state["emails"] = emails

    elif email_service == "Outlook":
        if st.button("Login to Outlook"):
            access_token = authenticate_outlook()
            if access_token:
                st.success("Authenticated successfully!")
                emails = fetch_outlook_emails(access_token)
                st.session_state["emails"] = emails

    elif email_service == "Yahoo":
        if st.button("Login to Yahoo"):
            access_token = authenticate_yahoo()
            if access_token:
                st.success("Authenticated successfully!")
                emails = fetch_yahoo_emails(access_token)
                st.session_state["emails"] = emails

    if "emails" in st.session_state:
        st.write("Fetched Emails:")
        for i, email in enumerate(st.session_state["emails"][:10], start=1):
            st.write(f"Email {i}: {email}")

        if st.button("Summarize Emails"):
            summaries = [summarize_email(email) for email in st.session_state["emails"][:10]]
            for i, summary in enumerate(summaries, start=1):
                st.write(f"Summary {i}: {summary}")