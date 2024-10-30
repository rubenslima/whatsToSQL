import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from utils_db.models import Conversa  # Importando o modelo correto
from utils_db.conecta_db import Base, usr, pwd, server, database  # Ajustando a importação
import json
from urllib.parse import quote_plus

# Configuração do SQLAlchemy
conn_str = f"mssql+pyodbc://{usr}:{quote_plus(pwd)}@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server"
engine = create_engine(conn_str)
Session = sessionmaker(bind=engine)
session = Session()

# Função para obter conversas do banco de dados
def obter_conversas():
    conversas = session.query(Conversa).all()
    return conversas

# Função principal do aplicativo Streamlit
def main():
    st.title("Exibição de Conversas do WhatsApp")

    # Obtendo as conversas do banco de dados
    conversas = obter_conversas()

    if not conversas:
        st.warning("Nenhuma conversa encontrada no banco de dados.")
        return

    # Seleção de conversa por número
    numero_celular = st.selectbox("Selecione um número de celular", [conversa.Origem for conversa in conversas])
    
    # Exibindo a conversa selecionada
    if numero_celular:
        conversa_selecionada = next((conversa for conversa in conversas if conversa.Origem == numero_celular), None)
        if conversa_selecionada:
            st.subheader(f"Conversa com: {numero_celular}")
            conversa_json = json.loads(conversa_selecionada.Conversa)
            
            for mensagem in conversa_json:
                st.write(f"**{mensagem['data']} {mensagem['hora']} - {mensagem['remetente']}:** {mensagem['mensagem']}")

if __name__ == "__main__":
    main()
