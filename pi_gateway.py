import os


class GatewayError(RuntimeError):
    """Pi AI gateway cannot serve the current Robin session."""


def get_workbench_cookie(streamlit_module):
    """Read the httpOnly session cookie from Streamlit's read-only request context."""
    try:
        return streamlit_module.context.cookies.get("workbench_session")
    except (AttributeError, KeyError):
        return None


def _headers(session_cookie: str) -> dict:
    if not session_cookie:
        raise GatewayError("无法读取工作台登录态，请从工作台内打开 Robin 后重试。")
    return {"Cookie": f"workbench_session={session_cookie}"}


def fetch_robin_config(session_cookie: str, base_url: str, get=None) -> dict | None:
    """Fetch only the selected provider/model; the API key never leaves the gateway."""
    base = base_url.rstrip("/")
    headers = _headers(session_cookie)
    if get is None:
        import requests
        get = requests.get
    response = get(
        f"{base}/api/agent/robin/config",
        headers=headers,
        timeout=10,
    )
    if not response.ok:
        raise GatewayError(f"无法读取 Robin 模型设置（HTTP {response.status_code}）。")
    data = response.json()
    return data if data.get("configured") else None


def complete_with_gateway(
    session_cookie: str,
    system_prompt: str,
    messages: list[dict],
    *,
    base_url: str,
    post=None,
) -> str:
    """Delegate an already-prepared Robin prompt to pi-ai without exposing API keys."""
    base = base_url.rstrip("/")
    headers = _headers(session_cookie)
    if post is None:
        import requests
        post = requests.post
    response = post(
        f"{base}/api/agent/robin/complete",
        json={"system_prompt": system_prompt, "messages": messages},
        headers=headers,
        timeout=180,
    )
    if not response.ok:
        try:
            message = response.json().get("error")
        except Exception:
            message = None
        raise GatewayError(message or f"Robin 模型调用失败（HTTP {response.status_code}）。")
    text = response.json().get("text")
    if not isinstance(text, str):
        raise GatewayError("Robin 模型网关返回了无效响应。")
    return text


def configured_gateway_url() -> str | None:
    value = os.getenv("ROBIN_GATEWAY_URL", "").strip()
    return value.rstrip("/") or None
