from kivy.config import Config
Config.set("graphics", "width", "360")
Config.set("graphics", "height", "700")

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.image import Image
from kivy.metrics import dp
from kivy.properties import StringProperty
from kivy.utils import platform
from pathlib import Path
from datetime import datetime
import shutil

from database import Database

UNGU = (0.58, 0.38, 0.82, 1)


def folder_foto():
    """Folder awal file chooser: galeri di Android, Pictures asli di Windows."""
    if platform == "android":
        kandidat = ["/storage/emulated/0/Pictures", "/storage/emulated/0/DCIM"]
    elif platform == "win":
        import ctypes
        buf = ctypes.create_unicode_buffer(260)
        ctypes.windll.shell32.SHGetFolderPathW(None, 0x27, None, 0, buf)  # 0x27 = My Pictures
        kandidat = [buf.value]
    else:
        kandidat = [str(Path.home() / "Pictures")]
    return next((p for p in kandidat if p and Path(p).exists()), str(Path.home()))


def pilih_foto(judul, tujuan, callback):
    """Popup pilih foto. Foto disalin ke folder `tujuan`, lalu callback(path)."""
    app = App.get_running_app()
    chooser = FileChooserListView(
        path=folder_foto(), filters=["*.png", "*.jpg", "*.jpeg", "*.webp"]
    )
    pilih = Button(text="PILIH", background_normal="", background_color=UNGU, bold=True)
    batal = Button(text="BATAL")
    tombol = BoxLayout(size_hint_y=None, height=dp(50))
    tombol.add_widget(pilih)
    tombol.add_widget(batal)
    isi = BoxLayout(orientation="vertical")
    isi.add_widget(chooser)
    isi.add_widget(tombol)
    popup = Popup(title=judul, content=isi, size_hint=(0.95, 0.85))

    def simpan(*_):
        if not chooser.selection:
            return
        sumber = Path(chooser.selection[0])
        folder = Path(app.user_data_dir) / tujuan
        folder.mkdir(parents=True, exist_ok=True)
        hasil = folder / sumber.name
        try:
            shutil.copy2(sumber, hasil)
            callback(str(hasil))
            popup.dismiss()
        except Exception:
            app.show_popup("Error", "Foto tidak dapat digunakan.")

    pilih.bind(on_release=simpan)
    batal.bind(on_release=popup.dismiss)
    popup.open()


def cek_angka(teks, nama):
    """Ubah teks jadi angka > 0. Jika tidak valid, tampilkan popup dan return None."""
    try:
        angka = int(teks.replace(".", ""))
        if angka > 0:
            return angka
        pesan = f"{nama} harus lebih dari 0."
    except ValueError:
        pesan = f"{nama} harus berupa angka."
    App.get_running_app().show_popup("Peringatan", pesan)


def lbl(text, color, size, h, **kw):
    return Label(text=text, color=color, font_size=size,
                 size_hint_y=None, height=dp(h), **kw)


class LoginScreen(Screen):

    def login(self):
        app = App.get_running_app()
        user, pw = self.ids.username.text.strip(), self.ids.password.text
        if not user or not pw:
            return app.show_popup("Peringatan", "Username dan password harus diisi.")
        data = app.db.login(user, pw)
        if not data:
            return app.show_popup("Login Gagal", "Username atau password salah.")
        app.current_user = dict(data)
        self.ids.username.text = self.ids.password.text = ""
        app.root.current = "dashboard"

    def register(self):
        App.get_running_app().root.current = "register"


class RegisterScreen(Screen):

    def register_account(self):
        app = App.get_running_app()
        user, pw = self.ids.username.text.strip(), self.ids.password.text
        if not user or not pw:
            return app.show_popup("Peringatan", "Username dan password harus diisi.")
        if pw != self.ids.confirm.text:
            return app.show_popup("Peringatan", "Konfirmasi password tidak sama.")
        if not app.db.register(user, pw):
            return app.show_popup("Gagal", "Username sudah digunakan.")
        self.ids.username.text = self.ids.password.text = self.ids.confirm.text = ""
        app.show_popup("Berhasil", "Account berhasil dibuat.")
        app.root.current = "login"


