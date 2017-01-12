define($HOST s1-eth1, $NETWORK s2-eth2)

// we just forward traffic from the host
FromDevice($HOST, SNIFFER false) -> Queue(8) -> ToDevice($NETWORK);

// before giving traffic to the host we need to do some checks
FromDevice($NETWORK, SNIFFER false) -> ether :: Classifier(12/0806, -);

out :: Queue(8) -> EnsureEther -> ToDevice($HOST);

// ARP can go through directly
ether[0] -> out;

// IP needs some fixes
ether[1] -> Strip(14) -> CheckIPHeader -> ip :: IPClassifier(ip proto udp, ip proto tcp, -);

// udp checksum fix
ip[0] -> SetUDPChecksum -> out;

// tcp checksum fix
ip[1] -> SetTCPChecksum -> out;

// others
ip[2] -> out;

