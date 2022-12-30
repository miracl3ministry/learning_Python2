import imaplib
import email
from fast_mail_parser import parse_email, ParseError

# значения объекта email
# email.subject
# email.date
# email.text_plain
# email.text_html
# email.headers
# email.attachments
#   attachment.mimetype
#   attachment.content
#   attachment.filename

def getMailFromFile(files):
    # парсит письма из загруженных через форму файлов и возвращает массив
    parsedMessages = []
    for filePath in files:
        with open(filePath, 'r') as f:
            message_payload = f.read()
        try:
            email2 = parse_email(message_payload)
        except ParseError as e:
            print("Failed to parse email: ", e)
            return False
        parsedMessages.append(email2)
    return parsedMessages

def getMailByIMAP(mail_address: str, mail_pass:str, server_domain:str):
    # mail_pass пароль приложения
    # фенуция принимает логин-пароль, берет письма по imap
    host = f'imap.{server_domain}'
    imap = imaplib.IMAP4_SSL(host)
    imap.login(mail_address, mail_pass)
    print(imap.list()) # список доступных ящиков
    imap.select()
    typ, data = imap.search(None, 'ALL')
    parsedMessages = []
    for num in data[0].split():
        typ, data = imap.fetch(num, '(RFC822)')
        for response_part in data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                email2 = parse_email(msg.as_string())
                parsedMessages.append(email2)
    return parsedMessages