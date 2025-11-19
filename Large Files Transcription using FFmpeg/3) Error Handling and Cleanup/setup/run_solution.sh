#!/bin/bash

cd /usercode/FILESYSTEM

source /bootstrap-apps/.virtualenvs/playwright/bin/activate

python transcriber.py
