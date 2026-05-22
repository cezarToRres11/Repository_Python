from flask import Flask, render_template, request

app = Flask(__name__)

# Lista contendo dicionários de usuários autorizados
usuarios_permitidos = [
    {"usuario": "marcos", "senha": "cotemig2026"},
    {"usuario": "janaina", "senha": "cotemig2026"},
    {"usuario": "arthur", "senha": "12401650"},
    {"usuario": "pedro", "senha": "cotemig2026"},
    {"usuario": "joao", "senha": "cotemig2026"},
    {"usuario": "caio", "senha": "cotemig2026"}  
]

@app.route('/', methods=['GET', 'POST'])
def login():
    mensagem = None
    
    if request.method == 'POST':
        # Captura os dados enviados via formulário HTTP POST
        usuario_digitado = request.form.get('input_usuario')
        senha_digitada = request.form.get('input_senha')
        
        acesso_concedido = False
        
        # Percorre a lista de dicionários para checar as credenciais
        for registro in usuarios_permitidos:
            if registro["usuario"] == usuario_digitado and registro["senha"] == senha_digitada:
                acesso_concedido = True
                break  # Para o loop se encontrar correspondência válida
        
        if acesso_concedido:
            return render_template('dashboard.html', nome_usuario=usuario_digitado)
        else:
            mensagem = "Usuário ou senha incorretos! Tente novamente."

    return render_template('login.html', erro=mensagem)

if __name__ == '__main__':
    app.run(debug=True)
