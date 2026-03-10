from ..common.database import get_db_session
from ..common.models import Dispute, StreamType, DisputeStatus

class DisputeProcessor:
    def process(self, provider_id, dispute_payload):
        print(f"Processing dispute for provider {provider_id}")
        stream_type_str = dispute_payload.get('stream_type')

        session = get_db_session(provider_id)
        try:
            dispute = Dispute(
                provider_id=provider_id,
                claim_id=dispute_payload.get('claim_id'),
                stream_type=StreamType(stream_type_str),
                status=DisputeStatus.PROCESSING,
                data=dispute_payload
            )
            session.add(dispute)
            session.commit()

            # Dispatch to specific stream handlers
            if stream_type_str == StreamType.ELIGIBILITY.value:
                self.handle_eligibility(dispute, session)
            elif stream_type_str == StreamType.MEDICAL_NECESSITY.value:
                self.handle_medical_necessity(dispute, session)
            elif stream_type_str == StreamType.BILLING_CODING.value:
                self.handle_billing_coding(dispute, session)
            elif stream_type_str == StreamType.AUTHORIZATION.value:
                self.handle_authorization(dispute, session)
            elif stream_type_str == StreamType.PHARMACY_BENEFIT.value:
                self.handle_pharmacy_benefit(dispute, session)
            elif stream_type_str == StreamType.CONTRACTUAL_DISPUTE.value:
                self.handle_contractual_dispute(dispute, session)
            elif stream_type_str == StreamType.COORDINATION_OF_BENEFITS.value:
                self.handle_cob(dispute, session)
            else:
                print(f"Stream {stream_type_str} not handled.")

            dispute.status = DisputeStatus.COMPLETED
            session.commit()
        except Exception as e:
            print(f"Error processing dispute: {e}")
            if 'dispute' in locals():
                dispute.status = DisputeStatus.FAILED
                session.commit()
        finally:
            session.close()

    def handle_eligibility(self, dispute, session):
        print(f"Handling Eligibility for claim {dispute.claim_id}")
        dispute.data['sub_operations'] = ["verify_coverage", "check_enrollment"]

    def handle_medical_necessity(self, dispute, session):
        print(f"Handling Medical Necessity for claim {dispute.claim_id}")
        dispute.data['sub_operations'] = ["clinical_review", "guideline_validation"]

    def handle_billing_coding(self, dispute, session):
        print(f"Handling Billing & Coding for claim {dispute.claim_id}")
        dispute.data['sub_operations'] = ["cpt_validation", "modifier_check"]

    def handle_authorization(self, dispute, session):
        print(f"Handling Authorization for claim {dispute.claim_id}")
        dispute.data['sub_operations'] = ["prior_auth_verification", "referral_check"]

    def handle_pharmacy_benefit(self, dispute, session):
        print(f"Handling Pharmacy Benefit for claim {dispute.claim_id}")
        # Sub-stream operations: Formulary check, drug interaction review
        dispute.data['sub_operations'] = ["formulary_verification", "drug_interaction_review"]

    def handle_contractual_dispute(self, dispute, session):
        print(f"Handling Contractual Dispute for claim {dispute.claim_id}")
        # Sub-stream operations: Fee schedule review, contract term validation
        dispute.data['sub_operations'] = ["fee_schedule_audit", "contract_term_validation"]

    def handle_cob(self, dispute, session):
        print(f"Handling COB for claim {dispute.claim_id}")
        # Sub-stream operations: Primary insurer check, benefit coordination
        dispute.data['sub_operations'] = ["primary_insurer_verification", "benefit_synchronization"]
