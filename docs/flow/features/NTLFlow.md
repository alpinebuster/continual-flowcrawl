No. | Feature Name | Description
-- | -- | --
1 | Flow ID | Unique identifier for the network flow (flow key)
2 | IP Source | The IP address of the source node
3 | Source Port | The port number used by the source in the network flow
4 | IP Destination | The IP address of the destination node
5 | Destination Port | The port number used by the destination in the network flow
6 | Protocol | The protocol used in the flow (e.g., TCP, UDP)
7 | Flow Duration | Total duration of the flow in microseconds
8 | Total Packet Count | Sum of forward and backward packet counts
9 | Forward Packet Count | Number of packets sent from source to destination
10 | Backward Packet Count | Number of packets sent from destination to source
11 | Total Packet Length | Sum of packet lengths in the flow (in bytes)
12 | Forward Total Packet Length | Total length of packets in the forward direction (in bytes)
13 | Backward Total Packet Length | Total length of packets in the backward direction (in bytes)
14 | Maximum Packet Length in Flow | Maximum packet length observed in the flow
15 | Minimum Packet Length in Flow | Minimum packet length observed in the flow
16 | Mean Packet Length in Flow | Average packet length over the flow
17 | Standard Deviation of Packet Length in Flow | Standard deviation of packet lengths in the flow
18 | Variance of Packet Length in Flow | Variance of packet lengths in the flow
19 | Maximum Packet Length Forward Direction | Maximum packet length in the forward direction
20 | Minimum Packet Length Forward Direction | Minimum packet length in the forward direction
21 | Mean Packet Length Forward Direction | Average packet length in the forward direction
22 | Standard Deviation of Packet Length Forward Direction | Standard deviation of packet lengths in the forward direction
23 | Variance of Packet Length Forward Direction | Variance of packet lengths in the forward direction
24 | Maximum Packet Length Backward Direction | Maximum packet length in the backward direction
25 | Minimum Packet Length Backward Direction | Minimum packet length in the backward direction
26 | Mean Packet Length Backward Direction | Average packet length in the backward direction
27 | Standard Deviation of Packet Length Backward Direction | Standard deviation of packet lengths in the backward direction
28 | Variance of Packet Length Backward Direction | Variance of packet lengths in the backward direction
29 | Total Header Length | Sum of header lengths for the flow (in bytes)
30 | Maximum Header Length in Flow | Maximum header length observed in the flow
31 | Minimum Header Length in Flow | Minimum header length observed in the flow
32 | Mean Header Length in Flow | Average header length in the flow
33 | Standard Deviation of Header Length in Flow | Standard deviation of header lengths in the flow
34 | Forward Total Header Length | Total header length in the forward direction
35 | Maximum Header Length Forward Direction | Maximum header length in the forward direction
36 | Minimum Header Length Forward Direction | Minimum header length in the forward direction
37 | Mean Header Length Forward Direction | Average header length in the forward direction
38 | Standard Deviation of Header Length Forward Direction | Standard deviation of header lengths in the forward direction
39 | Backward Total Header Length | Total header length in the backward direction
40 | Maximum Header Length Backward Direction | Maximum header length in the backward direction
41 | Minimum Header Length Backward Direction | Minimum header length in the backward direction
42 | Mean Header Length Backward Direction | Average header length in the backward direction
43 | Standard Deviation of Header Length Backward Direction | Standard deviation of header lengths in the backward direction
44 | Forward Segment Length Mean | Mean segment length in the forward direction
45 | Backward Segment Length Mean | Mean segment length in the backward direction
46 | Flow Segment Length Mean | Mean segment length for the entire flow
47 | Initial Window Size in Forward Direction | Initial window size used in the forward direction for flow control
48 | Initial Window Size in Backward Direction | Initial window size used in the backward direction for flow control
49 | Minimum Active Duration | Minimum duration of active (non-idle) periods in the flow
50 | Maximum Active Duration | Maximum duration of active periods in the flow
51 | Mean Active Duration | Average active duration in the flow
52 | Standard Deviation of Active Duration | Standard deviation of active durations in the flow
53 | Minimum Idle Duration | Minimum idle period duration in the flow
54 | Maximum Idle Duration | Maximum idle period duration in the flow
55 | Mean Idle Duration | Average idle period duration in the flow
56 | Standard Deviation of Idle Duration | Standard deviation of idle durations in the flow
57 | Bytes per Second (Total) | Total data transfer rate (bytes per second) for the flow
58 | Bytes per Second (Forward) | Data transfer rate in the forward direction (bytes per second)
59 | Bytes per Second (Backward) | Data transfer rate in the backward direction (bytes per second)
60 | Packets per Second (Total) | Total packet rate (packets per second) for the flow
61 | Packets per Second (Backward) | Packet rate in the backward direction (packets per second)
62 | Packets per Second (Forward) | Packet rate in the forward direction (packets per second)
63 | Down/Up Ratio | Ratio of downstream to upstream traffic
64 | Forward Bytes (Bulk Transfer) | Total bytes transferred in bulk in the forward direction
65 | Forward Packets (Bulk Transfer) | Total packets transferred in bulk in the forward direction
66 | Forward Bulk Rate | Bulk data transfer rate in the forward direction
67 | Backward Bytes (Bulk Transfer) | Total bytes transferred in bulk in the backward direction
68 | Backward Packets (Bulk Transfer) | Total packets transferred in bulk in the backward direction
69 | Backward Bulk Rate | Bulk data transfer rate in the backward direction
70 | Forward Bulk State Count | Number of bulk transfer states in the forward direction
71 | Forward Bulk Size Total | Total size of bulk transfers in the forward direction
72 | Forward Bulk Packet Count | Total number of packets in forward bulk transfers
73 | Forward Bulk Duration | Total duration of bulk transfers in the forward direction
74 | Backward Bulk State Count | Number of bulk transfer states in the backward direction
75 | Backward Bulk Size Total | Total size of bulk transfers in the backward direction
76 | Backward Bulk Packet Count | Total number of packets in backward bulk transfers
77 | Backward Bulk Duration | Total duration of bulk transfers in the backward direction
78 | Total FIN Flag Count | Combined FIN flag count from both directions
79 | Total PSH Flag Count | Combined PSH flag count from both directions
80 | Total URG Flag Count | Combined URG flag count from both directions
81 | Total ECE Flag Count | Combined ECE flag count from both directions
82 | Total SYN Flag Count | Combined SYN flag count from both directions
83 | Total ACK Flag Count | Combined ACK flag count from both directions
84 | Total CWE Flag Count | Combined CWE flag count from both directions
85 | Total RST Flag Count | Combined RST flag count from both directions
86 | Forward FIN Flag Count | FIN flag count in the forward direction
87 | Forward PSH Flag Count | PSH flag count in the forward direction
88 | Forward URG Flag Count | URG flag count in the forward direction
89 | Forward ECE Flag Count | ECE flag count in the forward direction
90 | Forward SYN Flag Count | SYN flag count in the forward direction
91 | Forward ACK Flag Count | ACK flag count in the forward direction
92 | Forward CWE Flag Count | CWE flag count in the forward direction
93 | Forward RST Flag Count | RST flag count in the forward direction
94 | Backward FIN Flag Count | FIN flag count in the backward direction
95 | Backward PSH Flag Count | PSH flag count in the backward direction
96 | Backward URG Flag Count | URG flag count in the backward direction
97 | Backward ECE Flag Count | ECE flag count in the backward direction
98 | Backward SYN Flag Count | SYN flag count in the backward direction
99 | Backward ACK Flag Count | ACK flag count in the backward direction
100 | Backward CWE Flag Count | CWE flag count in the backward direction
101 | Backward RST Flag Count | RST flag count in the backward direction
102 | Mean Inter-Arrival Time (IAT) | Average time between packet arrivals over the flow
103 | Standard Deviation of IAT | Standard deviation of packet inter-arrival times
104 | Maximum IAT | Maximum time gap between packet arrivals in the flow
105 | Minimum IAT | Minimum time gap between packet arrivals in the flow
106 | Total IAT (Forward + Backward) | Combined inter-arrival time for both directions
107 | Mean IAT Forward Direction | Average inter-arrival time for packets in the forward direction
108 | Standard Deviation of IAT Forward Direction | Standard deviation of inter-arrival times in the forward direction
109 | Maximum IAT Forward Direction | Maximum inter-arrival time in the forward direction
110 | Minimum IAT Forward Direction | Minimum inter-arrival time in the forward direction
111 | Total IAT Forward Direction | Total inter-arrival time for the forward direction
112 | Mean IAT Backward Direction | Average inter-arrival time for packets in the backward direction
113 | Standard Deviation of IAT Backward Direction | Standard deviation of inter-arrival times in the backward direction
114 | Maximum IAT Backward Direction | Maximum inter-arrival time in the backward direction
115 | Minimum IAT Backward Direction | Minimum inter-arrival time in the backward direction
116 | Total IAT Backward Direction | Total inter-arrival time for the backward direction
117 | Sub-Flow Forward Packets | Number of packets in the forward sub-flow
118 | Sub-Flow Backward Packets | Number of packets in the backward sub-flow
119 | Sub-Flow Forward Bytes | Total bytes in the forward sub-flow
120 | Sub-Flow Backward Bytes | Total bytes in the backward sub-flow