from django.test import TestCase
from rest_framework.test import APIClient
from accounts.models import User
from curriculum.models import Track, Level, Challenge

class ProgressTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="Password123!")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.track1 = Track.objects.create(slug="track1", name="Track 1", required_xp=0, order=1)
        self.level1 = Level.objects.create(track=self.track1, index=1, title="L1", xp_reward=50)
        self.level2 = Level.objects.create(track=self.track1, index=2, title="L2", xp_reward=50)

        self.mcq = Challenge.objects.create(
            level=self.level1,
            order=1,
            kind="mcq",
            title="Q1",
            prompt="Choose",
            xp=20,
            config={"options": ["A", "B", "C"]},
            solution={"answer": 1}
        )

        self.code_ch = Challenge.objects.create(
            level=self.level1,
            order=2,
            kind="code",
            title="Q2",
            prompt="Square",
            xp=30,
            config={"language": "python"},
            solution={
                "entrypoint": "square",
                "cases": [
                    {"args": [4], "expect": 16},
                    {"args": [5], "expect": 25, "hidden": True}
                ]
            }
        )

    def test_mcq_submission(self):
        # Incorrect submission
        res = self.client.post(f"/api/challenges/{self.mcq.id}/submit/", {"choice": 0}, format="json")
        self.assertEqual(res.status_code, 200)
        self.assertFalse(res.data["correct"])
        self.assertEqual(res.data["xp_awarded"], 0)

        # Correct submission
        res = self.client.post(f"/api/challenges/{self.mcq.id}/submit/", {"choice": 1}, format="json")
        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.data["correct"])
        self.assertEqual(res.data["xp_awarded"], 20)
        self.user.refresh_from_db()
        self.assertEqual(self.user.total_xp, 20)

    def test_code_submission(self):
        res = self.client.post(f"/api/challenges/{self.code_ch.id}/submit/", {
            "source": "def square(n):\n    return n * n\n"
        }, format="json")
        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.data["correct"])
        self.assertEqual(res.data["xp_awarded"], 30)
        self.assertEqual(res.data["detail"]["passed_count"], 2)

    def test_level_unlock_and_completion(self):
        # Level 2 should initially be locked
        res = self.client.get(f"/api/levels/{self.level2.id}/")
        self.assertEqual(res.status_code, 403)
        self.assertTrue(res.data["locked"])

        # Complete all challenges in level 1
        self.client.post(f"/api/challenges/{self.mcq.id}/submit/", {"choice": 1}, format="json")
        res2 = self.client.post(f"/api/challenges/{self.code_ch.id}/submit/", {
            "source": "def square(n):\n    return n * n\n"
        }, format="json")
        self.assertTrue(res2.data["level_completed"])

        # Level 2 should now be unlocked!
        res_l2 = self.client.get(f"/api/levels/{self.level2.id}/")
        self.assertEqual(res_l2.status_code, 200)

    def test_short_and_multi_challenge(self):
        short_ch = Challenge.objects.create(
            level=self.level1,
            order=3,
            kind="short",
            title="Short Q",
            prompt="Answer",
            xp=15,
            solution={"accept": ["O(1)", "O(log n)"], "ignore_case": True}
        )
        multi_ch = Challenge.objects.create(
            level=self.level1,
            order=4,
            kind="multi",
            title="Multi Q",
            prompt="Pick two",
            xp=25,
            config={"options": ["A", "B", "C", "D"]},
            solution={"answers": [0, 2]}
        )

        # Short answer test
        s_res = self.client.post(f"/api/challenges/{short_ch.id}/submit/", {"text": "  o(1) "}, format="json")
        self.assertTrue(s_res.data["correct"])

        # Multi answer test: partial should fail
        m_res1 = self.client.post(f"/api/challenges/{multi_ch.id}/submit/", {"choices": [0]}, format="json")
        self.assertFalse(m_res1.data["correct"])

        # Exact choices should pass
        m_res2 = self.client.post(f"/api/challenges/{multi_ch.id}/submit/", {"choices": [2, 0]}, format="json")
        self.assertTrue(m_res2.data["correct"])

    def test_history_and_reset(self):
        res = self.client.get("/api/history/")
        self.assertEqual(res.status_code, 200)
        self.assertIn("vault", res.data)
        self.assertIn("total_solved", res.data)

        # Test reset level
        reset_res = self.client.post(f"/api/levels/{self.level1.id}/reset/")
        self.assertEqual(reset_res.status_code, 200)
        self.assertTrue(reset_res.data["success"])
