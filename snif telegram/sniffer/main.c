#include <stdio.h>
#include <pcap.h>
#include <Windows.h>

int main(){
    system("cls");
    pcap_if_t *allodevice,*d;
    char errbuf[PCAP_ERRBUF_SIZE];
    if (pcap_findalldevs(&allodevice, errbuf) == -1){
        printf("NIC Not Found \n");
        return 1;
    }
    printf("                                                    Your NIC\n");
    for (d = allodevice; d; d = d->next){
        printf("[*]",d->name);
        if(d->description) printf("(%s)",d->description);
        printf("\n");

    }
    pcap_freealldevs(allodevice);
    return 0;

}