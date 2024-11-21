# Email Summarizer App

A Streamlit application that allows users to authenticate with Gmail, Outlook, or Yahoo to fetch their most recent emails and summarize them using OpenAI's API.

---

## Features

- **Email Authentication**: Supports Gmail, Outlook, and Yahoo email accounts.
- **Email Fetching**: Retrieves up to the 1,000 most recent emails.
- **Email Summarization**: Uses OpenAI's API to summarize fetched emails.

---

## Prerequisites

1. **Python**: Ensure Python 3.8 or later is installed.
2. **API Credentials**: Obtain credentials for Gmail, Outlook, and Yahoo as described below.
3. **Dependencies**: Install the required Python libraries from `requirements.txt`.

---

## Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
    ```
2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use: venv\Scripts\activate
    ```
3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Rename `.env.default` to `.env` and fill in the credentials.

| Key | Description |
| ----------- | ----------- |
| OPENAI_API_KEY | API key for OpenAI. Obtain from [OpenAI API Keys](https://platform.openai.com/signup/) |
| GMAIL_CLIENT_SECRET_FILE | Path to the `client_secret.json` file for Gmail API. |
| OUTLOOK_CLIENT_ID | Client ID for the Microsoft Graph API. Obtain from [Azure Portal](https://portal.azure.com/) |
| OUTLOOK_TENANT_ID | Tenant ID for your Microsoft application. |
| YAHOO_CLIENT_ID | Client ID for Yahoo OAuth2. Obtain from [Yahoo Developer Console](https://developer.yahoo.com/) |
| YAHOO_CLIENT_SECRET | Client secret for Yahoo OAuth2. |

## Setting Up API Credentials
### Gmail
1. Go to the Google Cloud Console.
1. Create a new project and enable the Gmail API.
1. Navigate to Credentials → Create Credentials → OAuth 2.0 Client IDs.
1. Choose Web Application as the application type.
1. Set the Authorized redirect URI to http://localhost:8501.
1. Download the client_secret.json file and save it in your project folder.