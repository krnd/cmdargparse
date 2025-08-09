#Requires -Version 5.1


# ################################ TASKS #######################################

# ###################### SETUP #############################

TASK setup          python:venv:setup

TASK requirements   python:venv:compile


# ###################### BUILD #############################

TASK build          python:setuptools:build


# ###################### CLEAN #############################

TASK clean          ...

TASK purge!         clean, python:venv:purge
