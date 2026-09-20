import json

from analyzer import analyze_log, build_evidence
from llm_client import ask_llm

def build_prompt(evidence):
    evidence_json = json.dumps(evidence, indent=2)

    return f"""
Analyze the log evidence below.

Use only the evidence provided.

Return valid JSON only.
Do not use Markdown or code fences.
Do not add fields outside the required schema.
Do not invent or alter facts, numbers, line numbers, timestamps, sources, or messages.
Do not treat an observed error, warning, or symptom as its own root cause.
Do not introduce systems, services, components, or technologies that are not named in the evidence.

Observations must contain only directly supported facts.
Possible root causes are hypotheses, not confirmed facts.
Every possible root cause must reference specific evidence.
Confidence must be one of: low, medium, high.
Unknowns must contain only information that cannot be determined from the evidence.
Recommended checks must be specific checks an engineer could perform to investigate the hypotheses.

Return exactly this JSON structure:

{{
  "observations": [
    "observation"
  ],
  "possible_root_causes": [
    {{
      "cause": "possible cause",
      "confidence": "low",
      "evidence": [
        "specific evidence"
      ],
      "reasoning": "why this hypothesis follows from the evidence"
    }}
  ],
  "unknowns": [
    "unknown"
  ],
  "recommended_checks": [
    "check"
  ]
}}

Evidence:
{evidence_json}
"""


def validate_result(result):
    if not isinstance(result, dict):
        return False

    required_fields = {
        "observations",
        "possible_root_causes",
        "unknowns",
        "recommended_checks",
    }

    if set(result.keys()) != required_fields:
        return False

    if not isinstance(result["observations"], list):
        return False

    if not isinstance(result["possible_root_causes"], list):
        return False

    if not isinstance(result["unknowns"], list):
        return False

    if not isinstance(result["recommended_checks"], list):
        return False

    for cause in result["possible_root_causes"]:
        required_cause_fields = {
            "cause",
            "confidence",
            "evidence",
            "reasoning",
        }

        if set(cause.keys()) != required_cause_fields:
            return False

        if cause["confidence"] not in ["low", "medium", "high"]:
            return False

        if not isinstance(cause["evidence"], list):
            return False

        if not isinstance(cause["cause"], str):
            return False

        if not isinstance(cause["evidence"], list):
            return False

        if not isinstance(cause["reasoning"], str):
            return False

    return True

def print_result(result):
    print("\nObservations")
    print("-------------")
    for observation in result["observations"]:
        print(f"- {observation}")

    print("\nPossible Root Causes")
    print("-------------")
    for cause in result["possible_root_causes"]:
        print(f"- {cause['cause']}")
        print(f"  Confidence: {cause['confidence']}")
        print("  Evidence:")
        for evidence in cause['evidence']:
            print(f"    - {evidence}")
        print(f"  Reasoning: {cause['reasoning']}")

    print("\nUnknowns")
    print("-------------")
    for unknown in result["unknowns"]:
        print(f"- {unknown}")

    print("\nRecommended Checks")
    print("-------------")
    for check in result["recommended_checks"]:
        print(f"- {check}")


def main():
    log_file = "logs/Hadoop_2k.log"

    analysis = analyze_log(log_file)
    evidence = build_evidence(analysis)

    prompt = build_prompt(evidence)

    data, MODEL = ask_llm(prompt)

    if data is not None:
        for item in data["output"]:
            if item.get("type") == "message":
                result = json.loads(item["content"])

                if validate_result(result):
                    print_result(result)
                    print("-------------")
                    print(f"Performance stats {MODEL}: {data.get('stats')}")
                else:
                    print("LLM response failed validation")
                break

if __name__ == "__main__":
    main()