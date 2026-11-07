"""
Démonstrateur d'outil de configuration automatisée pour plateforme PCCV.
Usage : python main.py
"""

import sys
from src.scl_parser import SCLParser
from src.validator import PCCVValidator
from src.orchestrator_gen import OrchestratorGenerator


def main():
    scl_file = "data/poste_source_sample.scd"
    compose_out = "output/docker-compose.pccv.yml"
    report_out = "output/pccv_deployment_audit.json"

    print("=" * 72)
    print(" DÉMONSTRATEUR PCCV — CONFIGURATION IEC 61850 VERS CONTENEURS")
    print("=" * 72)

    # 1. Parsing du fichier SCL (IEC 61850)
    print(f"\n[1/3] Lecture du fichier SCL : {scl_file}...")
    parser = SCLParser(scl_file)
    substation = parser.get_substation_name()
    ieds = parser.parse_ieds()
    print(f"      -> Poste Source identifié : {substation}")
    print(f"      -> {len(ieds)} IED(s) virtuel(s) extraits.")

    for ied in ieds:
        print(f"         * {ied.name} ({ied.ied_type}) | IP: {ied.network.ip} | LNs: {ied.logical_nodes}")

    # 2. Validation de l'architecture et des règles métier HTA/HTB
    print("\n[2/3] Exécution du moteur de validation métier (Contrôle-Commande & Réseau)...")
    is_valid, logs = PCCVValidator.validate_architecture(ieds)
    for log in logs:
        print(f"      {log}")

    if not is_valid:
        print("\n[ARRÊT] Échec de validation. Déploiement conteneurisé annulé par sécurité.")
        sys.exit(1)

    # 3. Génération des artefacts de virtualisation
    print("\n[3/3] Génération des fichiers de configuration de la plateforme virtualisée...")
    OrchestratorGenerator.generate_docker_compose(substation, ieds, compose_out)
    OrchestratorGenerator.generate_audit_report(substation, ieds, logs, report_out)
    print(f"      -> Manifeste d'orchestration généré : {compose_out}")
    print(f"      -> Rapport d'audit JSON généré      : {report_out}")
    print("\n[TERMINÉ] La plateforme virtualisée est prête à être déployée.")


if __name__ == "__main__":
    main()