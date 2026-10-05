import httpx


OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MODEL_NAME = "gemma3:4b"


async def ask_gemma(prompt: str) -> str:
    payload = {
    "model": MODEL_NAME,
    "prompt": prompt,
    "stream": False,
    "options": {
        "temperature": 0.2,
        "num_predict": 300
    }
}
    try:
        async with httpx.AsyncClient(
            timeout=90.0,
            trust_env=False
        ) as client:

            response = await client.post(
                OLLAMA_URL,
                json=payload
            )

        response.raise_for_status()

        data = response.json()

        return data.get(
            "response",
            "Gemma did not return a response."
        )

    except httpx.ConnectError as error:
        return f"Unable to connect to Ollama at {OLLAMA_URL}: {error}"

    except httpx.TimeoutException as error:
        return f"Ollama request timed out: {error}"

    except httpx.HTTPStatusError as error:
        return f"Gemma/Ollama returned an HTTP error: {error}"

    except httpx.RequestError as error:
        return f"Ollama request error: {error}"

    except Exception as error:
        return f"Unexpected AI error: {error}"