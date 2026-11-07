"""
Générateur d'orchestration pour la plateforme de virtualisation PCCV.
Traduit les IED validés en services conteneurisés (Docker Compose) et profils JSON.
"""

import json
import os
from datetime import datetime
from typing import List
from src.scl_parser import VirtualIED


class OrchestratorGenerator:
    @staticmethod
    def generate_docker_compose(substation_name: str, ieds: List[VirtualIED], output_path: str):
        lines = [
            f"# Manifeste généré automatiquement pour le poste source : {substation_name}",
            f"# Date de génération : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "version: '3.8'",
            "services:",
        ]

        for ied in ieds:
            service_name = ied.name.lower()
            is_protection = any(ln.startswith("PTOC") for ln in ied.logical_nodes)
            cpu_quota = "0.50" if is_protection else "0.25"
            mem_limit = "256M" if is_protection else "128M"

            lines.extend([
                f"  {service_name}:",
                f"    image: registry.mohaman.pccv/{ied.ied_type.lower()}:v1.0",
                f"    container_name: pccv_{service_name}",
                "    restart: always",
                "    cap_add:",
                "      - NET_ADMIN",
                "      - SYS_NICE  # Temps réel pour les trames GOOSE / Sampled Values",
                "    environment:",
                f"      - SUBSTATION={substation_name}",
                f"      - IED_NAME={ied.name}",
                f"      - LOGICAL_DEVICE={ied.logical_device}",
                f"      - ACTIVE_LNS={','.join(ied.logical_nodes)}",
                f"      - VLAN_ID={ied.network.vlan_id}",
                f"      - VLAN_PRIORITY={ied.network.vlan_priority}",
                "    deploy:",
                "      resources:",
                "        limits:",
                f"          cpus: '{cpu_quota}'",
                f"          memory: {mem_limit}",
                "    networks:",
                "      pccv_process_bus:",
                f"        ipv4_address: {ied.network.ip}",
                "",
            ])

        lines.extend([
            "networks:",
            "  pccv_process_bus:",
            "    driver: macvlan",
            "    ipam:",
            "      config:",
            "        - subnet: 192.168.10.0/24",
        ])

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

    @staticmethod
    def generate_audit_report(substation_name: str, ieds: List[VirtualIED], logs: List[str], output_path: str):
        report = {
            "substation": substation_name,
            "timestamp": datetime.now().isoformat(),
            "total_virtual_ieds": len(ieds),
            "validation_logs": logs,
            "deployed_containers": [
                {
                    "ied_name": ied.name,
                    "type": ied.ied_type,
                    "logical_device": ied.logical_device,
                    "logical_nodes": ied.logical_nodes,
                    "ip_address": ied.network.ip if ied.network else None,
                    "vlan_id": ied.network.vlan_id if ied.network else None,
                }
                for ied in ieds
            ],
        }
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=4, ensure_ascii=False)