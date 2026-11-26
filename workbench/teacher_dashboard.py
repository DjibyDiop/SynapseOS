"""
SynapseOS Teacher Dashboard Dialog
===================================
A standalone GTK3 dialog with 5 tabs for the classroom teacher:
  1. 📋 Registre de classe  — live student roster
  2. 📅 Planning           — editable schedule
  3. 📝 Notes / Bulletin   — grades + HTML export
  4. 📢 Diffusion rapide   — 1-click LAN broadcast
  5. ✋ Main levée          — student hands-up queue

Dependencies: stdlib + gi.repository only (zero external packages).
"""

import os
import time

try:
    import gi
    gi.require_version("Gtk", "3.0")
    from gi.repository import Gtk, GLib  # noqa: E402
    GTK_AVAILABLE = True
except Exception:
    GTK_AVAILABLE = False
    Gtk = None  # type: ignore[assignment]
    GLib = None  # type: ignore[assignment]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _ts() -> str:
    return time.strftime("%H:%M:%S")


def _safe_call(fn, *args, default=None, **kwargs):
    """Call fn(*args, **kwargs) and return default on any exception."""
    try:
        return fn(*args, **kwargs)
    except Exception:
        return default


# ---------------------------------------------------------------------------
# Main dialog class
# ---------------------------------------------------------------------------

