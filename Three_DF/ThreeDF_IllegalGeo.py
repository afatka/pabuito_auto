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
#import xml.etree.ElementTree as etree

def ThreeDF_IllegalGeo(xmlDefaults, *args):
	gradeValue = {'A': int(xmlDefaults.find('gradeValue').find('A').text),
				'B': int(xmlDefaults.find('gradeValue').find('B').text),
				'C': int(xmlDefaults.find('gradeValue').find('C').text),
				'F-': int(xmlDefaults.find('gradeValue').find('F-').text),
				}
	development = False
	if development:
		print '3DF Illegal Geo running'

	gMainProgressBar = maya.mel.eval('$tmp = $gMainProgressBar')

	cmds.progressBar( gMainProgressBar,
					edit=True,
					beginProgress=True,
					isInterruptable=True,
					status='Checking for Illegal Geo',
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



	spottedTriangles = utils.triFinder(cleanedNodes)
	# print('triangles: {}'.format(spottedTriangles))
	spottedNGons = utils.nGonFinder(cleanedNodes)
	# print('nGons: {}'.format(spottedNGons))
	spottedLamina = utils.laminaFinder(cleanedNodes)
	# print('Lamina: {}'.format(spottedLamina))
 	
 	troubleGeo = ''
 	if len(spottedTriangles[0]) != 0:
 		troubleGeo += 'Triangles'
 	if len(spottedNGons[0]) != 0:
 		if troubleGeo != '':
	 		troubleGeo += ', '
 		troubleGeo += 'NGons'
 	if len(spottedLamina[0]) != 0:
 		if troubleGeo != '':
	 		troubleGeo += ', '
 		troubleGeo += 'Lamina Faces'
	total_trouble_geo = len(spottedTriangles[1]) + len(spottedLamina[1]) + len(spottedNGons[1])

	cmds.progressBar(gMainProgressBar, edit=True, step=step)
	print "Illegal Geo Automation Successful!"
	if total_trouble_geo >= 11 and troubleGeo != '':
		tempDict = {
					'grade_value':gradeValue['F-'],
					'comment_text':'',
					'default_comments_text':'Illegal Geometry detected. Detected geometry includes {}.'.format(troubleGeo),
					'example_comments_text':''}
	elif 6 <= total_trouble_geo <= 10 and troubleGeo != '':
		tempDict = {
					'grade_value':gradeValue['C'],
					'comment_text':'',
					'default_comments_text':'Illegal Geometry detected. Detected geometry includes {}.'.format(troubleGeo),
					'example_comments_text':''}
	elif 1 <= total_trouble_geo <= 5 and troubleGeo != '':
		tempDict = {
					'grade_value':gradeValue['B'],
					'comment_text':'',
					'default_comments_text':'Illegal Geometry detected. Detected geometry includes {}.'.format(troubleGeo),
					'example_comments_text':''}
	else:
		tempDict = {
					'grade_value':gradeValue['A'],
					'comment_text':'',
					'default_comments_text':'No Illegal Geometry found. Good job!',
					'example_comments_text':''}

	cmds.progressBar(gMainProgressBar, edit=True, step=step)
	
	
	cmds.progressBar(gMainProgressBar, edit=True, endProgress=True)
	return tempDict



