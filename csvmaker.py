from random import random, choice
from csv import DictWriter
from itertools import accumulate
from bisect import bisect

class QuestionExp(Exception): pass

class RandomSentences:
    def __init__(self):
        Lorem = '''Lorem ipsum dolor sit amet, consectetur adipisci elit, sed eiusmod tempor incidunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur. Quis aute iure reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint obcaecat cupiditat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'''
        Iliade = '''Cantami, o diva, del Pelìde Achille l'ira funesta che infiniti addusse lutti agli Achei, molte anzi tempo all'Orco generose travolse alme d'eroi, e di cani e d'augelli orrido pasto lor salme abbandonò (così di Giove l'alto consiglio s'adempia), da quando primamente disgiunse aspra contesa il re de' prodi Atride e il divo Achille.'''
        Fox = '''The quick brown fox jumps over the lazy dog'''
        Pranzo = '''Pranzo d'acqua fa volti sghembi'''
        Victor = '''Zwölf Boxkämpfer jagen Victor quer über den großen Sylter Deich'''
        Brick = '''Voyez le brick géant que j'examine près du wharf'''
        Eco = '''Tv? Quiz, Br, Flm, Dc... Oh, spenga!'''
        Mattia = '''Una delle poche cose, anzi forse la sola ch'io sapessi di certo era questa: che mi chiamavo Mattia Pascal. E me ne approfittavo. Ogni qual volta qualcuno de' miei amici o conoscenti dimostrava d'aver perduto il senno fino al punto di venire da me per qualche consiglio o suggerimento, mi stringevo nelle spalle, socchiudevo gli occhi e gli rispondevo: — Io mi chiamo Mattia Pascal. — Grazie, caro. Questo lo so. — E ti par poco?'''
        Hamlet = '''To be, or not to be: that is the question: Whether 'tis nobler in the mind to suffer The slings and arrows of outrageous fortune, Or to take arms against a sea of troubles, And by opposing end them? To die: to sleep; No more; and by a sleep to say we end The heart-ache and the thousand natural shocks That flesh is heir to, 'tis a consummation Devoutly to be wish'd. To die, to sleep; To sleep: perchance to dream: ay, there's the rub; For in that sleep of death what dreams may come When we have shuffled off this mortal coil, Must give us pause: there's the respect That makes calamity of so long life; For who would bear the whips and scorns of time, The oppressor's wrong, the proud man's contumely, The pangs of despised love, the law's delay, The insolence of office and the spurns That patient merit of the unworthy takes, When he himself might his quietus make With a bare bodkin? who would fardels bear, To grunt and sweat under a weary life, But that the dread of something after death, The undiscover'd country from whose bourn No traveller returns, puzzles the will And makes us rather bear those ills we have Than fly to others that we know not of? Thus conscience does make cowards of us all; And thus the native hue of resolution'''
        Inferno = '''Nel mezzo del cammin di nostra vita mi ritrovai per una selva oscura, ché la diritta via era smarrita. Ahi quanto a dir qual era è cosa dura esta selva selvaggia e aspra e forte che nel pensier rinova la paura! Tant’è amara che poco è più morte; ma per trattar del ben ch’i’ vi trovai, dirò de l’altre cose ch’i’ v’ ho scorte.'''
        self.sentences = [Lorem[:116], Hamlet[199:367], Iliade, Lorem[117:248],
                          Inferno[:102], Fox, Lorem[249:], Pranzo, Mattia[107:],
                          Hamlet[890:], Victor, Inferno[103:210],
                          Brick, Eco, Mattia[:106], Hamlet[:198],
                          Hamlet[367:889], Inferno[211:]]

        self.count = {'multichoice': 0,
                      'truefalse': 0,
                      'plaintext': 0}

        self.functions = (self._multichoice,
                          self._truefalse,
                          self._plaintext)
        return

    def getSentences(self, quantity):
        output = []
        for i in range(quantity):
            output.append(choice(self.sentences))

        return output

    def getQuestions(self, n=4, multichoice=0.8, truefalse=0.15, plaintext=0.05):
        if (multichoice + truefalse + plaintext) != 1:
            raise QuestionExp('multichoice + truefalse + plaintext != 1')
        if n < 2 and truefalse != 0:
            raise QuestionExp('n < 2 and truefalse != 0')
        
        aggregate = list(accumulate((multichoice, truefalse, plaintext)))
        r = random() * aggregate[-1]

        return self.functions[bisect(aggregate, r)](n)
    
    def _multichoice(self, n):
        self.count['multichoice'] += 1
        return self.getSentences(n+1)

    def _truefalse(self, n):
        self.count['truefalse'] += 1
        return (self.getSentences(1) + ['Vero', 'Falso'] +
                ['' for i in range(2, n)])
        
    def _plaintext(self, n):
        self.count['plaintext'] += 1
        return self.getSentences(2) + ['' for i in range(1, n)]
        
    
rowsNum = 6
category = ['10', '20', '30']
image = ['image/a.png', 'image/b.png', 'image/c.png', '', '', '']
fieldnames = ('category',
                  'question',
                 'A',
                 'B',
                 'C',
                 'D',
                 'image')

rSentences = RandomSentences()
questArg = {'n': 4, 'multichoice': 0.34,
            'truefalse': 0.33, 'plaintext': 0.33}

with open('sample.csv', 'w') as csvfile:
    writer = DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for i in range(rowsNum):
        questAnswers = rSentences.getQuestions(**questArg)
        
        row = {key: value for key, value in zip(fieldnames[1:6], questAnswers)}
        row['category'] = choice(category)
        row['image'] = choice(image)
        writer.writerow(row)

print(rSentences.count)
