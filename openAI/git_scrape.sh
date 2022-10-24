#! /bin/sh

OUTPUT="/Users/kewing/Desktop/odit/openAI/test.json"
PROMPT="Summarize, in a few sentences, what has changed in the git diff\n\n"
# COUNT=$(git rev-list --all --count)

git_repo=('https://github.com/torvalds/linux' 'https://github.com/golang/go/commits/master' 'https://github.com/Bukkit/Bukkit' 'https://github.com/cognitect-labs/aws-api' 'https://github.com/airblade/vim-gitgutter' '')

loop_clone(){
    touch "$OUTPUT"

    for repo in ${git_repo[@]}
    do
        # Get repo name
        name=$(echo "${url##*/}" | cut -f1 -d".")

        # Clone
        git clone $repo $name
        REPO_NAME=$(echo $repo | rev | cut -d'/' -f 1 | rev | cut -d'.' -f 1)
        cd $REPO_NAME
        iter=1
        COMMITS=$(git rev-list --all)
        for n in $COMMITS
        do
            COMMIT_MESSAGE=$(git log -n 1 --pretty=format:%B $n | awk '{$1=$1};1' | tr '\n' ' ' | sed 's/"/\\"/g')
            COMMIT_DIFF=$(git diff $n --minimal | sed 's/\\//g' | sed 's/"/\\"/g')
            TMP_PROMPT="$PRMOPT"
            TMP_PROMPT+=$COMMIT_DIFF

            if ((${#COMMIT_DIFF} > 5 && ${#COMMIT_DIFF} < 20000))
            then
                echo {\"prompt\": \"$TMP_PROMPT \", \"completion\": \"$COMMIT_MESSAGE\"} >> "$OUTPUT"
            fi
            

        done

        cd ..
        rm -rf $REPO_NAME
    done
}


loop_clone



