"""
Pabuito Auto Script

MCR Scene Layered

This script contains a auto script for the Pabuito Grade Tool. 
This tool searches objects in layers.

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
reload(utilities) 

def MCR_SceneLayered(xmlDefaults, *args):

	max_master_asseblies = 1

	gradeValue = {'Aplus': int(xmlDefaults.find('gradeValue').find('Aplus').text),
				'F': int(xmlDefaults.find('gradeValue').find('F').text),
				}


	development = True
	if development:
		print 'MCR Scene Layered running'

	gMainProgressBar = maya.mel.eval('$tmp = $gMainProgressBar')

	cmds.progressBar( gMainProgressBar,
					edit=True,
					beginProgress=True,
					isInterruptable=True,
					status='MCR_SceneLayered',
					maxValue=100 )
	step = 100/7
	cmds.progressBar(gMainProgressBar, edit=True, step=step)
	utils = utilities.utilities()
	cmds.progressBar(gMainProgressBar, edit=True, step=step)
	rootNodes = utils.masterGroupTest()
	cmds.progressBar(gMainProgressBar, edit=True, step=step)
	collectedNodes = utils.nodeCollector(rootNodes)
	cmds.progressBar(gMainProgressBar, edit=True, step=step)
	sortedNodes = utils.sortNodeList(collectedNodes, 'mesh')
	cmds.progressBar(gMainProgressBar, edit=True, step=step)
	
	fail = True
	
	displayLayers = utils.findLayers()
	initialLayerStates = utils.collectLayerState(displayLayers)
	utils.hideAllLayers(displayLayers)
	if development: 
		print('sortedNodes: {}'.format(sortedNodes))
	visibleNodes = utils.visibilityBulkTest(sortedNodes)
	utils.setLayersVisibility(displayLayers, initialLayerStates)

	if development:
		print('vis: {}'.format(visibleNodes))
	cmds.progressBar(gMainProgressBar, edit=True, step=step)
	print "Scene Layered Automation Successful!"
	if visibleNodes:
		tempDict = {
					'grade_value':gradeValue['F'],
					'comment_text':'',
					'default_comments_text':'Scene not layered correctly. ',
					'example_comments_text':''}
	else:
		tempDict = {
					'grade_value':gradeValue['Aplus'],
					'comment_text':'',
					'default_comments_text':'Scene layered correctly. Good job!',
					'example_comments_text':''}

	cmds.progressBar(gMainProgressBar, edit=True, step=step)
	
	
	cmds.progressBar(gMainProgressBar, edit=True, endProgress=True)
	return tempDict



