# 🤖 Chatbot de Análise de Dados com Gemini

Este projeto é um chatbot interativo que permite fazer perguntas sobre um conjunto de dados carregado na nuvem da AWS e obter análises e visualizações geradas automaticamente com o auxílio da API Gemini da Google. 

Ele utiliza `pandas` para manipulação dos dados e `matplotlib` para visualização gráfica, integrados com um modelo de linguagem para interpretar as perguntas em código Python e executar análises em tempo real.

![image](https://github.com/user-attachments/assets/1cef942d-beca-4d9f-a46a-c23e6e8141ee)

---

## Exemplo de funcionamento



https://github.com/user-attachments/assets/28b274c2-4b29-40b6-b466-05f45ed72ac3



link para o video completo no youtube: https://youtu.be/NFT1O7GbTdA

---

## Pré-requisitos

- Python 3.8+
- Conta Google Cloud com acesso à API Gemini (Gemini-1.5-flash-latest)
- Chave da API Gemini (`GEMINI_API_KEY`)
- AWS S3 configurado (para carregar o CSV com os dados)
- Ambiente virtual recomendado (`venv`)

---

## Instalação

1. Clone este repositório:
    ```bash
    git clone https://github.com/(copie e cole o nome desse repositorio)
    cd SEU_REPOSITORIO
    ```

2. Crie e ative um ambiente virtual:
    ```bash
    python -m venv venv
    source venv/bin/activate   # Linux/macOS
    venv\Scripts\activate      # Windows
    ```

3. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

4. Configure suas variáveis de ambiente no arquivo `.env` (exemplo no próximo tópico, copie e cole o arquivo Exemplo_env.txt em um arquivo .env substitua por suas credenciais).

5. modifique o caminho do o arquivo que voce seseja subir para o seu bucket no arquivo `s3_setup.py` em:

```
if __name__ == "__main__":
    criar_bucket()
    enviar_arquivo("caminho/para/seu/arquivo.csv", os.getenv("S3_FILE"))
```

---

## Formato Esperado:

Arquivo `.env` na raiz do projeto deve conter:

```env
GEMINI_API_KEY=seu_token_gemini_aqui
AWS_ACCESS_KEY_ID=sua_chave_aws
AWS_SECRET_ACCESS_KEY=sua_chave_secreta_aws
AWS_S3_BUCKET=nome_do_bucket
AWS_REGION=regiao_do_bucket
```

## Descrição dos Arquivos

- `app_Gemini_trat_erros.py`:  
  Aplicação principal em Streamlit que integra o chatbot com a API Gemini, executa código Python gerado pela IA e mostra gráficos e resultados interativos.

- `s3_reader.py`:  
  Contém função para carregar o arquivo CSV armazenado no AWS S3, utilizando as credenciais e configurações definidas no `.env`. Retorna um DataFrame pandas para análise.

- `s3_setup.py`:  
  Script para criação do bucket no S3 (caso não exista) e para envio de arquivos locais para o bucket configurado. Também usa variáveis do `.env` para credenciais e configurações.

- `teste_gemini.py`:  
  Script de teste para verificar se a integração com a API Gemini está funcionando corretamente, configurando a API Key, criando o modelo e gerando uma resposta simples.

- `teste_leitura.py`:  
  Script simples para testar a função de leitura do CSV do S3 (`carregar_csv_do_s3`). Ele carrega o DataFrame e exibe as primeiras linhas no console para verificar se o carregamento foi bem-sucedido.

- `.env` (não versionado):  
  Arquivo de configuração onde ficam armazenadas as chaves secretas e variáveis de ambiente, como a API Key do Gemini e credenciais AWS.

- `.gitignore`:  
  Lista arquivos e pastas que não devem ser versionados, garantindo que a `venv` e o `.env` fiquem fora do repositório.

- `requirements.txt`:  
  Lista as dependências Python do projeto para facilitar a instalação do ambiente.

- `README.md`:  
  Este arquivo, que explica o projeto, como configurar, usar e contribuir.

- `venv/` (não versionado):  
  Ambiente virtual com as bibliotecas instaladas, isolado do sistema global.

