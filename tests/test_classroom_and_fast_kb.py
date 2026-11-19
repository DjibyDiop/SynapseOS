import os
import tempfile
import time
import unittest
from unittest.mock import patch

from cortex.engine import CortexEngine
from workbench.classroom_hub import ClassroomHubManager
from workbench.safe_media_sandbox import SafeMediaSandboxWidget


class TestFastSubMillisecondAndClassroomHub(unittest.TestCase):
    def setUp(self):
        self.engine = CortexEngine()

    def test_instant_1ms_button_never_blocks_on_ollama(self):
        """
        Regression test for 2009 MacBook Pro reviewer bug:
        Clicking '⚡ Instant (<1ms)' (force_llm=False) must NEVER invoke query_local_ollama()
        even for lab IDs like 'raycast_car', 'swarm_ecosystem', or arbitrary user text.
        """
        queries = [
            "moon_lander",
            "raycast_car",
            "rl_gridworld",
            "cartpole_rl",
            "nn_playground",
            "swarm_ecosystem",
            "prime_attention",
            "unmatched_custom_student_question_xyz",
        ]
        with patch.object(self.engine, "query_local_ollama", side_effect=AssertionError("Should NOT call Ollama when force_llm=False!")):
            for q in queries:
                t0 = time.perf_counter()
                res = self.engine.explain_ai_concept(q, force_llm=False)
                elapsed_ms = (time.perf_counter() - t0) * 1000.0
                self.assertIn("title", res)
                self.assertIn("SQLite FTS5", res.get("source", ""))
                self.assertLess(elapsed_ms, 25.0, f"Query '{q}' took {elapsed_ms:.2f}ms!")

            for cmd_q in ["check free memory", "unmatched_weird_linux_command_xyz"]:
                t0 = time.perf_counter()
                cmd_res = self.engine.synthesize_command_and_instructions(cmd_q, force_llm=False)
                elapsed_ms = (time.perf_counter() - t0) * 1000.0
                self.assertIn("command", cmd_res)
                self.assertLess(elapsed_ms, 25.0)

    def test_classroom_hub_broadcast_schedule_files_and_hands_up(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            state_file = os.path.join(tmpdir, "hub_state.json")
            files_dir = os.path.join(tmpdir, "shared_files")
            hub = ClassroomHubManager(state_path=state_file, shared_files_dir=files_dir, enable_udp=False)

            # 1. Schedule management
            initial_sched = hub.get_schedule()
            self.assertGreaterEqual(len(initial_sched), 4)
            updated_sched = hub.add_schedule_item(
                period="Period 5 (13:00 - 13:45)",
                title="Robotics Challenge",
                lab_id="raycast_car",
                mode="Student Mode",
            )
            self.assertEqual(len(updated_sched), len(initial_sched) + 1)

            # 2. File attachment & Course upload
            sample_py = os.path.join(tmpdir, "custom_reward.py")
            with open(sample_py, "w", encoding="utf-8") as f:
                f.write("def custom_reward(x): return x * 2.0\n")
            attached_name = hub.attach_file(sample_py)
            self.assertEqual(attached_name, "custom_reward.py")
            self.assertIn("custom_reward", hub.read_attached_file("custom_reward.py"))

            course = hub.upload_course(
                title="Teacher Custom Lidar Course",
                lab_id="raycast_car",
                description="Use 5 lasers to steer smoothly.",
                starter_code="print('Hello Classroom')",
                attached_files=[attached_name],
            )
            self.assertEqual(course["title"], "Teacher Custom Lidar Course")

            # 3. 1-Click LAN Broadcast
            bcast = hub.broadcast_to_classroom(
                title="All Students: Start Raycast Car!",
                message="Load custom_reward.py and test 5 laps.",
                lab_id="raycast_car",
                code_snippet="print('LAN Broadcast')",
                attached_files=[attached_name],
            )
            self.assertEqual(hub.get_state()["active_broadcast"]["id"], bcast["id"])

            # 4. Student Raise Hand with Code & Parameters, Teacher Reply & Teleport
            hand = hub.raise_hand(
                student_name="Djiby (2009 MacBook Pro)",
                question="How do I make the car slow down before sharp turns?",
                lab_id="raycast_car",
                level="Level 2",
                code_snippet="def steer(): return 0.5",
                lab_params={"sensor_range": 160.0, "max_speed": 4.5},
            )
            self.assertEqual(hand["status"], "open")
            self.assertEqual(hand["code_snippet"], "def steer(): return 0.5")

            # 5. Teacher Teleportation
            teleported = hub.teleport_to_student(hand["id"])
            self.assertIsNotNone(teleported)
            self.assertEqual(teleported["lab_id"], "raycast_car")
            self.assertEqual(teleported["lab_params"]["sensor_range"], 160.0)

            replied = hub.reply_to_hand(
                hand["id"],
                "Lower throttle to 0.4 when center raycast distance < 0.35!",
            )
            self.assertIsNotNone(replied)
            self.assertEqual(replied["status"], "answered")
            self.assertIn("Lower throttle", replied["teacher_reply"])

            # 6. Teacher Classroom Focus Mode (Pause Student Screens)
            f_res = hub.set_focus_mode(True, "Eyes on the whiteboard for 5 minutes!")
            self.assertTrue(f_res["enabled"])
            self.assertTrue(hub.get_focus_mode()["enabled"])
            self.assertIn("whiteboard", hub.get_focus_mode()["message"])

            hub.set_focus_mode(False)
            self.assertFalse(hub.get_focus_mode()["enabled"])

    def test_safe_media_sandbox_episodes_and_kiwix_search(self):
        episodes = SafeMediaSandboxWidget.get_episodes()
        self.assertGreaterEqual(len(episodes), 5)
        self.assertIn("Moon", episodes[0]["title"])
        self.assertTrue(any("Hyperdimensional" in ep["title"] for ep in episodes))

        kiwix_hits = SafeMediaSandboxWidget.search_encyclopedia("ternary")
        self.assertGreaterEqual(len(kiwix_hits), 1)
        self.assertIn("Ternary", kiwix_hits[0]["title"])

        hdc_hits = SafeMediaSandboxWidget.search_encyclopedia("hillock")
        self.assertGreaterEqual(len(hdc_hits), 1)
        self.assertIn("Hillock", hdc_hits[0]["title"])

    def test_udp_discovery_and_stations(self):
        from workbench.classroom_hub import ClassroomHubManager
        with tempfile.TemporaryDirectory() as tmpdir:
            state_file = os.path.join(tmpdir, "hub_state.json")
            files_dir = os.path.join(tmpdir, "shared_files")
            hub = ClassroomHubManager(state_path=state_file, shared_files_dir=files_dir, enable_udp=False)

            # Test discover_ping handling
            ping_pkt = {
                "type": "discover_ping",
                "payload": {"sender_ip": "192.168.1.199", "sender_host": "station-remote"},
            }
            hub._handle_incoming_udp(ping_pkt)

            # Test get_discovered_stations
            stations = hub.get_discovered_stations()
            self.assertIsInstance(stations, list)

            # Test update_student_telemetry and heartbeat
            hub.update_student_telemetry(
                student_name="Station-Test",
                active_lab="moon_lander",
                mode="Kid Arcade",
                best_score="+199.0",
                status="Active",
            )
            state = hub.get_state()
            self.assertIn("Station-Test", state.get("students_roster", {}))
            self.assertEqual(state["students_roster"]["Station-Test"]["best_score"], "+199.0")

    def test_kiwix_zim_scanner_and_server_fallback(self):
        from workbench.safe_media_sandbox import scan_local_zim_files, open_zim_with_kiwix_serve
        # Test scan_local_zim_files returns a list without crashing
        found = scan_local_zim_files()
        self.assertIsInstance(found, list)

        # Test open_zim_with_kiwix_serve on non-existent file
        res_nonexistent = open_zim_with_kiwix_serve("non_existent_file_xyz.zim")
        self.assertIn("introuvable", res_nonexistent)

        # Test open_zim_with_kiwix_serve fallback on a dummy zip file
        import zipfile
        with tempfile.NamedTemporaryFile(suffix=".zim", delete=False) as tf:
            tf_path = tf.name
        try:
            with zipfile.ZipFile(tf_path, "w") as zf:
                zf.writestr("index.html", "<html><body>Kiwix Article</body></html>")
            res_dummy = open_zim_with_kiwix_serve(tf_path)
            self.assertTrue("ZIM" in res_dummy or "kiwix-serve" in res_dummy)
        finally:
            if os.path.exists(tf_path):
                os.remove(tf_path)

    def test_teacher_dashboard_export_and_helpers(self):
        from workbench.teacher_dashboard import _esc, _resolve_tmp_path
        self.assertEqual(_esc("<script>alert('xss')</script>"), "&lt;script&gt;alert('xss')&lt;/script&gt;")
        tmp_path = _resolve_tmp_path("test_report.html")
        self.assertTrue(tmp_path.endswith("test_report.html"))


if __name__ == "__main__":
    unittest.main()
