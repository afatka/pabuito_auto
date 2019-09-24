"""
Pabuito Auto Script

MCR Objects Named

This script contains a auto script for the Pabuito Grade Tool. 
This tool searches for node names containing default names, 
as stored in a default name list.


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

def MCR_ObjectNamed(xmlDefaults, *args):

	maximum_default_names = 3

	gradeValue = {'Aplus': int(xmlDefaults.find('gradeValue').find('Aplus').text),
				'F': int(xmlDefaults.find('gradeValue').find('F').text),
				}


	development = False
	if development:
		print 'MCR Objects Named running'

	gMainProgressBar = maya.mel.eval('$tmp = $gMainProgressBar')

	cmds.progressBar( gMainProgressBar,
					edit=True,
					beginProgress=True,
					isInterruptable=True,
					status='Checking for default names',
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
	hasDefaultName = utils.compareDefaultNames(sortedNodes)

	if development:
		print 'hasDefaultName: {}'.format(hasDefaultName)
	
	cmds.progressBar(gMainProgressBar, edit=True, step=step)
	print "Default Names Automation Successful!"
	if len(hasDefaultName) > maximum_default_names:
		tempDict = {
					'grade_value':gradeValue['F'],
					'comment_text':'',
					'default_comments_text':'Default names detected.',
					'example_comments_text':''}
	else:
		tempDict = {
					'grade_value':gradeValue['Aplus'],
					'comment_text':'',
					'default_comments_text':'No default names found. Good job!',
					'example_comments_text':''}

	cmds.progressBar(gMainProgressBar, edit=True, step=step)
	
	
	cmds.progressBar(gMainProgressBar, edit=True, endProgress=True)
	return tempDict



