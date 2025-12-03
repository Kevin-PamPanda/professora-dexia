# web/app.py
import streamlit as st
import requests
import sys
from pathlib import Path

# ==== Ajuste de caminho para importar o pacote src ====
ROOT = Path(__file__).resolve().parents[1]  # pasta "professora-dexia"
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from src.dexia_engine import gerar_time_com_professora_dexia  # type: ignore

# ==== Mini "modelo" compatível com o dexia_engine ====
class Preferencias:
    def __init__(self, formato: str, estilo_jogo: str, nivel_jogador: str, regulamentacao: str):
        self.formato = formato
        self.estilo_jogo = estilo_jogo
        self.nivel_jogador = nivel_jogador
        self.regulamentacao = regulamentacao


class WebUserInput:
    def __init__(
        self,
        formato: str,
        estilo_jogo: str,
        nivel_jogador: str,
        regulamentacao: str,
        pokemons_existentes: list[str],
        mensagem_livre: str,
    ):
        self.preferencias = Preferencias(formato, estilo_jogo, nivel_jogador, regulamentacao)
        self.pokemons_existentes = pokemons_existentes
        self.mensagem_livre = mensagem_livre


# ==== Cache de imagens da PokéAPI ====
@st.cache_data(show_spinner=False)
def get_pokemon_image_url(name: str) -> str | None:
    """
    Busca a imagem do Pokémon na PokéAPI.
    Tenta usar o 'official-artwork'; se não tiver, cai no sprite padrão.
    Retorna a URL ou None.
    """
    if not name:
        return None

    slug = (
        name.strip()
        .lower()
        .replace(" ", "-")
        .replace(".", "")
        .replace("'", "")
        .replace("é", "e")
    )

    url = f"https://pokeapi.co/api/v2/pokemon/{slug}"
    try:
        resp = requests.get(url, timeout=5)
    except Exception:
        return None

    if resp.status_code != 200:
        return None

    try:
        data = resp.json()
        img = (
            data.get("sprites", {})
            .get("other", {})
            .get("official-artwork", {})
            .get("front_default")
        )
        if not img:
            img = data.get("sprites", {}).get("front_default")
        return img
    except Exception:
        return None


# ==== Estado de sessão ====
if "last_data" not in st.session_state:
    st.session_state["last_data"] = None
if "last_input" not in st.session_state:
    st.session_state["last_input"] = None
if "last_raw" not in st.session_state:
    st.session_state["last_raw"] = ""


# ==== Config da página ====
st.set_page_config(
    page_title="Professora Dexia",
    page_icon="⚡",
    layout="wide",
)

st.title("⚡ Professora Dexia – Pesquisadora de Batalhas Pokémon")
st.write("Monte e ajuste seu time competitivo com ajuda de IA. Projeto de fã, para estudo e diversão.")

col_form, col_result = st.columns([1, 2])

# ================================
# COLUNA ESQUERDA – FORMULÁRIO
# ================================
with col_form:
    st.header("Configuração do time")

    formato = st.selectbox("Formato", ["singles", "doubles"], index=1)
    estilo = st.selectbox("Estilo de jogo", ["agressivo", "balanceado", "defensivo"], index=0)
    nivel = st.selectbox("Seu nível como jogador", ["iniciante", "intermediario", "pro"], index=2)
    regulamento = st.text_input("Regulamentação (Reg H, Reg J, VGC, OU, UU, etc.)", "VGC")

    pokemons_str = st.text_input("Pokémon obrigatórios (0–6, separados por vírgula)", "pikachu")
    pokemons_list = [p.strip() for p in pokemons_str.split(",") if p.strip()]

    mensagem_extra = st.text_area(
        "Mensagem para a Professora Dexia (ex: dificuldade, estilo, clima etc.)",
        "Quero um time de chuva agressivo.",
    )

    if st.button("✨ Gerar time com IA"):
        user_input = WebUserInput(
            formato=formato,
            estilo_jogo=estilo,
            nivel_jogador=nivel,
            regulamentacao=regulamento,
            pokemons_existentes=pokemons_list,
            mensagem_livre=mensagem_extra,
        )

        st.info("Consultando o laboratório da Professora Dexia...")
        data, raw = gerar_time_com_professora_dexia(user_input)

        st.session_state["last_data"] = data
        st.session_state["last_input"] = user_input
        st.session_state["last_raw"] = raw

