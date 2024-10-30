from sqlalchemy import (
    create_engine, 
    Column, 
    Integer, 
    String, 
    Date, 
    DECIMAL, 
    ForeignKey, 
    CheckConstraint, 
    CHAR,  
    NVARCHAR, 
    Boolean,
    Text,
    func
)

from utils_db.conecta_db import Base, usr, pwd, server, database  # Ajustando a importação
from sqlalchemy.orm import relationship, sessionmaker
from urllib.parse import quote_plus



class Conversa(Base):
    __tablename__ = 'conversas'
    
    ID = Column(Integer, primary_key=True, autoincrement=True)
    Origem = Column(String(15))  # Numero do celular
    Conversa = Column(Text)      # Armazena a conversa no formato JSON
    
    

