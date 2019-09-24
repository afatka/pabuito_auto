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

def ThreeDF_Seamless(xmlDefaults, *args):
	gradeValue = {'A': int(xmlDefaults.find('gradeValue').find('A').text),
				'F-': int(xmlDefaults.find('gradeValue').find('F-').text),
				}

	development = False
	if development:
		print '3DF Seamless Check running'

	gMainProgressBar = maya.mel.eval('$tmp = $gMainProgressBar')

	cmds.progressBar( gMainProgressBar,
					edit=True,
					beginProgress=True,
					isInterruptable=True,
					status='Checking Seamless',
					maxValue=100 )
	step = 100/7
	cmds.progressBar(gMainProgressBar, edit=True, step=step)
	utils = utilities.utilities()
	cmds.progressBar(gMainProgressBar, edit=True, step=step)
	rootNodes = utils.masterGroupTest()
	cmds.progressBar(gMainProgressBar, edit=True, step=step)
	collectedNodes = utils.nodeCollector(rootNodes)
	cmds.progressBar(gMainProgressBar, edit=True, step=step)
	sortedNodes = utils.sortNodeList(collectedNodes, 'transform')
	cmds.progressBar(gMainProgressBar, edit=True, step=step)
	
	cleanedNodes = []

	for node in sortedNodes:
		try:
			if cmds.nodeType(cmds.listRelatives(node)[0]) != 'imagePlane':
				cleanedNodes.append(node)
		except RuntimeError:
			cmds.warning('RuntimeError Occurred - Adding node anyway...')
			cleanedNodes.append(node)
		except TypeError:
			pass


	
	storeSelection = cmds.ls(selection = True)
	cmds.select(clear = True)

	for node in cleanedNodes:
		cmds.select(node, add = True)
	cmds.polySelectConstraint(type = 0x8000, mode = 3, where = 1)
	borderEdges = cmds.ls(selection = True)

	cmds.polySelectConstraint(disable = True)
	cmds.select(clear = True)
	for node in storeSelection:
		cmds.select(node, add = True)


	cmds.progressBar(gMainProgressBar, edit=True, step=step)
	print "Seamless Check Automation Successful!"
	if borderEdges:
		tempDict = {
					'grade_value':gradeValue['F-'],
					'comment_text':'',
					'default_comments_text':'Border Edges detected. Model not seamless.',
					'example_comments_text':''}
	else:
		tempDict = {
					'grade_value':gradeValue['A'],
					'comment_text':'',
					'default_comments_text':'No Border Edges found. Good job!',
					'example_comments_text':''}

	cmds.progressBar(gMainProgressBar, edit=True, step=step)
	
	
	cmds.progressBar(gMainProgressBar, edit=True, endProgress=True)
	return tempDict

