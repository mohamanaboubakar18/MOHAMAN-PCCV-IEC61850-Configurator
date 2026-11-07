#  PCCV-Config-Engine — Démonstrateur de Configuration IEC 61850 pour Postes Sources Virtualisés

##  Contexte & Objectif du Projet

À l'heure de la modernisation des postes sources HTB/HTA (**Projet PCCV — Palier de Contrôle-Commande Virtualisé**), les fonctions historiques hébergées dans des équipements physiques dédiés (relais de protection numériques, régleurs en charge, passerelles de téléconduite) migrent vers des **architectures virtualisées à base de conteneurs**.

Ce démonstrateur répond à une problématique industrielle clé : **comment automatiser et fiabiliser la configuration d'une plateforme de virtualisation directement à partir des fichiers normés IEC 61850 (`.scd`, `.icd`, `.cid`) ?**

Fort de **6 ans d'expérience terrain en exploitation et maintenance de postes HT/BT** (paramétrage de relais de protection numériques SEPAM, essais fonctionnels de tranches électriques) et de ma formation d'ingénieur à l'**ENIB**, j'ai conçu cet outil pour faire le pont entre la **sûreté de fonctionnement électrique** et l'**orchestration logicielle**.

---

## Architecture & Fonctionnalités

Le moteur s'articule autour de 3 briques modulaires en Python (sans dépendances lourdes externes pour garantir la portabilité en environnement industriel contraint) :

1. **Parseur SCL / IEC 61850 (`src/scl_parser.py`)**
   * Analyse de l'arbre XML normé IEC 61850 (`Substation`, `Communication`, `IED`).
   * Extraction des équipements logiques (`LDevice`) et des nœuds fonctionnels (`LN` : `PTOC`, `PTRC`, `XCBR`, `ATCC`, `MMXU`, `GGIO`).
   * Cartographie automatique du plan d'adressage IP et de la segmentation VLAN (`ProcessBus`).

2. **Validateur Métier Contrôle-Commande (`src/validator.py`)**
   * **Cohérence électrique des protections :** Vérifie qu'un conteneur embarquant une fonction de détection de surintensité (`PTOC` - ANSI 51) dispose bien de sa logique de déclenchement (`PTRC`) et de l'interface disjoncteur (`XCBR`).
   * **Sûreté réseau & Temps réel :** Détecte les conflits d'adresses IPv4 et vérifie que la priorité VLAN IEEE 802.1Q est compatible avec les exigences temps réel des trames `GOOSE` ($\ge 4$).

3. **Générateur de Plateforme Conteneurisée (`src/orchestrator_gen.py`)**
   * Génère automatiquement le fichier d'orchestration `docker-compose.pccv.yml` (attribution des capacités Linux `SYS_NICE` et `NET_ADMIN`, quotas CPU/RAM différenciés selon la criticité protection/conduite, attachement au driver réseau `macvlan`).
   * Produit un rapport d'audit JSON traçable (`pccv_deployment_audit.json`) avant mise en service.

---

##  Exécution rapide (en 1 commande)

```bash
git clone [https://github.com/mohamanaboubakar18/MOHAMAN-PCCV-IEC61850-Configurator.git](https://github.com/mohamanaboubakar18/MOHAMAN-PCCV-IEC61850-Configurator.git)
cd ENEDIS-PCCV-IEC61850-Configurator
python main.py


Mohaman ABOUBAKAR

Élève-Ingénieur en 4e année à l'ENIB (Brest) | 6 ans d'expérience en maintenance et contrôle-commande des postes HT/BT