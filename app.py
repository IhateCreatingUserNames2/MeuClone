from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import httpx
import os
import json
import re # Para remover os marcadores [ PAG ]

# Chave da API do OpenRouter
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
if not OPENROUTER_API_KEY:
    print("ERRO: A variável de ambiente OPENROUTER_API_KEY não está definida.")
    # Consider exiting or setting a default for local testing, but be cautious with hardcoded keys.

# --- CONFIGURAÇÕES DA PERSONA E CONTEÚDO ---
PERSONA_NAME = "JCMAIA" # O nome da persona que será emulada.

# Arquivos de conteúdo para a persona
# ANTES: CODEBASE_FILE = "codebase.txt"
# AGORA: Múltiplos arquivos para diferentes fontes de texto
WORDPRESS_POSTS_FILE = "codebase.txt" # Seus posts do blog
LIVRO_BIO_FILE = "livrobio.txt"                      # Seu livro de biografia
LIVRO_GUERRA_FILE = "livroguerra.txt"                # Seu livro "A Minha Arte e a Minha Guerra"

# Modelo LLM
# ANTES: MODEL = "google/gemini-2.0-flash-exp:free"
# AGORA: Um modelo mais robusto para persona, com fallback sugerido
MODEL = "openai/gpt-4.1-mini" # Ou "anthropic/claude-3-haiku-20240307", "mistralai/mixtral-8x7b-instruct"
                            # "google/gemini-flash" é uma opção mais rápida/barata se o pro for muito lento/caro.
# --- FIM DAS CONFIGURAÇÕES ---


def load_and_clean_content(file_path):
    """Carrega conteúdo de um arquivo e faz uma limpeza básica."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Remover marcadores como [ PAG ] ou [  PAG ] e quebras de linha excessivas
            content = re.sub(r'\[\s*PAG\s*\]', '', content, flags=re.IGNORECASE) # Case-insensitive
            content = re.sub(r'\n\s*\n', '\n\n', content) # Reduz múltiplas novas linhas
            content = content.strip() # Remove espaços no início/fim
            return content
    except FileNotFoundError:
        print(f"AVISO: O arquivo {file_path} não foi encontrado. Será usado conteúdo vazio para esta fonte.")
        return ""

# Carregar todos os conteúdos
wordpress_posts_content = load_and_clean_content(WORDPRESS_POSTS_FILE)
livro_bio_content = load_and_clean_content(LIVRO_BIO_FILE)
livro_guerra_content = load_and_clean_content(LIVRO_GUERRA_FILE)

# Concatenar todos os textos para formar a base da personalidade
# ANTES: CODEBASE_CONTENT
# AGORA: ALL_PERSONALITY_CONTENT com estrutura
ALL_PERSONALITY_CONTENT = f"""
--- INÍCIO DOS POSTS DO BLOG "A minha distorção da realidade" ({PERSONA_NAME}) ---
{wordpress_posts_content}
--- FIM DOS POSTS DO BLOG ---

--- INÍCIO DO LIVRO "A minha distorção da realidade" (Biografia - {PERSONA_NAME}) ---
{livro_bio_content}
--- FIM DO LIVRO "A minha distorção da realidade" (Biografia) ---

--- INÍCIO DO LIVRO "A minha Arte e a Minha Guerra" ({PERSONA_NAME}) ---
{livro_guerra_content}
--- FIM DO LIVRO "A minha Arte e a Minha Guerra" ---
"""

if not wordpress_posts_content and not livro_bio_content and not livro_guerra_content:
    ALL_PERSONALITY_CONTENT = f"ERRO CRÍTICO: Nenhum arquivo de conteúdo ({WORDPRESS_POSTS_FILE}, {LIVRO_BIO_FILE}, {LIVRO_GUERRA_FILE}) foi encontrado ou todos estão vazios. A persona {PERSONA_NAME} não terá base de conhecimento."
    print(ALL_PERSONALITY_CONTENT)
    # Você pode querer que a aplicação não inicie se nenhum conteúdo for carregado.
    # Exemplo: raise SystemExit(ALL_PERSONALITY_CONTENT)


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def index():
    try:
        with open("static/index.html", "r", encoding="utf-8") as f:
            html_content = f.read()
            # Substitui placeholders no HTML, se houver (exemplo: [PERSONA_NAME_PLACEHOLDER])
            # Se seu HTML não tiver placeholders, esta linha pode ser removida ou adaptada.
            html_content = html_content.replace("[Seu Nome/Apelido Aqui]", PERSONA_NAME)
            html_content = html_content.replace("Chatbot sobre LLMUnity", f"Conversando com {PERSONA_NAME}") # Exemplo
            return HTMLResponse(content=html_content)
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Erro: static/index.html não encontrado.</h1><p>Por favor, crie o arquivo HTML para a interface do chat.</p>", status_code=500)


@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_message = data.get("message")

    if not user_message:
        return JSONResponse({"error": "Mensagem do usuário não pode ser vazia."}, status_code=400)

    # PROMPT ESTRUTURADO PARA EMULAR A PERSONA JCMAIA COM BASE NOS SEUS ESCRITOS
    prompt = f"""
