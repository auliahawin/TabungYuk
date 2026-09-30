[app]

title = TabungYuk
package.name = tabungyuk
package.domain = org.tabungyuk

source.dir = .
source.include_exts = py,kv,png,jpg,jpeg,db

version = 1.0

requirements = python3,kivy

orientation = portrait
fullscreen = 0

android.api = 35
android.minapi = 24
android.archs = arm64-v8a

android.accept_sdk_license = True
android.debug_artifact = apk

[buildozer]

log_level = 2
warn_on_root = 1
