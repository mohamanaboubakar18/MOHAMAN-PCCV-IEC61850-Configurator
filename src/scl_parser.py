"""
Module de parsing des fichiers de configuration IEC 61850 (SCL : ICD/SCD/CID).
Extrait l'architecture du poste source, les paramètres réseau et les nœuds logiques (LN).
"""

import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class NetworkConfig:
    ip: str
    subnet: str
    vlan_id: int
    vlan_priority: int
    subnetwork_name: str


@dataclass
class VirtualIED:
    name: str
    ied_type: str
    manufacturer: str
    logical_device: str
    logical_nodes: List[str] = field(default_factory=list)
    network: NetworkConfig = None


class SCLParser:
    def __init__(self, scl_filepath: str):
        self.scl_filepath = scl_filepath
        self.tree = ET.parse(scl_filepath)
        self.root = self.tree.getroot()
        # Gestion automatique de l'espace de noms (namespace) IEC 61850
        self.ns = {"scl": self.root.tag.split("}")[0].strip("{")} if "}" in self.root.tag else {}

    def _find_all(self, element, path: str):
        return element.findall(path, self.ns) if self.ns else element.findall(path.replace("scl:", ""))

    def _find(self, element, path: str):
        return element.find(path, self.ns) if self.ns else element.find(path.replace("scl:", ""))

    def get_substation_name(self) -> str:
        sub = self._find(self.root, "scl:Substation")
        return sub.attrib.get("name", "POSTE_INCONNU") if sub is not None else "POSTE_INCONNU"

    def parse_network_map(self) -> Dict[str, NetworkConfig]:
        network_map = {}
        for subnet in self._find_all(self.root, ".//scl:SubNetwork"):
            subnet_name = subnet.attrib.get("name", "DefaultBus")
            for cap in self._find_all(subnet, "scl:ConnectedAP"):
                ied_name = cap.attrib.get("iedName")
                params = {}
                for p in self._find_all(cap, ".//scl:P"):
                    p_type = p.attrib.get("type")
                    params[p_type] = p.text.strip() if p.text else ""

                network_map[ied_name] = NetworkConfig(
                    ip=params.get("IP", "0.0.0.0"),
                    subnet=params.get("IP-SUBNET", "255.255.255.0"),
                    vlan_id=int(params.get("VLAN-ID", 1)),
                    vlan_priority=int(params.get("VLAN-PRIORITY", 0)),
                    subnetwork_name=subnet_name,
                )
        return network_map

    def parse_ieds(self) -> List[VirtualIED]:
        net_map = self.parse_network_map()
        ied_list = []

        for ied_elem in self._find_all(self.root, "scl:IED"):
            name = ied_elem.attrib.get("name")
            ied_type = ied_elem.attrib.get("type", "Generic_IED")
            manufacturer = ied_elem.attrib.get("manufacturer", "Standard")

            ld_elem = self._find(ied_elem, ".//scl:LDevice")
            ld_inst = ld_elem.attrib.get("inst", "LD0") if ld_elem is not None else "LD0"

            lns = []
            if ld_elem is not None:
                ln0 = self._find(ld_elem, "scl:LN0")
                if ln0 is not None:
                    lns.append(ln0.attrib.get("lnClass", "LLN0"))
                for ln in self._find_all(ld_elem, "scl:LN"):
                    ln_class = ln.attrib.get("lnClass", "")
                    ln_inst = ln.attrib.get("inst", "")
                    lns.append(f"{ln_class}{ln_inst}")

            ied_list.append(
                VirtualIED(
                    name=name,
                    ied_type=ied_type,
                    manufacturer=manufacturer,
                    logical_device=ld_inst,
                    logical_nodes=lns,
                    network=net_map.get(name),
                )
            )
        return ied_list