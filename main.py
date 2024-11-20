import imaplib
import email
import pandas as pd

# Function to read credentials from a file
def read_credentials(file_path):
    accounts = []
    with open(file_path, 'r') as file:
        for line in file:
            email, password, serv = line.strip().split(',')
            accounts.append({'email': email.strip(), 'password': password.strip(), 'imap_server': serv.strip()})
    return accounts

# Function to connect to an email account
def connect_to_email(account):
    mail = imaplib.IMAP4_SSL(account['imap_server'])
    mail.login(account['email'], account['password'])
    return mail

# # Function to fetch emails from an account
# def fetch_emails(mail):
#     mail.select('inbox')
#     _, data = mail.search(None, 'ALL')
#     mail_ids = data[0]

#     id_list = mail_ids.split()
#     emails = []

#     for i in id_list:
#         _, data = mail.fetch(i, '(RFC822)')
#         for response_part in data:
#             if isinstance(response_part, tuple):
#                 msg = email.message_from_bytes(response_part[1])
#                 emails.append({
#                     'from': msg['from'],
#                     'to': msg['to'],
#                     'subject': msg['subject'],
#                     'date': msg['date']
#                 })

#     return emails

# Function to fetch emails from an account
def fetch_emails(mail):
    mail.select('inbox')
    _, data = mail.search(None, 'ALL')
    mail_ids = data[0]

    id_list = mail_ids.split()
    emails = []

    for i in id_list:
        _, data = mail.fetch(i, '(RFC822)')
        for response_part in data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])

                # Initialize email text as empty
                email_text = ""

                # Check if the email message is multipart
                if msg.is_multipart():
                    for part in msg.walk():
                        # Check the content type of the email part
                        if part.get_content_type() == "text/plain":
                            try:
                                email_text = part.get_payload(decode=True).decode()
                                break  # Stop after finding the first text/plain part
                            except UnicodeDecodeError:
                                continue
                else:
                    # If not multipart, simply extract the payload
                    if msg.get_content_type() == "text/plain":
                        try:
                            email_text = msg.get_payload(decode=True).decode()
                        except:
                            continue
                payload = {
                            'from': msg['from'],
                            'to': msg['to'],
                            'subject': msg['subject'],
                            'date': msg['date'],
                            'text': email_text  # Add the extracted text to the email info
                        }
                emails.append(payload) 

    return emails


# Main script
search_filter = input('Filter? ')
if search_filter == '':
    search_filter = None
credentials_file = './logins.txt'  # Update with the path to your credentials file
accounts = read_credentials(credentials_file)
print("Num. of accounts: ", len(accounts))

all_emails = []

for account in accounts:
    try:
        mail = connect_to_email(account)
        print("Connected.")
        emails = fetch_emails(mail)
        print("Got emails.")
        all_emails.append(emails)
        print("Added to list.")
        mail.logout()
    except Exception as e:
        print("Error: ",e)
        continue

# for account in accounts:
#     mail = connect_to_email(account)
#     print("Connected.")
#     emails = fetch_emails(mail)
#     print("Got emails.")
#     all_emails.append(emails)
#     print("Added to list.")
#     mail.logout()

# Save emails to CSV
emails = []
for e in all_emails:
    temp_df = pd.DataFrame(e)
    emails.append(temp_df)

df = pd.concat(emails)
for c in df.columns:
    df[c] = df[c].apply(str)
df = df.copy()
if search_filter != None:
    final_df = df.loc[(df['from'].apply(str.lower).str.contains(search_filter.lower())) |
                      (df['subject'].apply(str.lower).str.contains(search_filter.lower())) |
                      (df['text'].apply(str.lower).str.contains(search_filter.lower()))]
else:
    final_df = df.copy()
    
final_df.to_csv(f'{search_filter}_emails.csv', index=False)