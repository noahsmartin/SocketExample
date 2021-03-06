/*
 * client.c - Socket client example based off Beej's guide
 * Capitalizes the text sent by the server
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <unistd.h>
#include <ctype.h>

#define BUFFSIZE 104857600

int main(int argc, char *argv[])
{
    struct addrinfo hints, *res, *addr_list;
    int status;

    FILE *outfile;

    if (argc != 3) {
      printf("usage: %s <hostname> <outfile>\n", argv[0]);
        return 1;
    }

    memset(&hints, 0, sizeof hints);
    hints.ai_family = AF_UNSPEC; // AF_INET or AF_INET6 to force version
    hints.ai_socktype = SOCK_STREAM;
    hints.ai_protocol = getprotobyname("tcp")->p_proto;

    if ((status = getaddrinfo(argv[1], "3490", &hints, &res)) != 0) {
        fprintf(stderr, "getaddrinfo: %s\n", gai_strerror(status));
        return 2;
    }

    printf("Trying to connect to %s:\n", argv[1]);

    int fd;
    for(addr_list = res; addr_list != NULL; addr_list = addr_list->ai_next) {
        void *addr;

        
        fd = socket(addr_list->ai_family, addr_list->ai_socktype, addr_list->ai_protocol);
        if(connect(fd, addr_list->ai_addr, addr_list->ai_addrlen))
        {
            close(fd);
            continue;
        }
           
        // This addrinfo worked, continue connecting
        printf("connected to %s with %s and %s\n", argv[1], addr_list->ai_family == AF_INET ? "ipv4" : "ipv6", addr_list->ai_protocol == getprotobyname("tcp")->p_proto ? "TCP" : "UDP");
        break;
    }

    if(addr_list == NULL)
    {
        printf("Could not connect to %s\n", argv[1]);
        return 2;
    }

    outfile = fopen(argv[2], "w");


    unsigned char* rec = (unsigned char*) malloc(BUFFSIZE);
    int len;
    while((len = recv(fd, rec, BUFFSIZE, 0)) > 0)
    {
    	int i;
    	for(i = 0; i < len; i++)
    	{
    		fputc(rec[i], outfile);
    	}
    }
    if(len == -1)
    {
    	perror("recv error");
    	close(fd);
    	return 2;
    }

    close(fd);
    fclose(outfile);
    free(rec);
    freeaddrinfo(res); // free the linked list

    return 0;
}