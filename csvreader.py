import csv

def main():
##    fieldnames = ('category',
##                  'question',
##                 'A',
##                 'B',
##                 'C',
##                 'D',
##                 'image')
    
    cvs_name = 'AAtest.csv'

    with open(cvs_name) as fd:
##        data = csv.DictReader(fd, fieldnames=fieldnames)
        data = csv.DictReader(fd)        
        for dictRec in data:
##            for name in fieldnames:
##                print(dictRec[name])
            for key, value in dictRec.items():
                print(key, ': ', value[:20])

    return

if __name__ == '__main__':
    main()
