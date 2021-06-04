#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from __future__ import annotations;
from copy import copy;

from src.fol.classes import Expression;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# GLOBAL CONSTANTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHODS: Generic const, unary, binary
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def genericZeroary(kind: str) -> Expression:
    t = Expression(kind);
    t.outerBrackets   = False;
    t.glueOption      = 'polish';
    t.glueOuterOption = 'polish';
    return t;

def genericUnary(kind: str, args0: Expression) -> Expression:
    t = Expression(kind, args0);
    t.outerBrackets   = False;
    t.glueOption      = 'polish';
    t.glueOuterOption = 'polish';
    return t;

def genericBinary(kind: str, args0: Expression, args1: Expression) -> Expression:
    t = Expression(kind, args0, args1);
    t.outerBrackets   = False;
    t.glueOption      = 'infix';
    t.glueOuterOption = 'infixwithouter';
    return t;

def genericAssociative(kind: str, *args: Expression) -> Expression:
    t = Expression(kind, *args);
    t.outerBrackets   = False;
    t.glueOption      = 'infix';
    t.glueOuterOption = 'infixwithouter';
    return t;

def genericPolishFuncReln(kind: str, S: Expression, *terms: Expression) -> Expression:
    t = Expression(kind, *terms);
    t.isLabelled      = True;
    t.outerBrackets   = True;
    t.label           = S.label;
    t.symbol          = S.symbol;
    t.display         = S.display;
    t.glueOption      = 'polishwithouter';
    t.glueOuterOption = 'polishwithouter';
    return t;

def genericInfixFuncReln(kind: str, S: Expression, *terms: Expression) -> Expression:
    t = Expression(kind, *terms);
    t.isLabelled      = True;
    t.outerBrackets   = True;
    t.label           = S.label;
    t.symbol          = S.symbol;
    t.display         = S.display;
    t.glueOption      = 'infix';
    t.glueOuterOption = 'infixwithouter';
    return t;

def genericQuantified(kind: str, x: Expression, fml: Expression) -> Expression:
    t = Expression(kind, x, fml);
    t.glueOption      = 'quantifier';
    t.glueOuterOption = 'quantifierwithouter';
    t.outerBrackets   = False;
    return t;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHODS: variable, constant, function, relation
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def Variable(symb: str) -> Expression:
    kind = 'variable';
    t = genericZeroary(kind);
    t.isLabelled = True;
    t.label      = symb;
    t.symbol     = symb;
    t.display    = symb;
    return t;

def Constant(symb: str) -> Expression:
    kind = 'constant';
    t = genericZeroary(kind);
    t.isLabelled = True;
    t.label      = symb;
    t.symbol     = symb;
    t.display    = symb;
    return t;

def Function(symb: str) -> Expression:
    kind = 'function';
    t = genericZeroary(kind);
    t.label   = symb;
    t.symbol  = symb;
    t.display = symb;
    return t;

def FunctionExpression(F: Expression, *terms: Expression, polish: bool = True) -> Expression:
    kind = 'functionexpression';
    if polish:
        t = genericPolishFuncReln(kind, F, *terms);
    else:
        t = genericInfixFuncReln(kind, F, *terms);
    return t;

def Relation(symb: str) -> Expression:
    kind = 'relation';
    t = genericZeroary(kind);
    t.label   = symb;
    t.symbol  = symb;
    t.display = symb;
    return t;

def RelationExpression(R: Expression, *terms: Expression, polish: bool = True) -> Expression:
    kind = 'relationexpression';
    if polish:
        t = genericPolishFuncReln(kind, R, *terms);
    else:
        t = genericInfixFuncReln(kind, R, *terms);
    return t;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHODS: 0th order connectives
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def Not(subfml: Expression) -> Expression:
    kind = 'not';
    t = genericUnary(kind, subfml);
    t.symbol  = '!';
    t.display = r'\mathop{\neg}';
    return t;

def And(*subfmls: Expression) -> Expression:
    if len(subfmls) == 0:
        raise Exception('Conjunciton of 0 formulae not yet implemented!');
    elif len(subfmls) == 1:
        return copy(subfmls[0]);
    kind = 'and';
    t = genericAssociative(kind, *subfmls);
    t.symbol  = '&&';
    t.display = r'\mathbin{\wedge}';
    return t;

def Or(*subfmls: Expression) -> Expression:
    if len(subfmls) == 0:
        raise Exception('Conjunciton of 0 formulae not yet implemented!');
    elif len(subfmls) == 1:
        return copy(subfmls[0]);
    kind = 'or';
    t = genericAssociative(kind, *subfmls);
    t.symbol  = '||';
    t.display = r'\mathbf{\vee}';
    return t;

def Implies(subfml0: Expression, subfml1: Expression) -> Expression:
    kind = 'implies';
    t = genericBinary(kind, subfml0, subfml1);
    t.symbol  = '->';
    t.display = r'\mathbin{\rightarrow}';
    return t;

def Iff(subfml0: Expression, subfml1: Expression) -> Expression:
    kind = 'iff';
    t = genericBinary(kind, subfml0, subfml1);
    t.symbol  = '<->';
    t.display = r'\mathbin{\leftrightarrow}';
    return t;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHODS: 1st order quantifiers
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def QuantifiedAll(x: Expression, subfml: Expression) -> Expression:
    kind = 'all';
    t = genericQuantified(kind, x, subfml);
    t.symbol = 'all';
    t.display = r'\mathop{\forall}';
    return t;

def QuantifiedExists(x: Expression, subfml: Expression) -> Expression:
    kind = 'exists';
    t = genericQuantified(kind, x, subfml);
    t.symbol = 'exists';
    t.display = r'\mathop{\exists}';
    return t;
