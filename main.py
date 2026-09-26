import json

import analyzer
import agent
import retriever
import prompt
import result
import llm_client


INDEX_PATH = "knowledge/index.json"
LOG_FILE = "logs/Hadoop_2k.log"


def main():
    analysis = analyzer.analyze_log(LOG_FILE)
    evidence = analyzer.build_evidence(analysis)

    index = retriever.load_index(INDEX_PATH)

    query_parts = []
    for item in evidence["message_evidence"][:3]:
        query_parts.append(item["message"])

    query = "\n".join(query_parts)

    print("\nRetrieval query:")
    print(query)

    retrieved_chunks = retriever.semantic_retrieve(query, index["chunks"])

    print("\nRetrieved knowledge:")
    for chunk in retrieved_chunks:
        print(f"Score: {chunk['score']}")
        print(f"Section: {chunk['section']}")
        # print(f"Content: {chunk['content']}")

    investigation_prompt = prompt.build_prompt(evidence, retrieved_chunks)

    messages = [
        {"role": "user", "content": investigation_prompt}
    ]
    response, stats = agent.run_tool_loop(messages, LOG_FILE)

    if response is None:
        print("LLM investigation failed")
        return

    content = response["choices"][0]["message"]["content"]

    try:
        investigation_result = result.parse_result(content)
    except (TypeError, json.JSONDecodeError):
        print("LLM response was not valid JSON")
        print("Raw response:")
        print(repr(content))
        return

    if result.validate_result(investigation_result):
        result.print_result(investigation_result)
        print('\nAgent stats:')
        print("-------------")
        print(
            f"Model: {llm_client.MODEL} | LLM calls: {stats['llm_calls']} | Tool calls: {stats['tool_calls']} "
            f"| Prompt tokens: {stats['prompt_tokens']} | Completion tokens: {stats['completion_tokens']} "
            f"| Total tokens: {stats['total_tokens']} | Elapsed: {stats['elapsed_seconds']:.2f}s"
        )
    else:
        print("LLM response failed validation")


if __name__ == "__main__":
    main()
