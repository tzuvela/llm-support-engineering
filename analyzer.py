
def parse_line(line):
    parts = line.split(maxsplit=3)

    date = parts[0]
    time = parts[1]
    level = parts[2]
    remaining = parts[3]

    context_end = remaining.find("]")

    if context_end == -1:
        raise ValueError("Invalid log format")

    context = remaining[:context_end + 1]
    remaining = remaining[context_end + 1:].strip()

    source, message = remaining.split(":", maxsplit=1)

    return{
        "date": date,
        "time": time,
        "level": level,
        "context": context,
        "source": source,
        "message": message.strip(),
    }



def load_log(log_file):
    with open(log_file) as f:
        for number, line in enumerate(f, start=1):
            line = line.strip()

            if not line:
                continue
            record = parse_line(line)
            record["line_number"] = number

            yield record


def analyze_log(log_file):
    count = 0
    level_stats = {}
    serious_records = []

    for record in load_log(log_file):
        count += 1

        level = record["level"]
        if level in level_stats:
            level_stats[level] += 1
        else:
            level_stats[level] = 1

        if level in ["WARN", "ERROR", "FATAL"]:
            serious_records.append(record)

    return {
        "count": count,
        "level_stats": level_stats,
        "serious_records": serious_records
    }


def get_message_stats(records):
    messages = {}

    for record in records:
        message = record["message"]

        if message in messages:
            messages[message] += 1
        else:
            messages[message] = 1
    return messages


def get_source_stats(records):
    sources = {}

    for record in records:
        source = record["source"]

        if source in sources:
            sources[source] += 1
        else:
            sources[source] = 1
    return sources


def build_evidence(analysis):
    message_stats = get_message_stats(analysis["serious_records"])
    top_messages = sorted(message_stats.items(), key=lambda x: x[1], reverse=True)[:5]

    source_stats = get_source_stats(analysis["serious_records"])
    top_sources = sorted(source_stats.items(), key=lambda x: x[1], reverse=True)[:5]
    message_evidence = get_message_evidence(analysis["serious_records"], top_messages,)

    top_sources = [{"source": source, "count": count} for source, count in top_sources]

    return {
        "record_count": analysis["count"],
        "level_stats": analysis["level_stats"],
        "top_sources": top_sources,
        "message_evidence": message_evidence,
    }


def get_message_evidence(records, messages):
    selected = []

    for message, count in messages:
        for record in records:
            if record["message"] == message:
                selected.append({
                    "count": count,
                    "line_number": record["line_number"],
                    "date": record["date"],
                    "time": record["time"],
                    "level": record["level"],
                    "source": record["source"],
                    "context": record["context"],
                    "message": record["message"],
                })
                break
    return selected
