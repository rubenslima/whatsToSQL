import re
import emoji

def substituir_emojis(texto, substituicao='[emoji]'):
    # Cria uma expressão regular para capturar todos os emojis
    emojis = sorted(emoji.EMOJI_DATA, key=len, reverse=True)
    pattern = '(' + '|'.join(re.escape(u) for u in emojis) + ')'
    emoji_regex = re.compile(pattern)
    
    return emoji_regex.sub(repl=substituicao, string=texto)


def substituir_emojis_por_texto(texto):
    def _emoji_to_ascii(c):
        if c in emoji.EMOJI_DATA:   
            return emoji.demojize(c, language='pt')   
        else:
            return c
    return ''.join(map(_emoji_to_ascii, texto))


