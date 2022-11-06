from flask import Blueprint, Flask, request, render_template, json
from blueprint_query.route import blueprint_query


app = Flask(__name__)
app.register_blueprint(blueprint_query, url_prefix='/zaproses')


with open('data_files/dbconfig.json', 'r') as f:
    db_config = json.load(f)
app.config['dbconfig'] = db_config


@app.route('/')
def index():
    return render_template('start_request.html')


@app.route('/goodbye')
def goodbye():
    return 'Bye'


@app.route('/greeting/')
@app.route('/greeting/<name>')
def greeting_handler(name: str = None) -> str:
    str = 'Hello, '
    if name is None:
         str += 'unknown'
    else:
        str += name
    return str


@app.route('/form', methods=['GET', 'POST'])
def form_handler():
    if request.method == 'GET':
        return render_template('form.html')
    else:
        login = request.form.get('login')
        password = request.form.get('password')
        return f'Login: {login}, Password: {password}'


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001)