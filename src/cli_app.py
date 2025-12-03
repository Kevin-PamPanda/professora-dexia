# src/cli_app.py
from .models import UserPreferences, UserInput
from .dexia_engine import gerar_time_com_professora_dexia

def perguntar_usuario() -> UserInput:
    print("=== Laboratório da Professora Dexia ===")
    formato = input("Formato (singles/doubles): ").strip().lower()
    estilo = input("Estilo de jogo (agressivo/balanceado/defensivo): ").strip().lower()
    nivel = input("Seu nível como jogador (iniciante/intermediario/pro): ").strip().lower()
    if nivel not in ("iniciante", "intermediario", "pro"):
        print("Nível não reconhecido. Vou assumir 'iniciante'.")
        nivel = "iniciante"
    regulamentacao = input("Regulamentação (Reg H, Reg J, VGC, OU, UU, etc.): ").strip()

    print("\nDigite os Pokémon que você quer obrigatoriamente no time (0 a 6).")
    print("Separe por vírgula, ou deixe vazio se não tiver preferência.")
    pokes_str = input("Pokémon: ").strip()
    if pokes_str:
        pokemons_existentes = [p.strip() for p in pokes_str.split(",")]
    else:
        pokemons_existentes = []

    print("\nEscreva qualquer informação extra para a Professora Dexia (ex: 'tenho dificuldade contra chuva', 'não gosto de usar lendário').")
    msg_extra = input("Mensagem: ").strip()
    if not msg_extra:
        msg_extra = None

    prefs = UserPreferences(
        formato=formato,
        estilo_jogo=estilo,
        regulamentacao=regulamentacao,
        nivel_jogador=nivel,
    )


    user_input = UserInput(
        preferencias=prefs,
        pokemons_existentes=pokemons_existentes,
        mensagem_livre=msg_extra,
    )

    return user_input

def exibir_time_formatado(data: dict) -> None:
    print("\n=== Time sugerido pela Professora Dexia ===\n")

    time = data.get("time", [])
    for idx, poke in enumerate(time, start=1):
        print(f"[{idx}] {poke.get('nome', '???')}")
        print(f"  Item: {poke.get('item', '-')}")
        print(f"  Habilidade: {poke.get('habilidade', '-')}")
        print(f"  Nature: {poke.get('nature', '-')}")
        print(f"  EVs: {poke.get('evs', '-')}")
        ivs = poke.get("ivs", "")
        if ivs:
            print(f"  IVs: {ivs}")
        moves = poke.get("moveset", [])
        if moves:
            print("  Moveset:")
            for m in moves:
                print(f"    - {m}")
        papel = poke.get("papel", "")
        if papel:
            print(f"  Papel no time: {papel}")
        print()

    plano = data.get("plano_de_jogo", "")
    if plano:
        print("=== Plano de jogo ===")
        print(plano)
        print()

def main():
    user_input = perguntar_usuario()
    print("\nGerando resposta da Professora Dexia...\n")
    data, raw_text = gerar_time_com_professora_dexia(user_input)

    if data is None:
        print("⚠ Não consegui interpretar a resposta como JSON válido.")
        print("Resposta bruta da IA:\n")
        print(raw_text)
    else:
        exibir_time_formatado(data)

if __name__ == "__main__":
    main()
