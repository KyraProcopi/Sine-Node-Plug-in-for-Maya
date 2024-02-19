'''
Sine Node v1.0
By Kyra Procopi 
'''
import sys
import math
from maya.api import OpenMaya

# Unique id
kPluginNodeTypeName = "SineNodeKP"
SineNodeId = OpenMaya.MTypeId(0x24171)
# Specify API
def maya_useNewAPI():
    pass
# Sine Node Class
class SineNode(OpenMaya.MPxNode):

    # Inputs
    input = OpenMaya.MObject()
    m_time = OpenMaya.MObject()
    amplitude = OpenMaya.MObject()
    offset = OpenMaya.MObject()
    
    # Outputs
    output = OpenMaya.MObject()

    def __init__(self):
        super(SineNode, self).__init__()

    def compute(self, plug, dataBlock):

        if (plug == SineNode.output):

            input_value = dataBlock.inputValue(SineNode.input).asFloat()
            output_value = dataBlock.outputValue(SineNode.output)
            output_value.setFloat(input_value * 2.0)

            amplitudeValue = dataBlock.inputValue(SineNode.amplitude).asFloat()
            offsetValue = dataBlock.inputValue(SineNode.offset).asFloat()

            sinResult = amplitudeValue * math.sin(offsetValue * input_value)
            sinHandle = dataBlock.outputValue(SineNode.output)
            sinHandle.setFloat(sinResult)

            dataBlock.setClean(plug)


# creator
def nodeCreator():
    return SineNode()


# Initializer
def nodeInitializer():

    nAttr = OpenMaya.MFnNumericAttribute()
    eAttr = OpenMaya.MFnNumericAttribute()
    tAttr = OpenMaya.MFnUnitAttribute()

    # Create Inputs
    # input Attribute
    SineNode.m_time = tAttr.create(
        'time', 'time', OpenMaya.MFnUnitAttribute.kTime, 0.0)
    OpenMaya.MPxNode.addAttribute(SineNode.m_time)

    SineNode.input = nAttr.create(
        "inputValue", "in", OpenMaya.MFnNumericData.kFloat, 0.0)
    nAttr.keyable = True
    nAttr.storable = True
    nAttr.readable = True
    nAttr.writable = True
    OpenMaya.MPxNode.addAttribute(SineNode.input)

    # Amplitude Attribute
    SineNode.amplitude = nAttr.create(
        "amplitude", "amp", OpenMaya.MFnNumericData.kFloat, 1.0)
    nAttr.keyable = True
    nAttr.storable = True
    nAttr.readable = True
    nAttr.writable = True
    OpenMaya.MPxNode.addAttribute(SineNode.amplitude)

    #Offset Attribute
    SineNode.offset = nAttr.create(
        "offset", "off", OpenMaya.MFnNumericData.kFloat, 1.0)
    nAttr.keyable = True
    nAttr.storable = True
    nAttr.readable = True
    nAttr.writable = True
    OpenMaya.MPxNode.addAttribute(SineNode.offset)

 # Create Outputs
    SineNode.output = nAttr.create(
        "outputValue", "out", OpenMaya.MFnNumericData.kFloat, 0.0)
    nAttr.storable = True
    OpenMaya.MPxNode.addAttribute(SineNode.output)

    # attribute affects
    OpenMaya.MPxNode.attributeAffects(SineNode.input, SineNode.output)
    OpenMaya.MPxNode.attributeAffects(SineNode.amplitude, SineNode.output)
    OpenMaya.MPxNode.attributeAffects(SineNode.m_time, SineNode.output)
    OpenMaya.MPxNode.attributeAffects(SineNode.offset, SineNode.output)


# Create plug-in
def initializePlugin(mobject):

    mplugin = OpenMaya.MFnPlugin(mobject)

    try:
        mplugin.registerNode(
            kPluginNodeTypeName, SineNodeId, nodeCreator, nodeInitializer)
    except:
        sys.stderr.write("Failed to register node: %s" % kPluginNodeTypeName)
        raise


# Uninitialize the script plug-in
def uninitializePlugin(mobject):

    mplugin = OpenMaya.MFnPlugin(mobject)

    try:
        mplugin.deregisterNode(SineNodeId)
    except:
        sys.stderr.write("Failed to deregister node: %s" % kPluginNodeTypeName)
        raise
