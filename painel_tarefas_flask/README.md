# Painel de Controle de Tarefas — Flask

Projeto baseado no exercício das páginas 40 e 41.

## Recursos

- Flask com templates
- SQLite
- Cadastro, login e logout
- Senhas com hash usando Werkzeug
- Sessão do Flask
- CRUD completo de tarefas
- Bootstrap 5
- Ícones Bootstrap
- Filtro de tarefas via API + fetch()
- Cards com cores por status
- Modo escuro persistido no localStorage
- Dashboard de progresso com Chart.js
- API REST em JSON
- Integração com Advice Slip API
- SECRET_KEY configurável por variável de ambiente
- DEBUG desativado por padrão

## 1. Criar ambiente virtual

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 2. Instalar dependências

```bash
pip install -r requirements.txt
```

## 3. Executar

```bash
python app.py
```

Abra no navegador:

```text
http://127.0.0.1:5000
```

O banco `banco.db` é criado automaticamente.

## 4. SECRET_KEY

Para desenvolvimento, o projeto possui uma chave padrão para facilitar o exercício.

Em um projeto real, defina uma chave própria.

Windows PowerShell:

```powershell
$env:SECRET_KEY="uma-chave-grande-e-secreta"
python app.py
```

## Rotas principais

- `/` — redireciona para login/dashboard
- `/login` — login
- `/cadastro` — cadastro
- `/logout` — sair
- `/dashboard` — painel e tarefas
- `/nova_tarefa` — criar tarefa
- `/editar/<id>` — editar tarefa
- `/excluir/<id>` — excluir tarefa
- `/progresso` — gráfico de progresso
- `/api/tarefas` — tarefas em JSON
- `/api/tarefas?status=Pendente` — filtro em JSON
- `/api/progresso` — quantidades por status
- `/api/frase` — frase motivacional

## Observação sobre o exercício

O enunciado usa `/dashboard` para a lista de tarefas e também menciona uma página adicional `/dashboard` para o gráfico. Como duas rotas iguais causariam conflito, este projeto mantém `/dashboard` como painel principal e usa `/progresso` para o gráfico.
