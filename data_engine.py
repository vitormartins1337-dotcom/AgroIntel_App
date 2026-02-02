# ARQUIVO: data_engine.py
# VERSÃO: V5 - HUNTER (Busca recursiva por biologia.json e manejo_avancado.json)

import json
import streamlit as st
import os
from pathlib import Path

# Função auxiliar para mesclar dicionários profundamente
def deep_merge(dict1, dict2):
    for key, value in dict2.items():
        if key in dict1 and isinstance(dict1[key], dict) and isinstance(value, dict):
            deep_merge(dict1[key], value)
        else:
            dict1[key] = value

@st.cache_data(show_spinner=False)
def get_database():
    combined_data = {}
    
    # Define o caminho absoluto para evitar erros de pasta não encontrada
    base_dir = Path(os.path.dirname(os.path.abspath(__file__)))
    db_folder = base_dir / "database"

    if not db_folder.exists():
        print("⚠️ Pasta database não encontrada.")
        return {}

    print(f"🚜 Data Engine: Varrendo {db_folder}...")

    # O os.walk desce em TODAS as subpastas, não importa a profundidade
    for root, dirs, files in os.walk(db_folder):
        
        # Só nos interessa pastas que tenham 'biologia.json'
        if "biologia.json" in files:
            cultura_path = Path(root)
            dados_cultura = {"vars": {}, "fases": {}, "t_base": 10}
            nome_cultura = None

            # 1. CARREGA BIOLOGIA (Obrigatório)
            try:
                with open(cultura_path / "biologia.json", 'r', encoding='utf-8') as f:
                    d_bio = json.load(f)
                    # Pega a primeira chave (Ex: "Soja (Glycine max)")
                    nome_cultura = list(d_bio.keys())[0]
                    # Preenche os dados base
                    dados_cultura = d_bio[nome_cultura]
            except Exception as e:
                print(f"❌ Erro lendo biologia em {cultura_path.name}: {e}")
                continue

            # 2. CARREGA MANEJO AVANÇADO (Opcional, mas desejado)
            if "manejo_avancado.json" in files:
                try:
                    with open(cultura_path / "manejo_avancado.json", 'r', encoding='utf-8') as f:
                        d_man = json.load(f)
                        # Verifica se a chave bate ou pega a primeira disponível
                        chave_man = list(d_man.keys())[0]
                        dados_manejo = d_man[chave_man]
                        
                        # AQUI ACONTECE A MÁGICA:
                        # O Engine injeta a química e estratégias dentro da biologia
                        # Ele procura pelas fases (Ex: "V3", "R1") e mescla os dados
                        if "fases" in dados_manejo:
                            for fase_nome, conteudos in dados_manejo["fases"].items():
                                if fase_nome in dados_cultura["fases"]:
                                    # Adiciona/Atualiza a lista 'quimica' na fase correspondente
                                    if "quimica" in conteudos:
                                        dados_cultura["fases"][fase_nome]["quimica"] = conteudos["quimica"]
                                    # Se tiver outras infos de manejo extra, adiciona também
                                    if "manejo_extra" in conteudos:
                                        dados_cultura["fases"][fase_nome]["manejo_extra"] = conteudos["manejo_extra"]

                except Exception as e:
                    print(f"⚠️ Erro lendo manejo em {cultura_path.name}: {e}")

            # Adiciona ao dicionário final se tudo deu certo
            if nome_cultura:
                combined_data[nome_cultura] = dados_cultura
                print(f"✅ Cultura Carregada: {nome_cultura}")

    return combined_data
