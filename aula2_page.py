from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return '''
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Currículo</title>
        </head>
        <body>
            <h1>Currículo</h1>

            <h2>Informações Pessoais</h2>
            <ul>
                <li><strong>Nome:</strong> Arthur Cezar</li>  
                <li><strong>Email:</strong> 12401650@aluno.cotemig.com.br</li>
                <li><strong>Telefone:</strong> (31) 99365-4035</li>
                <li><strong>Local:</strong> Belo Horizonte</li>
            </ul>
            
            <h2>Historico Escolar</h2>
            <ul>
                <li><strong>Ensino Fundamental:</strong> Santa Maria Minas</li>
                <li><strong>Ensino Medio:</strong> Cottemig Barroca - 3° ano em andamento</li>
                <li><strong>Idiomas:</strong> Ingles - nivel basico , Espanhol - nivel intermediario</li>
                
            </ul>

            <h2>Experiência Profissional</h2>
            <ul>
                <li><strong>Empresa:</strong> Emfal</li>
                <li><strong>Cargo:</strong> HelpDesk</li>
                <li><strong>Período:</strong> Abr 2025 - Presente</li>
            </ul>
        </body>
        </html>
    '''

if __name__ == '__main__':
    app.run(debug=True)
