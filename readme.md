# CloneME: Crie Seu Próprio Chatbot de Persona AI

CloneME é uma aplicação FastAPI que permite criar um chatbot que emula uma persona específica, utilizando conteúdo de texto fornecido por você (como posts de blog, livros ou outros escritos) para dar à IA sua voz, conhecimento e personalidade.

## Funcionalidades

- **Emulação Profunda de Persona**: A IA incorpora totalmente a persona com base nos textos fornecidos.
- **Múltiplas Fontes de Texto**: Combine vários arquivos de texto (posts de blog, capítulos de livros) para construir uma personalidade rica.
- **Integração com OpenRouter**: Alterne facilmente entre diferentes LLMs disponíveis no OpenRouter.
- **Interface Web Simples**: Inclui um frontend HTML/JavaScript básico para o chat.
- **Configurável**: Personalize o nome da persona, arquivos de texto e modelo LLM através do script Python.
- **Limpeza de Conteúdo**: Funções básicas para remoção de marcadores de paginação e novas linhas excessivas.

## Como Funciona

1. **Carregamento de Conteúdo**: A aplicação carrega texto de arquivos especificados (.txt).
2. **Engenharia de Prompt**: Um prompt de sistema detalhado é construído, instruindo o LLM a adotar a persona baseando-se nos textos fornecidos.
3. **Interação do Usuário**: Usuários enviam mensagens através da interface web.
4. **Chamada de API**: A mensagem do usuário e o prompt da persona são enviados para a API do OpenRouter.
5. **Geração de Resposta**: O LLM gera uma resposta na voz da persona.
6. **Exibição**: A resposta é mostrada ao usuário na interface web.

## Configuração

Abra o arquivo `app.py` e modifique a seção **"CONFIGURAÇÕES DA PERSONA E CONTEÚDO"**:

```python
# CONFIGURAÇÕES DA PERSONA E CONTEÚDO
PERSONA_NAME = "NomeDaSuaPersona"  # Ex: "MinhaPersonaLegal", "FilosofoBot"
WORDPRESS_POSTS_FILE = "posts.txt"  # Arquivo com posts/blog
LIVRO_BIO_FILE = "biografia.txt"    # Arquivo com biografia
LIVRO_GUERRA_FILE = "guerra.txt"    # Outro arquivo de conteúdo
MODEL = "openai/gpt-4.1-mini"       # Modelo LLM do OpenRouter
```

### Opções de Modelos LLM (OpenRouter)
- `openai/gpt-4.1-mini`
- `anthropic/claude-3-haiku-20240307`
- `google/gemini-flash`

## Preparando os Arquivos de Conteúdo

1. Reúna os textos para sua persona (exports de blog, manuscritos, coleções de cartas).
2. Salve-os como arquivos de texto simples (.txt) com codificação UTF-8.
3. Coloque-os no diretório raiz do projeto ou atualize os caminhos em `app.py`.
4. (Opcional) Adapte a função `load_and_clean_content` em `app.py` para necessidades específicas de limpeza.

**Dica**: Quanto mais texto representativo e de alta qualidade você fornecer, melhor será a emulação da persona. Textos muito curtos podem levar a respostas genéricas.

## Executando o Projeto

1. Instale as dependências:
```bash
pip install fastapi uvicorn
```

2. Execute o servidor:
```bash
uvicorn app:app --reload
```

3. Acesse a interface web em `http://localhost:8000`
