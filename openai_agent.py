"""
G3 - OpenAI Agents SDK: Agente de Cálculo Matemático
Disciplina: Tópicos em Engenharia de Software - PUC-Campinas
Checkpoint 2 - Comparação comportamental entre SDKs
"""

import os
import time
from dotenv import load_dotenv
from agents import Agent, Runner, function_tool

load_dotenv()

# ── Ferramenta de cálculo ────────────────────────────────────────────────────

@function_tool
def calcular_media(numeros: list[float]) -> float:
    """Calcula a média aritmética de uma lista de números."""
    if not numeros:
        return 0.0
    return sum(numeros) / len(numeros)

@function_tool
def calcular_soma(numeros: list[float]) -> float:
    """Calcula a soma de uma lista de números."""
    return sum(numeros)

@function_tool
def calcular_maximo(numeros: list[float]) -> float:
    """Retorna o maior número de uma lista."""
    return max(numeros) if numeros else 0.0

# ── Agente ───────────────────────────────────────────────────────────────────

agente = Agent(
    name="AgenteCalculoOpenAI",
    instructions=(
        "Você é um assistente de cálculo matemático. "
        "Use as ferramentas disponíveis para realizar operações numéricas "
        "e apresente os resultados de forma clara e objetiva."
    ),
    tools=[calcular_media, calcular_soma, calcular_maximo],
    model="gpt-4o-mini",
)

# ── Execução e coleta de métricas ────────────────────────────────────────────

TAREFA = (
    "Tenho as seguintes notas de alunos: 7.5, 8.0, 6.5, 9.0, 7.0. "
    "Calcule a média, a soma total e qual foi a maior nota."
)

def executar():
    print("=" * 60)
    print("SDK: OpenAI Agents SDK")
    print("Modelo: gpt-4o-mini")
    print("=" * 60)
    print(f"Tarefa: {TAREFA}\n")

    inicio = time.perf_counter()
    resultado = Runner.run_sync(agente, TAREFA)
    fim = time.perf_counter()

    tempo_execucao = fim - inicio

    print(f"Resposta:\n{resultado.final_output}\n")
    print("-" * 60)
    print("── MÉTRICAS ──")
    print(f"Tempo de execução : {tempo_execucao:.3f}s")

    # Contagem de tool calls via histórico de mensagens
    tool_calls = sum(
        1
        for msg in resultado.new_messages
        if hasattr(msg, "role") and msg.role == "assistant"
        and hasattr(msg, "tool_calls") and msg.tool_calls
    )
    print(f"Chamadas de tool  : {tool_calls}")
    print(f"Total de mensagens: {len(resultado.new_messages)}")
    print("-" * 60)

    return {
        "sdk": "OpenAI Agents SDK",
        "modelo": "gpt-4o-mini",
        "resposta": resultado.final_output,
        "tempo_s": round(tempo_execucao, 3),
        "tool_calls": tool_calls,
        "n_mensagens": len(resultado.new_messages),
    }

if __name__ == "__main__":
    metricas = executar()
