from tools.sk import Corpus
import configuration

with Corpus(configuration.CORPUS_FILE) as corpus:
    with open('preload_corpus.txt.csv') as fp:
        for line in fp:
            word, lang = line.rstrip().split('\t')
            if lang == 'SK':
                print(word)
                print(corpus.get_frequency(word))
