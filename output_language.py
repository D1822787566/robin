"""Shared language requirements for user-visible Robin model output."""

_SIMPLIFIED_CHINESE_REQUIREMENT = """

输出语言（硬性规则）：
- 所有面向用户的标题、分析、结论和建议必须使用简体中文。
- URL、IOC、站点名和原始来源标题必须保持原样；如需解释，在其后使用中文说明。
- 模板中的英文段落标题必须翻译为中文后再输出。
- 证据不足时，必须用中文明确说明“未发现足够证据”，不得猜测或补全事实。
"""


def chinese_output_prompt(prompt: str) -> str:
    """Append the non-negotiable language and evidence-handling requirements."""
    return prompt.rstrip() + _SIMPLIFIED_CHINESE_REQUIREMENT
