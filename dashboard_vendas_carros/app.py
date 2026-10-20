import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Dashboard de Vendas de Carros",
    page_icon="🚗",
    layout="wide"
)

# Catálogo demonstrativo: altere os modelos e preços conforme necessário.
CATALOGO = {
    "Fiat Mobi Like 1.0": {"categoria": "Hatch", "ano": 2025, "preco": 69990.00, "estoque": 5},
    "Hyundai HB20 Comfort 1.0": {"categoria": "Hatch", "ano": 2025, "preco": 84990.00, "estoque": 4},
    "Chevrolet Onix LT 1.0": {"categoria": "Hatch", "ano": 2025, "preco": 89990.00, "estoque": 3},
    "Volkswagen Polo Track 1.0": {"categoria": "Hatch", "ano": 2025, "preco": 87990.00, "estoque": 4},
    "Toyota Corolla GLi 2.0": {"categoria": "Sedã", "ano": 2025, "preco": 154990.00, "estoque": 2},
    "Honda Civic Advanced Hybrid": {"categoria": "Sedã", "ano": 2025, "preco": 199990.00, "estoque": 1},
    "Jeep Renegade Sport T270": {"categoria": "SUV", "ano": 2025, "preco": 119990.00, "estoque": 3},
    "Hyundai Creta Comfort 1.0 TGDI": {"categoria": "SUV", "ano": 2025, "preco": 139990.00, "estoque": 2},
    "BYD Dolphin Mini": {"categoria": "Elétrico", "ano": 2025, "preco": 115800.00, "estoque": 2},
}

# Corrige-se o preço do Civic caso você edite o catálogo acima.
CATALOGO["Honda Civic Advanced Hybrid"]["preco"] = 199990.00

if "carrinho" not in st.session_state:
    st.session_state.carrinho = []
if "vendas" not in st.session_state:
    st.session_state.vendas = []
if "ultima_venda" not in st.session_state:
    st.session_state.ultima_venda = None

def moeda(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

st.title("🚗 Dashboard de Vendas de Carros")
st.caption("Sistema demonstrativo de concessionária — seleção de veículos, carrinho e fechamento de venda.")
st.markdown("---")

# Indicadores gerais
total_vendido = sum(v["Total (R$)"] for v in st.session_state.vendas)
qtd_vendas = len(st.session_state.vendas)
qtd_veiculos = sum(v["Qtd. veículos"] for v in st.session_state.vendas)

m1, m2, m3 = st.columns(3)
m1.metric("Faturamento registrado", moeda(total_vendido))
m2.metric("Vendas concluídas", qtd_vendas)
m3.metric("Veículos vendidos", qtd_veiculos)
st.markdown("---")

col1, col2 = st.columns([1.1, 1], gap="large")

with col1:
    st.subheader("🛞 Seleção de veículos")
    with st.form("form_veiculo", clear_on_submit=False):
        modelo = st.selectbox("Modelo do veículo", list(CATALOGO.keys()))
        dados = CATALOGO[modelo]
        info1, info2 = st.columns(2)
        info1.caption(f"Categoria: **{dados['categoria']}**")
        info2.caption(f"Ano: **{dados['ano']}**")
        st.write(f"**Preço unitário:** {moeda(dados['preco'])}")
        st.write(f"**Estoque demonstrativo:** {dados['estoque']} unidade(s)")
        quantidade = st.number_input(
            "Quantidade", min_value=1, max_value=dados["estoque"], value=1, step=1
        )
        adicionar = st.form_submit_button("Adicionar ao carrinho", use_container_width=True)

        if adicionar:
            ja_adicionado = sum(
                item["Qtd."] for item in st.session_state.carrinho
                if item["Modelo"] == modelo
            )
            if ja_adicionado + quantidade > dados["estoque"]:
                st.error("A quantidade no carrinho ultrapassa o estoque demonstrativo.")
            else:
                st.session_state.carrinho.append({
                    "Modelo": modelo,
                    "Categoria": dados["categoria"],
                    "Ano": dados["ano"],
                    "Preço unit. (R$)": dados["preco"],
                    "Qtd.": int(quantidade),
                    "Subtotal (R$)": dados["preco"] * quantidade,
                })
                st.success(f"{modelo} adicionado ao carrinho!")
                st.rerun()

    st.subheader("🛒 Carrinho da venda")
    if st.session_state.carrinho:
        df_carrinho = pd.DataFrame(st.session_state.carrinho)
        st.dataframe(
            df_carrinho,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Preço unit. (R$)": st.column_config.NumberColumn("Preço unitário", format="R$ %.2f"),
                "Subtotal (R$)": st.column_config.NumberColumn("Subtotal", format="R$ %.2f"),
                "Qtd.": st.column_config.NumberColumn("Qtd.", format="%d"),
            }
        )
        total_compra = sum(item["Subtotal (R$)"] for item in st.session_state.carrinho)
        st.metric("Total da venda", moeda(total_compra))
        if st.button("Limpar carrinho", use_container_width=True):
            st.session_state.carrinho = []
            st.rerun()
    else:
        total_compra = 0.0
        st.info("O carrinho está vazio. Selecione um veículo acima para começar.")

