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

class huffman:
    
    # Contains the 3 following variables and the encode and decode functions
    
    message=''     # original message
    coded=''       # coded message
    tree=[]        # tree determining the encryption
    
    def __init__(self,**kwargs):
        if 'message' in kwargs:
            self.message=kwargs['message']
        if 'coded' in kwargs:
            self.coded=kw['coded']
        if 'tree' in kwargs:
            self.tree=kwargs['tree']
    
    def tree_2_code(self,rel_tree,bin_code):
        # Auxiliar function for huffman_encode
        # Recursive function transforming a tree into an association of letters and bin sequences
        k=[]
        for i,x in enumerate(rel_tree):
            if type(x)==str:
                k.append((x,bin_code+str(i)))
            else:
                k+=self.tree_2_code(x,bin_code+str(i))
        return k
    
    def encode(self):
        # the *args allows a predefined tree as a list in a format similar to the one in the output of this function.
        
        if self.tree==[]:
            self.tree=[]
            
            # Count
            for letter in self.message:
                if not letter in [x[0] for x in self.tree]:
                    self.tree.append([letter,self.message.count(letter)])
            
            # Make self.tree
            while len(self.tree)>1:
                self.tree.sort(key=lambda x:x[1])
                self.tree.insert(0,[[self.tree[0][0],self.tree[1][0]],self.tree[0][1]+self.tree[1][1]])
                self.tree.pop(1)
                self.tree.pop(1)
            self.tree=self.tree[0][0]
            
            # Make code
            code_list=self.tree_2_code(self.tree,'')
            code_dic={x[0]:x[1] for x in code_list}
        
        else:
            # Make code
            code_list=self.tree_2_code(self.tree,'')
            code_dic={x[0]:x[1] for x in code_list}
            
            # if a letter is not encodable, generates a new tree
            for letter in self.message:
                if not letter in code_dic:
                    self.tree=[]
                    return self.encode()
        
        # Encode
        self.coded=""
        for letter in self.message:
            self.coded+=code_dic[letter]
        
        return self.coded,self.tree
    
    def decode(self):
        self.message=""
        self.tree_rel=self.tree
        for x in self.coded:
            if type(self.tree_rel[int(x)])==str:
                self.message+=self.tree_rel[int(x)]
                self.tree_rel=self.tree
            else:
                self.tree_rel=self.tree_rel[int(x)]
      
        return self.message
