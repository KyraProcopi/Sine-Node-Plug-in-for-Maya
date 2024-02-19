from PySide2 import QtWidgets
from shiboken2 import wrapInstance
from maya import cmds, OpenMayaUI
import sys

#Global Variables 
main_channelbox_name = "mainChannelBox"
node_data_code = "main_channelbox_name = " + """'mainChannelBox'"""

#Change channel BG box color
def channelBoxColorOverride(code):
    
    #Find pyside widget
    channelbox_widget = wrapInstance(int(OpenMayaUI.MQtUtil.findControl(main_channelbox_name)),QtWidgets.QWidget)
    selected_attributes = cmds.channelBox(main_channelbox_name, q=True, sma=True)
    
    #Script Node
    if cmds.objExists("channelColorData"):
        channelBoxColorsData = "channelColorData"
    else:
        channelBoxColorsData = cmds.scriptNode(n="channelColorData", st=1)
        cmds.setAttr("channelColorData.sourceType", 1)
    
    #Change Color
    def color_change(selected_attribute):
        cmds.channelBox(
        main_channelbox_name,
        edit=True,
        attrRegex=(selected_attribute),
        attrBgColor=values
        )
        color_data = ("cmds.channelBox(" +
            "main_channelbox_name," +
            "edit=True," +
            """attrRegex='{}',""".format(selected_attribute) +
            """attrBgColor={})""".format(values)+ """\n""") 
        color_data_code = str(color_data)
        return color_data_code 
   
    if selected_attributes==None:
        sys.stderr.write("Please select attributes in channel box \n")
        return
        
    else:
        #Color Editor 
        cmds.colorEditor()
        if cmds.colorEditor(query=True, result=True):
            values = cmds.colorEditor(query=True, rgb=True)  
            #Loop through 
            color_output = str()
            color_data = color_output.join(color_change(attr)for attr in selected_attributes)

        else:
            sys.stderr.write("Editor was dismissed \n")
            return
                      
    #Plug Code intro Script Node 
    if cmds.objExists("channelColorData"):
        code = cmds.scriptNode("channelColorData", bs=True, q=True)
    
    if color_data != None:
        try:
            code += "\n" + color_data
            cmds.scriptNode("channelColorData", edit=True, bs=code)
            
        except:
            code = node_data_code + "\n" + color_data
            cmds.scriptNode("channelColorData", edit=True, bs=code)
                          
#Select Script Node
def channelColorData(code):
    if cmds.objExists("channelColorData"):
        sys.stderr.write("Node Exists \n")
        channelBoxColorsData = "channelColorData"
        cmds.select("channelColorData")
        return channelBoxColorsData
    else:
        sys.stderr.write("Script node has not been created. Please apply color overrides to create script node \n")

#Get Exsiting data         
def get_existing_data(code):
    if cmds.objExists("channelColorData"):
        code = cmds.scriptNode("channelColorData", bs=True, q=True)
        sys.stderr.write("Exisiting Override Data retrieved \n") 
        return code
    else:
        sys.stderr.write("No existing data \n")         

#Reset Overrides
def reset(code):
    if cmds.objExists("channelColorData"):
        code = node_data_code
        cmds.scriptNode("channelColorData", edit=True, bs=code)
        sys.stderr.write("Overrides restored to default. Please close Maya and re-open \n")
    
    else:
        sys.stderr.write("Script node has not been created. Please apply color overrides to create script node \n")
                
#UI
cmds.window(menuBar=True, width=255, h=50, s=False)
cmds.columnLayout( columnAttach=('both', 5), rowSpacing=10, columnWidth=250 )
cmds.button('Change Color', c=channelBoxColorOverride)
cmds.button('Select Script Node', c=channelColorData)
cmds.button('Get Existing Data', c=get_existing_data)
cmds.button('Reset All Overrides',c=reset)
cmds.showWindow()
