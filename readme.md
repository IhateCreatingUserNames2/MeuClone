CloneME: Crie Seu Próprio Chatbot de Persona AI



CloneME é uma aplicação FastAPI que permite criar um chatbot que emula uma persona específica. Ele usa conteúdo de texto fornecido por você (como posts de blog, livros ou quaisquer escritos) para dar à IA sua voz, conhecimento e personalidade. O backend se comunica com LLMs (Modelos de Linguagem Grandes) através da API do OpenRouter.
Este projeto fornece um modelo para você configurar e executar facilmente um chatbot que "se torna" a persona definida pelos seus textos.



Funcionalidades


Emulação Profunda de Persona: A IA é instruída a incorporar totalmente a persona com base nos textos fornecidos.
Múltiplas Fontes de Texto: Combine vários arquivos de texto (por exemplo, posts de blog, capítulos de livros) para construir uma personalidade rica.
Integração com OpenRouter: Alterne facilmente entre diferentes LLMs disponíveis no OpenRouter.
Interface Web Simples: Vem com um frontend HTML/JavaScript básico para o chat.
Configurável: Altere facilmente o nome da persona, arquivos de texto e modelo LLM através do script Python.
Limpeza de Conteúdo: Limpeza básica de arquivos de texto (por exemplo, remoção de marcadores de paginação).



Como Funciona



Carregamento de Conteúdo: A aplicação carrega texto de arquivos especificados (.txt).
Engenharia de Prompt: Um prompt de sistema detalhado é construído, instruindo o LLM a adotar a persona baseando-se exclusivamente nos textos fornecidos. Este prompt inclui os escritos da persona.
Interação do Usuário: Usuários enviam mensagens através de uma interface web.
Chamada de API: A mensagem do usuário, juntamente com o prompt que define a persona, é enviada para a API do OpenRouter.
Geração de Resposta: O LLM gera uma resposta na voz da persona.
Exibição: A resposta é exibida de volta para o usuário na interface web.




Configuração

Abra o arquivo app.py e modifique a seção "CONFIGURAÇÕES DA PERSONA E CONTEÚDO":
PERSONA_NAME: O nome da persona que sua IA irá emular (ex: "MinhaPersonaLegal", "FilosofoBot").
WORDPRESS_POSTS_FILE, LIVRO_BIO_FILE, LIVRO_GUERRA_FILE: Altere esses nomes de arquivo para corresponder aos seus arquivos de origem de texto. Você pode adicionar mais ou remover alguns. Certifique-se de que esses arquivos estejam no mesmo diretório que app.py ou forneça o caminho correto.
MODEL: Escolha um modelo LLM do OpenRouter (ex: "openai/gpt-4.1-mini", "anthropic/claude-3-haiku-20240307", "google/gemini-flash"). Considere os pontos fortes do modelo, tamanho da janela de contexto e custo.


Criando os Arquivos de Conteúdo da Sua Persona


Reúna os textos para sua persona (ex: exports de blog, manuscritos de livros, coleções de cartas).
Salve-os como arquivos de texto simples (.txt) com codificação UTF-8.
Coloque-os no diretório raiz do projeto (ou atualize os caminhos dos arquivos em app.py).
O script inclui uma função básica load_and_clean_content para remover marcadores [ PAG ] e novas linhas excessivas. Você pode precisar adaptá-la para outras necessidades específicas de limpeza.
Qualidade e Quantidade: Quanto mais texto representativo e de alta qualidade você fornecer, melhor será a emulação da persona. Textos muito curtos podem levar a respostas genéricas.
