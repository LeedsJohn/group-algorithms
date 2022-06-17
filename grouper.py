"""
John Leeds
6/17/2022
grouper.py

Creates a .json file with different ways to group
Rubik's cube algorithms
"""
import json


class Grouper:
    def __init__(self):
        self.algsets = ["CMLL", "COLL", "ELL", "OLL", "PLL", "WVLS", "WVLS_FL",
                        "ZBLL_AS", "ZBLL_H", "ZBLL_L", "ZBLL_Pi", "ZBLL_S", "ZBLL_T", "ZBLL_U"]
        self.groupingInstructions = {
            "CMLL": {"method": "contain", "AS": " AS ", "H": " H ", "L": " L "},
            "COLL": {"method": "contain", "B": "B", "C": "C", "D": "D", "E": "E", "F": "F", "G": "G", "H": "H"},
            "ELL": {"method": "contain", "Ua": " Ua", "Ub": " Ub", "Z": " Z", "H": " H", "Edge flip": ["Adjacent", "Opposite"]},
            "OLL": {"method": "between", "All edges": [21, 28], "No edges": [1, 5, 17, 21], "All Corners": [20, 21, 28, 29, 57, 58], "Square": [5, 7], "Small lightning": [7, 9, 11, 13],
                    "Knight move": [13, 17], "Fish": [9, 11, 35, 36, 37, 38], "Tree": [29, 31, 41, 43], "P": [31, 33, 43, 45], "T": [33, 34, 45, 46],
                    "C": [34, 35, 46, 47], "W": [36, 37, 38, 39], "Z": [39, 41], "Triangle": [47, 51, 53, 55], "Line": [51, 53, 55, 57]},
            "PLL": {"method": "contain", "Edges": ["Ua", "Ub", "Z", "H"], "Corners": ["Aa", "Ab", "E"], "A": ["Aa", "Ab"], "G": "G", "J": "J", "N": "N", "R": "R", "U": "U"},
            "WVLS": {"method": "between", "3 corners": [1, 2], "2 corners": [2, 8], "1 corner": [8, 19], "0 corners": [20, 28]},
        }
        self.specialCases = [["ELL", "Edge flip", "4-flip"]]
        self.groupingInstructions["WVLS_FL"] = self.groupingInstructions["WVLS"]
        for ZBLL in ["ZBLL_AS", "ZBLL_H", "ZBLL_L", "ZBLL_Pi", "ZBLL_S", "ZBLL_T", "ZBLL_U"]:
            self.groupingInstructions[ZBLL] = {"method": "contain"}

    def createGroupings(self):
        groupings = {}
        for algset in self.groupingInstructions:
            groupings[algset] = {}
            if self.groupingInstructions[algset]["method"] == "contain":
                for group in self.groupingInstructions[algset]:
                    if group == "method":
                        groupings[algset]["All"] = ["all"]
                        continue
                    groupings[algset][group] = self.getScramblesContaining(
                        algset, self.groupingInstructions[algset][group])

            elif self.groupingInstructions[algset]["method"] == "between":
                for group in self.groupingInstructions[algset]:
                    if group == "method":
                        groupings[algset]["All"] = ["all"]
                        continue
                    groupings[algset][group] = self.getScramblesBetween(
                        algset, self.groupingInstructions[algset][group])

        for special in self.specialCases:
            groupings[special[0]][special[1]].append(special[2])

        with open("groupings.json", "w") as f:
            json.dump(groupings, f)

    def getScramblesBetween(self, algset, between):
        if between == "contain" or between == "between":
            return ["all"]
        names = []
        with open(f"data/{algset}.json") as f:
            names = json.load(f)
        ans = []
        for i in range(0, len(between), 2):
            ans += [name for name in names if self._between(
                name, between[i], between[i+1])]

        return ans

    def getScramblesContaining(self, algset, phrase):
        if phrase == "contain" or phrase == "between":
            return ["all"]

        if isinstance(phrase, str):
            phrase = [phrase]

        names = []
        with open(f"data/{algset}.json") as f:
            names = json.load(f)

        ans = []
        for c in phrase:
            ans += [name for name in names if c in name]
        return ans

    def _between(self, name, x, y):
        num = self.getNumeric(name)
        if num >= x and num < y:
            return True
        return False

    def getNumeric(self, str):
        newString = ""
        for c in str:
            if c.isnumeric():
                newString += c
        return int(newString)
