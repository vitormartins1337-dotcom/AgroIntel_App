import os
import json

# 1. Caminho Profissional
# Organizamos dentro de 'Graos' (ou 'Fibra' se preferir, mas Graos padroniza a pasta)
caminho_pasta = os.path.join("database", "01_Graos", "02_Algodao")
caminho_arquivo = os.path.join(caminho_pasta, "biologia.json")

# 2. CONTEÚDO PADRÃO OURO (ALGODÃO)
dados_algodao = {
  "Algodão (Gossypium hirsutum)": {
    "t_base": 15,
    "vars": {
      "FiberMax 985 GLTP": {
        "kc": 1.20,
        "gda_meta": 1650,
        "info": "Ciclo Médio. Tecnologia GlyTol Liberty TwinLink Plus. Alta tolerância a Ramulária. Exige manejo de regulador mais agressivo."
      },
      "TMG 44 B2RF": {
        "kc": 1.15,
        "gda_meta": 1580,
        "info": "Ciclo Precoce. Tecnologia Bollgard II RR Flex. Ideal para fechamento de plantio. Alta exigência de fertilidade."
      },
      "IMA 5801 B2RF": {
        "kc": 1.18,
        "gda_meta": 1600,
        "info": "Material rústico com alta estabilidade produtiva. Sistema radicular agressivo (tolerância a veranico)."
      }
    },
    "fases": {
      "V4 - Quarta Folha": {
        "desc": "Quarta folha verdadeira totalmente aberta.",
        "fisiologia": "Definição do potencial radicular. Planta sensível a competição por ervas daninhas e tripes.",
        "manejo": "Monitoramento de Tripes e Pulgão. Aplicação inicial de herbicidas em pós-emergência (Glufosinato/Glifosato).",
        "quimica": [
          {
            "Alvo": "Tripes/Pulgão",
            "Ativo": "Acefato ou Imidacloprido",
            "Tipo": "Químico Sistêmico",
            "Estrategia": "Controle inicial para evitar 'encharutamento' das folhas."
          },
          {
            "Alvo": "Ervas Daninhas",
            "Ativo": "Glufosinato de Amônio",
            "Tipo": "Herbicida Contato",
            "Estrategia": "Limpeza da entre-linha (se cultivar tolerante)."
          }
        ]
      },
      "B1 - Botão Floral (Pinhead)": {
        "desc": "Primeiro botão floral visível (cabeça de alfinete).",
        "fisiologia": "Mudança hormonal drástica (Vegetativo -> Reprodutivo). Início da demanda exponencial por Boro.",
        "manejo": "INÍCIO DO REGULADOR DE CRESCIMENTO (Obrigatório). Monitoramento de Bicudo nas bordaduras (Instalação de armadilhas).",
        "quimica": [
          {
            "Alvo": "Regulador de Crescimento",
            "Ativo": "Cloreto de Mepiquat",
            "Tipo": "Fisiológico",
            "Estrategia": "Dose baixa (50-100ml) para modular o crescimento sem travar a planta."
          },
          {
            "Alvo": "Bicudo (Bordadura)",
            "Ativo": "Malationa",
            "Tipo": "Químico Choque",
            "Estrategia": "Bateria de 3 aplicações a cada 5 dias SOMENTE na bordadura se houver captura em armadilha."
          },
          {
            "Alvo": "Bicudo (Biológico)",
            "Ativo": "Beauveria bassiana",
            "Tipo": "Biológico",
            "Estrategia": "Aplicação em área total para reduzir população hibernante."
          }
        ]
      },
      "F1 - Primeira Flor Branca": {
        "desc": "Abertura da primeira flor no primeiro ramo frutífero.",
        "fisiologia": "Pico de consumo de água e Potássio. A planta define quantas 'maçãs' vai segurar.",
        "manejo": "Manejo preventivo de Ramulária é MANDATÓRIO. Monitoramento de Lagartas no ponteiro.",
        "quimica": [
          {
            "Alvo": "Ramulária",
            "Ativo": "Azoxistrobina + Difenoconazol",
            "Tipo": "Químico Sistêmico",
            "Estrategia": "Rotação de ativos (Triazol + Estrobirulina). Adicionar protetor (Mancozebe)."
          },
          {
            "Alvo": "Lagartas (Spodoptera)",
            "Ativo": "Clorantraniliprole",
            "Tipo": "Químico Seletivo",
            "Estrategia": "Proteção das estruturas reprodutivas com produto de longa duração."
          }
        ]
      },
      "C1 - Maçã (Cutout)": {
        "desc": "Maçãs formadas no baixeiro, flores no ponteiro.",
        "fisiologia": "Enchimento de fibra. Cutout (a planta para de crescer para encher maçã). Dreno total de energia.",
        "manejo": "Controle de Ácaro Rajado (clima seco) e Bicudo (proteção da maçã nova).",
        "quimica": [
          {
            "Alvo": "Ácaro Rajado",
            "Ativo": "Abamectina + Espirodiclofeno",
            "Tipo": "Químico Acaricida",
            "Estrategia": "Aplicação com alto volume de calda para atingir face inferior da folha."
          },
          {
            "Alvo": "Bicudo (Área Total)",
            "Ativo": "Fipronil ou Beta-Ciflutrina",
            "Tipo": "Químico Choque",
            "Estrategia": "Se houver ataque em maçãs, entrada em área total."
          }
        ]
      },
      "M1 - Abertura de Capulhos": {
        "desc": "Primeiros capulhos abrindo no baixeiro.",
        "fisiologia": "Maturação da fibra. Senescência natural das folhas.",
        "manejo": "Planejamento da Desfolha e Maturação. Evitar 'mela' da fibra (Pulgão/Mosca Branca).",
        "quimica": [
          {
            "Alvo": "Maturação (Desfolha)",
            "Ativo": "Tidiazurom + Diurom",
            "Tipo": "Herbicida Desfolhante",
            "Estrategia": "Aplicar quando 60-70% dos capulhos estiverem abertos."
          },
          {
            "Alvo": "Acelerador de Abertura",
            "Ativo": "Etefom",
            "Tipo": "Fisiológico",
            "Estrategia": "Uniformiza a abertura para colheita mecânica única."
          }
        ]
      }
    }
  }
}

# 3. GRAVAÇÃO BLINDADA
try:
    # Cria a pasta se não existir
    os.makedirs(caminho_pasta, exist_ok=True)
    
    # Grava o arquivo
    with open(caminho_arquivo, "w", encoding="utf-8") as f:
        json.dump(dados_algodao, f, indent=2, ensure_ascii=False)
        
    print("="*50)
    print("✅ CULTURA CRIADA: ALGODÃO MASTER")
    print(f"Local: {caminho_arquivo}")
    print("Conteúdo: Fenologia, Reguladores, Manejo de Bicudo e Ramulária.")
    print("="*50)

except Exception as e:
    print(f"❌ Erro ao criar Algodão: {e}")
