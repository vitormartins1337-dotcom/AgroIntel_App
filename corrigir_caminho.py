import os
import json

# 1. Caminho EXATO revelado pelo erro
caminho_arquivo = "database/01_Graos/01_Soja/biologia.json"

# 2. O Conteúdo Padrão Ouro (Sem Erros)
conteudo_soja = {
  "Soja (Glycine max)": {
    "t_base": 10,
    "vars": {
      "Intacta 2 Xtend": {
        "kc": 1.15,
        "gda_meta": 1380,
        "info": "Tecnologia I2X. Resistência a Dicamba."
      },
      "Brasmax": {
        "kc": 1.15,
        "gda_meta": 1350,
        "info": "Alto teto produtivo."
      }
    },
    "fases": {
      "V3 - Vegetativo": {
        "desc": "Terceiro trifólio.",
        "fisiologia": "Definição de nós.",
        "manejo": "Monitorar lagartas."
      },
      "R1 - Início Floração": {
        "desc": "Flor aberta.",
        "fisiologia": "Mudança hormonal.",
        "manejo": "Fungicida obrigatório."
      }
    }
  }
}

# 3. Gravação Forçada
try:
    # Garante que a pasta existe (caso tenha sido apagada parcialmente)
    os.makedirs(os.path.dirname(caminho_arquivo), exist_ok=True)
    
    with open(caminho_arquivo, "w", encoding="utf-8") as f:
        json.dump(conteudo_soja, f, indent=2, ensure_ascii=False)
    
    print(f"✅ SUCESSO! O arquivo em '{caminho_arquivo}' foi recuperado.")

except Exception as e:
    print(f"❌ ERRO: {e}")
