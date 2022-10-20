# odit
Open Dialogue for Git (CS 701 Senior Seminar Project)

## Setup

### Prerequisites
Python 3.8
OpenAI GPT-3 access and api key.

### Virtual Environment for openAI testing
```{bash}
cd openAI
python3.8 -m venv venv
source venv/bin/activate
pip3 install -r openAI_requirements.txt
export OPENAI_API_KEY=''
```

Also export 

### Virtual Environment for dialogue testing
```{bash}
cd dialogue
python3.8 -m venv venv
source venv/bin/activate
pip3 install -r dialogue_requirements.txt
```