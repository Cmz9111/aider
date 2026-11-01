import unittest

from aider.linter import Linter, find_filenames_and_linenums


class TestDiagnosticFilenames(unittest.TestCase):
    def test_leading_punctuation(self):
        for filename in [".config.py", "-script.py", "normal.py", "/tmp/code.py"]:
            with self.subTest(filename=filename):
                diagnostic = f"{filename}:12: syntax error\n{filename}:14: another error"
                self.assertEqual(
                    find_filenames_and_linenums(diagnostic, [filename]),
                    {filename: {12, 14}},
                )
                result = Linter().errors_to_lint_result(filename, diagnostic)
                self.assertEqual(set(result.lines), {11, 13})

    def test_does_not_match_inside_another_name(self):
        self.assertEqual(
            find_filenames_and_linenums("other.config.py:12: error", [".config.py"]),
            {},
        )

    def test_rejects_suffixes_of_other_filenames(self):
        for prefix in ["other-", "other.", "other+", "directory/"]:
            with self.subTest(prefix=prefix):
                self.assertEqual(
                    find_filenames_and_linenums(prefix + ".config.py:12: error", [".config.py"]),
                    {},
                )

    def test_diagnostic_delimiters(self):
        for prefix in ["", " ", "\t", "\n", "'", '"', "(", "["]:
            with self.subTest(prefix=prefix):
                self.assertEqual(
                    find_filenames_and_linenums(prefix + ".config.py:12: error", [".config.py"]),
                    {".config.py": {12}},
                )
