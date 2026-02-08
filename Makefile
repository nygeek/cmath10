# Complex Digital Math library

#
# SPDX-License-Identifier: MIT
# Copyright (C) 2025 Marc Donner
#

.PHONY: help

help:
	cat Makefile
	@ echo "OS: " ${OS}
	@ echo "HOME:" ${HOME}
	@ echo "DATE: " ${DATE}
	@ echo "ENSCRIPT:" ${ENSCRIPT}
	@ echo "PS2PDF:" ${PS2PDF}
	@ echo "BASH:" ${BASH}
	@ echo "PYTHON:" ${PYTHON}
	@ echo "run source bin/activate"

# Make us OS-independent ... at least for MacOS and Linux
OS := $(shell uname -s)
ifeq (Linux, ${OS})
    DATE := $(shell date --iso-8601)
else
    DATE := $(shell date "+%Y-%m-%d")
endif

DIRS := "."
BASH := $(shell which bash)
ENSCRIPT := $(shell which enscript)
GAWK := $(shell which gawk)
PS2PDF := $(shell which ps2pdf)
PYTHON := $(shell which python3)
HOME := $(shell echo ${HOME})
PWD := $(shell pwd)

PYTHON_CODE = \
	cmath10.py \
	csmoke.py \
	math10.py \
	ssmoke.py \
	test_math10.py \
	test_cmath10.py

FILES = \
	${PYTHON_CODE} \
	LICENSE \
	Makefile \
	mathdata/README.md \
	mathdata/cmath_testcases.txt \
	.gitattributes \
	.github/workflows/pylint.yml \
	.gitignore \
	pylintrc \
	pyproject.toml \
	pyvenv.cfg \
	README.md

.PHONY: lint pylint
lint:
	pylint math10.py
	pylint cmath10.py
	pylint ssmoke.py
	pylint csmoke.py
	pylint test_math10.py
	pylint test_cmath10.py

pylint: lint

.PHONY: test
test:
	${PYTHON} csmoke.py

%.ps: %.py
	${ENSCRIPT} -G $< -o $@

%.ps: %.awk
	${ENSCRIPT} -G $< -o $@

%.pdf: %.ps
	${PS2PDF} $< $@
	rm $<

Makefile.ps: Makefile
	${ENSCRIPT} -G $< -o $@

listings: \
	Makefile.pdf \
	cmath10.pdf \
	math10.pdf 


.PHONY: clean

clean:
	- rm *.pdf

# GIT operations

diff: .gitattributes
	git diff

.PHONY: status
status:
	git status

# this brings the remote copy into sync with the local one
commit: .gitattributes
	git add ${FILES}
	git commit
	git push -u origin main

# This brings the local copy into sync with the remote (main)
pull: .gitattributes
	git pull origin main

log: .gitattributes
	git log --pretty=oneline
