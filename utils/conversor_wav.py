from pydub import AudioSegment
import os

def convert_opus_to_wav(input_file, output_file):
    try:
        # Carrega o arquivo OPUS
        sound = AudioSegment.from_file(input_file)

        # Exporta para wav
        sound.export(output_file, format="wav")
        print(f"Arquivo convertido com sucesso: {output_file}")

    except Exception as e:
        print(f"Erro durante a conversão de {input_file}: {e}")

def convert_all_opus_in_directory(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.opus'):
                input_file = os.path.join(root, file)
                output_file = os.path.splitext(input_file)[0] + '.wav'
                convert_opus_to_wav(input_file, output_file)

def substituir_palavras(diretorio_raiz, palavra_antiga, palavra_nova):
    for root, _, files in os.walk(diretorio_raiz):
        for file in files:
            if file.endswith(".txt"):
                caminho_arquivo = os.path.join(root, file)

                try:
                    # Lê o arquivo com codificação utf-8
                    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
                        conteudo = f.read()

                    # Substitui a palavra
                    novo_conteudo = conteudo.replace(palavra_antiga, palavra_nova)

                    # Escreve de volta o conteúdo no arquivo com codificação utf-8
                    with open(caminho_arquivo, 'w', encoding='utf-8') as f:
                        f.write(novo_conteudo)

                    print(f"Conteúdo do arquivo {file} modificado.")
                
                except UnicodeDecodeError:
                    print(f"Erro de codificação ao ler o arquivo {file}. Verifique a codificação.")

directory = "conversas\\mensagens"  

convert_all_opus_in_directory(directory)
substituir_palavras(directory, "opus", "wav") 
