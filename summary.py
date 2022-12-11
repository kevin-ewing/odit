import os
import openai
import pygit2

SHORT_OPEN_AI_PROMPT = "Describe in detail, in a few sentences, what has changed: \n\n"
LONG_OPEN_AI_PROMPT = "Describe what has changed in the git diff\n\n"
CHARACTER_CUTOFF = 1200

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
  diff_out = os.popen('git diff --stat')
  diff_summary = diff_out.read()
  if len(diff_summary) == 0:
    head_out = os.popen('git diff --stat HEAD')
    diff_summary = head_out.read()
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
    # repo  = get_git_repo()
    # diff = repo.diff()
    # return diff.patch
    diff_out = os.popen('git diff')
    dif_response = diff_out.read()
    if len(dif_response) == 0:
      head_out = os.popen('git diff HEAD')
      return head_out.read()
    else:
      return dif_response


def summarize():
    diff = get_diff()
    if len(diff) == 0:
      return "Nothing to summarize, working tree clean"
    elif (len(diff) < CHARACTER_CUTOFF):
      response = short_open_ai_call(diff)
    else:
      response = long_open_ai_call()
    return response.choices[0].text[1: ]