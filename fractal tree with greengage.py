#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 20 21:13:50 2021

@author: stefan
"""

import turtle

MINIMUM_BRANCH_LENGTH = 20
def build_tree(t, branch_length, shorten_by, angle):
    if branch_length > MINIMUM_BRANCH_LENGTH:
        t.width(branch_length//8)
        t.forward(branch_length)
        new_length = branch_length - shorten_by    
        t.left(angle)
        build_tree(t, new_length, shorten_by, angle)    
        t.right(angle * 2)
        build_tree(t, new_length, shorten_by, angle)    
        t.left(angle)
        t.backward(branch_length)
    elif branch_length == MINIMUM_BRANCH_LENGTH:
        t.width(1)
        t.fillcolor('green')
        t.begin_fill()
        t.circle(10,80)
        t.left(100)
        t.circle(10,80)
        t.right(360-100)        
        t.end_fill()
        t.begin_fill()
        t.circle(4,360)
        t.end_fill()
tree = turtle.Turtle()
tree.hideturtle()
tree.setheading(90)
tree.color('chocolate')
build_tree(tree, 40, 4, 15)
turtle.speed(0)
turtle.hideturtle()
turtle.mainloop()
