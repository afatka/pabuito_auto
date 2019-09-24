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

def ThreeDF_Polycount(xmlDefaults, *args):
	gradeValue = {'A': int(xmlDefaults.find('gradeValue').find('A').text),
				'F-': int(xmlDefaults.find('gradeValue').find('F-').text),
				}
	#print('polycount: {}'.format(xmlDefaults.find('polycount')))

	polygon_lower_limit = 300
	polygon_excel_lower_limit = 480
	polygon_upper_limit = 500

	if xmlDefaults.find('polycount') != None:
		polycount_value = xmlDefaults.find('polycount').text
		#print(polycount_value)
		values = [int(x) for x in polycount_value.split(',')]
		#print(values)
		if len(values) == 3:
			polygon_lower_limit = values[0]
			polygon_excel_lower_limit = values[1]
			polygon_upper_limit = values[2]

	#print('polygon_lower_limit: {}\npolygon_excel_lower: {}\npolygon_upper_limit: {}'.format(polygon_lower_limit, polygon_excel_lower_limit, polygon_upper_limit))

	good_comment = "Polycount is within range! Good Job!"
	great_comment = "Excellent job utilizing your poly budget! Great work!"
	tooLow_comment = "Your poly budget allowed for many more polygons. Try to use all the polygons you are able to polish the model."
	tooHigh_comment = "You've exceeded your poly budget! In production this can lead to slow run times or longer renders! Oh no!"

	development = False

	if development:
		print '3DF Polycount running'

	gMainProgressBar = maya.mel.eval('$tmp = $gMainProgressBar')

	cmds.progressBar( gMainProgressBar,
					edit=True,
					beginProgress=True,
					isInterruptable=True,
					status='Counting Polycount',
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
	
	if development:
		print('sortedNodes: {}'.format(sortedNodes))

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




	if development:
		print('cleanedNodes: {}'.format(cleanedNodes))

	polyCount = 0
	for node in cleanedNodes:
		try:
			#print('\n\n')
			#print(cmds.polyEvaluate(node, face = True))
			polyCount += int(cmds.polyEvaluate(node, face = True))
		except ValueError:
			pass

	if development:
		print 'Number of polys: {}'.format(polyCount)
	
	if polygon_lower_limit <= polyCount <= polygon_upper_limit:
		comment = good_comment
		fail = False
	elif polyCount < polygon_lower_limit:
		comment = tooLow_comment
		fail = True
	else:
		comment = tooHigh_comment
		fail = True
	if polygon_excel_lower_limit <= polyCount <= polygon_upper_limit:
		comment = great_comment
		fail = False


	cmds.progressBar(gMainProgressBar, edit=True, step=step)
	print "Polycount Automation Successful!"
	if fail:
		#print 'fail'
		tempDict = {
					'grade_value':gradeValue['F-'],
					'comment_text':'',
					'default_comments_text':comment,
					'example_comments_text':''}
	else:
		tempDict = {
					'grade_value':gradeValue['A'],
					'comment_text':'',
					'default_comments_text':comment,
					'example_comments_text':''}

	cmds.progressBar(gMainProgressBar, edit=True, step=step)
	
	
	cmds.progressBar(gMainProgressBar, edit=True, endProgress=True)
	return tempDict



