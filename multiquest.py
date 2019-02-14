from random import shuffle

from singlequest import SingleQuest

class MultiQuest:
    '''Put more shuffled Simplequest together and save as flowable
    '''
    def __init__(self, questsLst, to_shuffle=False):
        if to_shuffle:
            shuffle(questsLst)
        
        self.questsLst = []
        for quest, count in zip(questsLst, range(1, len(questsLst) + 1)):
            sQuest = SingleQuest(questID=count, **quest)
            self.questsLst.append(sQuest)

        return

    def __str__(self):
        return ''.join([item.__str__() + '\n' for item in self.questsLst])
        
    def get_flowables(self):
        flowLst = [item.getFlowable()[0] for item in self.questsLst]

        return flowLst
