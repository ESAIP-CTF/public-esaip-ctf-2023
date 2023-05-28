#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/stat.h>
#include <fcntl.h>

#define PORT 8080
#define MAX_CLIENTS 5
#define BUFFER_SIZE 1024

void handle_request(int clientSocket);
void render_error_resp(int clientSocket, char *path);
void render_forbidden_resp(int clientSocket, char *path);
int url_decode(char* str);

int isPathSafe(const char* path) {
    // Implement your own logic here to determine if the path is safe
    // You can use whitelist-based checks or regex matching, for example
    // Return 1 if the path is safe, 0 otherwise

    // Example of a simple check: Disallow paths containing '..'
    return (strstr(path, "..") == NULL);
}

void render_file(int fd_socket, int fd_file) {

    char buffer[BUFFER_SIZE];

    ssize_t bytesRead;
    ssize_t bytesSent;
    while ((bytesRead = read(fd_file, buffer, BUFFER_SIZE)) > 0) {
        bytesSent = write(fd_socket, buffer, bytesRead);
        if (bytesSent < 0) {
            perror("Write failed");
            break;
        }
    }

}

int main() {
    int serverSocket, newSocket;
    struct sockaddr_in serverAddress, clientAddress;
    socklen_t clientAddressLength;
    char buffer[BUFFER_SIZE];
    char receivedData[BUFFER_SIZE];

    // Create the socket
    serverSocket = socket(AF_INET, SOCK_STREAM, 0);
    if (serverSocket == -1) {
        perror("Socket creation failed");
        exit(EXIT_FAILURE);
    }

    // Prepare the server address structure
    serverAddress.sin_family = AF_INET;
    serverAddress.sin_addr.s_addr = INADDR_ANY;
    serverAddress.sin_port = htons(PORT);

    // Bind the socket to the server address
    if (bind(serverSocket, (struct sockaddr *)&serverAddress, sizeof(serverAddress)) < 0) {
        perror("Bind failed");
        exit(EXIT_FAILURE);
    }

    // Listen for incoming connections
    if (listen(serverSocket, MAX_CLIENTS) < 0) {
        perror("Listen failed");
        exit(EXIT_FAILURE);
    }

    printf("Server listening on port %d\n", PORT);

    // Accept client connections
    clientAddressLength = sizeof(clientAddress);
    while ((newSocket = accept(serverSocket, (struct sockaddr *)&clientAddress, &clientAddressLength))) {
        printf("New request\n");
 
        handle_request(newSocket);

        close(newSocket);
    }

    if (newSocket == -1) {
        perror("Accept failed");
        exit(EXIT_FAILURE);
    }

    // Close the server socket
    close(serverSocket);

    return 0;
}

void handle_request(int clientSocket) {
    char* buffer = (char*)malloc(BUFFER_SIZE * sizeof(char));
    ssize_t bytesRead;

    // Read client request
    bytesRead = read(clientSocket, buffer, BUFFER_SIZE);
    if (bytesRead <= 0) {
        perror("Read failed");
        free(buffer);
        return;
    }

    // Parse request to get the file path
    char* path_start = strchr(buffer, ' ') + 1;
    char* path_end = strchr(path_start, ' ');
    *path_end = '\0';

    char* path;
    if (!strcmp(path_start, "/")) {
        path = "/index.html";
    }
    else {
        path = path_start;
    }

    const char* base_path = "websrc/";
    size_t full_path_length = strlen(base_path) + strlen(path) + 1;
    char* full_path = (char*)malloc(full_path_length * sizeof(char));

    strcpy(full_path, base_path);
    strcat(full_path, path);

    url_decode(full_path);

    printf("GET %s\n", path);

    if(isPathSafe(full_path)){
        // Open the file for reading
        int fileDescriptor = open(full_path, O_RDONLY);

        if (fileDescriptor == -1) {
            perror("File open failed");

            render_error_resp(clientSocket, path);

            free(full_path);
            free(buffer);

            return;
        }
        else {
            // Send 200 OK response
            const char* okResponse = "HTTP/1.1 200 OK\r\n\r\n";
            write(clientSocket, okResponse, strlen(okResponse));
            render_file(clientSocket, fileDescriptor);
            free(full_path);
        }
        close(fileDescriptor);
    }
    else{
        render_forbidden_resp(clientSocket, path);
    }

    free(buffer);
}

void render_error_resp(int clientSocket, char *path){
    char notFoundResponse[100] = "HTTP/1.1 404 Not Found\r\n\r\nUnable to find ";
    int length = strlen(notFoundResponse);

    // Make a copy of the path
    char* pathCopy = (char*)malloc((strlen(path) + 1) * sizeof(char));
    strcpy(pathCopy, path);

    url_decode(pathCopy);

    sprintf(notFoundResponse + length, pathCopy);
    write(clientSocket, notFoundResponse, strlen(notFoundResponse));

    // Free the dynamically allocated memory
    free(pathCopy);
}

void render_forbidden_resp(int clientSocket, char *path){
    char forbiddenResponse[100] = "HTTP/1.1 403 Forbidden\r\n\r\nForbidden path ";
    int length = strlen(forbiddenResponse);

    // Make a copy of the path
    char* pathCopy = (char*)malloc((strlen(path) + 1) * sizeof(char));
    strcpy(pathCopy, path);

    int size = url_decode(pathCopy);

    for(int i = 0; i < size; i++){
        forbiddenResponse[length + i] = pathCopy[i];
    }
    
    write(clientSocket, forbiddenResponse, strlen(forbiddenResponse));

    // Free the dynamically allocated memory
    free(pathCopy);
}

int url_decode(char* str) {
    int length = strlen(str);
    int read_index = 0;
    int write_index = 0;

    int size = 0;

    while (read_index < length) {
        if (str[read_index] == '%') {
            if (read_index + 2 < length) {
                char hex[3] = { str[read_index + 1], str[read_index + 2], '\0' };
                int value = strtol(hex, NULL, 16);

                // Check if strtol encountered an error during conversion
                if (value == 0 && hex[0] != '0') {
                    read_index++;
                }
                else {
                    str[write_index++] = (char)value;
                    read_index += 3;
                }
            }
            else {
                // Invalid encoded string: '%' character without enough following characters
                str[write_index++] = '\0';
                read_index++;
            }
        }
        else {
            str[write_index++] = str[read_index++];
        }
        size++;
    }

    str[write_index] = '\0';
    return size;
}