"""
Module de validation métier et d'ingénierie système pour le projet PCCV.
Vérifie l'intégrité réseau et la conformité fonctionnelle des chaînes de protection HTA/HTB.
"""

import ipaddress
from typing import List, Tuple
from src.scl_parser import VirtualIED


class PCCVValidator:
    @staticmethod
    def validate_architecture(ieds: List[VirtualIED]) -> Tuple[bool, List[str]]:
        logs = []
        is_valid = True
        seen_ips = set()

        for ied in ieds:
            # 1. Vérification de la présence d'une configuration réseau
            if not ied.network:
                logs.append(f"[ERREUR] {ied.name} : Aucune configuration réseau (ConnectedAP) trouvée.")
                is_valid = False
                continue

            # 2. Validation syntaxique de l'adresse IPv4 et unicité
            try:
                ipaddress.IPv4Address(ied.network.ip)
                if ied.network.ip in seen_ips:
                    logs.append(f"[ERREUR] Conflit d'adresse IP détecté sur {ied.network.ip} ({ied.name}).")
                    is_valid = False
                seen_ips.add(ied.network.ip)
            except ipaddress.AddressValueError:
                logs.append(f"[ERREUR] {ied.name} : Adresse IP invalide ({ied.network.ip}).")
                is_valid = False

            # 3. Règle métier Poste Source : Cohérence de la chaîne de protection HTA
            # Si un IED contient une fonction de protection (PTOC), il doit pouvoir commander
            # le déclenchement (PTRC) et avoir l'état du disjoncteur (XCBR).
            has_ptoc = any(ln.startswith("PTOC") for ln in ied.logical_nodes)
            if has_ptoc:
                has_ptrc = any(ln.startswith("PTRC") for ln in ied.logical_nodes)
                has_xcbr = any(ln.startswith("XCBR") for ln in ied.logical_nodes)
                if not (has_ptrc and has_xcbr):
                    logs.append(
                        f"[ALERTE MÉTIER] {ied.name} : Fonction ampèremétrique PTOC détectée sans "
                        f"nœud de déclenchement (PTRC) ou disjoncteur associé (XCBR)."
                    )
                    is_valid = False
                else:
                    logs.append(
                        f"[OK MÉTIER] {ied.name} : Chaîne de protection départ HTA complète (PTOC -> PTRC -> XCBR)."
                    )

            # 4. Règle temps réel IEC 61850 GOOSE : Priorité VLAN (802.1Q)
            if has_ptoc and ied.network.vlan_priority < 4:
                logs.append(
                    f"[AVERTISSEMENT QoS] {ied.name} : Priorité VLAN ({ied.network.vlan_priority}) "
                    f"insuffisante pour des messages GOOSE de déclenchement (recommandé >= 4)."
                )

        if is_valid:
            logs.insert(0, "[SUCCÈS] Audit de conformité IEC 61850 / PCCV validé sans erreur bloquante.")

        return is_valid, logs