import json


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

def parse_result(content):
    content = content.strip()

    if content.startswith("```json"):
        content = content[7:]

    if content.endswith("```"):
        content = content[:-3]

    content = content.strip()
    return json.loads(content)