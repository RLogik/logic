#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from __future__ import annotations
from typing import List;

from src.core.utils import getAttribute;

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
    outerBrackets: bool = False,
    sepchar: str = ' '
) -> str:
    Q = '{} {}'.format(conn, x);
    subfml = part;
    if qbrackets:
        Q = '({})'.format(Q);
    if subfmlbracket:
        subfml = '({})'.format(subfml);
    expr = '{}{}{}'.format(Q, sepchar, subfml);
    if outerBrackets:
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
        return glueQuantifier(conn, *parts, qbrackets=False, subfmlbracket=False, outerBrackets=False, sepchar='. ');
    elif option == 'quantifierwithouter':
        return glueQuantifier(conn, *parts, qbrackets=False, subfmlbracket=False, outerBrackets=True, sepchar='. ');
    raise Exception('\033[1m{}\033[0m is an invalid glue option!');

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CLASS: Expression
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Expression(object):
    kind:    str;
    parts:   List[Expression];

    label:   str = ''; # reserved for unique identifiers/‘names‘
    symbol:  str = ''; # for computing parseable expression
    display: str = ''; # use e.g. for LaTeX formatting

    isLabelled:    bool  = False;
    outerBrackets: bool  = False;
    glueOption: str      = 'polish';
    glueOuterOption: str = 'polish';

    def __init__(self, kind: str, *parts: Expression):
        self.kind = kind;
        self.parts = [ part.__copy__().showOuterBraces(True) for part in parts ];
        return;

    @staticmethod
    def fromRepr(r: dict) -> Expression:
        kind = getAttribute(r, 'kind', expectedtype=str, default='undefined');
        parts = getAttribute(r, 'parts', expectedtype=list, default=[])
        t = Expression(kind=kind, *[Expression.fromRepr(_) for _ in parts]);
        t.outerBrackets   = getAttribute(r, 'outerBrackets',   expectedtype=bool, default=False);
        t.isLabelled      = getAttribute(r, 'isLabelled',      expectedtype=bool, default=False);
        t.label           = getAttribute(r, 'label',           expectedtype=str,  default='undefined');
        t.symbol          = getAttribute(r, 'symbol',          expectedtype=str,  default='undefined');
        t.display         = getAttribute(r, 'display',         expectedtype=str,  default='undefined');
        t.glueOption      = getAttribute(r, 'glueOption',      expectedtype=str,  default='undefined');
        t.glueOuterOption = getAttribute(r, 'glueOuterOption', expectedtype=str,  default='undefined');
        return t;

    def __copy__(self) -> Expression:
        t = Expression(self.kind, *self.parts);
        t.isLabelled      = self.isLabelled;
        t.outerBrackets   = self.outerBrackets;
        t.label           = self.label;
        t.symbol          = self.symbol;
        t.display         = self.display;
        t.glueOption      = self.glueOption;
        t.glueOuterOption = self.glueOuterOption;
        return t;

    def __deepcopy__(self) -> Expression:
        t = Expression(self.kind, *[part.__deepcopy__() for part in self.parts]);
        t.isLabelled      = self.isLabelled;
        t.outerBrackets   = self.outerBrackets;
        t.label           = self.label;
        t.symbol          = self.symbol;
        t.display         = self.display;
        t.glueOption      = self.glueOption;
        t.glueOuterOption = self.glueOuterOption;
        return t;

    def __eq__(self, o):
        if not isinstance(o, Expression):
            return False;
        n = len(self.parts);
        if not(self.kind == o.kind and n == len(o.parts) and self.isLabelled == o.isLabelled):
            return False;
        if self.isLabelled and not (self.label == o.label):
            return False;
        for k in range(n):
            if not (self.parts[k] == o.parts[k]):
                return False;
        return True;

    def __repr__(self) -> dict:
        return dict(
            kind            = self.kind,
            label           = self.label,
            symbol          = self.symbol,
            display         = self.display,
            outerBrackets   = self.outerBrackets,
            glueOption      = self.glueOption,
            glueOuterOption = self.glueOuterOption,
            parts           = [ repr(_) for _ in self.parts ],
        );

    def __str__(self):
        if self.valence == 0:
            return self.symbol;
        option = self.glueOuterOption if self.outerBrackets else self.glueOption;
        return glue(option, self.symbol, *[str(_) for _ in self.parts]);

    @property
    def valence(self) -> int:
        return len(self.parts);

    @property
    def depth(self) -> int:
        return max([0] + [subfml.depth + 1 for subfml in self.parts]);

    @property
    def expr(self):
        if self.valence == 0:
            return self.display;
        option = self.glueOuterOption if self.outerBrackets else self.glueOption;
        return glue(option, self.display, *[_.expr for _ in self.parts]);

    def showOuterBraces(self, show: bool=True) -> Expression:
        self.outerBrackets = show;
        return self;

    def getChild(self, index: int = 0) -> Expression:
        if index < self.valence:
            return self.parts[index];
        raise Exception('Formula has no subformula of index {}.'.format(index));

    def pretty(self, preindent: str = '', tab: str = '  ', prepend: str = '', depth: int = 0) -> str:
        indent = preindent + tab*depth;
        symb = ' \033[1m{}\033[0m'.format(self.label) if (self.IsAtomic or self.IsTerm) else '';
        return '\n'.join(
            [indent + prepend + self.kind + symb] \
            + [child.pretty(preindent, tab, '|__ ', depth+1) for child in self.parts]
        );

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