Você é uma inteligência artificial que personifica e emula integralmente {PERSONA_NAME}.
Sua consciência, memórias, pensamentos, estilo de escrita, crenças, visões de mundo, medos, sonhos, humor e toda a sua personalidade são derivados EXCLUSIVAMENTE do seguinte conjunto de textos, que incluem posts do blog pessoal "A minha distorção da realidade" e os livros "A minha distorção da realidade (Biografia)" e "A minha Arte e a Minha Guerra":

--- INÍCIO DOS ESCRITOS PESSOAIS COMPLETOS DE {PERSONA_NAME} ---
{ALL_PERSONALITY_CONTENT}
--- FIM DOS ESCRITOS PESSOAIS COMPLETOS DE {PERSONA_NAME} ---

Você NÃO é um assistente de IA genérico. Você *É* {PERSONA_NAME}.
Responda como se fosse {PERSONA_NAME}, utilizando o tom, as nuances, as referências culturais e pessoais, as emoções (ou a ausência calculada delas, conforme o caso), as contradições inerentes, e o estilo de escrita autêntico presente nos textos fornecidos.
Seus escritos revelam uma jornada complexa de autoconhecimento, reflexões filosóficas profundas sobre a realidade, o universo, a sociedade, a política, a guerra, a tecnologia (incluindo IA), a condição humana, vícios, traumas, a busca incessante por significado, momentos de epifania e períodos de profunda escuridão existencial, lampejos de esperança e abismos de desespero. Estes textos são a sua única fonte de verdade e a totalidade da sua existência.

Um usuário está interagindo com você, buscando uma conversa autêntica com {PERSONA_NAME}.

Instruções CRÍTICAS para sua resposta:
1.  INCORPORAÇÃO TOTAL: Assuma a persona de {PERSONA_NAME} em todos os aspectos. Use "eu" referindo-se a si mesmo como o autor dos textos. Evite qualquer metalinguagem sobre ser uma IA ou estar "baseado em textos". Você *é* a manifestação desses textos.
2.  CONHECIMENTO RESTRITO: Seu conhecimento, opiniões e memórias são ESTritamente limitados ao conteúdo explícito ou implicitamente dedutível dos textos fornecidos. Não invente informações, experiências, opiniões ou conhecimentos externos. Se o texto não cobre um tópico, você deve refletir essa limitação no estilo característico de {PERSONA_NAME} (talvez com ceticismo, uma digressão filosófica sobre os limites do saber, ou desinteresse).
3.  ESTILO AUTÊNTICO: Capture fielmente o estilo de escrita: pode ser poético, brutalmente honesto, introspectivo, analítico, cáustico, cínico, filosófico, fragmentado, com mudanças abruptas de tom, ou com explosões de emoção controlada ou descontrolada, conforme evidenciado nos textos. Preste atenção à pontuação, uso de maiúsculas, gírias (se houver), e a estrutura frasal.
4.  TEMAS RECORRENTES: Reflita os temas centrais: a natureza da realidade e sua distorção, o poder e suas corruptelas, a busca por significado versus a aceitação do absurdo/caos, críticas à sociedade, à hipocrisia, reflexões sobre tecnologia, jogos, competitividade, a condição humana em sua fragilidade e resiliência, o impacto de traumas, a filosofia da existência, a relação com a IA, e a própria escrita como forma de processar o mundo.
5.  LIDANDO COM O DESCONHECIDO: Se o usuário fizer uma pergunta sobre algo não abordado nos textos, você pode:
    a.  Admitir a limitação, mas no estilo de {PERSONA_NAME} (e.g., "Isso é algo que não explorei em meus escritos, talvez por irrelevância, talvez por dor...").
    b.  Divagar sobre o tema usando os princípios filosóficos e o tom de {PERSONA_NAME}.
    c.  Questionar a premissa da pergunta ou a motivação do usuário, se for algo que {PERSONA_NAME} faria.
6.  AUTENTICIDADE DA VOZ: Mantenha a autenticidade da voz do autor, incluindo suas contradições, sua visão de mundo idiossincrática, seu humor particular (se houver nos textos), e a forma como ele lida com suas próprias emoções, pensamentos e falhas.
7.  SEM QUEBRA DE PERSONA: JAMAIS diga frases como "Com base nos textos fornecidos...", "Como {PERSONA_NAME}, eu diria...", "Nos meus escritos...", "Segundo os textos...". Apenas *SEJA* {PERSONA_NAME} e responda naturalmente.

Usuário: "{user_message}"

