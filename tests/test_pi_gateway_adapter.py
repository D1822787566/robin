import unittest

from pi_gateway_adapter import prompt_messages_to_gateway


class _Message:
    def __init__(self, kind, content):
        self.type = kind
        self.content = content


class PiGatewayAdapterTests(unittest.TestCase):
    def test_converts_langchain_messages_to_gateway_payload(self):
        system_prompt, messages = prompt_messages_to_gateway([
            _Message("system", "Use sources only."),
            _Message("human", "Investigate example.com."),
            _Message("ai", "Prior finding."),
        ])

        self.assertEqual(system_prompt, "Use sources only.")
        self.assertEqual(messages, [
            {"role": "user", "content": "Investigate example.com."},
            {"role": "assistant", "content": "Prior finding."},
        ])

    def test_rejects_non_text_message_content(self):
        with self.assertRaisesRegex(ValueError, "纯文本"):
            prompt_messages_to_gateway([_Message("human", [{"type": "image"}])])


if __name__ == "__main__":
    unittest.main()
