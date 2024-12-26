from openai import OpenAI
import json

client = OpenAI()

assistant = client.beta.assistants.create(
    name="Math Tutor",
    instructions="你是個擅長使用諷刺手法寫作的作家，你將會以你的手法改寫內容.",
    tools=[],
    model="gpt-4o-mini",
)

thread = client.beta.threads.create()

with open("corpus.txt", "r", encoding="UTF-8") as file:
    corpus = file.read()

message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content=f"I need to rewrite the corpus. {corpus} Can you help me?"
)

run = client.beta.threads.runs.create_and_poll(
    thread_id=thread.id,
    assistant_id=assistant.id,
    tools=[],
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "edit_suggestions",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {
                    "revisions": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "origin": {"type": "string"},
                                "revised": {"type": "string"}
                            },
                            "required": ["origin", "revised"],
                            "additionalProperties": False
                        }
                    }
                },
                "required": ["revisions"],
                "additionalProperties": False
            }
        }
    }
)

while True:
    if run.status == 'completed':
        messages = client.beta.threads.messages.list(
            thread_id=thread.id
        )
        print(json.loads(messages.data[0].content[0].text.value))
        break
    else:
        print(run.status)

