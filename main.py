from kivy.app import App
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle
from kivy.properties import NumericProperty


# =========================================================
# WINDOW
# =========================================================

Window.size = (390, 760)
Window.minimum_width = 350
Window.minimum_height = 600
Window.clearcolor = (0.98, 0.97, 0.90, 1)


# =========================================================
# COLORS
# =========================================================

GREEN = (0.08, 0.48, 0.20, 1)
DARK_GREEN = (0.04, 0.32, 0.12, 1)
YELLOW = (1, 0.88, 0.35, 1)
CREAM = (1, 0.97, 0.72, 1)
LIGHT = (0.97, 0.96, 0.90, 1)
WHITE = (1, 1, 1, 1)
BLACK = (0.08, 0.08, 0.08, 1)
GRAY = (0.45, 0.45, 0.45, 1)
RED = (0.72, 0.12, 0.08, 1)


# =========================================================
# DATA PRODUK
# =========================================================

PRODUCTS = [
    {
        "name": "Classic Beef",
        "price": 28000,
        "description": "Burger daging sapi juicy dengan selada, tomat, keju dan saus spesial.",
        "category": "Burger",
    },
    {
        "name": "Black Burger",
        "price": 30000,
        "description": "Burger roti hitam dengan daging sapi, keju dan saus spesial Click Burger.",
        "category": "Burger",
    },
    {
        "name": "French Fries",
        "price": 15000,
        "description": "Kentang goreng renyah dan gurih.",
        "category": "Snack",
    },
    {
        "name": "Chicken Sandwich",
        "price": 25000,
        "description": "Sandwich ayam dengan sayuran segar dan saus.",
        "category": "Snack",
    },
    {
        "name": "Ice Tea",
        "price": 8000,
        "description": "Es teh manis yang menyegarkan.",
        "category": "Drink",
    },
]


# =========================================================
# HELPER
# =========================================================

def rupiah(number):
    return "Rp {:,}".format(int(number)).replace(",", ".")


def rounded_background(widget, color, radius=18):
    with widget.canvas.before:
        Color(*color)
        widget._background = RoundedRectangle(
            pos=widget.pos,
            size=widget.size,
            radius=[dp(radius)]
        )

    def update(*args):
        widget._background.pos = widget.pos
        widget._background.size = widget.size

    widget.bind(pos=update, size=update)


def make_label(
    text="",
    size=16,
    color=BLACK,
    bold=False,
    halign="left",
    valign="middle"
):
    label = Label(
        text=text,
        font_size=dp(size),
        color=color,
        bold=bold,
        halign=halign,
        valign=valign,
    )
    label.bind(size=lambda instance, value: setattr(
        instance, "text_size", value
    ))
    return label


def make_button(
    text,
    bg=GREEN,
    color=WHITE,
    height=48,
    font_size=14
):
    button = Button(
        text=text,
        size_hint_y=None,
        height=dp(height),
        background_normal="",
        background_down="",
        background_color=bg,
        color=color,
        font_size=dp(font_size),
        bold=True,
    )

    rounded_background(button, bg, 12)

    return button


def make_card(color=WHITE, padding=12):
    card = BoxLayout(
        orientation="vertical",
        padding=dp(padding),
        spacing=dp(8),
        size_hint_y=None,
    )

    rounded_background(card, color, 16)

    return card


# =========================================================
# BASE SCREEN
# =========================================================

