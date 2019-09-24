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

def ThreeDF_PivotPlacement(xmlDefaults, *args):
	gradeValue = {'A': int(xmlDefaults.find('gradeValue').find('A').text),
				'F-': int(xmlDefaults.find('gradeValue').find('F-').text),
				}

	offset = 0.1 #margin of error / tolerance

	development = True
	if development:
		print '3DF Pivot Placement running'

	gMainProgressBar = maya.mel.eval('$tmp = $gMainProgressBar')

	cmds.progressBar( gMainProgressBar,
					edit=True,
					beginProgress=True,
					isInterruptable=True,
					status='Checking History',
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
	pivotNotOrigin = []
	
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

	for node in cleanedNodes:
		print('position: {}'.format(cmds.xform(node, worldSpace=1, query=1, rotatePivot=1)))
		clean_position = [round(num, 2) for num in cmds.xform(node, worldSpace=1, query=1, rotatePivot=1)]
		print('clean pos: {}'.format(clean_position))
		if  not ([-offset, -offset, -offset] <= clean_position <= [offset, offset, offset]):
			pivotNotOrigin.append(node)

	if development:
		print 'pivotNotOrigin: {}'.format(pivotNotOrigin)
	


	cmds.progressBar(gMainProgressBar, edit=True, step=step)
	print "Pivot Placement Automation Successful!"
	if pivotNotOrigin:
		tempDict = {
					'grade_value':gradeValue['F-'],
					'comment_text':'',
					'default_comments_text':'Pivots are not at the origin.',
					'example_comments_text':''}
	else:
		tempDict = {
					'grade_value':gradeValue['A'],
					'comment_text':'',
					'default_comments_text':'Pivot properly placed. Good job!',
					'example_comments_text':''}

	cmds.progressBar(gMainProgressBar, edit=True, step=step)
	
	
	cmds.progressBar(gMainProgressBar, edit=True, endProgress=True)
	return tempDict



