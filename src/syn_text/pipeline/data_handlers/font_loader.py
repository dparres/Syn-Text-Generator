import yaml


class FontLoader:
    @staticmethod
    def load_fonts_from_yaml(file_path):
        """Loads fonts from a YAML file."""
        with open(file_path, 'r') as file:
            fonts_data = yaml.safe_load(file)
        return fonts_data.get('fonts', [])
