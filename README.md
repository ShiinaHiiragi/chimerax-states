# ChimeraX-SessionStates

## Introduction

Reveal inner states of ChimeraX.

## Installation

1. Downloads specific version (e.g. v0.2) from GitHub:

    ```shell
    wget https://github.com/ShiinaHiiragi/chimerax-states/archive/refs/tags/0.2.zip -P ~/Downloads
    unzip ~/Downloads/0.2.zip -d ~/Downloads
    chimerax --nogui --exit --cmd "devel install ~/Downloads/chimerax-states-0.2 exit true"
    ```

2. If updation is needed, uninstall it first:

    ```
    # NOTE: these are NOT Linux shell commands
    toolshed uninstall SessionStates
    devel clean ~/Downloads/chimerax-states-0.2
    devel install ~/Downloads/chimerax-states-0.2
    states ~/Downloads output
    ```
