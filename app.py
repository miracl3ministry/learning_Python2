import os
import json
import flask
import controller

template_folder = os.path.join(os.getcwd(), 'public/templates')
static_folder = os.path.join(os.getcwd(), 'public/static')

app = flask.Flask('MailApp', template_folder=template_folder, static_folder=static_folder)
app.config['EXPLAIN_TEMPLATE_LOADING'] = True
app.secret_key = os.urandom(24)
app.config['UPLOAD_FOLDER'] = 'UploadFiles'
# определяем routs и их логику

# принимаемые параметры data для index.html: 
# находятся в controller.py/collectDataResponse()
# inbox = письма в формате массива как я понимаю
# selectedMessageF = наверное выбранное письмо
# selectedMessageHTML = видимо текст в хтмл формате
# selectedMessageSubjectF = тема письма

@app.route('/', methods=['POST', 'GET'])
def returnIndexPage():
    data = controller.show_index_page()
    return flask.render_template('index.html', data=data)

@app.route('/selectmsg', methods=['POST'])
# выбирает письмо и что-то дальше делает
def selectMessage():
    data = controller.selectmsg(flask.request.form['messsageListItem'])
    if hasattr(data, 'error'): print("/selectmsg error", data) # render template error.html
    return flask.render_template('index.html', data=data)

@app.route('/get_files', methods=['POST'])
# загружаем файлы через форму 
def getFilesByPost():
    if 'file' not in flask.request.files:
        flask.flash('No file part')
        return 'No file part'
    files = flask.request.files.getlist("file")
    for file in files:
        if file.filename == '':
            flask.flash('No selected file')
            return 'No selected file'
        if file and allowed_file(file.filename):
            file.save(os.path.join('UploadFiles', file.filename))
    data = controller.getFilesByPOST(files)
    return flask.render_template('index.html', data=data)

@app.route('/get_mail', methods=['POST'])
# вызывается при выгрузки писем из сторонних почт, на фронте это форма "Загрузить из почты" с логином, паролем и список из google.com|yandex.ru
def getMail():
    data = controller.get_mail(flask.request.form['username'], flask.request.form['userpw'], flask.request.form['providerList'])
    return flask.render_template('index.html', data=data)

@app.route('/checkforspam', methods=['POST'])
def shalom():
    msg = controller.checkForSpam()
    data = {
        'status': 'OK',
        'message': msg,
    }
    print(json.dumps(data), type(json.dumps(data)))
    return json.dumps(data)

def allowed_file(filename):
    # проверяет формат файла, пропускает только .eml
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'eml'}

if __name__ == '__main__':  
    app.run('127.0.0.1', port=8000, debug=True)