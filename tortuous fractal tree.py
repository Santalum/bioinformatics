#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 21 14:20:48 2021

@author: stefan
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 20 21:13:50 2021

@author: stefan
"""

import turtle

MINIMUM_BRANCH_LENGTH = 40
def build_tree(t, branch_length, shorten_by, angle):
    if branch_length > MINIMUM_BRANCH_LENGTH:
        t.forward(branch_length//2)
        new_length = branch_length - shorten_by 
        t.fillcolor('green')
        t.begin_fill()
        t.circle(branch_length//2,angle)
        t.left(180-angle)
        t.circle(branch_length//2,angle)
        t.right(-60-angle)
        t.end_fill()
        #t.left(angle)
        build_tree(t, new_length, shorten_by, angle)    
        t.right(angle)
        build_tree(t, new_length, shorten_by, angle)    
        t.left(angle)
        t.backward(branch_length)
    elif branch_length == MINIMUM_BRANCH_LENGTH:
        #t.up()
        #t.goto(-100,-100)
        #t.down()
        t.fillcolor('green')
        t.begin_fill()
        t.circle(8,360)
        #t.left(120)
        #t.circle(30,60)
        #t.right(360-120)
        t.end_fill()
        return
tree = turtle.Turtle()
tree.hideturtle()
tree.setheading(90)
tree.color('chocolate')
build_tree(tree, 80, 8, 45)
turtle.speed(0)
turtle.hideturtle()
turtle.mainloop()
