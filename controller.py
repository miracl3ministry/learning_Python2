import model
import os
import shutil

eml_files_path = os.path.join(os.getcwd(), 'UploadFiles') #'./venv/UploadFiles/' "C:/Users/user/source/repos/SpamFilterProject/SpamFolder/" 
if (not os.path.isdir(eml_files_path)): os.makedirs('UploadFiles')

# тут происходит валидация данных и отправка в model
# ниже идут функции, которые возвращают данные в app

def show_index_page():
    model.selectedMessage.clear()
    model.selectedMessageText = ""
    model.selectedMessageSubject = ""
    return collectDataResponse()

def selectmsg(messsageListItem):
    # Выбор и открытие письма
    model.selectMail(str(messsageListItem))
    return collectDataResponse()

def getFilesByPOST(upload_files):
    # Загрузка eml файла в систему
    filePaths = []
    for file in upload_files:
        filePaths.append(os.path.join(eml_files_path, file.filename))
    model.parceMailFromFiles(filePaths)
    clean_folder()
    return collectDataResponse()

def get_mail(mail_address, mail_pass, mail_domain):
    # Загрузка писем из ящика
    model.getMailFromIMAP(str(mail_address), str(mail_pass), str(mail_domain))
    return collectDataResponse()

def checkForSpam():
    model.checkForSpam()
    return "OK"

def collectDataResponse():
    # собирает словарь данных для отправки ответа на фронт-энд
    data = {
        'inbox': model.messages,
        'selectedMessageHTML': model.selectedMessageHTML,
        'selectedMessageHeaders': model.selectedMessageHeaders,
        'selectedMessageAttachment': model.selectedMessageAttachment,
    }
    return data

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