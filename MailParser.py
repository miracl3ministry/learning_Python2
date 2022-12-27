import eml_parser
import email
import quopri
import imaplib
import base64
from os import walk

def getMailFromFile(files):
    # парсит письма из загруженных через форму файлов и возвращает массив
    parsedMessages = []
    ep = eml_parser.EmlParser()
    for filePath in files:
        with open(filePath, 'rb') as f:
            mail = ep.decode_email_bytes(f.read())
            # print(json.dumps(mail['header']['header']))
        with open(filePath, 'r') as f:
            mail['mailText'] = parseTextFromMail(email.message_from_file(f)) # .encode('utf-8').strip()
        
        for text in mail['mailText']:
            if (type(text) is str): text = text.strip().replace('\\n','<br>').replace('\\t','    ')

        parsedMessages.append(mail)
    return parsedMessages

def getMailByIMAP(mail_address: str, mail_pass:str, server_domain:str):
    # mail_pass пароль приложения
    # фенуция принимает логин-пароль и читает письма по imap
    host = f'imap.{server_domain}'
    imap = imaplib.IMAP4_SSL(host)
    imap.login(mail_address, mail_pass)
    print(imap.list()) # список доступных ящиков
    imap.select()
    typ, data = imap.search(None, 'ALL')
    parsedMessages = []
    ep = eml_parser.EmlParser()
    for num in data[0].split():
        typ, data = imap.fetch(num, '(RFC822)')
        for item in data:
            if (type(item[0]) is bytes):
                mailData = ep.decode_email_bytes(item[1])
                # sdeyayyqmfdsiyrw
                mailData['mailText'] = parseTextFromMail(email.message_from_bytes(item[1]))
                parsedMessages.append(mailData)
    return parsedMessages

def parseTextFromMail(mail, recursion=False, charset="utf-8"):
    # парсит текст, хтмл и названия файлов
    cp = mail.get_content_type()
    print("==== На вход парсера получен файл ==== \n Рекурсия:", recursion, 'Кодировка:', charset, 'content type:', cp)
    print('Is multipart?', mail.get_content_maintype() == 'multipart', mail.is_multipart())
    if not mail.is_multipart() or recursion:
        for part in mail.walk():
            print('\t 1. part content type:', part.get_content_type())
            # TODO вместо return попробовать сохранить всё в массив и посмотреть что там
            # и вообще всё переработать, пересмотреть и переделать
            if cp == "text/plain":
                try:
                    return letter_type(part)
                except UnicodeDecodeError:
                    print("except error")
                    if (type(part) is str): return part.decode("utf-8", errors='replace')
                    else: return part.get_payload(decode=True).decode("utf-8")
            elif cp == "text/html": 
                try:
                    return letter_type(mail)
                except UnicodeDecodeError:
                    print("except error")
                    return base64.b64decode(part.get_payload(decode=True)).decode("utf-8")
            elif part.get_content_disposition() == 'attachment':
                print("В письме есть необработанный файл:", part.get_filename(), "乁[ ◕ ᴥ ◕ ]ㄏ")
                return part.get_filename()
            else:
                # на случай если когда-то попадет сюда https://stackoverflow.com/questions/31392361/how-to-read-eml-file-in-python
                print("idk how to fix", mail.get("content-type"), part.get("content-type"), part.get_filename())
                return part.get("content-type")
    else:
        # если письмо состоит их нескольких частей попадаем в эту ветку
        # далее происходит какая-то магия 
        parts = []
        for part in mail.walk():
            print('\t 2. part content type:', part.get_content_type())
            content_type = part.get_all('content-type')[0]
            print('content-type', part.get_all('content-type'), content_type)
            index = content_type.find('charset')
            charset = "utf-8"
            if (index > 0): 
                charset = content_type[index:].split('\"')
                if (len(charset) == 1): charset = charset[0].split('=')[1]
                else: charset = charset[1]
            print('charset', charset)
            # print('date', part.get_all('date'))
            if (cp == 'multipart/alternative'): 
                print('boundary', part.get_all('boundary'))
                continue
            # рабочие варианты получения текста
            # parts.append(part.as_string())
            # parts.append(letter_type(part))
            # parts.append(part.get_payload(decode=True))
            parts.append(parseTextFromMail(part, True, charset))
            parts.append("<hr>")
        return parts

def letter_type(part):
    if part["Content-Transfer-Encoding"] in (None, "7bit", "8bit", "binary"):
        return part.get_payload()
    elif part["Content-Transfer-Encoding"] == "base64":
        encoding = part.get_content_charset()
        return base64.b64decode(part.get_payload()).decode(encoding)
    elif part["Content-Transfer-Encoding"] == "quoted-printable":
        encoding = part.get_content_charset()
        return quopri.decodestring(part.get_payload()).decode(encoding)
    else:  # all possible types: quoted-printable, base64, 7bit, 8bit, and binary
        return part.get_payload()
