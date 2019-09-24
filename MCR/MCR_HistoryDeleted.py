"""
Pabuito Auto Script

MCR History Deleted

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

def MCR_HistoryDeleted(xmlDefaults, *args):

	output_comment = 'Objects have Construction History.'

	# tell which box is missed
	#gut check?
	#width / two rows of tabs?


	gradeValue = {'Aplus': int(xmlDefaults.find('gradeValue').find('Aplus').text),
				'C': int(xmlDefaults.find('gradeValue').find('C').text),
				'F': int(xmlDefaults.find('gradeValue').find('F').text),
				'F-': int(xmlDefaults.find('gradeValue').find('F-').text),
				}
	development = True
	if development:
		print 'MCR History Deleted running'

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
	hasHistory = utils.historyFinder(sortedNodes)

	if development:
		print 'hasHistory: {}'.format(hasHistory)
	
	try:
		percent_w_history = int((100 * (float(len(hasHistory))/float(len(sortedNodes)))))
		print('HasH: {}\nTotalNodes: {}'.format(len(hasHistory), len(sortedNodes)))
		print('%wH: {}'.format(percent_w_history))
	except ZeroDivisionError:
		percent_w_history = 0
	output_comment = '{}% of {}'.format(percent_w_history, output_comment)

	cmds.progressBar(gMainProgressBar, edit=True, step=step)

	print "Delete History Automation Successful!"
	if percent_w_history > 50:
		tempDict = {
					'grade_value':gradeValue['F-'],
					'comment_text':'',
					'default_comments_text':output_comment,
					'example_comments_text':''}
	elif percent_w_history > 15:
		tempDict = {
					'grade_value':gradeValue['F'],
					'comment_text':'',
					'default_comments_text':output_comment,
					'example_comments_text':''}
	elif percent_w_history > 5:
		tempDict = {
					'grade_value':gradeValue['C'],
					'comment_text':'',
					'default_comments_text':output_comment,
					'example_comments_text':''}
	else:
		tempDict = {
					'grade_value':gradeValue['Aplus'],
					'comment_text':'',
					'default_comments_text': (output_comment + ' Good Job!') ,
					'example_comments_text':''}

	cmds.progressBar(gMainProgressBar, edit=True, step=step)
	
	
	cmds.progressBar(gMainProgressBar, edit=True, endProgress=True)
	return tempDict



