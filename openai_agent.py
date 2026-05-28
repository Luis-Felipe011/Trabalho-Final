"""
G3 - OpenAI Agents SDK: Agente de Cálculo Matemático
Disciplina: Tópicos em Engenharia de Software - PUC-Campinas
Checkpoint 2 - Comparação comportamental entre SDKs
"""

import asyncio
import os
import time
from agents import Agent, Runner, function_tool

# ── Ferramentas de cálculo ────────────────────────────────────────────────────

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

TAREFA = (
    "Tenho as seguintes notas de alunos: 7.5, 8.0, 6.5, 9.0, 7.0. "
    "Calcule a média, a soma total e qual foi a maior nota."
)

# ── Execução async (usada pelo comparativo.py) ────────────────────────────────

async def executar() -> dict:
    print("=" * 60)
    print("SDK: OpenAI Agents SDK")
    print("Modelo: gpt-4o-mini")
    print("=" * 60)
    print(f"Tarefa: {TAREFA}\n")

    inicio = time.perf_counter()
    resultado = await Runner.run(agente, TAREFA)
    fim = time.perf_counter()

    tempo_execucao = fim - inicio

    print(f"Resposta:\n{resultado.final_output}\n")
    print("-" * 60)
    print("── MÉTRICAS ──")
    print(f"Tempo de execução : {tempo_execucao:.3f}s")

    # Contagem de tool calls via raw_responses (versões recentes do SDK)
    tool_calls = 0
    n_mensagens = 0
    try:
        for resp in resultado.raw_responses:
            output = resp.output if isinstance(resp.output, list) else []
            for item in output:
                n_mensagens += 1
                if hasattr(item, "type") and item.type == "function_call":
                    tool_calls += 1
    except Exception:
        pass

    # fallback para versões que expõem new_messages
    if n_mensagens == 0:
        try:
            msgs = resultado.new_messages
            n_mensagens = len(msgs)
            tool_calls = sum(
                1 for msg in msgs
                if hasattr(msg, "role") and msg.role == "assistant"
                and hasattr(msg, "tool_calls") and msg.tool_calls
            )
        except Exception:
            pass

    print(f"Chamadas de tool  : {tool_calls}")
    print(f"Total de mensagens: {n_mensagens}")
    print("-" * 60)

    return {
        "sdk": "OpenAI Agents SDK",
        "modelo": "gpt-4o-mini",
        "resposta": resultado.final_output,
        "tempo_s": round(tempo_execucao, 3),
        "tool_calls": tool_calls,
        "n_mensagens": n_mensagens,
    }

if __name__ == "__main__":
    asyncio.run(executar())