# ARQUIVO: data_engine.py
import json
import streamlit as st
from pathlib import Path
import collections.abc
import os

def deep_update(d, u):
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
    
    # 1. DEBUG: Mostra na tela onde ele está procurando
    # st.warning(f"🕵️ Procurando arquivos na pasta: {db_folder}")

    if not db_folder.exists():
        return {}

    json_files = list(db_folder.rglob("*.json"))
    
    for json_file in json_files:
        try:
            # 2. IGNORA ARQUIVOS VAZIOS (A SOLUÇÃO DO SEU PROBLEMA)
            # Se o arquivo tiver menos de 5 bytes (vazio ou só chaves {}), ele pula.
            if json_file.stat().st_size < 5:
                # Opcional: Mostra qual arquivo está vazio para você saber
                print(f"⚠️ Ignorando arquivo vazio: {json_file.name}")
                continue

            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                combined_data = deep_update(combined_data, data)
                
        except json.JSONDecodeError as e:
            # 3. DEDO DURO: Mostra o caminho exato do arquivo com erro
            st.error(f"""
            ❌ ARQUIVO CORROMPIDO ENCONTRADO!
            Nome: {json_file.name}
            Localização Exata: {json_file.absolute()}
            Erro: O arquivo está em branco ou mal formatado.
            """)
        except Exception as e:
            st.warning(f"Erro genérico em {json_file.name}: {e}")

    return combined_data
