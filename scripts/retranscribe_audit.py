# -*- coding: utf-8 -*-
import glob
import os
import subprocess
import re

whisper_exe = r"c:\Users\noid\Documents\antigravity\kind-fermi\tools\whisper.cpp\Release\whisper-cli.exe"
model_bin = r"c:\Users\noid\Documents\antigravity\kind-fermi\tools\whisper.cpp\models\ggml-base.en.bin"
audio_dir = r"duo_francais\Duo3.0 original\DUO audio"

# Let's inspect how many sentences whisper produces WITH timestamps for all 45 sections!
# And compare with what was in Duo3.0 original/transcripts/
