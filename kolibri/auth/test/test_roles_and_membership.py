"""
Tests of role and membership calculations.
"""

from __future__ import absolute_import, print_function, unicode_literals

from django.test import TestCase

from ..constants import role_kinds
from ..models import DeviceOwner
from .helpers import create_dummy_facility_data


def flatten(lst):
    if lst == []:
        return lst
    if isinstance(lst[0], list):
        return flatten(lst[0]) + flatten(lst[1:])
    return lst[:1] + flatten(lst[1:])


class RolesWithinFacilityTestCase(TestCase):

    def setUp(self):
        self.data = create_dummy_facility_data()

    def test_admin_has_admin_role_for_own_facility(self):
        admin = self.data["facility_admin"]
        facility = self.data["facility"]
        self.assertTrue(admin.has_role_for(role_kinds.ADMIN, facility))
        self.assertIn(role_kinds.ADMIN, admin.get_roles_for(facility))

    def test_coach_has_coach_role_for_own_classroom(self):
        coach0 = self.data["classroom_coaches"][0]
        classroom0 = self.data["classrooms"][0]
        self.assertTrue(coach0.has_role_for(role_kinds.COACH, classroom0))
        self.assertIn(role_kinds.COACH, coach0.get_roles_for(classroom0))

    def test_coach_has_no_coach_role_for_other_classroom(self):
        coach0 = self.data["classroom_coaches"][0]
        classroom1 = self.data["classrooms"][1]
        self.assertFalse(coach0.has_role_for(role_kinds.COACH, classroom1))
        self.assertNotIn(role_kinds.COACH, coach0.get_roles_for(classroom1))

    def test_coach_has_coach_role_for_learner_from_own_classroom(self):
        coach0 = self.data["classroom_coaches"][0]
        learner0 = self.data["learners_one_group"][0][0]
        self.assertTrue(coach0.has_role_for(role_kinds.COACH, learner0))
        self.assertIn(role_kinds.COACH, coach0.get_roles_for(learner0))

    def test_coach_has_no_coach_role_for_learner_from_other_classroom(self):
        coach0 = self.data["classroom_coaches"][0]
        learner1 = self.data["learners_one_group"][1][0]
        self.assertFalse(coach0.has_role_for(role_kinds.COACH, learner1))
        self.assertNotIn(role_kinds.COACH, coach0.get_roles_for(learner1))


class RolesAcrossFacilitiesTestCase(TestCase):

    def setUp(self):
        self.data1 = create_dummy_facility_data()
        self.data2 = create_dummy_facility_data()

    def test_no_roles_between_users_across_facilities(self):
        users1 = self.data1["all_users"]
        users2 = self.data2["all_users"]
        for user1 in users1:
            for user2 in users2:
                self.assertEqual(len(user1.get_roles_for(user2)), 0)

    def test_no_roles_for_collections_across_facilities(self):
        users1 = self.data1["classroom_coaches"] + [self.data1["facility_admin"]] + list(self.data1["facility"].get_members())
        collections2 = [self.data2["facility"]] + self.data2["classrooms"] + flatten(self.data2["learnergroups"])
        for user1 in users1:
            for collection2 in collections2:
                self.assertEqual(len(user1.get_roles_for(collection2)), 0)


class MembershipWithinFacilityTestCase(TestCase):

    def setUp(self):
        self.data = create_dummy_facility_data()

    def test_facility_membership(self):
        actual_members = flatten(self.data["learners_one_group"] + [self.data["learner_all_groups"]] +
                                 self.data["unattached_users"] + [self.data["facility_admin"]] +
                                 [self.data["facility_coach"]] + self.data["classroom_admins"] +
                                 self.data["classroom_coaches"])
        returned_members = self.data["facility"].get_members()
        self.assertSetEqual(set(actual_members), set(returned_members))
        for user in actual_members:
            self.assertTrue(user.is_member_of(self.data["facility"]))

    def test_classroom_membership(self):
        for i, classroom in enumerate(self.data["classrooms"]):
            actual_members = flatten(self.data["learners_one_group"][i] + [self.data["learner_all_groups"]])
            returned_members = classroom.get_members()
            self.assertSetEqual(set(actual_members), set(returned_members))
            # ensure that `is_member` is True for all users in the classroom
            for user in actual_members:
                self.assertTrue(user.is_member_of(classroom))
            # ensure that `is_member` is False for all users not in the classroom
            for user in set(self.data["all_users"]) - set(actual_members):
                self.assertFalse(user.is_member_of(classroom))

    def test_learnergroup_membership(self):
        for i, classroom_users in enumerate(self.data["learners_one_group"]):
            for j, learnergroup_users in enumerate(classroom_users):
                learnergroup = self.data["learnergroups"][i][j]
                actual_members = [self.data["learners_one_group"][i][j]] + [self.data["learner_all_groups"]]
                returned_members = learnergroup.get_members()
                self.assertSetEqual(set(actual_members), set(returned_members))
                # ensure that `is_member` is True for all users in the learnergroup
                for user in actual_members:
                    self.assertTrue(user.is_member_of(learnergroup))
                # ensure that `is_member` is False for all users not in the learnergroup
                for user in set(self.data["all_users"]) - set(actual_members):
                    self.assertFalse(user.is_member_of(learnergroup))


class MembershipAcrossFacilitiesTestCase(TestCase):

    def setUp(self):
        self.data1 = create_dummy_facility_data()
        self.data2 = create_dummy_facility_data()

    def test_users_are_not_members_of_other_facility(self):
        for user in self.data1["all_users"]:
            self.assertFalse(user.is_member_of(self.data2["facility"]))

    def test_users_are_not_members_of_other_facility_classroom(self):
        for user in self.data1["all_users"]:
            self.assertFalse(user.is_member_of(self.data2["classrooms"][0]))

    def test_users_are_not_members_of_other_facility_learnergroup(self):
        for user in self.data1["all_users"]:
            self.assertFalse(user.is_member_of(self.data2["learnergroups"][0][0]))


class DeviceOwnerRolesTestCase(TestCase):

    def setUp(self):
        self.data = create_dummy_facility_data()
        self.device_owner = DeviceOwner.objects.create(username="blooh", password="#")
        self.device_owner2 = DeviceOwner.objects.create(username="blaah", password="#")

    def test_device_owner_has_admin_role_for_everyone(self):
        for user in self.data["all_users"]:
            self.assertTrue(self.device_owner.has_role_for(role_kinds.ADMIN, user))

    def test_device_owner_has_admin_role_for_all_collections(self):
        for coll in self.data["all_collections"]:
            self.assertTrue(self.device_owner.has_role_for(role_kinds.ADMIN, coll))

    def test_nobody_has_roles_to_device_owner(self):
        for user in self.data["all_users"]:
            self.assertEqual(len(user.get_roles_for(self.device_owner)), 0)

    def test_device_owner_has_admin_role_for_itself(self):
        self.assertTrue(self.device_owner.has_role_for(role_kinds.ADMIN, self.device_owner))

    def test_device_owner_has_admin_role_for_other_device_owner(self):
        self.assertTrue(self.device_owner.has_role_for(role_kinds.ADMIN, self.device_owner2))
