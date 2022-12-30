import mailParser
import SpamFilter

messages = list()
selectedMessage = []
selectedMessageHTML = ""
selectedMessageSubject = "Тема выбранного письма"
selectedMessageHeaders = ""
selectedMessageAttachment = ""

def selectMail(messsageListItem):
    global messages
    global selectedMessage
    global selectedMessageHTML
    global selectedMessageSubject
    global selectedMessageHeaders
    global selectedMessageAttachment
    selectedMessageSubject = messsageListItem
    try:
        for msg in messages:
            if(msg.subject == selectedMessageSubject):
                selectedMessage.clear()
                selectedMessage.append(msg)
                selectedMessageHeaders = msg.headers
                selectedMessageAttachment = msg.attachments
                if hasattr(msg, 'text_html') and (bool(msg.text_html)): selectedMessageHTML = msg.text_html[0]
                else: selectedMessageHTML = msg.text_plain[0].strip().replace('\\n','<br>').replace('\\t','    ')
    except Exception as e:
        print(f'Couldn\'t load HTML msg: {e}')

def parceMailFromFiles(filePaths):
    global messages
    messages += mailParser.getMailFromFile(filePaths)

def getMailFromIMAP(mail_address, mail_pass, mail_domain):
    global messages
    messages += mailParser.getMailByIMAP(mail_address, mail_pass, mail_domain)

def checkForSpam():
    global messages
    pass