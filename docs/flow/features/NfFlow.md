| No. | Feature Name                                         | Description                                                             |
|-----|------------------------------------------------------|-------------------------------------------------------------------------|
| 1   | **Flow ID**                                          | Unique identifier for the network flow                                  |
| 2   | **Source IP**                                        | Source IP address                                |
| 3   | **Source Port**                                      | Source Network port                              |
| 4   | **Destination IP**                                   | Destination IP address                                 |
| 5   | **Destination Port**                                 | Destination Network port                               |
| 6   | **Protocol**                                         | Transport layer protocol used                                           |
| 7   | **Start Time (Milliseconds since UNIX Epoch)**       | Start time of the flow in milliseconds since the UNIX epoch             |
| 8   | **End Time (Milliseconds since UNIX Epoch)**         | End time of the flow in milliseconds since the UNIX epoch               |
| 9   | **Flow Duration (Milliseconds)**                     | Total duration of the flow in milliseconds                              |
| 10  | **Total Packet Count**                               | Total number of packets in the flow (ingress + egress)                  |
| 11  | **Total Packet Length**                              | Total length of packets in the flow (ingress + egress)                  |
| 12  | **Ingress First Timestamp (Milliseconds since UNIX Epoch)** | First timestamp of ingress traffic in milliseconds since UNIX epoch |
| 13  | **Ingress Last Timestamp (Milliseconds since UNIX Epoch)** | Last timestamp of ingress traffic in milliseconds since UNIX epoch  |
| 14  | **Ingress Duration (Milliseconds)**                  | Duration of ingress traffic in milliseconds                             |
| 15  | **Ingress Packet Count**                             | Number of packets in the ingress traffic                                |
| 16  | **Ingress Packet Total Length**                      | Total length of ingress packets                                         |
| 17  | **Egress First Timestamp (Milliseconds since UNIX Epoch)** | First timestamp of egress traffic in milliseconds since UNIX epoch |
| 18  | **Egress Last Timestamp (Milliseconds since UNIX Epoch)** | Last timestamp of egress traffic in milliseconds since UNIX epoch  |
| 19  | **Egress Duration (Milliseconds)**                   | Duration of egress traffic in milliseconds                              |
| 20  | **Egress Packet Count**                              | Number of packets in the egress traffic                                 |
| 21  | **Egress Packet Total Length**                       | Total length of egress packets                                          |
| 22  | **Minimum Flow Packet Length**                       | Minimum length of packets in the flow                                   |
| 23  | **Mean Flow Packet Length**                          | Average length of packets in the flow                                   |
| 24  | **Standard Deviation of Flow Packet Length**         | Standard deviation of packet lengths in the flow                        |
| 25  | **Maximum Flow Packet Length**                       | Maximum length of packets in the flow                                   |
| 26  | **Minimum Ingress Packet Length**                    | Minimum length of ingress packets                                       |
| 27  | **Mean Ingress Packet Length**                       | Average length of ingress packets                                       |
| 28  | **Standard Deviation of Ingress Packet Length**      | Standard deviation of ingress packet lengths                            |
| 29  | **Maximum Ingress Packet Length**                    | Maximum length of ingress packets                                       |
| 30  | **Minimum Egress Packet Length**                     | Minimum length of egress packets                                        |
| 31  | **Mean Egress Packet Length**                        | Average length of egress packets                                        |
| 32  | **Standard Deviation of Egress Packet Length**       | Standard deviation of egress packet lengths                             |
| 33  | **Maximum Egress Packet Length**                     | Maximum length of egress packets                                        |
| 34  | **Minimum Flow Inter-Arrival Time (Milliseconds)**        | Minimum time between packets in the flow (converted to Milliseconds)         |
| 35  | **Mean Flow Inter-Arrival Time (Milliseconds)**           | Average time between packets in the flow (converted to Milliseconds)         |
| 36  | **Standard Deviation of Flow Inter-Arrival Time (Milliseconds)** | Standard deviation of times between packets in the flow (Milliseconds)  |
| 37  | **Maximum Flow Inter-Arrival Time (Milliseconds)**        | Maximum time between packets in the flow (converted to Milliseconds)         |
| 38  | **Minimum Ingress Inter-Arrival Time (Milliseconds)**     | Minimum time between ingress packets (converted to Milliseconds)             |
| 39  | **Mean Ingress Inter-Arrival Time (Milliseconds)**        | Average time between ingress packets (converted to Milliseconds)             |
| 40  | **Standard Deviation of Ingress Inter-Arrival Time (Milliseconds)** | Standard deviation of times between ingress packets (Milliseconds)     |
| 41  | **Maximum Ingress Inter-Arrival Time (Milliseconds)**     | Maximum time between ingress packets (converted to Milliseconds)             |
| 42  | **Minimum Egress Inter-Arrival Time (Milliseconds)**      | Minimum time between egress packets (converted to Milliseconds)              |
| 43  | **Mean Egress Inter-Arrival Time (Milliseconds)**         | Average time between egress packets (converted to Milliseconds)              |
| 44  | **Standard Deviation of Egress Inter-Arrival Time (Milliseconds)** | Standard deviation of times between egress packets (Milliseconds)      |
| 45  | **Maximum Egress Inter-Arrival Time (Milliseconds)**      | Maximum time between egress packets (converted to Milliseconds)              |
| 46  | **Total SYN Flag Count**                            | Total number of SYN flags seen in the flow                              |
| 47  | **Total CWE Flag Count**                            | Total number of CWE flags seen in the flow                              |
| 48  | **Total ECE Flag Count**                            | Total number of ECE flags seen in the flow                              |
| 49  | **Total URG Flag Count**                            | Total number of URG flags seen in the flow                              |
| 50  | **Total ACK Flag Count**                            | Total number of ACK flags seen in the flow                              |
| 51  | **Total PSH Flag Count**                            | Total number of PSH flags seen in the flow                              |
| 52  | **Total RST Flag Count**                            | Total number of RST flags seen in the flow                              |
| 53  | **Total FIN Flag Count**                            | Total number of FIN flags seen in the flow                              |
| 54  | **Ingress SYN Flag Count**                          | Number of SYN flags seen in ingress traffic                             |
| 55  | **Ingress CWE Flag Count**                          | Number of CWE flags seen in ingress traffic                             |
| 56  | **Ingress ECE Flag Count**                          | Number of ECE flags seen in ingress traffic                             |
| 57  | **Ingress URG Flag Count**                          | Number of URG flags seen in ingress traffic                             |
| 58  | **Ingress ACK Flag Count**                          | Number of ACK flags seen in ingress traffic                             |
| 59  | **Ingress PSH Flag Count**                          | Number of PSH flags seen in ingress traffic                             |
| 60  | **Ingress RST Flag Count**                          | Number of RST flags seen in ingress traffic                             |
| 61  | **Ingress FIN Flag Count**                          | Number of FIN flags seen in ingress traffic                             |
| 62  | **Egress SYN Flag Count**                           | Number of SYN flags seen in egress traffic                              |
| 63  | **Egress CWE Flag Count**                           | Number of CWE flags seen in egress traffic                              |
| 64  | **Egress ECE Flag Count**                           | Number of ECE flags seen in egress traffic                              |
| 65  | **Egress URG Flag Count**                           | Number of URG flags seen in egress traffic                              |
| 66  | **Egress ACK Flag Count**                           | Number of ACK flags seen in egress traffic                              |
| 67  | **Egress PSH Flag Count**                           | Number of PSH flags seen in egress traffic                              |
| 68  | **Egress RST Flag Count**                           | Number of RST flags seen in egress traffic                              |
| 69  | **Egress FIN Flag Count**                           | Number of FIN flags seen in egress traffic                              |