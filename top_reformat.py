# top_reformat.py
#
# Created on: 11/29/2021
#     Author: Anyka
#      		  Phoebe Luo
import re
import os
import sys


# ------------------------------------Input Intended File Information for Generation------------------------------------
top_file = "/home/luozx/work/top_reformat/S3_new/S3_analog_top_verilog_netlist_20211130"
result_file = "/home/luozx/work/top_reformat/S3_new/S3_analog_top_verilog_netlist_20211130_result"
# ----------------------------------------------------------------------------------------------------------------------


# --------------------------------------------------Part 1. Functions---------------------------------------------------
# Function 1. strip the extra enters, tabs, and spaces
def stripextra(line):
    # strip the extra strings
    line = line.replace(" ", "")
    line = line.replace("\r", "")
    line = line.replace("\t", "")
    line = line.replace("\n", "")

    # if extra strings still exists, strip again by recursively calling
    if line.find(" ") >= 0 or line.find("\r") >= 0 or line.find("\t") >= 0 or line.find("\n") >= 0:
        stripextra(line)
    else:
        return line


# Function 2. strip semicolon
def stripsemicolon(line):
    # strip the semicolon
    line = line.replace(";", "")
    line = line.replace(")", "")
    return line


# Main Function
def top_reformat(top_file, result_file):
    # open the top_file
    top_file = open(top_file, "r+")
    # open the result_file
    result_file = open(result_file, "w")

    # inst_list to keep track of all the port names extracted from inst_file
    inst_list = []

    # end_check to indicate the end of the list is reached
    end_check = -1
    # dec_type to state the type of the declaration
    dec_type = -1
    # com_check to indicate when the lines need to be commented
    com_check = 0
    # inst_check to indicate when the lines are initiation lines
    inst_check = 0
    # inst_list_num to keep track of the number in the list
    inst_list_num = 0
    # special_character to write the port that is wrapped by {}
    special_character_check = 0
    # is_char to tell the list to skip the characters within {}
    is_char = 0

    # go into the file to check lines
    for line in top_file:
        # norm_form to indicate that it is the normal form and the lines can be directly transferred to the result file
        norm_form = 1

        # 1. if the line belongs to module declaration, extract and write it into result file
        # the output declaration starts
        if line.find("output") >= 0 and line.find(",") >= 0:
            norm_form = 0
            end_check = 0
            # delete the output part of the line
            line = line[7:]
            # get the separated names
            list = line.split(",")
            # get rid of the extra content
            for i in range(len(list)):
                list[i] = stripextra(list[i])
                list[i] = stripsemicolon(list[i])
                if list[i] != "":
                    result_file.write("output           " + list[i] + ";\n")
            # identify the type of the declaration
            dec_type = 0
            # if the end of the declaration is reached
            if line.find(";") >= 0:
                end_check = 1
        # the input declaration starts
        elif line.find("input") >= 0 and line.find(",") >= 0:
            norm_form = 0
            end_check = 0
            # delete the input part of the
