text = 

sentences = nltk.sent_tokenize(text.lower())

total_sentence_length = sum(len(sentences) for sentence in sentences)
average_sentence_length = total_sentence_length / len(sentences)

words = nltk.word_tokenize(text.lower())

english_words = set(words)


# Load the Carnegie Mellon University Pronouncing Dictionary
cmu_dict = cmudict.dict()

# Define the syllable_count function
def syllable_count(word):
    if word.lower() in cmu_dict:
        return max([len(list(y for y in x if y[-1].isdigit())) for x in cmu_dict[word.lower()]])
    else:
        # If the word is not found in the dictionary, estimate the syllables based on vowels.
        # This is a simple method and may not be accurate for all words.
        vowels = "aeiouy"
        count = 0
        for char in word:
            if char in vowels:
                count += 1
        return count

def count_hard_and_simple_words(text):

    # Initialize counters
    hard_word_count = 0
    simple_word_count = 0

    # Determine syllable count for each word
    for word in words:
        if word.lower() in english_words:
            # Check if the word is in the set of common English words
            syllables = syllable_count(word)
            if syllables >= 3:
                hard_word_count += 1
            else:
                simple_word_count += 1

    return hard_word_count, simple_word_count


hard, simple = count_hard_and_simple_words(text)


def find_complex_words(text):

    # Initialize a list to store complex words
    complex_words = []

    # Determine syllable count for each word and add to the list if it's complex
    for word in words:
        if word.lower() in english_words:
            # Check if the word is in the set of common English words
            syllables = syllable_count(word)
            if syllables >= 3:
                complex_words.append(word)

    return complex_words


complex_words = find_complex_words(text)
# print('complex_words:', complex_words)

complex_words_len = len(complex_words)

percentage_complex_words = ((complex_words_len / len(words)) * 100)


def Linsear_Write_Formula(text):

    sim_complex = 2 * complex_words
    sim_word = (simple) + len(sim_complex)
    lwf = sim_word / len(sentences)
    # lwf = (simple + 2 × complex_words) / len(sentences)
    return lwf


def FORCAST_Readability_Formula(text):
    ave_sen_com = average_sentence_length + percentage_complex_words
    frf = ave_sen_com * 0.165
    return frf

def Spache_Readability_Formula(text):
    spache_simple = 0.121 * (simple)
    spache_sentence = 0.082 * len(sentences)
    spache_total = spache_simple + spache_sentence
    return spache_total

def RIX(text):
  RIX_Index = (len(long_words) / len(sentences)) + ((len(complex_words) * 100) / len(words))
  return RIX_Index


def LIX(text):
    LIX_Index = (len(words) / len(sentences)) + (len(long_words) * 100) / len(words)
    return LIX_Index


def Gulpease_Index(text):
    Letr_word = ratio/len(words)
    mul_letr_word = 10 * Letr_word

    sen_word = len(sentences)/len(words)
    mul_sen_word = 300 * sen_word

    tot_letr_sen = mul_letr_word + mul_sen_word
    total_letr_sen = 89 - tot_letr_sen

    return total_letr_sen


def fry_readability(text):
    # Fry Readability Graph
    dic = pyphen.Pyphen(lang='en_US')

    num_syllables = len(dic.inserted(text).split("-"))

    Readability =((len(sentences) / len(words)) * 100 + ((num_syllables) / len(words)) * 10.6 - 15.59)*(-1)
    return Readability

def readiability(text):
    FK = textstat.flesch_kincaid_grade(text)
    GF = textstat.gunning_fog(text)
    DC = textstat.dale_chall_readability_score(text)
    SI = textstat.smog_index(text)
    return {'flesch_kincaid_grade':FK,
           'Gunning_fog':GF,
           'Dale Chall':"{:.0f}".format(DC),
           'Smog index':SI}

report = readiability(text)


nlp = spacy.load("en_core_web_sm")

doc = nlp(text)



def relation_list(nouns):

    relation_list = defaultdict(list)

    for k in range (len(nouns)):
        relation = []
        for syn in wordnet.synsets(nouns[k], pos = wordnet.NOUN):
            for l in syn.lemmas():
                relation.append(l.name())
                if l.antonyms():
                    relation.append(l.antonyms()[0].name())
            for l in syn.hyponyms():
                if l.hyponyms():
                    relation.append(l.hyponyms()[0].name().split('.')[0])
            for l in syn.hypernyms():
                if l.hypernyms():
                    relation.append(l.hypernyms()[0].name().split('.')[0])
        relation_list[nouns[k]].append(relation)
    return relation_list


def avg_u_entity_sentence(text):
    doc = nlp(text)
    senlength = len(list(doc.sents))

    unique_entity = sum(len(set(ent.text.lower() for ent in sent.ents)) for sent in doc.sents)

    avg_unique_entity = unique_entity / senlength


    words_per_sentence = [nltk.word_tokenize(sentence.text) for sentence in doc.sents]
    avg_words_per_sentence = sum(len(words) for words in words_per_sentence) / len(words_per_sentence)

    percentage_avg_unique_entity = (avg_unique_entity / avg_words_per_sentence) * 100
    return percentage_avg_unique_entity



def avg_entity_sentence(text):
    doc = nlp(text)
    senlength2 = len(list(doc.sents))
    num_entity_mentions2 = sum(len(sent.ents) for sent in doc.sents)
    avg_entity_mention = num_entity_mentions2 / senlength2
    # Calculate the percentage of average entity mentions per sentence
    words_per_sentence2 = [nltk.word_tokenize(sentence.text) for sentence in doc.sents]
    avg_words_per_sentence2 = sum(len(words) for words in words_per_sentence2) / len(words_per_sentence2)
    percentage_avg_entity_mentions2 = (avg_entity_mention / avg_words_per_sentence2) * 100
    return percentage_avg_entity_mentions2


def Raygor_Readability_Estimate(text):
    simple_words = 0.787 * simple
    hard_words = 0.121 * hard
    rre = (simple_words) + (hard_words)
    return rre


