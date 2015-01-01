import nltk
import json
from nltk import word_tokenize
from urllib import request
from nltk.corpus import wordnet as wn

#Basic text processing: loading the book, breaking it into words.
url = "http://www.gutenberg.org/files/45839/45839.txt"
response = request.urlopen(url)
raw = response.read().decode('utf8')
raw = raw[6671:858399]
sents = nltk.sent_tokenize(raw)

characters = ['Dracula', 'Count', 'Helsing', 'Mina', 'Lucy',
              'Jonathan', 'John', 'Arthur', 'Quincey']

#Tagging all words in Dracula w/ their parts of speech
tagged_sents = []
for s in sents:
    s = nltk.word_tokenize(s)
    tagged_sents.append(nltk.pos_tag(s))

#Create adj. dicts for each character
drac_dict = {}
has_char = False
for c in characters:
    drac_dict[c] = []
    for ts in tagged_sents:
        for w in ts:
            if w[0] == c:
                has_char = True
        for w in ts:
            if has_char == True:
                if w[1] == 'JJ':
                    drac_dict[c].append(w[0])
        has_char = False

#Count and Dracula are the same person!
drac_adjs = drac_dict['Dracula'] + drac_dict['Count']

#Find most common adjs for each character
dracula_fd = nltk.FreqDist(drac_adjs)
mina_fd = nltk.FreqDist(drac_dict['Mina'])
helsing_fd = nltk.FreqDist(drac_dict['Helsing'])
lucy_fd = nltk.FreqDist(drac_dict['Lucy'])
jonathan_fd = nltk.FreqDist(drac_dict['Jonathan'])
john_fd = nltk.FreqDist(drac_dict['John'])
arthur_fd = nltk.FreqDist(drac_dict['Arthur'])
quincey_fd = nltk.FreqDist(drac_dict['Quincey'])

#Accumulate lists of synonyms of most common adjective
drac_syns = wn.synsets(dracula_fd.most_common(3)[2][0])
drac_synos = []
for s in drac_syns:
    drac_synos += s.lemma_names()
drac_synos = set(drac_synos)

mina_syns = wn.synsets(mina_fd.most_common(1)[0][0])
mina_syns = mina_syns[2:6]
mina_synos = []
for s in mina_syns:
    mina_synos += s.lemma_names()
mina_synos = set(mina_synos)

hels_syns = wn.synsets('last')
hels_syns = hels_syns[12:19]
hels_synos = []
for s in hels_syns:
    hels_synos += s.lemma_names()
hels_synos = set(hels_synos)

lucy_syns = wn.synsets(lucy_fd.most_common(1)[0][0])
lucy_syns = lucy_syns[1:2] + lucy_syns[5:7]
lucy_synos = []
for s in lucy_syns:
    lucy_synos += s.lemma_names()
lucy_synos = set(lucy_synos)

jon_syns = wn.synsets(jonathan_fd.most_common(3)[2][0])
jon_syns = jon_syns[7:25]
jon_synos = []
for s in jon_syns:
    jon_synos += s.lemma_names()
jon_synos = set(jon_synos)

john_syns = wn.synsets(john_fd.most_common(2)[1][0])
john_syns = john_syns[-4:]
john_synos = []
for s in john_syns:
    john_synos += s.lemma_names()
john_synos = set(john_synos)

art_syns = wn.synsets(arthur_fd.most_common(1)[0][0])
art_syns = art_syns[3:]
art_synos = []
for s in art_syns:
    art_synos += s.lemma_names()
art_synos = set(art_synos)

quin_syns = wn.synsets(quincey_fd.most_common(2)[1][0])
quin_syns = quin_syns[1:]
quin_synos = []
for s in quin_syns:
    quin_synos += s.lemma_names()
quin_synos = set(quin_synos)

drac_dict2 = {'name': 'characters', 'children': []}
new_char_list = ['Count Dracula', 'Mina Harker', 'Abraham Van Helsing',
                 'Lucy Westenra', 'Jonathan Harker', 'John Seward',
                 'Arthur Holmwood', 'Quincey Morris']
all_synos = [drac_synos, mina_synos, hels_synos, lucy_synos, jon_synos,
             john_synos, art_synos, quin_synos]
for i in range(len(new_char_list)):
    drac_dict1 = {'name': new_char_list[i], 'children': []}
    for a in all_synos[i]:
        drac_dict1['children'].append({'name': a, 'value': 0})
    drac_dict2['children'].append(drac_dict1)

with open('data.json', 'w') as outfile:
    json.dump(drac_dict2, outfile, sort_keys=True, indent=4, ensure_ascii=False)
