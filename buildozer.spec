name: Build TabungYuk APK

on:
  push:
    branches:
      - main
  workflow_dispatch:

env:
  PYTHONFORANDROID_PREREQUISITES_INSTALL_INTERACTIVE: "0"

jobs:
  build:
    name: Build APK
    runs-on: ubuntu-latest

    steps:

      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Setup Java
        uses: actions/setup-java@v4
        with:
          java-version: "17"
          distribution: "temurin"

      - name: Install Linux dependencies
        run: |
          sudo apt update
          sudo apt install -y \
            git \
            zip \
            unzip \
            autoconf \
            automake \
            libtool \
            libltdl-dev \
            pkg-config \
            zlib1g-dev \
            libncurses5-dev \
            libncursesw5-dev \
            cmake \
            libffi-dev \
            libssl-dev

      - name: Install Buildozer
        run: |
          python -m pip install --upgrade pip
          pip install buildozer cython

      - name: Accept Android SDK licenses
        run: |
          mkdir -p ~/.buildozer
          mkdir -p ~/.android
          yes | sdkmanager --licenses || true

      - name: Build APK
        run: |
          buildozer android debug

      - name: Upload APK
        uses: actions/upload-artifact@v4
        with:
          name: TabungYuk-APK
          path: bin/*.apk
          if-no-files-found: error
