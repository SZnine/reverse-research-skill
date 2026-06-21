# Source Registry

This registry records the public methodology and tool-documentation anchors used when designing this skill pack. Sources should be treated by authority tier:

- S0: official standard/spec/tool documentation.
- S1: official project repository or API documentation.
- S2: high-reputation research/community material.
- S3: anecdotal community content; hypothesis only.

## S0/S1 sources used

1. OWASP MASTG / MAS: reverse engineering, static analysis, dynamic analysis, Android techniques, method hooking, execution tracing, repackaging and re-signing.
   - https://mas.owasp.org/MASTG/0x04c-Tampering-and-Reverse-Engineering/
   - https://mas.owasp.org/MASTG/techniques/
   - https://mas.owasp.org/MASTG/techniques/generic/MASTG-TECH-0047/
   - https://mas.owasp.org/MASTG/techniques/generic/MASTG-TECH-0048/
   - https://mas.owasp.org/MASTG/techniques/generic/MASTG-TECH-0049/
   - https://mas.owasp.org/MASTG/techniques/generic/MASTG-TECH-0050/
   - https://mas.owasp.org/MASTG/techniques/generic/MASTG-TECH-0051/
   - https://mas.owasp.org/MASTG/techniques/android/MASTG-TECH-0043/
   - https://mas.owasp.org/MASTG/techniques/android/MASTG-TECH-0032/
   - https://mas.owasp.org/MASTG/techniques/android/MASTG-TECH-0039/
2. Frida documentation: modes of operation, Gadget, JavaScript API, Android usage, Stalker.
   - https://frida.re/docs/modes/
   - https://frida.re/docs/javascript-api/
   - https://frida.re/docs/examples/android/
   - https://frida.re/docs/stalker/
3. Ghidra official documentation and repository: SRE framework, decompiler, program tree, symbol table/tree, function graph, call tree, scripting/headless.
   - https://github.com/NationalSecurityAgency/ghidra
   - https://ghidra.re/ghidra_docs/GhidraClass/Beginner/Introduction_to_Ghidra_Student_Guide.html
   - https://ghidra.re/ghidra_docs/api/ghidra/app/util/headless/HeadlessScript.html
4. Apktool documentation: disassemble, assemble, analyze APK resources and manifests.
   - https://apktool.org/
5. JADX official repository: Dex/APK Java decompiler with decompilation caveat.
   - https://github.com/skylot/jadx
6. Android Developers apksigner documentation: APK signing schemes v1-v4.
   - https://developer.android.com/tools/apksigner
7. Official Radare2 Book: static/dynamic distinction and ESIL emulation concept.
   - https://book.rada.re/emulation/intro.html

## Source use policy

- Official tool/platform docs can define tool capabilities and invariants, but still require version applicability.
- Community tips must enter `KNOWLEDGE_CANDIDATES.md` first.
- Project-specific findings must never be added to the generic source registry as universal rules.
