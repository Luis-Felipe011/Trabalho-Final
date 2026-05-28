"""
G3 - Google Agent Development Kit (ADK): Agente de Cálculo Matemático
Disciplina: Tópicos em Engenharia de Software - PUC-Campinas
Checkpoint 2 - Comparação comportamental entre SDKs
"""

import asyncio
import os
import time
from dotenv import load_dotenv
load_dotenv()

from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "")
if not GOOGLE_API_KEY:
    raise EnvironmentError(
        "\n❌ GOOGLE_API_KEY não encontrada!\n"
        "Verifique se o arquivo .env contém:\n"
        "   GOOGLE_API_KEY=AIza...\n"
    )

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
    return {"resultado": round(sum(numeros) / len(numeros), 4), "operacao": "média"}


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


# ── Modelos a tentar (ordem de preferência) ──────────────────────────────────
MODELOS_CANDIDATOS = [
    "gemini-2.5-flash",    # confirmado funcional
    "gemini-2.0-flash",    # fallback
    "gemini-2.0-flash-lite",
]

TAREFA = (
    "Tenho as seguintes notas de alunos: 7.5, 8.0, 6.5, 9.0, 7.0. "
    "Calcule a média, a soma total e qual foi a maior nota."
)

APP_NAME   = "g3_comparativo"
USER_ID    = "usuario_g3"
SESSION_ID = "sessao_01"


async def _tentar_modelo(modelo: str) -> dict:
    agente = Agent(
        name="agente_calculo_adk",
        model=modelo,
        description="Agente de cálculo matemático usando Google ADK.",
        instruction=(
            "Você é um assistente de cálculo matemático. "
            "Use as ferramentas disponíveis para realizar operações numéricas "
            "e apresente os resultados de forma clara e objetiva."
        ),
        tools=[calcular_media, calcular_soma, calcular_maximo],
    )

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

    resposta_final = ""
    tool_calls = 0
    for evento in eventos:
        if hasattr(evento, "is_final_response") and evento.is_final_response():
            if evento.content and evento.content.parts:
                resposta_final = evento.content.parts[0].text
        if hasattr(evento, "content") and evento.content:
            for part in evento.content.parts:
                if hasattr(part, "function_call") and part.function_call:
                    tool_calls += 1

    return {
        "sdk": "Google ADK",
        "modelo": modelo,
        "resposta": resposta_final,
        "tempo_s": round(fim - inicio, 3),
        "tool_calls": tool_calls,
        "n_eventos": len(eventos),
    }


async def executar() -> dict:
    print("=" * 60)
    print("SDK: Google Agent Development Kit (ADK)")
    print("=" * 60)
    print(f"Tarefa: {TAREFA}\n")

    ultimo_erro = None
    for modelo in MODELOS_CANDIDATOS:
        print(f"  → Tentando modelo: {modelo} ...", end=" ", flush=True)
        try:
            metricas = await _tentar_modelo(modelo)
            print("OK ✅")
            print(f"\nModelo usado    : {modelo}")
            print(f"Resposta:\n{metricas['resposta']}\n")
            print("-" * 60)
            print("── MÉTRICAS ──")
            print(f"Tempo de execução : {metricas['tempo_s']}s")
            print(f"Chamadas de tool  : {metricas['tool_calls']}")
            print(f"Total de eventos  : {metricas['n_eventos']}")
            print("-" * 60)
            return metricas
        except Exception as e:
            msg = str(e)
            if "429" in msg or "RESOURCE_EXHAUSTED" in msg:
                print("quota esgotada ⚠️")
                ultimo_erro = e
            else:
                print(f"erro ❌: {msg[:120]}")
                ultimo_erro = e

    print("\n❌ Nenhum modelo disponível. Verifique sua GOOGLE_API_KEY.")
    raise ultimo_erro


if __name__ == "__main__":
    asyncio.run(executar())