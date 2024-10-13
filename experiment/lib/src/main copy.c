/*
 * @Author       : YongkangXiao xiaoyongkang@whu.edu.cn
 * @Date         : 2024-05-10 09:38:49
 * @LastEditTime : 2024-06-07 16:39:34
 * @FilePath     : /type-tamarin/src/main.c
 * @Description  :
 * @Encoding     : UTF-8
 */
#include "ast.h"
#include "global.h"
#include "syntax.h"
#include <assert.h>
#include <getopt.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

extern int yyparse();
extern FILE* yyin;

AstNode* AST = NULL;

char* input = NULL;
char* output = NULL;
char* treefile = NULL;

void print_usage(const char* program_name)
{
    printf("Usage: %s [OPTIONS] INPUT\n", program_name);
    printf("Options:\n");
    printf("  -o, --output FILE    Specify the output file\n");
    printf("  -t, --tree FILE      Specify the file Output to write abstract syntax tree\n");
    printf("  -h, --help           Display this help message\n");
    printf("Arguments:\n");
    printf("  INPUT                Specify the input file\n");
}

int parse_arguments(int argc, char* const argv[])
{
    int opt;
    int option_index = 0;
    static struct option long_options[] = {
        { "output", required_argument, 0, 'o' },
        { "tree", required_argument, 0, 't' },
        { "help", no_argument, 0, 'h' },
        { 0, 0, 0, 0 }
    };

    while ((opt = getopt_long(argc, argv, "o:t:h", long_options, &option_index)) != -1) {
        switch (opt) {
        case 'o':
            output = optarg;
            break;
        case 't':
            treefile = optarg;
            break;
        case 'h':
            return -1;
        default:
            return -1;
        }
    }

    if (optind < argc) {
        input = argv[optind];
    } else {
        fprintf(stderr, "Error: Missing input file\n");
        return -1;
    }

    if (!output) {
        output = "output.spthy";
    }

    return 0;
}

int main(int argc, char* const argv[])
{

#ifdef DEBUG
    extern int yydebug;
    yydebug = 1;
#endif

    if (-1 == parse_arguments(argc, argv)) {
        print_usage(argv[0]);
        return -1;
    }

    printf("input: %s\n", input);
    printf("output: %s\n", output);
    printf("treefile: %s\n", treefile);

    yyin = fopen(input, "r");
    assert(yyin);

    int ret = yyparse();
    assert(!ret);
    fclose(yyin);

    if (treefile) {
        FILE* tree = fopen(treefile, "w");
        print_ast_tree(AST, tree);
        fclose(tree);
    }

    syntax_extend(AST);
    FILE* out = fopen(output, "w");
    print_ast_code(AST, out);
    fclose(out);


    ast_tree_destory(AST);
    return 0;
}
