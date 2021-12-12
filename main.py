import importlib
import math
import sys
sys.path.append('C:\\Users\\thishandp7\\Documents\\maya\\2020\\SceneController')
import maya.cmds as cmds
from pymel.core import mel
import dataStructures.ObjectGraph as og
import dataStructures.ObjectContainer as oc

importlib.reload(og)
importlib.reload(oc)

class SubjectController(object):


    def __init__(self):
        # can only save up to 6 objects.
        self.OBJECT_IDS = { 'obj1': 100, 'obj2': 0, 'obj3': 0, 'obj4': 0, 'obj5': 0, 'obj6': 0 }
        self.SCALE_MAX = 100
        self.SCALE_MIN = 0

        # self.objectGraph = ObjectGraph()

        self.center = None
        self.container = {}
        self.placementId = { 'obj1': 'obj1', 'obj2': 'obj2', 'obj3': 'obj3', 'obj4': 'obj4', 'obj5': 'obj5', 'obj6': 'obj6' }
        self.removeControllerButtons = {}
        self.setControllerButtons = {}
        self.sliders = {}
        self.objectNames = []

        self.initializeContainer()
        self.printContainer()

    # TODO: Use with ObjectContainer
    def initializeContainer(self):
        # initialize with 6 object for test purposes
        for ids in self.OBJECT_IDS:
            self.setObjectInContainer(ids, self.OBJECT_IDS[ids])

    # TODO: Use with ObjectContainer
    def setObjectInContainer(self, objectName, value):
        self.container[objectName] = value

    # TODO: Use with ObjectContainer
    def addObjectToContainer(self, key, objectName, value=0):
        currentRecordFromContainer = self.container[key]
        self.container[objectName] = currentRecordFromContainer
        print('object name from Container: {value}'.format(value=objectName))
        del self.container[key]

        currentRecordFromSlider = self.sliders[key]
        self.sliders[objectName] = currentRecordFromSlider
        del self.sliders[key]

        currentRecordFromSetButton = self.setControllerButtons[key]
        self.setControllerButtons[objectName] = currentRecordFromSetButton
        del self.setControllerButtons[key]

        self.placementId[key] = objectName
        self.objectNames.append(objectName)
        self.printContainer()
        self.printPlacements()
        self.printControllerButtons()
        self.printObjectNames()

    # TODO: Use with ObjectContainer
    def getTotalOfSubObject(self, mainObject):
        totalOfSubs = 0
        for item in self.container:
            if item != mainObject:
                totalOfSubs += self.container[item]
        return totalOfSubs

    # TODO: Use with ObjectContainer
    def modifyObject(self, objectName, scalarValue):
        print('scaling {name}:{scale}'.format(name=objectName, scale=scalarValue))
        updateValue = (scalarValue/100) * 1
        if objectName in self.objectNames:
            cmds.scale(updateValue, updateValue, updateValue, objectName)

    # TODO: Use with ObjectContainer
    def getNewValue(self, currentObject, starObject, totalOfSub):
        diff = 100 - (totalOfSub + self.container[starObject])
        # print('diff {value}'.format(value=diff))
        value = math.ceil(self.container[currentObject] / 100) * diff
        return value


    def createSubjectControls(self, parentLayout):
        print('Creating Scene Controls...')
        columnLayout = cmds.columnLayout(parent=parentLayout)
        self.buildSliders(columnLayout)
        print('sliders: ', self.sliders)

    # TODO: Use with ObjectContainer
    def setObjectToControl(self, *args):
        print('button pressed: {value}'.format(value=args))
        objectName = args[0]
        newObjectName = cmds.ls(sl=True, sn=True)[0]
        if newObjectName in self.container:
            print('{value} already exist'.format(value=newObjectName))
            return
        cmds.button(self.setControllerButtons[objectName], edit=True, label=newObjectName, enable=False)
        cmds.intSliderGrp(self.sliders[objectName], edit=True, label=newObjectName, enable=True)
        self.addObjectToContainer(objectName, newObjectName)


    def createRollerCenter(self, *args):
        print('Creating roller...', args)
        self.center = cmds.spaceLocator(name='center')
        for object in self.objectNames:
            cmds.parent(object, 'center')


    # TODO: Use with ObjectContainer
    def buildSliders(self, columnLayout):
        for objName in self.OBJECT_IDS:
            print('object name: {name}'.format(name=objName))
            dragCommandFunc = lambda value: lambda sliderName: self.setDragSliderValue(value, sliderName)
            setControllerCommand = lambda value: lambda name: self.setObjectToControl(value, name)
            localLayout = cmds.rowLayout(
                numberOfColumns=2,
                columnWidth2=(350, 120),
                columnAttach=[(1, 'both', 2), (2, 'both', 2)],
                adjustableColumn=2,
                parent=columnLayout)
            self.sliders[objName] = cmds.intSliderGrp(
                            enable=False,
                            label=objName,
                            field=True,
                            minValue=self.SCALE_MIN,
                            maxValue=self.SCALE_MAX,
                            fieldMinValue=self.SCALE_MIN,
                            fieldMaxValue=self.SCALE_MAX,
                            value=self.OBJECT_IDS[objName],
                            parent=localLayout,
                            dc=dragCommandFunc(objName))
            self.setControllerButtons[objName] = cmds.button(label=objName, command=setControllerCommand(objName), parent=localLayout)

        secondLayout = cmds.rowLayout(
            numberOfColumns=2,
            columnWidth2=(250, 250),
            columnAttach=[(1, 'both', 2), (2, 'both', 2)],
            adjustableColumn=2,
            parent=columnLayout)
        cmds.button(label='Create Roller', command=self.createRollerCenter, parent=secondLayout)


    def printContainer(self):
        print('-------------')
        print('==Container==')
        for item in self.container:
            print('{name}: {data}'.format(name=item, data=self.container[item]))
        print('=============')
        print('-------------')


    def printPlacements(self):
        print('-------------')
        print('=Placements==')
        for ids in self.placementId:
            print('{name}: {data}'.format(name=ids, data=self.placementId[ids]))
        print('=============')
        print('-------------')


    def printControllerButtons(self):
        print('-------------')
        print('=CtrlButtons=')
        for ids in self.setControllerButtons:
            print('{name}: {data}'.format(name=ids, data=self.setControllerButtons[ids]))
        print('=============')
        print('-------------')


    def printObjectNames(self):
        print('-------------')
        print('===Objects===')
        for objects in self.objectNames:
            print('{name}'.format(name=objects))
        print('=============')
        print('-------------')


    def printSlider(self):
        print('-------------')
        print('=============')
        for item in self.sliders:
            print('{name}: {data}'.format(name=item, data=self.sliders[item]))
        print('=============')
        print('-------------')


