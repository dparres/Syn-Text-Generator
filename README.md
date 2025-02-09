# Syn-Text-Generator  
Generate random Wikipedia sentences as images.  

## Installation  

Ensure you have [Poetry](https://python-poetry.org/) installed. Then, install dependencies with:  

```bash
pip install --no-cache-dir poetry==1.8.5
poetry config virtualenvs.create false
poetry install --no-interaction
```
## Usage

Run the pipeline with the following command:
```bash
python main.py <output_folder> \
                --num_words <num> \
                --num_sentences <num> \
                --apply_augmentation \
                --lang <language> -\
                -fonts_yaml <path_to_fonts_yaml>
```

## Example
```bash
python main.py images_output_folder \
                --num_words 12 \
                --num_sentences 10 \
                --apply_augmentation \
                --lang en \
                --fonts_yaml ./src/syn_text/config/fonts.yaml
```

### Parameters:  

- `<output_folder>` – Directory where generated images will be saved.  
- `--num_words <num>` – Number of words per sentence.  
- `--num_sentences <num>` – Number of sentences to generate.  
- `--apply_augmentation` – Apply text augmentation (optional).  
- `--lang <language>` – Language code (e.g., `en` for English).  
- `--fonts_yaml <path>` – Path to a YAML file specifying font configurations.  
