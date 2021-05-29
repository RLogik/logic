#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from __future__ import annotations;
from typing import List;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# GLOBAL CONSTANTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def gluePolish(conn: str, *parts: str) -> str:
    return '{}{}'.format(conn, ''.join(parts));

def gluePolishWithOuter(conn: str, *parts: str) -> str:
    return '{}({})'.format(conn, ','.join(parts));

def glueInfix(conn: str, *parts: str) -> str:
    return (' ' + conn + ' ').join(parts);

def glueInfixWithOuter(conn: str, *parts: str) -> str:
    expr = (' ' + conn + ' ').join(parts);
    if len(parts) > 1:
        return '({})'.format(expr);
    return expr;

def glueQuantifier(
    conn: str, x: str, part: str,
    qbrackets: bool = False,
    subfmlbracket: bool = False,
    outerbrackets: bool = False,
    sepchar: str = ' '
) -> str:
    Q = '{} {}'.format(conn, x);
    subfml = part;
    if qbrackets:
        Q = '({})'.format(Q);
    if subfmlbracket:
        subfml = '({})'.format(subfml);
    expr = '{}{}{}'.format(Q, sepchar, subfml);
    if outerbrackets:
        expr = '({})'.format(expr);
    return expr;

def glue(option: str, conn: str, *parts: str) -> str:
    if option == 'polish':
        return gluePolish(conn, *parts);
    elif option == 'polishwithouter':
        return gluePolishWithOuter(conn, *parts);
    elif option == 'infix':
        return glueInfix(conn, *parts);
    elif option == 'infixwithouter':
        return glueInfixWithOuter(conn, *parts);
    elif option == 'quantifier':
        return glueQuantifier(conn, *parts, qbrackets=False, subfmlbracket=False, outerbrackets=False, sepchar='. ');
    elif option == 'quantifierwithouter':
        return glueQuantifier(conn, *parts, qbrackets=False, subfmlbracket=False, outerbrackets=True, sepchar='. ');
    raise Exception('\033[1m{}\033[0m is an invalid glue option!');

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CLASS: Expression
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Expression(object):
    kind:    str;
    valence: int;
    parts:   List[Expression];

    label:   str = ''; # reserved for 'names'
    symbol:  str = ''; # for computing parseable expression
    display: str = ''; # use e.g. for LaTeX formatting

    depth:   int;
    nnfdepth:int;

    outerbrackets: bool = False;
    glueOption: str      = 'polish';
    glueOuterOption: str = 'polish';

    def __init__(self, kind: str, *parts: Expression):
        self.kind = kind;
        self.depth = 0;
        self.parts = []
        for part in parts:
            part_ = part.__deepcopy__();
            part_.outerbrackets = True;
            self.parts.append(part_);
        self.valence = len(self.parts);
        self.depth = max([0] + [subfml.depth + 1 for subfml in parts]);
        if self.kind == 'not' and self.depth == 1:
            self.nnfdepth = 0;
        else:
            self.nnfdepth = max([0] + [subfml.depth + 1 for subfml in parts]);
        return;

    def __copy__(self) -> Expression:
        t = Expression(self.kind, *self.parts);
        t.label            = self.label;
        t.symbol           = self.symbol;
        t.display          = self.display;
        t.outerbrackets = self.outerbrackets;
        t.glueOption       = self.glueOption;
        t.glueOuterOption  = self.glueOuterOption;
        return t;

    def __deepcopy__(self) -> Expression:
        parts = [];
        for part in self.parts:
            parts.append(part.__deepcopy__());
        t = Expression(self.kind, *parts);
        t.label            = self.label;
        t.symbol           = self.symbol;
        t.display          = self.display;
        t.outerbrackets = self.outerbrackets;
        t.glueOption       = self.glueOption;
        t.glueOuterOption  = self.glueOuterOption;
        return t;

    def __eq__(self, o):
        if not isinstance(o, Expression):
            return False;
        n = len(self.parts);
        if not(self.kind == o.kind and n == len(o.parts)):
            return False;
        if self.kind in [
            'variable',
            'constant',
            'function',
            'functionexpression',
            'relation',
            'relationexpression',
        ] and not (self.symbol == o.symbol):
            return False;
        for k in range(n):
            if not (self.parts[k] == o.parts[k]):
                return False;
        return True;

    def __str__(self):
        if self.valence == 0:
            return self.symbol;
        option = self.glueOuterOption if self.outerbrackets else self.glueOption;
        return glue(option, self.symbol, *[str(_) for _ in self.parts]);

    def pretty(self,
        preindent: str = '',
        tab: str = '  ',
        prepend: str = '',
        depth: int = 0
    ) -> str:
        indent = preindent + tab*depth;
        symb = ' \033[1m{}\033[0m'.format(self.symbol) if (self.IsAtomic or self.IsTerm) else '';
        return '\n'.join(
            [indent + prepend + self.kind + symb] \
            + [child.pretty(preindent, tab, '|__ ', depth+1) for child in self.parts]
        );

    @property
    def expr(self):
        if self.valence == 0:
            return self.display;
        option = self.glueOuterOption if self.outerbrackets else self.glueOption;
        return glue(option, self.display, *[str(_) for _ in self.parts]);

    def showOuterBraces(self, show: bool=True) -> Expression:
        self.outerbrackets = show;
        return self;

    def getChild(self, index: int = 0) -> Expression:
        if index < self.valence:
            return self.parts[index];
        raise Exception('Formula has no subformula of index {}.'.format(index));

    @property
    def IsTerm(self) -> bool:
        return self.IsVariable or self.IsConstant or self.IsFunctionExpression

    @property
    def IsAtomic(self) -> bool:
        return self.kind == 'relationexpression';

    @property
    def IsNegatedAtomic(self) -> bool:
        return self.IsNegation and self.getChild().IsAtomic;

    @property
    def IsConnective(self) -> bool:
        return self.IsNegation or self.IsConjunction or self.IsDisjunction or self.IsImplication or self.IsDoubleImplication;

    @property
    def IsExpression(self) -> bool:
        return self.IsAtomic or self.IsConnective or self.IsQuantified;

    @property
    def IsVariable(self) -> bool:
        return self.kind == 'variable';

    @property
    def IsConstant(self) -> bool:
        return self.kind == 'constant';

    @property
    def IsFunction(self) -> bool:
        return self.kind == 'function';

    @property
    def IsFunctionExpression(self) -> bool:
        return self.kind == 'functionexpression';

    @property
    def IsRelation(self) -> bool:
        return self.kind == 'relation';

    @property
    def IsRelationExpression(self) -> bool:
        return self.kind == 'relationexpression';

    @property
    def IsNegation(self) -> bool:
        return self.kind == 'not';

    @property
    def IsConjunction(self) -> bool:
        return self.kind == 'and';

    @property
    def IsDisjunction(self) -> bool:
        return self.kind == 'or';

    @property
    def IsImplication(self) -> bool:
        return self.kind == 'implies';

    @property
    def IsDoubleImplication(self) -> bool:
        return self.kind == 'iff';

    @property
    def IsQuantified(self) -> bool:
        return self.IsUniversalQuantified or self.IsExistentialQuantified;

    @property
    def IsUniversalQuantified(self) -> bool:
        return self.kind == 'all';

    @property
    def IsExistentialQuantified(self) -> bool:
        return self.kind == 'exists';