class DashboardScreen(Screen):

    mode = StringProperty("ongoing")

    def on_pre_enter(self):
        self.refresh()

    def show_ongoing(self):
        self.mode = "ongoing"
        self.refresh()

    def show_completed(self):
        self.mode = "completed"
        self.refresh()

    def refresh(self):
        app = App.get_running_app()
        box = self.ids.goal_box
        box.clear_widgets()
        if not app.current_user:
            return
        for goal in app.db.get_goals(app.current_user["id"]):
            total = app.db.get_goal_total(goal["id"])
            selesai = total >= goal["target"]
            if selesai == (self.mode == "completed"):
                self.create_card(goal, total)
        if not box.children:
            teks = "tercapai" if self.mode == "completed" else "berlangsung"
            box.add_widget(lbl(f"Belum ada celengan {teks}.",
                               (0.45, 0.35, 0.55, 1), "14sp", 55))

    def create_card(self, goal, total):
        app = App.get_running_app()
        target = goal["target"]
        persen = min(int(total / target * 100), 100) if target > 0 else 0
        gelap, ungu, abu = (0.25, 0.18, 0.35, 1), (0.45, 0.27, 0.65, 1), (0.40, 0.33, 0.48, 1)

        card = BoxLayout(orientation="vertical", padding=dp(14), spacing=dp(7),
                         size_hint_y=None, height=dp(430))
        card.add_widget(lbl(goal["name"], gelap, "21sp", 35, bold=True))

        if goal["image"] and Path(goal["image"]).exists():
            kotak = BoxLayout(size_hint_y=None, height=dp(190), padding=dp(15))
            kotak.add_widget(Image(source=goal["image"], allow_stretch=True, keep_ratio=True))
            card.add_widget(kotak)
        else:
            card.add_widget(lbl("Belum ada gambar", (0.5, 0.4, 0.6, 1), "15sp", 190))

        status = ("Target sudah tercapai" if total >= target
                  else "Sisa: " + app.rupiah(target - total))
        card.add_widget(lbl(app.rupiah(total), ungu, "24sp", 35, bold=True))
        card.add_widget(lbl("Target: " + app.rupiah(target), abu, "14sp", 25))
        card.add_widget(lbl(f"{persen}% tercapai", ungu, "14sp", 25, bold=True))
        card.add_widget(lbl(status, abu, "14sp", 25, bold=True))

        tombol = Button(text="Lihat Celengan", background_normal="", background_color=UNGU,
                        bold=True, size_hint_y=None, height=dp(45))
        tombol.bind(on_release=lambda x: app.open_goal(goal["id"]))
        card.add_widget(tombol)
        self.ids.goal_box.add_widget(card)


class AddGoalScreen(Screen):

    selected_image = StringProperty("")

    def choose_image(self):
        def hasil(path):
            self.selected_image = path
            self.ids.image_label.text = Path(path).name
        pilih_foto("Pilih Foto", "images", hasil)

    def save_goal(self):
        app = App.get_running_app()
        nama, teks = self.ids.name.text.strip(), self.ids.target.text.strip()
        if not nama or not teks:
            return app.show_popup("Peringatan", "Nama dan target harus diisi.")
        target = cek_angka(teks, "Target")
        if not target:
            return
        app.db.add_goal(app.current_user["id"], nama, target, self.selected_image)
        self.ids.name.text = self.ids.target.text = ""
        self.ids.image_label.text = "Belum ada gambar"
        self.selected_image = ""
        app.root.current = "dashboard"


