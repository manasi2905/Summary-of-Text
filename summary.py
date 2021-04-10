import nltk 
# nltk.download('punkt') inorder to use tokenize
# nltk.download('stopwords') for stopwords present in english
import re                                               #to remove special characters
from heapq import nlargest                              #find largest sentence

def create_summary_file():
    #opening the text file
    filename = "generatedFile.txt"
    txtFile = open(filename, "r")
    fileContent = txtFile.read()                            #reading the contents of file

    #intializations
    maxlen_sentence = 40                                    #sentence can be of max 40 characters
    size_of_summary = 5                                     #no. of sentences in summary 

    #CALCULATING FREQUENCY
    stopwords = nltk.corpus.stopwords.words('english')      #stopwords -> a, the, you etc
    formated_content = re.sub('[^a-zA-Z]', ' ', fileContent)#remove special characters
    formated_words_list = formated_content.lower().split()           #converting to words
    #frequencies of each word
    word_frequencies = {}
    for word in formated_words_list:
        if word not in stopwords:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1                  #if word not already present, add it
            else:
                word_frequencies[word] += 1                 #increment the value of the word freq
    #weighted frequency
    max_freq = max(word_frequencies.values())
    for word in word_frequencies.keys():
        word_frequencies[word] = (word_frequencies[word]/max_freq)

    #CALCULATING SENTENCE SCORE
    sentence_scores = {}
    sentences_list = nltk.sent_tokenize(fileContent)        #converting to sentences
    word_list = fileContent.lower().split()                 #converting to words
    for sentence in sentences_list:
        for word in word_list:
            if word in word_frequencies.keys():
                if len(sentence.split(' ')) < maxlen_sentence:           #limitng the max length of sentence
                    if sentence not in sentence_scores.keys():
                        sentence_scores[sentence] = word_frequencies[word]
                    else:
                        sentence_scores[sentence] += word_frequencies[word]

    #finding 'size_of_summary' number of sentences with largest score
    summary_sentences = nlargest(size_of_summary, sentence_scores, key=sentence_scores.get)

    #printing the contents
    summary = ' '.join(summary_sentences)
    print("\n")
    print (summary)

    #closing the file 
    txtFile.close()

    finalText = open("summary.txt","a")
    finalText.write(summary)
    finalText.close()