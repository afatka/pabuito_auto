"""
Pabuito Auto Script

MCR Scene Grouped

This script contains a auto script for the Pabuito Grade Tool. 
This tool searches for a single main assembly and sub group nodes.

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

def MCR_SceneGrouped(xmlDefaults, *args):

	max_master_asseblies = 1

	gradeValue = {'Aplus': int(xmlDefaults.find('gradeValue').find('Aplus').text),
				'F': int(xmlDefaults.find('gradeValue').find('F').text),
				}


	development = True
	if development:
		print 'MCR Scene Grouped running'

	gMainProgressBar = maya.mel.eval('$tmp = $gMainProgressBar')

	cmds.progressBar( gMainProgressBar,
					edit=True,
					beginProgress=True,
					isInterruptable=True,
					status='MCR_SceneGrouped',
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
	master_assemblies = utils.masterGroupTest()
	fail = True
	if development:
		print ('Master Assemblies: {}'.format(master_assemblies))
		for node in master_assemblies:
			print("{} is type: {}".format(node, cmds.nodeType(node)))
			print("{}'s relatives: {}".format(node,cmds.listRelatives(node, path = True)))
			if cmds.listRelatives(node, path = True) != None:
				for relative in cmds.listRelatives(node, path = True):
					print("{} is type: {}".format(relative, cmds.nodeType(relative)))
			print '\n'

	redFlagNodes = []

	for node in master_assemblies:
		# print('checking node: {}'.format(node))
		if cmds.listRelatives(node, path = True) != None:
			if len(cmds.listRelatives(node, path = True)) <= 2:
				# print('{} has <= 2 relatives'.format(node))
				# print('Relatives: {}'.format(cmds.listRelatives(node)))
				for relative in cmds.listRelatives(node, path = True):
					print('checking relative: {}: type: {}'.format(relative, cmds.nodeType(relative)))
					if cmds.nodeType(relative) not in ('transform', 'shape'):
						# print ('Red Flag!: {}'.format(node))
						if node not in redFlagNodes:
							redFlagNodes.append(node)

	if len(redFlagNodes):
		# print('red flag nodes!!!')
		for node in redFlagNodes:
			master_assemblies.remove(node)
	# print('master_assemblies: {}'.format(master_assemblies))

	# print('red flags: {}'.format(redFlagNodes))

	if len(master_assemblies) == max_master_asseblies:
		nodes_with_subs = utils.subGroupsTest(master_assemblies)
		# print('nodes_with_subs: {}'.format(nodes_with_subs))
		if nodes_with_subs:
			fail = False





	cmds.progressBar(gMainProgressBar, edit=True, step=step)
	print "Pivot Placement Automation Successful!"
	if fail:
		tempDict = {
					'grade_value':gradeValue['F'],
					'comment_text':'',
					'default_comments_text':'Scene not grouped correctly. ',
					'example_comments_text':''}
	else:
		tempDict = {
					'grade_value':gradeValue['Aplus'],
					'comment_text':'',
					'default_comments_text':'Scene grouped correctly. Good job!',
					'example_comments_text':''}

	cmds.progressBar(gMainProgressBar, edit=True, step=step)
	
	
	cmds.progressBar(gMainProgressBar, edit=True, endProgress=True)
	return tempDict



