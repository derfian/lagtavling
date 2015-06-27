#!/usr/bin/python

import os
import sys
import csv
import math
import optparse

from tavling.models import *

def main():
    parser = optparse.OptionParser()

    parser.add_option("-s", "--size=", dest="size")

    parser.add_option("-l", "--lag",
                      action="store_true",
                      dest="lag")

    parser.add_option("-i", "--individuell",
                      action="store_false",
                      dest="lag")

    parser.add_option("-j", "--jump",
                      action="store_false",
                      dest="agility")

    parser.add_option("-a", "--agility",
                      action="store_true",
                      dest="agility")
                      
    (options, args) = parser.parse_args()

    IN = csv.reader(sys.stdin, delimiter='\t')

    for row in IN:
        insert_contestant(row,
                          options.agility,
                          options.lag,
                          options.size)

"""
Data
Agility?
Lag?
Size: SML
"""
STARTNR = 0
TEAM = 2
DOGNAME = 5
HANDLER_SURNAME = 7
HANDLER_GIVENNAME = 8

TEAM_COUNTERS = {}
TEAM_ORDER_LETTERS = "ABCD"

def insert_contestant(row, agility, lag, size):
    print "Handling data:", row
    c = Contestant(handler="%s %s" % (row[HANDLER_GIVENNAME],
                                      row[HANDLER_SURNAME]),
                   dog=row[DOGNAME])
    c.save()

    r_agility = None
    r_jumping = None
    
    if lag:
        if row[TEAM] not in TEAM_COUNTERS:
            mt = Team(size=size,
                      name=row[TEAM],
                      order=1+int(math.floor(float(row[STARTNR]) / 4.0)))
            mt.save()
            TEAM_COUNTERS[row[TEAM]] = 0
        
        myteam = Team.objects.get(name=row[TEAM])
        tm = TeamMember(team=myteam,
                        contestant=c,
                        teamorder=TEAM_ORDER_LETTERS[TEAM_COUNTERS[row[TEAM]]],
                        agility_result=r_agility,
                        jumping_result=r_jumping)
        tm.save()
        TEAM_COUNTERS[row[TEAM]] += 1

        print "Added %s" % tm
    else:
        i_s = IndividualStart(contestant=c,
                              order=row[STARTNR],
                              agility_result=r_agility,
                              jumping_result=r_jumping,
                              size=size)
        i_s.save()
        print "Added %s" % i_s
                             
if __name__ == '__main__':
    main()

