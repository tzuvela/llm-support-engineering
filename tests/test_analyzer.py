from analyzer import parse_line, load_log, search_log

def test_parse_line_basic():
    line = (
        "2015-10-18 18:01:47,978 INFO [main] "
        "org.apache.hadoop.mapreduce.v2.app.MRAppMaster: "
        "Created MRAppMaster for application appattempt_123"
    )

    result = parse_line(line)

    assert result["date"] == "2015-10-18"
    assert result["time"] == "18:01:47,978"
    assert result["level"] == "INFO"
    assert result["context"] == "[main]"
    assert result["source"] == "org.apache.hadoop.mapreduce.v2.app.MRAppMaster"
    assert result["message"] == "Created MRAppMaster for application appattempt_123"


def test_parse_line_context_with_spaces():
    line = (
        "2015-10-18 18:06:01,840 ERROR "
        "[RMCommunicator Allocator] "
        "org.apache.hadoop.mapreduce.v2.app.rm.RMContainerAllocator: "
        "ERROR IN CONTACTING RM."
    )

    result = parse_line(line)

    assert result["level"] == "ERROR"
    assert result["context"] == "[RMCommunicator Allocator]"
    assert result["source"] == "org.apache.hadoop.mapreduce.v2.app.rm.RMContainerAllocator"
    assert result["message"] == "ERROR IN CONTACTING RM."


def test_load_log_skips_malformed_line(tmp_path):
    log_file = tmp_path / "test.log"

    log_file.write_text(
        "2015-10-18 18:01:47,978 INFO [main] "
        "org.apache.hadoop.mapreduce.v2.app.MRAppMaster: "
        "Started\n"
        "this is a malformed line\n"
        "2015-10-18 18:06:01,840 ERROR "
        "[RMCommunicator Allocator] "
        "org.apache.hadoop.mapreduce.v2.app.rm.RMContainerAllocator: "
        "ERROR IN CONTACTING RM.\n"
    )

    records = list(load_log(log_file))

    assert len(records) == 2
    assert records[0]["line_number"] == 1
    assert records[1]["line_number"] == 3


def test_search_log_find_matching_lines(tmp_path):
    log_file = tmp_path / "test.log"

    log_file.write_text(
        "INFO [main] something happened\n"
        "ERROR IN CONTACTING RM.\n"
        "INFO [main] another event\n"
        "ERROR IN CONTACTING RM.\n"
    )

    matches = search_log(log_file, "ERROR IN CONTACTING RM")

    assert len(matches) == 2
    assert matches[0]["line_number"] == 2
    assert matches[1]["line_number"] == 4
