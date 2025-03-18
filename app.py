

import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

# Interface Streamlit
def main():
    st.title("ERP Financeiro com Streamlit")
    
    menu = ["Clientes", "Contas a Pagar", "Contas a Receber", "Lançamentos", "Relatórios", "Top 5 Clientes"]
    choice = st.sidebar.selectbox("Selecione uma opção", menu)
    conn = sqlite3.connect("erp_finance.db", detect_types=sqlite3.PARSE_DECLTYPES)
    cursor = conn.cursor()
    
    if choice == "Clientes":
        st.subheader("Cadastro de Clientes")
        df = pd.read_sql_query("SELECT * FROM clientes", conn)
        st.dataframe(df)
        
    elif choice == "Contas a Pagar":
        st.subheader("Contas a Pagar")
        df = pd.read_sql_query("SELECT * FROM contas_pagar", conn)
        st.dataframe(df)
        
    elif choice == "Contas a Receber":
        st.subheader("Contas a Receber")
        df = pd.read_sql_query("SELECT * FROM contas_receber", conn)
        st.dataframe(df)
        
    elif choice == "Lançamentos":
        st.subheader("Lançamentos Financeiros")
        df = pd.read_sql_query("SELECT * FROM lancamentos", conn)
        st.dataframe(df)
        
    elif choice == "Relatórios":
        st.subheader("Relatório de Fluxo de Caixa")
        df = pd.read_sql_query("SELECT strftime('%Y-%m', data) AS mes, tipo, SUM(valor) as total FROM lancamentos GROUP BY mes, tipo", conn)
        
        if not df.empty:
            df_pivot = df.pivot(index="mes", columns="tipo", values="total").fillna(0)
            df_pivot["Saldo"] = df_pivot.get("Receita", 0) - df_pivot.get("Despesa", 0)
            
            st.dataframe(df_pivot)
            
            # Gráfico de barras
            st.subheader("Gráfico de Fluxo de Caixa")
            fig, ax = plt.subplots()
            df_pivot[["Receita", "Despesa"]].plot(kind="bar", stacked=True, ax=ax)
            plt.xlabel("Mês")
            plt.ylabel("Valor (R$)")
            plt.title("Fluxo de Caixa por Mês")
            plt.xticks(rotation=45)
            st.pyplot(fig)
        
        # Distribuição das Contas a Pagar por Fornecedor
        st.subheader("Distribuição das Contas a Pagar por Fornecedor")
        df_fornecedores = pd.read_sql_query("SELECT fornecedor, SUM(valor) as total FROM contas_pagar GROUP BY fornecedor ORDER BY total DESC", conn)
        
        if not df_fornecedores.empty:
            fig, ax = plt.subplots()
            wedges, texts, autotexts = ax.pie(df_fornecedores["total"], labels=df_fornecedores["fornecedor"], autopct='%1.1f%%', startangle=90, textprops={'fontsize': 6})
            
            plt.title("Distribuição das Contas a Pagar por Fornecedor")
            st.pyplot(fig)
    
    elif choice == "Top 5 Clientes":
        st.subheader("Top 5 Clientes com Maior Receita")
        
        # Consulta para obter os 5 clientes com maior receita
        df_receita = pd.read_sql_query("""
            SELECT c.nome, SUM(r.valor) as total_receita
            FROM clientes c
            JOIN contas_receber r ON c.id = r.cliente_id
            GROUP BY c.nome
            ORDER BY total_receita DESC
            LIMIT 5
        """, conn)
        
        if not df_receita.empty:
            # Exibe a tabela com os top 5 clientes
            st.dataframe(df_receita)
            
            # Gráfico de barras para os top 5 clientes
            fig, ax = plt.subplots()
            ax.bar(df_receita["nome"], df_receita["total_receita"], color='skyblue')
            plt.xlabel("Clientes")
            plt.ylabel("Receita (R$)")
            plt.title("Top 5 Clientes com Maior Receita")
            plt.xticks(rotation=45)
            st.pyplot(fig)
    
    conn.close()
    
if __name__ == "__main__":
    main()

