import spacy
from spacy.lang.en.examples import sentences 

from spacy import displacy
nlp = spacy.load('en_core_web_sm')

from pprint import pprint

def main():
  doc = nlp('John is known for simplicty')
  print(doc.text)
  pprint([(X, X.ent_iob_, X.ent_type_) for X in doc])

if __name__ == '__main__':
  main()
