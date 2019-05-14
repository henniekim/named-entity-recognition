import json
import glob

mode = 'train'
print('Selected mode is '+mode)

if mode == 'dev':
    filePath = glob.glob("corpus/*dev.json")
elif mode == 'test':
    filePath = glob.glob("corpus/*test.json")
elif mode == 'train':
    filePath = glob.glob("corpus/*train.json")

print("Read corpus from '{}'".format(filePath[0]))

f = open(filePath[0], "r", encoding='UTF8')
corpus = json.load(f)
print("Corpus loaded")

result = []
for sentenceIdx in range(len(corpus['sentence'])):
    _sentence = corpus['sentence'][sentenceIdx]
    _morph = []
    for morphIdx in range(len(_sentence['morp'])):
        _line = []
        _lemma = _sentence['morp'][morphIdx]['lemma']
        _type = _sentence['morp'][morphIdx]['type']
        _line.append(_lemma+'/'+_type)
        _line.append('O')
        _morph.append(_line)
    for neIdx in range(len(_sentence['NE'])):
        type = _sentence['NE'][neIdx]['type']
        begin = _sentence['NE'][neIdx]['begin']
        end = _sentence['NE'][neIdx]['end']

        length = end - begin

        _morph[begin][1] = 'B-'+type
        if length == 0:
            continue
        else :
            for bioIdx in range(length):
                _morph[begin+bioIdx+1][1] = 'I-'+type


    result.append(_morph)
print("Parsing complete")


with open("result/NER_"+mode+".txt", 'w', encoding='utf-8') as f:
    for sublist in result:
        for subsublist in sublist:
            line = "{} {}\n".format(subsublist[0], subsublist[1])
            f.write(line)
        f.write('\n')
print("Result saved")
