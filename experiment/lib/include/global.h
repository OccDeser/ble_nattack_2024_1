/*
 * @Author       : YongkangXiao xiaoyongkang@whu.edu.cn
 * @Date         : 2024-05-08 10:29:34
 * @LastEditTime : 2024-05-10 10:12:15
 * @FilePath     : /type-tamarin/include/global.h
 * @Description  : Global variables and types
 * @Encoding     : UTF-8
 */

#ifndef GLOBAL_H
#define GLOBAL_H

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#ifndef YYPARSER
#include "yacc.tab.h"
#define ENDFILE 0
#endif
#include "ast.h"

/****************************************************************
 *  Global Flags
 ****************************************************************/
extern bool FlagError;

/****************************************************************
 *  Global Variables
 ****************************************************************/
extern AstNode* AST;

#endif