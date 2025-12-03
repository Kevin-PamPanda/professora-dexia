⚡ Professora Dexia – Pesquisadora de Batalhas Pokémon
Monte e ajuste times competitivos com ajuda de IA

📌 Sobre o projeto

Professora Dexia é uma IA especializada em ajudar treinadores a montar, ajustar e entender times de Pokémon competitivo (VGC, Singles, OU, etc.).
Ela analisa estilo de jogo, formato, regulamento e preferências do jogador — e monta um time completo com:

Pokémon

Itens

Habilidades

Nature

EVs / IVs

Movesets

Papel no time

Plano de jogo completo

Sugestões baseadas em meta e matchmaking

O projeto nasceu em 2025, criado por Kevin de Freitas Minervino, com objetivo educativo e recreativo.

Dexia também permite conversas contínuas:
➡️ Você pode pedir ajustes (“troque X”, “quero um time mais bulky”, “mude o lead”)
➡️ Ela gera uma nova versão do time, mantendo coerência e lógica competitiva.

🧪 Tecnologias usadas

Este projeto utiliza:

Python 3.11

Streamlit (interface web)

OpenAI API (IA do backend)

PokéAPI (imagens oficiais dos Pokémon)

dotenv (segurança das variáveis locais)

Requests (acesso às APIs externas)

🚀 Funcionalidades
✔ Gerador de time completo

Dexia constrói automaticamente um time competitivo baseado nas suas preferências.

✔ Ajustes inteligentes

Não gostou de algum Pokémon?
Dexia ajusta, troca, refaz EVs, muda itens e reequilibra a estratégia.

✔ Análise detalhada

Inclui explicações para jogadores:

Iniciantes

Intermediários

Profissionais

✔ Respeito aos regulamentos

Dexia considera regras de:

VGC (Pokémon Company International)

Reg H / Reg J

Singles OU / UU / Ubers

Formatos customizados

✔ Interface web completa

App acessível diretamente no navegador, sem instalar nada.

🖥 Demonstração online

🔗 (Adicione aqui o link do Streamlit Cloud após publicar)
Exemplo:

https://professora-dexia-kevin.streamlit.app

📂 Estrutura do Projeto
professora-dexia/
│
├── data/
│   └── example_pokemon.json        # (Opcional) Exemplo de dataset local
│
├── src/
│   ├── __pycache__/                # Cache do Python
│   ├── __init__.py                 # Torna 'src' um pacote importável
│   │
│   ├── ai_client.py                # Conexão com OpenAI (modelo da Dexia)
│   ├── cli_app.py                  # Interface CLI (modo terminal)
│   ├── dexia_engine.py             # Motor principal: monta e ajusta times
│   ├── pokemon_db.py               # (Opcional) Funções auxiliares de dados
│   ├── prompt_builder.py           # Construção dos prompts avançados
│
├── web/
│   └── app.py                      # Interface web construída em Streamlit
│
├── requirements.txt                # Dependências do projeto
├── README.md                       # Documentação


⚙ Como executar localmente
1️⃣ Clone o repositório
git clone https://github.com/SEU-USUARIO/professora-dexia.git
cd professora-dexia

2️⃣ Crie um ambiente virtual (opcional mas recomendado)
python -m venv venv
.\venv\Scripts\activate

3️⃣ Instale as dependências
pip install -r requirements.txt

4️⃣ Configure sua OpenAI API Key

Crie o arquivo .env:

OPENAI_API_KEY=sk-xxxx

5️⃣ Rode a interface
streamlit run web/app.py

💡 Roadmap futuro

Adicionar exportação do time em PDF

Criar análise de fraquezas e gráficos de matchup

Suporte para múltiplos treinadores (login)

Histórico de times

Editor manual com sugestões automáticas

Deploy com domínio próprio (professoradexia.com)

Versão mobile otimizada

⚠ Aviso Legal

Professora Dexia é um projeto de fã, criado para fins educativos e de estudo.

Pokémon © Nintendo / GAME FREAK / Creatures Inc.
Este projeto não é afiliado, endossado ou patrocinado pelas empresas proprietárias.

As sugestões da IA são recreativas e não garantem performance competitiva.

👤 Autor

Kevin de Freitas Minervino (2025)
Desenvolvedor, criador do conceito e implementação do sistema.





