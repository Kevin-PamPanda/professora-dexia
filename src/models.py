# src/models.py
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class UserPreferences:
    formato: str              # "singles" ou "doubles"
    estilo_jogo: str          # "agressivo", "balanceado", "defensivo"
    regulamentacao: str       # "Reg H", "Reg J", "VGC", "OU", "UU", etc.
    nivel_jogador: str        # "iniciante", "intermediario", "pro"

@dataclass
class PokemonSlot:
    nome: str
    habilidade: Optional[str] = None
    item: Optional[str] = None
    nature: Optional[str] = None
    evs: Optional[str] = None      # você pode começar como string simples "252 Atk / 252 Spe / 4 HP"
    ivs: Optional[str] = None
    moveset: Optional[List[str]] = None
    papel_time: Optional[str] = None  # sweeper, wall, suporte etc.
    imagem_url: Optional[str] = None  # futuro: link da imagem

@dataclass
class Team:
    pokemons: List[PokemonSlot]
    plano_de_jogo: Optional[str] = None  # explicação geral do time

@dataclass
class UserInput:
    preferencias: UserPreferences
    pokemons_existentes: List[str]   # lista de nomes que o usuário já quer no time (0 a 6)
    mensagem_livre: Optional[str] = None  # texto que o usuário escreveu pra Dexia
