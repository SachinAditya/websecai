
import httpx

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MODEL_NAME = "qwen3:1.7b"


async def ask_gemma(prompt: str) -> str:
    """Generate an AI response using local Ollama."""

    payload = {
        "model": MODEL_NAME,
        "prompt": (
            "You are WebSecAI, a defensive web security assistant. "
            "Analyze only the supplied scanner evidence. "
            "Do not invent vulnerabilities. "
            "Explain the issue, impact, and recommended fix.\n\n"
            f"{prompt}"
        ),
        "stream": False,
        "think": False,
        "options": {
            "temperature": 0.2,
            "num_predict": 300,
        },
    }

    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                OLLAMA_URL,
                json=payload,
            )
            response.raise_for_status()
            data = response.json()

        answer = data.get("response", "").strip()

        if not answer:
            return "AI analysis returned an empty response."

        return answer

    except httpx.ConnectError:
        return (
            "AI error: Cannot connect to Ollama. "
            "Make sure Ollama is running on this computer."
        )

    except httpx.TimeoutException:
        return "AI error: Ollama took too long to respond."

    except httpx.HTTPStatusError as exc:
        return f"AI error: Ollama returned HTTP {exc.response.status_code}."

    except (httpx.RequestError, ValueError, TypeError):
        return "AI error: Could not complete the local AI request."

