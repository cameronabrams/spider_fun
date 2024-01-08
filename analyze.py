import json
import argparse as ap
import inflect
from wordcloud import WordCloud, STOPWORDS 
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import re
ie=inflect.engine()

excludes=['do','of','and','in','the','a','or',
        'to','on','for','by','from','an',
        'as','its','with','-','at','using',
        'via','through','into','toward','b',
        'within','it','is','t','H','2','12','a-c','-o','2005','6803']
not_plurals=['analysis','amorphous','aqueous',
            'metadynamics','spontaneous','address',
            'viscous','stress','mols','dynamics','axis','angle-axis','toughness','campus','this']
#no_splits=['Streptoccocus mutans']

eup=[]
for e in excludes:
    eup.append(e.title())
excludes.extend(eup)
caps = ['HIV-1','CO2','Si','H','N2','DGEBA',
        'AdResS','Monte-Carlo','MOLS','FRET','PAA-PMA','NMR','GFP'
        'PNIPAm','SWINGER','TIP3P','PPE','DPD','Monte','Carlo','PAA']

def remove_escapes(word):
    ret=''
    tfr=True
    for c in word:
        if ord(c)>128:
            tfr=False
        if tfr:
            ret+=c
    return ret
        

def process_line_into_wordlist(ln):
    this_split=re.sub("[^\w-]", " ", ln).split()
    raw_ws = []
    nesc=0
    for ww in this_split:
        w=remove_escapes(ww)
        if w not in excludes:
            if w in caps:
                raw_ws.append(w)
            else:
                token = w.lower()
                if token not in not_plurals:
                    sing=ie.singular_noun(token)
                    if not sing:
                        raw_ws.append(token)
                    else:
                        raw_ws.append(sing)
                else:
                    raw_ws.append(token)
    return raw_ws

if __name__=='__main__':
    parser=ap.ArgumentParser()
    parser.add_argument('-f',type=str,help='name of json input file')
    args=parser.parse_args()
    with open(args.f,'r',encoding='utf-8') as f:
        data=f.read()
        dataset=json.loads(data)
    all_w=[]
    print(f'{args.f} has data for {len(dataset)} items')
    for item in dataset:
        xfr=False
        for p in item['body']:
            if 'Sincerely' in p:
                xfr=False
            if xfr:
                all_w.extend(process_line_into_wordlist(p))
            if 'Dear' in p:
                xfr=True
    word_count={}
    for w in set(all_w):
        word_count[w]=all_w.count(w)
    print(f'{len(all_w)} words, {len(word_count)} distinct')
    # for w in sorted(word_count,key=word_count.get,reverse=True):
    # #    print(w,word_count[w])
    #     print('{:30s} {:4d}'.format(str(w),word_count[w]))
    comment_words = ' '
    stopwords = set(STOPWORDS) 
    for wd in all_w:
        if len(wd)>2:
            comment_words = comment_words + wd + ' '
    #help(WordCloud)
    wordcloud = WordCloud(width=900,height=600, 
                    background_color='white',normalize_plurals=False, collocations=False,
                    min_font_size=10,colormap=cm.gist_stern).generate(comment_words) 
    
    # plot the WordCloud image                        
    plt.figure(figsize=(9,6),facecolor=None) 
    plt.imshow(wordcloud) 
    plt.axis("off") 
    plt.tight_layout(pad=0)
    plt.savefig('wordcloud-fry.png')
