try:
    from nltk import CFG, Production, Nonterminal
    from hazm import word_tokenize, POSTagger
    from nltk import ChartParser
    from langdetect import detect
    import matplotlib.pyplot as plt
    tagger = POSTagger(model='pos_tagger.model')
except:
    print("Make sure the following modules are installed: nltk, hazm, matplotlib.pyplot, langdetect. There also should be a 'pos_tagger.model' file in the directory that can be downloaded via the link: https://drive.google.com/file/d/1Q3JK4NVUC2t5QT63aDiVrCRBV225E_B3")

base_grammar = CFG.fromstring("""
    FulS -> S PUNCT | S | PUNCT S | PUNCT S PUNCT
    S -> NP VP | VP | VP CP | VP SConjP
    SConjP -> SCONJ VP
    CP -> CONJ NP | CONJ VP
    CompV -> N V | ADJ V
    NP_ez -> N_ez NP | N_ez AdjP | N_ez NP_ez | NP_ez PRO
    ProP -> PRO NP | PRO NP_ez
    NP -> N | N_ez | N NP | N AdjP | NP CONJ NP | N AdjP | NP N | NP PRO | PRO NP | NUM NP | ProP CONJ NP | NP CONJ ProP | PUNCT N PUNCT | PUNCT NP PUNCT
    VP -> NP V | NP_ez V | AdjP V | ADV VP | N VP | PP V | PP VP | PostP V | ProP VP | V | V VP | DetP VP
    ProP -> PRO | PRO CONJ PRO
    DemP -> DEM NP
    AdjP -> ADJ | ADJ_ez | ADJ_ez AdjP | ADJ_ez DetP | ADJ_ez NP | ADJ_ez ProP
    DetP -> DET NP | DetP ADJ
    PP -> P NP | P NP_ez | P DetP | P CONJ | PP VP | NUM PP | P NUM
    PostP -> NP P | ProP P
""")

"""
    FulS::= PUNCT* S PUNCT* SConjP* PUNCT*                                                                                          // целое предложение
    S ::= NP* VP CP*                                                                                                                // главное предложение
    SConjP ::= SCONJ VP                                                                                                             // зависимое предложене
    CP ::= CONJ+ NP | CONJ+ VP                                                                                                      // conjunction phrase
    CompV ::= (N | ADJ)+ V                                                                                                          // комплимента глагольной группы
    PP ::= P (NP | NP_ez | DetP) | PP VP | NUM PP                                                                                   // prepositional phrase
    PostP -> (NP | NP_ez) P | ProP P                                                                                                // postpositional phrase
    ProP ::= PRO (NP | NP_ez+)                                                                                                      // pronoun phrase
    NP_ez ::= N_ez+ (NP | AdjP) | N_ez+ PRO                                                                                         // изафетная конструкция
    DetP ::= DET (NP | NP_ez)                                                                                                       // determinant phrase
    VP ::= (NP| DemP | NP_ez | AdjP| PP | PostP | DetP) V | (ADV | PP | N | ProP | DetP | VP CONJ) VP | V VP*                       // verb phrase
    DemP ::= DEM NP                                                                                                                 // demonstrative phrase
    NP ::= N (NP | AdjP) | NP CONJ NP | NP (N | PRO) | (PRO | NUM) NP | ProP CONJ NP | NP CONJ ProP | PUNCT (N | NP) PUNCT          // noun phrase
    ProP ::= PRO (CONJ PRO)*                                                                                                        // местоименная группа
    AdjP ::= ADJ | ADJ_ez (ADJ | AdjP | DetP | NP | ProP)                                                                           // adjective phrase
"""
# base_grammar = CFG.fromstring("""
#     FulS -> S PUNCT | S | PUNCT S | PUNCT S PUNCT
#     S -> NP VP | VP | VP CP | VP SConjP
#     SConjP -> SCONJ VP
#     CP -> CONJ NP | CONJ VP
#     CompV -> N V | ADJ V
#     NP_ez -> N_ez NP | N_ez AdjP | N_ez NP_ez | NP_ez PRO
#     ProP -> PRO NP | PRO NP_ez
#     NP -> N | N_ez | N NP | N AdjP | NP CONJ NP | N AdjP | NP N | NP PRO | PRO NP | NUM NP | ProP CONJ NP | NP CONJ ProP | PUNCT N PUNCT | PUNCT NP PUNCT
#     VP -> NP V | NP_ez V | AdjP V | ADV VP | N VP | PP V | PP VP | PostP V | ProP VP | V | V VP | DetP VP
#     ProP -> PRO | PRO CONJ PRO
#     DemP -> DEM NP
#     AdjP -> ADJ | ADJ_ez | ADJ_ez AdjP | ADJ_ez DetP | ADJ_ez NP | ADJ_ez ProP
#     DetP -> DET NP | DetP ADJ
#     PP -> P NP | P NP_ez | P DetP | P CONJ | PP VP | NUM PP | P NUM
#     PostP -> NP P | ProP P
# """)

