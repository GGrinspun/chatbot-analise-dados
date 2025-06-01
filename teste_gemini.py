import os
import google.generativeai as genai
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env (se você estiver usando um)
load_dotenv()

# Configura a API Key
# Certifique-se de que a variável de ambiente GOOGLE_API_KEY está definida no seu .env
# ou substitua os.getenv("GOOGLE_API_KEY") diretamente pela sua chave "SUA_API_KEY_REAL"
try:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        # Se não estiver no .env, substitua a string abaixo pela sua chave diretamente
        if api_key == "bbb": # Verifica se ainda é o placeholder
            raise ValueError("API Key não encontrada. Defina GOOGLE_API_KEY no seu ambiente ou substitua o placeholder no código.")
    genai.configure(api_key=api_key)
except ValueError as e:
    print(e)
    exit()
except Exception as e:
    print(f"Ocorreu um erro ao configurar a API Key: {e}")
    exit()


# Escolha o modelo.
# 'gemini-1.5-flash-latest' é uma boa opção para ser rápido e eficiente.
# 'gemini-pro' também é uma opção popular.
model_name = 'gemini-1.5-flash-latest' # Ou 'gemini-pro'

try:
    # Cria o modelo generativo
    model = genai.GenerativeModel(model_name)

    # Gera o conteúdo
    prompt = "quantos dedos um humano tem, normalmente??"
    response = model.generate_content(prompt)

    # Imprime a resposta
    if response and response.text:
        print(response.text)
    else:
        print("Não foi possível obter uma resposta do modelo.")
        if response:
            print("Detalhes da resposta (se houver partes bloqueadas):")
            print(response.prompt_feedback) # Para verificar se o prompt foi bloqueado

except Exception as e:
    print(f"Ocorreu um erro ao gerar conteúdo: {e}")