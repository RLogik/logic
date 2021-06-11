#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from __future__ import annotations;
from lark import Lark;
from lark import Tree;
from typing import List;
from typing import Tuple;
from typing import Union;

from src.fol.classes import Expression;
from src.fol.construction import Constant;
from src.fol.construction import Variable;
from src.fol.construction import Function;
from src.fol.construction import FunctionExpression;
from src.fol.construction import Relation;
from src.fol.construction import RelationExpression;
from src.fol.construction import Not;
from src.fol.construction import And;
from src.fol.construction import Or;
from src.fol.construction import Iff;
from src.fol.construction import Implies;
from src.fol.construction import QuantifiedAll;
from src.fol.construction import QuantifiedExists;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# GLOBAL CONSTANTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PATH_GRAMMAR: str = 'src/grammars/fol.lark';
LEXER: Lark;

# lexer durch LARK erzeugen
with open(PATH_GRAMMAR, 'r') as fp:
    grammar = ''.join(fp.readlines());
    LEXER   = Lark(grammar, start='search', regex=True);

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MAIN METHOD string -> PropLogicExpr
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def parseFolExprToStr(u: str) -> str:
    return str(parseFolExpr(u));

def parseFolExprsToStr(u: str) -> List[str]:
    return [str(_) for _ in parseFolExprs(u)];

def parseFolExpr(u: str) -> Expression:
    fmls = parseFolExprs(u);
    if len(fmls) == 1:
        return fmls[0];
    raise Exception('String \033[1m{}\033[0m must contain exactly one expression!'.format(u));

def parseFolExprs(u: str) -> List[Expression]:
    try:
        fmls = lexedToExprs(LEXER.parse(u));
    except:
        raise Exception('Could not parse expressions \033[1m{}\033[0m!'.format(u));
    return fmls;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# PRIVATE METHODS: recursive lex -> Expression
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def lexedToExprs(u: Tree) -> List[Expression]:
    typ = u.data;
    if typ in ['term', 'expr']:
        return [ lexedToExpr(u) ];
    elif typ in ['terms', 'exprs']:
        return [ lexedToExpr(uu) for uu in filterSubexpr(u) ];
    raise Exception('Could not parse expression!');

def lexedToExpr(u: Tree) -> Expression:
    children = filterSubexpr(u);
    typ = u.data;
    if typ == 'expr':
        return lexedToExpr(children[0]);
    if typ == 'exprclosed':
        return lexedToExpr(children[0]).showOuterBraces(True);
    elif typ == 'expropen':
        return lexedToExpr(children[0]).showOuterBraces(False);
    elif typ == 'constant':
        label = lexedToLabel(children[0], is_indexlike=True);
        return Constant(*label);
    elif typ == 'variable':
        label = lexedToLabel(children[0]);
        return Variable(*label);
    elif typ == 'term':
        return lexedToExpr(children[0]);
    elif typ == 'termclosed':
        return lexedToExpr(children[0]).showOuterBraces(True);
    elif typ == 'termopen':
        return lexedToExpr(children[0]).showOuterBraces(False);
    elif typ == 'funcpolish':
        label = lexedToLabel(children[0]);
        return FunctionExpression(Function(*label), *lexedToExprs(children[1]), polish=True);
    elif typ == 'funcinfix':
        labels = list(set([ lexedToLabel(child) for child in filterOps(u) ]));
        assert len(labels) == 1, 'Cannot parse expression with inconsistent infix symbols';
        return FunctionExpression(Function(*labels[0]), *[ lexedToExpr(child) for child in filterOutOps(u) ], polish=False);
    elif typ == 'relnpolish':
        label = lexedToLabel(children[0]);
        return RelationExpression(Relation(*label), *lexedToExprs(children[1]), polish=True);
    elif typ == 'relninfix':
        labels = list(set([ lexedToLabel(child) for child in filterOps(u) ]));
        assert len(labels) == 1, 'Cannot parse expression with inconsistent infix symbols';
        return RelationExpression(Relation(*labels[0]), *[ lexedToExpr(child) for child in filterOutOps(u) ], polish=False);
    elif typ == 'not':
        return Not(lexedToExpr(children[0]));
    elif typ == 'and':
        return And(*[lexedToExpr(child) for child in children]);
    elif typ == 'or':
        return Or(*[lexedToExpr(child) for child in children]);
    elif typ == 'implies':
        return Implies(lexedToExpr(children[0]), lexedToExpr(children[1]));
    elif typ == 'iff':
        return Iff(lexedToExpr(children[0]), lexedToExpr(children[1]));
    elif typ == 'quantified':
        return lexedToExpr(children[0]);
    elif typ == 'all':
        return QuantifiedAll(lexedToExpr(children[0]), lexedToExpr(children[1]));
    elif typ == 'exists':
        return QuantifiedExists(lexedToExpr(children[0]), lexedToExpr(children[1]));
    raise Exception('Could not parse expression!');

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# AUXILIARY METHODS: filtration
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def lexedToLabel(u: Tree, is_indexlike: bool = False) -> Tuple[str, Union[str, None], bool, bool]:
    typ = u.data;
    if typ == 'op':
        children = filterSubexpr(u);
        return lexedToLabel(children[0]);
    elif typ == 'name':
        is_generic = False;
        children = filterOutNoncapture(u);
        name = lexedToStr(children[0]);
        index = lexedToStr(children[1]) if len(children) >= 2 else None;
        is_generic = ( isinstance(children[0], Tree) and children[0].data == 'symb' );
        if is_indexlike:
            if is_generic:
                is_indexlike = False;
            else:
                index = name;
                name = '';
        return name, index, is_indexlike, is_generic;
    raise Exception('Could not parse label!');

def lexedToStr(u: Union[str, Tree]) -> str:
    if isinstance(u, str):
        return str(u);
    return ''.join([ lexedToStr(uu) for uu in u.children ]);

def filterSubexpr(u: Tree) -> List[Tree]:
    return [uu for uu in u.children if isinstance(uu, Tree) and hasattr(uu, 'data') and not uu.data == 'noncapture'];

def filterOps(u: Tree) -> List[Tree]:
    return [uu for uu in filterSubexpr(u) if uu.data == 'op' ];

def filterOutOps(u: Tree) -> List[Tree]:
    return [uu for uu in filterSubexpr(u) if not uu.data == 'op' ];

def filterOutNoncapture(u: Tree) -> List[Union[str, Tree]]:
    return [uu for uu in u.children if not isinstance(uu, Tree) or ( hasattr(uu, 'data') and not uu.data == 'noncapture' ) ];
