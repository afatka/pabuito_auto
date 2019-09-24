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

def ThreeDF_FrozenTransforms(xmlDefaults, *args):
	gradeValue = {'A': int(xmlDefaults.find('gradeValue').find('A').text),
				'F-': int(xmlDefaults.find('gradeValue').find('F-').text),
				}

	development = True
	if development:
		print '3DF Frozen Transforms running'

	gMainProgressBar = maya.mel.eval('$tmp = $gMainProgressBar')

	cmds.progressBar( gMainProgressBar,
					edit=True,
					beginProgress=True,
					isInterruptable=True,
					status='Checking Transforms',
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
	hasTransforms = utils.frozenTransforms(sortedNodes)

	if development:
		print 'hasTransforms: {}'.format(hasTransforms)
	
	cleanedNodes = []
	# print('here\n\n')
	if hasTransforms:
		for node in hasTransforms:
			# print('node: {}'.format(node))
			if cmds.nodeType(cmds.listRelatives(node, fullPath = 1)) != None:
				try:
					if cmds.nodeType(cmds.listRelatives(node, fullPath = 1)[0]) != 'imagePlane':
						cleanedNodes.append(node)
				except RuntimeError:
					cmds.warning('RuntimeError Occurred - Adding node anyway...')
					cleanedNodes.append(node)
			else:
				cleanedNodes.append(node)


	cmds.progressBar(gMainProgressBar, edit=True, step=step)
	print "Frozen Transforms Automation Successful!"
	if cleanedNodes:
		tempDict = {
					'grade_value':gradeValue['F-'],
					'comment_text':'',
					'default_comments_text':'Object has non frozen transforms.',
					'example_comments_text':''}
	else:
		tempDict = {
					'grade_value':gradeValue['A'],
					'comment_text':'',
					'default_comments_text':'Transforms Frozen! Good job!',
					'example_comments_text':''}

	cmds.progressBar(gMainProgressBar, edit=True, step=step)
	
	
	cmds.progressBar(gMainProgressBar, edit=True, endProgress=True)
	return tempDict



