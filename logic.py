from databaseX import DatabaseX


class Logic:
    def __init__(self):
        self.__databaseXObj = self.createDatabaseX()

    def get_databaseXObj(self):
        return self.__databaseXObj

    def createDatabaseX(self):
        database = DatabaseX()
        return database

    def tupleToDictionaryList(self, tupleList, keyList):
        newDict = {}
        newList = []
        for item in tupleList:
            counter = 0
            currentList = list(item)
            for key in keyList:
                newDict[key] = currentList[counter]
                counter += 1
            newList.append(newDict)
            newDict = {}
        return newList