with col2:
    st.subheader("💳 Dados do cliente e pagamento")
    with st.form("form_pagamento"):
        cliente = st.text_input("Nome do cliente")
        documento = st.text_input("CPF/CNPJ (opcional)")
        forma_pagamento = st.selectbox(
            "Forma de pagamento",
            ["Pix", "Dinheiro", "Cartão de crédito", "Cartão de débito", "Financiamento", "Transferência"]
        )
        valor_recebido = st.number_input(
            "Valor recebido / entrada (R$)", min_value=0.0, value=0.0, step=1000.0, format="%.2f"
        )
        finalizar = st.form_submit_button("Concluir venda", type="primary", use_container_width=True)

    total_compra = sum(item["Subtotal (R$)"] for item in st.session_state.carrinho)
    if finalizar:
        if not st.session_state.carrinho:
            st.warning("Adicione pelo menos um veículo ao carrinho antes de concluir a venda.")
        elif not cliente.strip():
            st.warning("Informe o nome do cliente para registrar a venda.")
        elif forma_pagamento in ["Dinheiro", "Pix", "Cartão de crédito", "Cartão de débito", "Transferência"] and valor_recebido < total_compra:
            st.error(f"Valor insuficiente. Faltam {moeda(total_compra - valor_recebido)} para cobrir o total.")
        elif forma_pagamento == "Financiamento" and valor_recebido > total_compra:
            st.warning("A entrada não pode ser maior que o valor total da venda.")
        else:
            venda = {
                "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "Cliente": cliente.strip(),
                "CPF/CNPJ": documento.strip() or "Não informado",
                "Veículos": ", ".join(f'{item["Qtd."]}x {item["Modelo"]}' for item in st.session_state.carrinho),
                "Qtd. veículos": sum(item["Qtd."] for item in st.session_state.carrinho),
                "Forma de pagamento": forma_pagamento,
                "Total (R$)": total_compra,
                "Valor recebido/entrada (R$)": valor_recebido,
                "Saldo (R$)": max(0.0, total_compra - valor_recebido),
            }
            st.session_state.vendas.append(venda)
            st.session_state.ultima_venda = venda
            st.session_state.carrinho = []
            st.success("Venda registrada com sucesso!")
            st.rerun()

    if st.session_state.ultima_venda:
        with st.expander("Ver comprovante da última venda", expanded=False):
            venda = st.session_state.ultima_venda
            st.write(f"**Cliente:** {venda['Cliente']}")
            st.write(f"**Veículos:** {venda['Veículos']}")
            st.write(f"**Pagamento:** {venda['Forma de pagamento']}")
            st.write(f"**Total:** {moeda(venda['Total (R$)'])}")
            st.write(f"**Valor recebido/entrada:** {moeda(venda['Valor recebido/entrada (R$)'])}")
            st.write(f"**Saldo restante:** {moeda(venda['Saldo (R$)'])}")
            st.write(f"**Data:** {venda['Data']}")

st.markdown("---")
st.subheader("📊 Histórico de vendas")
if st.session_state.vendas:
    df_vendas = pd.DataFrame(st.session_state.vendas)
    st.dataframe(
        df_vendas,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Total (R$)": st.column_config.NumberColumn("Total", format="R$ %.2f"),
            "Valor recebido/entrada (R$)": st.column_config.NumberColumn("Recebido/entrada", format="R$ %.2f"),
            "Saldo (R$)": st.column_config.NumberColumn("Saldo", format="R$ %.2f"),
        }
    )
    csv = df_vendas.to_csv(index=False).encode("utf-8-sig")
    st.download_button("Baixar histórico em CSV", data=csv, file_name="historico_vendas_carros.csv", mime="text/csv")
else:
    st.info("Ainda não há vendas registradas nesta sessão.")

with st.expander("📋 Catálogo completo de veículos"):
    df_catalogo = pd.DataFrame([
        {"Modelo": nome, "Categoria": dados["categoria"], "Ano": dados["ano"],
         "Preço (R$)": dados["preco"], "Estoque": dados["estoque"]}
        for nome, dados in CATALOGO.items()
    ])
    st.dataframe(
        df_catalogo, use_container_width=True, hide_index=True,
        column_config={"Preço (R$)": st.column_config.NumberColumn("Preço", format="R$ %.2f")}
    )
