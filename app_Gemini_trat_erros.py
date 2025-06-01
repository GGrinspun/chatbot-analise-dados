import streamlit as st
import matplotlib.pyplot as plt
from s3_reader import carregar_csv_do_s3
import google.generativeai as genai
import os
from dotenv import load_dotenv
import re
import traceback
import logging
from google.api_core.exceptions import GoogleAPIError

# Configurar logging
logging.basicConfig(level=logging.INFO)

# Carregar variáveis de ambiente
load_dotenv()

# Configurar API Key do Gemini
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("API Key da Gemini não encontrada. Defina GEMINI_API_KEY no seu .env.")
    st.stop()
genai.configure(api_key=api_key)

# Criar modelo
model = genai.GenerativeModel("gemini-1.5-flash-latest")

# Carregar dataset do S3
df = carregar_csv_do_s3()

st.title("🤖 Chatbot de Análise de Dados com Gemini")

# Mostrar dataset
if st.checkbox("Mostrar dataset"):
    st.dataframe(df)

# Formulário para entrada de pergunta com botão de envio
with st.form(key="pergunta_form"):
    pergunta = st.text_input("Faça uma pergunta sobre os dados:", "")
    submitted = st.form_submit_button("Enviar")

def executar_codigo(codigo, df, plt):
    """
    Executa o código Python recebido com acesso completo.
    """
    exec_locals = {"df": df.copy(), "plt": plt}
    exec(codigo, globals(), exec_locals)
    return exec_locals

if submitted and pergunta:
    st.write("🔍 Interpretando sua pergunta com IA...")

    # Prompt para Gemini
    prompt = f"""
Você é um cientista de dados experiente utilizando pandas e matplotlib.

Considere que você está fazendo análise em um DataFrame chamado `df`, que já está carregado e contém as seguintes colunas:

- `REF_DATE`: datas no formato datetime.
- `TARGET`: valores binários, apenas 0 e 1.
- `SEXO`: strings "M" e "F".
- `IDADE`: valores como 34.137 (idade em anos, possivelmente com decimais).
- `OBITO`: muitos valores como "none" (pode conter valores ausentes ou nulos).
- `Unidade Federativa`: siglas dos estados do Brasil, como "PE", "RO", etc.
- `CLASSE SOCIAL`: categorias como "D", "E", "B".

Com base na seguinte pergunta, gere **somente o código Python** que:

- Use exclusivamente o DataFrame `df` como fonte de dados.
- Armazene o resultado em uma variável chamada `resultado`, se a pergunta envolver uma resposta tabular ou estatística.
- Se a pergunta exigir visualização, utilize `matplotlib.pyplot` e chame `plt.show()` ao final do gráfico.
- Não utilize `print()` nem leia ou salve arquivos.
- Retorne apenas o código limpo e funcional, com no máximo 2 comentários explicativos usando '#'.

Agora, responda com **somente o código** para a seguinte pergunta:

Pergunta: {pergunta}
"""

    try:
        with st.spinner("Consultando IA e executando código..."):
            response = model.generate_content(prompt)

        codigo = re.sub(r"```(?:python)?", "", response.text).strip()
        codigo = codigo.replace("```", "").strip()

        st.code(codigo, language='python')
        logging.info(f"Código gerado:\n{codigo}")

        exec_locals = executar_codigo(codigo, df, plt)

        # Mostrar resultado se existir
        resultado = exec_locals.get("resultado")
        if resultado is not None:
            st.write("📊 Resultado:")
            st.write(resultado)

        # Exibir todos os gráficos gerados
        figs = plt.get_fignums()
        if figs:
            for fig_num in figs:
                fig = plt.figure(fig_num)
                st.pyplot(fig)
                plt.close(fig)

    except GoogleAPIError as api_err:
        st.error(f"Erro na API Gemini: {api_err}")

    except Exception as e:
        st.error("❌ Erro ao processar a pergunta.")
        trace_text = traceback.format_exc()
        st.code(trace_text, language="python")

        # ✅ NOVO BLOCO: gerar explicação com IA sobre o erro
        try:
            explicacao_prompt = f"""
Sou um analista de dados e encontrei o seguinte erro ao executar um código em Python com pandas e matplotlib:

{trace_text}

Com base nesse erro, explique de forma simples e objetiva qual foi a provável causa e como corrigir.
Considere que o DataFrame `df` possui as seguintes colunas:
{list(df.columns)}

Explique como se estivesse ajudando um usuário iniciante a entender o problema.
"""
            with st.spinner("Analisando erro com IA..."):
                explicacao_erro = model.generate_content(explicacao_prompt).text
                st.markdown("### 🤖 Explicação do erro:")
                st.markdown(explicacao_erro)

        except Exception as explicacao_falhou:
            st.warning("⚠️ Não foi possível gerar explicação para o erro.")
