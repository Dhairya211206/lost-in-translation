import re
import spacy
import enchant

nlp=spacy.load("en_core_web_sm")
d=enchant.Dict("en_US")

typos = {
    '5':'s',
    '0':'o',
    'e':'c',
    'c':'e',
    '1':'l',
    'h':'b',
    'b':'h'
}
discourse_punc={'however','therefore','moreover','nevertheless','meanWhile'}

def properNouns(text):
    doc=nlp(text)

    return list(set(ent.text for ent in doc.ents if ent.label_ in {'PERSON', 'ORG', 'GPE', 'PRODUCT'}))


def correct_typo(word,typo_map):
    for i,char in enumerate(word):
        if char in typo_map:
            return word[:i]+typo_map[char]+word[i+1:]
    return word


def fix_commas(text):
    for marker in discourse_punc:
        pattern=r'\b' + re.escape(marker) + r'\b(?!,)'
        replacement=marker.capitalize() + ','
        text=re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    return text


def autocorrect(text, proper_nouns):
    doc = nlp(text)
    corrected = []

    for token in doc:
        word = token.text
       
        if token.is_punct:
            corrected.append(word + token.whitespace_)
            continue
      
        if word in proper_nouns or token.ent_type_ in {'PERSON', 'ORG', 'GPE', 'PRODUCT'}:
            corrected.append(word + token.whitespace_)
            continue

     
        if d.check(word):
            corrected.append(word + token.whitespace_)
            continue


        fixed = correct_typo(word, typos)

       
        if word.istitle():
            fixed = fixed.capitalize()
        corrected.append(fixed + token.whitespace_)
    return fix_commas(''.join(corrected))


def process_text(text):
    proper_nouns = properNouns(text)
    corrected = autocorrect(text, proper_nouns)
    return corrected, proper_nouns

texts = [
    '''In April 2023, Sundar Pichai did announce that Google would be launehing a new AI product namcd Gemini.
    Barack Obama also gave a speech at Harvard University, cmphasizing the role of technology in modern education.''',

    '''Project X is an exclusive elub at Veermata Jijabai Technological Institute, Mumbai, mcant to 5erve as a healthy environment for 5tudents to learn from each other and grow together.
    Through the guidance of their mcntors these 5tudents are able to complete daunting tasks in a relatively short time frame, gaining significant exposure and knowledge in their domain of choice.''',

    '''I will be eompleting my BTech dcgree in Mechanical Engineering from VJTI in 2028''',

    '''However the rcsults were clear'''
]

for i, text in enumerate(texts,1):
    corrected, nouns=process_text(text)
    print(f"\nText {i}")
    print("Corrected Text:\n", corrected)
    print("Proper Nouns:\n", nouns)
