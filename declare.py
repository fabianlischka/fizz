import bs4
import urllib.request
import re
import random

# import functools

evil = True # if evil, we mix all declarations up before printing

noDeclaration = ["Argentina", "Germany", "Hong", "China"]
declarationTemplates = [
    'I am not a citizen of {0}.', 
    'I am not a "{0} resident alien".',
    'I was not born in {0} or a territory thereof.',
    'I am not a "{0} person" under any sensible principles (and thus, presumably, under {0} tax principles), as far as I can tell.',
    'I hereby declare that I am the beneficial owner of the assets and income to which this form relates, according to any sensible principles (and thus, presumably, according to {0} tax principles), and that no other beneficial owner exists.',
    'I hereby undertake to notify the Bank, at my own initiative and within 30 days, if my status under {0} tax principles changes to the status of a {0} Person under {0} tax principles, subject to the change being due to a change in my circumstances, not a change in the {0} tax principles, and furthermore subject to the Bank explicitly having requested me to do so.',
    'I declare that if there is a substantial presence test under {0} tax principles and it allows for treatment as a nonresident alien under certain conditions (e.g. that I stay in {0} less than 183 days a year and I maintain a tax home in a foreign country during the year to which I have a closer connection than to {0}), then, as far as I can tell, I qualify for treatment as a nonresident alien under {0} tax principles, because said conditions hold.'
    ]


def splitjoin(f,ss):
    return [" - ".join(map(f,s.split("-"))) for s in ss]

def wrap(s):
    ss = s.split("-")
    if len(ss) > 1:
        return ss[0].strip() + " (" + ss[1].strip() + ")"
    else:
        return s

def removeNotes(s):
    pattern = re.compile("\[.*\]")
    return re.sub(pattern, u"", s)

def notInNoDeclaration(s):
    for subs in noDeclaration:
        if subs in s:
            print("dropping '{}', because '{}' is on the noDeclaration list.".format(s,subs))
            return False
    return True

transforms = [
    (map,       lambda s: s.text.replace(u'\xa0', u' ').strip()), # remove nbsp, leading/trailing spaces
    (filter,    lambda s: "→" not in s and "ZZZ" not in s),       # remove synonyms
    (map,       lambda s: s.replace(u"–","-")),                   # fix dashes
    (map,       removeNotes),                                     # remove [Notes]
    (splitjoin, lambda s: " ".join(reversed(s.split(","))).strip()), # turn "x, the" into "the x" 
    (filter,    notInNoDeclaration),                              # filter out noDeclare list 
    (map,       lambda s: s.replace(u"  ",u" ")),                 # remove double spaces
    (map,       wrap)                                             # turn "a - b" into "a (b)"
    ]


# get sovereign states
u = "http://en.wikipedia.org/wiki/List_of_sovereign_states"
b = bs4.BeautifulSoup(urllib.request.urlopen(u))

col = b.table.find_all("td")
ct = [col[12+k*4] for k in range((len(col)-12)//4)]

# transform them
for tf1, tf2 in transforms:
    ctn = tf1(tf2,ct)
    ct = ctn

ct = list(ct) # force filtering to run before printing

# generate declarations
declarations = [d.format(c) for c in ct for d in declarationTemplates]
if evil:
    random.shuffle(declarations)

# print them
print("\n\nPrinting {} declarations:\n\n".format(len(declarations)))
for d in declarations:
    print(d)
