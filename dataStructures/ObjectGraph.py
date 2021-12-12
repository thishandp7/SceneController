class ObjectGraph(object):


    def __init__(self):
        self.graph = {}


    def addObject(self, key, obj):
        self.graph[key] = obj


    def removeObjectByKey(self, key):
        del self.graph[key]


    def removeObjectByValue(self, obj):
        for key, value in self.graph.items():
            if obj == value:
                del self.graph[key]
                return


    def getObjectByKey(self, key):
        return self.graph[key]


    def getKeyByValue(self, obj):
        for key, value in self.graph.items():
            if obj == value:
                return key


    def getScalerByKey(self, key):
        container = self.getObjectByKey(key)
        return container.getScalarValue()


    def updateScalerByKey(self, key, value):
        container = self.getObjectByKey(key)
        container.setScalarValue(value)
        print('updating {key} scale: {value}'.format(key=key, value=value))


    def getFullGraph(self):
        return self.graph