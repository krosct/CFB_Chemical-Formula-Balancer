import re
import flet as ft

from math import gcd
from fractions import Fraction

class Matrix:
    def __init__(self, *, numRows: int = 0, numColumns: int = 0, default: int = 0, matrix:list[list] = []):
        if not matrix:
            self.numRows = numRows
            self.numColumns = numColumns
            self.default = default
            self.matrix = [[Fraction(self.default) for x in range(self.numColumns)] for y in range(self.numRows)]
        else:
            self.numRows = len(matrix)
            self.numColumns = len(matrix[0])
            self.default = default
            self.matrix = [[Fraction(self.default) for x in range(self.numColumns)] for y in range(self.numRows)]
            for iRow in range(self.numRows):
                for iColumn in range(self.numColumns):
                    self.matrix[iRow][iColumn] = Fraction(matrix[iRow][iColumn])

    def __str__(self):
        rtn = ""
        for row in self.matrix:
            for i in row:
                rtn += str(i).rjust(5) + " "
            rtn += "\n"
        rtn = rtn[:-2]
        return rtn

    def toRREF(self):
        # Reduced Row Echelon Form (RREF)
        for i in range(self.numRows):
            self.one(i)
            self.zero(i)

        self.removeNegativeZeros()

    def one(self, target: int):
        row = column = target
        for i in range(row, self.numRows):
            if self.matrix[i][column] > 0:
                self.divRow(i, column)
                if self.matrix[row][column] < 0:
                    self.changeRowSignal(row)
                if i != row:
                    self.exchangeRows(i, row)
                break

    def divRow(self, iRow: int, iColumn: int):
        divisor = self.matrix[iRow][iColumn]
        for i in range(iColumn, self.numColumns):
            self.matrix[iRow][i] = Fraction(self.matrix[iRow][i], divisor)

    def changeRowSignal(self, iRow: int):
        for i in range(self.numColumns):
            self.matrix[iRow][i] *= -1

    def exchangeRows(self, iRowA: int, iRowB: int):
        temp = self.matrix[iRowA]
        self.matrix[iRowA] = self.matrix[iRowB]
        self.matrix[iRowB] = temp

    def zero(self, target: int):
        row = column = target
        if self.matrix[row][column] == 0:
            return
        
        for i in range(self.numRows):
            if self.matrix[i][column] != 0 and i != row:
                factor = Fraction(self.matrix[i][column], self.matrix[row][column])
                self.subRows(i, row, factor)

    def subRows(self, iRowA: int, iRowB: int, factor: int = 1):
        for i in range(self.numColumns):
            self.matrix[iRowA][i] -= factor * self.matrix[iRowB][i]

    def removeNegativeZeros(self):
        for row in range(self.numRows):
            for column in range(self.numColumns):
                if self.matrix[row][column] == 0:
                    self.matrix[row][column] = Fraction(0)

