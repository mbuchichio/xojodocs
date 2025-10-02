/**
 * display.c - Terminal display formatting
 */

#include "display.h"
#include <stdio.h>
#include <string.h>

// ANSI color codes (optional, can be disabled)
#define RESET   "\033[0m"
#define BOLD    "\033[1m"
#define CYAN    "\033[36m"
#define GREEN   "\033[32m"
#define YELLOW  "\033[33m"
#define GRAY    "\033[90m"

// Use colors only on Unix/Linux, plain on Windows by default
#ifdef _WIN32
    #define C_RESET   ""
    #define C_BOLD    ""
    #define C_CYAN    ""
    #define C_GREEN   ""
    #define C_YELLOW  ""
    #define C_GRAY    ""
#else
    #define C_RESET   RESET
    #define C_BOLD    BOLD
    #define C_CYAN    CYAN
    #define C_GREEN   GREEN
    #define C_YELLOW  YELLOW
    #define C_GRAY    GRAY
#endif

void display_error(const char *message) {
    fprintf(stderr, "ERROR: %s\n", message);
    fflush(stderr);
}

void display_search_results(const SearchResult *results) {
    if (!results || !results[0].class_name) {
        printf("No results found.\n");
        fflush(stdout);
        return;
    }
    
    printf("\n");
    printf("%-30s %-20s %s\n", "CLASS", "MODULE", "DESCRIPTION");
    printf("%-30s %-20s %s\n", "-----", "------", "-----------");
    
    for (int i = 0; results[i].class_name != NULL; i++) {
        printf("%s%-30s%s ", C_BOLD, results[i].class_name, C_RESET);
        printf("%s%-20s%s ", C_CYAN, results[i].module, C_RESET);
        
        if (results[i].description) {
            // Truncate long descriptions
            char desc_truncated[81];
            strncpy(desc_truncated, results[i].description, 80);
            desc_truncated[80] = '\0';
            
            if (strlen(results[i].description) > 80) {
                desc_truncated[77] = '.';
                desc_truncated[78] = '.';
                desc_truncated[79] = '.';
            }
            
            printf("%s%s%s", C_GRAY, desc_truncated, C_RESET);
        }
        
        printf("\n");
    }
    
    printf("\n");
    fflush(stdout);
}

void display_class_details(const ClassInfo *info, const MemberInfo *properties, const MemberInfo *methods, int sections) {
    if (!info) {
        printf("Class not found.\n");
        return;
    }
    
    printf("\n");
    printf("%s%s%s\n", C_BOLD, info->name, C_RESET);
    printf("Module: %s%s%s\n", C_CYAN, info->module, C_RESET);
    
    // Description
    if ((sections & SECTION_DESCRIPTION) && info->description) {
        printf("\nDescription:\n%s\n", info->description);
    }
    
    if (info->compatibility) {
        printf("\n%sCompatibility: %s%s\n", C_YELLOW, info->compatibility, C_RESET);
    }
    
    // Properties
    if ((sections & SECTION_PROPERTIES) && properties && properties[0].name) {
        printf("\n%sPROPERTIES:%s\n", C_GREEN, C_RESET);
        
        for (int i = 0; properties[i].name != NULL; i++) {
            printf("  * %s", properties[i].name);
            
            if (properties[i].type) {
                printf(" : %s%s%s", C_CYAN, properties[i].type, C_RESET);
            }
            
            if (properties[i].description) {
                printf("\n    %s%s%s", C_GRAY, properties[i].description, C_RESET);
            }
            
            printf("\n");
        }
    }
    
    // Methods
    if ((sections & SECTION_METHODS) && methods && methods[0].name) {
        printf("\n%sMETHODS:%s\n", C_GREEN, C_RESET);
        
        for (int i = 0; methods[i].name != NULL; i++) {
            printf("  * %s", methods[i].name);
            
            if (methods[i].type) {
                printf(" → %s%s%s", C_CYAN, methods[i].type, C_RESET);
            }
            
            if (methods[i].description) {
                printf("\n    %s%s%s", C_GRAY, methods[i].description, C_RESET);
            }
            
            printf("\n");
        }
    }
    
    // Sample code
    if ((sections & SECTION_SAMPLE) && info->sample_code) {
        printf("\n%sSAMPLE CODE:%s\n", C_YELLOW, C_RESET);
        printf("%s\n", info->sample_code);
    }
    
    printf("\n");
}

void display_help(void) {
    printf("\nXojoDoc v2.0 - Fast Xojo Documentation Browser (C Edition)\n\n");
    printf("USAGE:\n");
    printf("  xojodoc <search_term>          Search for classes, properties, methods\n");
    printf("  xojodoc -c <class_name>        Show class details\n");
    printf("  xojodoc -c <class> -m <method> Show specific method details\n");
    printf("  xojodoc -c <class> -DPMS       Filter sections (D=desc, P=props, M=methods, S=sample)\n");
    printf("  xojodoc --help                 Show this help\n");
    printf("  xojodoc --version              Show version\n\n");
    
    printf("SEARCH:\n");
    printf("  Fuzzy prefix matching (automatic):\n");
    printf("    timer          Matches 'Timer', 'WebTimer', 'IOSTimer', etc.\n");
    printf("    desk           Matches 'Desktop*', 'DeskHelper', etc.\n");
    printf("  \n");
    printf("  List all:\n");
    printf("    *              Shows all classes (up to 20 results)\n\n");
    
    printf("SECTION FILTERS:\n");
    printf("  -D                             Show only description\n");
    printf("  -P                             Show only properties\n");
    printf("  -M                             Show only methods\n");
    printf("  -S                             Show only sample code\n");
    printf("  -PM                            Show properties and methods (no desc/sample)\n");
    printf("  (default: show all sections)\n\n");
    
    printf("EXAMPLES:\n");
    printf("  xojodoc timer                  Find classes starting with 'timer'\n");
    printf("  xojodoc desk                   Find all Desktop* classes\n");
    printf("  xojodoc *                      List all classes\n");
    printf("  xojodoc -c Timer               Show Timer class details (all sections)\n");
    printf("  xojodoc -c Timer -P            Show only Timer properties\n");
    printf("  xojodoc -c Timer -PM           Show Timer properties and methods\n");
    printf("  xojodoc -c Timer -m RunMode    Show Timer.RunMode details\n\n");
    
    printf("DATABASE:\n");
    printf("  Uses xojo.db generated by Python indexer (v1-python)\n");
    printf("  Run 'xojodoc --reindex' in v1-python to update database\n\n");
    fflush(stdout);
}

void display_version(void) {
    printf("XojoDoc v2.0.0-alpha (C Edition)\n");
    printf("Ultra-fast documentation browser for Xojo\n");
    printf("Database: SQLite FTS5\n");
    fflush(stdout);
}
