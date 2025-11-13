# program for applying the stemming operation using NLTK 

# Program for applying the stemming operation using NLTK

import nltk
from nltk.stem import PorterStemmer, SnowballStemmer, LancasterStemmer

# Download required NLTK data (only first time)
nltk.download("punkt")

# Example sentence
sentence = "He was running and playing while enjoying the beautiful scenery."

# Tokenizing (splitting into words)
words = nltk.word_tokenize(sentence)

# Initializing stemmers
porter = PorterStemmer()
snowball = SnowballStemmer("english")
lancaster = LancasterStemmer()

print("Original Words:")
print(words)
print()

print("Porter Stemmer Results:")
for w in words:
    print(w, "→", porter.stem(w))
print()

print("Snowball Stemmer Results:")
for w in words:
    print(w, "→", snowball.stem(w))
print()

print("Lancaster Stemmer Results:")
for w in words:
    print(w, "→", lancaster.stem(w))
print()

# Additional example list
extra_words = ["running", "happiness", "studies", "flying", "boxes", "better"]

print("Extra Words Stemming (Porter):")
for w in extra_words:
    print(w, "→", porter.stem(w))
