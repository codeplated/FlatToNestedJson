import os, sys, json, itertools

class FlatToNested:
    def __init__(self):
        os.chdir(os.path.abspath(os.path.dirname(__file__)))
 
    def newDict(self, dictname):
        setattr(self, dictname, {})
 
    def addNode(self, parent, nodename, lastNode):
        if not lastNode:
            node = parent[nodename] = {}
        else:
            node = parent[nodename] = [{}]
        return node
     
    def addCell(self, nodename, cellname, value):
        cell =  nodename[0] = {cellname:value}
        return cell

    def getParent(self, row, parentDict, sortingOrder):
        parent = {}

        for j, i in enumerate(sortingOrder):
            if not row[i] in parentDict:
                return parent, j
            else:
                parent = parentDict[row[i]]     
        return parent

    def mergeLists(self, *lists):
        newlist = []

        for x in itertools.chain.from_iterable(lists):
            if x not in newlist:
                newlist.append(x)
        return newlist
    
    def nestJson(self, sortingOrder, flatJson):
        nestingLevel = len(sortingOrder)
        keyList =  list(flatJson[0].keys())
        sortingOrder = self.mergeLists(sortingOrder, keyList)   
        lastNode = False
        parentDict = {}

        for row in flatJson:
            parent, index = self.getParent(row, parentDict, sortingOrder)
            if not bool(parent):
                parent = self.nestedJson
    
            for i in range(index,len(row)):
                if(i<nestingLevel-1):
                    if i == nestingLevel-2:
                        lastNode = True
                    parent = self.addNode(parent, row[sortingOrder[i]], lastNode)
                    parentDict[row[sortingOrder[i]]] = parent
                    lastNode = False
                else:
                    self.addCell(parent, sortingOrder[i], row[sortingOrder[i]]) 
        return self.nestedJson   

    def filterJson(self, sortingOrder, jsonData):
        filteredJson = []

        for row in jsonData['features']:
            pairs = {}

            for key in sortingOrder:
                if not 'place' in key:
                    pairs[key] = row['properties'][key]
                else:
                    place = row['properties'][key]
                    if ', ' in place:
                        place = place.split(', ')[1]     
                    pairs[key] = place
            filteredJson.append(pairs)
        return filteredJson

def loadInputFile(inputJsonFile):
    with open(inputJsonFile, 'r') as myfile:
        file= myfile.read()
    return json.loads(file)

def dumpJson(jsonData):
    with open('output.json', 'w') as fp:
        json.dump(jsonData, fp, sort_keys=True, indent=2)
    
def mainFunc(sortingOrder):
    sortingOrder.pop(0)
    inputJsonFile = sortingOrder.pop(0)
    
    flatJson = loadInputFile(inputJsonFile)
    flatToNested = FlatToNested()
    flatToNested.newDict('nestedJson')
    nestedJson = flatToNested.nestJson(sortingOrder, flatJson)

    dumpJson(nestedJson)
    flatToNested.printDict(nestedJson)
    print(f'\nraw data: {nestedJson}')           
 
if __name__ == '__main__':
    mainFunc(sys.argv)
