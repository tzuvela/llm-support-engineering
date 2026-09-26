import pytest

from tools import execute_tool


def test_execute_tool_search_log(tmp_path):
    log_file = tmp_path / "test.log"

    log_file.write_text(
        "INFO startup complete\n"
        "ERROR IN CONTACTING RM.\n"
        "INFO shutdown complete\n"
    )


    tool_call = {
        "function": {
            "name": "search_log",
            "arguments": '{"query":"ERROR IN CONTACTING RM."}'
        }
    }

    results = execute_tool(tool_call, log_file)

    assert len(results) == 1
    assert results[0]["line_number"] == 2


def test_execute_unknown_tool():
    tool_call = {
        "function": {
            "name": "unknown_tool",
            "arguments": "{}"
        }
    }

    with pytest.raises(ValueError, match="Unknown tool: unknown_tool"):
        execute_tool(tool_call, "logs/Hadoop_2k.log")