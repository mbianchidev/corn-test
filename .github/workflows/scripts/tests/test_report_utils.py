import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS_DIR))

from _report_utils import generate_markdown_report, parse_junit_xml  # noqa: E402


class ParseJUnitXmlTests(unittest.TestCase):
    def test_nested_phpunit_suites_include_failure_details(self) -> None:
        xml = r"""<?xml version="1.0" encoding="UTF-8"?>
<testsuites>
  <testsuite name="phpunit.xml" tests="2" failures="1" errors="0" skipped="0" time="0.02">
    <testsuite name="CornTest Suite" tests="2" failures="1" errors="0" skipped="0" time="0.02">
      <testsuite name="CornTest\Tests\RandomMathOperationsTest" tests="2" failures="1" errors="0" skipped="0" time="0.02">
        <testcase name="randomAddReturnsExpectedRange" classname="CornTest.Tests.RandomMathOperationsTest" time="0.01"/>
        <testcase name="randomDivideReturnsExpectedRange" classname="CornTest.Tests.RandomMathOperationsTest" time="0.01">
          <failure type="PHPUnit\Framework\ExpectationFailedException">Failed asserting that 12 is less than or equal to 10.</failure>
        </testcase>
      </testsuite>
    </testsuite>
  </testsuite>
</testsuites>
"""
        with tempfile.TemporaryDirectory() as tmp_dir:
            report_path = Path(tmp_dir) / "phpunit-results.xml"
            report_path.write_text(xml, encoding="utf-8")
            result = parse_junit_xml(report_path)

        self.assertIsNotNone(result)
        assert result is not None
        self.assertEqual(result.tests, 2)
        self.assertEqual(result.failures, 1)
        self.assertEqual(len(result.test_failures), 1)
        self.assertEqual(
            result.test_failures[0].test_name,
            "randomDivideReturnsExpectedRange",
        )

        markdown = generate_markdown_report("PHP", "PHPUnit", [result])
        self.assertIn("## Failed Tests", markdown)
        self.assertIn("Failed asserting that 12 is less than or equal to 10.", markdown)
        self.assertNotIn("All tests passed", markdown)


if __name__ == "__main__":
    unittest.main()
