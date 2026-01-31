# ARQUIVO: data_engine.py
# VERSÃO: Enterprise Silent (Ignora falhas sem travar o app)
import json
import streamlit as st
from pathlib import Path
import collections.abc

def deep_update(d, u):
    """
    Função recursiva para fundir dicionários (Merge Profundo).
    Garante que dados novos não apaguem dados antigos, apenas complementem.
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
    
    # 1. Localiza a pasta database de forma robusta
    base_dir = Path(__file__).parent.resolve()
    db_folder = base_dir / "database"
    
    # Se a pasta não existir, retorna vazio silenciosamente (sem erro vermelho)
    if not db_folder.exists():
        print(f"⚠️ Alerta: Pasta {db_folder} não encontrada.")
        return {}

    # 2. Varre todos os arquivos .json em todas as subpastas
    json_files = list(db_folder.rglob("*.json"))
    
    for json_file in json_files:
        try:
            # --- BLINDAGEM NÍVEL 1: Tamanho do Arquivo ---
            # Se for menor que 5 bytes (vazio ou só "{}"), pula silenciosamente.
            if json_file.stat().st_size < 5:
                continue 

            # --- BLINDAGEM NÍVEL 2: Leitura Segura ---
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                # Verifica se o JSON realmente tem dados (não é uma lista vazia ou null)
                if data:
                    combined_data = deep_update(combined_data, data)
                
        except (json.JSONDecodeError, OSError, UnicodeDecodeError):
            # --- BLINDAGEM NÍVEL 3: Supressão de Erro ---
            # Se der QUALQUER erro de leitura, nós NÃO mostramos st.error.
            # Apenas imprimimos no console (invisível para o usuário final) e continuamos.
            print(f"⚠️ Arquivo ignorado (corrompido/vazio): {json_file.name}")
            continue
            
        except Exception as e:
            # Erros genéricos também são apenas logados
            print(f"⚠️ Erro inesperado em {json_file.name}: {e}")
            continue

    return combined_data
