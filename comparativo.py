"""
G3 - Análise Comparativa: OpenAI Agents SDK vs Google ADK
Disciplina: Tópicos em Engenharia de Software - PUC-Campinas
Checkpoint 2

Executa o mesmo agente de cálculo nos dois SDKs e gera
uma tabela comparativa lado a lado com métricas coletadas.
"""

import asyncio
import json

from openai_agent import executar as executar_openai
from google_adk_agent import executar as executar_adk


async def comparar():
    print("\n🔵 Executando OpenAI Agents SDK...")
    metricas_openai = await executar_openai()

    print("\n🟢 Executando Google ADK...")
    metricas_adk = await executar_adk()

    # ── Tabela comparativa ───────────────────────────────────────────────────
    print("\n")
    print("=" * 70)
    print("          ANÁLISE COMPARATIVA — G3 | PUC-Campinas")
    print("          OpenAI Agents SDK  vs  Google ADK")
    print("=" * 70)

    cabecalho = f"{'Critério':<30} {'OpenAI Agents SDK':<20} {'Google ADK':<20}"
    print(cabecalho)
    print("-" * 70)

    linhas = [
        ("Modelo LLM",           metricas_openai["modelo"],          metricas_adk["modelo"]),
        ("Tempo de execução (s)", str(metricas_openai["tempo_s"]),    str(metricas_adk["tempo_s"])),
        ("Chamadas de tool",      str(metricas_openai["tool_calls"]), str(metricas_adk["tool_calls"])),
        ("Unidade de fluxo",      "Mensagens",                        "Eventos"),
        ("Paradigma de config.",  "Decorator @function_tool",         "Docstring + tipo dict"),
        ("Inicialização runner",  "Runner.run(agent, task)",          "Runner(agent, app, session)"),
        ("Gestão de sessão",      "Automática (Runner)",              "InMemorySessionService"),
        ("Linguagem suportada",   "Python-first",                     "Multi-linguagem (Java, Go)"),
        ("Protocolo A2A nativo",  "Não",                              "Sim"),
        ("Tracing nativo",        "Sim (OpenAI dashboard)",           "Sim (Cloud Trace / stdout)"),
        ("Vendor lock-in",        "Alto (GPT)",                       "Médio (Gemini/Vertex)"),
    ]

    for criterio, val_openai, val_adk in linhas:
        print(f"{criterio:<30} {val_openai:<20} {val_adk:<20}")

    print("=" * 70)

    # ── Linhas de código ─────────────────────────────────────────────────────
    print("\n── CONTAGEM DE LINHAS DE CÓDIGO (linhas funcionais, sem comentários) ──")
    loc = {
        "Definição da ferramenta": {
            "openai": "4 linhas (@function_tool + def + docstring + return)",
            "adk":    "6 linhas (def + docstring Args/Returns + return dict)",
        },
        "Instância do agente": {
            "openai": "6 linhas (Agent: name, instructions, tools, model)",
            "adk":    "7 linhas (Agent: name, model, description, instruction, tools)",
        },
        "Execução do agente": {
            "openai": "1 linha  (await Runner.run)",
            "adk":    "8 linhas (session_service + session + Runner + Content + run)",
        },
    }
    for etapa, vals in loc.items():
        print(f"\n  {etapa}:")
        print(f"    OpenAI : {vals['openai']}")
        print(f"    ADK    : {vals['adk']}")

    print("\n── OBSERVAÇÕES SOBRE ERGONOMIA ──")
    print("""
  OpenAI Agents SDK:
  • API mais enxuta: @function_tool converte automaticamente type hints em schema JSON.
  • Runner.run abstrai toda a gestão de sessão — ideal para scripts rápidos.
  • Fortemente acoplado ao ecossistema OpenAI (modelos GPT, tracing no dashboard deles).

  Google ADK:
  • Mais verboso na inicialização: exige SessionService e Content/Part explícitos.
  • Ferramentas retornam dict (não tipos nativos), o que força um contrato mais explícito.
  • Protocolo A2A nativo e suporte multi-linguagem tornam-no mais adequado a sistemas
    distribuídos e enterprise.
  • Modelo de eventos (vs mensagens) oferece granularidade maior para observabilidade.
""")

    # ── Salva resultado em JSON ──────────────────────────────────────────────
    resultado = {"openai": metricas_openai, "adk": metricas_adk}
    with open("resultados_comparativos.json", "w", encoding="utf-8") as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)

    print("  ✅ Resultados salvos em resultados_comparativos.json")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(comparar())