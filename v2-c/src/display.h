/**
 * display.h - Terminal output formatting for XojoDoc
 */

#ifndef DISPLAY_H
#define DISPLAY_H

#include "database.h"

/**
 * Display search results in a formatted table
 */
void display_search_results(const SearchResult *results);

/**
 * Display detailed class information
 */
void display_class_details(const ClassInfo *info, const MemberInfo *properties, const MemberInfo *methods);

/**
 * Display error message
 */
void display_error(const char *message);

/**
 * Display help message
 */
void display_help(void);

/**
 * Display version info
 */
void display_version(void);

#endif /* DISPLAY_H */
