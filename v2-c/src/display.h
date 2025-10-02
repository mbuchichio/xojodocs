/**
 * display.h - Terminal output formatting for XojoDoc
 */

#ifndef DISPLAY_H
#define DISPLAY_H

#include "database.h"

// Section filters for display_class_details
#define SECTION_DESCRIPTION  0x01
#define SECTION_PROPERTIES   0x02
#define SECTION_METHODS      0x04
#define SECTION_SAMPLE       0x08
#define SECTION_ALL          (SECTION_DESCRIPTION | SECTION_PROPERTIES | SECTION_METHODS | SECTION_SAMPLE)

/**
 * Display search results in a formatted table
 */
void display_search_results(const SearchResult *results);

/**
 * Display detailed class information
 * @param sections Bitmask of SECTION_* flags to display (default: SECTION_ALL)
 */
void display_class_details(const ClassInfo *info, const MemberInfo *properties, const MemberInfo *methods, int sections);

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
