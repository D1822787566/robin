import unittest
from pathlib import Path

from output_language import chinese_output_prompt


class OutputLanguageTests(unittest.TestCase):
    def test_adds_a_hard_simplified_chinese_requirement(self):
        prompt = chinese_output_prompt("Analyze only the supplied sources.")

        self.assertIn("简体中文", prompt)
        self.assertIn("标题、分析、结论和建议", prompt)
        self.assertIn("URL、IOC、站点名和原始来源标题", prompt)

    def test_report_and_followup_calls_use_the_language_requirement(self):
        llm_source = (Path(__file__).resolve().parents[1] / "llm.py").read_text(encoding="utf-8")

        self.assertIn("from output_language import chinese_output_prompt", llm_source)
        self.assertGreaterEqual(
            llm_source.count("system_prompt = chinese_output_prompt(system_prompt)"),
            2,
        )
        self.assertIn("_FOLLOWUP_SYSTEM = chinese_output_prompt", llm_source)


if __name__ == "__main__":
    unittest.main()
