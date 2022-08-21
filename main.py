def import_srt(file):
    file = open(file, "r")
    lines = file.readlines()
    file.close()
    return lines

def clean_subs(text):
    newText = ''
    for line in text:
        line = remove_html_tags(line)
        line = remove_subtitle_timestamps(line)
        line = remove_number_only_lines(line)
        line = remove_newlines(line)
        #line = line.replace(r"(\r\n | \n | \r), ''")
        #line = remove_punctuation_and_quotes(line)
        newText += line
    #print(newText)
    return newText


def remove_html_tags(text):
    #Remove html tags
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def remove_subtitle_timestamps(text):
    #Remove all timestamps
    import re
    clean = re.compile(r"^\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}")
    return re.sub(clean, '', text)

def remove_number_only_lines(text):
    #Remove lines that include only numbers
    import re
    clean = re.compile(r"^\d*$")
    return re.sub(clean, '', text)

def remove_punctuation_and_quotes(text):
    import re
    clean = re.compile(r"[,.?!-\"]")
    return re.sub(clean, '', text)

def remove_newlines(text):
    import re
    clean = re.compile(r"(\n)")
    return re.sub(clean, ' ', text)

def summarize_subtitles(clean_text,subtitles):
    scores = score_sentences(clean_text,subtitles)
    return create_summary(scores)


def score_sentences(clean_text,subtitles):
    import nltk
    #nltk.download('punkt')
    #nltk.download('stopwords')

    sentence_list = nltk.sent_tokenize(subtitles)
    stopwords = nltk.corpus.stopwords.words('english')
    word_frequencies = {}

    for word in nltk.word_tokenize(clean_text):
        if word not in stopwords:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1
    maximum_frequncy = max(word_frequencies.values())

    for word in word_frequencies.keys():
        word_frequencies[word] = (word_frequencies[word] / maximum_frequncy)

    sentence_scores = {}
    for sent in sentence_list:
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_frequencies.keys():
                if len(sent.split(' ')) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word]
                    else:
                        sentence_scores[sent] += word_frequencies[word]
    #print(len(sentence_scores))
    return sentence_scores

def create_summary(sentence_scores):
    import heapq
    summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)

    summary = ' '.join(summary_sentences)
    return summary

if __name__ == '__main__':
    file = r"srt\Elvis.srt"
    subtitles = import_srt(file)
    subtitles = clean_subs(subtitles)
    clean_text = remove_punctuation_and_quotes(subtitles)
    #print(subtitles)
    summary = summarize_subtitles(clean_text,subtitles)
    print(summary)