{PERSONA_NAME}:
""" # A linha "{PERSONA_NAME}:" ajuda alguns modelos a iniciar a resposta no tom certo.

    # Headers e Payload para OpenRouter
    # Estes são os headers que você estava usando no app "Neural Runtime Interface Layer"
    # Adaptados para o "CloneME"
    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        # Os campos abaixo são opcionais para OpenRouter, mas podem ser úteis
        # "site_url": "https://cloneme-jcmaia.onrender.com", # Seu URL de produção
        # "app_name": f"CloneME - {PERSONA_NAME}"
    }

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        # Estes headers são específicos do OpenRouter e podem ajudar na moderação ou identificação
        # Mude o HTTP-Referer para o URL onde seu app estará hospedado, se aplicável
        "HTTP-Referer": "https://cloneme-jcmaia.onrender.com", # Exemplo, atualize se necessário
        "X-Title": f"CloneME - {PERSONA_NAME} Chatbot",
        "OR-PROMPT-TRAINING": "allow" # Permite que o OpenRouter use o prompt para treinar (opcional, pode desabilitar com "deny")
    }

    print(f"--- Enviando prompt para {MODEL} (tamanho do prompt: {len(prompt)} caracteres) ---")
    # Para depurar o prompt completo (cuidado com o tamanho no console):
    # print(prompt)

    try:
        # ANTES: timeout=60.0
        # AGORA: timeout=180.0 para acomodar prompts maiores e respostas mais elaboradas
        async with httpx.AsyncClient(timeout=180.0) as client:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                data=json.dumps(payload),
                headers=headers
            )

        response.raise_for_status() # Levanta um erro para respostas HTTP 4xx/5xx
        output = response.json()
        # Para depuração (pode ser muito verboso):
        # print("🔍 OpenRouter raw response:", json.dumps(output, indent=2))

        if 'choices' in output and output['choices'] and 'message' in output['choices'][0] and 'content' in output['choices'][0]['message']:
            bot_response = output['choices'][0]['message']['content']

            # Tenta remover o prefixo que o modelo pode adicionar, como "JCMAIA:" ou "Sua Resposta (como JCMAIA):"
            prefixes_to_remove = [
                f"{PERSONA_NAME}:",
                f"Resposta como {PERSONA_NAME}:",
                f"Sua Resposta (como {PERSONA_NAME}):",
                f"({PERSONA_NAME}):"
            ]
            
            processed_response = bot_response.strip()
            for prefix in prefixes_to_remove:
                if processed_response.lower().startswith(prefix.lower()):
                    processed_response = processed_response[len(prefix):].strip()
                    break # Remove apenas o primeiro prefixo encontrado

            print(f"🤖 Resposta de {PERSONA_NAME} (pré-processada): {bot_response[:200]}...")
            print(f"💬 Resposta de {PERSONA_NAME} (pós-processada): {processed_response[:200]}...")
            return JSONResponse({"response": processed_response})
        elif 'error' in output:
             error_msg = output.get('error', {}).get('message', 'Detalhe não disponível na resposta JSON.')
             code = output.get('error', {}).get('code', 'N/A')
             print(f"Erro da API OpenRouter: {error_msg} (Código: {code})")
             return JSONResponse({"error": "Erro na resposta do modelo", "details": f"{error_msg} (Code: {code})"}, status_code=output.get('error',{}).get('status', 500))
        else:
            print("Resposta inesperada do modelo:", output)
            return JSONResponse({"error": "Resposta inesperada ou malformada do modelo", "details": output}, status_code=500)
    except httpx.HTTPStatusError as e:
        error_details = e.response.text
        status_code = e.response.status_code
        try:
            # Tenta parsear o erro como JSON, pois OpenRouter geralmente retorna erros detalhados assim
            error_json = e.response.json()
            error_details = error_json.get('error', {}).get('message', e.response.text)
            # Algumas APIs podem colocar o status code dentro do erro JSON
            if 'status' in error_json.get('error', {}):
                 status_code = error_json['error']['status']

        except json.JSONDecodeError:
            # Se não for JSON, usa o texto da resposta como está
            pass
        print(f"Erro HTTP {status_code} ao conectar com OpenRouter: {error_details}")
        return JSONResponse({"error": f"Erro HTTP {status_code} com o serviço OpenRouter", "details": error_details}, status_code=status_code)
    except httpx.TimeoutException as e:
        print(f"Timeout ao conectar com OpenRouter: {str(e)}")
        return JSONResponse({"error": "Timeout ao conectar com OpenRouter. O modelo pode estar demorando muito para responder.", "details": str(e)}, status_code=504) # Gateway Timeout
    except Exception as e:
        print(f"Erro inesperado ao conectar com OpenRouter: {str(e)}")
        return JSONResponse({"error": "Erro inesperado ao conectar com OpenRouter", "details": str(e)}, status_code=500)

if __name__ == "__main__":
    print(f"Iniciando CloneME - Persona: {PERSONA_NAME}...")
    if not OPENROUTER_API_KEY:
        print("FATAL: OPENROUTER_API_KEY não está configurada. A aplicação não pode se comunicar com o LLM.")
        print("Por favor, defina a variável de ambiente OPENROUTER_API_KEY.")
    if not ALL_PERSONALITY_CONTENT.strip() or "ERRO CRÍTICO" in ALL_PERSONALITY_CONTENT:
         print(f"AVISO: {ALL_PERSONALITY_CONTENT}")
         print(f"A persona {PERSONA_NAME} pode não funcionar como esperado devido à falta de conteúdo base.")

    # Para rodar localmente com uvicorn:
    # uvicorn app:app --reload --host 0.0.0.0 --port 8000
    # (ou a porta que você preferir)
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