# ================================
# COLUNA DIREITA – RESULTADOS
# ================================
with col_result:
    data = st.session_state["last_data"]
    raw = st.session_state["last_raw"]

    if data:
        time = data.get("time", [])
        plano = data.get("plano_de_jogo", "")

        st.markdown("### 🧩 Time sugerido")
        if not time:
            st.info("A IA respondeu, mas não veio nenhum Pokémon no campo `time`.")
        else:
            for i, mon in enumerate(time, start=1):
                nome = mon.get("nome", "???")
                st.markdown(f"#### [{i}] {nome}")

                img_url = get_pokemon_image_url(nome)
                if img_url:
                    st.image(img_url, width=96)

                st.write(f"**Item:** {mon.get('item', '')}")
                st.write(f"**Habilidade:** {mon.get('habilidade', '')}")
                st.write(f"**Nature:** {mon.get('nature', '')}")
                st.write(f"**EVs:** {mon.get('evs', '')}")
                st.write(f"**IVs:** {mon.get('ivs', '')}")
                st.write("**Moveset:**")
                for mv in mon.get("moveset", []):
                    st.write(f"- {mv}")
                st.write(f"**Papel no time:** {mon.get('papel', '')}")
                st.markdown("---")

        st.markdown("### 🎯 Plano de jogo")
        st.write(plano or "Sem plano de jogo retornado.")

        # ==== BLOCO DE AJUSTE DO TIME ====
        st.markdown("### 🔄 Ajustar este time com a Professora Dexia")
        ajuste_texto = st.text_area(
            "Explique o que você quer mudar (ex: 'não gostei de Roserade, troque por algo mais bulky')",
            key="ajuste_texto",
        )

        if st.button("📨 Enviar ajuste para este time"):
            if not data or not st.session_state["last_input"]:
                st.warning("Gere um time primeiro antes de pedir ajustes.")
            else:
                time_atual = data.get("time", [])
                linhas = []
                for mon in time_atual:
                    linhas.append(
                        f"- {mon.get('nome','???')} @ {mon.get('item','')} — {mon.get('papel','')}"
                    )
                resumo_time = "\n".join(linhas)

                mensagem_completa = (
                    "Quero que você AJUSTE o time abaixo, mantendo a ideia geral, "
                    "mas aplicando o meu pedido.\n\n"
                    "TIME ATUAL:\n"
                    f"{resumo_time}\n\n"
                    "PEDIDO DO TREINADOR:\n"
                    f"{ajuste_texto}\n\n"
                    "IMPORTANTE:\n"
                    "- Você pode trocar Pokémon, itens, EVs e moveset, desde que o time continue "
                    "coerente com o estilo, formato e regulamento.\n"
                    "- Explique no campo 'plano_de_jogo' quais mudanças foram feitas e por quê."
                )

                last_input = st.session_state["last_input"]
                user_input_ajuste = WebUserInput(
                    formato=last_input.preferencias.formato,
                    estilo_jogo=last_input.preferencias.estilo_jogo,
                    nivel_jogador=last_input.preferencias.nivel_jogador,
                    regulamentacao=last_input.preferencias.regulamentacao,
                    pokemons_existentes=[],  # deixa livre pra IA mexer no time todo
                    mensagem_livre=mensagem_completa,
                )

                st.info("Enviando ajuste para o laboratório da Professora Dexia...")
                data2, raw2 = gerar_time_com_professora_dexia(user_input_ajuste)

                st.session_state["last_data"] = data2
                st.session_state["last_input"] = user_input_ajuste
                st.session_state["last_raw"] = raw2

                st.success("Ajuste recebido! Abaixo está a nova sugestão de time.")
                st.rerun()

        # ==== Debug opcional ====
        with st.expander("🔍 Resposta bruta da IA (debug)"):
            st.code(raw or "", language="json")

    else:
        st.info("Nenhum time gerado ainda. Preencha o formulário à esquerda e clique em **Gerar time com IA**.")

# ==========================
# RODAPÉ – Aviso legal e autoria
# ==========================
st.markdown("---")
st.markdown(
    """
### Sobre o projeto

**Professora Dexia** é um projeto de fã criado por **Kevin de Freitas Minervino** em 2025, com o objetivo de ajudar treinadores a entender e montar times de Pokémon competitivo usando inteligência artificial.

Este site é não-oficial e **não é afiliado, endossado ou patrocinado** por Nintendo, GAME FREAK, Creatures Inc. ou The Pokémon Company.  
Pokémon e todos os nomes relacionados são marcas registradas de seus respectivos donos.

As sugestões da Professora Dexia têm caráter recreativo e educacional, **sem garantia de resultado** em torneios oficiais.

© 2025 – Conceito original e implementação por **Kevin de Freitas Minervino**.
"""
)