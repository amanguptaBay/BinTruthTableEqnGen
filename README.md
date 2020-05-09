# BinTruthTableEqnGen
Created to simplify my workload for my EECS 31L class. Takes a Truth Table (for a Finite State Machine) in CSV form from a file and converts it into a minimized binary equation.

Takes in a input csv file in the form

|<Any String>|....St01....|....St02....|...
|....In01....|....0101....|....0102....|
|....In02....|....0201....|....0202....|
|....In03....|....0301....|....0302....|
...

Where In is the Input, St is the Current State, the other values are the outputs (a single bit)
