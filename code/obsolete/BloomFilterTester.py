import random
import sys
import BloomFilter


class BloomFilterTester:
    # Beginning and end of the alphabet for random gene generation
    Astart = 97
    Zend = 122

    def __init__(self):
        self.goodData = []
        self.goodDataLength = 0

    def load(self, filename):
        with open(filename) as fd:
            x = fd.readline()
            line = x.replace("\n", "")
            while line:
                self.goodData.append(line)
                x = fd.readline()
                line = x.replace("\n", "").replace("\r", "")

        self.goodDataLength = len(self.goodData)
        self.filter = BloomFilter.BloomFilter(self.goodDataLength)

        print("Tester: Read ", len(self.goodData), " good genes")

    def train(self):
        print("Training filter...")
        for gene in self.goodData:
            self.filter.train(gene)

    def createGene(self):
        return "".join(map(lambda i: chr(random.randint(self.Astart, self.Zend)), range(random.randint(4, 8)))).upper()

    def check(self):
        gene = ""
        ok = False
        falsePos = 0
        falseNeg = 0
        checkSize = 2 * len(self.goodData)

        print("Checking filter...")

        for i in range(1, checkSize):
            if i % 50000 == 0:
                print((i / checkSize * 100), "percent done")
                print("Classifications: ", i)
                print("False negative rate:", falseNeg / i)
                print("False positive rate:", falsePos / i)

            r = random.randint(0, 10)
            # test random gene from the good data
            if(r == 7):
                idx = random.randint(0, self.goodDataLength - 1)
                gene = self.goodData[idx]

                if not self.filter.classify(gene):
                    falseNeg += 1
            else:
                gene = self.createGene()

                if self.filter.classify(gene):
                    falsePos += 1

        print("Total classifications: ", checkSize)
        print("False negative rate:", falseNeg / checkSize)
        print("False positive rate:", falsePos / checkSize)

        if falseNeg > 0:
            print("FAIL: some good strings were classified as bad")
        elif (falsePos / checkSize) > 0.05:
            print("FAIL: the rate of false positives is larger than 0.05:",
                  (falsePos / checkSize))
        else:
            print("Correct")


tester = BloomFilterExe()
tester.load(sys.argv[1])
tester.train()
tester.check()
