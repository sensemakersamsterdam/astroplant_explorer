EESchema Schematic File Version 4
EELAYER 26 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title "MH-Z19B mount"
Date "2020-02-11"
Rev "1.0"
Comp "SenseMakers Amsterdam"
Comment1 "Author: Gijs Mos"
Comment2 ""
Comment3 ""
Comment4 "sensemakersams.org"
$EndDescr
$Comp
L Mechanical:MountingHole MH1
U 1 1 5E41CE43
P 1050 7075
F 0 "MH1" H 1150 7121 50  0000 L CNN
F 1 "MountingHole" H 1150 7030 50  0000 L CNN
F 2 "MountingHole:MountingHole_2.2mm_M2" H 1050 7075 50  0001 C CNN
F 3 "~" H 1050 7075 50  0001 C CNN
	1    1050 7075
	1    0    0    -1  
$EndComp
$Comp
L Mechanical:MountingHole MH2
U 1 1 5E41D011
P 1800 7075
F 0 "MH2" H 1900 7121 50  0000 L CNN
F 1 "MountingHole" H 1900 7030 50  0000 L CNN
F 2 "MountingHole:MountingHole_2.2mm_M2" H 1800 7075 50  0001 C CNN
F 3 "~" H 1800 7075 50  0001 C CNN
	1    1800 7075
	1    0    0    -1  
$EndComp
$Comp
L Mechanical:MountingHole MH3
U 1 1 5E41D0DF
P 2575 7075
F 0 "MH3" H 2675 7121 50  0000 L CNN
F 1 "MountingHole" H 2675 7030 50  0000 L CNN
F 2 "MountingHole:MountingHole_2.2mm_M2" H 2575 7075 50  0001 C CNN
F 3 "~" H 2575 7075 50  0001 C CNN
	1    2575 7075
	1    0    0    -1  
$EndComp
$Comp
L Mechanical:MountingHole MH4
U 1 1 5E41D1C3
P 3400 7075
F 0 "MH4" H 3500 7121 50  0000 L CNN
F 1 "MountingHole" H 3500 7030 50  0000 L CNN
F 2 "MountingHole:MountingHole_2.2mm_M2" H 3400 7075 50  0001 C CNN
F 3 "~" H 3400 7075 50  0001 C CNN
	1    3400 7075
	1    0    0    -1  
$EndComp
$Comp
L Connector:Conn_01x04_Female J4
U 1 1 5E41D3FB
P 7650 1825
F 0 "J4" H 7475 2100 50  0000 L CNN
F 1 "Z19B-C2" H 7350 1450 50  0000 L CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Vertical" H 7650 1825 50  0001 C CNN
F 3 "~" H 7650 1825 50  0001 C CNN
	1    7650 1825
	1    0    0    -1  
$EndComp
$Comp
L Connector:Conn_01x03_Male J1
U 1 1 5E41D57E
P 8100 1825
F 0 "J1" H 8225 2100 50  0000 C CNN
F 1 "Buck" H 8225 1625 50  0000 C CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical" H 8100 1825 50  0001 C CNN
F 3 "~" H 8100 1825 50  0001 C CNN
	1    8100 1825
	1    0    0    -1  
$EndComp
$Comp
L Connector:Conn_01x05_Female J2
U 1 1 5E41D6C0
P 7050 1925
F 0 "J2" H 6875 2300 50  0000 L CNN
F 1 "Z19B-C1" H 6750 1650 50  0000 L CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x05_P2.54mm_Vertical" H 7050 1925 50  0001 C CNN
F 3 "~" H 7050 1925 50  0001 C CNN
	1    7050 1925
	1    0    0    -1  
$EndComp
$Comp
L Connector:Conn_01x04_Male J3
U 1 1 5E41D81D
P 8725 1825
F 0 "J3" H 8831 2103 50  0000 C CNN
F 1 "GroveSer" H 8800 1525 50  0000 C CNN
F 2 "Connector_JST:JST_PH_B4B-PH-K_1x04_P2.00mm_Vertical" H 8725 1825 50  0001 C CNN
F 3 "~" H 8725 1825 50  0001 C CNN
	1    8725 1825
	1    0    0    -1  
$EndComp
Text Label 6850 1725 2    50   ~ 0
Vo
NoConn ~ 6850 1725
NoConn ~ 6850 2025
Text Label 6850 1825 2    50   ~ 0
RxTx
Text Label 6850 1925 2    50   ~ 0
TxRx
Text Label 6850 2125 2    50   ~ 0
HD
NoConn ~ 6850 2125
Text Label 7450 1725 2    50   ~ 0
V5
Text Label 7450 1825 2    50   ~ 0
Gnd
NoConn ~ 7450 1925
NoConn ~ 7450 2025
Text Label 7450 2025 2    50   ~ 0
PWM
Text Label 8300 1725 0    50   ~ 0
V3.3
Text Label 8300 1825 0    50   ~ 0
Gnd
Text Label 8300 1925 0    50   ~ 0
V5
Text Label 8925 1725 0    50   ~ 0
TxRx
Text Label 8925 1825 0    50   ~ 0
RxTx
Text Label 8925 1925 0    50   ~ 0
V3.3
Text Label 8925 2025 0    50   ~ 0
Gnd
$EndSCHEMATC
