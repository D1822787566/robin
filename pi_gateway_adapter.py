def prompt_messages_to_gateway(messages) -> tuple[str, list[dict]]:
    """Translate LangChain prompt messages to the text-only pi-ai gateway contract."""
    system_parts = []
    gateway_messages = []
    role_map = {"human": "user", "user": "user", "ai": "assistant", "assistant": "assistant"}

    for message in messages:
        content = getattr(message, "content", "")
        if not isinstance(content, str):
            raise ValueError("Pi AI 网关暂只支持纯文本消息。")
        kind = getattr(message, "type", "")
        if kind == "system":
            system_parts.append(content)
            continue
        role = role_map.get(kind)
        if role:
            gateway_messages.append({"role": role, "content": content})

    return "\n\n".join(system_parts), gateway_messages
