/**
 * database.c - SQLite FTS5 database implementation
 */

#include "database.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

sqlite3* db_open(const char *db_path) {
    sqlite3 *db = NULL;
    int rc = sqlite3_open(db_path, &db);
    
    if (rc != SQLITE_OK) {
        fprintf(stderr, "Cannot open database: %s\n", sqlite3_errmsg(db));
        sqlite3_close(db);
        return NULL;
    }
    
    return db;
}

void db_close(sqlite3 *db) {
    if (db) {
        sqlite3_close(db);
    }
}

SearchResult* db_search(sqlite3 *db, const char *query, int max_results) {
    const char *sql = 
        "SELECT c.name, c.module, c.description "
        "FROM classes c "
        "JOIN search_index si ON c.id = si.rowid "
        "WHERE search_index MATCH ? "
        "ORDER BY rank "
        "LIMIT ?";
    
    sqlite3_stmt *stmt;
    int rc = sqlite3_prepare_v2(db, sql, -1, &stmt, NULL);
    
    if (rc != SQLITE_OK) {
        fprintf(stderr, "SQL error: %s\n", sqlite3_errmsg(db));
        return NULL;
    }
    
    sqlite3_bind_text(stmt, 1, query, -1, SQLITE_STATIC);
    sqlite3_bind_int(stmt, 2, max_results);
    
    // Allocate result array
    SearchResult *results = calloc(max_results + 1, sizeof(SearchResult));
    int i = 0;
    
    while (sqlite3_step(stmt) == SQLITE_ROW && i < max_results) {
        const unsigned char *name = sqlite3_column_text(stmt, 0);
        const unsigned char *module = sqlite3_column_text(stmt, 1);
        const unsigned char *desc = sqlite3_column_text(stmt, 2);
        
        results[i].class_name = strdup((const char*)name);
        results[i].module = strdup((const char*)module);
        results[i].description = desc ? strdup((const char*)desc) : NULL;
        results[i].rank = i;
        i++;
    }
    
    // NULL-terminate
    results[i].class_name = NULL;
    
    sqlite3_finalize(stmt);
    return results;
}

ClassInfo* db_get_class(sqlite3 *db, const char *class_name) {
    const char *sql = 
        "SELECT id, name, module, description, sample_code, compatibility "
        "FROM classes "
        "WHERE name = ? COLLATE NOCASE";
    
    sqlite3_stmt *stmt;
    int rc = sqlite3_prepare_v2(db, sql, -1, &stmt, NULL);
    
    if (rc != SQLITE_OK) {
        fprintf(stderr, "SQL error: %s\n", sqlite3_errmsg(db));
        return NULL;
    }
    
    sqlite3_bind_text(stmt, 1, class_name, -1, SQLITE_STATIC);
    
    ClassInfo *info = NULL;
    
    if (sqlite3_step(stmt) == SQLITE_ROW) {
        info = calloc(1, sizeof(ClassInfo));
        
        info->id = sqlite3_column_int(stmt, 0);
        
        const unsigned char *name = sqlite3_column_text(stmt, 1);
        const unsigned char *module = sqlite3_column_text(stmt, 2);
        const unsigned char *desc = sqlite3_column_text(stmt, 3);
        const unsigned char *sample = sqlite3_column_text(stmt, 4);
        const unsigned char *compat = sqlite3_column_text(stmt, 5);
        
        info->name = strdup((const char*)name);
        info->module = strdup((const char*)module);
        info->description = desc ? strdup((const char*)desc) : NULL;
        info->sample_code = sample ? strdup((const char*)sample) : NULL;
        info->compatibility = compat ? strdup((const char*)compat) : NULL;
    }
    
    sqlite3_finalize(stmt);
    return info;
}

MemberInfo* db_get_properties(sqlite3 *db, int class_id) {
    const char *sql = 
        "SELECT name, type, description "
        "FROM properties "
        "WHERE class_id = ? "
        "ORDER BY name";
    
    sqlite3_stmt *stmt;
    sqlite3_prepare_v2(db, sql, -1, &stmt, NULL);
    sqlite3_bind_int(stmt, 1, class_id);
    
    // Count results first
    int count = 0;
    while (sqlite3_step(stmt) == SQLITE_ROW) count++;
    sqlite3_reset(stmt);
    
    MemberInfo *members = calloc(count + 1, sizeof(MemberInfo));
    int i = 0;
    
    while (sqlite3_step(stmt) == SQLITE_ROW) {
        const unsigned char *name = sqlite3_column_text(stmt, 0);
        const unsigned char *type = sqlite3_column_text(stmt, 1);
        const unsigned char *desc = sqlite3_column_text(stmt, 2);
        
        members[i].name = strdup((const char*)name);
        members[i].type = type ? strdup((const char*)type) : NULL;
        members[i].description = desc ? strdup((const char*)desc) : NULL;
        i++;
    }
    
    members[i].name = NULL; // NULL-terminate
    
    sqlite3_finalize(stmt);
    return members;
}

MemberInfo* db_get_methods(sqlite3 *db, int class_id) {
    const char *sql = 
        "SELECT name, return_type, description "
        "FROM methods "
        "WHERE class_id = ? "
        "ORDER BY name";
    
    sqlite3_stmt *stmt;
    sqlite3_prepare_v2(db, sql, -1, &stmt, NULL);
    sqlite3_bind_int(stmt, 1, class_id);
    
    // Count results first
    int count = 0;
    while (sqlite3_step(stmt) == SQLITE_ROW) count++;
    sqlite3_reset(stmt);
    
    MemberInfo *members = calloc(count + 1, sizeof(MemberInfo));
    int i = 0;
    
    while (sqlite3_step(stmt) == SQLITE_ROW) {
        const unsigned char *name = sqlite3_column_text(stmt, 0);
        const unsigned char *type = sqlite3_column_text(stmt, 1);
        const unsigned char *desc = sqlite3_column_text(stmt, 2);
        
        members[i].name = strdup((const char*)name);
        members[i].type = type ? strdup((const char*)type) : NULL;
        members[i].description = desc ? strdup((const char*)desc) : NULL;
        i++;
    }
    
    members[i].name = NULL; // NULL-terminate
    
    sqlite3_finalize(stmt);
    return members;
}

void db_free_search_results(SearchResult *results) {
    if (!results) return;
    
    for (int i = 0; results[i].class_name != NULL; i++) {
        free(results[i].class_name);
        free(results[i].module);
        if (results[i].description) free(results[i].description);
    }
    
    free(results);
}

void db_free_class_info(ClassInfo *info) {
    if (!info) return;
    
    free(info->name);
    free(info->module);
    if (info->description) free(info->description);
    if (info->sample_code) free(info->sample_code);
    if (info->compatibility) free(info->compatibility);
    free(info);
}

void db_free_member_info(MemberInfo *members) {
    if (!members) return;
    
    for (int i = 0; members[i].name != NULL; i++) {
        free(members[i].name);
        if (members[i].type) free(members[i].type);
        if (members[i].description) free(members[i].description);
    }
    
    free(members);
}
