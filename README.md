# Telegram-Sniffer
Get Target IP Address By Video Call Or Call Through Libpcap Library

---
Hello. In this project, the goal is to capture video calls exchanged via Telegram—using the pcap library (which powers tools like Nmap and Wireshark)—and display them to the user.
##### The key point here is that for the user to see the target's actual IP address, two conditions regarding the target's settings must be met: first, the target must not have disabled the P2P (peer-to-peer) option—or, more specifically, must not have set it to "Nobody."

#### path: Privacy and security |  Calls | Peer To Peer

<img width="576" height="645" alt="image" src="https://github.com/user-attachments/assets/15583287-0731-42f6-9a27-e3ce47e2772f" />

So, what is the purpose of this Telegram option?

When this feature is enabled for a user, the calls taking place are routed through Telegram's servers; in other words, Telegram acts as a redirector.

<img width="1024" height="1024" alt="image" src="https://github.com/user-attachments/assets/106f1833-e8c2-4587-85a2-9ab194257aee" />

However, if this option has not been disabled or restricted, we can view these packets using specific filters in tools such as Wireshark, Tshark, or other network packet capture utilities like TCPdump—for example, by applying a filter like this in Wireshark.

```
udp && ip.src == 147.135.6.149 && (udp.port >= 10000 || stun)
```

<img width="1697" height="746" alt="image" src="https://github.com/user-attachments/assets/c55acf41-6880-4571-9777-1059f89b68df" />

As you can see, using filters like these allows us to view the sender's IP address in the "Source" field—specifically the IP of the party sending data to us.

Alternatively, we can make our query less specific and simply look for UDP packets.

```
udp.stream eq 0
```

But the question is: what is the STUN protocol?

What is the STUN protocol? (In simple terms)

STUN = Session Traversal Utilities for NAT  

Meaning: NAT traversal tool for communication.

Main problem: NAT (like a home router)

When you call the laptop from your phone, the phone doesn't know its own public IP address and cannot say, "Send the audio to this IP."

What does STUN do?

1. The phone asks the STUN server (e.g., stun.l.google.com:19302 or a Telegram server):

    "Who am I? What is my public IP?"

2. The STUN server replies:

    "From my perspective, you are connecting via IP 185.23.45.67 and port 54321!"

3. The phone sends this information to the other party (the laptop) so it knows where to send the audio.

##### How do you view STUN in Wireshark? STUN filter in Wireshark:

```
udp && stun
```

Or more precisely: 

plaintext

```
udp && (udp.port == 3478 || udp.port == 5349 || udp.port == 19302) && stun
```

We are going to write a C program to accomplish this—but without assuming the user already knows the other party's IP address (unlike the Wireshark filtering method, where the IP was already known). Instead, leveraging Telegram's encryption, we will use the `libpcap` library—which captures network interface packets—to intercept the specific bits used for voice transmission. Then, we will write a Python tool that utilizes design patterns to process this data; it will use a reliable service like IPLogger to resolve the IP address into location and other details, effectively performing a "Whois" lookup and displaying the results in the shell.
