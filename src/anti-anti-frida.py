import lief
import sys
import random
import string
import os
 
def log_color(msg):
    print(f"\033[1;31;40m{msg}\033[0m")
 
if __name__ == "__main__":
    input_file = sys.argv[1]
    letters = string.ascii_letters
    log_color(f"[*] Patch frida-agent: {input_file}")
    binary = lief.parse(input_file)
 
    if not binary:
        log_color(f"[*] Not elf, exit")
        exit()

    all_patch_string = ["FridaScriptEngine", "GLib-GIO", "GDBusProxy", "GumScript"]  # 字符串特征修改 尽量与源字符一样
    for section in binary.sections:
        if section.name != ".rodata":
            continue
        for patch_str in all_patch_string:
            addr_all = section.search_all(patch_str)  # Patch 内存字符串
            for addr in addr_all:
                patch_values = "".join(random.sample(letters, len(patch_str)))
                patch = [ord(n) for n in patch_values]
                log_color(f"[*] Patching section name={section.name} offset={hex(section.file_offset + addr)} orig:{patch_str} new:{patch_values}")
                binary.patch_address(section.file_offset + addr, patch)
 
    binary.write(input_file)
 
    for key in ['gum-js-loop', 'gmain', 'gdbus']:
        res = "".join(random.sample(letters, len(key)))
        log_color(f"[*] Patch `{key}` to `{res}`")
        os.system(f"sed -b -i s/{key}/{res}/g {input_file}")

    log_color(f"[*] Patch Finish")
