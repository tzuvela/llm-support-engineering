import llm_client
import tools


def run_tool_loop(messages, log_file):
    response = llm_client.chat_completion(messages, tools.TOOLS)
    if response is None:
        return None

    while True:
        message = response["choices"][0]["message"]
        tool_calls = message["tool_calls"]

        if not tool_calls:
            return response

        messages.append({
            "role": "assistant",
            "tool_calls": tool_calls,
        })

        for tool_call in tool_calls:
            results = tools.execute_tool(tool_call, log_file)

            messages.append(
                tools.build_tool_result_message(tool_call, results)
            )

        response = llm_client.chat_completion(messages)
        if response is None:
            return None
