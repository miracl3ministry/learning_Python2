import MailParser as mp
import SpamFilter
import os
import shutil

eml_files = []
eml_files_path = os.path.join(os.getcwd(), 'UploadFiles') #'./venv/UploadFiles/' "C:/Users/user/source/repos/SpamFilterProject/SpamFolder/" 
if (not os.path.isdir(eml_files_path)): os.makedirs('UploadFiles')

mail_address = "Rashat03@yandex.ru"
mail_pass = ""
mail_domain = "yandex.ru"

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

def parceMailFromFiles(upload_files):
    filePaths = []
    for file in upload_files:
        filePaths.append(os.path.join(eml_files_path, file.filename))
    global messages
    messages += mp.getMailFromFile(filePaths)
    clean_folder()

def getMailFromIMAP(mail_address, mail_pass, mail_domain):
    global messages
    messages += mp.getMailByIMAP(mail_address, mail_pass, mail_domain)

def checkForSpam():
    global messages
    pass

def clean_folder():
    """ Очищает папку eml_files_path = ./UploadFiles """
    for filename in os.listdir(eml_files_path):
        file_path = os.path.join(eml_files_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    return