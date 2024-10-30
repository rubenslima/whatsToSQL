# Processador de Conversas de Mensagens

Este projeto em Python permite processar conversas em arquivos .txt para armazená-las em um banco de dados SQL Server. O script identifica e processa mensagens, incluindo arquivos anexados (imagens, vídeos, áudios) e links, além de lidar com casos onde uma nova mensagem precisa ser concatenada a uma conversa já existente.


## Visão Geral

Este script processa mensagens armazenadas em arquivos .txt e salva o conteúdo estruturado em JSON em um banco de dados SQL Server. Para mensagens de uma mesma origem (número de celular) que já possuem registro no banco, o usuário é notificado e pode optar por concatenar a nova conversa ao registro existente, evitando duplicação de dados.


## Funcionalidades

- Processamento de mensagens e detecção de anexos (áudio, imagem, vídeo).
- Armazenamento de mensagens em formato JSON no banco de dados.
- Conversão de áudio para texto, substituição de emojis e links por texto.
- Mensagem de alerta para identificar mensagens duplicadas de uma mesma origem e opção para atualizar o JSON existente.

## Requisitos

- Python 3.7 ou superior
- Dependências do projeto (especificadas em `requirements.txt`)
- Driver ODBC para SQL Server

## Tecnologias Utilizadas

- **SQLAlchemy**: Para a conexão e manipulação do banco de dados.
- **shutil e tqdm**: Para manipulação de arquivos e exibição de progresso.
- **Regex e JSON**: Para manipulação e armazenamento de mensagens.

## Banco de Dados

Crie a tabela necessária no banco de dados para armazenar as conversas:
```SQL
CREATE TABLE Conversa (
    ID INT PRIMARY KEY IDENTITY,
    Origem VARCHAR(20),
    Conversa NVARCHAR(MAX)
);
```

## Estrutura de Pastas
- Conversas/
  - audios/
  - imagens/
  - mensagens/
  - videos/
  - outros/

## Como Usar

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/seu-usuario/conversas-processor.git
   cd conversas-processor

## Execução
Para rodar o script, execute o comando abaixo no terminal:
```bash
python processador_conversas.py
```

Durante a execução:
- O script pedirá confirmação caso já exista uma conversa para o mesmo número no banco de dados.
- As mensagens e arquivos anexados serão processados e salvos nas respectivas pastas


## Organização do Projeto
- processador_conversas.py: Script principal que executa o processamento das mensagens.
- utils_db/: Contém configurações e modelos de banco de dados, como models.py e conecta_db.py
- utils/: Módulos de utilidades, incluindo funções para conversão de áudio e emojis.
- conversas/: Diretório onde os arquivos processados são organizados (audios, imagens, etc.).

## Licença

Este projeto é distribuído sob a licença GNU General Public License (GPL). Veja o arquivo LICENSE para mais detalhes.

