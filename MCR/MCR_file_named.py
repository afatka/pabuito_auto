"""
Pabuito Auto Script

MCR File Named Correctly

This script contains a auto script for the Pabuito Grade Tool. 
This tool checks the active Maya file name against the provided convention.




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
import os
import re
import random
import xml.etree.ElementTree as xml_elemTree

def MCR_file_named(xmlDefaults, *args):
    gradeValue = {'Aplus': int(xmlDefaults.find('gradeValue').find('Aplus').text),
                'F': int(xmlDefaults.find('gradeValue').find('F').text),
                }

    naming_convention = xmlDefaults.find('naming_convention').text

    bad_comment = 'Submitted Maya file name is not in line with expectations. Please review the documentation for naming convention.'
    good_comment = 'Submitted Maya file name is in line with expectations. Good job!'

    development = False
    if development:
        print '3DF Turn In running'

    gMainProgressBar = maya.mel.eval('$tmp = $gMainProgressBar')

    cmds.progressBar( gMainProgressBar,
                    edit=True,
                    beginProgress=True,
                    isInterruptable=True,
                    status='Checking file name',
                    maxValue=100 )
    step = 100/7
    cmds.progressBar(gMainProgressBar, edit=True, step=step)
    sceneNameWPath = cmds.file(query = True, sceneName = True)
    sceneName = cmds.file(query = True, sceneName = True, shortName = True)

    fail = False

    print('\n\n')

    # if True:
    if xmlDefaults.find('term_id') == None:
        count = 0

        message_list = [
        'Please enter the Term ID:', 
        'Invalid. Please enter the Term ID:',
        'Term ID is YYMM', 
        'Come on now... You know this',
        'This is getting ridiculous...'
        ]

        mean_message_list = [
        'Maybe you could get an adult to help you?',
        'Do you click all the buttons this much?!',
        'I know you\'re lonely...but let\'s get on with it...', 
        'Help! Police! Stranger Danger!'
        ]
        term_id_prompt = ''
        while True:
            if count < len(message_list):
                message_is = message_list[count]
            else:
                message_is = mean_message_list[random.randint(0, len(mean_message_list)-1)]

            term_id_prompt = cmds.promptDialog(
                                title='Term ID',
                                 message= message_is,
                                 button=['Set ID'],
                                 defaultButton='Set ID',
                                 dismissString='Cancel')
            count += 1
            if term_id_prompt == 'Cancel':
                break
            term_id = cmds.promptDialog(query=True, text=True)
            if len(term_id) == 4:
                print('len 4')
                if term_id.isdigit():
                    break

        print('no term ID')
        xml_elemTree.SubElement(xmlDefaults, 'term_id')
        xmlDefaults.find('term_id').text = term_id

    #check the file name
    if naming_convention != None:
        term_id = xmlDefaults.find('term_id').text
        # print('naming_convention: {}'.format(naming_convention))
        file_name = cmds.file(query = True, sceneName = True, shortName = True)
        source_string = naming_convention
        replace_list = [('lastname', '[a-zA-Z-]+'),('firstname', '[a-zA-Z]+'), ('yearMonth', term_id)]
        for item in replace_list:
            if item[0] in source_string:
                source_string = source_string.replace(item[0], item[1])
        source_string = '^' + source_string + '$'
        file_regex = re.compile(source_string)#add ,re.IGNORECASE to do case insensitive matching
        match_object = file_regex.match(file_name) 
        if match_object == None:
            fail = True
            # bad_comment += ' File name incorrect.'
            # print('file no match')

        # print('file_name: {}\nsource_string: {}'.format(file_name, source_string))
            
    cmds.progressBar(gMainProgressBar, edit=True, step=step)
    print "File Named Automation Successful!"
    if fail:
        tempDict = {
                    'grade_value':gradeValue['F'],
                    'comment_text':'',
                    'default_comments_text':bad_comment,
                    'example_comments_text':''}
    else:
        tempDict = {
                    'grade_value':gradeValue['Aplus'],
                    'comment_text':'',
                    'default_comments_text':good_comment,
                    'example_comments_text':''}

    cmds.progressBar(gMainProgressBar, edit=True, step=step)
    
    
    cmds.progressBar(gMainProgressBar, edit=True, endProgress=True)
    return tempDict



