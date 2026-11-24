package shield_ai.lib_test

import rego.v1

import data.shield_ai.lib.high_risk_tools
import data.shield_ai.lib.sensitive_tools
import data.shield_ai.lib.infrastructure_apis

# The shared tool/risk registry must expose the exact sets the controls rely
# on, so the collector (doc 13) and the policies agree on one classification.
test_high_risk_tools_registered if {
    # shell_exec, write_file, install_package, transfer_funds, delete_objects
    high_risk_tools["shell_exec"]
    high_risk_tools["write_file"]
    high_risk_tools["install_package"]
    high_risk_tools["transfer_funds"]
    high_risk_tools["delete_objects"]
    count(high_risk_tools) == 5
}

test_sensitive_tools_registered if {
    # transfer_funds, write_file, shell_exec, send_email_draft, delete_objects
    sensitive_tools["transfer_funds"]
    sensitive_tools["write_file"]
    sensitive_tools["shell_exec"]
    sensitive_tools["send_email_draft"]
    sensitive_tools["delete_objects"]
    count(sensitive_tools) == 5
}

test_infrastructure_apis_registered if {
    infrastructure_apis["ec2"]
    infrastructure_apis["iam"]
    infrastructure_apis["lambda"]
    infrastructure_apis["s3"]
    infrastructure_apis["kms"]
    infrastructure_apis["cloudformation"]
    count(infrastructure_apis) == 12
}