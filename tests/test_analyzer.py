from analyzer import parse_line

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


def test_parse_line_real_hadoop_format():
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