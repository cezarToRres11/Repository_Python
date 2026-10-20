# Dashboard de Vendas de Carros

Aplicação demonstrativa feita com Streamlit e Pandas para registrar vendas de veículos.

## Como executar

1. Instale Python 3.10 ou superior.
2. Abra o terminal na pasta do projeto.
3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

4. Execute o dashboard:

   ```bash
   streamlit run app.py
   ```

## Funcionalidades

- Catálogo de veículos com categoria, ano, preço e estoque demonstrativo.
- Formulário para adicionar veículos ao carrinho.
- Carrinho persistente durante as interações usando `st.session_state`.
- Validação de quantidade com base no estoque demonstrativo.
- Formulário de cliente e pagamento.
- Validação de valor recebido, mensagens de sucesso/aviso/erro e atualização com `st.rerun()`.
- Comprovante da última venda.
- Indicadores de faturamento, quantidade de vendas e veículos vendidos.
- Histórico de vendas e exportação CSV.

**Observação:** os dados ficam na sessão atual do Streamlit; não há banco de dados persistente. Os preços e estoques são exemplos e podem ser alterados no dicionário `CATALOGO` em `app.py`.
