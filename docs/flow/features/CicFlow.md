| No. | Feature Name                                       | Description                                                             |
|-----|----------------------------------------------------|-------------------------------------------------------------------------|
| 1   | **Flow ID**                                        | Unique identifier for the network flow                                  |
| 2   | **Source IP**                                      | IP address of the source                                                |
| 3   | **Source Port**                                    | Network port of the source                                              |
| 4   | **Destination IP**                                 | IP address of the destination                                           |
| 5   | **Destination Port**                               | Network port of the destination                                         |
| 6   | **Protocol**                                       | Transport layer protocol used                                           |
| 7   | **Start Time**                                     | Timestamp when the flow started                                         |
| 8   | **End Time**                                       | Timestamp When the Flow Ended                                           |
| 9   | **Duration**                                       | Total duration of the flow in microseconds                              |
| 10   | **Forward Packet Count**                           | Number of packets from ingress traffic                                  |
| 11  | **Backward Packet Count**                          | Number of packets from egress traffic                                   |
| 12  | **Total Forward Packet Length**                    | Total size of packets from ingress traffic                              |
| 13  | **Total Backward Packet Length**                   | Total size of packets from egress traffic                               |
| 14  | **Maximum Forward Packet Length**                  | Maximum size of a single packet from ingress traffic                    |
| 15  | **Minimum Forward Packet Length**                  | Minimum size of a single packet from ingress traffic                    |
| 16  | **Mean Forward Packet Length**                     | Average size of packets from ingress traffic                            |
| 17  | **Standard Deviation of Forward Packet Length**    | Standard deviation in size of packets from ingress traffic              |
| 18  | **Maximum Backward Packet Length**                 | Maximum size of a single packet from egress traffic                      |
| 19  | **Minimum Backward Packet Length**                 | Minimum size of a single packet from egress traffic                      |
| 20  | **Mean Backward Packet Length**                    | Average size of packets sent from egress traffic                              |
| 21  | **Standard Deviation of Backward Packet Length**   | Standard deviation in size of packets from egress traffic                |
| 22  | **Flow Bytes per Second**                          | Average flow byte rate                                                  |
| 23  | **Flow Packets per Second**                        | Average flow packet rate                                                |
| 24  | **Mean Inter-Arrival Time of Flow**                | Average time between packets in the flow                                |
| 25  | **Standard Deviation of Inter-Arrival Time**       | Standard deviation of time between packets in the flow                  |
| 26  | **Maximum Inter-Arrival Time**                     | Maximum time between packets in the flow                                |
| 27  | **Minimum Inter-Arrival Time**                     | Minimum time between packets in the flow                                |
| 28  | **Total Forward Inter-Arrival Time**               | Total time between packets from ingress traffic                         |
| 29  | **Mean Forward Inter-Arrival Time**                | Average time between packets from ingress traffic                       |
| 30  | **Standard Deviation of Forward Inter-Arrival Time** | Standard deviation of time between packets from ingress traffic       |
| 31  | **Maximum Forward Inter-Arrival Time**             | Maximum time between packets from ingress traffic                       |
| 32  | **Minimum Forward Inter-Arrival Time**             | Minimum time between packets from ingress traffic                       |
| 33  | **Total Backward Inter-Arrival Time**              | Total time between packets from egress traffic                           |
| 34  | **Mean Backward Inter-Arrival Time**               | Average time between packets from egress traffic                         |
| 35  | **Standard Deviation of Backward Inter-Arrival Time** | Standard deviation of time between packets from egress traffic         |
| 36  | **Maximum Backward Inter-Arrival Time**            | Maximum time between packets from egress traffic                         |
| 37  | **Minimum Backward Inter-Arrival Time**            | Minimum time between packets from egress traffic                         |
| 38  | **Forward PSH Flag Count**                         | Number of PSH flags set in packets from ingress traffic                 |
| 39  | **Backward PSH Flag Count**                        | Number of PSH flags set in packets from egress traffic                   |
| 40  | **Forward URG Flag Count**                         | Number of URG flags set in packets from ingress traffic                 |
| 41  | **Backward URG Flag Count**                        | Number of URG flags set in packets from egress traffic                   |
| 42  | **Forward Header Length**                          | Total length of all headers from ingress traffic                    |
| 43  | **Backward Header Length**                         | Total length of all headers from egress traffic                   |
| 44  | **Forward Packets per Second**                     | Rate of packets from ingress traffic per second                         |
| 45  | **Backward Packets per Second**                    | Rate of packets from egress traffic per second                           |
| 46  | **Minimum Packet Length**                          | Smallest packet size observed in the flow                               |
| 47  | **Maximum Packet Length**                          | Largest packet size observed in the flow                                |
| 48  | **Mean Packet Length**                             | Average packet size observed in the flow                                |
| 49  | **Standard Deviation of Packet Length**            | Variability in packet size observed in the flow                         |
| 50  | **Variance of Packet Length**                      | Statistical measure of the dispersion of packet sizes in the flow       |
| 51  | **Total FIN Flag Count**                           | Combined count of FIN flags from both directions                        |
| 52  | **Total SYN Flag Count**                           | Combined count of SYN flags from both directions                        |
| 53  | **Total RST Flag Count**                           | Combined count of RST flags from both directions                        |
| 54  | **Total PSH Flag Count**                           | Combined count of PSH flags from both directions                        |
| 55  | **Total ACK Flag Count**                           | Combined count of ACK flags from both directions                        |
| 56  | **Total URG Flag Count**                           | Combined count of URG flags from both directions                        |
| 57  | **Total CWE Flag Count**                           | Combined count of CWE flags from both directions                        |
| 58  | **Total ECE Flag Count**                           | Combined count of ECE flags from both directions                        |
| 59  | **Download/Upload Ratio**                          | Ratio of downlink to uplink traffic                                     |
| 60  | **Mean Flow Segment Length**                   | Average segment length |
| 61  | **Mean Flow Segment Length (Forward)**                   | Average segment length from ingress traffic                                |
| 62  | **Mean Flow Segment Length (Backward)**                  | Average segment length from egress traffic                                  |
| 63  | **Forward Bytes in Bulk**                          | Total bytes sent in bulk from ingress traffic                                |
| 64  | **Forward Packets in Bulk**                        | Total packets sent in bulk from ingress traffic                              |
| 65  | **Forward Bulk Rate**                              | Rate at which data is sent in bulk from ingress traffic                      |
| 66  | **Backward Bytes in Bulk**                         | Total bytes received in bulk from egress traffic                              |
| 67  | **Backward Packets in Bulk**                       | Total packets received in bulk from egress traffic                            |
| 68  | **Backward Bulk Rate**                             | Rate at which data is received in bulk from egress traffic                    |
| 69  | **Subflow Forward Packets**                        | Number of packets in the subflow from ingress traffic                        |
| 70  | **Subflow Forward Bytes**                          | Number of bytes in the subflow from ingress traffic                          |
| 71  | **Subflow Backward Packets**                       | Number of packets in the subflow from egress traffic                          |
| 72  | **Subflow Backward Bytes**                         | Number of bytes in the subflow from egress traffic                            |
| 73  | **Initial Window Bytes (Forward)**                 | Initial window size in bytes from ingress traffic                  |
| 74  | **Initial Window Bytes (Backward)**                | Initial window size in bytes from egress traffic                 |
| 75  | **Active Packets**                                 | Number of packets sent during active periods of flow                    |
| 76  | **Minimum Forward Header Length**                  | Minimum header length from ingress traffic                          |
| 77  | **Mean Active Time**                               | Average time in which the flow is actively sending data                 |
| 78  | **Standard Deviation of Active Time**              | Variability in the active times of the flow                             |
| 79  | **Maximum Active Time**                            | Longest time the flow was active without interruption                   |
| 80  | **Minimum Active Time**                            | Shortest active period of the flow                                      |
| 81  | **Mean Idle Time**                                 | Average time in which the flow is not actively sending data             |
| 82  | **Standard Deviation of Idle Time**                | Variability in the idle times of the flow                               |
| 83  | **Maximum Idle Time**                              | Longest idle time without any packets sent                              |
| 84  | **Minimum Idle Time**                              | Shortest idle period of the flow                                        |