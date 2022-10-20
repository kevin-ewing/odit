import os
import openai
import pygit2

OPEN_AI_PROMPT = "Summarize, in a few sentences, what has changed in the git diff\n\n"

# $ export OPENAI_API_KEY='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'
openai.api_key = os.getenv("OPENAI_API_KEY")


def open_ai_call(diff):
  prompt = OPEN_AI_PROMPT + diff
  response = openai.Completion.create(
    model="text-davinci-002",
    prompt=prompt,
    temperature=0.7,
    max_tokens=100,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
  )
  return response


def get_git_repo():
    curr_dir = os.getcwd()
    repo = pygit2.Repository(curr_dir)
    return repo 


def get_diff():
    repo  = get_git_repo()
    diff = repo.diff()
    return diff.patch


if __name__ == "__main__":
    diff = get_diff()
    response = open_ai_call(diff)
    print(response.choices[0].text)