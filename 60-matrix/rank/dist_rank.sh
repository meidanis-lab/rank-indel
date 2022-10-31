#!/usr/bin/bash

PARENTPATH=$(cd $(dirname "${BASH_SOURCE[0]}"); pwd -P)

${PARENTPATH}/dist.py 0 0 $1 $2
