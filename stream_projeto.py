import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Configuração do Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
#creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
#client = gspread.authorize(creds)
#sheet = client.open("Temas_CD").sheet1

# Use st.secrets para acessar a chave no Streamlit Cloud
credentials_dict = st.secrets["gcp_service_account"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, scope)
client = gspread.authorize(creds)
sheet = client.open("Temas_CD").sheet1

def carregar_dados():
    dados = sheet.get_all_records()
    return pd.DataFrame(dados)

def salvar_dados(grupo, integrantes, tema):
    data_hora = datetime.now().strftime("%d/%m/%Y %H:%M")
    sheet.append_row([grupo, integrantes, tema, data_hora])

# Lista de temas disponíveis
TEMAS = [
    "1. Churn (cancelamento de clientes)",
    "2. Fatores de risco para doenças cardíacas",
    "3. Desempenho de alunos",
    "4. Desempenho de atletas",
    "5. Previsão de demanda por componente",
    "6. Previsão de safras agrícolas",
    "7. Previsão do tempo de entrega de pacotes"
]

st.title("📘 Escolha do Tema para o Trabalho de Ciência de Dados")

codigo = st.text_input("Digite o código de acesso para continuar:", type="password")
if codigo != "cd2025":
    st.warning("🔒 Acesso restrito. Informe o código correto para continuar.")
    st.stop()

st.success("🔓 Acesso liberado!")

st.info("Escolha sua dupla e selecione um tema ainda disponível. Cada tema só pode ser escolhido uma vez.")

df = carregar_dados()
temas_ocupados = df["Tema"].tolist() if not df.empty else []
temas_disponiveis = [t for t in TEMAS if t not in temas_ocupados]

with st.form("form_escolha"):
    grupo = st.text_input("Número do grupo (ex: Grupo 1)")
    integrantes = st.text_input("Nome dos integrantes (ex: João e Maria)")
    tema_escolhido = st.selectbox("Tema disponível:", temas_disponiveis)
    enviar = st.form_submit_button("Enviar Escolha")

    if enviar:
        if tema_escolhido in temas_ocupados:
            st.warning("❌ Esse tema já foi escolhido por outro grupo.")
        elif grupo and integrantes:
            salvar_dados(grupo, integrantes, tema_escolhido)
            st.success("✅ Escolha registrada com sucesso!")
            st.rerun()
        else:
            st.warning("⚠️ Preencha todos os campos para registrar sua escolha.")

st.markdown("---")

st.subheader("📋 Temas já escolhidos")
df = carregar_dados()
if not df.empty:
    st.dataframe(df[["Grupo", "Integrantes", "Tema"]].sort_values("Grupo"))
else:
    st.write("Nenhum grupo fez a escolha ainda.")
