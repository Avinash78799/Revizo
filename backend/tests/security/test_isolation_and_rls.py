import pytest
from app.services.authorization import AuthorizationService, AuthorizationError

def test_student_data_isolation_success_for_own_data():
    student_a_id = "student-aaa-111"
    
    # Student A accessing their own resource
    assert AuthorizationService.verify_ownership(
        current_user_id=student_a_id,
        resource_owner_id=student_a_id,
        current_user_role="student"
    ) is True

def test_student_cross_tenant_data_access_strictly_prevented():
    student_a_id = "student-aaa-111"
    student_b_id = "student-bbb-222"
    
    # Student A attempting to access Student B's attempt/mastery/mistakes
    with pytest.raises(AuthorizationError) as exc_info:
        AuthorizationService.verify_ownership(
            current_user_id=student_a_id,
            resource_owner_id=student_b_id,
            current_user_role="student"
        )
    assert "Security Violation" in str(exc_info.value.detail)

def test_admin_oversight_access_allowed():
    admin_id = "admin-999"
    student_b_id = "student-bbb-222"
    
    # Admin auditing student performance record
    assert AuthorizationService.verify_ownership(
        current_user_id=admin_id,
        resource_owner_id=student_b_id,
        current_user_role="admin"
    ) is True

def test_student_cannot_perform_admin_mutations():
    student_role = "student"
    
    # Attempting admin operations (quarantine, approve, question creation)
    with pytest.raises(AuthorizationError):
        AuthorizationService.require_admin(student_role)
        
    with pytest.raises(AuthorizationError):
        AuthorizationService.require_reviewer_or_admin(student_role)

def test_admin_and_reviewer_role_gates():
    assert AuthorizationService.require_admin("admin") is True
    assert AuthorizationService.require_reviewer_or_admin("admin") is True
    assert AuthorizationService.require_reviewer_or_admin("medical_reviewer") is True
