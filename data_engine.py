# ARQUIVO: data_engine.py
import json
import streamlit as st
import os
from pathlib import Path

@st.cache_data(show_spinner=False)
def get_database():
    combined_data = {}
    base_dir = Path(os.path.dirname(os.path.abspath(__file__)))
    db_folder = base_dir / "database"

    if not db_folder.exists():
        return {}

    # Varre as pastas de culturas (ex: 01_Soja, 02_Algodao)
    for root, dirs, files in os.walk(db_folder):
        # Filtramos para agir apenas em pastas que contenham arquivos JSON
        if not any(f.endswith('.json') for f in files):
            continue
            
        cultura_dir = Path(root)
        dados_cultura = {"vars": {}, "fases": {}, "t_base": 10}
        nome_cultura = None

        # 1. Tenta carregar BIOLOGIA (Genética + Estádios)
        f_bio = cultura_dir / "biologia.json"
        if f_bio.exists():
            try:
                with open(f_bio, 'r', encoding='utf-8') as f:
                    d = json.load(f)
                    # O JSON pode ter o nome da cultura como chave principal
                    first_key = list(d.keys())[0]
                    nome_cultura = first_key
                    dados_cultura["vars"] = d[first_key].get("vars", {})
                    dados_cultura["fases"] = d[first_key].get("fases", {})
                    dados_cultura["t_base"] = d[first_key].get("t_base", 10)
            except Exception as e:
                print(f"Erro no biologia.json de {cultura_dir.name}: {e}")

        # 2. Tenta carregar MANEJO_AVANCADO (Protocolos Químicos)
        f_man = cultura_dir / "manejo_avancado.json"
        if f_man.exists():
            try:
                with open(f_man, 'r', encoding='utf-8') as f:
                    d_man = json.load(f)
                    key = list(d_man.keys())[0]
                    protocolos = d_man[key].get("fases", {})
                    
                    # Mescla a química dentro da fase correspondente na biologia
                    for fase_nome, info_man in protocolos.items():
                        if fase_nome in dados_cultura["fases"]:
                            dados_cultura["fases"][fase_nome]["quimica"] = info_man.get("quimica", [])
            except Exception as e:
                print(f"Erro no manejo_avancado.json de {cultura_dir.name}: {e}")

        if nome_cultura:
            combined_data[nome_cultura] = dados_cultura

    return combined_data
