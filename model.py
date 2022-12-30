import MailParser as mp
import SpamFilter

messages = list()
selectedMessage = []
selectedMessageText = ""
selectedMessageSubject = "Тема выбранного письма"

def selectMail(messsageListItem):
    global messages
    global selectedMessage
    global selectedMessageText
    global selectedMessageSubject
    selectedMessageSubject = messsageListItem
    try:
        for msg in messages:
            if(msg['header']['subject'] == selectedMessageSubject):
                selectedMessage.clear()
                selectedMessage.append(msg)
                selectedMessageText = msg['mailText']
    except Exception as e:
        print(f'Couldn\'t load HTML msg: {e}')

def parceMailFromFiles(filePaths):
    global messages
    messages += mp.getMailFromFile(filePaths)

def getMailFromIMAP(mail_address, mail_pass, mail_domain):
    global messages
    messages += mp.getMailByIMAP(mail_address, mail_pass, mail_domain)

def checkForSpam():
    global messages
    pass