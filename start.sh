#!/bin/bash
source $(conda info --base)/etc/profile.d/conda.sh
conda activate myenv
python 1.py
read -p "Press any key to continue..."