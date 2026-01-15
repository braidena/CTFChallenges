#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdbool.h>


// NOTES AND IDEAS
// - Make a menu so that its like System Query option1 option2
// - Make it so that it doesnt check the length of option2
// - If option1 doesnt match to system, sprintf log the error, this is the buffer overflow
// - Since its sprintf, will need to pivot ROP chain to somewhere where you can write null bytes
// - Make system information like 1000 bytes long so you can leak and write rop chain there

const char *globalLogs[] = {
    "System started successfully.",
    "User admin logged in.",
    "Error: Invalid password attempt.",
    "Network connection established.",
    "Warning: Low disk space on drive C:."
};

char systemDescription[1024] = "Blah blah blah this device is super secret blah blah blah\n";

char systemVersion[64] = "Version 1.0.0\n";
char systemUptime[64] = "Uptime: 24 hours\n";


int printSystemCommands() {
    printf("? - Help menu / See options for commands Ex: info ?\n");
    printf("query - Search system logs for items\n");
    printf("info - Display system information\n");
    printf("settings - Change system settings\n");
    printf("quit - Exit\n\n");
    return 0;
}

int querySystemLogs(char *options) {
    char errorBuffer[24];
    bool found = false;
    if (strlen(options) == 0) {
        printf("Invalid!\n");
        return 0;
    }
    if (strncmp(options, "?", 1) == 0 ) {
        printf("Usage: query <search_term>\n");
        return 0;
    }
    printf("Searching logs for: %s...\n", options);
    for (int i = 0; i < 5; i++) {
        if (strstr(globalLogs[i], options) != NULL) {
            printf("Log found: %s\n", globalLogs[i]);
            found = true;
        }
    }
    if (found == true) {
        printf("Search complete.\n");
    }
    else {
        sprintf(errorBuffer, "No logs found for: %s", options);
        printf("%s\n", errorBuffer);
    }
    return 0;
}

int infoSystem(char *options) {
    if (strlen(options) == 0) {
        printf("Invalid!\n");
        return 0;
    }
    if (strncmp(options, "?", 1) == 0 ) {
        printf("Usage: info <version or uptime>\n");
        return 0;
    }
    if (strncmp(options, "version", 7) == 0 ) {
        printf(systemVersion);
        return 0;
    }
    if (strncmp(options, "uptime", 6) == 0 ) {
        printf(systemUptime);
        return 0;
    }
    if (strncmp(options, "description", 11) == 0 ) {
        printf(systemDescription);
        return 0;
    }
    printf("Unknown system info request.\n");
    return 0;
}

int settingsSystem(char *options) {
    char *settingName;
    char changeValue[1024];
    if (strlen(options) == 0) {
        printf("Invalid!\n");
        return 0;
    }
    if (strncmp(options, "?", 1) == 0 ) {
        printf("Usage: settings <setting_name> <change_value>\n");
        return 0;
    }
    settingName = strtok(options, " ");
    strcpy(changeValue, strtok(NULL, " "));

    if (strcmp(settingName, "description") == 0) {
        memcpy(systemDescription, changeValue, 1024);
        printf("System description updated.\n");
        return 0;
    }
    if (strcmp(settingName, "version") == 0) {
        memcpy(systemVersion, changeValue, 64);
        printf("System version updated.\n");
        return 0;
    }
    if (strcmp(settingName, "uptime") == 0) {
        memcpy(systemUptime, changeValue, 64);
        printf("System uptime updated.\n");
        return 0;
    }
    printf("Invalid setting or value.\n");
    return 0;
}



int main() {
    char buffer[100];
    int userInput;
    printf("\n---- SYSTEM CONSOLE ----\n");
    printSystemCommands();

    while (1) {

        printf("> ");
        fgets(buffer, sizeof(buffer), stdin);

        if (strncmp(buffer, "quit", 4) == 0) {
            printf("Exiting system console.\n");
            break;

        } else if (strncmp(buffer, "?", 1) == 0) {
            printSystemCommands();

        } else if (strncmp(buffer, "query", 5) == 0) {
            char options[100];
            // Copy user input after "query " into options
            strncpy(options, buffer + 6, sizeof(options) - 1);
            options[sizeof(options) - 1] = '\0'; // Ensure null-termination
            // Remove newline character from options if present
            options[strcspn(options, "\n")] = 0;
            querySystemLogs(options);

        } else if (strncmp(buffer, "info", 4) == 0) {
            char options[100];
            // Copy user input after "info " into options
            strncpy(options, buffer + 5, sizeof(options) - 1);
            options[sizeof(options) - 1] = '\0'; // Ensure null-termination
            // Remove newline character from options if present
            options[strcspn(options, "\n")] = 0;
            infoSystem(options);

        } else if (strncmp(buffer, "settings", 8) == 0) {
            char options[100];
            // Copy user input after "settings " into options
            strncpy(options, buffer + 9, sizeof(options) - 1);
            options[sizeof(options) - 1] = '\0'; // Ensure null-termination
            // Remove newline character from options if present
            options[strcspn(options, "\n")] = 0;
            settingsSystem(options);

        } else {
            printf("Unknown command. Type '?' for help.\n");
        }
        memset(buffer, 0, sizeof(buffer));
    }

    return 0;
}
