| No. | Feature Name                                       | Description                                                             |
|-----|----------------------------------------------------|-------------------------------------------------------------------------|
| 1   | **Start Time**                                     | Timestamp when the network flow started                                 |
| 2   | **Flow Duration (Milliseconds)**                   | Total duration of the flow in milliseconds                              |
| 3   | **Protocol Type**                                  | Type of protocol used (TCP, UDP, OTHER) based on protocol number  |
| 4   | **Source IP Address**                              | Source IP address                             |
| 5   | **Source Port**                                    | Source Network port           |
| 6   | **Destination IP Address**                         | Destination IP address                                |
| 7   | **Destination Port**                               | Destination Network port              |
| 8   | **Total Packet Count**                             | Total number of packets in the flow (sum of ingress and egress packets) |
| 9   | **Total Bytes**                                    | Total number of bytes transferred in the flow                           |
| 10  | **Flags String**                                   | Concatenated string of all TCP flags set throughout the flow (`UAPRSF`, with a `.` on the place of the flag that was not in the flow. Ex: `.A.RS.`)   |