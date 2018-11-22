from query_processing import QueryProcessor
import os
import operator
import pprint

class GeneralQuery:
    def __init__(self, queryString, description, OS, ram, storage, price, useTfIdf = True):
        self.queryString = queryString
        self.description = description
        self.OS = OS
        self.ram = ram
        self.storage = storage
        self.price = price
        self.documents = os.path.abspath('../inverted_index/db/')
        self.twoTermsPath = os.path.abspath('../inverted_index/twoTerms.json')
        self.invIndexPath = os.path.abspath('../inverted_index/frequency.json')
        self.fieldQuery = QueryProcessor(invIndexPath=self.twoTermsPath, documentsPath=self.documents)
        self.wordQuery = QueryProcessor(invIndexPath=self.invIndexPath, documentsPath=self.documents)
        self.useTfIdf = useTfIdf

    def processQuery(self):
        gameList = []
        if(self.queryString != ''):
            games = self.wordQuery.query(self.queryString, useTfIdf = self.useTfIdf)
            gameList.append(games)
        if(self.description != ''):
            games = self.fieldQuery.query(self.description, useTfIdf=self.useTfIdf, field="description")
            gameList.append(games)
        if(self.storage != ''):
            games = self.fieldQuery.query(self.storage, useTfIdf=self.useTfIdf, field="storage")
            gameList.append(games)
        if(self.OS != ''):
            games = self.fieldQuery.query(self.OS, useTfIdf=self.useTfIdf, field="os")
            gameList.append(games)
        if(self.price != ''):
            games = self.fieldQuery.query(self.price, useTfIdf=self.useTfIdf, field="price")
            gameList.append(games)
        if(self.ram != ''):
            games = self.fieldQuery.query(self.ram, useTfIdf=self.useTfIdf, field="ram")
            gameList.append(games)
        
        gamesHash = {}
        #take average of the tfidf of each game returned in the query
        for i in range(len(gameList)): 
            for game in gameList[i]:
                if not str(game[0]) in gamesHash:
                    gamesHash[str(game[0])] = float(game[1])
                else:
                    gamesHash[str(game[0])] += float(game[1])
    
        for name in gamesHash:
            gamesHash[name] /= 6

        #sort by highest tfidf average
        sorted_games = sorted(gamesHash.items(), key=operator.itemgetter(1), reverse=True)

        return sorted_games