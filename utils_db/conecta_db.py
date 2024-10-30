from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os


# Base para nossas tabelas
Base = declarative_base()

# Carregar variáveis de ambiente
load_dotenv()

# Recuperar as variáveis do arquivo .env
server = os.getenv('SERVIDOR')
usr = os.getenv('USUARIO')
pwd = os.getenv('SENHA')
database = os.getenv('BANCO')
