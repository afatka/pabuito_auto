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

def ThreeDF_Scale(xmlDefaults, *args):
	gradeValue = {'A': int(xmlDefaults.find('gradeValue').find('A').text),
				'F-': int(xmlDefaults.find('gradeValue').find('F-').text),
				}

	defaultMaxWidth = 8
	defaultMinWidth = 4

	if xmlDefaults.find('scale') != None:
		print('Scale found')
		scale_value = xmlDefaults.find('scale').text
		print('scale value: {}'.format(scale_value))
		values = [int(x) for x in scale_value.split(',')]
		if len(values) == 2:
			defaultMinWidth = values[0]
			defaultMaxWidth = values[1]
			print('min: {}\nmax: {}'.format(defaultMinWidth, defaultMaxWidth))
	
	hydrantShotgunMaxWidth = 7
	hydrantShotgunMinWidth = 4

	chairMaxWidth = 8
	chairMinidth = 6


	development = False
	if development:
		print '3DF Scale running'

	gMainProgressBar = maya.mel.eval('$tmp = $gMainProgressBar')

	cmds.progressBar( gMainProgressBar,
					edit=True,
					beginProgress=True,
					isInterruptable=True,
					status='Checking Scale',
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

	scaleWonky = []
	for node in cleanedNodes:
		
		xmin, ymin, zmin, xmax, ymax, zmax = cmds.xform(node, worldSpace=1, query=1, boundingBox = True)
		if 'hydrant'.lower() in node.lower() or 'shotgun'.lower() in node.lower():
			if not any(hydrantShotgunMinWidth <= x <= hydrantShotgunMaxWidth for x in ((abs(xmax - abs(xmin))),(abs(zmax - abs(zmin))), (abs(ymax - abs(ymin))))):
				scaleWonky.append(node)
				break
		elif 'chair'.lower() in node.lower():
			if not any(chairMinidth <= x <= chairMaxWidth for x in ((abs(xmax - abs(xmin))),(abs(zmax - abs(zmin))), (abs(ymax - abs(ymin))))):
				if node not in scaleWonky:
					scaleWonky.append(node)
					break
		else:
			if not any(defaultMinWidth <= x <= defaultMaxWidth for x in ((abs(xmax - abs(xmin))),(abs(zmax - abs(zmin))), (abs(ymax - abs(ymin))))):
				if node not in scaleWonky:
					scaleWonky.append(node)



	if development:
		print 'ScaleWonky: {}'.format(scaleWonky)
	


	cmds.progressBar(gMainProgressBar, edit=True, step=step)
	print "Scale Automation Successful!"
	if scaleWonky:
		tempDict = {
					'grade_value':gradeValue['F-'],
					'comment_text':'',
					'default_comments_text':'Scale not in line with expectations.',
					'example_comments_text':''}
	else:
		tempDict = {
					'grade_value':gradeValue['A'],
					'comment_text':'',
					'default_comments_text':'Scale in line with expectations. Good job!',
					'example_comments_text':''}

	cmds.progressBar(gMainProgressBar, edit=True, step=step)
	
	
	cmds.progressBar(gMainProgressBar, edit=True, endProgress=True)
	return tempDict



