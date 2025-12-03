# src/dexia_engine.py
import json
from typing import Any, Dict, Tuple

from .models import UserInput
from .prompt_builder import build_dexia_prompt
from .ai_client import call_dexia_model


def gerar_time_com_professora_dexia(user_input: UserInput) -> Tuple[Dict[str, Any], str]:
    """
    Função principal do MVP.
    Recebe o input do usuário, conversa com a IA e retorna:
      - um dicionário com os dados do time (sempre com as chaves "time" e "plano_de_jogo")
      - o texto bruto da IA (raw_response), para debug/log
    """

    # 1) Monta o prompt e chama o modelo
    prompt = build_dexia_prompt(user_input)
    raw_response = call_dexia_model(prompt)  # string retornada pela IA

    # 2) Tenta interpretar como JSON
    data: Dict[str, Any] | None = None

    # Tentativa direta
    try:
        data = json.loads(raw_response)
    except json.JSONDecodeError:
        # Tentativa com limpeza básica
        cleaned = raw_response.strip()

        # Se vier dentro de ```json ... ``` ou ``` ... ```
        if cleaned.startswith("```"):
            cleaned = cleaned.strip("`")
            # Ex.: "json\n{...}"
            if cleaned.lower().startswith("json"):
                cleaned = cleaned[4:].lstrip()

        try:
            data = json.loads(cleaned)
        except json.JSONDecodeError:
            data = None

    # Se ainda não deu certo, garante um dicionário mínimo
    if data is None or not isinstance(data, dict):
        print("Falha ao interpretar a resposta da Dexia como JSON.")
        print("Resposta bruta recebida:\n", raw_response)
        data = {"time": [], "plano_de_jogo": ""}

    # Garante que as chaves existam
    if "time" not in data or not isinstance(data["time"], list):
        data["time"] = []
    if "plano_de_jogo" not in data or not isinstance(data["plano_de_jogo"], str):
        data["plano_de_jogo"] = ""

    # 3) Filtro anti-duplicado de Pokémon
    time = data.get("time", [])
    nomes_vistos = set()
    time_unico = []

    for mon in time:
        if not isinstance(mon, dict):
            continue

        nome = (mon.get("nome") or "").strip().lower()
        if not nome:
            # se por algum motivo não tiver nome, deixa passar
            time_unico.append(mon)
            continue

        if nome in nomes_vistos:
            # já temos esse pokémon, então pulamos (não colocamos de novo)
            continue

        nomes_vistos.add(nome)
        time_unico.append(mon)

    data["time"] = time_unico
    # fim do filtro anti-duplicado

    return data, raw_response


