import unittest

from pi_gateway import (
    GatewayError,
    complete_with_gateway,
    get_workbench_cookie,
    fetch_robin_config,
)


class _Response:
    def __init__(self, payload, ok=True, status_code=200):
        self._payload = payload
        self.ok = ok
        self.status_code = status_code

    def json(self):
        return self._payload


class PiGatewayTests(unittest.TestCase):
    def test_reads_workbench_cookie_from_streamlit_context(self):
        class Streamlit:
            class context:
                cookies = {"workbench_session": "signed-cookie"}

        self.assertEqual(get_workbench_cookie(Streamlit), "signed-cookie")

    def test_fetches_sanitized_robin_model_status_with_cookie(self):
        called = {}

        def fake_get(url, headers, timeout):
            called.update(url=url, headers=headers, timeout=timeout)
            return _Response({"configured": True, "provider": "deepseek", "model": "deepseek-chat"})

        config = fetch_robin_config(
            "signed-cookie",
            base_url="http://pi-agent:8044",
            get=fake_get,
        )

        self.assertEqual(config["model"], "deepseek-chat")
        self.assertEqual(called["url"], "http://pi-agent:8044/api/agent/robin/config")
        self.assertEqual(called["headers"]["Cookie"], "workbench_session=signed-cookie")

    def test_sends_only_messages_to_gateway_and_returns_text(self):
        called = {}

        def fake_post(url, json, headers, timeout):
            called.update(url=url, json=json, headers=headers, timeout=timeout)
            return _Response({"text": "Gateway answer"})

        text = complete_with_gateway(
            "signed-cookie",
            "Use sources only.",
            [{"role": "user", "content": "Investigate."}],
            base_url="http://pi-agent:8044",
            post=fake_post,
        )

        self.assertEqual(text, "Gateway answer")
        self.assertEqual(called["url"], "http://pi-agent:8044/api/agent/robin/complete")
        self.assertNotIn("api_key", called["json"])
        self.assertEqual(called["headers"]["Cookie"], "workbench_session=signed-cookie")

    def test_requires_workbench_cookie(self):
        with self.assertRaisesRegex(GatewayError, "工作台登录"):
            complete_with_gateway(None, "", [], base_url="http://pi-agent:8044")


if __name__ == "__main__":
    unittest.main()
