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

    def test_exam_session_and_printable_worksheet(self):
        from workbench.classroom_hub import ClassroomHubManager
        with tempfile.TemporaryDirectory() as tmpdir:
            state_file = os.path.join(tmpdir, "hub_state.json")
            files_dir = os.path.join(tmpdir, "shared_files")
            hub = ClassroomHubManager(state_path=state_file, shared_files_dir=files_dir, enable_udp=False)

            # 1. Start timed exam
            exam = hub.start_exam(
                title="Contrôle de Physique Numérique",
                duration_minutes=30,
                instructions="Atteindre +200 points sur la Lune.",
                lab_id="moon_lander",
            )
            self.assertTrue(exam["active"])
            self.assertEqual(exam["duration_sec"], 1800)

            # 2. Check exam status
            st = hub.get_exam_status()
            self.assertTrue(st["active"])
            self.assertEqual(st["title"], "Contrôle de Physique Numérique")
            self.assertGreater(st["remaining_sec"], 0)

            # 3. Student submits work
            sub = hub.submit_exam_work(
                student_name="Élève-Test",
                code="def steer(): return 1.0",
                notes="Atterrissage réussi avec 10L de carburant restant",
            )
            self.assertEqual(sub["student_name"], "Élève-Test")
            self.assertIn("def steer", sub["code"])

            # 4. Check submission collected
            st_after = hub.get_exam_status()
            self.assertEqual(st_after["collected_count"], 1)
            self.assertIn("Élève-Test", st_after["submissions"])

            # 5. End exam
            hub.end_exam()
            st_ended = hub.get_exam_status()
            self.assertFalse(st_ended["active"])

            # 6. Test printable worksheet generation
            html = hub.export_printable_worksheet(
                title="Devoir sur Table",
                lab_id="Physique",
                questions=["Quelle est l'accélération de la gravité sur la Lune ?"],
                instructions="Remplissez les encadrés ci-dessous.",
            )
            self.assertIn("<!DOCTYPE html>", html)
            self.assertIn("Devoir sur Table", html)
            self.assertIn("Quelle est l'accélération", html)

    def test_direct_boot_no_menu_prompt(self):
        """Verify build-iso.sh configures instant direct boot without asking 3 options."""
        iso_script_path = os.path.join(os.path.dirname(__file__), "..", "distro", "build-iso.sh")
        with open(iso_script_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn('set timeout=0', content)
        self.assertIn('set timeout_style=hidden', content)

    def test_coop_mesh_pods_pairing_and_sync(self):
        from workbench.classroom_hub import ClassroomHubManager
        with tempfile.TemporaryDirectory() as tmpdir:
            state_file = os.path.join(tmpdir, "hub_state.json")
            files_dir = os.path.join(tmpdir, "shared_files")
            hub = ClassroomHubManager(state_path=state_file, shared_files_dir=files_dir, enable_udp=False)

            # 1. Pilot creates a Co-Op pod
            pod = hub.create_coop_pod(lab_id="moon_lander", student_name="Alice (Pilot)", role="pilot")
            self.assertEqual(pod["status"], "waiting")
            self.assertEqual(pod["host_role"], "pilot")
            self.assertEqual(len(hub.get_active_coop_pods()), 1)

            # 2. Engineer joins the pod
            joined = hub.join_coop_pod(pod["pod_id"], student_name="Bob (Engineer)", role="engineer")
            self.assertIsNotNone(joined)
            self.assertEqual(joined["status"], "paired")
            self.assertEqual(joined["partner_name"], "Bob (Engineer)")

            # 3. Telemetry sync
            hub.sync_coop_telemetry(
                pod["pod_id"],
                role="engineer",
                controls={"fuel_boost": 1.2, "gravity_damping": 0.9},
                telemetry={"altitude": 45.2, "speed": 1.1},
            )
            state = hub.get_state()
            active_pod = state["coop_pods"][pod["pod_id"]]
            self.assertEqual(active_pod["last_sync"]["controls"]["fuel_boost"], 1.2)

    def test_session_intelligence_and_airdrop_bundle(self):
        from workbench.classroom_hub import ClassroomHubManager
        with tempfile.TemporaryDirectory() as tmpdir:
            state_file = os.path.join(tmpdir, "hub_state.json")
            files_dir = os.path.join(tmpdir, "shared_files")
            hub = ClassroomHubManager(state_path=state_file, shared_files_dir=files_dir, enable_udp=False)

            # 1. Generate session intelligence report
            report = hub.generate_session_intelligence_report()
            self.assertIn("total_students", report)
            self.assertIn("mastery_rate", report)
            self.assertIn("summary_text", report)
            self.assertGreaterEqual(len(report["recommendations"]), 1)

            # 2. Air-drop export and import
            bundle_file = os.path.join(tmpdir, "airdrop_courses.json")
            out = hub.export_courses_airdrop_bundle(bundle_file)
            self.assertTrue(os.path.exists(out))

            # Import on a second hub
            state_file2 = os.path.join(tmpdir, "hub_state_2.json")
            hub2 = ClassroomHubManager(state_path=state_file2, shared_files_dir=files_dir, enable_udp=False)
            imported_count = hub2.import_courses_airdrop_bundle(bundle_file)
            self.assertIsInstance(imported_count, int)

    def test_lumi_adaptive_micro_pathing(self):
        from workbench.classroom_hub import LumiAdaptiveMicroPathing
        tutor = LumiAdaptiveMicroPathing(student_name="Student-Test")

        # 1. Normal single crash -> no intrusion
        res1 = tutor.record_attempt(score=-50.0, landed=False, lab_id="moon_lander")
        self.assertIsNone(res1)

        # 2. 3 consecutive crashes -> Socratic guidance triggered
        tutor.record_attempt(score=-80.0, landed=False, lab_id="moon_lander")
        res3 = tutor.record_attempt(
            score=-120.0,
            landed=False,
            lab_id="moon_lander",
            params={"gravity": -9.81, "fuel": 30.0},
        )
        self.assertIsNotNone(res3)
        self.assertEqual(res3["type"], "socratic_assistance")
        self.assertIn("Lumi", res3["title"])

        # 3. 3 consecutive successes -> Master challenge unlocked
        tutor.record_attempt(score=250.0, landed=True, lab_id="moon_lander")
        tutor.record_attempt(score=280.0, landed=True, lab_id="moon_lander")
        master_res = tutor.record_attempt(score=310.0, landed=True, lab_id="moon_lander")
        self.assertIsNotNone(master_res)
        self.assertEqual(master_res["type"], "master_challenge_unlocked")

    def test_learning_games_all_5_subjects_and_adventure_odyssey(self):
        from workbench.learning_games import (
            LearningGamesEngine,
            LearningGamesDialog,
            MATH_QUESTIONS,
            LANGUAGE_QUESTIONS,
            GEOGRAPHY_QUESTIONS,
            HISTORY_QUESTIONS,
            SCIENCE_QUESTIONS,
        )
        from workbench.pack_manager import LearningPackManager
        from workbench.classroom_hub import LumiAdaptiveMicroPathing

        # Verify 20+ questions per subject bank
        self.assertGreaterEqual(len(MATH_QUESTIONS), 20)
        self.assertGreaterEqual(len(LANGUAGE_QUESTIONS), 20)
        self.assertGreaterEqual(len(GEOGRAPHY_QUESTIONS), 20)
        self.assertGreaterEqual(len(HISTORY_QUESTIONS), 20)
        self.assertGreaterEqual(len(SCIENCE_QUESTIONS), 20)

        pack_mgr = LearningPackManager()
        tutor = LumiAdaptiveMicroPathing(student_name="TestCadet")
        engine = LearningGamesEngine(lang="en", pack_mgr=pack_mgr, adaptive_tutor=tutor)

        # 1. Math Quest
        self.assertTrue(engine.select_game("math"))
        q_math = engine.get_current_question()
        self.assertIn("question_en", q_math)
        res_math = engine.submit_answer(q_math["correct_idx"])
        self.assertTrue(res_math["is_correct"])
        self.assertGreater(res_math["points_earned"], 0)
        self.assertEqual(engine.combo_streak, 1)

        # 2. Language Voyage
        self.assertTrue(engine.select_game("language"))
        q_lang = engine.get_current_question()
        self.assertIn("question_en", q_lang)
        res_wrong = engine.submit_answer((q_lang["correct_idx"] + 1) % 4)
        self.assertFalse(res_wrong["is_correct"])
        self.assertEqual(engine.combo_streak, 0)

        # 3. Geo Explorer
        self.assertTrue(engine.select_game("geography"))
        q_geo = engine.get_current_question()
        self.assertIn("category", q_geo)

        # 4. Time Traveler (History)
        self.assertTrue(engine.select_game("history"))
        q_hist = engine.get_current_question()
        self.assertIn("options", q_hist)

        # 5. Science Explorer (New 6th Educational Game)
        self.assertTrue(engine.select_game("science"))
        q_sci = engine.get_current_question()
        self.assertIn("Physics", q_sci.get("category", "") + q_sci.get("question_en", ""))
        res_sci = engine.submit_answer(q_sci["correct_idx"])
        self.assertTrue(res_sci["is_correct"])
        self.assertEqual(engine.combo_streak, 1)

        # 6. Adventure Odyssey Dungeon Quest (across all 5 fields)
        self.assertTrue(engine.select_game("adventure"))
        q_adv = engine.get_current_question()
        self.assertEqual(q_adv["room_num"], 1)
        self.assertEqual(q_adv["gems"], 0)

        # Solve rooms to advance
        for _ in range(5):
            cur_q = engine.get_current_question()
            engine.submit_answer(cur_q["correct_idx"])
            engine.next_question()

        metrics = engine.get_summary_metrics()
        self.assertEqual(metrics["dungeon_gems"], 5)
        self.assertTrue(metrics["dungeon_completed"])
        self.assertGreater(metrics["score"], 400)
        self.assertIn("subject_stats", metrics)

        # Verify Student Profile Persistence & Report Card Export
        profile_stats = pack_mgr.profile.get("learning_games_stats", {})
        self.assertGreater(profile_stats.get("total_answered", 0), 5)
        self.assertGreater(profile_stats.get("total_correct", 0), 4)

        report = pack_mgr.export_printable_report_card()
        self.assertTrue(os.path.exists(report["html_path"]))
        with open(report["html_path"], "r", encoding="utf-8") as f:
            html_text = f.read()
        self.assertIn("Learning Games Stats", html_text)

        # 6. Test Dialog headless instantiation
        dlg = LearningGamesDialog(parent_window=None, lang="en")
        self.assertIsNotNone(dlg.engine)

    def test_multidisciplinary_worksheet_and_kb_entries(self):
        from workbench.classroom_hub import ClassroomHubManager
        from cortex.engine import CortexEngine

        hub = ClassroomHubManager(enable_udp=False)
        for subj in ("math", "science", "atom_physics"):
            qs = hub.generate_subject_worksheet_questions(subject=subj, count=4, lang="fr")
            self.assertEqual(len(qs), 4)
            html = hub.export_printable_worksheet(title=f"Eval {subj}", lab_id=subj, questions=qs)
            self.assertIn("SynapseOS", html)

        # Verify Level 8 in Kid Arcade (works even headless without gi)
        kav_path = os.path.join(os.path.dirname(__file__), "..", "workbench", "kid_arcade_view.py")
        with open(kav_path, "r", encoding="utf-8") as f:
            kav_src = f.read()
        self.assertIn('"lab_id": "atom_physics"', kav_src)
        self.assertIn("Level 8: Quantum Molecule Builder", kav_src)

        # Verify FTS5 KB entries for Lab 8 and Learning Games
        ce = CortexEngine()
        r_atom = ce.kb.search_ai("atom physics", limit=1)
        self.assertTrue(len(r_atom) >= 1)
        self.assertIn("Atom", r_atom[0]["title"])
        r_games = ce.kb.search_ai("learning games", limit=1)
        self.assertTrue(len(r_games) >= 1)
        self.assertIn("Learning Games", r_games[0]["title"])


if __name__ == "__main__":
    unittest.main()
