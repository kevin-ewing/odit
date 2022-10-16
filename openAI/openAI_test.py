import os
import openai
import json
import git
import re

# Testing the openAI gpt-3 code-davinci-002 code translator
# $ export OPENAI_API_KEY='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'
openai.api_key = os.getenv("OPENAI_API_KEY")

 
# def get_diff_added():
#   repo = git.Repo('.')
#   t = repo.head.commit.tree
#   added_diff = ''
#   removed_diff = ''
#   for line in str.splitlines(repo.git.diff(t)):
#     if re.match('^[a-zA-Z]+', line) is not None:
#       added_diff = added_diff + "\n" + line
  
#   print(added_diff)

def main():
  response = None
  # diff = get_diff_added()

  try:
    response = openai.Completion.create(
      model="code-davinci-002",
      prompt="class Log:\n    def __init__(self, path):\n        dirname = os.path.dirname(path)\n        os.makedirs(dirname, exist_ok=True)\n        f = open(path, \"a+\")\n\n        # Check that the file is newline-terminated\n        size = os.path.getsize(path)\n        if size > 0:\n            f.seek(size - 1)\n            end = f.read(1)\n            if end != \"\\n\":\n                f.write(\"\\n\")\n        self.f = f\n        self.path = path\n\n    def log(self, event):\n        event[\"_event_id\"] = str(uuid.uuid4())\n        json.dump(event, self.f)\n        self.f.write(\"\\n\")\n\n    def state(self):\n        state = {\"complete\": set(), \"last\": None}\n        for line in open(self.path):\n            event = json.loads(line)\n            if event[\"type\"] == \"submit\" and event[\"success\"]:\n                state[\"complete\"].add(event[\"id\"])\n                state[\"last\"] = event\n        return state\n\n\"\"\"\nHere's what the above class is doing:\n1.",
      temperature=0,
      max_tokens=64,
      top_p=1.0,
      frequency_penalty=0.0,
      presence_penalty=0.0,
      stop=["\"\"\""]
    )
  except openai.error.InvalidRequestError as e:
    print(e)

  if response is not None:
    text_response = response.choices[0]["text"]
    print(text_response)

if __name__ == "__main__":
    main()