class ChemistryFormula:
    def __init__(self, *, formula: str = "", reagents: str = "", products: str = ""):
        if not formula:
            self.formula = reagents + " >>> " + products
            self.reagents = reagents
            self.products = products
        else:
            self.formula = formula
            self.reagents, self.products = formula.split(" >>> ")
            
        self.floorFormula = self.getFloorFormula()
        self.reagentMolecules, self.productMolecules = [x.replace(" ", "").split("+") for x in self.floorFormula.split(" >>> ")]
        self.numReagentMolecules = len(self.reagentMolecules)
        self.numProductMolecules = len(self.productMolecules)
        self.reagentElements = self.splitElements(self.reagentMolecules)
        self.productElements = self.splitElements(self.productMolecules)
        self.reagentFrags = self.splitElementNumber(self.reagentElements)
        self.productFrags = self.splitElementNumber(self.productElements)
        self.unbalancedFormulaMatrix = self.getFormulaMatrix()
        self.balancedFormulaMatrix, self.balancingIndexes = self.balanceFormula()

    def getFloorFormula(self):
        previous = ""
        floorFormula = ""

        for char in self.formula:
            if char.isdigit():
                if previous == " " or previous == "+":
                    continue
            
            floorFormula += char
            previous = char

        return floorFormula

    def splitElements(self, molecules: list[str]):
        elements = []

        for molecule in molecules:
            temp = []
            element = ""
            for char in molecule:
                if char.isupper():
                    temp.append(element)
                    element = char
                else:
                    element += char
            temp.append(element)
            elements.append(temp)
        
        for i in range(len(molecules)):
            elements[i].pop(0)

        return elements

    def splitElementNumber(self, formula: list[list[str]]):
        temp0 = []
        for iMolecule in range(len(formula)):
            temp1 = []
            for iElement in range(len(formula[iMolecule])):
                noNumber = True
                temp2 = []
                for iChar in range(len(formula[iMolecule][iElement])):
                    if formula[iMolecule][iElement][iChar].isdigit():
                        temp2.append(formula[iMolecule][iElement][:iChar])
                        temp2.append(int(formula[iMolecule][iElement][iChar:]))
                        noNumber = False
                        break
                if noNumber:
                    temp2.append(formula[iMolecule][iElement])
                    temp2.append(1)
                temp1.append(temp2)
            temp0.append(temp1)
            
        return temp0

    def getFormulaMatrix(self):
        def partialMatrix(formula: list):
            elementDict = {}
            numMolecules = len(formula)
            
            for i, molecule in enumerate(formula):
                for element in molecule:
                    if not elementDict.get(element[0], False):
                        elementDict[element[0]] = [0] * numMolecules
                        
                    elementDict[element[0]][i] = elementDict.get(element[0], [])[i] + element[1]

            return elementDict

        reagentsDict = partialMatrix(self.reagentFrags)
        productsDict = partialMatrix(self.productFrags)

        if not isValidElements(reagentsDict, productsDict):
            raise AssertionError("ELEMENT EXIST ONLY IN ONE SIDE")

        mountedMatrix = []
        for i in reagentsDict:
            mountedMatrix.append(list(x for x in reagentsDict[i]) + list(-y for y in productsDict[i]) + [0])

        matrix = Matrix(matrix=mountedMatrix)
        
        return matrix

    def balanceFormula(self):
        def coefficientList(m: Matrix):
            indexes = []
            targetColumn = m.numColumns-2
            for i in range(m.numRows):
                if m.matrix[i][targetColumn] == 0:
                    break
                else:
                    indexes.append(abs(m.matrix[i][targetColumn]))

            if len(indexes) <= 0:
                raise ArithmeticError("IMPOSSIBLE")

            indexes.append(1)
            
            lcm = fractionLcm(indexes)
            for i in range(len(indexes)):
                indexes[i] *= lcm
                
            return indexes

        formulaMatrix = self.unbalancedFormulaMatrix
        formulaMatrix.toRREF()

        return formulaMatrix, coefficientList(formulaMatrix)

def isValidElements(dictA: dict, dictB: dict):
    for i in dictA:
        if dictB.get(i, -1) == -1:
            return False    
        
    for i in dictB:
        if dictA.get(i, -1) == -1:
            return False

    return True    

def giveMeAnswer(e):
    reagentFormula = objsDict['reagents'].value
    productFormula = objsDict['products'].value

    try:
        if not isValidChemistry(reagentFormula) or not isValidChemistry(productFormula):
            objsDict["resultReagents"].value = " "
            objsDict["resultProducts"].value = " "
            page.update()
            return
        f = ChemistryFormula(reagents=reagentFormula, products=productFormula)
    except ArithmeticError as id:
        page.open(objsDict['dialog'])
        objsDict["resultReagents"].value = id.args[0]
        objsDict["resultProducts"].value = id.args[0]
        page.update()
        return
    except AssertionError as id:
        page.open(objsDict['dialog'])
        objsDict["resultReagents"].value = id.args[0]
        objsDict["resultProducts"].value = id.args[0]
        page.update()
        return
    
    indexes = f.balancingIndexes

    rAnswer = ""
    pAnswer = ""

    rIndexes = indexes[:f.numReagentMolecules]
    pIndexes = indexes[f.numReagentMolecules:]

    for i in range(len(rIndexes)):
        rAnswer += str(rIndexes[i] * int(objsDict['answerFactor'].value)) + " " + str(f.reagentMolecules[i])
        if i < (f.numReagentMolecules - 1):
            rAnswer += " + "

    for i in range(len(pIndexes)):
        pAnswer += str(pIndexes[i] * int(objsDict['answerFactor'].value)) + " " + str(f.productMolecules[i])
        if i < (f.numProductMolecules - 1):
            pAnswer += " + "

    rtn = rAnswer + " >>> " + pAnswer

    objsDict["resultReagents"].value, objsDict["resultProducts"].value = rtn.split(" >>> ")
    page.update()
        
def fractionLcm(fractions: list[Fraction]):
    denominators = [f.denominator for f in fractions]
    actualLcm = 1
    for i in range(len(denominators)):
        actualLcm = (actualLcm * denominators[i]) // gcd(actualLcm, denominators[i])

    return actualLcm

def isValidChemistry (equacao: str) -> bool:
    equacao = equacao.replace(" ", "")
    molecula_regex = r"(\d*)(([A-Z][a-z]?\d*)+)"
    equacao_regex = rf"^({molecula_regex})(\+{molecula_regex})*$"
    return bool(re.fullmatch(equacao_regex, equacao))

