import pytest

from users.services import has_element_access


@pytest.mark.django_db
def test_has_element_access_own_vs_all(regular_user, issue_rule):
    issue_rule(
        "user",
        "order",
        read_permission=True,
        read_all_permission=False,
    )
    assert has_element_access(
        regular_user,
        "order",
        "read",
        owner_id=regular_user.pk,
    )
    assert not has_element_access(
        regular_user,
        "order",
        "read",
        owner_id=regular_user.pk + 1,
    )


@pytest.mark.django_db
def test_has_element_access_read_all(guest_user, issue_rule):
    issue_rule(
        "guest",
        "book",
        read_permission=False,
        read_all_permission=True,
    )
    assert has_element_access(
        guest_user,
        "book",
        "read",
        owner_id=None,
    )
