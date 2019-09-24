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
import os
import re
import random
import xml.etree.ElementTree as xml_elemTree

def ThreeDF_TurnIn(xmlDefaults, *args):
    gradeValue = {'A': int(xmlDefaults.find('gradeValue').find('A').text),
                'F-': int(xmlDefaults.find('gradeValue').find('F-').text),
                }

    naming_convention = xmlDefaults.find('naming_convention').text
    extensions = xmlDefaults.find('extensions').text

    bad_comment = 'Turn in procedures not in line with expectations.'
    good_comment = 'Turn in procedures followed. Good job!'

    development = False
    if development:
        print '3DF Turn In running'

    gMainProgressBar = maya.mel.eval('$tmp = $gMainProgressBar')

    cmds.progressBar( gMainProgressBar,
                    edit=True,
                    beginProgress=True,
                    isInterruptable=True,
                    status='Checking Turn In',
                    maxValue=100 )
    step = 100/7
    cmds.progressBar(gMainProgressBar, edit=True, step=step)
    sceneNameWPath = cmds.file(query = True, sceneName = True)
    parentFolder = sceneNameWPath.rsplit('/',2)[1]
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
        print('naming_convention: {}'.format(naming_convention))
        file_name = cmds.file(query = True, sceneName = True, shortName = True)
        source_string = naming_convention
        replace_list = [('lastname', '([a-zA-Z-]+)'),('firstname', '([a-zA-Z]+)'), ('yearMonth', '({})'.format(term_id))]
        if extensions != None:
            print('extensions found: {}'.format(extensions))
            replace_list.append(('extension', '({})'.format(extensions)))
        for item in replace_list:
            if item[0] in source_string:
                source_string = source_string.replace(item[0], item[1])
        source_string = '^' + source_string + '$'
        print('source_string: {}'.format(source_string))
        file_regex = re.compile(source_string, re.IGNORECASE)#add ,re.IGNORECASE to do case insensitive matching
        match_object = file_regex.match(file_name) 
        if match_object == None:
            fail = True
            bad_comment += ' File name incorrect.'
            print('file no match')

        print('file_name: {}\nsource_string: {}'.format(file_name, source_string))

    print('\n\n')
    #check the folder name
    if naming_convention != None:
        file_name = cmds.file(query = True, sceneName = True, shortName = True)
        folder_source_string = naming_convention.split('.')[0]
        replace_list = [('lastname', '[a-zA-Z]+'),('firstname', '[a-zA-Z]+'), ('yearMonth', term_id)]
        for item in replace_list:
            if item[0] in folder_source_string:
                folder_source_string = folder_source_string.replace(item[0], item[1])
        folder_source_string = '^' + folder_source_string + '$'
        folder_regex = re.compile(folder_source_string, re.IGNORECASE)#add ,re.IGNORECASE to do case insensitive matching
        match_object = folder_regex.search(parentFolder) 
        print('match_object: {}'.format(match_object))
        if match_object == None:
            fail = True
            bad_comment += ' Folder name incorrect.'
            print('folder no match')

        print('folder name: {}\nfolder_source_string: {}'.format(parentFolder, folder_source_string))
        print('\n\n')

    folderContents = os.listdir(sceneNameWPath.rsplit('/',1)[0])

    if not any(x.startswith(sceneName.rsplit('.',1)[0]) for x in folderContents):
        fail = True
        bad_comment += ' Reference not included or named incorrectly.'
            
    cmds.progressBar(gMainProgressBar, edit=True, step=step)
    print "Turn In Automation Successful!"
    if fail:
        tempDict = {
                    'grade_value':gradeValue['F-'],
                    'comment_text':bad_comment,
                    'default_comments_text':'',
                    'example_comments_text':''}
    else:
        tempDict = {
                    'grade_value':gradeValue['A'],
                    'comment_text':good_comment,
                    'default_comments_text':'',
                    'example_comments_text':''}

    cmds.progressBar(gMainProgressBar, edit=True, step=step)
    
    
    cmds.progressBar(gMainProgressBar, edit=True, endProgress=True)
    return tempDict