class SubjectControllerV2(object):


    def __init__(self):
        self.graph = og.ObjectGraph()
        self.SCALE_MAX = 100
        self.SCALE_MIN = 0


    def createSubjectControls(self, parentLayout):
        print('Creating Scene Controls...')
        row = cmds.rowLayout(
            numberOfColumns=1,
            columnWidth=(1, 500),
            adjustableColumn=1,
            columnAttach=[(1, 'both', 100)],
            parent=parentLayout)
        self.buildSliderSetup(row, parentLayout)


    def addObjectCommand(self, *args):
        print('Pressed!', args)
        parentLayout = args[1]
        # try:
        selectedObjects = cmds.ls(sl=True, sn=True)
        graph = self.graph.getFullGraph()
        for selectedObjectName in selectedObjects:
            if selectedObjectName in graph:
                print('{value} already exist'.format(value=selectedObjectName))
                return
            newSlider = self.renderSliders(selectedObjectName, parentLayout)
            newObject = oc.ObjectContainer(name=selectedObjectName, slider=newSlider, scalarValue=0)
            self.graph.addObject(selectedObjectName, newObject)


    def buildSliderSetup(self, row, parentLayout):
        cmds.button(label='Add Selected Objects', parent=row, command=lambda x: self.addObjectCommand(x, parentLayout))


    def renderSliders(self, objectName, columnLayout=None):
        dragCommandFunc = lambda value: lambda sliderName: self.updateValues(value, sliderName)
        localLayout = cmds.rowLayout(
            numberOfColumns=2,
            columnWidth2=(350, 120),
            columnAttach=[(1, 'both', 2), (2, 'both', 2)],
            adjustableColumn=2,
            parent=columnLayout)
        slider = cmds.intSliderGrp(
            label=objectName,
            field=True,
            minValue=self.SCALE_MIN,
            maxValue=self.SCALE_MAX,
            fieldMinValue=self.SCALE_MIN,
            fieldMaxValue=self.SCALE_MAX,
            value=0,
            parent=localLayout,
            dc=dragCommandFunc(objectName))
        return slider


    def getTotalOfSubObject(self, mainObject):
        totalOfSubs = 0
        for item in self.graph.getFullGraph():
            if item != mainObject:
                totalOfSubs += self.graph.getScalerByKey(item)
        return totalOfSubs


    def getNewValue(self, currentObject, starObject, totalOfSub):
        diff = 100 - (totalOfSub + self.graph.getScalerByKey(starObject))
        # print('diff {value}'.format(value=diff))
        value = math.ceil(self.graph.getScalerByKey(currentObject) / 100) * diff
        return value


    def updateValues(self, objectName, newValue):
        print('objectName, {value}'.format(value=objectName))
        cmds.scale(newValue/100, newValue/100, newValue/100, objectName)
        self.graph.updateScalerByKey(objectName, newValue)
        totalOfSubs = self.getTotalOfSubObject(objectName)
        # print('total of subs: {total}'.format(total=totalOfSubs))
        for item in self.graph.getFullGraph():
            if item != objectName:
                newValue = self.getNewValue(item, objectName, totalOfSubs)
                # print('newValue: {value}'.format(value=newValue))
                itemContainer = self.graph.getObjectByKey(item)
                boundedScalerValue = itemContainer.getScalarValue()
                boundedScalerValue += 0 if (boundedScalerValue < 0) else newValue
                itemContainer.setScalarValue(boundedScalerValue)
                if boundedScalerValue < 0:
                    itemContainer.setScalarValue(0)
                cmds.intSliderGrp(itemContainer.getSlider(), e=True, value=itemContainer.getScalarValue())
                # print('item from Container: {value}'.format(value=itemContainer))
                self.graph.updateScalerByKey(item, self.graph.getScalerByKey(item))
                cmds.scale(boundedScalerValue/100, boundedScalerValue/100, boundedScalerValue/100, item)


