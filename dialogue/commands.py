import os
from os import environ
import pygit2
import summary
import pretty_print

def get_git_repo():
    curr_dir = os.getcwd()
    repo = pygit2.Repository(curr_dir)
    return repo 

def get_project_root_dir():
    curr_dir = os.getcwd()
    repo = pygit2.discover_repository(curr_dir)
    return repo[:-5]

def add(text):
    files = text.split()[1:]
    repo = get_git_repo()

    if "." in files:
        repo.index.add_all()
        repo.index.write()
        return "Added all files to to be committed.\n"
    else:
        for temp_file in files:
            repo.index.add(temp_file)
            repo.index.write()

        if len(files) < 3:
            return "Added " + " and ".join(files) + " to to be committed.\n"
        else:
            return "Added " + ", ".join(files[:-1]) + ", and " + files[-1] + " to be committed.\n"

def summarize():
    if environ.get('OPENAI_API_KEY') is not None:
        return pretty_print.pprint(summary.summarize())
    else:
        return "Make sure you have exported your OpenAI API key \n    For example:\n    $ export OPENAI_API_KEY='**********************************************'"