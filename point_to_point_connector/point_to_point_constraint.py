'''
point_to_point_constraint.py
Description:All point to point connector core functions.
Show: None
Author: Martin Lee
Created: 09 May 2023
Last Updated: 09 May 2023 - Martin Lee
Usuage - --
'''

import maya.cmds as mc
import maya.mel as mm


def pp_constraint(p1, p2):
    mc.select([p1, p2])
    mm.eval("createNConstraint pointToPoint 0;")
    mc.select(cl=True)

