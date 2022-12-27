import model

# тут происходит валидация данных и отправка их дальше 
# ниже идут функции, которые возвращают данные в app

def show_index_page():
    model.selectedMessage.clear()
    model.selectedMessageText = ""
    model.selectedMessageSubject = ""
    data = {
        'inbox': model.messages,
        'selectedMessageF': model.selectedMessage,
        'selectedMessageHTML': model.selectedMessageText,
        'selectedMessageSubjectF': model.selectedMessageSubject,
    }
    return data

# Выбор и открытие письма
def selectmsg(messsageListItem):
    model.selectMail(str(messsageListItem))
    data = {
        'inbox': model.messages,
        'selectedMessageF': model.selectedMessage,
        'selectedMessageHTML': model.selectedMessageText,
        'selectedMessageSubjectF': model.selectedMessageSubject,
    }
    return data

# Загрузка eml файла в систему
def getFilesByPOST(upload_files):
    model.parceMailFromFiles(upload_files)
    data = {
        'inbox': model.messages,
        'selectedMessageHTML': model.selectedMessageText,
        'selectedMessageSubjectF': model.selectedMessageSubject,
    }
    return data

# Загрузка писем из ящика
def get_mail(mail_address, mail_pass, mail_domain):
    mail_address = str(mail_address)
    mail_pass = str(mail_pass)
    mail_domain = str(mail_domain)
    model.getMailFromIMAP(mail_address, mail_pass, mail_domain)
    data = {
        'inbox': model.messages,
        'selectedMessageHTML': model.selectedMessageText,
        'selectedMessageSubjectF': model.selectedMessageSubject,
    }
    return data

def checkForSpam():
    model.checkForSpam()
    return "OK"