class FloorController(object):


    def __init__(self):
        self.ELEVATION_SLIDER_NAME  = 'Globe Elevation: '
        self.GLOBE_GEO_NAME         = 'globe'
        self.GLOBE_GEO_GROUP_NAME   = 'globeGroup'
        self.SCALE_SLIDER_NAME      = 'Globe Scale: '

        self.ELEVATION_MIN          = 0
        self.ELEVATION_MAX          = 100
        self.ELEVATION_DEFAULT      = 0

        self.GLOBE_MIN_SIZE         = 2.0
        self.GLOBE_MAX_SIZE         = 600
        self.GLOBE_DEFAULT_SIZE     = 600

        self.floorControlsLayout    = None
        self.globeEvevationSlider   = None
        self.globeScaleSlider       = None

        self.buildGlobeSphere()


    def buildGlobeSphere(self):
        globeName = cmds.polySphere(n=self.GLOBE_GEO_NAME, sx=300, sy=300)
        # objectName = globeName[0]
        # polySphereNodeName = globeName[1]
        cmds.group(self.GLOBE_GEO_NAME, n=self.GLOBE_GEO_GROUP_NAME)
        cmds.setAttr(self.GLOBE_GEO_GROUP_NAME + '.rotateZ', 90)
        cmds.move(0, 1, 0, self.GLOBE_GEO_GROUP_NAME + '.scalePivot', self.GLOBE_GEO_GROUP_NAME + '.rotatePivot', relative=True)
        cmds.setAttr(self.GLOBE_GEO_GROUP_NAME + '.translateX', 0)
        cmds.setAttr(self.GLOBE_GEO_GROUP_NAME + '.translateY', -1)
        cmds.setAttr(self.GLOBE_GEO_GROUP_NAME + '.translateZ', 0)
        cmds.setAttr(self.GLOBE_GEO_GROUP_NAME + '.scaleX', self.GLOBE_DEFAULT_SIZE)
        cmds.setAttr(self.GLOBE_GEO_GROUP_NAME + '.scaleY', self.GLOBE_DEFAULT_SIZE)
        cmds.setAttr(self.GLOBE_GEO_GROUP_NAME + '.scaleZ', self.GLOBE_DEFAULT_SIZE)


    def setGlobeSize(self, scalar):
        print('setGlobeSize with {data}'.format(data=scalar))
        cmds.setAttr(self.GLOBE_GEO_GROUP_NAME + '.scaleX', scalar)
        cmds.setAttr(self.GLOBE_GEO_GROUP_NAME + '.scaleY', scalar)
        cmds.setAttr(self.GLOBE_GEO_GROUP_NAME + '.scaleZ', scalar)


    def setElevation(self, height):
        print('setElevation with {data}'.format(data=height))
        elevation = height * -1
        cmds.setAttr(self.GLOBE_GEO_GROUP_NAME + '.translateY', elevation)


    def createFloorControls(self, parentLayout):
        print('Creating Floor Controls')
        self.floorControlsLayout = cmds.rowColumnLayout(numberOfColumns=2,
                                   columnWidth=[(1, 250), (2, 250)],
                                   columnOffset=[(2, 'both', 5), (2, 'both', 5)],
                                   parent=parentLayout)

        columnLayout = cmds.columnLayout(parent=parentLayout)

        cmds.floatSliderGrp(label=self.SCALE_SLIDER_NAME,
                            field=True,
                            minValue=self.GLOBE_MIN_SIZE,
                            maxValue=self.GLOBE_MAX_SIZE,
                            fieldMinValue=self.GLOBE_MIN_SIZE,
                            fieldMaxValue=self.GLOBE_MAX_SIZE,
                            value=self.GLOBE_DEFAULT_SIZE,
                            parent=columnLayout,
                            dc=self.setGlobeSize)

        cmds.floatSliderGrp(label=self.ELEVATION_SLIDER_NAME,
                            field=True,
                            minValue=-self.ELEVATION_MIN,
                            maxValue=self.ELEVATION_MAX,
                            fieldMinValue=self.ELEVATION_MIN,
                            fieldMaxValue=self.ELEVATION_MAX,
                            value=self.ELEVATION_DEFAULT,
                            parent=columnLayout,
                            dc=self.setElevation)


