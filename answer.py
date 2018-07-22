import pickle
import json
import tflearn
import tensorflow as tf
import numpy as np
import re
import random

import nltk
from nltk.stem.snowball import ItalianStemmer

stemmer = ItalianStemmer()

data = pickle.load( open( "training_data", "rb" ) )
words = data['words']
classes = data['classes']
train_x = data['train_x']
train_y = data['train_y']

# import our chat-bot intents file
with open('intents.json') as json_data:
    intents = json.load(json_data)

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(re.sub(r'[^\w\s]', ' ', sentence), language='italian')
    sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence
def bow(sentence, words, show_details=False):
    sentence_words = clean_up_sentence(sentence)
    bag = [0]*len(words)  
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)

    return np.array(bag)


ERROR_THRESHOLD=0.25
def classify(sentence, show_details=False):
    results = model.predict([bow(sentence, words, show_details)])[0]
    results = [[i,r] for i,r in enumerate(results) if r>ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append((classes[r[0]], r[1]))

    if show_details: print(return_list)
    return return_list


def response(sentence, show_details=False):
    results = classify(sentence, show_details=show_details)
    if results:
        for i in intents['intents']:
            if i['intent'] == results[0][0]:
                return random.choice(i['responses'])

def test():
    sentences = [
        "buongiorno",
        "Ciao", 
        "Come va?",
        "vorrei acquistare un'auto.", 
        "vorrei una macchina usata", 
        "oggi siete aperti?", 
        "mi date il numero di telefono?",
        "avrei bisogno di una macchina a noleggio",
        "avete qualche offerta sull'usato?"
    ]

    for s in sentences:
        print(s)
        print(response(s, show_details=True))

# load our saved model
tf.reset_default_graph()
net = tflearn.input_data(shape=[None, len(train_x[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(train_y[0]), activation='softmax')
net = tflearn.regression(net)

# Define model and setup tensorboard
model = tflearn.DNN(net, tensorboard_dir='tflearn_logs')
model.load('./model.tflearn')

test()