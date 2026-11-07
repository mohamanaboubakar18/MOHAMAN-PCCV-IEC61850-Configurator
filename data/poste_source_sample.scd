<?xml version="1.0" encoding="UTF-8"?>
<SCL xmlns="http://www.iec.ch/61850/2003/SCL" version="2007" revision="B">
    <Header id="MOHAMAN_POSTE_SOURCE_PCCV_DEMO" version="1.0" toolID="PCCV-Config-Tool"/>
    
    <Substation name="PS_92">
        <VoltageLevel name="HTA_20kV">
            <Bay name="DEPART_HTA_01">
                <ConductingEquipment name="DISJ_01" type="CBR"/>
            </Bay>
            <Bay name="TRANSFO_HTB_HTA_1">
                <ConductingEquipment name="TR_01" type="PTR"/>
            </Bay>
        </VoltageLevel>
    </Substation>

    <Communication>
        <SubNetwork name="ProcessBus_SV_GOOSE" type="8-MMS">
            <ConnectedAP iedName="IED_PROT_DEP01" apName="S1">
                <Address>
                    <P type="IP">192.168.10.11</P>
                    <P type="IP-SUBNET">255.255.255.0</P>
                    <P type="VLAN-ID">100</P>
                    <P type="VLAN-PRIORITY">4</P>
                </Address>
            </ConnectedAP>
            <ConnectedAP iedName="IED_REGUL_TR01" apName="S1">
                <Address>
                    <P type="IP">192.168.10.12</P>
                    <P type="IP-SUBNET">255.255.255.0</P>
                    <P type="VLAN-ID">100</P>
                    <P type="VLAN-PRIORITY">4</P>
                </Address>
            </ConnectedAP>
            <ConnectedAP iedName="IED_SCADA_GW" apName="S1">
                <Address>
                    <P type="IP">192.168.10.250</P>
                    <P type="IP-SUBNET">255.255.255.0</P>
                    <P type="VLAN-ID">200</P>
                    <P type="VLAN-PRIORITY">2</P>
                </Address>
            </ConnectedAP>
        </SubNetwork>
    </Communication>

    <IED name="IED_PROT_DEP01" type="Virtual_SEPAM_HTA" manufacturer="MOHAMAN_PCCV">
        <AccessPoint name="S1">
            <Server>
                <LDevice inst="LD_Protection">
                    <LN0 lnClass="LLN0" inst="" lnType="LLN0_Type"/>
                    <!-- PTOC : Protection à maximum de courant (ANSI 51) -->
                    <LN lnClass="PTOC" inst="1" lnType="PTOC_ANSI51"/>
                    <!-- PTRC : Déclenchement (Trip Conditioning) -->
                    <LN lnClass="PTRC" inst="1" lnType="PTRC_Trip"/>
                    <!-- XCBR : Image du disjoncteur HT -->
                    <LN lnClass="XCBR" inst="1" lnType="XCBR_Disj"/>
                </LDevice>
            </Server>
        </AccessPoint>
    </IED>

    <IED name="IED_REGUL_TR01" type="Virtual_ATCC_Transfo" manufacturer="MOHAMAN_PCCV">
        <AccessPoint name="S1">
            <Server>
                <LDevice inst="LD_Regulation">
                    <LN0 lnClass="LLN0" inst="" lnType="LLN0_Type"/>
                    <!-- ATCC : Régleur en charge automatique (Automatic Tap Changer Controller) -->
                    <LN lnClass="ATCC" inst="1" lnType="ATCC_Regul"/>
                    <!-- MMXU : Mesures triphasées U, I, P, Q -->
                    <LN lnClass="MMXU" inst="1" lnType="MMXU_Measurement"/>
                </LDevice>
            </Server>
        </AccessPoint>
    </IED>

    <IED name="IED_SCADA_GW" type="Virtual_Teleconduite_Gateway" manufacturer="MOHAMAN_PCCV">
        <AccessPoint name="S1">
            <Server>
                <LDevice inst="LD_Gateway">
                    <LN0 lnClass="LLN0" inst="" lnType="LLN0_Type"/>
                    <!-- GGIO : Entrées/Sorties génériques de télésignalisation -->
                    <LN lnClass="GGIO" inst="1" lnType="GGIO_TS"/>
                </LDevice>
            </Server>
        </AccessPoint>
    </IED>
</SCL>