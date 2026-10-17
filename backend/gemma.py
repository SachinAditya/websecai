import os
import httpx

HF_API_URL = "https://router.huggingface.co/v1/chat/completions"
MODEL_NAME = "google/gemma-2-2b-it"


async def ask_gemma(prompt: str) -> str:
    """
    Send a prompt to Hugging Face Inference Providers
    and return the generated AI response.
    """

    token = os.getenv("HF_TOKEN")

    if not token:
        return "AI analysis unavailable: HF_TOKEN is not configured."

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "user",
                "content": prompt,
            }
        ],
        "max_tokens": 250,
        "temperature": 0.2,
        "stream": False,
    }

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                HF_API_URL,
                headers=headers,
                json=payload,
            )

            response.raise_for_status()
            result = response.json()

        content = result["choices"][0]["message"]["content"]

        if not isinstance(content, str) or not content.strip():
            return "AI analysis returned an empty response."

        return content.strip()

    except httpx.HTTPStatusError as exc:
        status = exc.response.status_code

        if status in (401, 403):
            return (
                "AI error: Check HF_TOKEN and its "
                "Inference Providers permissions."
            )

        if status == 429:
            return (
                "AI error: Inference quota or rate limit reached."
            )

        if status in (400, 404):
            return (
                f"AI error: Hugging Face returned HTTP {status}. "
                "Check model availability and request parameters."
            )

        return f"AI error: Hugging Face returned HTTP {status}."

    except httpx.TimeoutException:
        return "AI error: The hosted AI request timed out."

    except httpx.RequestError:
        return "AI error: Could not connect to the hosted AI service."

    except (ValueError, KeyError, IndexError, TypeError):
        return "AI error: The hosted AI returned an unexpected response."
