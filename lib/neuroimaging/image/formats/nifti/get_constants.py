import os, string, re

constants = file('constants.py', 'w')

def remove_comment(line):
    '''Replace C comments with python comments.'''
    uncomment_re = re.compile('(.*)/\*(.*)\*/')
    clean = uncomment_re.match(line)
    if clean:
        return string.join(clean.groups(), '#')
    else:
        return line

dt_list = []
nifti_type_list = []
nifti_intent_list = []
nifti_units_list = []
nifti_xform_list = []
nifti_slice_list = []

for line in string.split(file('nifti1.h').read(), '\n'):
    line = string.strip(line)
    if line.find('#define') == 0:
        line = remove_comment(line)
        line = line.replace('#define', '').strip()
        line = line.split()
        if line[0].find('(') == -1 and len(line) > 1: # no macros and no "empty" defines
            if line[0][0:3] == 'DT_':
                dt_list.append(line[0])

            if line[0][0:10] == 'NIFTI_TYPE':
                nifti_type_list.append(line[0])

            if line[0][0:12] == 'NIFTI_INTENT':
                nifti_intent_list.append(line[0])

            if line[0][0:11] == 'NIFTI_XFORM':
                nifti_xform_list.append(line[0])

            if line[0][0:11] == 'NIFTI_UNITS':
                nifti_units_list.append(line[0])

            if line[0][0:11] == 'NIFTI_SLICE':
                nifti_slice_list.append(line[0])

            line = '%s = %s\n' % (line[0], string.join(line[1:]))

            constants.write(line)

constants.write('\n\n')
constants.write('DT = [%s]\n\n' % string.join(dt_list, ', '))
constants.write('NIFTI_TYPE = [%s]\n\n' % string.join(nifti_type_list, ', '))
constants.write('NIFTI_INTENT = [%s]\n\n' % string.join(nifti_intent_list, ', '))
constants.write('NIFTI_XFORM = [%s]\n\n' % string.join(nifti_xform_list, ', '))
constants.write('NIFTI_UNITS = [%s]\n\n' % string.join(nifti_units_list, ', '))
constants.write('NIFTI_SLICE = [%s]\n\n' % string.join(nifti_slice_list, ', '))


constants.close()
