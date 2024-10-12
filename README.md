# ChimeraX-SessionStates

## Introduction

Reveal inner states of ChimeraX.

## Usage

1. Downloads specific version (e.g. v0.2.0) from GitHub:

    ```shell
    wget https://github.com/ShiinaHiiragi/chimerax-states/archive/refs/tags/0.2.0.zip -P ~/Downloads
    unzip ~/Downloads/0.2.0.zip -d ~/Downloads
    chimerax --nogui --exit --cmd "devel install ~/Downloads/chimerax-states-0.2.0 exit true"
    ```

2. If some different version is installed, uninstall it first (the following are NOT shell commands):

    ```
    toolshed uninstall SessionStates
    devel clean ~/Downloads/chimerax-states-0.2.0
    devel install ~/Downloads/chimerax-states-0.2.0
    states ~/Downloads output
    ```
