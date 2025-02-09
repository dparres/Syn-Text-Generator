import argparse

from syn_text.pipeline import Pipeline


def main():
    # Setup argument parser for command-line arguments
    parser = argparse.ArgumentParser(description="Generate random Wikipedia sentences as images.")
    parser.add_argument("output_folder", help="The folder where images will be saved.")
    parser.add_argument("--num_words", type=int, default=10, help="Maximum number of words per sentence.")
    parser.add_argument("--num_sentences", type=int, default=5, help="Number of sentences to generate.")
    parser.add_argument("--apply_augmentation", action="store_true", help="Whether to apply random augmentations.")
    parser.add_argument("--lang", type=str, default="en", help="Language of Wikipedia text.")
    parser.add_argument("--fonts_yaml", type=str, help="YAML file that contains the selected fonts.")

    args = parser.parse_args()

    # Initialize Pipeline
    pipeline = Pipeline(language=args.lang,
                        num_words=args.num_words,
                        num_sentences=args.num_sentences,
                        output_folder=args.output_folder,
                        apply_augmentation=args.apply_augmentation,
                        fonts_yaml=args.fonts_yaml)

    # Run Pipeline
    pipeline.run()


if __name__ == "__main__":
    main()
