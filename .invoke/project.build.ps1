#Requires -Version 5.1


# ################################ TASKS #######################################

TASK build python:setuptools:build


# ###################### ENVIRONMENT #######################

TASK env:setup python:venv:setup

TASK env:purge python:venv:purge
