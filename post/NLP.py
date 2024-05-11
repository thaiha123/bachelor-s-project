import gensim
import gensim.downloader
import spacy
import pypdf as pdf
from wordcloud import WordCloud
from gensim.similarities import SparseTermSimilarityMatrix, WordEmbeddingSimilarityIndex

preprocess_model = gensim.utils.simple_preprocess
stopwords = gensim.parsing.preprocessing.STOPWORDS
phrase_model = gensim.models.phrases.Phrases
phrasher_model = gensim.models.phrases.Phraser
dictionary_model = gensim.corpora.Dictionary
api = gensim.downloader
nlp = spacy.load("en_core_web_sm")

def process_pdf(file):
    pdf_content = pdf.PdfReader(file)
    doc = ''
    for i in range(pdf_content._get_num_pages() - 1):
        doc += pdf_content._get_page(i).extract_text()
    return doc

def preprocess(file):
    pdf_content = pdf.PdfReader(file)
    allowed_postags = ["NOUN", "ADJ", "ADV"]
    pages = []
    for i in range(pdf_content._get_num_pages() - 1):
        pages.append(pdf_content._get_page(i).extract_text())
    nlp = spacy.load("en_core_web_sm")
    texts = [nlp(page) for page in pages]
    words = []
    for text in texts:
        words.append([word.lemma_ for word in text if word.pos_ in allowed_postags])
    new_texts = [" ".join(word) for word in words]
    token_list = [preprocess_model(new_text, min_len=3, deacc=True) for new_text in new_texts]
    processed_texts =[]
    for tokens in token_list:
        processed_texts.append([token for token in tokens if token not in stopwords])
    bigram_phrases = phrase_model(processed_texts)
    trigram_phrases = phrase_model(bigram_phrases[processed_texts])
    bigram = phrasher_model(bigram_phrases)
    trigram = phrasher_model(trigram_phrases)
    docs_bigram = [bigram[processed_text] for processed_text in processed_texts]
    docs_trigram = [trigram[doc_bigram] for doc_bigram in docs_bigram]
    return docs_trigram

def tfidf_corpus(texts, dic):
    corpus = [dic.doc2bow(text) for text in texts]
    tfidf_model = gensim.models.TfidfModel(corpus, id2word=dic)
    for i in range(0, len(corpus)):
        bow = corpus[i]
        tfidf_ids = [id for id, value in tfidf_model[bow]]
        bow_ids = [id for id, value in bow]
        low_value_words = [id for id, value in tfidf_model[bow] if value < 0.03]
        missing_words = [id for id in bow_ids if id not in tfidf_ids]
        corpus[i] = [b for b in bow if b[0] not in low_value_words and b[0] not in missing_words]
    return corpus

def create_dictionary(texts):
    dictionary = dictionary_model(texts)
    return dictionary

def topic_ide(texts, dic):
    corpus = tfidf_corpus(texts, dic)
    lda = gensim.models.LdaModel(corpus=corpus, id2word=dic, num_topics=5)
    tags = []
    for idx, topic in lda.print_topics(-1, num_words=30):
        topic = [word.split('*')[1].replace('"', '').strip() for word in topic.split('+')]
        wordcloud = WordCloud(width=200, height=100, max_words=20, background_color="white").generate_from_frequencies({w: 1 for w in topic})
        word_counts = {word: count for word, count in wordcloud.words_.items() if word in topic}
        topic_name = " ".join(sorted(word_counts, key=lambda w: word_counts[w], reverse=True)[:3])
        for tag in topic_name.split(' '):
            if tag not in tags:
                tags.append(tag)
    return tags

def cosin_sim_ide(text1, text2):
    preprocessed_text = []
    preprocessed_text.append(sum(text1, []))
    preprocessed_text.append(sum(text2, []))
    dictionary = dictionary_model(preprocessed_text)
    corpus1 = dictionary.doc2bow(preprocessed_text[0])
    corpus2 = dictionary.doc2bow(preprocessed_text[1])
    word2vect = api.load("glove-wiki-gigaword-50")
    similarity_index = WordEmbeddingSimilarityIndex(word2vect)
    similarity_matrix = SparseTermSimilarityMatrix(similarity_index, dictionary)
    similarity = similarity_matrix.inner_product(corpus1, corpus2, normalized=(True, True))
    return similarity