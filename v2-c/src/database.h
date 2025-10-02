/**
 * database.h - SQLite FTS5 database interface for XojoDoc
 */

#ifndef DATABASE_H
#define DATABASE_H

#include <sqlite3.h>

/**
 * Search result entry
 */
typedef struct {
    char *class_name;
    char *module;
    char *description;
    int rank;
} SearchResult;

/**
 * Class details
 */
typedef struct {
    int id;
    char *name;
    char *module;
    char *description;
    char *sample_code;
    char *compatibility;
} ClassInfo;

/**
 * Property/Method info
 */
typedef struct {
    char *name;
    char *type;
    char *description;
} MemberInfo;

/**
 * Open database connection
 * Returns: sqlite3* on success, NULL on failure
 */
sqlite3* db_open(const char *db_path);

/**
 * Close database connection
 */
void db_close(sqlite3 *db);

/**
 * Search classes using FTS5
 * Returns: Array of SearchResult (NULL-terminated)
 * @param include_deprecated If 0, exclude deprecated classes
 */
SearchResult* db_search(sqlite3 *db, const char *query, int max_results, int include_deprecated);

/**
 * Get class details by name
 * Returns: ClassInfo* on success, NULL if not found
 */
ClassInfo* db_get_class(sqlite3 *db, const char *class_name);

/**
 * Get properties for a class
 * Returns: Array of MemberInfo (NULL-terminated)
 */
MemberInfo* db_get_properties(sqlite3 *db, int class_id);

/**
 * Get methods for a class
 * Returns: Array of MemberInfo (NULL-terminated)
 */
MemberInfo* db_get_methods(sqlite3 *db, int class_id);

/**
 * Free search results
 */
void db_free_search_results(SearchResult *results);

/**
 * Free class info
 */
void db_free_class_info(ClassInfo *info);

/**
 * Free member info array
 */
void db_free_member_info(MemberInfo *members);

#endif /* DATABASE_H */
