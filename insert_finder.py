#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 11:24:28 2020

@author: stefan
"""

def type_finder(sequence):
    for i in range(len(sequence)):
        if sequence[i]=="U":
            type="RNA"
            break
        elif sequence[i]=="T":
            type="DNA"
            break
    return type

def c_sequence(type,sequence):
    c_sequence=""
    for i in range(len(sequence)):
        if type=="RNA":
            if sequence[i]=='G':
                c_sequence+='C'                               
            elif sequence[i]=='C':
                c_sequence+='G'
            elif sequence[i]=='A':
                c_sequence+='U'
            elif sequence[i]=='U':
                c_sequence+='A'
        elif type=="DNA":
            if sequence[i]=='G':
                c_sequence+='C'                                
            elif sequence[i]=='C':
                c_sequence+='G'
            elif sequence[i]=='A':
                c_sequence+='T'
            elif sequence[i]=='T':
                c_sequence+='A'
    return c_sequence

def insert_finder(sequence_type, sequence, insert_sequence):
    c_insert_sequence=c_sequence(sequence_type,insert_sequence)
    position=-1
    for i in range(len(sequence)-len(insert_sequence)+1):
        if sequence[i:i+len(insert_sequence)]==insert_sequence:
            position=i
            break
        elif sequence[i:i+len(c_insert_sequence)]==c_insert_sequence:
            position=i
            break
#    c_sequence=c_sequence(sequence_type,sequence)
#    for i in range(len(c_sequence)-len(c_insert_sequence)+1):
#        if c_sequence[i:i+len(insert_sequence)]==insert_sequence:
#            position=i
#            break
#        elif c_sequence[i:i+len(c_insert_sequence)]==c_insert_sequence:
#            position=i
#            break
    if position!=-1:
        return position,position+len(c_insert_sequence)-1
    else:
        return "Error, insert not found in sequence."