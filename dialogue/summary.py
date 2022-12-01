import os
import openai
import pygit2

SHORT_OPEN_AI_PROMPT = "Summarize, in a few sentences, what has changed in the git diff\n\n"
LONG_OPEN_AI_PROMPT = "Briefly summarize what has changed in the git diff\n\n"

# $ export OPENAI_API_KEY='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'
openai.api_key = os.getenv("OPENAI_API_KEY")


def short_open_ai_call(diff):
  prompt = SHORT_OPEN_AI_PROMPT + diff
  response = openai.Completion.create(
    model="text-davinci-003",
    prompt=prompt,
    temperature=0.7,
    max_tokens=100,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
  )
  return response

def long_open_ai_call():
  p = os.popen('git diff --stat')
  diff_summary = p.read()
  prompt = LONG_OPEN_AI_PROMPT + diff_summary
  response = openai.Completion.create(
    model="text-davinci-003",
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


def summarize():
    diff = get_diff()
    if (len(diff) < 4097):
      response = short_open_ai_call(diff)
    else:
      response = long_open_ai_call()
    return response.choices[0].text[1: ]