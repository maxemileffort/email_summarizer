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
### OpenAI
1. Go to the [OpenAI API Keys](https://platform.openai.com/signup/).
1. Navigate to Dashboard → API Keys → Create New Secret Key.
1. Set permissions as needed, then name the key, and create.
1. Note the key somewhere, as you will only see it once.
1. Update `.env` file with the API key like so:2. 

```
OPENAI_API_KEY=your_openai_api_key
```

### Gmail
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
1. Create a new project and enable the Gmail API.
1. Navigate to Credentials → Create Credentials → OAuth 2.0 Client IDs.
1. Choose Web Application as the application type.
1. Set the Authorized redirect URI to `http://localhost:8501`.
1. Download the `client_secret.json` file and save it in your project folder.
1. Add path of `client_secret.json` to `.env` file like so:
 
```
GMAIL_CLIENT_SECRET_FILE=path/to/client_secret.json
```

### Outlook
1. Go to the [Azure Portal](https://portal.azure.com/).
1. Register a new application.
1. Add API Permissions for Mail.Read under the Microsoft Graph API.
1. Set the Redirect URI to `http://localhost:8501`.
1. Note the Application (client) ID and Directory (tenant) ID.
1. Update the `.env` file with the following:
```
OUTLOOK_CLIENT_ID=your_outlook_client_id
OUTLOOK_TENANT_ID=your_tenant_id
```

### Yahoo
1. Go to the [Yahoo Developer Console](https://developer.yahoo.com/).
1. Create a new project and choose OAuth2 as the authentication type.
1. Set the Redirect URI to `http://localhost:8501`.
1. Note the Client ID and Client Secret.
1. Update the .env file with:

```
YAHOO_CLIENT_ID=your_yahoo_client_id
YAHOO_CLIENT_SECRET=your_yahoo_client_secret
```

## Project Structure

```
email-summarizer/
├── .env.default         # Template for environment variables
├── requirements.txt     # Python dependencies
├── app.py               # Main Streamlit app
```

## Troubleshooting

### Missing Credentials
Ensure all necessary API credentials and JSON files are correctly added to the .env file.
### OAuth Redirect Issues
Make sure the redirect URI in the respective API configuration matches `http://localhost:8501`.
### Fetching Errors
Double-check the email permissions in your Gmail/Outlook/Yahoo app configuration.

## License
This project is licensed under the MIT License. Feel free to use, modify, and distribute it as needed.