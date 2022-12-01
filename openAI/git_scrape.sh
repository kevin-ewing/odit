#! /bin/sh

OUTPUT="/Users/kewing/Desktop/odit/openAI/test2.json"
PROMPT="Summarize, in a few sentences, what has changed in the git diff\n\n"
# COUNT=$(git rev-list --all --count)

git_repo=(
'https://github.com/babashka/babashka.git'
'https://github.com/open-sdr/openwifi.git'
'https://github.com/kubernetes-sigs/cluster-api.git'
'https://github.com/travist/jsencrypt.git'
'https://github.com/Textualize/textual.git'
'https://github.com/vercel/turbo.git'
'https://github.com/heartcombo/devise.git'
'https://github.com/dotnet/csharplang.git'
'https://github.com/ryanoasis/nerd-fonts.git'
'https://github.com/darold/pgbadger.git'
'https://github.com/citusdata/citus.git'
'https://github.com/cilium/tetragon.git'
'https://github.com/hathach/tinyusb.git'
'https://github.com/commaai/openpilot.git'
'https://github.com/facebookresearch/esm.git'
'https://github.com/geohot/tinygrad.git'
'https://github.com/public-apis/public-apis.git'
'https://github.com/pre-commit/pre-commit.git'
'https://github.com/PyCQA/isort.git'
'https://github.com/logseq/logseq.git'
'https://github.com/pangloss/pattern.git'
'https://github.com/lax1dude/eaglercraft.git'
'https://github.com/line/armeria.git'
'https://github.com/Netflix/zuul.git'
'https://github.com/jamealg/KT-companion.git'
'https://github.com/poteto/hiring-without-whiteboards.git'
'https://github.com/PipedreamHQ/pipedream.git'
'https://github.com/moment/moment.git'
'https://github.com/hapijs/joi.git'
'https://github.com/Shopify/liquid.git'
'https://github.com/varvet/pundit.git'
'https://github.com/koalaman/shellcheck.git'
'https://github.com/purescript/purescript.git'
'https://github.com/SagerNet/sing-box.git'
'https://github.com/kubernetes/client-go.git'
'https://github.com/gofiber/fiber.git')


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

            if ((${#COMMIT_DIFF} > 5 && ${#COMMIT_DIFF} < 2048))
            then
                echo {\"prompt\": \"$TMP_PROMPT \", \"completion\": \"$COMMIT_MESSAGE\"} >> "$OUTPUT"
            fi
            

        done

        cd ..
        rm -rf $REPO_NAME
    done
}


loop_clone



