import time

import llm_client
import tools


def update_stats(stats, response):
    usage = response.get("usage", {})

    stats["llm_calls"] += 1
    stats["prompt_tokens"] += usage.get("prompt_tokens", 0)
    stats["completion_tokens"] += usage.get("completion_tokens", 0)
    stats["total_tokens"] += usage.get("total_tokens", 0)


def run_tool_loop(messages, log_file):
    stats = {
        "llm_calls": 0,
        "tool_calls": 0,
        "prompt_tokens": 0,
        "completion_tokens": 0,
        "total_tokens": 0,
    }
    start_time = time.perf_counter()

    response = llm_client.chat_completion(messages, tools.TOOLS)
    if response is None:
        stats["elapsed_seconds"] = time.perf_counter() - start_time
        return None, stats
    update_stats(stats, response)

    while True:
        message = response["choices"][0]["message"]
        tool_calls = message.get("tool_calls", [])

        if not tool_calls:
            stats["elapsed_seconds"] = time.perf_counter() - start_time
            return response, stats

        messages.append({
            "role": "assistant",
            "tool_calls": tool_calls,
        })

        for tool_call in tool_calls:
            stats['tool_calls'] += 1
            results = tools.execute_tool(tool_call, log_file)

            messages.append(
                tools.build_tool_result_message(tool_call, results)
            )

        response = llm_client.chat_completion(messages, tools.TOOLS)
        if response is None:
            stats["elapsed_seconds"] = time.perf_counter() - start_time
            return None, stats
        update_stats(stats, response)
