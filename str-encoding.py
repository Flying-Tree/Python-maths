#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 19 20:14:06 2021

@author: Olivier Henry
"""

# Scripts to encode and decode strings

from math import *

# =============================================================================
# HUFFMAN CODING
# =============================================================================

def tree_2_code(tree,bin_code):
    # Auxiliar function for huffman_encode
    # Recursive function transforming a tree into an association of letters and bin sequences
    k=[]
    for i,x in enumerate(tree):
        if type(x)==str:
            k.append((x,bin_code+str(i)))
        else:
            k+=tree_2_code(x,bin_code+str(i))
    return k

def huffman_encode(message,*args):
    # the *args allows a predefined tree as a list in a format similar to the one in the output of this function.
    
    if len(args)==0:
        tree=[]
        
        # Count
        for letter in message:
            if not letter in [x[0] for x in tree]:
                tree.append([letter,message.count(letter)])
        
        # Make tree
        while len(tree)>1:
            tree.sort(key=lambda x:x[1])
            tree.insert(0,[[tree[0][0],tree[1][0]],tree[0][1]+tree[1][1]])
            tree.pop(1)
            tree.pop(1)
        tree=tree[0][0]
    else:
        tree=args[0]
    
    # Make code
    code_list=tree_2_code(tree,'')
    code_dic={x[0]:x[1] for x in code_list}
    
    # Encode
    coded=""
    for letter in message:
        coded+=code_dic[letter]
    
    return coded,tree

def huffman_decode(coded,tree):
    message=""
    tree_rel=tree
    for x in coded:
        if type(tree_rel[int(x)])==str:
            message+=tree_rel[int(x)]
            tree_rel=tree
        else:
            tree_rel=tree_rel[int(x)]
  
    return message
