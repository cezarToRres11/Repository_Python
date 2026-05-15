from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def exibir_curriculo():
    return render_template('index.html')


@app.route('/cotemig/<nome>')
def saudar_usuario(nome):
    return f"<h1>Ola {nome}!, Bem-vindo ao COTEMIG.</h1>"

if __name__ == '__main__':
    app.run(debug=True)

