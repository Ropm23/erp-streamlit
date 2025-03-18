
import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

# Interface Streamlit
def main():
    st.title("ERP Financeiro com Streamlit")
    
    menu = ["Clientes", "Contas a Pagar", "Contas a Receber", "Lançamentos", "Relatórios"]
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
    
    conn.close()
    
if __name__ == "__main__":
    main()