# Global Consts
windowTitle = "Equilibrando equações químicas usando sistemas lineares"
reagentTitle = "Reagentes"
productTitle = "Produtos"
defaultAnswerText = "Balanced formula will be shown here!"
titleSize = 50
iconSize = 40
titleIconSize = 60
answerSize = 30
columnHeight = 300
columnWidth = 150
totalElems = 10
textFieldWidthA = 125
objsDict = {}
windowWidth = 850
windowHeight = 500
page = None

def main(page1: ft.Page):
    global page
    page = page1
    
    page.title = windowTitle
    page.theme_mode = ft.ThemeMode.LIGHT
    page.scroll = ft.ScrollMode.AUTO
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER
    page.window.width = windowWidth
    page.window.height = windowHeight
    objsDict["reagents"] = ft.TextField(label="Reagents", on_blur=giveMeAnswer, on_submit=giveMeAnswer)
    objsDict["products"] = ft.TextField(label="Products", on_blur=giveMeAnswer, on_submit=giveMeAnswer)
    objsDict["answerFactor"] = ft.TextField(label="Factor", value=1, width=textFieldWidthA, text_align=ft.TextAlign.CENTER, on_change=giveMeAnswer, icon=ft.Icons.CALCULATE)
    objsDict["answerText"] = ft.Text(value=defaultAnswerText, size=answerSize)
    objsDict["signature"] = ft.Text(value="Made by: Gabriel Monteiro Silva - 2025", size=10, color=ft.Colors.GREY)
    objsDict["iconButton1"] = ft.IconButton(icon=ft.Icons.BALANCE, on_click=giveMeAnswer, icon_color=ft.Colors.BLACK, icon_size=iconSize, bgcolor=ft.Colors.GREY_300)
    objsDict["icon0"] = ft.Icon(name=ft.Icons.SCIENCE, size=titleIconSize, color=ft.Colors.BLACK)
    objsDict["icon1"] = ft.Icon(name=ft.Icons.ARROW_FORWARD, size=iconSize, color=ft.Colors.BLACK)
    objsDict["icon2"] = ft.Icon(name=ft.Icons.BALANCE, size=titleIconSize, color=ft.Colors.BLACK)
    objsDict["title"] = ft.Text(value="Chemical Formula Balancer", size=titleSize, weight=ft.FontWeight.BOLD)
    objsDict["resultReagents"] = ft.TextField(label="Reagents Result", read_only=True, value=" ")
    objsDict["resultProducts"] = ft.TextField(label="Products Result", read_only=True, value=" ")
    objsDict['dialog'] = ft.SnackBar(content=ft.Text("There is something wrong with the formulas. Check this out."), show_close_icon=True, bgcolor=ft.Colors.RED)

    objsDict["row4"] = ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls = 
                        [
                            objsDict['answerFactor'],
                        ],)
    objsDict['row3'] = ft.Row(alignment=ft.MainAxisAlignment.SPACE_EVENLY, controls = 
                        [
                            objsDict['answerFactor'],
                            objsDict['answerText'],
                        ],)
    objsDict['row3ALT'] = ft.Row(alignment=ft.MainAxisAlignment.SPACE_EVENLY, controls = 
                        [
                            objsDict['resultReagents'],
                            objsDict["icon1"],
                            objsDict['resultProducts'],
                        ],)
    objsDict['row2'] = ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=
                        [
                            objsDict["iconButton1"],
                        ],)
    objsDict['row1'] = ft.Row(alignment=ft.MainAxisAlignment.SPACE_EVENLY, controls=
                        [
                            objsDict["reagents"],
                            objsDict["icon1"],
                            objsDict["products"],
                        ],)
    objsDict['div2'] = ft.Divider(height=2)
    objsDict['row0'] = ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=
                        [
                            objsDict["icon0"],
                            objsDict["title"],
                            objsDict["icon2"],
                        ],)
    objsDict['col1'] = ft.Column(spacing=30, controls=[objsDict["row0"], objsDict['div2'], objsDict["row1"], objsDict["row4"], objsDict["row3ALT"], objsDict['div2']])
    
    page.add(
        objsDict['col1'],
        objsDict["signature"]
    )

ft.app(main)

# Suggestions of inputs:
# Na2CO3 + HCl
# NaCl + H2O + CO2
#
# CH4 + O2
# CO2 + H2O
#
# HCl + Na3PO4
# H3PO4 + NaCl
#
# Al2O3 + HCl
# AlCl3 + H2O
# 
# C2H6O + O2
# CO2 + H2O