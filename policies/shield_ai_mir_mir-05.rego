package shield_ai.mir.mandatory_reporting_integratio

import rego.v1

# SHIELD-AI(TM) MIR-05: Mandatory Reporting Integration
# Pillar: MIR -- Monitoring, Logging, and Incident Response
#
# Integrate incident detection with automated regulatory reporting triggers for SOCI Act, APRA CPS 234, and Notifiable Data Breaches, with pre-populated report templates.
#
# Maturity indicators:
#   L1: No automated reporting. Incidents reported manually (if at all).
#   L2: Manual incident reports using templates. Deadlines tracked in spreadsheets.
#   L3: Automated incident detection triggers pre-populated reports. Escalation workflows active.
#   L4: Fully automated reporting lifecycle. Continuous compliance monitoring with regulator dashboards.
#
# IMPLEMENTED (v1.7, Aug 2026) -- reference implementation.
# Input model: input.action.incident (bool); input.action.reporting_triggered
# (bool). Any confirmed incident must trigger the regulatory reporting path
# (SOCI 12-hour / APRA 72-hour windows); fail closed on a missing trigger.

deny contains msg if {
    input.action.incident == true
    not input.action.reporting_triggered
    msg := sprintf("MIR-05 deny: incident reported by agent %q has no regulatory reporting trigger (SOCI 12h / APRA 72h windows)", [input.agent.id])
}

allow if {
    count(deny) == 0
}
