/**
 * main.c - XojoDoc CLI entry point
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "database.h"
#include "display.h"

#define DB_FILENAME "xojo.db"
#define VERSION "2.0.0"
#define MAX_RESULTS 20

// Windows compatibility for strcasecmp
#ifdef _WIN32
    #define strcasecmp _stricmp
    #include <windows.h>
#else
    #include <unistd.h>
    #include <libgen.h>
#endif

// Get database path (same directory as executable)
char* get_db_path(const char *exe_path) {
    static char db_path[1024];
    
    #ifdef _WIN32
        char exe_dir[512];
        GetModuleFileNameA(NULL, exe_dir, sizeof(exe_dir));
        char *last_slash = strrchr(exe_dir, '\\');
        if (last_slash) {
            *last_slash = '\0';
        }
        snprintf(db_path, sizeof(db_path), "%s\\%s", exe_dir, DB_FILENAME);
    #else
        char exe_copy[512];
        strncpy(exe_copy, exe_path, sizeof(exe_copy));
        char *exe_dir = dirname(exe_copy);
        snprintf(db_path, sizeof(db_path), "%s/%s", exe_dir, DB_FILENAME);
    #endif
    
    return db_path;
}

int main(int argc, char *argv[]) {
    // No arguments - show help
    if (argc < 2) {
        display_help();
        return 0;
    }

    // Parse arguments
    const char *command = argv[1];
    
    // --help
    if (strcmp(command, "--help") == 0 || strcmp(command, "-h") == 0) {
        display_help();
        return 0;
    }
    
    // --version
    if (strcmp(command, "--version") == 0 || strcmp(command, "-v") == 0) {
        display_version();
        return 0;
    }
    
    // Get database path (next to executable)
    const char *db_path = get_db_path(argv[0]);
    
    // Open database
    sqlite3 *db = db_open(db_path);
    if (!db) {
        fprintf(stderr, "ERROR: Database not found: %s\n\n", db_path);
        fprintf(stderr, "Please ensure xojo.db is in the same directory as xojodoc.exe\n");
        fprintf(stderr, "To create the database, run:\n");
        fprintf(stderr, "  cd v1-python\n");
        fprintf(stderr, "  xojodoc --reindex\n");
        fprintf(stderr, "  copy xojo.db <path-to-xojodoc-exe>\n\n");
        fflush(stderr);
        return 1;
    }
    
    // -c CLASS [-m METHOD] [-DPMS]
    if (strcmp(command, "-c") == 0) {
        if (argc < 3) {
            display_error("Usage: xojodoc -c <class> [-m <method>] [-DPMS]");
            db_close(db);
            return 1;
        }
        
        const char *class_name = argv[2];
        int sections = 0;  // 0 means SECTION_ALL
        int member_index = -1;
        const char *member_name = NULL;
        
        // Parse optional flags
        for (int i = 3; i < argc; i++) {
            if (strcmp(argv[i], "-m") == 0 && i + 1 < argc) {
                member_name = argv[i + 1];
                member_index = i;
                i++;  // Skip next arg
            } else if (argv[i][0] == '-') {
                // Parse section flags: -D, -P, -M, -S
                for (int j = 1; argv[i][j] != '\0'; j++) {
                    switch (argv[i][j]) {
                        case 'D': sections |= SECTION_DESCRIPTION; break;
                        case 'P': sections |= SECTION_PROPERTIES; break;
                        case 'M': sections |= SECTION_METHODS; break;
                        case 'S': sections |= SECTION_SAMPLE; break;
                        default:
                            fprintf(stderr, "Unknown flag: -%c\n", argv[i][j]);
                            fprintf(stderr, "Valid flags: -D (description), -P (properties), -M (methods), -S (sample)\n");
                            db_close(db);
                            return 1;
                    }
                }
            }
        }
        
        // If no sections specified, show all
        if (sections == 0) {
            sections = SECTION_ALL;
        }
        
        // Get class info
        ClassInfo *class_info = db_get_class(db, class_name);
        if (!class_info) {
            fprintf(stderr, "Class '%s' not found.\n", class_name);
            db_close(db);
            return 1;
        }
        
        // If -m specified, show only method/property
        if (member_name) {
            
            // Search in properties first
            MemberInfo *properties = db_get_properties(db, class_info->id);
            int found = 0;
            
            for (int i = 0; properties && properties[i].name != NULL; i++) {
                if (strcasecmp(properties[i].name, member_name) == 0) {
                    printf("\n%s.%s (Property)\n", class_name, properties[i].name);
                    if (properties[i].type) {
                        printf("Type: %s\n", properties[i].type);
                    }
                    if (properties[i].description) {
                        printf("\n%s\n", properties[i].description);
                    }
                    found = 1;
                    break;
                }
            }
            
            // If not found in properties, search in methods
            if (!found) {
                MemberInfo *methods = db_get_methods(db, class_info->id);
                
                for (int i = 0; methods && methods[i].name != NULL; i++) {
                    if (strcasecmp(methods[i].name, member_name) == 0) {
                        printf("\n%s.%s (Method)\n", class_name, methods[i].name);
                        if (methods[i].type) {
                            printf("Returns: %s\n", methods[i].type);
                        }
                        if (methods[i].description) {
                            printf("\n%s\n", methods[i].description);
                        }
                        found = 1;
                        break;
                    }
                }
                
                db_free_member_info(methods);
            }
            
            if (!found) {
                fprintf(stderr, "Member '%s' not found in class '%s'.\n", member_name, class_name);
                fflush(stderr);
            } else {
                printf("\n");
                fflush(stdout);
            }
            
            db_free_member_info(properties);
        } else {
            // Show full class details with section filters
            MemberInfo *properties = db_get_properties(db, class_info->id);
            MemberInfo *methods = db_get_methods(db, class_info->id);
            
            display_class_details(class_info, properties, methods, sections);
            
            db_free_member_info(properties);
            db_free_member_info(methods);
        }
        
        db_free_class_info(class_info);
        db_close(db);
        return 0;
    }
    
    // Default: search query
    const char *query = command;
    SearchResult *results = db_search(db, query, MAX_RESULTS);
    
    if (!results || results[0].class_name == NULL) {
        printf("No results found for '%s'.\n", query);
        db_free_search_results(results);
        db_close(db);
        return 0;
    }
    
    display_search_results(results);
    
    db_free_search_results(results);
    db_close(db);
    return 0;
}
