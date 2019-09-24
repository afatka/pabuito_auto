"""
Pabuito Auto Script

MCR History Deleted

This script contains a auto script for the Pabuito Grade Tool. 
This tool searches centered pivots on all transform nodes.

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

def MCR_PivotPlacement(xmlDefaults, *args):

	maximum_pivots_NOT_centered = 0

	gradeValue = {'Aplus': int(xmlDefaults.find('gradeValue').find('Aplus').text),
				'F': int(xmlDefaults.find('gradeValue').find('F').text),
				}


	development = True
	if development:
		print 'MCR Pivot Placement running'

	gMainProgressBar = maya.mel.eval('$tmp = $gMainProgressBar')

	cmds.progressBar( gMainProgressBar,
					edit=True,
					beginProgress=True,
					isInterruptable=True,
					status='MCR_PivotPlacement',
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
	pivotsNotCentered = utils.pivotsCentered(sortedNodes)

	if development:
		print 'pivotsNotCentered: {}'.format(pivotsNotCentered)
	


	cmds.progressBar(gMainProgressBar, edit=True, step=step)
	print "Pivot Placement Automation Successful!"
	if len(pivotsNotCentered) > maximum_pivots_NOT_centered:
		tempDict = {
					'grade_value':gradeValue['F'],
					'comment_text':'',
					'default_comments_text':'Pivots are not centered.',
					'example_comments_text':''}
	else:
		tempDict = {
					'grade_value':gradeValue['Aplus'],
					'comment_text':'',
					'default_comments_text':'Pivot properly placed. Good job!',
					'example_comments_text':''}

	cmds.progressBar(gMainProgressBar, edit=True, step=step)
	
	
	cmds.progressBar(gMainProgressBar, edit=True, endProgress=True)
	return tempDict



