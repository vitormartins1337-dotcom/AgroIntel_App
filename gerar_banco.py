# ARQUIVO: gerar_banco.py
import json
import os
from pathlib import Path

# 1. Definição dos Caminhos
base_dir = Path("database")
dir_soja = base_dir / "01_Soja"

# Cria as pastas se não existirem
os.makedirs(dir_soja, exist_ok=True)

# ---------------------------------------------------------
# 2. CONTEÚDO DA BIOLOGIA (Soja)
# ---------------------------------------------------------
dados_biologia = {
  "Soja (Glycine max)": {
    "t_base": 10,
    "vars": {
      "Intacta 2 Xtend (I2X)": {
        "kc": 1.15,
        "gda_meta": 1380,
        "info": "Biotecnologia I2X. Tolerância a Dicamba/Glifosato. Refúgio 20% obrigatório."
      },
      "Brasmax": {
        "kc": 1.15,
        "gda_meta": 1350,
        "info": "Alto teto produtivo. Exige alta fertilidade de solo."
      }
    },
    "fases": {
      "VE - Emergência": {
        "desc": "Cotilédones acima do solo.",
        "fisiologia": "Início da autotrofia. Raiz pivotante descendo.",
        "manejo": "Avaliação de stand e pragas de solo."
      },
      "V3 - Terceiro Trifólio": {
        "desc": "Três nós abertos.",
        "fisiologia": "Definição de nós produtivos. FBN ativa.",
        "manejo": "Monitoramento de lagartas e ervas."
      },
      "R1 - Início Floração": {
        "desc": "Início do florescimento.",
        "fisiologia": "Mudança hormonal. Alta demanda de Boro.",
        "manejo": "Entrada obrigatória de fungicidas."
      },
      "R5.1 - Enchimento": {
        "desc": "Grãos perceptíveis (3mm).",
        "fisiologia": "Máxima translocação. Definição de peso.",
        "manejo": "Controle rigoroso de Percevejos."
      }
    }
  }
}

# ---------------------------------------------------------
# 3. CONTEÚDO DO MANEJO AVANÇADO (Química/FRAC/IRAC)
# ---------------------------------------------------------
dados_manejo = {
  "Soja (Glycine max)": {
    "fases": {
      "R1 - Início Floração": {
        "quimica": [
          {
            "Alvo": "Ferrugem Asiática",
            "Ativo": "Protioconazol + Trifloxistrobina",
            "Codigos": "FRAC 3 + 11",
            "Tipo": "Químico Sistêmico",
            "Estrategia": "Base do programa preventivo."
          },
          {
            "Alvo": "Blindagem (Multissítio)",
            "Ativo": "Mancozebe",
            "Codigos": "FRAC M03",
            "Tipo": "Químico Protetor",
            "Estrategia": "Essencial para evitar resistência."
          },
          {
            "Alvo": "Bioestimulante",
            "Ativo": "Extrato de Algas + Aminoácidos",
            "Codigos": "Bio",
            "Tipo": "Fisiológico",
            "Estrategia": "Redução de abortamento floral."
          }
        ]
      },
      "R5.1 - Enchimento": {
        "quimica": [
          {
            "Alvo": "Percevejo Marrom",
            "Ativo": "Acefato",
            "Codigos": "IRAC 1B",
            "Tipo": "Químico Choque",
            "Estrategia": "Limpeza de área (Knockdown)."
          },
          {
            "Alvo": "Percevejo (Residual)",
            "Ativo": "Dinotefuram",
            "Codigos": "IRAC 4A",
            "Tipo": "Químico Sistêmico",
            "Estrategia": "Proteção prolongada."
          }
        ]
      }
    }
  }
}

# ---------------------------------------------------------
# 4. GRAVAÇÃO DOS ARQUIVOS (Perfeição Matemática)
# ---------------------------------------------------------
try:
    with open(dir_soja / "biologia.json", "w", encoding="utf-8") as f:
        json.dump(dados_biologia, f, indent=2, ensure_ascii=False)
    print("✅ Sucesso! Arquivo biologia.json criado.")

    with open(dir_soja / "manejo_avancado.json", "w", encoding="utf-8") as f:
        json.dump(dados_manejo, f, indent=2, ensure_ascii=False)
    print("✅ Sucesso! Arquivo manejo_avancado.json criado.")
    
except Exception as e:
    print(f"❌ Erro ao gravar: {e}")