class TeacherDashboardDialog:
    """
    Modal (blocking) GTK3 dialog that wraps the full teacher dashboard.

    Usage::

        TeacherDashboardDialog(hub=self.hub, parent_window=self.window).show()
    """

    def __init__(self, hub, parent_window=None):
        self.hub = hub
        self._grade_data: dict = {}           # {student_name: (grade, comment)}
        self._refresh_timer_id = None

        if not GTK_AVAILABLE:
            self.dialog = None
            return

        # ---- Root dialog ------------------------------------------------
        self.dialog = Gtk.Dialog(
            title="🏫 Tableau de bord Professeur",
            transient_for=parent_window,
            flags=0,
        )
        self.dialog.set_default_size(960, 640)
        self.dialog.set_resizable(True)
        self.dialog.add_button("Fermer", Gtk.ResponseType.CLOSE)

        content = self.dialog.get_content_area()
        content.set_margin_top(6)
        content.set_margin_bottom(6)
        content.set_margin_start(6)
        content.set_margin_end(6)

        # ---- Notebook (5 tabs) ------------------------------------------
        self.notebook = Gtk.Notebook()
        self.notebook.set_scrollable(True)
        content.pack_start(self.notebook, True, True, 0)

        self._build_tab_roster()
        self._build_tab_schedule()
        self._build_tab_grades()
        self._build_tab_broadcast()
        self._build_tab_hands_up()
        self._build_tab_exam()

        self.dialog.show_all()

        # Initial data load
        self._refresh_roster()
        self._refresh_schedule()
        self._refresh_hands()

        # Auto-refresh timer (5 s)
        self._refresh_timer_id = GLib.timeout_add(5000, self._auto_refresh)

    # ======================================================================
    # Tab 1 — 📋 Registre de classe
    # ======================================================================

    def _build_tab_roster(self):
        label = Gtk.Label(label="📋 Registre")

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        vbox.set_margin_top(6)
        vbox.set_margin_bottom(6)
        vbox.set_margin_start(6)
        vbox.set_margin_end(6)

        # Toolbar
        toolbar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
        btn_refresh = Gtk.Button(label="↻ Actualiser")
        btn_refresh.connect("clicked", lambda _b: self._refresh_roster())
        toolbar.pack_start(btn_refresh, False, False, 0)

        btn_report = Gtk.Button(label="📊 Bilan de Séance")
        btn_report.set_tooltip_text("Génère une synthèse pédagogique intelligente de la séance (taux de maîtrise, points de blocage)")
        btn_report.connect("clicked", lambda _b: self._on_show_session_report())
        toolbar.pack_start(btn_report, False, False, 0)

        self._roster_status_lbl = Gtk.Label(label="")
        toolbar.pack_start(self._roster_status_lbl, False, False, 6)
        vbox.pack_start(toolbar, False, False, 0)

        # TreeView  — Nom | IP | Lab actif | Meilleur score | Statut | Dernière vue
        self._roster_store = Gtk.ListStore(str, str, str, str, str, str)
        tv = Gtk.TreeView(model=self._roster_store)
        tv.set_grid_lines(Gtk.TreeViewGridLines.HORIZONTAL)

        col_defs = [
            ("Nom", 0, 170),
            ("IP", 1, 110),
            ("Lab actif", 2, 110),
            ("Meilleur score", 3, 130),
            ("Statut", 4, 130),
            ("Dernière vue", 5, 90),
        ]
        for title, col_idx, width in col_defs:
            renderer = Gtk.CellRendererText()
            col = Gtk.TreeViewColumn(title, renderer, text=col_idx)
            col.set_min_width(width)
            col.set_resizable(True)
            tv.append_column(col)

        self._roster_tv = tv
        sw = Gtk.ScrolledWindow()
        sw.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        sw.add(tv)
        vbox.pack_start(sw, True, True, 0)

        self.notebook.append_page(vbox, label)

    def _refresh_roster(self):
        try:
            state = _safe_call(self.hub.get_state, default={})
            roster = state.get("students_roster", {}) if state else {}
            self._roster_store.clear()
            for _key, info in roster.items():
                self._roster_store.append([
                    info.get("student_name", _key),
                    info.get("ip", "—"),
                    info.get("active_lab", "—"),
                    info.get("best_score", "—"),
                    info.get("status", "—"),
                    info.get("last_seen", "—"),
                ])
            count = len(roster)
            self._roster_status_lbl.set_text(
                f"{count} élève{'s' if count != 1 else ''} · MAJ {_ts()}"
            )
        except Exception:
            self._roster_status_lbl.set_text("⚠ Impossible de charger le registre")
        return False  # for GLib.timeout_add — do NOT reschedule automatically

    def _on_show_session_report(self):
        """Affiche le Bilan de Séance Automatisé (Invisible Assessment & Class Intelligence)."""
        report = _safe_call(self.hub.generate_session_intelligence_report, default={})
        summary = report.get("summary_text", "Aucune donnée disponible.")

        dlg = Gtk.Dialog(
            title="📊 Bilan Pédagogique de Séance",
            transient_for=self.dialog,
            flags=0,
        )
        dlg.set_default_size(650, 450)
        dlg.add_button("Fermer", Gtk.ResponseType.CLOSE)

        content = dlg.get_content_area()
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        tv = Gtk.TextView()
        tv.set_editable(False)
        tv.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        tv.set_left_margin(12)
        tv.set_right_margin(12)
        tv.set_top_margin(10)
        buf = tv.get_buffer()
        buf.set_text(summary)
        scroll.add(tv)
        content.pack_start(scroll, True, True, 0)
        dlg.show_all()
        dlg.run()
        dlg.destroy()

    # ======================================================================
    # Tab 2 — 📅 Planning
    # ======================================================================

    def _build_tab_schedule(self):
        label = Gtk.Label(label="📅 Planning")

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        vbox.set_margin_top(6)
        vbox.set_margin_bottom(6)
        vbox.set_margin_start(6)
        vbox.set_margin_end(6)

        # --- Add form ---
        form_frame = Gtk.Frame(label=" Nouvelle période ")
        form_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
        form_vbox.set_margin_top(4)
        form_vbox.set_margin_bottom(4)
        form_vbox.set_margin_start(6)
        form_vbox.set_margin_end(6)
        form_frame.add(form_vbox)

        def _lbl_entry(placeholder):
            e = Gtk.Entry()
            e.set_placeholder_text(placeholder)
            return e

        row1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
        self._sched_period_entry = _lbl_entry("Période (ex: Period 5 — 11:55-12:40)")
        self._sched_topic_entry  = _lbl_entry("Sujet / titre")
        row1.pack_start(self._sched_period_entry, True, True, 0)
        row1.pack_start(self._sched_topic_entry, True, True, 0)
        form_vbox.pack_start(row1, False, False, 0)

        row2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
        self._sched_labid_entry = _lbl_entry("Lab ID (ex: moon_lander)")
        self._sched_mode_entry  = _lbl_entry("Mode (ex: Kid Arcade)")
        btn_add = Gtk.Button(label="+ Ajouter")
        btn_add.connect("clicked", self._on_schedule_add)
        row2.pack_start(self._sched_labid_entry, True, True, 0)
        row2.pack_start(self._sched_mode_entry, True, True, 0)
        row2.pack_start(btn_add, False, False, 0)
        form_vbox.pack_start(row2, False, False, 0)

        vbox.pack_start(form_frame, False, False, 0)

        # --- TreeView ---
        self._sched_store = Gtk.ListStore(str, str, str, str)  # period, topic, lab_id, mode
        tv = Gtk.TreeView(model=self._sched_store)
        tv.set_grid_lines(Gtk.TreeViewGridLines.HORIZONTAL)

        for title, col_idx, width in [
            ("Période", 0, 190),
            ("Sujet", 1, 220),
            ("Lab ID", 2, 110),
            ("Mode", 3, 140),
        ]:
            renderer = Gtk.CellRendererText()
            col = Gtk.TreeViewColumn(title, renderer, text=col_idx)
            col.set_min_width(width)
            col.set_resizable(True)
            tv.append_column(col)

        self._sched_tv = tv
        sw = Gtk.ScrolledWindow()
        sw.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        sw.add(tv)
        vbox.pack_start(sw, True, True, 0)

        # --- Delete toolbar ---
        del_bar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
        btn_del = Gtk.Button(label="✕ Supprimer sélection")
        btn_del.connect("clicked", self._on_schedule_delete)
        del_bar.pack_end(btn_del, False, False, 0)
        vbox.pack_start(del_bar, False, False, 0)

        self.notebook.append_page(vbox, label)

    def _refresh_schedule(self):
        try:
            schedule = _safe_call(self.hub.get_schedule, default=[]) or []
            self._sched_store.clear()
            for item in schedule:
                self._sched_store.append([
                    item.get("period", ""),
                    item.get("title", ""),
                    item.get("lab_id", ""),
                    item.get("mode", ""),
                ])
        except Exception:
            pass
        return False

    def _on_schedule_add(self, _btn):
        period = self._sched_period_entry.get_text().strip()
        topic  = self._sched_topic_entry.get_text().strip()
        lab_id = self._sched_labid_entry.get_text().strip()
        mode   = self._sched_mode_entry.get_text().strip()
        if not period:
            period = f"Période {self._sched_store.iter_n_children(None) + 1}"
        try:
            self.hub.add_schedule_item(
                period=period,
                title=topic or "Lab Session",
                lab_id=lab_id or "moon_lander",
                mode=mode or "Student Mode",
            )
            self._refresh_schedule()
            for entry in [self._sched_period_entry, self._sched_topic_entry,
                          self._sched_labid_entry, self._sched_mode_entry]:
                entry.set_text("")
        except Exception:
            pass

    def _on_schedule_delete(self, _btn):
        selection = self._sched_tv.get_selection()
        model, itr = selection.get_selected()
        if itr is None:
            return
        path = model.get_path(itr)
        index = path.get_indices()[0]
        try:
            self.hub.remove_schedule_item(index)
            self._refresh_schedule()
        except Exception:
            pass

    # ======================================================================
    # Tab 3 — 📝 Notes / Bulletin
    # ======================================================================

    def _build_tab_grades(self):
        label = Gtk.Label(label="📝 Notes")

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        vbox.set_margin_top(6)
        vbox.set_margin_bottom(6)
        vbox.set_margin_start(6)
        vbox.set_margin_end(6)

        info_lbl = Gtk.Label(
            label="Double-cliquez une cellule pour la modifier. Les notes sont sauvegardées localement."
        )
        info_lbl.set_xalign(0)
        info_lbl.set_line_wrap(True)
        vbox.pack_start(info_lbl, False, False, 0)

        # ListStore: nom, note, commentaire
        self._grades_store = Gtk.ListStore(str, str, str)

        tv = Gtk.TreeView(model=self._grades_store)
        tv.set_grid_lines(Gtk.TreeViewGridLines.BOTH)

        # Col 0 — Nom (read-only)
        r0 = Gtk.CellRendererText()
        c0 = Gtk.TreeViewColumn("Nom élève", r0, text=0)
        c0.set_min_width(170)
        c0.set_resizable(True)
        tv.append_column(c0)

        # Col 1 — Note (editable)
        r1 = Gtk.CellRendererText()
        r1.set_property("editable", True)
        r1.connect("edited", self._on_grade_edited, 1)
        c1 = Gtk.TreeViewColumn("Note (A/B/C/D/E ou %)", r1, text=1)
        c1.set_min_width(140)
        c1.set_resizable(True)
        tv.append_column(c1)

        # Col 2 — Commentaire (editable)
        r2 = Gtk.CellRendererText()
        r2.set_property("editable", True)
        r2.connect("edited", self._on_grade_edited, 2)
        c2 = Gtk.TreeViewColumn("Commentaire", r2, text=2)
        c2.set_min_width(260)
        c2.set_resizable(True)
        tv.append_column(c2)

        self._grades_tv = tv
        sw = Gtk.ScrolledWindow()
        sw.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        sw.add(tv)
        vbox.pack_start(sw, True, True, 0)

        # Toolbar
        toolbar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
        btn_reload = Gtk.Button(label="↻ Recharger depuis le registre")
        btn_reload.connect("clicked", lambda _b: self._reload_grades_from_roster())
        btn_export = Gtk.Button(label="📄 Exporter HTML")
        btn_export.connect("clicked", lambda _b: self._export_bulletin_html())
        self._grades_status_lbl = Gtk.Label(label="")
        toolbar.pack_start(btn_reload, False, False, 0)
        toolbar.pack_start(btn_export, False, False, 0)
        toolbar.pack_start(self._grades_status_lbl, False, False, 6)
        vbox.pack_start(toolbar, False, False, 0)

        self.notebook.append_page(vbox, label)
        # Pre-populate from roster
        self._reload_grades_from_roster()

    def _reload_grades_from_roster(self):
        try:
            state = _safe_call(self.hub.get_state, default={}) or {}
            roster = state.get("students_roster", {})
            # Keep existing grade data
            existing = {}
            itr = self._grades_store.get_iter_first()
            while itr:
                name  = self._grades_store.get_value(itr, 0)
                grade = self._grades_store.get_value(itr, 1)
                comment = self._grades_store.get_value(itr, 2)
                existing[name] = (grade, comment)
                itr = self._grades_store.iter_next(itr)

            self._grades_store.clear()
            for _key, info in roster.items():
                name = info.get("student_name", _key)
                grade, comment = existing.get(name, ("", ""))
                self._grades_store.append([name, grade, comment])

            self._grades_status_lbl.set_text(f"MAJ {_ts()}")
        except Exception:
            self._grades_status_lbl.set_text("⚠ Erreur chargement registre")

    def _on_grade_edited(self, renderer, path_str, new_text, col_idx):
        try:
            itr = self._grades_store.get_iter_from_string(path_str)
            self._grades_store.set_value(itr, col_idx, new_text)
        except Exception:
            pass

    def _export_bulletin_html(self):
        try:
            rows_html = ""
            itr = self._grades_store.get_iter_first()
            while itr:
                nom     = self._grades_store.get_value(itr, 0)
                note    = self._grades_store.get_value(itr, 1) or "—"
                comment = self._grades_store.get_value(itr, 2) or ""
                # Simple grade-colour mapping
                colour = {
                    "A": "#16a34a", "B": "#2563eb", "C": "#d97706",
                    "D": "#ea580c", "E": "#dc2626",
                }.get(note.strip().upper(), "#374151")
                rows_html += (
                    f"<tr>"
                    f"<td>{_esc(nom)}</td>"
                    f"<td style='color:{colour};font-weight:bold'>{_esc(note)}</td>"
                    f"<td>{_esc(comment)}</td>"
                    f"</tr>\n"
                )
                itr = self._grades_store.iter_next(itr)

            html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <title>Bulletin SynapseOS</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 40px; color: #111; }}
    h1   {{ color: #1d4ed8; }}
    table {{ border-collapse: collapse; width: 100%; margin-top: 20px; }}
    th   {{ background: #1d4ed8; color: #fff; padding: 8px 12px; text-align: left; }}
    td   {{ border: 1px solid #d1d5db; padding: 7px 12px; }}
    tr:nth-child(even) {{ background: #f3f4f6; }}
  </style>
</head>
<body>
  <h1>🏫 Bulletin SynapseOS</h1>
  <p>Généré le {time.strftime("%d/%m/%Y à %H:%M:%S")}</p>
  <table>
    <thead>
      <tr><th>Nom élève</th><th>Note</th><th>Commentaire</th></tr>
    </thead>
    <tbody>
{rows_html}    </tbody>
  </table>
</body>
</html>"""
            # On Windows /tmp may not exist; fall back to temp dir
            out_path = _resolve_tmp_path("synapse_bulletin.html")
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(html)
            self._grades_status_lbl.set_text(f"✓ Exporté → {out_path}")
        except Exception as exc:
            self._grades_status_lbl.set_text(f"⚠ Erreur export: {exc}")

    # ======================================================================
    # Tab 4 — 📢 Diffusion rapide
    # ======================================================================

    def _build_tab_broadcast(self):
        label = Gtk.Label(label="📢 Diffusion")

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        vbox.set_margin_top(10)
        vbox.set_margin_bottom(10)
        vbox.set_margin_start(10)
        vbox.set_margin_end(10)

        frame = Gtk.Frame(label=" Message à diffuser sur le réseau de classe ")
        inner = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        inner.set_margin_top(8)
        inner.set_margin_bottom(8)
        inner.set_margin_start(8)
        inner.set_margin_end(8)
        frame.add(inner)

        # Title row
        title_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
        lbl_t = Gtk.Label(label="Titre :")
        lbl_t.set_xalign(1)
        lbl_t.set_size_request(60, -1)
        self._bcast_title_entry = Gtk.Entry()
        self._bcast_title_entry.set_placeholder_text("ex: Rappel — sauvegardez votre travail !")
        title_row.pack_start(lbl_t, False, False, 0)
        title_row.pack_start(self._bcast_title_entry, True, True, 0)
        inner.pack_start(title_row, False, False, 0)

        # Message row
        msg_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
        lbl_m = Gtk.Label(label="Message :")
        lbl_m.set_xalign(1)
        lbl_m.set_size_request(60, -1)
        sw_msg = Gtk.ScrolledWindow()
        sw_msg.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        sw_msg.set_size_request(-1, 90)
        self._bcast_msg_buf = Gtk.TextBuffer()
        tv_msg = Gtk.TextView(buffer=self._bcast_msg_buf)
        tv_msg.set_wrap_mode(Gtk.WrapMode.WORD)
        sw_msg.add(tv_msg)
        msg_row.pack_start(lbl_m, False, False, 0)
        msg_row.pack_start(sw_msg, True, True, 0)
        inner.pack_start(msg_row, False, False, 0)

        # Send button
        btn_send = Gtk.Button(label="📡 Envoyer à tous")
        btn_send.connect("clicked", self._on_broadcast_send)
        inner.pack_start(btn_send, False, False, 4)

        self._bcast_status_lbl = Gtk.Label(label="")
        self._bcast_status_lbl.set_xalign(0)
        inner.pack_start(self._bcast_status_lbl, False, False, 0)

        vbox.pack_start(frame, False, False, 0)
        self.notebook.append_page(vbox, label)

    def _on_broadcast_send(self, _btn):
        title = self._bcast_title_entry.get_text().strip()
        buf   = self._bcast_msg_buf
        message = buf.get_text(buf.get_start_iter(), buf.get_end_iter(), False).strip()

        if not title:
            title = "Message du professeur"
        if not message:
            self._bcast_status_lbl.set_text("⚠ Le message ne peut pas être vide.")
            return
        try:
            result = self.hub.broadcast_to_classroom(title=title, message=message)
            # Count students in roster
            state   = _safe_call(self.hub.get_state, default={}) or {}
            n_students = len(state.get("students_roster", {}))
            self._bcast_status_lbl.set_text(
                f"✓ Diffusé à {n_students} élève(s) · {_ts()}"
            )
            self._bcast_title_entry.set_text("")
            buf.set_text("")
        except Exception as exc:
            self._bcast_status_lbl.set_text(f"⚠ Erreur: {exc}")

    # ======================================================================
    # Tab 5 — ✋ Main levée
    # ======================================================================

    def _build_tab_hands_up(self):
        label = Gtk.Label(label="✋ Mains levées")

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        vbox.set_margin_top(6)
        vbox.set_margin_bottom(6)
        vbox.set_margin_start(6)
        vbox.set_margin_end(6)

        # TreeView  — Nom | Question | Statut | Heure
        self._hands_store = Gtk.ListStore(str, str, str, str, str)  # id(hidden), nom, question, statut, heure
        tv = Gtk.TreeView(model=self._hands_store)
        tv.set_grid_lines(Gtk.TreeViewGridLines.HORIZONTAL)

        for title, col_idx, width in [
            ("Nom", 1, 150),
            ("Question", 2, 310),
            ("Statut", 3, 110),
            ("Heure", 4, 80),
        ]:
            renderer = Gtk.CellRendererText()
            renderer.set_property("wrap-mode", 2)   # WORD
            renderer.set_property("wrap-width", width - 10)
            col = Gtk.TreeViewColumn(title, renderer, text=col_idx)
            col.set_min_width(width)
            col.set_resizable(True)
            tv.append_column(col)

        self._hands_tv = tv
        sw = Gtk.ScrolledWindow()
        sw.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        sw.add(tv)
        vbox.pack_start(sw, True, True, 0)

        # Reply area
        reply_frame = Gtk.Frame(label=" Répondre à l'élève sélectionné ")
        reply_inner = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
        reply_inner.set_margin_top(4)
        reply_inner.set_margin_bottom(4)
        reply_inner.set_margin_start(6)
        reply_inner.set_margin_end(6)
        reply_frame.add(reply_inner)

        self._reply_entry = Gtk.Entry()
        self._reply_entry.set_placeholder_text("Votre réponse / indice…")
        btn_reply = Gtk.Button(label="💬 Répondre")
        btn_reply.connect("clicked", self._on_hand_reply)
        btn_teleport = Gtk.Button(label="🎯 Téléporter")
        btn_teleport.set_tooltip_text("Charge les paramètres du lab de l'élève sélectionné")
        btn_teleport.connect("clicked", self._on_hand_teleport)

        reply_inner.pack_start(self._reply_entry, True, True, 0)
        reply_inner.pack_start(btn_reply, False, False, 0)
        reply_inner.pack_start(btn_teleport, False, False, 0)

        vbox.pack_start(reply_frame, False, False, 0)

        self._hands_status_lbl = Gtk.Label(label="")
        self._hands_status_lbl.set_xalign(0)
        vbox.pack_start(self._hands_status_lbl, False, False, 2)

        self.notebook.append_page(vbox, label)

        # Auto-refresh every 3 s — separate timer
        self._hands_timer_id = GLib.timeout_add(3000, self._auto_refresh_hands)

    def _refresh_hands(self):
        try:
            state = _safe_call(self.hub.get_state, default={}) or {}
            queue = state.get("hands_up_queue", [])
            self._hands_store.clear()
            for hand in queue:
                self._hands_store.append([
                    hand.get("id", ""),
                    hand.get("student_name", "—"),
                    hand.get("question", ""),
                    hand.get("status", "open"),
                    hand.get("timestamp", ""),
                ])
            open_count = sum(1 for h in queue if h.get("status") == "open")
            self._hands_status_lbl.set_text(
                f"{open_count} main(s) levée(s) ouverte(s) · MAJ {_ts()}"
            )
        except Exception:
            self._hands_status_lbl.set_text("⚠ Erreur chargement mains levées")
        return False

    def _auto_refresh_hands(self):
        self._refresh_hands()
        return True  # reschedule

    def _get_selected_hand_id(self):
        """Return the hidden hand_id of the selected TreeView row, or None."""
        selection = self._hands_tv.get_selection()
        model, itr = selection.get_selected()
        if itr is None:
            return None
        return model.get_value(itr, 0)  # col 0 = id

    def _on_hand_reply(self, _btn):
        hand_id = self._get_selected_hand_id()
        if not hand_id:
            self._hands_status_lbl.set_text("⚠ Sélectionnez un élève d'abord.")
            return
        reply = self._reply_entry.get_text().strip()
        if not reply:
            self._hands_status_lbl.set_text("⚠ La réponse ne peut pas être vide.")
            return
        try:
            self.hub.reply_to_hand(hand_id=hand_id, teacher_reply=reply)
            self._reply_entry.set_text("")
            self._refresh_hands()
        except Exception as exc:
            self._hands_status_lbl.set_text(f"⚠ Erreur: {exc}")

    def _on_hand_teleport(self, _btn):
        hand_id = self._get_selected_hand_id()
        if not hand_id:
            self._hands_status_lbl.set_text("⚠ Sélectionnez un élève d'abord.")
            return
        try:
            data = _safe_call(self.hub.teleport_to_student, hand_id, default=None)
            if data:
                lab  = data.get("lab_id", "?")
                lvl  = data.get("level", "?")
                name = data.get("student_name", "?")
                self._hands_status_lbl.set_text(
                    f"🎯 Téléportation → {name} · Lab: {lab} · Niveau: {lvl}"
                )
            else:
                self._hands_status_lbl.set_text("⚠ Données introuvables pour cet élève.")
        except Exception as exc:
            self._hands_status_lbl.set_text(f"⚠ Erreur: {exc}")

    # ======================================================================
    # Tab 6 — ⏱️ Devoirs & Fiches d'exercices
    # ======================================================================

    def _build_tab_exam(self):
        label = Gtk.Label(label="⏱️ Devoirs & Fiches")

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        vbox.set_margin_top(8)
        vbox.set_margin_bottom(8)
        vbox.set_margin_start(8)
        vbox.set_margin_end(8)

        # 1. Section Examen / Devoir minuté
        exam_frame = Gtk.Frame(label=" ⏱️ Session de Devoir / Évaluation Minutée ")
        exam_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        exam_box.set_margin_top(6)
        exam_box.set_margin_bottom(6)
        exam_box.set_margin_start(8)
        exam_box.set_margin_end(8)

        # Titre et Durée
        row1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        lbl_title = Gtk.Label(label="Titre :")
        row1.pack_start(lbl_title, False, False, 0)
        self._exam_title_entry = Gtk.Entry()
        self._exam_title_entry.set_text("Défi Réseau de Neurones & Fusée Lunaire")
        row1.pack_start(self._exam_title_entry, True, True, 0)

        lbl_dur = Gtk.Label(label="Durée (min) :")
        row1.pack_start(lbl_dur, False, False, 0)
        self._exam_dur_spin = Gtk.SpinButton.new_with_range(5.0, 120.0, 5.0)
        self._exam_dur_spin.set_value(30.0)
        row1.pack_start(self._exam_dur_spin, False, False, 0)
        exam_box.pack_start(row1, False, False, 0)

        # Consignes
        self._exam_instr_entry = Gtk.Entry()
        self._exam_instr_entry.set_placeholder_text("Consignes pour l'évaluation (ex: Réglez la gravité et atteignez +200 pts)...")
        self._exam_instr_entry.set_text("Réglez les curseurs d'apprentissage et faites atterrir doucement votre fusée 3 fois consécutives.")
        exam_box.pack_start(self._exam_instr_entry, False, False, 0)

        # Boutons d'action
        btn_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        btn_start_exam = Gtk.Button(label="▶ Lancer l'Évaluation")
        btn_start_exam.set_tooltip_text("Démarre le compte à rebours sur tous les postes élèves du réseau local")
        btn_start_exam.connect("clicked", lambda _b: self._on_start_exam())
        btn_row.pack_start(btn_start_exam, True, True, 0)

        btn_end_exam = Gtk.Button(label="⏹ Clôturer & Collecter")
        btn_end_exam.set_tooltip_text("Arrête l'examen et collecte tous les travaux des élèves")
        btn_end_exam.connect("clicked", lambda _b: self._on_end_exam())
        btn_row.pack_start(btn_end_exam, True, True, 0)
        exam_box.pack_start(btn_row, False, False, 0)

        self._exam_status_lbl = Gtk.Label(label="Aucune évaluation active actuellement.")
        self._exam_status_lbl.set_xalign(0.0)
        exam_box.pack_start(self._exam_status_lbl, False, False, 2)
        exam_frame.add(exam_box)
        vbox.pack_start(exam_frame, False, False, 0)

        # 2. Section Fiche d'exercice imprimable
        print_frame = Gtk.Frame(label=" 🖨️ Générateur de Fiche d'Exercice Imprimable ")
        print_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        print_box.set_margin_top(6)
        print_box.set_margin_bottom(6)
        print_box.set_margin_start(8)
        print_box.set_margin_end(8)

        p_row1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        lbl_p_title = Gtk.Label(label="Titre fiche :")
        p_row1.pack_start(lbl_p_title, False, False, 0)
        self._sheet_title_entry = Gtk.Entry()
        self._sheet_title_entry.set_text("TP Physique, Chimie & Apprentissage IA")
        p_row1.pack_start(self._sheet_title_entry, True, True, 0)

        self._sheet_subj_combo = Gtk.ComboBoxText()
        for sid, slbl in [
            ("ai_labs", "🤖 AI Labs (Fusée & Neurones)"),
            ("atom_physics", "⚛️ Lab 8: Atomes & Molécules"),
            ("math", "📐 Math Quest"),
            ("language", "🔤 Word Voyage"),
            ("geography", "🌍 Geo Explorer"),
            ("history", "⏳ Time Traveler"),
            ("science", "🔬 Science Explorer"),
        ]:
            self._sheet_subj_combo.append(sid, slbl)
        self._sheet_subj_combo.set_active(0)
        p_row1.pack_start(self._sheet_subj_combo, False, False, 0)

        btn_gen_sheet = Gtk.Button(label="📄 Exporter Fiche Prête à Imprimer")
        btn_gen_sheet.set_tooltip_text("Génère un document HTML propre, aéré et directement imprimable")
        btn_gen_sheet.connect("clicked", lambda _b: self._on_export_worksheet())
        p_row1.pack_start(btn_gen_sheet, False, False, 0)
        print_box.pack_start(p_row1, False, False, 0)

        self._sheet_status_lbl = Gtk.Label(label="")
        self._sheet_status_lbl.set_xalign(0.0)
        print_box.pack_start(self._sheet_status_lbl, False, False, 2)
        print_frame.add(print_box)
        vbox.pack_start(print_frame, False, False, 0)

        self.notebook.append_page(vbox, label)

    def _on_start_exam(self):
        title = self._exam_title_entry.get_text().strip() or "Évaluation"
        dur = int(self._exam_dur_spin.get_value())
        instr = self._exam_instr_entry.get_text().strip()
        data = _safe_call(self.hub.start_exam, title=title, duration_minutes=dur, instructions=instr)
        if data:
            self._exam_status_lbl.set_markup(
                f"<b><span foreground='#22c55e'>✓ Évaluation en cours ({dur} min)</span></b> · "
                f"Titre: {title} · Début: {data.get('created_at', '')}"
            )
        else:
            self._exam_status_lbl.set_text("Erreur lors du lancement de l'évaluation.")

    def _on_end_exam(self):
        _safe_call(self.hub.end_exam)
        st = _safe_call(self.hub.get_exam_status, default={})
        count = st.get("collected_count", 0)
        self._exam_status_lbl.set_markup(
            f"<b><span foreground='#f59e0b'>⏹ Évaluation clôturée</span></b> · "
            f"Devoirs collectés : <b>{count} élève(s)</b>."
        )

    def _refresh_exam_status(self):
        st = _safe_call(self.hub.get_exam_status, default={})
        if st and st.get("active", False):
            rem_min = st.get("remaining_min", 0.0)
            collected = st.get("collected_count", 0)
            self._exam_status_lbl.set_markup(
                f"<b><span foreground='#22c55e'>⏱ En cours ({rem_min:.1f} min restantes)</span></b> · "
                f"Devoirs reçus : <b>{collected}</b>"
            )

    def _on_export_worksheet(self):
        title = self._sheet_title_entry.get_text().strip() or "Fiche d'Exercice"
        subj = self._sheet_subj_combo.get_active_id() if hasattr(self, "_sheet_subj_combo") else "ai_labs"
        if subj == "ai_labs" or not subj:
            questions = [
                "Expliquez le rôle de la gravité lunaire (-1.62 m/s²) par rapport à la poussée du réacteur.",
                "Quel curseur de mutation génétique permet d'éviter que le véhicule ne tourne en rond ?",
                "Décrivez en 2 phrases comment le réseau de neurones ajuste ses poids après chaque tentative.",
                "Proposez une fonction de récompense mathématique favorisant une consommation minimale de carburant.",
            ]
            lab_lbl = "Physique & IA"
        else:
            questions = _safe_call(
                self.hub.generate_subject_worksheet_questions,
                subject=subj,
                count=5,
                lang="fr",
                default=[],
            )
            lab_lbl = subj
        html_content = _safe_call(
            self.hub.export_printable_worksheet,
            title=title,
            lab_id=lab_lbl,
            questions=questions,
            instructions="Répondez aux questions ci-dessous avec soin après avoir testé vos hypothèses dans le simulateur.",
            default="",
        )
        if not html_content:
            self._sheet_status_lbl.set_text("⚠ Impossible de générer la fiche.")
            return
        out_path = _resolve_tmp_path("fiche_exercice_synapse.html")
        try:
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(html_content)
            self._sheet_status_lbl.set_markup(
                f"<b><span foreground='#22c55e'>✓ Fiche prête :</span></b> {out_path} (ouvrable dans tout navigateur)"
            )
        except Exception as exc:
            self._sheet_status_lbl.set_text(f"⚠ Erreur fichier: {exc}")

    # ======================================================================
    # Global auto-refresh (every 5 s)
    # ======================================================================

    def _auto_refresh(self):
        self._refresh_roster()
        self._refresh_schedule()
        self._refresh_exam_status()
        return True  # keep the timer alive

    # ======================================================================
    # Public API
    # ======================================================================

    def show(self):
        """Run the dialog modally, then clean up timers and destroy."""
        if not GTK_AVAILABLE or not getattr(self, "dialog", None):
            return
        # Cancel timers
        if self._refresh_timer_id is not None:
            try:
                GLib.source_remove(self._refresh_timer_id)
            except Exception:
                pass
        if hasattr(self, "_hands_timer_id") and self._hands_timer_id is not None:
            try:
                GLib.source_remove(self._hands_timer_id)
            except Exception:
                pass
        self.dialog.destroy()


# ---------------------------------------------------------------------------
# Utility helpers
# ---------------------------------------------------------------------------

def _esc(text: str) -> str:
    """HTML-escape a string."""
    return (
        text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
    )


def _resolve_tmp_path(filename: str) -> str:
    """Return /tmp/<filename> on POSIX or %TEMP%/<filename> on Windows."""
    tmp_dir = os.environ.get("TEMP") or os.environ.get("TMP") or "/tmp"
    return os.path.join(tmp_dir, filename)
