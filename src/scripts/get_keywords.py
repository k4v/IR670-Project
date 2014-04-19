from topia.termextract import extract
from nltk.corpus import stopwords
import pickle
import re
from types import *
from experience_item import ExperienceItem

def get_keywords(input_text):

    input_text = input_text.lower()
    stop_words = stopwords.words('english')
    remove = '|'.join(stop_words)
    regex = re.compile(r'\b('+remove+r')\b', flags=re.IGNORECASE)
    input_text = regex.sub("", input_text)

    keyword_set = set()

    extractor = extract.TermExtractor()
    for x in sorted(extractor(input_text)):
        words = re.sub('[^0-9a-zA-Z@#]+', ' ', x[0]).split()
        for word in words:
            keyword_set.add(word)
    return keyword_set


if __name__ == '__main__':
    experience_corpus = ""
    company_info = pickle.load( open( "data/company_dump.pickle", "rb" ) )
    for profile in company_info:
        experience_object_list = company_info[profile]['experience']
        for item in experience_object_list:
            print item.company
            if 'nvidia' in item.company.lower():
                if type(item.desc) == NoneType:
                    continue
                else:
                    experience_corpus += item.desc.encode('ascii', 'ignore')

    exp_keywords = get_keywords(experience_corpus)
    my_exp = "- Developed the software framework for the PSU card on an L2/L3 Switch. Also did basic L3 testing on the said card.Added enhancements for an STM-1 encryptor.- Developed the entire software framework ranging from device drivers to the top layer user interface for an Optical Fiber Amplifier (OFA) card used in DWDM networks.- Developed the software framework for V.35 interface in a DSL card."
    my_exp_keywords = get_keywords(my_exp)
    print len(my_exp_keywords)
    print exp_keywords
    print len(set.intersection(exp_keywords, my_exp_keywords))