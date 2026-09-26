import json

def build_prompt(evidence, retrieved_chunks):
    evidence_json = json.dumps(evidence, indent=2)

    knowledge_sections = []

    for chunk in retrieved_chunks:
        knowledge_sections.append(
            f"Source: {chunk['source']}\n"
            f"Section: {chunk['section']}\n"
            f"Content: {chunk['content']}"
        )
    knowledge_text = "\n\n".join(knowledge_sections)

    return f"""
Analyze the log evidence below.

Use only the log evidence and retrieved knowledge provided below.
Treat log evidence as factual evidence about this incident.
Treat retrieved knowledge as background context only; do not present information from it as a fact about this specific incident unless the log evidence supports it.

You have access to a search_log tool that can inspect the original log file.
Use it when additional raw log evidence would help investigate the incident.
Treat results returned by the tool as incident evidence.

Before listing an item as an unknown, consider whether the retrieved knowledge provides relevant background about the underlying concept or mechanism.
When retrieved knowledge provides a general explanation, use it to interpret the incident, but do not treat that explanation as proof that the same mechanism caused this specific incident.

Return valid JSON only.
Do not use Markdown or code fences.
Do not add fields outside the required schema.
Do not invent or alter facts, numbers, line numbers, timestamps, sources, or messages.
Do not treat an observed error, warning, or symptom as its own root cause.
Do not introduce systems, services, components, or technologies that are not named in the log evidence or retrieved knowledge.

Observations must contain only directly supported facts.
Possible root causes are hypotheses, not confirmed facts.
Every possible root cause must reference specific evidence.
Retrieved knowledge may be used only as background context to explain or interpret the log evidence.
Do not put retrieved knowledge itself in the evidence array.
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

RETRIEVED KNOWLEDGE:
{knowledge_text}
"""
