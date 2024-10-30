import speech_recognition as sr  # Para converter áudio em texto (opcional)

# def limpar_nome_arquivo(nome_arquivo):
#     return re.sub(r'[^\w\.\-_]', '', nome_arquivo)

    
# Função para converter áudio em texto
def converter_audio_para_texto(caminho_audio):
    reconhecedor = sr.Recognizer()
    with sr.AudioFile(caminho_audio) as fonte_audio:
        audio = reconhecedor.record(fonte_audio)
        try:
            texto_convertido = reconhecedor.recognize_google(audio, language="pt-BR")
            return f"Transcrição audio: {texto_convertido}"
        except sr.UnknownValueError:
            return "Áudio não pôde ser reconhecido."
        except sr.RequestError:
            return "Erro na conexão com o serviço de reconhecimento de voz."