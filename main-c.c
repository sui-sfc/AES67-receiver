#include <stdio.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>

int
main()
{
 int sock;
 struct sockaddr_in addr;
 struct ip_mreq mreq;

 char buf[2048];

 sock = socket(AF_INET, SOCK_DGRAM, 0);

 addr.sin_family = AF_INET;
 addr.sin_port = htons(12345);
 addr.sin_addr.s_addr = INADDR_ANY;

 bind(sock, (struct sockaddr *)&addr, sizeof(addr));

 /* setsockoptは、bind以降で行う必要あり */
 memset(&mreq, 0, sizeof(mreq));
 mreq.imr_interface.s_addr = INADDR_ANY;
 mreq.imr_multiaddr.s_addr = inet_addr("239.192.1.2");

 if (setsockopt(sock,
	IPPROTO_IP,
	IP_ADD_MEMBERSHIP,
	(char *)&mreq, sizeof(mreq)) != 0) {
	perror("setsockopt");
	return 1;
 }

 memset(buf, 0, sizeof(buf));
 recv(sock, buf, sizeof(buf), 0);

 printf("%s\n", buf);

 close(sock);

 return 0;
}