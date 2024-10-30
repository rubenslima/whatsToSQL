import os

# Defina o diretório base
diretorio_base = os.path.join(os.getcwd(), 'conversas')

# Atualize o dicionário com os caminhos completos
pastas_destino = {
    "audios": os.path.join(diretorio_base, "audios"),
    "imagens": os.path.join(diretorio_base, "imagens"),
    "mensagens": os.path.join(diretorio_base, "mensagens"),
    "videos": os.path.join(diretorio_base, "videos"),
    "outros": os.path.join(diretorio_base, "outros")
}

def verificar_criar_pastas(pastas):
    for nome, caminho in pastas.items():
        if not os.path.exists(caminho):
            os.makedirs(caminho)
            print(f"Pasta criada: {caminho}")
        else:
            print(f"Pasta já existe: {caminho}")

verificar_criar_pastas(pastas_destino)
