import os
import json

# Caminho exato onde está o arquivo do Algodão
caminho_arquivo = os.path.join("database", "01_Graos", "02_Algodao", "biologia.json")

# Conteúdo RICO e DETALHADO (Preenchendo o campo 'Estrategia')
dados_algodao_master = {
  "Algodão (Gossypium hirsutum)": {
    "t_base": 15,
    "vars": {
      "FiberMax 985 GLTP": {
        "kc": 1.20,
        "gda_meta": 1650,
        "info": "Ciclo Médio. Tecnologia GlyTol Liberty TwinLink Plus. Alta tolerância a Ramulária. Exige manejo de regulador mais agressivo devido ao alto vigor."
      },
      "TMG 44 B2RF": {
        "kc": 1.15,
        "gda_meta": 1580,
        "info": "Ciclo Precoce. Tecnologia Bollgard II RR Flex. Ideal para fechamento de plantio. Atenção redobrada com Ramulária no final de ciclo."
      }
    },
    "fases": {
      "V4 - Quarta Folha": {
        "desc": "Quarta folha verdadeira exposta. Início da definição produtiva.",
        "fisiologia": "Planta define o sistema radicular. Período crítico de competição com daninhas (Matocompetição zero).",
        "manejo": "Manejo de Tripes (evitar engruvinhamento) e Pulgão. Aplicação de herbicidas seletivos.",
        "quimica": [
          {
            "Alvo": "Tripes e Pulgão",
            "Ativo": "Acefato / Imidacloprido",
            "Grupo": "Organofosforado / Neonicotinoide",
            "Tipo": "Químico Sistêmico",
            "Estrategia": "Controle preventivo para evitar danos no meristema apical e transmissão de viroses (Mosaico)."
          }
        ]
      },
      "B1 - Botão Floral (Pinhead)": {
        "desc": "Primeiros botões florais (cabeça de alfinete) visíveis.",
        "fisiologia": "Transição hormonal. A planta começa a priorizar estruturas reprodutivas. Alta demanda de Boro.",
        "manejo": "Início obrigatório do Regulador. Instalação de armadilhas para Bicudo. Monitoramento de bordaduras.",
        "quimica": [
          {
            "Alvo": "Bicudo (Monitoramento/Borda)",
            "Ativo": "Malationa",
            "Grupo": "Organofosforado",
            "Tipo": "Choque (Baixa Seletividade)",
            "Estrategia": "Bateria de 3 aplicações (intervalo 3-5 dias) APENAS nas bordaduras e reboleiras. Foco em eliminar fêmeas migrantes antes da oviposição."
          },
          {
            "Alvo": "Regulador de Crescimento",
            "Ativo": "Cloreto de Mepiquat",
            "Grupo": "Inibidor de Giberelina",
            "Tipo": "Fisiológico (Dose baixa sequencial)",
            "Estrategia": "Sistema Pix: Doses baixas (50-70ml) e frequentes baseadas na taxa de crescimento. Objetivo é modular os internódios sem travar a planta."
          }
        ]
      },
      "F1 - Primeira Flor Branca": {
        "desc": "Abertura da primeira flor no primeiro ramo frutífero.",
        "fisiologia": "Máximo consumo de água e nutrientes (K). Definição da carga de capulhos.",
        "manejo": "Proteção total contra Ramulária. O baixeiro não pode ser perdido.",
        "quimica": [
          {
            "Alvo": "Ramulária (Preventivo)",
            "Ativo": "Azoxistrobina + Difenoconazol",
            "Grupo": "Estrob + Triazol",
            "Tipo": "Sistêmico",
            "Estrategia": "Aplicação preventiva mandatória. INDISPENSÁVEL adição de multissítio (Mancozebe/Clorotalonil) para evitar resistência e proteger folhas velhas."
          },
          {
            "Alvo": "Lagarta das Maçãs",
            "Ativo": "Clorantraniliprole",
            "Grupo": "Diamida",
            "Tipo": "Seletivo de Longa Duração",
            "Estrategia": "Proteção das estruturas reprodutivas. Produto de alta seletividade para inimigos naturais."
          }
        ]
      }
    }
  }
}

# --- GRAVAÇÃO DOS DADOS ---
try:
    os.makedirs(os.path.dirname(caminho_arquivo), exist_ok=True)
    with open(caminho_arquivo, "w", encoding="utf-8") as f:
        json.dump(dados_algodao_master, f, indent=2, ensure_ascii=False)
    
    print("="*50)
    print("✅ ESTRATÉGIAS AGRONÔMICAS ATUALIZADAS COM SUCESSO!")
    print(f"Arquivo: {caminho_arquivo}")
    print("O 'None' foi substituído por recomendações técnicas detalhadas.")
    print("="*50)

except Exception as e:
    print(f"❌ Erro: {e}")
