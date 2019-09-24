"""
Pabuito Auto Script

MCR Optional - F 

This script contains a auto script for the Pabuito Grade Tool. 
This tool searches for history on all transform nodes.


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

def MCR_OptionalF(xmlDefaults, *args):


	gradeValue = {'A': int(xmlDefaults.find('gradeValue').find('A').text),
				'F-': int(xmlDefaults.find('gradeValue').find('F-').text),
				}
	development = True
	if development:
		print 'MCR Optional F running'

	gMainProgressBar = maya.mel.eval('$tmp = $gMainProgressBar')

	cmds.progressBar( gMainProgressBar,
					edit=True,
					beginProgress=True,
					isInterruptable=True,
					status='Optional F',
					maxValue=100 )
	
	

	cmds.progressBar(gMainProgressBar, edit=True, step=50)
	print "Optional F Automation Successful!"
	tempDict = {
				'grade_value':gradeValue['F-'],
				'comment_text':'',
				'default_comments_text':'',
				'example_comments_text':''}
	
	cmds.progressBar(gMainProgressBar, edit=True, step=50)
	
	
	cmds.progressBar(gMainProgressBar, edit=True, endProgress=True)
	return tempDict



