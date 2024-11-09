import lief
import sys
import random
import os
 
def log_color(msg):
    print(f"\033[1;31;40m{msg}\033[0m")
 
if __name__ == "__main__":
    input_file = sys.argv[1]
    random_charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    log_color(f"[*] Patch frida-agent: {input_file}")
    binary = lief.parse(input_file)
 
    if not binary:
        log_color(f"[*] Not elf, exit")
        exit()
    
    random_name = "".join(random.sample(random_charset, 5))
    log_color(f"[*] Patch `frida` to `{random_name}`")

    for symbol in binary.symbols:
        if symbol.name == "frida_agent_main":
            symbol.name = "main"
 
        if "frida" in symbol.name:
            symbol.name = symbol.name.replace("frida", random_name)
 
        if "FRIDA" in symbol.name:
            symbol.name = symbol.name.replace("FRIDA", random_name)
 
    all_patch_string = ["FridaScriptEngine", "GLib-GIO", "GDBusProxy", "GumScript"]  # 字符串特征修改 尽量与源字符一样
    for section in binary.sections:
        if section.name != ".rodata":
            continue
        for patch_str in all_patch_string:
            addr_all = section.search_all(patch_str)  # Patch 内存字符串
            for addr in addr_all:
                patch_values = "".join(random.sample(random_charset, len(patch_str)))
                patch = [ord(n) for n in patch_values]
                log_color(f"[*] Patching section name={section.name} offset={hex(section.file_offset + addr)} orig:{patch_str} new:{patch_values}")
                binary.patch_address(section.file_offset + addr, patch)
 
    binary.write(input_file)
 
    # thread_gum_js_loop
    random_name = "".join(random.sample(random_charset, 11))
    log_color(f"[*] Patch `gum-js-loop` to `{random_name}`")
    os.system(f"sed -b -i s/gum-js-loop/{random_name}/g {input_file}")
 
    # thread_gmain
    random_name = "".join(random.sample(random_charset, 5))
    log_color(f"[*] Patch `gmain` to `{random_name}`")
    os.system(f"sed -b -i s/gmain/{random_name}/g {input_file}")
 
    # thread_gdbus
    random_name = "".join(random.sample(random_charset, 5))
    log_color(f"[*] Patch `gdbus` to `{random_name}`")
    os.system(f"sed -b -i s/gdbus/{random_name}/g {input_file}")

    log_color(f"[*] Patch Finish")
