import MailParser as mp
import os
import shutil

eml_files = []
eml_files_path = os.path.join(os.getcwd(), 'UploadFiles') #'./venv/UploadFiles/' "C:/Users/user/source/repos/SpamFilterProject/SpamFolder/" 
if (not os.path.isdir(eml_files_path)): os.makedirs('UploadFiles')
mail_address = "Rashat03@yandex.ru"
mail_pass = ""
mail_domain = "yandex.ru"
selectedMessage = []
selectedMessageText = ""
selectedMessageSubject = "Тема выбранного письма"
messages = list()

# тут происходит валидация данных и отправка их дальше 
# нижу идут функции, которые возвращают данные в app

def show_index_page():
    global selectedMessageText
    global selectedMessageSubject
    global messages
    messages.clear()
    data = {
        'inbox': messages,
        'selectedMessageF': selectedMessage,
        'selectedMessageHTML': selectedMessageText,
        'selectedMessageSubjectF': selectedMessageSubject,
    }
    return data

# Выбор письма и открытие его
def selectmsg(messsageListItem):
    global selectedMessage
    global selectedMessageText
    global selectedMessageSubject
    global messages
    selectedMessageSubject = str(messsageListItem)
    try:
        for msg in messages:
            if(msg['header']['subject'] == selectedMessageSubject):
                selectedMessage.clear()
                selectedMessage.append(msg)
                # selectedMessageText = msg['header']['html'] ## старый вариант
                selectedMessageText = msg['mailText']
    except Exception as e:
        print(f'Couldn\'t load HTML msg: {e}')
    data = {
        'inbox': messages,
        'selectedMessageF': selectedMessage,
        'selectedMessageHTML': selectedMessageText,
        'selectedMessageSubjectF': selectedMessageSubject,
    }
    return data

def getFilesByPOST(upload_files):
    global eml_files
    global messages
    filePaths = []
    for file in upload_files:
        filePaths.append(os.path.join(eml_files_path, file.filename))
    # eml_files = get_eml_files(eml_files_path) ## разобраться что это
    # messages = mp.Get_Parsed_EML_Messages(eml_files) ## и это
    messages += mp.getMailFromFile(filePaths)
    clean_folder()
    data = {
        'inbox': messages,
        'selectedMessageHTML': selectedMessageText,
        'selectedMessageSubjectF': selectedMessageSubject,
    }
    return data

def get_mail(mail_address, mail_pass, mail_domain):
    # Загрузка писем из почты
    global messages
    mail_address = str(mail_address)
    mail_pass = str(mail_pass)
    mail_domain = str(mail_domain)
    # messages = mp.Get_Messages_From_Mail(mail_address, mail_pass, mail_domain) # старая функция
    messages += mp.getMailByIMAP(mail_address, mail_pass, mail_domain)
    data = {
        'inbox': messages,
        'selectedMessageHTML': selectedMessageText,
        'selectedMessageSubjectF': selectedMessageSubject,
    }
    return data

def checkForSpam():
    print('pass')
    pass

# дальше идут функции модуля

def get_eml_files(folder_path):
    eml_files_list = []
    eml_paths_list = []

    for (dirpath, dirnames, filenames) in os.walk(folder_path):
        eml_paths_list.extend(filenames)
        break
    for file in eml_paths_list:
        if(file.endswith('meta')):
            continue
        #print(file)
        with open(folder_path+file, 'rb') as f:
            eml_files_list.append(f.read())

    return eml_files_list

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

if __name__ == '__main__': 
    print("not work")