def parse_sentence(sentence:str):
    try:
        # Проверяем язык текста
        lang = detect(sentence)
        if lang != 'fa':
            return print("Пожалуйста, введите предложение на персидском языке.")
        else:
            tagged_s = tagger.tag(word_tokenize(sentence))
        
        return tagged_s
    except:
        return print("Не удалось распознать предложение.")
    
def update_grammar_with_pos_tags(base_grammar, tagged_s):
    # Собираем множества слов для каждой части речи
    nouns = set()
    nouns_ez = set()
    pronouns = set()
    verbs = set()
    adjectives = set()
    adjectives_ez = set()
    adverbs = set()
    demonstratives = set()
    determinatives = set()
    prepositions = set()
    conjunctions = set()
    sconjunctions = set()
    punctuation = set()
    numer = set()
    for word, tag in tagged_s:
        if tag == 'NOUN':
            nouns.add(word)
        elif tag == 'NOUN,EZ':
            nouns_ez.add(word)
        elif tag.startswith('V'):
            verbs.add(word)
        elif tag == 'ADJ':
            adjectives.add(word)
        elif tag == 'ADJ,EZ':
            adjectives_ez.add(word)
        elif tag == 'DEM':
            demonstratives.add(word)
        elif tag == 'DET':
            determinatives.add(word)
        elif tag == 'ADP' or tag == 'ADP,EZ':
            prepositions.add(word)
        elif tag == 'CCONJ':
            conjunctions.add(word)
        elif tag == 'SCONJ':
            sconjunctions.add(word)
        elif tag == 'PRON':
            pronouns.add(word)
        elif tag == 'NUM':
            numer.add(word)
        elif tag == 'ADV':
            adverbs.add(word)
        elif tag == 'PUNCT':
            punctuation.add(word)

    # Создаем список правил для обновления грамматики
    new_productions = []
    for noun in nouns:
        new_productions.append(Production('N', [noun]))
    for noun_ez in nouns_ez:
        new_productions.append(Production('N_ez', [noun_ez]))
    for pronoun in pronouns:
        new_productions.append(Production('PRO', [pronoun]))
    for verb in verbs:
        new_productions.append(Production('V', [verb]))
    for adj in adjectives:
        new_productions.append(Production('ADJ', [adj]))
    for adj_ez in adjectives_ez:
        new_productions.append(Production('ADJ_ez', [adj_ez]))
    for num in numer:
        new_productions.append(Production('NUM', [num]))
    for adv in adverbs:
        new_productions.append(Production('ADV', [adv]))
    for conj in conjunctions:
        new_productions.append(Production('CONJ', [conj]))
    for sconj in sconjunctions:
        new_productions.append(Production('SCONJ', [sconj]))
    for dem in demonstratives:
        new_productions.append(Production('DEM', [dem]))
    for det in determinatives:
        new_productions.append(Production('DET', [det]))
    for prep in prepositions:
        new_productions.append(Production('P', [prep]))
    for punct in punctuation:
        new_productions.append(Production('PUNCT', [punct]))
    
    # Создаем CFG с объединенными правилами
    updated_grammar = CFG(base_grammar.start(), base_grammar.productions() + new_productions)
    
    words_and_phrases = {}
    # Избавляемся от ненужных одиночных кавычек в правилах
    for production in updated_grammar.productions():
        nonterminal = production.lhs()  
        if isinstance(production.rhs()[0], str):
            if nonterminal not in words_and_phrases:
                words_and_phrases[nonterminal] = [] 
            words_and_phrases[nonterminal].append(production.rhs()[0])

    productions = list(base_grammar.productions())
    for nonterminal, words_list in words_and_phrases.items():
        for word in words_list:
            productions.append(Production(Nonterminal(nonterminal), [word]))

    grammar = CFG(base_grammar.start(), productions)
    return grammar

def get_the_tree(sentence:str):
    tagged_s = parse_sentence(sentence)
    grammar = update_grammar_with_pos_tags(base_grammar, tagged_s)
    parser = ChartParser(grammar)
    for tree in parser.parse(word_tokenize(sentence)):
        print(tree)
        fig, ax = plt.subplots(figsize=(12, 6))
        tree.draw()
        plt.show()
        break