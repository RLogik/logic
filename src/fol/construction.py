#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from __future__ import annotations;
from copy import copy;
from typing import Union;

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

def genericLabelledToken(kind, name: str, index: Union[str, None] = None, is_indexlike: bool = False, is_generic: bool = False) -> Expression:
    t = genericZeroary(kind);
    t.isLabelled = True;
    if index is None:
        t.label      = name;
        t.symbol     = name;
        t.display    = name;
    elif is_indexlike:
        if is_generic:
            t.label      = index;
            t.symbol     = '{}{{{}}}'.format(name, index);
            t.display    = '{{{}}}'.format(index);
        else:
            t.label      = '{{{}}}'.format(index);
            t.symbol     = '{{{}}}'.format(index);
            t.display    = '{{{}}}'.format(index);
    else:
        if is_generic:
            t.label      = index;
            t.symbol     = '{}{{{}}}'.format(name, index);
            t.display    = '{}_{{{}}}'.format(name, index);
        else:
            t.label      = '{}_{{{}}}'.format(name, index);
            t.symbol     = '{}_{{{}}}'.format(name, index);
            t.display    = '{}_{{{}}}'.format(name, index);
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

def Variable(name: str, index: Union[str, None], is_indexlike: bool, is_generic: bool) -> Expression:
    return genericLabelledToken('variable', name, index, is_indexlike, is_generic);

def Constant(name: str, index: Union[str, None], is_indexlike: bool, is_generic: bool) -> Expression:
    return genericLabelledToken('constant', name, index, is_indexlike, is_generic);

def Function(name: str, index: Union[str, None], is_indexlike: bool, is_generic: bool) -> Expression:
    return genericLabelledToken('function', name, index, is_indexlike, is_generic);

def FunctionExpression(F: Expression, *terms: Expression, polish: bool = True) -> Expression:
    kind = 'functionexpression';
    return genericPolishFuncReln(kind, F, *terms) if polish else genericInfixFuncReln(kind, F, *terms);

def Relation(name: str, index: Union[str, None], is_indexlike: bool, is_generic: bool) -> Expression:
    return genericLabelledToken('relation', name, index, is_indexlike, is_generic);

def RelationExpression(R: Expression, *terms: Expression, polish: bool = True) -> Expression:
    kind = 'relationexpression';
    return genericPolishFuncReln(kind, R, *terms) if polish else genericInfixFuncReln(kind, R, *terms);

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
    t.symbol  = 'all';
    t.display = r'\mathop{\forall}';
    return t;

def QuantifiedExists(x: Expression, subfml: Expression) -> Expression:
    kind = 'exists';
    t = genericQuantified(kind, x, subfml);
    t.symbol  = 'exists';
    t.display = r'\mathop{\exists}';
    return t;
