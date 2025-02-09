import random
import re

import wikipedia
import wikipediaapi


class WikiSentenceGenerator:
    def __init__(self, lang="en"):
        self.lang = lang
        self.wiki = wikipediaapi.Wikipedia(language=lang)

    def get_random_wikipedia_page(self):
        """Fetches a random Wikipedia page title and returns its content."""
        try:
            random_title = wikipedia.random()  # Get a random page title
            page = self.wiki.page(random_title)
            return page.text if page.exists() else None
        except Exception as e:
            print(f"Error fetching Wikipedia page: {e}")
            return None

    @staticmethod
    def clean_text(text):
        """Removes section headers, references, and unwanted lines."""
        lines = text.split("\n")
        clean_lines = []
        for line in lines:
            line = line.strip()
            if line.startswith("==") and line.endswith("=="):  # Remove section headers
                continue
            if "Retrieved" in line or "References" in line or "External links" in line:
                continue  # Remove reference lines
            if re.search(r'https?://\S+', line):  # Remove URLs
                continue
            clean_lines.append(line)
        return " ".join(clean_lines)

    def extract_sentences(self, text, num_words, num_sentences):
        """Extracts sentences within the word limit from the cleaned text."""
        text = self.clean_text(text)  # Clean text before processing
        sentences = re.split(r'(?<=[.!?])\s+', text)  # Split text into sentences
        valid_sentences = [s for s in sentences if len(s.split()) <= num_words and len(s.split()) > 3]  # Filter by word limit
        return random.sample(valid_sentences, min(num_sentences, len(valid_sentences)))

    def generate_sentences(self, num_words, num_sentences):
        """Generates a given number of random Wikipedia sentences."""
        collected_sentences = []
        while len(collected_sentences) < num_sentences:
            text = None
            while not text:
                text = self.get_random_wikipedia_page()
            
            sentences = self.extract_sentences(text, num_words, num_sentences - len(collected_sentences))
            collected_sentences.extend(sentences)
        
        return collected_sentences
