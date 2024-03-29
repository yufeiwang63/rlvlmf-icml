## Install
```
conda env create -f conda_env.yml  
pip install git+https://github.com/Farama-Foundation/Metaworld.git@master#egg=metaworld  
```

For clip: pip install ftfy regex tqdm & pip install git+https://github.com/openai/CLIP.git   
For using blip2 you need to install lavis, follow the instructions here: https://github.com/salesforce/LAVIS  
for using openai you need to install openai  
for gemini: pip install -q -U google-generativeai  

## Run experiments with gemini
see scripts/train_command.sh  
see vlms/gemini_infer.py to change the gemini api key
