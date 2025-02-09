import os

from syn_text.pipeline.data_handlers import FontLoader
from syn_text.pipeline.data_handlers import ImageGenerator
from syn_text.pipeline.data_handlers import WikiSentenceGenerator


class Pipeline:
    def __init__(self,
                 language: str = "en",
                 num_words: int = 10,
                 num_sentences: int = 10,
                 output_folder: str = "./output_images",
                 apply_augmentation: bool = True,
                 fonts_yaml: str = "./src/syn_text/fonts.yaml"):
        self.language = language
        self.num_words = num_words
        self.num_sentences = num_sentences
        self.output_folder = output_folder
        self.apply_augmentation = apply_augmentation
        self.fonts_yaml = fonts_yaml

    def run(self):
        # Load the fonts from the YAML file
        fonts = FontLoader.load_fonts_from_yaml(self.fonts_yaml)
        
        if not fonts:
            print("No fonts found in the YAML file. Exiting.")
            exit(1)

        # Generate sentences
        wiki_generator = WikiSentenceGenerator(lang=self.language)
        sentences = wiki_generator.generate_sentences(self.num_words, self.num_sentences)
        
        # Create images
        image_generator = ImageGenerator(
            fonts=fonts,
            output_folder=self.output_folder,
            apply_augmentation=self.apply_augmentation
        )

        for i, sentence in enumerate(sentences, 1):
            print(f"{i}. {sentence}")
            image_generator.create_image_with_text(sentence, i)
        
        # Open the file in write mode (or create it if it doesn't exist)
        transcription_path = os.path.join(
            self.output_folder, "transcriptions.txt")
        with open(transcription_path, "w") as file:
            # Loop through each string in the list and write it to the file
            for i, sentence in enumerate(sentences, 1):
                sentence = f"sentence_{i}\t{sentence}\n"
                file.write(sentence)  # Write each string followed by a newline
