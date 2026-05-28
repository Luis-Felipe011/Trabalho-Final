"""
G3 - Google Agent Development Kit (ADK): Agente de Cálculo Matemático
Disciplina: Tópicos em Engenharia de Software - PUC-Campinas
Checkpoint 2 - Comparação comportamental entre SDKs
"""

import asyncio
import time
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

load_dotenv()

# ── Ferramentas de cálculo ───────────────────────────────────────────────────

def calcular_media(numeros: list) -> dict:
    """Calcula a média aritmética de uma lista de números.

    Args:
        numeros: Lista de números para calcular a média.

    Returns:
        Dicionário com o resultado da média.
    """
    if not numeros:
        return {"resultado": 0.0, "operacao": "média"}
    media = sum(numeros) / len(numeros)
    return {"resultado": round(media, 4), "operacao": "média"}


def calcular_soma(numeros: list) -> dict:
    """Calcula a soma de uma lista de números.

    Args:
        numeros: Lista de números para somar.

    Returns:
        Dicionário com o resultado da soma.
    """
    return {"resultado": sum(numeros), "operacao": "soma"}


def calcular_maximo(numeros: list) -> dict:
    """Retorna o maior número de uma lista.

    Args:
        numeros: Lista de números.

    Returns:
        Dicionário com o maior valor encontrado.
    """
    return {"resultado": max(numeros) if numeros else 0.0, "operacao": "máximo"}


# ── Agente ───────────────────────────────────────────────────────────────────

agente = Agent(
    name="agente_calculo_adk",
    model="gemini-1.5-flash",
    description="Agente de cálculo matemático usando Google ADK.",
    instruction=(
        "Você é um assistente de cálculo matemático. "
        "Use as ferramentas disponíveis para realizar operações numéricas "
        "e apresente os resultados de forma clara e objetiva."
    ),
    tools=[calcular_media, calcular_soma, calcular_maximo],
)

# ── Execução e coleta de métricas ────────────────────────────────────────────

TAREFA = (
    "Tenho as seguintes notas de alunos: 7.5, 8.0, 6.5, 9.0, 7.0. "
    "Calcule a média, a soma total e qual foi a maior nota."
)

APP_NAME = "g3_comparativo"
USER_ID  = "usuario_g3"
SESSION_ID = "sessao_01"


async def executar():
    print("=" * 60)
    print("SDK: Google Agent Development Kit (ADK)")
    print("Modelo: gemini-1.5-flash")
    print("=" * 60)
    print(f"Tarefa: {TAREFA}\n")

    session_service = InMemorySessionService()
    await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
    )

    runner = Runner(
        agent=agente,
        app_name=APP_NAME,
        session_service=session_service,
    )

    mensagem = types.Content(
        role="user",
        parts=[types.Part(text=TAREFA)],
    )

    inicio = time.perf_counter()
    eventos = []
    async for evento in runner.run_async(
        user_id=USER_ID,
        session_id=SESSION_ID,
        new_message=mensagem,
    ):
        eventos.append(evento)
    fim = time.perf_counter()

    tempo_execucao = fim - inicio

    resposta_final = ""
    tool_calls = 0
    for evento in eventos:
        if evento.is_final_response():
            resposta_final = evento.content.parts[0].text
        if hasattr(evento, "content") and evento.content:
            for part in evento.content.parts:
                if hasattr(part, "function_call") and part.function_call:
                    tool_calls += 1

    print(f"Resposta:\n{resposta_final}\n")
    print("-" * 60)
    print("── MÉTRICAS ──")
    print(f"Tempo de execução : {tempo_execucao:.3f}s")
    print(f"Chamadas de tool  : {tool_calls}")
    print(f"Total de eventos  : {len(eventos)}")
    print("-" * 60)

    return {
        "sdk": "Google ADK",
        "modelo": "gemini-2.0-flash",
        "resposta": resposta_final,
        "tempo_s": round(tempo_execucao, 3),
        "tool_calls": tool_calls,
        "n_eventos": len(eventos),
    }


if __name__ == "__main__":
    metricas = asyncio.run(executar())