class CameraController(object):


    def __init__(self):
        self.CAMERA_NAME                = 'mainCam'
        self.CAMERA_CENTER_SLIDER_NAME  = 'Center Position: '
        self.CAMERA_ZOOM_SLIDER_NAME    = 'Camera Zoom: '

        self.CENTER_MIN                 = -20
        self.CENTER_MAX                 = 5
        self.CENTER_DEFAULT             = 4.5

        self.ZOOM_MIN                   = -150
        self.ZOOM_MAX                   = 150
        self.ZOOM_DEFAULT               = 0
        self.zoomPrev                   = 0

        self.buildMainCamera()


    def setCameraCenter(self, position):
        print('Camera center: {data}'.format(data=position))
        cmds.setAttr(self.CAMERA_NAME + '1_aim.translateY', position)


    def setCameraZoom(self, zoomLevel):
        print('Camera zoom: {data}'.format(data=zoomLevel))
        cmds.select(self.CAMERA_NAME + '1')
        moveValue = self.zoomPrev - zoomLevel
        cmds.move(0, 0, moveValue, relative=True, objectSpace=True, worldSpaceDistance=True)
        self.zoomPrev = zoomLevel


    def buildMainCamera(self):
        print('Building Main Camera')
        cmds.camera(name=self.CAMERA_NAME,
                    centerOfInterest=5,
                    focalLength=35,
                    lensSqueezeRatio=1,
                    cameraScale=1,
                    horizontalFilmAperture=1.41732,
                    horizontalFilmOffset=0,
                    verticalFilmAperture=0.94488,
                    verticalFilmOffset=0,
                    filmFit='Fill',
                    overscan=1,
                    motionBlur=0,
                    shutterAngle=144,
                    nearClipPlane=0.1,
                    farClipPlane=10000,
                    orthographic=0,
                    orthographicWidth=30,
                    panZoomEnabled=0,
                    horizontalPan=0,
                    verticalPan=0,
                    zoom=1)
        mel.objectMoveCommand()
        mel.cameraMakeNode(2, "")
        cmds.setAttr(self.CAMERA_NAME + '1.translateX', 119)
        cmds.setAttr(self.CAMERA_NAME + '1.translateY', 114)
        cmds.setAttr(self.CAMERA_NAME + '1.translateZ', 124)

        cmds.setAttr(self.CAMERA_NAME + '1.scaleX', 20)
        cmds.setAttr(self.CAMERA_NAME + '1.scaleY', 20)
        cmds.setAttr(self.CAMERA_NAME + '1.scaleZ', 20)

        cmds.setAttr(self.CAMERA_NAME + '1_aim.translateY', self.CENTER_DEFAULT)
        cmds.setAttr(self.CAMERA_NAME + '1_aim.translateZ', 0)

        cmds.setAttr(self.CAMERA_NAME + 'Shape1.focalLength', 300)


    def createCameraControls(self, parentLayout):
        print('Creating Camera Controls...')
        columnLayout = cmds.columnLayout(parent=parentLayout)

        cmds.floatSliderGrp(label=self.CAMERA_CENTER_SLIDER_NAME,
                            field=True,
                            minValue=self.CENTER_MIN,
                            maxValue=self.CENTER_MAX,
                            fieldMinValue=self.CENTER_MIN,
                            fieldMaxValue=self.CENTER_MAX,
                            value=self.CENTER_DEFAULT,
                            parent=columnLayout,
                            cc=self.setCameraCenter,
                            dc=self.setCameraCenter)

        cmds.floatSliderGrp(label=self.CAMERA_ZOOM_SLIDER_NAME,
                            field=True,
                            minValue=self.ZOOM_MIN,
                            maxValue=self.ZOOM_MAX,
                            fieldMinValue=self.ZOOM_MIN,
                            fieldMaxValue=self.ZOOM_MAX,
                            value=self.ZOOM_DEFAULT,
                            parent=columnLayout,
                            dc=self.setCameraZoom)


class Context(object):


    def __init__(self):
        self.SIZE                   = (500, 600)
        self.TITLE                  = 'Scene Controller'
        self.WINDOW                 = 'sceneControllerUI'
        # self.cameraController       = CameraController()
        # self.floorController        = FloorController()
        # self.subjectController      = SubjectController()
        self.subjectController      = SubjectControllerV2()

        if cmds.window(self.WINDOW, exists=True):
            print
            'window exist: ' + self.WINDOW
            cmds.deleteUI(self.WINDOW, window=True)

        self.WINDOW = cmds.window(self.WINDOW, title=self.TITLE, widthHeight=self.SIZE)
        # print("creating window...")

        self.main_layout = cmds.columnLayout(adjustableColumn=True)
        cmds.separator(height=20)
        cmds.text(self.TITLE)
        cmds.separator(height=20)

        self.run()

        cmds.showWindow(self.WINDOW)


    def run(self):
        # self.cameraController.createCameraControls(parentLayout=self.main_layout)
        # self.floorController.createFloorControls(parentLayout=self.main_layout)
        self.subjectController.createSubjectControls(parentLayout=self.main_layout)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    Context()
