from pathlib import Path
from html import escape
import re

ROOT = Path(__file__).parent
OUT = ROOT / 'assets'
OUT.mkdir(exist_ok=True)

def diagram(lang):
    zh = lang == 'zh'
    parts = ['''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="1040" viewBox="0 0 1200 1040" role="img" aria-labelledby="title desc">
<title id="title">Reverse Research Skills architecture</title>
<desc id="desc">Evidence-driven investigation loop with three target adapters, conditional tooling and state support, operator observations, and claim-matched verification.</desc>
<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#64748b"/></marker></defs>
<style>text{font-family:Arial,'Microsoft YaHei',sans-serif;fill:#25344b} .title{font-size:26px;font-weight:700}.label{font-size:19px;font-weight:700}.body{font-size:17px}.small{font-size:15px;fill:#53657a}.edge{fill:none;stroke:#64748b;stroke-width:1.8;marker-end:url(#arrow)}.optional{stroke-dasharray:6 5}</style>
<rect width="1200" height="1040" rx="20" fill="#ffffff"/>
''']
    def text(x,y,value,cls='body',anchor='middle'):
        parts.append(f'<text x="{x}" y="{y}" class="{cls}" text-anchor="{anchor}">{escape(value)}</text>')
    def box(x,y,w,h,name,lines,color='#eef3ff',stroke='#adc0e4'):
        parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{color}" stroke="{stroke}"/>')
        text(x+w/2,y+31,name,'label')
        for i,line in enumerate(lines): text(x+w/2,y+59+i*24,line)
    def edge(d,optional=False):
        parts.append(f'<path d="{d}" class="edge {"optional" if optional else ""}"/>')
    text(40,45,'技能分工与调用关系' if zh else 'Skills and connections','title','start')
    text(40,75,'分析方法、工具、进度记录与结果检查' if zh else 'Analysis methods, tools, progress, and checks','body','start')
    box(430,105,340,88,'要解决的问题' if zh else 'The problem', ['目标 · 测试范围 · 预期结果' if zh else 'Goal · Test scope · Expected result'])
    edge('M600 193 V230')
    box(430,230,340,110,'reverse-research', ['决定下一步怎么查' if zh else 'Decide what to check next','换方法，或结束分析' if zh else 'Change approach or finish'])
    edge('M600 340 V460')
    text(612,407,'开始检查' if zh else 'Run the check','small','start')
    box(430,460,340,126,'分析与测试' if zh else 'Analyze and test', ['看代码 / 跑程序 / 修改后对比' if zh else 'Read code / Run / Compare changes','记录结果，找出还没查清的问题' if zh else 'Record results and open questions'])
    edge('M430 512 H395 V284 H430')
    text(371,365,'没有查清' if zh else 'Unresolved','small','end')
    text(371,387,'换个方法' if zh else 'Try another way','small','end')
    parts.append('<rect x="30" y="430" width="330" height="376" rx="16" fill="#f4faf8" stroke="#b9d9ce"/>')
    text(195,462,'按分析对象选择' if zh else 'Choose by target','label')
    box(47,481,296,88,'reverse-apk',['APK / DEX / smali / JNI'],'#e5f4ee','#9cccb8')
    box(47,581,296,88,'reverse-native',['二进制 / ABI / 调试' if zh else 'Binary / ABI / Debugging'],'#e5f4ee','#9cccb8')
    box(47,681,296,88,'reverse-protocol',['协议 / 文件 / 存档 / 解析' if zh else 'Protocol / File / Save / Parser'],'#e5f4ee','#9cccb8')
    edge('M430 306 H195 V430',True)
    text(206,325,'按目标选择' if zh else 'Select by target','small','start')
    edge('M360 549 H430',True)
    box(855,230,315,110,'reverse-state',['记进度，保留重要文件' if zh else 'Save progress and important files','清理临时文件，方便下次继续' if zh else 'Clean up and resume later'],'#f1f3f7','#bac4d2')
    edge('M855 284 H770',True)
    text(812,270,'继续' if zh else 'Resume','small')
    box(855,460,315,110,'reverse-toolbox',['查找、安装和检查工具' if zh else 'Find, install, and check tools','用到时再准备' if zh else 'Set up tools when needed'],'#f1f3f7','#bac4d2')
    edge('M855 507 H770',True)
    text(812,492,'工具' if zh else 'Tools','small')
    edge('M770 550 H831 V318 H855',True)
    text(843,375,'记录' if zh else 'Save','small','start')
    text(843,396,'进度与结果' if zh else 'Progress / results','small','start')
    edge('M600 586 V700')
    text(612,633,'确认原因或准备交付' if zh else 'Confirm the cause /','small','start')
    if not zh: text(612,655,'Prepare a deliverable','small','start')
    box(430,700,340,110,'reverse-verify',['检查是否真正解决问题' if zh else 'Check whether the problem is fixed','实际使用 / 保存 / 重启后再测' if zh else 'Use it / Save / Test after a restart'],'#fff1dc','#d5ad67')
    edge('M430 755 H380 V284 H430')
    text(371,841,'尚未确认 → 继续查' if zh else 'Not confirmed: keep investigating','small','end')
    box(855,700,315,110,'请用户操作' if zh else 'Ask the user',['点几下或看一眼就能确认时' if zh else 'When a few clicks or a look is faster','给出步骤，等用户返回结果' if zh else 'Give steps and wait for the result'],'#f1f3f7','#bac4d2')
    edge('M1012 700 V614 H751 V586',True)
    text(1024,647,'操作结果' if zh else 'Result','small','start')
    edge('M600 810 V900')
    text(614,858,'检查通过' if zh else 'Checks pass','small','start')
    edge('M770 575 H803 V942 H770')
    text(815,854,'简单问题已查清' if zh else 'Simple question answered','small','start')
    text(815,876,'直接回答' if zh else 'Answer directly','small','start')
    box(430,900,340,88,'给出结果' if zh else 'Report the result',['原因、修改内容及测试结果' if zh else 'Cause, changes, and test results'])
    edge('M40 1016 H90')
    text(102,1022,'分析步骤' if zh else 'Analysis steps','small','start')
    edge('M430 1016 H480',True)
    text(492,1022,'需要时调用或传递结果' if zh else 'Tools, methods, and saved results','small','start')
    parts.append('</svg>')
    (OUT/f'architecture.{lang}.svg').write_text('\n'.join(parts),encoding='utf-8')

for lang in ['zh','en']: diagram(lang)

print('Generated Chinese and English diagrams.')
