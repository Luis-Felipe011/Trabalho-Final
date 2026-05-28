# G3 — OpenAI Agents SDK vs Google ADK

**PUC-Campinas · Sistemas de Informação · Tópicos em Engenharia de Software**  
Prof. Douglas H. S. Abreu · 2026/1

## Integrantes

| Nome | Responsabilidade |
|------|-----------------|
| Bernardo | Arquitetura comparativa e análise técnica |
| Geovana | Pesquisa bibliográfica e síntese acadêmica |
| Leonardo | OpenAI Agents SDK — levantamento e primitivas |
| Luis Felipe | Mini-projeto: script comparativo |
| Samantha | Google ADK — levantamento e README |

---

## Objetivo

Comparação comportamental entre o **OpenAI Agents SDK** e o **Google Agent Development Kit (ADK)** para construção de agentes de IA baseados em LLMs.

Ambos os SDKs instanciam o **mesmo agente de cálculo matemático** (calcular média, soma e máximo de uma lista de notas), permitindo análise objetiva das diferenças de:

- Sintaxe e configuração de ferramentas
- Inicialização e execução do agente
- Ergonomia da API
- Traces e saídas geradas

---

## Estrutura do Repositório

```
.
├── openai_agent.py          # Agente via OpenAI Agents SDK (gpt-4o-mini)
├── google_adk_agent.py      # Agente via Google ADK (gemini-2.0-flash)
├── comparativo.py           # Executa ambos e gera tabela comparativa
├── resultados_comparativos.json  # Saídas e métricas (gerado ao rodar)
├── requirements.txt         # Dependências
└── README.md
```

---

## Pré-requisitos

- Python 3.11+
- Chaves de API:
  - `OPENAI_API_KEY` — [platform.openai.com](https://platform.openai.com)
  - `GOOGLE_API_KEY` ou `GOOGLE_GENAI_USE_VERTEXAI=true` — [aistudio.google.com](https://aistudio.google.com)

---

## Instalação

```bash
# Clone o repositório
git clone https://github.com/Luis-Felipe011/Trabalho-Final.git
cd Trabalho-Final

# Crie e ative um ambiente virtual
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows

# Instale as dependências
pip install -r requirements.txt
```

---

## Configuração das Chaves de API

```bash
# Linux/macOS
export OPENAI_API_KEY="sk-..."
export GOOGLE_API_KEY="AIza..."

# Windows (PowerShell)
$env:OPENAI_API_KEY=""
$env:GOOGLE_API_KEY=""
```

Ou crie um arquivo `.env` na raiz:

```
OPENAI_API_KEY=sk-...
GOOGLE_API_KEY=AIza...
```

---

## Como Rodar

### Rodar apenas o agente OpenAI

```bash
python openai_agent.py
```

### Rodar apenas o agente Google ADK

```bash
python google_adk_agent.py
```

### Rodar a comparação completa (recomendado)

```bash
python comparativo.py
```

Gera no terminal a tabela comparativa e salva `resultados_comparativos.json`.

---

## Tarefa do Agente

> *"Tenho as seguintes notas de alunos: 7.5, 8.0, 6.5, 9.0, 7.0.  
> Calcule a média, a soma total e qual foi a maior nota."*

Ambos os agentes dispõem das mesmas três ferramentas:
- `calcular_media(numeros)` — média aritmética
- `calcular_soma(numeros)` — soma total
- `calcular_maximo(numeros)` — maior valor

---

## Métricas Coletadas

| Métrica | Descrição |
|---------|-----------|
| Tempo de execução (s) | Tempo total da chamada ao SDK |
| Chamadas de tool | Número de invocações de ferramentas |
| Unidades de fluxo | Mensagens (OpenAI) vs Eventos (ADK) |

---

## Principais Diferenças Observadas

| Critério | OpenAI Agents SDK | Google ADK |
|----------|-------------------|------------|
| Definição de tool | `@function_tool` + type hints | `def` + docstring Args/Returns + `dict` |
| Execução | `Runner.run_sync(agent, task)` | `Runner` + `SessionService` + `Content` |
| Gestão de sessão | Automática | Explícita (`InMemorySessionService`) |
| Modelo | GPT-4o-mini | Gemini 2.0 Flash |
| Protocolo A2A | Não | Sim (nativo) |
| Multi-linguagem | Não (Python-first) | Sim (Java, Go, Python) |
| Tracing nativo | Sim (dashboard OpenAI) | Sim (Cloud Trace / stdout) |
| Vendor lock-in | Alto | Médio |

---

## Referências

1. OPENAI. *OpenAI Agents SDK: Official Documentation*. 2025. https://openai.github.io/openai-agents-python
2. GOOGLE. *Agent Development Kit (ADK): Official Documentation*. 2025. https://google.github.io/adk-docs
3. OPENAI. *OpenAI Agents SDK: GitHub Repository*. 2025. https://github.com/openai/openai-agents-python
4. GOOGLE. *ADK: GitHub Repository*. 2025. https://github.com/google/adk-python
5. WANG, L. et al. A Survey on Large Language Model based Autonomous Agents. *Frontiers of Computer Science*, v. 18, n. 6, 2024.
6. WU, Q. et al. AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation. arXiv:2308.08155, 2023.
7. ANTHROPIC. *Building Effective Agents*. 2024. https://anthropic.com/research/building-effective-agents
8. ANTHROPIC. *Tool Use (Function Calling): Claude Platform Docs*. 2025. https://platform.claude.com/docs
