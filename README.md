# Syn-Text-Generator
Generate random Wikipedia sentences as images.

## Installation
Install dependencies with Poetry:
```bash
pip install --no-cache-dir poetry==1.8.5
poetry config virtualenvs.create false
poetry install --no-interaction
```

## Run Pipeline
```bash
python main.py images_output_folder --num_words 12 --num_sentences 10 --apply_augmentation --lang en --fonts_yaml ./src/syn_text/config/fonts.yaml
```
