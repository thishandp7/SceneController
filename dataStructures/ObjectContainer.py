

class ObjectContainer(object):


    def __init__(self, name=None, slider=None, scalarValue=0):
        self.controllerButton = None
        self.name = name
        self.slider = slider
        self.scalarValue = scalarValue


    def setName(self, name):
        self.name = name


    def getName(self):
        return self.name


    def setSlider(self, slider):
        self.slider = slider


    def getSlider(self):
        return self.slider


    def setControllerButton(self, controllerButton):
        self.controllerButton = controllerButton


    def getControllerButton(self):
        return self.controllerButton


    def setScalarValue(self, scaler):
        self.scalarValue = scaler


    def getScalarValue(self):
        return self.scalarValue