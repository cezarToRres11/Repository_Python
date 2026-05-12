from flask import Flask


app = Flask(__name__) # inicio o flask

@app.route('/') # Isso é o decorator, ele é usado para mapear a função abaixo para a rota '/'
def ola_mundo():
    return 'Olá, Mundo!' # Isso é o que será retornado quando a rota '/' for acessada

@app.route('/decorator') # Isso é outro decorator, mapeando a função abaixo para a rota '/hello'
def hello():
    return 'Um decorator é uma ferramenta que "embrulha" uma função para adicionar novos comportamentos sem mudar o código original, usando o símbolo @. Serve para reutilizar lógica (como segurança ou logs) em várias partes do projeto de forma limpa.No Flask, ele é usado principalmente para:Rotas: Associar URLs a funções (@app.route).Segurança: Bloquear páginas para usuários não logados.Automação: Rodar códigos antes ou depois de cada clique no site.Quer que eu monte um exemplo de código curto com esses pontos?' # Isso é o que será retornado quando a rota '/hello' for acessada

if __name__ == '__main__':
    app.run(debug=True) # Isso inicia o servidor Flask em modo de depuração, o que é útil para desenvolvimento
