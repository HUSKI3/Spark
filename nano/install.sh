# Bash
loc="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
bin=$1

cp $loc/bin/* $bin