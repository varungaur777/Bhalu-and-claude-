import re
RULES=[
 ("Cloze Test", r"passage.{0,40}(words|blanks?) (have been|has been|are) (deleted|removed|left)|fill in the blanks? .{0,40}passage|in the following passage,? some|blank (number|no\.?)\s*\d|passage.{0,60}fill in the blank"),
 ("Reading Comprehension", r"read the (following|given)? ?passage|passage .{0,30}answer the question|answer the questions? (that follow|given|based)|based on the passage|comprehension"),
 ("Active & Passive Voice", r"passive|active (form|voice)"),
 ("Direct & Indirect Speech", r"indirect|direct (form|speech)|reported speech|narration"),
 ("Para Jumbles", r"\(s1\)|s1 to s4|jumble|rearrange|arrange the (parts|sentences)|correct (order|sequence)|logical sequence|coherent paragraph|static|first and (the )?last sentences"),
 ("Idioms & Phrases", r"proverb|underlined phrase|idiom|phrase given|phrasal verb"),
 ("One Word Substitution", r"substituted for the given words|set of words|one[- ]word|group of words|single word"),
 ("Spelling Errors", r"spelt|spelled|misspel|spelling"),
 ("Synonyms", r"meaning of the underlined word|synonym|similar (in )?meaning|means the same|same meaning|nearest in meaning|closest meaning"),
 ("Antonyms", r"antonym|opposite"),
 ("Sentence Improvement", r"improve|substitute the underlined|underlined (segment|part)|substitution|replace the underlined"),
 ("Error Spotting", r"incorrect sentence|degree|error|incorrectly used|segments?|divided into|grammatically (in)?correct|parts of the (following|given) sentence"),
 ("Fill in the Blanks", r"collocation|fill in the blank|complete the (given )?sentence|blank|homonym|homophone"),
]
def classify(qtext):
    t=qtext.lower()
    head=t[:400]
    for name,rx in RULES:
        if re.search(rx,head): return name
    return "Miscellaneous"