class BaseScreen(Screen):

    def go(self, name, direction="left"):
        """
        Navigasi aman.
        Tidak menggunakan manager.go().
        """
        self.manager.transition = SlideTransition(
            direction=direction,
            duration=0.20
        )
        self.manager.current = name

    def header(self, title, back=False):
        header = BoxLayout(
            size_hint_y=None,
            height=dp(58),
            spacing=dp(8)
        )

        if back:
            back_button = Button(
                text="<",
                size_hint_x=None,
                width=dp(50),
                background_normal="",
                background_color=GREEN,
                color=WHITE,
                font_size=dp(24),
                bold=True
            )

            rounded_background(back_button, GREEN, 12)
            back_button.bind(
                on_release=lambda instance: self.go(
                    "home",
                    "right"
                )
            )

            header.add_widget(back_button)

        title_label = make_label(
            title,
            size=20,
            color=DARK_GREEN,
            bold=True,
            halign="left"
        )

        header.add_widget(title_label)

        return header

    def bottom_nav(self):
        nav = BoxLayout(
            size_hint_y=None,
            height=dp(68),
            spacing=dp(6),
            padding=[dp(5), dp(5)]
        )

        home = make_button(
            "HOME",
            bg=LIGHT,
            color=DARK_GREEN,
            height=58,
            font_size=12
        )

        cart = make_button(
            "KERANJANG",
            bg=LIGHT,
            color=DARK_GREEN,
            height=58,
            font_size=12
        )

        profile = make_button(
            "PROFIL",
            bg=LIGHT,
            color=DARK_GREEN,
            height=58,
            font_size=12
        )

        home.bind(
            on_release=lambda instance: self.go(
                "home",
                "right"
            )
        )

        cart.bind(
            on_release=lambda instance: self.go(
                "cart",
                "left"
            )
        )

        profile.bind(
            on_release=lambda instance: self.go(
                "profile",
                "left"
            )
        )

        nav.add_widget(home)
        nav.add_widget(cart)
        nav.add_widget(profile)

        return nav


# =========================================================
# LOGIN
# =========================================================

