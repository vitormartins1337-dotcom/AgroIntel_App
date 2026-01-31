# ARQUIVO: data_engine.py
import json
import streamlit as st
from pathlib import Path
import collections.abc

def deep_update(d, u):
    """
    Função Mágica: Funde dois dicionários (Bio + Quimica) sem apagar dados.
    Se a chave existe nos dois, ele entra e funde o conteúdo interno.
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
        st.error("Pasta database não encontrada.")
        return {}

    # Lê todos os JSONs em todas as subpastas
    json_files = list(db_folder.rglob("*.json"))
    
    # DENTRO DO LOOP FOR no data_engine.py:
        try:
            # PULA O ARQUIVO SE ESTIVER VAZIO (0 BYTES)
            if json_file.stat().st_size == 0:
                continue

            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                combined_data = deep_update(combined_data, data)
        except Exception as e:
            st.warning(f"Erro no arquivo {json_file.name}: {e}")

    return combined_data