class GoalScreen(Screen):

    goal_id = None

    def on_pre_enter(self):
        self.refresh()

    def refresh(self):
        app, ids = App.get_running_app(), self.ids
        goal = app.db.get_goal(self.goal_id) if self.goal_id else None
        if not goal:
            return
        total, target = app.db.get_goal_total(self.goal_id), goal["target"]
        persen = min(total / target * 100, 100) if target else 0

        ids.goal_name.text = goal["name"]
        ids.goal_total.text = app.rupiah(total)
        ids.goal_target.text = "Target: " + app.rupiah(target)
        ids.goal_percent.text = f"{persen:.0f}% tercapai"
        ids.goal_remaining.text = ("Target sudah tercapai" if total >= target
                                   else "Sisa: " + app.rupiah(target - total))
        ada = goal["image"] and Path(goal["image"]).exists()
        ids.goal_image.source = goal["image"] if ada else ""

        ids.history_box.clear_widgets()
        for r in app.db.get_goal_savings(self.goal_id):
            teks = f'{r["tanggal"]}  {r["keterangan"]}  +{app.rupiah(r["jumlah"])}'
            ids.history_box.add_widget(lbl(teks, (0.30, 0.25, 0.38, 1), "12sp", 30))

    def add_saving(self):
        app = App.get_running_app()
        teks, note = self.ids.amount.text.strip(), self.ids.note.text.strip()
        if not teks:
            return app.show_popup("Peringatan", "Nominal harus diisi.")
        jumlah = cek_angka(teks, "Nominal")
        if not jumlah:
            return

        goal = app.db.get_goal(self.goal_id)
        sebelum = app.db.get_goal_total(self.goal_id)
        app.db.add_saving(self.goal_id, jumlah, note or "Setoran",
                          datetime.now().strftime("%Y-%m-%d %H:%M"))
        sesudah = app.db.get_goal_total(self.goal_id)

        self.ids.amount.text = self.ids.note.text = ""
        self.refresh()
        if sebelum < goal["target"] <= sesudah:
            app.show_popup("Target Tercapai!",
                           f"Selamat! Target celengan {goal['name']} sudah tercapai.")

    def delete_goal(self):
        app = App.get_running_app()
        app.db.delete_goal(self.goal_id)
        app.root.current = "dashboard"


class SettingsScreen(Screen):

    def on_pre_enter(self):
        self.refresh()

    def refresh(self):
        user = App.get_running_app().current_user
        if not user:
            return
        self.ids.account_name.text = user["username"]
        foto = user.get("profile_photo", "")
        self.ids.profile_image.source = foto if foto and Path(foto).exists() else ""

    def choose_profile(self):
        app = App.get_running_app()

        def hasil(path):
            app.db.update_profile_photo(app.current_user["id"], path)
            app.current_user["profile_photo"] = path
            self.ids.profile_image.source = path
        pilih_foto("Pilih Foto Profil", "profile", hasil)

    def logout(self):
        app = App.get_running_app()
        app.current_user = None
        app.root.current = "login"


class TabungYukApp(App):

    current_user = None

    def build(self):
        self.title = "TabungYuk"
        self.db = Database()
        Builder.load_file(str(Path(__file__).parent / "tabungan.kv"))
        manager = ScreenManager()
        for nama, layar in [("login", LoginScreen), ("register", RegisterScreen),
                            ("dashboard", DashboardScreen), ("add_goal", AddGoalScreen),
                            ("goal", GoalScreen), ("settings", SettingsScreen)]:
            manager.add_widget(layar(name=nama))
        return manager

    def rupiah(self, angka):
        return "Rp" + f"{int(angka):,}".replace(",", ".")

    def open_goal(self, goal_id):
        self.root.get_screen("goal").goal_id = goal_id
        self.root.current = "goal"

    def show_popup(self, title, message):
        ok = Button(text="OK", background_normal="", background_color=UNGU,
                    bold=True, size_hint_y=None, height=dp(45))
        box = BoxLayout(orientation="vertical", padding=dp(15), spacing=dp(10))
        box.add_widget(Label(text=message, color=(0.25, 0.20, 0.32, 1), halign="center"))
        box.add_widget(ok)
        popup = Popup(title=title, content=box, size_hint=(0.85, None), height=dp(210))
        ok.bind(on_release=popup.dismiss)
        popup.open()

    def on_stop(self):
        if hasattr(self, "db"):
            self.db.close()


if __name__ == "__main__":
    TabungYukApp().run()