class LoginScreen(BaseScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build()

    def build(self):

        root = BoxLayout(
            orientation="vertical",
            padding=dp(30),
            spacing=dp(12)
        )

        spacer = Widget(
            size_hint_y=0.15
        )

        root.add_widget(spacer)

        logo = make_label(
            "🍔",
            size=55,
            color=GREEN,
            bold=True,
            halign="center"
        )
        root.add_widget(logo)

        title = make_label(
            "CLICK\nBURGER",
            size=28,
            color=GREEN,
            bold=True,
            halign="center"
        )
        root.add_widget(title)

        subtitle = make_label(
            "Login untuk memesan burger favoritmu",
            size=13,
            color=GRAY,
            halign="center"
        )
        root.add_widget(subtitle)

        root.add_widget(Widget(size_hint_y=None, height=dp(15)))

        self.email = TextInput(
            hint_text="Email / No. HP",
            multiline=False,
            size_hint_y=None,
            height=dp(48),
            padding=[dp(14), dp(12)]
        )
        rounded_background(self.email, WHITE, 12)
        root.add_widget(self.email)

        self.password = TextInput(
            hint_text="Password",
            password=True,
            multiline=False,
            size_hint_y=None,
            height=dp(48),
            padding=[dp(14), dp(12)]
        )
        rounded_background(self.password, WHITE, 12)
        root.add_widget(self.password)

        login = make_button(
            "MASUK",
            bg=YELLOW,
            color=DARK_GREEN,
            height=48,
            font_size=14
        )

        login.bind(
            on_release=lambda instance: self.login()
        )

        root.add_widget(login)

        google = make_button(
            "Masuk dengan Google",
            bg=WHITE,
            color=BLACK,
            height=48,
            font_size=13
        )

        google.bind(
            on_release=lambda instance: self.login()
        )

        root.add_widget(google)

        register = make_label(
            "Belum punya akun? Daftar di sini",
            size=12,
            color=GRAY,
            halign="center"
        )
        root.add_widget(register)

        root.add_widget(
            Widget(size_hint_y=0.3)
        )

        self.add_widget(root)

    def login(self):
        self.go("home", "left")


# =========================================================
# HOME
# =========================================================

class HomeScreen(BaseScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_category = "Burger"
        self.build()

    def build(self):

        root = BoxLayout(
            orientation="vertical",
            spacing=dp(8),
            padding=[dp(10), dp(8)]
        )

        title = make_label(
            "Mau burger\napa hari ini?",
            size=22,
            color=BLACK,
            bold=True
        )
        title.size_hint_y = None
        title.height = dp(65)
        root.add_widget(title)

        search = TextInput(
            hint_text="Cari burger favoritmu...",
            multiline=False,
            size_hint_y=None,
            height=dp(44),
            padding=[dp(12), dp(10)]
        )
        rounded_background(search, WHITE, 10)
        root.add_widget(search)

        promo = BoxLayout(
            size_hint_y=None,
            height=dp(90),
            padding=dp(15)
        )
        rounded_background(promo, CREAM, 18)

        promo_text = make_label(
            "DISKON SPESIAL\nUP TO 20%\nNikmati sekarang!",
            size=15,
            color=DARK_GREEN,
            bold=True
        )

        promo.add_widget(promo_text)
        promo.add_widget(
            make_label(
                "🍔",
                size=45,
                color=GREEN,
                halign="center"
            )
        )

        root.add_widget(promo)

        categories = BoxLayout(
            size_hint_y=None,
            height=dp(48),
            spacing=dp(5)
        )

        for category in ["Burger", "Snack", "Drink"]:
            button = make_button(
                category,
                bg=YELLOW,
                color=DARK_GREEN,
                height=48,
                font_size=12
            )

            button.bind(
                on_release=lambda instance,
                c=category: self.show_category(c)
            )

            categories.add_widget(button)

        root.add_widget(categories)

        self.product_area = GridLayout(
            cols=1,
            spacing=dp(8),
            padding=[0, dp(3)]
        )

        scroll = ScrollView()
        scroll.add_widget(self.product_area)

        root.add_widget(scroll)

        root.add_widget(self.bottom_nav())

        self.add_widget(root)

        self.show_category("Burger")

    def show_category(self, category):

        self.selected_category = category
        self.product_area.clear_widgets()

        products = [
            product for product in PRODUCTS
            if product["category"] == category
        ]

        for product in products:
            card = make_card(
                color=CREAM,
                padding=10
            )

            card.height = dp(88)

            row = BoxLayout(
                spacing=dp(10)
            )

            image = make_label(
                "🍔" if category == "Burger"
                else "🍟" if category == "Snack"
                else "🥤",
                size=35,
                color=GREEN,
                halign="center"
            )
            image.size_hint_x = 0.20

            info = BoxLayout(
                orientation="vertical",
                spacing=dp(2)
            )

            info.add_widget(
                make_label(
                    product["name"],
                    size=15,
                    color=DARK_GREEN,
                    bold=True
                )
            )

            info.add_widget(
                make_label(
                    rupiah(product["price"]),
                    size=13,
                    color=GREEN,
                    bold=True
                )
            )

            row.add_widget(image)
            row.add_widget(info)

            detail = make_button(
                "DETAIL",
                bg=GREEN,
                color=WHITE,
                height=40,
                font_size=11
            )
            detail.size_hint_x = 0.24

            detail.bind(
                on_release=lambda instance,
                p=product: self.open_detail(p)
            )

            row.add_widget(detail)

            card.add_widget(row)
            self.product_area.add_widget(card)

    def open_detail(self, product):

        detail = self.manager.get_screen("detail")
        detail.set_product(product)

        self.go("detail", "left")


# =========================================================
# DETAIL
# =========================================================

class DetailScreen(BaseScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.product = PRODUCTS[0]
        self.quantity = 1
        self.build()

    def build(self):

        root = BoxLayout(
            orientation="vertical",
            padding=dp(10),
            spacing=dp(10)
        )

        root.add_widget(
            self.header("Detail Produk", back=True)
        )

        image = make_label(
            "🍔",
            size=90,
            color=GREEN,
            bold=True,
            halign="center"
        )
        image.size_hint_y = None
        image.height = dp(170)

        card_image = BoxLayout()
        rounded_background(card_image, CREAM, 20)
        card_image.add_widget(image)

        root.add_widget(card_image)

        self.name_label = make_label(
            "",
            size=23,
            color=DARK_GREEN,
            bold=True
        )
        self.name_label.size_hint_y = None
        self.name_label.height = dp(40)
        root.add_widget(self.name_label)

        self.price_label = make_label(
            "",
            size=17,
            color=GREEN,
            bold=True
        )
        self.price_label.size_hint_y = None
        self.price_label.height = dp(35)
        root.add_widget(self.price_label)

        self.description_label = make_label(
            "",
            size=13,
            color=GRAY
        )
        self.description_label.size_hint_y = None
        self.description_label.height = dp(75)
        root.add_widget(self.description_label)

        extras = make_card(
            color=WHITE,
            padding=10
        )
        extras.height = dp(110)

        extras.add_widget(
            make_label(
                "Pilihan Tambahan",
                size=14,
                color=DARK_GREEN,
                bold=True
            )
        )

        extras.add_widget(
            make_label(
                "Keju + Rp 3.000\nBacon + Rp 5.000\nTelur + Rp 4.000",
                size=12,
                color=GRAY
            )
        )

        root.add_widget(extras)

        quantity_row = BoxLayout(
            size_hint_y=None,
            height=dp(50),
            spacing=dp(8)
        )

        minus = make_button(
            "-",
            bg=LIGHT,
            color=DARK_GREEN,
            height=45,
            font_size=18
        )

        plus = make_button(
            "+",
            bg=GREEN,
            color=WHITE,
            height=45,
            font_size=18
        )

        self.quantity_label = make_label(
            "1",
            size=18,
            color=BLACK,
            bold=True,
            halign="center"
        )

        quantity_row.add_widget(minus)
        quantity_row.add_widget(self.quantity_label)
        quantity_row.add_widget(plus)

        minus.bind(
            on_release=lambda instance: self.change_quantity(-1)
        )

        plus.bind(
            on_release=lambda instance: self.change_quantity(1)
        )

        root.add_widget(quantity_row)

        add = make_button(
            "TAMBAH KE KERANJANG",
            bg=GREEN,
            color=WHITE,
            height=52,
            font_size=14
        )

        add.bind(
            on_release=lambda instance: self.add_to_cart()
        )

        root.add_widget(add)

        root.add_widget(
            self.bottom_nav()
        )

        self.add_widget(root)

    def set_product(self, product):

        self.product = product
        self.quantity = 1

        self.name_label.text = product["name"]
        self.price_label.text = rupiah(product["price"])
        self.description_label.text = product["description"]
        self.quantity_label.text = "1"

    def change_quantity(self, amount):

        self.quantity += amount

        if self.quantity < 1:
            self.quantity = 1

        self.quantity_label.text = str(self.quantity)

    def add_to_cart(self):

        app = App.get_running_app()

        name = self.product["name"]

        app.cart[name] = (
            app.cart.get(name, 0)
            + self.quantity
        )

        cart = self.manager.get_screen("cart")
        cart.refresh()

        self.go("cart", "left")


# =========================================================
# CART
# =========================================================

class CartScreen(BaseScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build()

    def build(self):

        root = BoxLayout(
            orientation="vertical",
            padding=dp(10),
            spacing=dp(8)
        )

        root.add_widget(
            self.header("Keranjang")
        )

        self.items_area = GridLayout(
            cols=1,
            spacing=dp(8),
            padding=[0, dp(3)]
        )

        scroll = ScrollView()
        scroll.add_widget(self.items_area)

        root.add_widget(scroll)

        self.total_label = make_label(
            "Total: Rp 0",
            size=17,
            color=DARK_GREEN,
            bold=True,
            halign="right"
        )

        self.total_label.size_hint_y = None
        self.total_label.height = dp(45)

        root.add_widget(self.total_label)

        checkout = make_button(
            "CHECKOUT",
            bg=GREEN,
            color=WHITE,
            height=50,
            font_size=14
        )

        checkout.bind(
            on_release=lambda instance: self.checkout()
        )

        root.add_widget(checkout)

        root.add_widget(
            self.bottom_nav()
        )

        self.add_widget(root)

        self.refresh()

    def refresh(self):

        self.items_area.clear_widgets()

        app = App.get_running_app()

        total = 0

        if not app.cart:

            empty = make_card(
                color=WHITE,
                padding=20
            )

            empty.height = dp(150)

            empty.add_widget(
                make_label(
                    "Keranjang masih kosong",
                    size=18,
                    color=GRAY,
                    bold=True,
                    halign="center"
                )
            )

            empty.add_widget(
                make_label(
                    "Yuk pilih burger favoritmu!",
                    size=13,
                    color=GRAY,
                    halign="center"
                )
            )

            self.items_area.add_widget(empty)

        else:

            for product in PRODUCTS:

                name = product["name"]

                if name not in app.cart:
                    continue

                quantity = app.cart[name]
                subtotal = product["price"] * quantity
                total += subtotal

                card = make_card(
                    color=WHITE,
                    padding=10
                )

                card.height = dp(82)

                row = BoxLayout(
                    spacing=dp(8)
                )

                info = BoxLayout(
                    orientation="vertical"
                )

                info.add_widget(
                    make_label(
                        name,
                        size=14,
                        color=DARK_GREEN,
                        bold=True
                    )
                )

                info.add_widget(
                    make_label(
                        f"{rupiah(product['price'])} x {quantity}",
                        size=12,
                        color=GRAY
                    )
                )

                row.add_widget(info)

                minus = make_button(
                    "-",
                    bg=LIGHT,
                    color=DARK_GREEN,
                    height=40,
                    font_size=16
                )
                minus.size_hint_x = 0.18

                plus = make_button(
                    "+",
                    bg=GREEN,
                    color=WHITE,
                    height=40,
                    font_size=16
                )
                plus.size_hint_x = 0.18

                minus.bind(
                    on_release=lambda instance,
                    n=name: self.change_item(n, -1)
                )

                plus.bind(
                    on_release=lambda instance,
                    n=name: self.change_item(n, 1)
                )

                row.add_widget(minus)
                row.add_widget(plus)

                card.add_widget(row)

                self.items_area.add_widget(card)

        self.total_label.text = f"Total: {rupiah(total)}"

    def change_item(self, name, amount):

        app = App.get_running_app()

        app.cart[name] = app.cart.get(name, 0) + amount

        if app.cart[name] <= 0:
            del app.cart[name]

        self.refresh()

    def checkout(self):

        app = App.get_running_app()

        if not app.cart:
            return

        checkout = self.manager.get_screen("checkout")
        checkout.refresh()

        self.go("checkout", "left")


# =========================================================
# CHECKOUT
# =========================================================

class CheckoutScreen(BaseScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build()

    def build(self):

        root = BoxLayout(
            orientation="vertical",
            padding=dp(10),
            spacing=dp(8)
        )

        root.add_widget(
            self.header("Checkout")
        )

        self.summary = make_card(
            color=WHITE,
            padding=12
        )

        self.summary.height = dp(260)

        root.add_widget(self.summary)

        address_title = make_label(
            "Alamat Pengiriman",
            size=14,
            color=DARK_GREEN,
            bold=True
        )
        address_title.size_hint_y = None
        address_title.height = dp(32)

        root.add_widget(address_title)

        self.address = TextInput(
            text="Jl. Contoh No. 10, Kediri",
            multiline=False,
            size_hint_y=None,
            height=dp(45),
            padding=[dp(12), dp(10)]
        )

        rounded_background(
            self.address,
            WHITE,
            10
        )

        root.add_widget(self.address)

        payment_info = make_label(
            "Pembayaran dilakukan pada halaman berikutnya.",
            size=12,
            color=GRAY
        )

        payment_info.size_hint_y = None
        payment_info.height = dp(35)

        root.add_widget(payment_info)

        continue_button = make_button(
            "LANJUT KE PEMBAYARAN",
            bg=GREEN,
            color=WHITE,
            height=50,
            font_size=14
        )

        continue_button.bind(
            on_release=lambda instance:
            self.go_to_payment()
        )

        root.add_widget(continue_button)

        self.add_widget(root)

    def refresh(self):

        self.summary.clear_widgets()

        app = App.get_running_app()

        total = 0

        self.summary.add_widget(
            make_label(
                "Ringkasan Pesanan",
                size=17,
                color=DARK_GREEN,
                bold=True
            )
        )

        for product in PRODUCTS:

            name = product["name"]

            if name not in app.cart:
                continue

            quantity = app.cart[name]
            subtotal = product["price"] * quantity
            total += subtotal

            self.summary.add_widget(
                make_label(
                    f"{name} x {quantity}   {rupiah(subtotal)}",
                    size=13,
                    color=BLACK
                )
            )

        self.summary.add_widget(
            Widget(size_hint_y=None, height=dp(8))
        )

        self.summary.add_widget(
            make_label(
                f"TOTAL: {rupiah(total)}",
                size=18,
                color=GREEN,
                bold=True
            )
        )

    def go_to_payment(self):

        payment = self.manager.get_screen("payment")
        payment.refresh()

        self.go("payment", "left")


# =========================================================
# PAYMENT
# =========================================================

class PaymentScreen(BaseScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_method = "QRIS"
        self.build()

    def build(self):

        root = BoxLayout(
            orientation="vertical",
            padding=dp(10),
            spacing=dp(10)
        )

        root.add_widget(
            self.header("Pembayaran")
        )

        self.total_label = make_label(
            "Total Pembayaran: Rp 0",
            size=19,
            color=DARK_GREEN,
            bold=True,
            halign="center"
        )

        self.total_label.size_hint_y = None
        self.total_label.height = dp(50)

        root.add_widget(self.total_label)

        root.add_widget(
            make_label(
                "Pilih metode pembayaran",
                size=15,
                color=BLACK,
                bold=True
            )
        )

        methods = BoxLayout(
            orientation="vertical",
            spacing=dp(8),
            size_hint_y=None,
            height=dp(180)
        )

        for method in [
            "QRIS",
            "TRANSFER BANK",
            "COD"
        ]:

            button = make_button(
                method,
                bg=WHITE,
                color=DARK_GREEN,
                height=52,
                font_size=13
            )

            button.bind(
                on_release=lambda instance,
                m=method: self.select_method(m)
            )

            methods.add_widget(button)

        root.add_widget(methods)

        self.method_label = make_label(
            "Metode dipilih: QRIS",
            size=14,
            color=GREEN,
            bold=True,
            halign="center"
        )

        self.method_label.size_hint_y = None
        self.method_label.height = dp(45)

        root.add_widget(self.method_label)

        payment_box = BoxLayout(
            orientation="vertical",
            padding=dp(15)
        )

        rounded_background(
            payment_box,
            CREAM,
            18
        )

        payment_box.add_widget(
            make_label(
                "CLICK BURGER",
                size=18,
                color=DARK_GREEN,
                bold=True,
                halign="center"
            )
        )

        payment_box.add_widget(
            make_label(
                "Pembayaran aman dan mudah",
                size=12,
                color=GRAY,
                halign="center"
            )
        )

        payment_box.add_widget(
            make_label(
                "SCAN QRIS / TRANSFER / BAYAR DI TEMPAT",
                size=12,
                color=GREEN,
                bold=True,
                halign="center"
            )
        )

        root.add_widget(payment_box)

        pay = make_button(
            "BAYAR SEKARANG",
            bg=GREEN,
            color=WHITE,
            height=52,
            font_size=15
        )

        pay.bind(
            on_release=lambda instance:
            self.process_payment()
        )

        root.add_widget(pay)

        self.add_widget(root)

    def select_method(self, method):

        self.selected_method = method

        self.method_label.text = (
            f"Metode dipilih: {method}"
        )

    def refresh(self):

        app = App.get_running_app()

        total = 0

        for product in PRODUCTS:

            name = product["name"]

            if name in app.cart:
                total += (
                    product["price"]
                    * app.cart[name]
                )

        self.total_label.text = (
            f"Total Pembayaran: {rupiah(total)}"
        )

    def process_payment(self):

        app = App.get_running_app()

        if not app.cart:
            self.go("home", "right")
            return

        app.last_payment = self.selected_method

        orders = self.manager.get_screen("orders")
        orders.create_order()

        self.go("orders", "left")


# =========================================================
# ORDERS
# =========================================================

class OrdersScreen(BaseScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build()

    def build(self):

        root = BoxLayout(
            orientation="vertical",
            padding=dp(10),
            spacing=dp(8)
        )

        root.add_widget(
            self.header("Pesanan Saya")
        )

        self.order_area = GridLayout(
            cols=1,
            spacing=dp(8)
        )

        scroll = ScrollView()
        scroll.add_widget(self.order_area)

        root.add_widget(scroll)

        back_home = make_button(
            "KEMBALI KE MENU",
            bg=GREEN,
            color=WHITE,
            height=50,
            font_size=13
        )

        back_home.bind(
            on_release=lambda instance:
            self.go("home", "right")
        )

        root.add_widget(back_home)

        root.add_widget(
            self.bottom_nav()
        )

        self.add_widget(root)

    def create_order(self):

        app = App.get_running_app()

        total = 0

        items = []

        for product in PRODUCTS:

            name = product["name"]

            if name in app.cart:

                quantity = app.cart[name]

                subtotal = (
                    product["price"]
                    * quantity
                )

                total += subtotal

                items.append(
                    f"{name} x {quantity}"
                )

        app.order_items = items
        app.order_total = total

        self.refresh()

        # Keranjang dikosongkan setelah pembayaran
        app.cart.clear()

        cart = self.manager.get_screen("cart")
        cart.refresh()

    def refresh(self):

        self.order_area.clear_widgets()

        app = App.get_running_app()

        if not app.order_items:

            card = make_card(
                color=WHITE,
                padding=20
            )

            card.height = dp(180)

            card.add_widget(
                make_label(
                    "Belum ada pesanan",
                    size=18,
                    color=GRAY,
                    bold=True,
                    halign="center"
                )
            )

            self.order_area.add_widget(card)

            return

        card = make_card(
            color=WHITE,
            padding=15
        )

        card.height = dp(280)

        card.add_widget(
            make_label(
                "PESANAN BERHASIL 🎉",
                size=18,
                color=GREEN,
                bold=True,
                halign="center"
            )
        )

        card.add_widget(
            make_label(
                "Status: Diproses",
                size=14,
                color=DARK_GREEN,
                bold=True,
                halign="center"
            )
        )

        card.add_widget(
            make_label(
                "\n".join(app.order_items),
                size=13,
                color=BLACK
            )
        )

        card.add_widget(
            make_label(
                f"Total: {rupiah(app.order_total)}",
                size=17,
                color=GREEN,
                bold=True
            )
        )

        card.add_widget(
            make_label(
                f"Pembayaran: {app.last_payment}",
                size=13,
                color=GRAY
            )
        )

        self.order_area.add_widget(card)


# =========================================================
# PROFILE
# =========================================================

class ProfileScreen(BaseScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build()

    def build(self):

        root = BoxLayout(
            orientation="vertical",
            padding=dp(12),
            spacing=dp(10)
        )

        title = make_label(
            "Profil",
            size=22,
            color=DARK_GREEN,
            bold=True,
            halign="center"
        )

        title.size_hint_y = None
        title.height = dp(55)

        root.add_widget(title)

        profile_card = make_card(
            color=RED,
            padding=20
        )

        profile_card.height = dp(190)

        profile_card.add_widget(
            make_label(
                "👤",
                size=55,
                color=WHITE,
                bold=True,
                halign="center"
            )
        )

        profile_card.add_widget(
            make_label(
                "CLICK BURGER USER",
                size=18,
                color=WHITE,
                bold=True,
                halign="center"
            )
        )

        profile_card.add_widget(
            make_label(
                "user@clickburger.com",
                size=12,
                color=WHITE,
                halign="center"
            )
        )

        root.add_widget(profile_card)

        account = make_button(
            "ACCOUNT INFORMATION",
            bg=WHITE,
            color=DARK_GREEN,
            height=48,
            font_size=12
        )

        password = make_button(
            "PASSWORD",
            bg=WHITE,
            color=DARK_GREEN,
            height=48,
            font_size=12
        )

        settings = make_button(
            "SETTINGS",
            bg=WHITE,
            color=DARK_GREEN,
            height=48,
            font_size=12
        )

        logout = make_button(
            "LOG OUT",
            bg=RED,
            color=WHITE,
            height=48,
            font_size=12
        )

        account.bind(
            on_release=lambda instance:
            self.show_message("Informasi akun siap digunakan.")
        )

        password.bind(
            on_release=lambda instance:
            self.show_message("Halaman password.")
        )

        settings.bind(
            on_release=lambda instance:
            self.show_message("Pengaturan aplikasi.")
        )

        logout.bind(
            on_release=lambda instance:
            self.go("login", "right")
        )

        root.add_widget(account)
        root.add_widget(password)
        root.add_widget(settings)
        root.add_widget(logout)

        root.add_widget(
            Widget()
        )

        root.add_widget(
            self.bottom_nav()
        )

        self.add_widget(root)

    def show_message(self, message):

        # Tidak membuat aplikasi keluar.
        # Pesan ditampilkan di console.
        print(message)


# =========================================================
# APP
# =========================================================

class ClickBurgerApp(App):

    def build(self):

        self.title = "CLICK BURGER"

        # Keranjang:
        # {"Classic Beef": 2, "Black Burger": 1}
        self.cart = {}

        self.last_payment = "QRIS"
        self.order_items = []
        self.order_total = 0

        manager = ScreenManager()

        manager.add_widget(
            LoginScreen(name="login")
        )

        manager.add_widget(
            HomeScreen(name="home")
        )

        manager.add_widget(
            DetailScreen(name="detail")
        )

        manager.add_widget(
            CartScreen(name="cart")
        )

        manager.add_widget(
            CheckoutScreen(name="checkout")
        )

        manager.add_widget(
            PaymentScreen(name="payment")
        )

        manager.add_widget(
            OrdersScreen(name="orders")
        )

        manager.add_widget(
            ProfileScreen(name="profile")
        )

        manager.current = "login"

        return manager


# =========================================================
# START
# =========================================================

if __name__ == "__main__":
    ClickBurgerApp().run()