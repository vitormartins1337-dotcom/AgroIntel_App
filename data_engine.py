# ARQUIVO: data_engine.py
import json
import streamlit as st
from pathlib import Path
import collections.abc

def deep_update(d, u):
    """
    Funde dicionários aninhados (Biologia + Manejo)
    """
    for k, v in u.items():
        if isinstance(v, collections.abc.Mapping):
            d[k] = deep_update(d.get(k, {}), v)
        else:
            d[k] = v
    return d

@st.cache_data(show_spinner=False)
def get_database():
    combined_data = {}
    base_dir = Path(__file__).parent.resolve()
    db_folder = base_dir / "database"
    
    if not db_folder.exists():
        return {}

    # Busca em todas as subpastas
    json_files = list(db_folder.rglob("*.json"))
    
    for json_file in json_files:
        try:
            # 1. PROTEÇÃO CONTRA ARQUIVO VAZIO (O ERRO QUE VOCÊ TEVE)
            if json_file.stat().st_size < 5: # Menor que 5 bytes é lixo ou vazio
                continue

            # 2. CARREGAMENTO SEGURO
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                combined_data = deep_update(combined_data, data)

        except Exception as e:
            # Apenas imprime no terminal, não quebra o app
            print(f"Ignorando arquivo corrompido: {json_file.name} - {e}")

    return combined_data
