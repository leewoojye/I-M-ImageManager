import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')

import sys
sys.path.insert(0, '../')
import soykeyword

class Corpus:
    def __init__(self, fname):
        self.fname = fname
        self.length = 0
    def __iter__(self):
        with open(self.fname, encoding='utf-8') as f:
            for doc in f:
                yield doc.strip()
    def __len__(self):
        if self.length == 0:
            with open(self.fname, encoding='utf-8') as f:
                for n_doc, _ in enumerate(f):
                    continue
                self.length = (n_doc + 1)
        return self.length

from soykeyword.proportion import CorpusbasedKeywordExtractor

def bridgefunction():
    tokenized_corpus_fname='./tokenized/doc2.txt'
    
    #for i, doc in enumerate(Corpus(tokenized_corpus_fname)):
    #    if i <= 5: continue
    #    if i > 11: break
    
    corpusbased_extractor = CorpusbasedKeywordExtractor(
    min_tf=0,
    min_df=0,
    tokenize=lambda x:x.strip().split(),
    verbose=True
    )
    
    corpusbased_extractor.train(Corpus(tokenized_corpus_fname)) #soykeyword: proportion 방식으로 학습 수행.
    
    keywords = corpusbased_extractor.extract_from_word(
    'Ethernet',
    min_score=0.8,
    min_frequency=3
    )
    return keywords[:20]