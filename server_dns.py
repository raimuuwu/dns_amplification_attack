
from socketserver import UDPServer, BaseRequestHandler
from dnslib import DNSRecord, RR, A, TXT, QTYPE, RCODE

# Konfiguracja serwera
HOST = "10.0.2.1"
PORT = 53

# Dozwolone rzeczywiste adresy klientów
ALLOWED_CLIENTS = {
    "10.0.1.1",  # attacker
    "10.0.1.2",  # legit_pc2
}


class DNSHandler(BaseRequestHandler):

    def handle(self):
        data, sock = self.request
        client_ip = self.client_address[0]

        try:
            request = DNSRecord.parse(data)

            # Kontrola adresu nadawcy
            if client_ip not in ALLOWED_CLIENTS:
                print(f"Odrzucono zapytanie z: {client_ip}")
                reply = request.reply()
                reply.header.rcode = RCODE.REFUSED
                sock.sendto(reply.pack(), self.client_address)
                return

            reply = request.reply()
            reply.header.aa = 1
            reply.header.ra = 0

            for question in request.questions:
                name = str(question.qname).rstrip(".")
                record_type = QTYPE[question.qtype]

                print(
                    f"Klient: {client_ip} | "
                    f"Domena: {name} | "
                    f"Typ: {record_type} | "
                    f"Rozmiar: {len(data)} B"
                )

                if name == "lab.test" and record_type == "A":
                    reply.add_answer(
                        RR(
                            "lab.test",
                            QTYPE.A,
                            rdata=A("192.0.2.10"),
                            ttl=60
                        )
                    )

                elif name == "info.lab.test" and record_type == "TXT":
                    reply.add_answer(
                        RR(
                            "info.lab.test",
                            QTYPE.TXT,
                            rdata=TXT("Kontrolny rekord TXT serwera laboratoryjnego"),
                            ttl=60
                        )
                    )

            response = reply.pack()

            sock.sendto(response, self.client_address)

            print(f"Wysłano odpowiedź: {len(response)} B\n")

        except Exception as error:
            print(f"Błąd obsługi DNS: {error}")


if __name__ == "__main__":

    with UDPServer((HOST, PORT), DNSHandler) as server:
        print(f"Serwer DNS uruchomiony na {HOST}:{PORT}")
        server.serve_forever()
