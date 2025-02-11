import { MACAddress, DancerDataSchema, DancerData } from "@/schema/DancerData";

// Record the RPi information according to MAC
const dancerTable: DancerData = {
  "E4:5F:01:B3:CC:19": { // 0
    IP: "192.168.0.0",
    MAC: "E4:5F:01:B3:CC:19",
    dancer: "0_xn",
    hostname: "lightdance-00",
    connected: false,
    interface: "ethernet",
  },
  "E4:5F:01:B3:CC:1A": { // 0
    IP: "192.168.0.0",
    MAC: "E4:5F:01:B3:CC:1A",
    dancer: "0_xn",
    hostname: "lightdance-00",
    connected: false,
    interface: "wifi",
  },
  "B8:27:EB:13:CE:84": { // 1
    IP: "192.168.0.0",
    MAC: "B8:27:EB:13:CE:84",
    dancer: "1_yck",
    hostname: "lightdance-01",
    connected: false,
    interface: "ethernet",
  },
  "B8:27:EB:46:9B:D1": { // 1
    IP: "192.168.0.0",
    MAC: "B8:27:EB:46:9B:D1",
    dancer: "1_yck",
    hostname: "lightdance-01",
    connected: false,
    interface: "wifi",
  },
  "B8:27:EB:AF:4E:7E": { // 2
    IP: "192.168.0.0",
    MAC: "B8:27:EB:AF:4E:7E",
    dancer: "2_sssam",
    hostname: "lightdance-02",
    connected: false,
    interface: "ethernet",
  },
  "B8:27:EB:FA:1B:2B": { // 2
    IP: "192.168.0.0",
    MAC: "B8:27:EB:FA:1B:2B",
    dancer: "2_sssam",
    hostname: "lightdance-02",
    connected: false,
    interface: "wifi",
  },
  "B8:27:EB:9A:43:92": { // 3
    IP: "192.168.0.0",
    MAC: "B8:27:EB:9A:43:92",
    dancer: "3_crc",
    hostname: "lightdance-03",
    connected: false,
    interface: "ethernet",
  },
  "B8:27:EB:CF:16:C7": { // 3
    IP: "192.168.0.0",
    MAC: "B8:27:EB:CF:16:C7",
    dancer: "3_crc",
    hostname: "lightdance-03",
    connected: false,
    interface: "wifi",
  },
  "B8:27:EB:A1:49:C6": { // 4
    IP: "192.168.0.0",
    MAC: "B8:27:EB:A1:49:C6",
    dancer: "4_arthur",
    hostname: "lightdance-04",
    connected: false,
    interface: "ethernet",
  },
  "B8:27:EB:F4:1C:93": { // 4
    IP: "192.168.0.0",
    MAC: "B8:27:EB:F4:1C:93",
    dancer: "4_arthur",
    hostname: "lightdance-04",
    connected: false,
    interface: "wifi",
  },
  "B8:27:EB:80:3E:DA": { // 5
    IP: "192.168.0.0",
    MAC: "B8:27:EB:80:3E:DA",
    dancer: "5_cs",
    hostname: "lightdance-05",
    connected: false,
    interface: "ethernet",
  },
  "B8:27:EB:D5:6B:8F": { // 5
    IP: "192.168.0.0",
    MAC: "B8:27:EB:D5:6B:8F",
    dancer: "5_cs",
    hostname: "lightdance-05",
    connected: false,
    interface: "wifi",
  },
  "D8:3A:DD:22:AB:29": { // 6
    IP: "192.168.0.44",
    MAC: "D8:3A:DD:22:AB:29",
    dancer: "6_rakec",
    hostname: "lightdance-06",
    connected: false,
    interface: "ethernet",
  },
  "D8:3A:DD:22:AB:2A": { // 6
    IP: "192.168.0.44",
    MAC: "D8:3A:DD:22:AB:2A",
    dancer: "6_rakec",
    hostname: "lightdance-06",
    connected: false,
    interface: "wifi",
  },
  "D8:3A:DD:22:AD:41": { // 7
    IP: "192.168.0.0",
    MAC: "D8:3A:DD:22:AD:41",
    dancer: "7_jya",
    hostname: "lightdance-07",
    connected: false,
    interface: "ethernet",
  },
  "D8:3A:DD:22:AD:43": { // 7
    IP: "192.168.0.0",
    MAC: "D8:3A:DD:22:AD:43",
    dancer: "7_jya",
    hostname: "lightdance-07",
    connected: false,
    interface: "wifi",
  },
  "D8:3A:DD:22:AC:1A": { // 8
    IP: "192.168.0.0",
    MAC: "D8:3A:DD:22:AC:1A",
    dancer: "8_circle",
    hostname: "lightdance-08",
    connected: false,
    interface: "ethernet",
  },
  "D8:3A:DD:22:AC:1B": { // 8
    IP: "192.168.0.0",
    MAC: "D8:3A:DD:22:AC:1B",
    dancer: "8_circle",
    hostname: "lightdance-08",
    connected: false,
    interface: "wifi",
  },
  "D8:3A:DD:22:AD:1E": { // 9
    IP: "192.168.0.0",
    MAC: "D8:3A:DD:22:AD:1E",
    dancer: "9_ricky",
    hostname: "lightdance-09",
    connected: false,
    interface: "ethernet",
  },
  "D8:3A:DD:22:AD:1F": { // 9
    IP: "192.168.0.0",
    MAC: "D8:3A:DD:22:AD:1F",
    dancer: "9_ricky",
    hostname: "lightdance-09",
    connected: false,
    interface: "wifi",
  },
  "D8:3A:DD:22:AC:DD": { // 10
    IP: "192.168.0.0",
    MAC: "D8:3A:DD:22:AC:DD",
    dancer: "10_chris",
    hostname: "lightdance-10",
    connected: false,
    interface: "ethernet",
  },
  "D8:3A:DD:22:AC:DE": { // 10
    IP: "192.168.0.0",
    MAC: "D8:3A:DD:22:AC:DE",
    dancer: "10_chris",
    hostname: "lightdance-10",
    connected: false,
    interface: "wifi",
  },
  "D8:3A:DD:22:AC:FE": { // 11
    IP: "192.168.0.0",
    MAC: "D8:3A:DD:22:AC:FE",
    dancer: "11_temple_1",
    hostname: "lightdance-11",
    connected: false,
    interface: "ethernet",
  },
  "D8:3A:DD:22:AC:FF": { // 11
    IP: "192.168.0.0",
    MAC: "D8:3A:DD:22:AC:FF",
    dancer: "11_temple_1",
    hostname: "lightdance-11",
    connected: false,
    interface: "wifi",
  },
  "B8:27:EB:32:39:A4": { // 12
    IP: "192.168.0.0",
    MAC: "B8:27:EB:32:39:A4",
    dancer: "12_temple_2",
    hostname: "lightdance-12",
    connected: false,
    interface: "ethernet",
  },
  "B8:27:EB:67:6C:F1": { // 12
    IP: "192.168.0.0",
    MAC: "B8:27:EB:67:6C:F1",
    dancer: "12_temple_2",
    hostname: "lightdance-12",
    connected: false,
    interface: "wifi",
  },
  "B8:27:EB:FA:D3:62": { // 13
    IP: "192.168.0.0",
    MAC: "B8:27:EB:FA:D3:62",
    dancer: "13_bridge_1",
    hostname: "lightdance-13",
    connected: false,
    interface: "ethernet",
  },
  "B8:27:EB:AF:86:37": { // 13
    IP: "192.168.0.0",
    MAC: "B8:27:EB:AF:86:37",
    dancer: "13_bridge_1",
    hostname: "lightdance-13",
    connected: false,
    interface: "wifi",
  },
  // 14 ether B8:27:EB:99:E2:00 wifi B8:27:EB:CC:B7:55
  "B8:27:EB:82:79:49": { // 15
    IP: "192.168.0.0",
    MAC: "B8:27:EB:82:79:49",
    dancer: "15_nian_1",
    hostname: "lightdance-15",
    connected: false,
    interface: "ethernet",
  },
  "B8:27:EB:D7:2C:1C": { // 15
    IP: "192.168.0.0",
    MAC: "B8:27:EB:D7:2C:1C",
    dancer: "15_nian_1",
    hostname: "lightdance-15",
    connected: false,
    interface: "wifi",
  },
  "B8:27:EB:3A:21:4F": { // 16
    IP: "192.168.0.0",
    MAC: "B8:27:EB:3A:21:4F",
    dancer: "16_nian_2",
    hostname: "lightdance-16",
    connected: false,
    interface: "ethernet",
  },
  "B8:27:EB:6F:74:1A": { // 16
    IP: "192.168.0.0",
    MAC: "B8:27:EB:6F:74:1A",
    dancer: "16_nian_2",
    hostname: "lightdance-16",
    connected: false,
    interface: "wifi",
  },
  "D8:3A:DD:22:AC:AA": { // 17
    IP: "192.168.0.0",
    MAC: "D8:3A:DD:22:AC:AA",
    dancer: "17_sword",
    hostname: "lightdance-17",
    connected: false,
    interface: "ethernet",
  },
  "D8:3A:DD:22:AC:AB": { // 17
    IP: "192.168.0.0",
    MAC: "D8:3A:DD:22:AC:AB",
    dancer: "17_sword",
    hostname: "lightdance-17",
    connected: false,
    interface: "wifi",
  },
  "E4:5F:01:85:05:6E": { // 18
    IP: "192.168.0.0",
    MAC: "E4:5F:01:85:05:6E",
    dancer: "18_guandao",
    hostname: "lightdance-18",
    connected: false,
    interface: "ethernet",
  },
  "E4:5F:01:85:05:6F": { // 18
    IP: "192.168.0.0",
    MAC: "E4:5F:01:85:05:6F",
    dancer: "18_guandao",
    hostname: "lightdance-18",
    connected: false,
    interface: "wifi",
  },
  "D8:3A:DD:22:AD:01": { // 19
    IP: "192.168.0.0",
    MAC: "D8:3A:DD:22:AD:01",
    dancer: "19_effectboard",
    hostname: "lightdance-19",
    connected: false,
    interface: "ethernet",
  },
  "D8:3A:DD:22:AD:02": { // 19
    IP: "192.168.0.0",
    MAC: "D8:3A:DD:22:AD:02",
    dancer: "19_effectboard",
    hostname: "lightdance-19",
    connected: false,
    interface: "wifi",
  },
  // 20 broken
  // 21 ether B8:27:EB:B5:9C:B5 wifi B8:27:EB:E0:C9:E0
  // 22 ether B8:27:EB:80:87:B3 wifi B8:27:EB:D5:D2:E6
  // 23 ether D8:3A:DD:22:AD:15 wifi D8:3A:DD:22:AD:16
  // 24 ether B8:27:EB:83:0B:44 wifi B8:27:EB:D6:5E:11
};

export const dancerToMAC: Record<
  string,
  { wifi: MACAddress; ethernet: MACAddress }
> = {};
Object.keys(dancerTable).forEach((MAC) => {
  const { dancer, interface: networkInterface } = dancerTable[MAC];
  dancerToMAC[dancer] ??= {
    wifi: "",
    ethernet: "",
  };
  dancerToMAC[dancer][networkInterface] = MAC;
});

// Validate the config file
DancerDataSchema.parse(dancerTable);
export default dancerTable;