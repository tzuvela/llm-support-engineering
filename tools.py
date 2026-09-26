import json

import analyzer


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_log",
            "description": "Search the log file for lines containing a query string.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Text to search for in the log.",
                    },
                },
                "required": ["query"],
            },
        },
    },
]


def execute_tool(tool_call, log_file):
    function_name = tool_call["function"]["name"]

    arguments = json.loads(tool_call["function"]["arguments"])

    if function_name == "search_log":
        query = arguments['query']

        return analyzer.search_log(log_file, query)

    raise ValueError(f"Unknown tool: {function_name}")

if __name__ == "__main__":
    test_call = {
        "function": {
            "name": "search_log",
            "arguments": '{"query":"ERROR IN CONTACTING RM."}'
        }
    }

    results = execute_tool(test_call, "logs/Hadoop_2k.log")

    print("Matches:", len(results))
    print("First match:", results[0])