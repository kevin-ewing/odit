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
    message = text.strip()[3:].strip()
    if not message:
        return "Select files to stage. For assistance type help"
    else:
        p = os.popen('git add ' + str(message))
        response = p.read()
        return response

def help():
    return "These are common odit commands used in various situations:\n\nwork on the current changes\n    add       Add file contents to the commit\n    restore   Restore working tree files\n    rm        Remove files from the working tree and from the index\nexamine the history and state\n    summarize Summary of changes since the last commit\n    log       Show commit logs\ngrow, mark and tweak your common history\n    branch    List, create, or delete branches\n    commit    Record changes to the repository\n    merge     Join two or more development histories together\n    rebase    Reapply commits on top of another base tip\n    reset     Reset current HEAD to the specified state\n    switch    Switch branches\n    tag       Create, list, delete or verify a tag object signed with GPG\ncollaborate\n    fetch     Download objects and refs from another repository\n    pull      Fetch from and integrate with another repository or a local branch\n    push      Update remote refs along with associated objects"


def commit(text):
    message = text.strip()[6:].strip()
    if not message:
        return "Add a commit message, for a overview of your changes type summarize"
    else:
        p = os.popen('git commit -m ' + str(message))
        response = p.read()
        return response


def summarize():
    if environ.get('OPENAI_API_KEY') is not None:
        return pretty_print.pprint(summary.summarize())
    else:
        return "Make sure you have exported your OpenAI API key \n    For example:\n    $ export OPENAI_API_KEY='**********************************************'"


def push():
    return ""

def pull():
    return ""