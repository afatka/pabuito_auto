"""
Pabuito Auto Script

3DF History Deleted

This script contains a auto script for the Pabuito Grade Tool. This tool searches for history on a single expected mesh.


!!!
All scripts need to create a progress bar and print status to stdout
!!!
All auto scripts need to return the grade information in the form of a dictionary

return {
		'grade_value': int, 
		'comment_text':string,
		'default_comments_text':string,
		'example_comments_text':string,
		}

the comments can remain '' without effecting the tools functionality. 

Written by: Adam Fatka
adam.fatka@gmail.com

"""

import maya.cmds as cmds
import maya.mel
from pabuito_auto import utilities 

def ThreeDF_Presentation(xmlDefaults, *args):
	gradeValue = {'A': int(xmlDefaults.find('gradeValue').find('A').text),
				'F-': int(xmlDefaults.find('gradeValue').find('F-').text),
				}

	good_comment = 'Presentation in line with expectations. Good job!'
	bad_comment = 'Presentation not in line with expectations.'


	development = False
	if development:
		print '3DF Presentation Check running'

	gMainProgressBar = maya.mel.eval('$tmp = $gMainProgressBar')

	cmds.progressBar( gMainProgressBar,
					edit=True,
					beginProgress=True,
					isInterruptable=True,
					status='Checking Presentation',
					maxValue=100 )
	step = 100/7
	
	fail = False

	visiblePanelsList = cmds.getPanel(visiblePanels = True)
	modelPanelList = []
	for p in visiblePanelsList:
		if cmds.getPanel(typeOf = p) == 'modelPanel':
			modelPanelList.append(p)
	#check if in single camera mode	
	if len(modelPanelList) > 1:
		fail = True
		bad_comment += ' Make sure a single camera is set. No 4 view.'

	#check for wireframe
	for p in modelPanelList:
		if cmds.modelEditor(p, query = True, displayAppearance = True) != 'wireframe':
			fail = True
			bad_comment += ' Make sure the viewer is set to wireframe mode.'

	#check for no image planes
	if cmds.ls(exactType = 'imagePlane'):
		fail = True
		bad_comment += ' Remember to delete your image planes.'

	#scene framed
	####
	####

	#margin of error increase
	####

	for p in modelPanelList:
	    modelCam =  cmds.modelPanel(p, query = True, camera = True)
	    camStart = cmds.xform(modelCam, worldSpace = True, query = True, translation = True) 
	    cmds.viewFit(all = True)
	    camEnd = cmds.xform(modelCam, worldSpace = True, query = True, translation = True) 
	    cmds.xform(modelCam, worldSpace = True, translation = camStart)
	    roundedStart = [round(x, 12) for x in camStart]
	    roundedEnd = [round(x,12) for x in camEnd]
	    if roundedStart != roundedEnd:
	    	#fail = True 
	    	bad_comment += ' Remember to frame your scene.'
	    	good_comment += ' Remember to frame your scene.'

	cmds.progressBar(gMainProgressBar, edit=True, step=step)
	print "Presentation Check Automation Successful!"
	if fail:
		tempDict = {
					'grade_value':gradeValue['F-'],
					'comment_text':'',
					'default_comments_text':bad_comment,
					'example_comments_text':''}
	else:
		tempDict = {
					'grade_value':gradeValue['A'],
					'comment_text':'',
					'default_comments_text':good_comment,
					'example_comments_text':''}

	cmds.progressBar(gMainProgressBar, edit=True, step=step)
	
	
	cmds.progressBar(gMainProgressBar, edit=True, endProgress=True)
	return tempDict



