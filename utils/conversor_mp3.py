from pydub import AudioSegment
import os

def convert_opus_to_mp3(input_file, output_file):
    try:
        # Carrega o arquivo OPUS
        sound = AudioSegment.from_file(input_file)

        # Exporta para MP3
        sound.export(output_file, format="mp3")
        print(f"Arquivo convertido com sucesso: {output_file}")

    except Exception as e:
        print(f"Erro durante a conversão de {input_file}: {e}")

def convert_all_opus_in_directory(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.opus'):
                input_file = os.path.join(root, file)
                output_file = os.path.splitext(input_file)[0] + '.mp3'
                convert_opus_to_mp3(input_file, output_file)

# Exemplo de uso:
directory = "conversas\\mensagens"  # Substitua pelo seu caminho
convert_all_opus_in_directory(directory)
