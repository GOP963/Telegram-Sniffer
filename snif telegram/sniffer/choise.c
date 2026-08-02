#include <stdio.h>
#include <pcap.h>
#include <string.h>
#include <time.h>

struct bpf_program fp;

const char* find_real_adapter(pcap_if_t *alldevs) {
    const char* wifi_candidates[10];
    int wifi_count = 0;
    const char* ethernet_candidate = NULL;

    for (pcap_if_t *d = alldevs; d != NULL; d = d->next) {
        if (!d->description) continue;
        const char* desc = d->description;

        if (strstr(desc, "Virtual") || strstr(desc, "VMware") || strstr(desc, "VirtualBox") ||
            strstr(desc, "Hyper-V") || strstr(desc, "Miniport") || strstr(desc, "Loopback") ||
            strstr(desc, "Bluetooth") || strstr(desc, "Wi-Fi Direct") || strstr(desc, "WAN Miniport") ||
            strstr(desc, "Network Monitor") || strstr(desc, "Adapter for loopback")) {
            continue;
        }

        if (strstr(desc, "Wi-Fi") || strstr(desc, "802.11") || strstr(desc, "Wireless") || strstr(desc, "WLAN")) {
            wifi_candidates[wifi_count++] = d->name;
            if (wifi_count >= 10) break;
            continue;
        }

        if (strstr(desc, "Realtek") || strstr(desc, "Intel") || strstr(desc, "Qualcomm") ||
            strstr(desc, "Atheros") || strstr(desc, "Broadcom")) {
            ethernet_candidate = d->name;
        }
    }

    if (wifi_count > 0) {
        printf("Wi-Fi adapter selected.\n");
        return wifi_candidates[0];
    }
    if (ethernet_candidate) {
        printf("Ethernet adapter selected.\n");
        return ethernet_candidate;
    }
    return NULL;
}

void print_adapter_info(const char *device_name, pcap_if_t *alldevs) {
    for (pcap_if_t *d = alldevs; d; d = d->next) {
        if (strcmp(d->name, device_name) == 0) {
            printf("Listening on: %s\n", d->description ? d->description : d->name);
            return;
        }
    }
}

void packet_handler(u_char *user_data, const struct pcap_pkthdr *header, const u_char *packet) {
    static int count = 0;
    static char detected_ip[16] = {0};

    if (detected_ip[0] != '\0') {
        return;
    }

    if (header->len < 34) return;

    if (packet[12] != 0x08 || packet[13] != 0x00) return;

    const u_char *ip = packet + 14;
    char src_ip[16], dest_ip[16];
    snprintf(src_ip,  sizeof(src_ip),  "%d.%d.%d.%d", ip[12], ip[13], ip[14], ip[15]);
    snprintf(dest_ip, sizeof(dest_ip), "%d.%d.%d.%d", ip[16], ip[17], ip[18], ip[19]);

    count++;

    printf("[Pkt %d] %s -> %s | Len = %d\n",
           count, src_ip, dest_ip, header->len);

    if (count == 3) {
        strcpy(detected_ip, dest_ip);

        printf("\n==========================================\n");
        printf("   Target IP detected: %s\n", detected_ip);
        printf("==========================================\n\n");

        return;
    }
}


int main() {

    pcap_if_t *alldevs = NULL;
    pcap_t *handle = NULL;
    char errbuf[PCAP_ERRBUF_SIZE];

    if (pcap_findalldevs(&alldevs, errbuf) == -1) {
        printf("Error finding devices: %s\n", errbuf);
        return 1;
    }

    const char *device = find_real_adapter(alldevs);
    if (!device) {
        printf("No suitable adapter found.\n");
        pcap_freealldevs(alldevs);
        return 1;
    }

    print_adapter_info(device, alldevs);

    handle = pcap_open_live(device, 65536, 1, 1000, errbuf);
    if (handle == NULL) {
        printf("Could not open device (run as Administrator): %s\n", errbuf);
        pcap_freealldevs(alldevs);
        return 1;
    }

    const char *filter_exp = "udp and (len = 106 or len = 138 or len = 199) and (udp[8] & 0xC0 = 0)";

    if (pcap_compile(handle, &fp, filter_exp, 0, PCAP_NETMASK_UNKNOWN) == -1) {
        printf("Filter compile error: %s\n", pcap_geterr(handle));
        pcap_close(handle);
        pcap_freealldevs(alldevs);
        return 1;
    }
    if (pcap_setfilter(handle, &fp) == -1) {
        printf("Filter set error: %s\n", pcap_geterr(handle));
        pcap_freecode(&fp);
        pcap_close(handle);
        pcap_freealldevs(alldevs);
        return 1;
    }

    printf("Filter: VoIP Call Detection (UDP high ports - Telegram, etc.)\n");
    printf("Capturing... (Ctrl+C to stop)\n");
    printf("----------------------------------------------------\n");

    pcap_loop(handle, 0, packet_handler, NULL);

    pcap_freecode(&fp);
    pcap_close(handle);
    pcap_freealldevs(alldevs);
    return 0;
}