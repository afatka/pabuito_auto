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

def ThreeDF_ObjectPlacement(xmlDefaults, *args):
	gradeValue = {'A': int(xmlDefaults.find('gradeValue').find('A').text),
				'F-': int(xmlDefaults.find('gradeValue').find('F-').text),
				}



	yDisplacementMax = 0.5
	yLowerLimit = -0.25
	xzDisplacementMax = 2

	development = False
	if development:
		print '3DF Object PLacement running'

	gMainProgressBar = maya.mel.eval('$tmp = $gMainProgressBar')

	cmds.progressBar( gMainProgressBar,
					edit=True,
					beginProgress=True,
					isInterruptable=True,
					status='Checking Object Placement',
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
	outOfPlace = []
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
		# print 'node is: {}'.format(node)			
		xmin, ymin, zmin, xmax, ymax, zmax = cmds.xform(node, worldSpace=1, query=1, boundingBox = True)
		if  not ( yLowerLimit < ymin < yDisplacementMax):
			outOfPlace.append(node)
		if (abs(xmax - abs(xmin)) > xzDisplacementMax) or (abs(zmax - abs(zmin)) > xzDisplacementMax):
			if node not in outOfPlace:
				outOfPlace.append(node)

	if development:
		print 'objectPlacement: {}'.format(outOfPlace)
	
	cmds.progressBar(gMainProgressBar, edit=True, step=step)
	print "Object Placement Automation Successful!"
	if outOfPlace:
		tempDict = {
					'grade_value':gradeValue['F-'],
					'comment_text':'',
					'default_comments_text':'Object placement needs refinement.',
					'example_comments_text':''}
	else:
		tempDict = {
					'grade_value':gradeValue['A'],
					'comment_text':'',
					'default_comments_text':'Object placed correctly. Good job!',
					'example_comments_text':''}

	cmds.progressBar(gMainProgressBar, edit=True, step=step)
	
	
	cmds.progressBar(gMainProgressBar, edit=True, endProgress=True)
	return tempDict



