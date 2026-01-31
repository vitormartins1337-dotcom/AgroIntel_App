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
    
    # Localiza a pasta onde o script está
    base_dir = Path(__file__).parent.resolve()
    db_folder = base_dir / "database"
    
    # Verifica se a pasta existe
    if not db_folder.exists():
        st.error(f"Pasta database não encontrada em: {db_folder}")
        return {}

    # Lê todos os JSONs em todas as subpastas
    json_files = list(db_folder.rglob("*.json"))
    
    # --- AQUI ESTAVA O ERRO: FALTAVA O LOOP FOR ---
    for json_file in json_files:
        try:
            # 1. PULA O ARQUIVO SE ESTIVER VAZIO (0 BYTES)
            # Isso evita o erro "Expecting value: line 1 column 1"
            if json_file.stat().st_size == 0:
                continue

            # 2. TENTA LER O ARQUIVO
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                # 3. FUNDE COM O BANCO GERAL
                combined_data = deep_update(combined_data, data)
                
        except json.JSONDecodeError as e:
            # Mostra erro específico se o JSON estiver mal formatado (vírgula sobrando, etc)
            st.warning(f"Erro de formatação no arquivo {json_file.name}: {e}")
            
        except Exception as e:
            # Erro genérico
            st.warning(f"Não foi possível ler {json_file.name}: {e}")

    return combined_data
