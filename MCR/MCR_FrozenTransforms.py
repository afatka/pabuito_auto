"""
Pabuito Auto Script

MCR Frozen Transforms

This script contains a auto script for the Pabuito Grade Tool. 
This tool searches for transforms on all transforms in the scene.

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

def MCR_FrozenTransforms(xmlDefaults, *args):
	gradeValue = {'Aplus': int(xmlDefaults.find('gradeValue').find('Aplus').text),
				'F': int(xmlDefaults.find('gradeValue').find('F').text),
				}

	development = True
	if development:
		print 'MCR Frozen Transforms running'

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
	
	cleanedNodes = []
	if hasTransforms:
		for node in hasTransforms:
			# print ('node: {}'.format(node))
			try:
				if cmds.listRelatives(node):
					# print('listRelatives(node): {}'.format(cmds.listRelatives(node)))
					f_type = cmds.nodeType(cmds.listRelatives(node, path = True)[0])
					if f_type not in ('imagePlane', 'camera'):
						cleanedNodes.append(node)
			except RuntimeError:
				cmds.warning('RuntimeError Occurred - Adding node anyway...')
				cmds.warning('Problematic node: {}'.format(node))
				cleanedNodes.append(node)

	redFlagNodes = []

	for node in cleanedNodes:
		# print('checking node: {}'.format(node))
		# print('Relatives: {}'.format(cmds.listRelatives(node)))
		if cmds.listRelatives(node) != None:
			if len(cmds.listRelatives(node)) <= 2:
				# print('{} has <= 1 relatives'.format(node))
				# print('Relatives: {}'.format(cmds.listRelatives(node)))
				for relative in cmds.listRelatives(node, path = True):
					if cmds.nodeType(relative) not in ('transform', 'shape'):
						# print ('Red Flag!: {}'.format(node))
						if node not in redFlagNodes:
							redFlagNodes.append(node)

	if len(redFlagNodes):
		# print('red flag nodes!!!\n{}'.format(redFlagNodes))
		for node in redFlagNodes:
			# print('removing node: {}'.format(node))
			cleanedNodes.remove(node)

	if development:
		print 'cleanedNodes: {}'.format(cleanedNodes)


	cmds.progressBar(gMainProgressBar, edit=True, step=step)
	print "Frozen Transforms Automation Successful!"
	if cleanedNodes:
		# if development:
		# 	print cleanedNodes
		tempDict = {
					'grade_value':gradeValue['F'],
					'comment_text':'',
					'default_comments_text':'Object has non frozen transforms.',
					'example_comments_text':''}
	else:
		tempDict = {
					'grade_value':gradeValue['Aplus'],
					'comment_text':'',
					'default_comments_text':'Transforms Frozen! Good job!',
					'example_comments_text':''}

	cmds.progressBar(gMainProgressBar, edit=True, step=step)
	
	
	cmds.progressBar(gMainProgressBar, edit=True, endProgress=True)
	return tempDict



