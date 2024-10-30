import os
import re
import json
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from utils_db.models import Conversa
from utils_db.conecta_db import Base, usr, pwd, server, database
from urllib.parse import quote_plus
from utils.emoji_converter import substituir_emojis_por_texto
from utils.audio import converter_audio_para_texto
import shutil
from tqdm import tqdm

# Configuração do SQLAlchemy para se conectar ao banco de dados
conn_str = f"mssql+pyodbc://{usr}:{quote_plus(pwd)}@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server"
engine = create_engine(conn_str)
Session = sessionmaker(bind=engine)

# Configuração do logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Definir pastas de destino
diretorio_Conversas = os.path.join(os.getcwd(), 'conversas')
pasta_audios = os.path.join(diretorio_Conversas, "audios")
pasta_imagens = os.path.join(diretorio_Conversas, "imagens")
pasta_mensagens = os.path.join(diretorio_Conversas, "mensagens")
pasta_videos = os.path.join(diretorio_Conversas, "videos")
pasta_genericos = os.path.join(diretorio_Conversas, "outros")

# Criação das pastas, caso não existam
for pasta in [pasta_audios, pasta_imagens, pasta_mensagens, pasta_videos, pasta_genericos]:
    os.makedirs(pasta, exist_ok=True)

# Funções auxiliares
def limpar_nome_arquivo(nome_arquivo):
    return re.sub(r'[^\w\.\-_]', '', nome_arquivo)

def mover_arquivo(nome_arquivo, numero_celular, pasta_arquivo):
    nome_arquivo_limpo = limpar_nome_arquivo(nome_arquivo)
    caminho_arquivo = os.path.join(pasta_mensagens, nome_arquivo_limpo)
    destino_arquivo = os.path.join(pasta_arquivo, f"{numero_celular}_{os.path.basename(nome_arquivo_limpo)}")
    if os.path.exists(caminho_arquivo):
        shutil.move(caminho_arquivo, destino_arquivo)
        return destino_arquivo
    else:
        logging.warning(f"Arquivo não encontrado: {nome_arquivo_limpo}")
        return f"Arquivo não encontrado: {nome_arquivo_limpo}"

def processar_mensagem(mensagem, numero_celular):
    if "http" in mensagem:
        return f"Link encontrado: {mensagem}"
    if "(arquivo anexado)" in mensagem:
        caminho_anexo = mensagem.split()[0].strip()
        if ".jpg" in mensagem or ".png" in mensagem:
            return mover_arquivo(caminho_anexo, numero_celular, pasta_imagens) + " (Imagem Anexada)"
        elif ".mp4" in mensagem:
            return mover_arquivo(caminho_anexo, numero_celular, pasta_videos) + " (Vídeo Anexado)"
        elif ".wav" in mensagem:
            caminho_audio = limpar_nome_arquivo(caminho_anexo)
            diretorio_audio = os.path.join(pasta_mensagens, caminho_audio)
            caminho_audio_convertido = mover_arquivo(caminho_audio, numero_celular, pasta_audios)
            try:
                if os.path.isfile(diretorio_audio):
                    mensagem_convertida = converter_audio_para_texto(diretorio_audio)
                    return mensagem_convertida if mensagem_convertida else "Erro na conversão do áudio."
                else:
                    logging.warning(f"Arquivo de áudio não encontrado: {diretorio_audio}")
                    return f"Arquivo de áudio não encontrado: {diretorio_audio}"
            except Exception as e:
                logging.error(f"Erro ao converter áudio: {str(e)}")
                return f"Erro ao converter áudio: {str(e)}"
        else:
            return mover_arquivo(caminho_anexo, numero_celular, pasta_genericos) + " (Arquivo Anexado)"
    return substituir_emojis_por_texto(mensagem.strip())

def ler_conversa_para_json(caminho_arquivo):
    conversa_json = []
    numero_celular = os.path.basename(caminho_arquivo).replace(".txt", "")
    buffer_mensagem = ""

    with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
        primeira_linha = arquivo.readline().strip()
        if re.match(r"\d{2}/\d{2}/\d{4} \d{2}:\d{2} - As mensagens e as ligações são protegidas com a criptografia", primeira_linha):
            logging.info("Linha de criptografia detectada e ignorada.")
        else:
            arquivo.seek(0)

        for linha in arquivo:
            match = re.match(r"(\d{2}/\d{2}/\d{4}) (\d{2}:\d{2}) - (.*?): (.*)", linha)
            if match:
                if buffer_mensagem and conversa_json:
                    conversa_json[-1]["mensagem"] = processar_mensagem(buffer_mensagem, numero_celular)
                    buffer_mensagem = ""
                data, hora, remetente, mensagem = match.groups()
                conversa_json.append({
                    "data": data,
                    "hora": hora,
                    "remetente": remetente.split()[0],
                    "mensagem": processar_mensagem(mensagem, numero_celular)
                })
            else:
                buffer_mensagem += linha

    return numero_celular, json.dumps(conversa_json, ensure_ascii=False)

def salvar_conversa_no_banco(numero_celular, nova_conversa_json):
    with Session() as session:
        conversa_existente = session.query(Conversa).filter_by(Origem=numero_celular).first()
        if conversa_existente:
            resposta = input(f"Já existe uma conversa para {numero_celular}. Deseja adicionar a nova conversa ao registro existente? (s/n): ")
            if resposta.lower() == 's':
                # Adicionar a nova conversa à conversa existente
                conversa_atualizada = json.loads(conversa_existente.Conversa) + json.loads(nova_conversa_json)
                conversa_existente.Conversa = json.dumps(conversa_atualizada, ensure_ascii=False)
                session.commit()
                logging.info(f"Conversa adicionada ao registro existente para {numero_celular}.")
            else:
                logging.info("Conversa não adicionada.")
        else:
            nova_conversa = Conversa(Origem=numero_celular, Conversa=nova_conversa_json)
            session.add(nova_conversa)
            session.commit()
            logging.info(f"Nova conversa salva no banco para {numero_celular}.")

def processar_arquivos_texto(pasta_mensagens_arquivos):
    arquivos_txt = [arquivo for arquivo in os.listdir(pasta_mensagens_arquivos) if arquivo.endswith(".txt")]
    for arquivo in tqdm(arquivos_txt, desc="Processando arquivos de texto", unit="arquivo"):
        caminho_arquivo = os.path.join(pasta_mensagens_arquivos, arquivo)
        numero_celular, conversa_json = ler_conversa_para_json(caminho_arquivo)
        salvar_conversa_no_banco(numero_celular, conversa_json)

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    processar_arquivos_texto(pasta_mensagens)
    logging.info('Processamento concluído.')
