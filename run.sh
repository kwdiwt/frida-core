./configure --host=android-arm64 && make
python3 src/anti-anti-frida.py build/server/frida-server
adb push build/server/frida-server /sdcard/Download
