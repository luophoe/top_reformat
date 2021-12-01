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
            # delete the input part of the line
            line = line[6:]
            # get the separated names
            split_list = line.split(",")
            # get rid of the extra content
            for i in rangw(len(split_list)):
                split_list[i] = stripextra(split_list[i])
                split_list[i] = stripsemicolon(split_list[i])
                if split_list[i] != "":
                    result_file.write("input           " + list[i] + ";\n")
            # identify the type of the declaration
            dec_type = 1
            # if the end of the declaration is reached
            if line.find(";") >= 0:
                end_check = 1
        # the inout declaration starts
        elif line.find("inout") >= 0 and line.find(",") >= 0:
            norm_form = 0
            end_check = 0
            # delete the input part of the line
            line = line[6:]
            # get the separated names
            split_list = line.split(",")
            # get rid of the extra content
            for i in rangw(len(split_list)):
                split_list[i] = stripextra(split_list[i])
                split_list[i] = stripsemicolon(split_list[i])
                if split_list[i] != "":
                    result_file.write("inout           " + list[i] + ";\n")
            # identify the type of the declaration
            dec_type = 2
            # if the end of the declaration is reached
            if line.find(";") >= 0:
                end_check = 1
        # still in the declaration
        elif end_check == 0:
            norm_form = 0
            # get the separated names
            split_list = line.split(",")
            # get rid of the extra content
            for i in range(len(split_list)):
                split_list[i] = stripextra(split_list[i])
                split_list[i] = stripsemicolon(split_list[i])
                if dec_type == 0:
                    if split_list[i] != "":
                        result_file.write("output           " + split_list[i] + ";\n")
                elif dec_type == 1:
                    if split_list[i] != "":
                        result_file.write("input           " + split_list[i] + ";\n")
                elif dec_type == 2:
                    if split_list[i] != "":
                        result_file.write("inout           " + split_list[i] + ";\n")
            # if the end of the declaration is reached
            if line.find(";") >= 0:
                end_check = 1
        # if it is the end of the declaration
        elif end_check == 1:
            end_check = -1
            dec_type = -1

        # 2. if the line has bit width, reformat by calculating the number of tabs and write into result file
        if (line.find("input") >= 0 or line.find("inout") >= 0 or line.find("output") >= 0) and (line.find("[") >= 0):
            norm_form = 0
            # calculate the number of tabs needed for writing
            tab_count = 16 - line.find("]")
            tab_str = ""
            for i in range(tab_count):
                tab_str = tab_str + " "
            # write into result file
            result_file.write(line[:line.find("]")+1] + tab_str + stripextra(line[line.find("]")+1:]) + "\n")

        # 3. if the lines are wrapped by specify and endspecify
        if line.find("specify") >= 0 and com_check == 0:
            norm_form = 0
            # add comment characters in front of it and write into result file
            com_check = 1
            result_file.write("// " + line)
        elif com_check == 1:
            norm_form = 0
            # add comment characters in front of it and write intp result file
            result_file.write("// " + line)
        if line.find("endspecify") >= 0:
            com_check = 0

        # 4. if the lines are for instantiation
        # the first comment line to indicate the start of instantiation
        if line.find("inst") >= 0 and line.find("//") >= 0:
            norm_form = 0
            inst_check = 1
            # find the instantiation file and find the module signal names
            inst_file = stripextra(line[line.find("inst")+4:])
            inst_file = open(inst_file, "r")
            inst_file_check = 0
            for line in inst_file:
                if line.find("module") >= 0 and line.find("(") >= 0:
                    inst_file_check = 0
                    for line in inst_file:
                        if line.find("module") >= 0 and line.find(")") >= 0:
                            inst_file_check = 1
                            line = line[line.find("(")+1:]
                            inst_list_lower = line.split(",")
                            for element in inst_list_lower:
                                element = stripextra(element)
                                element = stripsemicolon(element)
                                if element != "" and element != "\n":
                                    inst_list.append(element)
                        elif inst_file_check == 1:
                            inst_list_lower = line.split(",")
                            for element in inst_list_lower:
                                element = stripextra(element)
                                element = stripsemicolon(element)
                                if element != "" and element != "\n":
                                    inst_list.append(element)
                        if inst_file_check == 1 and line.find(")") >= 0:
                            inst_file_check = 0
        # find the moudle name and the port list
        elif inst_check == 1:
            norm_form = 0
            if line.find("(") >= 0:
                module_name = line[:line.find("(")]
                result_file.write(module_name + " (\n")
                line = line[line.find("(")+1:]
                if line.find("{") >= 0 and line.find("}") >= 0:
                    special_character = stripextra(line[line.find("{"):line.find("}")+1])
                elif line.find("{") >= 0 and line.find("}") < 0:
                    special_character = stripextra(line[line.find("{"):])
                    special_character_check = 1
                elif special_character_check == 1 and line.find("}") >= 0:
                    special_character = special_character + stripextra(line[:line.find("}")+1])
                inst_top_list = line.split(",")
                for element in inst_top_list:
                    element = stripextra(element)
                    element = stripsemicolon(element)
                    if element.find("{") >= 0:
                        is_char = 1
                    elif element.find("}") >= 0:
                        is_char = 0
                        tab_1 = ""
                        for i in range(25-len(inst_list[inst_list_num])):
                            tab_1 = tab_1 + " "
                        tab_2 = ""
                        for i in range(33-len(special_character)):
                            tab_2 = tab_2 + " "
                        result_file.write("         ." + inst_list[inst_list_num] + tab_1 + "(      " + special_character + tab_2 + "),\n")
                        inst_list_num += 1

                    elif element != "" and element != "\n" and is_char == 0:
                        tab_1 = ""
                        for i in range(25-len(inst_list[inst_list_nu,])):
                            tab_1 = tab_1 + " "
                        tab_2 = ""
                        for i in range(33-len(element)):
                            tab_2 = tab_2 + " "
                        result_file.write("         ." + inst_list[inst_list_num] + tab_1 + "(      " + element + tab_2 + "),\n")
                        inst_list_num += 1
                if line.find(")") >= 0:
                    result_file.write(");\n\n")
                    inst_check = 0
                    inst_list_num = 0
                    del inst_list[-len(inst_list):]

            # 5. if the line is not a part of the special lines, write directly into result_file
            if norm_form == 1:
                result_file.write(line)


# ----------------------------------------------------Part 2. Main------------------------------------------------------
# call top_file
# top_reformat(top_file, result_file)

top_reformat(top_file, result_file)
print("result file " + result_file + " updated.")
