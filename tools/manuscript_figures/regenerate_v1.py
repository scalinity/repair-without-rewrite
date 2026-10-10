#!/usr/bin/env python3
"""Render approved F01-F08 from public aggregate receipts; no scientific imports."""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import subprocess
from decimal import Decimal
from pathlib import Path

import reportlab
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[2]
PREPARATION = "2550823ca8f4f3c3ceb15a0de775e43878291422"
SCIENTIFIC = "609f97f31979d469ad8551d06b2c07c3513181ec"
INVENTORY = "experiments/manifests/manuscript_development_evidence/evidence-inventory.attempt01.json"
G1 = "experiments/manifests/six_10m_probes/descriptive-tables.attempt01.json"
G2 = "experiments/manifests/generation_2/scientific-results.attempt01.json"
ACCOUNTING = "experiments/manifests/generation_2/scientific-accounting-independent.attempt01.json"
SCHEDULE = "experiments/manifests/generation_2/byt5-execution-schedule.attempt01.json"
FEASIBILITY = "docs/reports/POST_G2_READ_ONLY_TASK_FEASIBILITY_V1.md"
BLUEPRINT = "docs/manuscript/CLAIM_AND_FIGURE_REGISTRY_V1.md"
BLUE, ORANGE, PURPLE = "#0072B2", "#B65C00", "#8755A5"
INK, GREY, RULE, LIGHT = "#202A33", "#53616D", "#D7DFE5", "#F3F6F8"
FONT = Path(reportlab.__file__).parent / "fonts"
pdfmetrics.registerFont(TTFont("Vera", str(FONT / "Vera.ttf")))
pdfmetrics.registerFont(TTFont("VeraBold", str(FONT / "VeraBd.ttf")))
CACHE = {}


def read(path):
    if path not in CACHE:
        CACHE[path] = json.loads((ROOT / path).read_text()) if path.endswith(".json") else (ROOT / path).read_text()
    return CACHE[path]


def resolve(spec):
    v = read(spec["path"])
    if "pointer" in spec:
        for key in spec["pointer"]:
            v = v[key]
    else:
        v = v.splitlines()[spec["line"] - 1]
        if "column" in spec:
            v = v.strip().strip("|").split("|")[spec["column"]].strip()
        numbers = re.findall(r"(?<![\w.])(?:[0-9][0-9,]*(?:\.[0-9]+)?|\.[0-9]+)", v)
        v = [Decimal(numbers[i].replace(",", "")) for i in spec["tokens"]]
        if len(v) == 1:
            v = v[0]
    scale = Decimal(str(spec.get("scale", 1)))
    if isinstance(v, list):
        return [Decimal(str(x)) * scale for x in v]
    return Decimal(str(v)) * scale


def j(path, *pointer, scale=1, fmt="int"):
    return {"path": path, "pointer": list(pointer), "scale": scale, "format": fmt}


def md(row, column, tokens=(0,), path=FEASIBILITY, fmt="int", table_header=None):
    lines = read(path).splitlines()
    hits = [i for i, line in enumerate(lines) if line.startswith("| " + row + " |")]
    if table_header:
        start = next(i for i, line in enumerate(lines) if line.startswith(table_header))
        end = next((i for i in range(start + 1, len(lines)) if not lines[i].startswith('|')), len(lines))
        hits = [i for i in hits if start < i < end]
    if len(hits) != 1:
        raise ValueError(f"Expected exactly one public row {row!r}: {hits}")
    return {"path": path, "line": hits[0] + 1, "column": column, "tokens": list(tokens), "format": fmt}


def text_numbers(needle, tokens, path=FEASIBILITY, fmt="dec"):
    hits = [i for i, line in enumerate(read(path).splitlines()) if needle in line]
    if len(hits) != 1:
        raise ValueError(f"Nonunique public line: {needle}")
    return {"path": path, "line": hits[0] + 1, "tokens": list(tokens), "format": fmt}


def format_value(v, fmt):
    if isinstance(v, list):
        if fmt == "frequency":
            return f"{v[0]:,.0f} x {v[1]:,.0f}; {v[2]:,.0f} x {v[3]:,.0f}"
        if v[0] == v[-1] and fmt == "range":
            return f"{v[0]:,.0f}"
        f = ",.0f" if fmt == "range" else ".6f"
        return "[" + format(v[0], f) + ", " + format(v[-1], f) + "]" if fmt == "interval" else format(v[0], f) + "-" + format(v[-1], f)
    if fmt == "int":
        return f"{v:,.0f}"
    if fmt == "signed_int":
        return f"{v:+,.0f}" if v else "0"
    return f"{v:.6f}"


class Measurement:
    def __init__(self, sheet, spec):
        self.spec, self.value = spec, resolve(spec)
        self.label = format_value(self.value, spec["format"])
        self.id = f"{sheet.id}-{len(sheet.data) + 1:04d}"
        sheet.data.append({"id": self.id, "source": spec, "value": [str(v) for v in self.value] if isinstance(self.value, list) else str(self.value), "label": self.label})


class Sheet:
    def __init__(self, ident, title, height=680, width=900):
        self.id, self.title, self.w, self.h = ident, title, width, height
        self.data, self.svg = [], []
        self.pdf = canvas.Canvas(str(OUT / f"{ident}.pdf"), pagesize=(width, height), invariant=1, pageCompression=1)
        self.pdf.setTitle(f"{ident}: {title}")
        self.pdf.setAuthor("")
        self.pdf.setSubject("Public aggregate DEVELOPMENT evidence; manuscript figures v1")
        self.rect(0, 0, width, height, "#FFFFFF")
        self.txt(36, 36, f"{ident}  |  {title}", 19, bold=True)
        self.txt(36, 59, "Repair Without Rewrite  /  DEVELOPMENT evidence  /  seed 42", 11, GREY)
        self.line(36, 73, width - 36, 73, RULE)

    def m(self, spec):
        return Measurement(self, spec)

    def txt(self, x, y, value, size=11, color=INK, bold=False, align="left"):
        m = value if isinstance(value, Measurement) else None
        text = m.label if m else str(value)
        font = "VeraBold" if bold else "Vera"
        width = pdfmetrics.stringWidth(text, font, size)
        left = x if align == "left" else x - width / (2 if align == "center" else 1)
        if left < 0 or left + width > self.w or y - size < 0 or y > self.h:
            raise ValueError(f"Text outside page: {self.id} {text}")
        self.pdf.setFont(font, size)
        self.pdf.setFillColor(color)
        self.pdf.drawString(left, self.h - y, text)
        attr = f' data-measurement="{m.id}" data-role="label"' if m else ""
        self.svg.append(f'<text x="{x:.6f}" y="{y:.6f}" font-size="{size}" fill="{color}" text-anchor="{ {"left":"start","center":"middle","right":"end"}[align]}" font-weight="{"bold" if bold else "normal"}"{attr}>{html.escape(text)}</text>')

    def line(self, x1, y1, x2, y2, color=INK, width=1, dashed=False, attrs=""):
        self.pdf.setStrokeColor(color)
        self.pdf.setLineWidth(width)
        self.pdf.setDash([4, 3] if dashed else [])
        self.pdf.line(x1, self.h-y1, x2, self.h-y2)
        self.pdf.setDash([])
        dash = ' stroke-dasharray="4 3"' if dashed else ""
        self.svg.append(f'<line x1="{x1:.6f}" y1="{y1:.6f}" x2="{x2:.6f}" y2="{y2:.6f}" stroke="{color}" stroke-width="{width}"{dash}{attrs}/>')

    def rect(self, x, y, w, h, color, stroke=None):
        self.pdf.setFillColor(color)
        self.pdf.setStrokeColor(stroke or color)
        self.pdf.rect(x, self.h-y-h, w, h, fill=1, stroke=bool(stroke))
        self.svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{color}" stroke="{stroke or "none"}"/>')

    def mark(self, x, y, color, shape="circle", attrs=""):
        self.pdf.setFillColor("#FFFFFF" if shape == "open" else color)
        self.pdf.setStrokeColor(color)
        if shape == "square":
            self.pdf.rect(x-3.5, self.h-y-3.5, 7, 7, fill=1, stroke=0)
            self.svg.append(f'<rect x="{x-3.5:.6f}" y="{y-3.5:.6f}" width="7" height="7" fill="{color}"{attrs}/>')
        else:
            self.pdf.circle(x, self.h-y, 3.7, fill=1, stroke=0)
            if shape == "open":
                self.pdf.circle(x, self.h-y, 3.7, fill=0, stroke=1)
            self.svg.append(f'<circle cx="{x:.6f}" cy="{y:.6f}" r="3.7" fill="{"#FFFFFF" if shape == "open" else color}" stroke="{color}"{attrs}/>')

    def section(self, y, title):
        self.txt(36, y, title, 13, bold=True)

    def table(self, y, headers, widths, rows, rowh=27):
        x0 = 36
        assert sum(widths) <= self.w - 72
        headerh = 43
        self.rect(x0, y, sum(widths), headerh, LIGHT)
        x = x0
        for header, width in zip(headers, widths):
            for i, part in enumerate(header.split("\n")):
                self.txt(x+8, y+16+i*14, part, 10, bold=True)
            x += width
        self.line(x0, y+headerh, x0+sum(widths), y+headerh, RULE)
        for n, row in enumerate(rows):
            top = y+headerh+n*rowh
            x = x0
            for val, width in zip(row, widths):
                if isinstance(val, Measurement):
                    self.txt(x+width-8, top+18, val, 11, align="right")
                elif str(val).isdecimal():
                    self.txt(x+width-8, top+18, val, 11, align="right")
                else:
                    self.txt(x+8, top+18, val, 11)
                x += width
            self.line(x0, top+rowh, x0+sum(widths), top+rowh, RULE, .6)
        return y+headerh+len(rows)*rowh

    def note(self, y, lines):
        for i, line in enumerate(lines):
            self.txt(36, y+i*17, line, 10, GREY)

    def save(self, caption, provenance, coverage):
        self.pdf.showPage()
        self.pdf.save()
        svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}pt" height="{self.h}pt" viewBox="0 0 {self.w} {self.h}" role="img" aria-labelledby="title desc"><title id="title">{html.escape(self.id+": "+self.title)}</title><desc id="desc">{html.escape(caption)}</desc><g font-family="Bitstream Vera Sans, DejaVu Sans, Arial, sans-serif">' + "\n".join(self.svg) + "</g></svg>\n"
        (OUT/f"{self.id}.svg").write_text(svg)
        (OUT/f"{self.id}.caption.md").write_text(f"# {self.id} — {self.title}\n\n{caption}\n\n## Data provenance\n\n{provenance}\n\n## Verification scope\n\n{coverage}\n\nFACT — Sources retain their historical status; plotting does not requalify a scientific result. No private payload, new bootstrap, neural execution or new analytical treatment is used.\n\nMANUSCRIPT_FIGURE_PREPARED\n")
        (OUT/f"{self.id}.data.json").write_text(json.dumps({"schema":"manuscript_figure_public_data_v1","figure":self.id,"preparation_checkpoint":PREPARATION,"scientific_checkpoint":SCIENTIFIC,"page_points":[self.w,self.h],"source_sha256":{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in sorted({v['source']['path'] for v in self.data})},"measurements":self.data},indent=2)+"\n")
        subprocess.run(["pdftoppm","-singlefile","-png","-r","180",str(OUT/f"{self.id}.pdf"),str(OUT/self.id)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)


class Plot:
    def __init__(self, s, x, y, w, h, xmin, xmax, ymin, ymax, xticks, yticks, title, xlabel):
        self.s, self.x, self.y, self.w, self.h = s,x,y,w,h
        self.xmin,self.xmax,self.ymin,self.ymax = xmin,xmax,ymin,ymax
        s.txt(x, y-33, title, 12, bold=True)
        for tick,label in yticks:
            yy=self.py(tick); s.line(x,yy,x+w,yy,RULE,.6); s.txt(x-10,yy+4,label,10,align="right")
        for tick,label in xticks:
            xx=self.px(tick); s.line(xx,y+h,xx,y+h+4,INK,.7); s.txt(xx,y+h+19,label,10,align="center")
        s.line(x,y,x,y+h,INK,.8); s.line(x,y+h,x+w,y+h,INK,.8)
        s.txt(x+w/2,y+h+39,xlabel,11,align="center")
        s.txt(x-38,y-14,"WER %",10)

    def px(self,v): return self.x+(float(v)-self.xmin)/(self.xmax-self.xmin)*self.w
    def py(self,v): return self.y+self.h-(float(v)-self.ymin)/(self.ymax-self.ymin)*self.h
    def yattrs(self,m):
        return f' data-measurement="{m.id}" data-y-domain="{self.ymin} {self.ymax}" data-y-pixels="{self.y+self.h} {self.y}"'

    def raw(self,m,label=True):
        yy=self.py(m.value)
        self.s.line(self.x,yy,self.x+self.w,yy,INK,1,True,self.yattrs(m)+' data-role="baseline"')
        if label: self.s.txt(self.x+7,yy-7,"RAW",10,bold=True)

    def point(self,x,m,color,shape="circle",label=False,xm=None):
        if not self.ymin <= float(m.value) <= self.ymax: raise ValueError("Point outside declared axis")
        attrs=self.yattrs(m)+' data-role="point"'
        if xm:
            attrs+=f' data-x-measurement="{xm.id}" data-x-domain="{self.xmin} {self.xmax}" data-x-pixels="{self.x} {self.x+self.w}"'
        self.s.mark(self.px(x),self.py(m.value),color,shape,attrs)
        if label: self.s.txt(self.px(x),self.py(m.value)-11,m,10,color,align="center")

    def interval(self,x,m,color):
        lo,hi=m.value
        self.s.line(self.px(x),self.py(lo),self.px(x),self.py(hi),color,1.3,attrs=self.yattrs(m)+' data-role="interval"')
        for v in [lo,hi]: self.s.line(self.px(x)-4,self.py(v),self.px(x)+4,self.py(v),color,1)

    def series(self,xs,ys,color,shape):
        for a,b,c,d in zip(xs[:-1],ys[:-1],xs[1:],ys[1:]):
            self.s.line(self.px(a.value),self.py(b.value),self.px(c.value),self.py(d.value),color,1.1)
        for x,y in zip(xs,ys): self.point(x.value,y,color,shape,xm=x)


def nat(s,key,field,fmt="int",scale=1): return s.m(j(G2,"tables",key,"natural",field,fmt=fmt,scale=scale))
def state(s,key,field): return s.m(j(G2,"tables",key,"state",field))
def endpoint(arm,cell): return f"archived-{arm}-D0-U1" if cell=="D0-U1" else f"G2-{arm}-{cell}-seed42-lr3e-4/update{305 if cell.endswith('U1') else 2440}"
RAWKEY=endpoint("C101","D1-U8")
def raw(s): return nat(s,RAWKEY,"RAW_WER",fmt="dec",scale=100)
COMMON="All natural G2 observations retain 2,696 cases, 50,926 reference words, 1,413 RAW errors and 52 groups. Repair rates use source errors; introduction rates use reference words."
HIST="FACT — Historical G2 result reconstruction independently verified the original scores, failures, intervals and fixed endpoint gates. This package checks public aggregates only; it does not rerun that reconstruction. Training-seed and domain/pretraining uncertainty remain unmeasured."


def f01():
    s=Sheet("F01","Generation-1 scratch outcomes",790)
    rows=[]; gen=[]
    for i,r in sorted(enumerate(read(G1)['outcomes']),key=lambda item:(item[1]['arm'],item[1]['peak_lr'])):
        ei=next(k for k,e in enumerate(r['learning_curve']) if e['nominal_endpoint']==10000000)
        p=("outcomes",i,"learning_curve",ei)
        label=r['arm']+" / "+{"1e-04":"1e-4","3e-04":"3e-4","6e-04":"6e-4"}[r['recipe_id'].split('lr')[-1]]
        rows.append([label]+[s.m(j(G1,*p,"natural",k,fmt=f,scale=sc)) for k,f,sc in [('output_errors','int',1),('wer','dec',100),('completed_repair','range',1),('introduced','range',1),('invalid_or_incomplete','int',1)]])
        gen.append([label]+[s.m(j(G1,*p,"generated",k)) for k in ['whole_case_conformance','required_repair_cases_completed','required_repair_fields_completed','structure_invalid','decoder_invalid_or_incomplete']])
    base=s.m(j(G1,'outcomes',0,'learning_curve',5,'natural','RAW_WER',scale=100,fmt='dec'))
    s.section(99,"Natural DEVELOPMENT: all six endpoints are ineligible")
    s.table(111,['Arm / peak LR','Errors\n/ 2,270 words','WER %','Completed repair\n/ 64 source errors','Introduced errors\n/ 2,270 words','Invalid/capped\n/ 108 cases'],[150,125,108,165,160,120],rows)
    s.txt(36,343,"RAW baseline: 64 / 2,270 reference words; WER % =",11)
    s.txt(441,343,base,11,bold=True)
    s.section(383,"Generated DEVELOPMENT: separate populations and structural qualification")
    s.table(395,['Arm / peak LR','Conformance\n/ 288 cases','Genuine repairs\n/ 192 cases','Repaired fields\n/ 288 fields','Structure invalid\n/ 288 cases','Decoder failures\n/ 288 cases'],[150,125,145,145,135,128],gen)
    s.note(640,['Natural repairs and introductions are alignment bounds, not statistical confidence intervals.','Generated successes require complete structural qualification; generated learning is not natural repair.','Single seed 42; no sampling bars; training-seed variability and domain transfer are unmeasured.','Both eligible rankings are empty and both selected learning rates are null.'])
    s.save('MEASURED RESULT — Six fixed seed-42 scratch endpoints at nominal 10M (actual 10,007,223 canonical exposures; 305 updates). The natural panel contains 108 cases, 2,270 words and 64 RAW errors (2.819383% WER). All endpoints fail natural adequacy; neither arm has a selected LR. Generated conformance (/288), genuine repaired cases (/192), and repaired fields (/288) are separately qualified and cannot substitute for natural repair. Decoder and structural failures remain visible. Repair/introduction ranges are alignment bounds; no sampling intervals are available here.',f'E03: `{G1}`, `outcomes[].learning_curve[]` where `nominal_endpoint=10000000`; endpoint selections in `experiments/manifests/six_10m_probes/endpoint-selection.attempt01.json`. Each numeric field is bound in F01.data.json. E04 independent metrics/provenance/report-consistency reviews bind the historical checks.','FACT — Historically independent G1 reconstruction covers all 36 panels; the dense oracle covered 11,783 of 14,256 case instances, leaving 2,473 outside its budget. No status is upgraded.')


def f02():
    s=Sheet('F02','Generation-2 factorial WER',985)
    rawm=raw(s); rows=[]
    for arm,x,ymax,yt in [('B100',84,140,[0,35,70,105,140]),('C101',510,14,[0,3.5,7,10.5,14])]:
        plot=Plot(s,x,132,340,225,-.5,1.5,0,ymax,[(0,'D0'),(1,'D1')],[(v,str(v)) for v in yt],arm+' (separate WER scale)','Data condition')
        plot.raw(rawm)
        for di,d in enumerate(['D0','D1']):
            for u,off,color,shape in [('U1',-.13,BLUE,'circle'),('U8',.13,ORANGE,'square')]:
                cell=d+'-'+u; key=endpoint(arm,cell)
                m=nat(s,key,'wer','dec',100); ci=s.m(j(G2,'paired_group_bootstrap','WER','intervals',key,scale=100,fmt='interval'))
                plot.interval(di+off,ci,color); plot.point(di+off,m,color,shape)
                rows.append([arm+' '+cell+(' *' if cell=='D0-U1' else ' †' if cell=='D1-U8' else ''),nat(s,key,'output_errors'),m,ci])
    s.mark(60,409,BLUE); s.txt(73,414,'U1: one update / master queue',11)
    s.mark(425,409,ORANGE,'square'); s.txt(438,414,'U8: eight complete subupdates / master queue',11)
    s.table(436,['Fixed cell','Output errors\n/ 50,926 words','WER %','95% paired group interval %'],[228,175,130,295],rows)
    s.txt(36,713,'RAW baseline WER %',11); s.txt(211,713,rawm,11,bold=True)
    s.section(748,'Prespecified WER contrasts (percentage points); exact fraction before ×100')
    effects=[]
    for arm in ['B100','C101']:
        prefix=('factorial_analysis',arm,'effects','WER')
        effect=s.m(j(G2,*prefix,'exact_effects','difference_in_differences','value',scale=100,fmt='dec'))
        n=s.m(j(G2,*prefix,'exact_effects','difference_in_differences','numerator'))
        den=s.m(j(G2,*prefix,'exact_effects','difference_in_differences','denominator'))
        interval=s.m(j(G2,*prefix,'paired_group_bootstrap','intervals','difference_in_differences',scale=100,fmt='interval'))
        effects.append([arm,n,den,effect,interval])
    s.table(760,['Arm','Numerator','Denominator','Interaction pp','95% group interval pp'],[105,130,150,160,283],effects)
    s.note(889,['* D0-U1 controls: archived and rescored on this panel; not retrained. † D1-U8: predeclared, failed adequacy.','Interaction = (D1U8 - D1U1) - (D0U8 - D0U1). D changes composition; U bundles optimizer effects.','Intervals: descriptive source-group sampling, 52 groups / 10,000 paired draws; not training-seed uncertainty.'])
    s.save('MEASURED RESULT/CALCULATION — All eight prespecified DEVELOPMENT endpoints, with RAW 1,413/50,926 = 2.774614% WER. B100 values above 100% are retained. Panels have explicitly different WER ranges. U1/U8 are separate marker shapes; bars represent the recorded descriptive 95% paired source-group percentile intervals (52 groups, 10,000 draws). The table retains exact values and rational WER interactions, with fractions multiplied by 100 to obtain percentage points. D0-U1 controls are archived/rescored, not retrained. Only D1-U8 supplies prescribed scratch adequacy and both candidates fail. D changes composition and U bundles optimizer behavior; cross-D actual exposures differ (D0 10,007,223; D1 10,006,223). Neither intervals nor descriptive cells establish H1 or a winner.',f'E06/E07: `{G2}`: eight `tables` endpoint keys, `paired_group_bootstrap.WER.intervals`, and `factorial_analysis.<arm>.effects.WER`. F02.data.json binds all plotted points, intervals and exact-fraction/effect labels. E09 historical independent results receipt verifies the original reconstruction.',HIST)


def f03():
    s=Sheet('F03','Completed repairs versus introduced errors',650)
    rows=[]
    for label,key in [('B100 D1-U8',endpoint('B100','D1-U8')),('C101 D1-U8',RAWKEY),('ByT5 ten-pass','G2-ByT5-D1-10pass-seed42-lr3e-4/update35283')]:
        rows.append([label]+[nat(s,key,k,f) for k,f in [('completed_repair','range'),('repair','range'),('introduced','range'),('output_errors','int'),('invalid_or_incomplete','int')]])
    rows.insert(0,['RAW (identity)','0','0','0',nat(s,RAWKEY,'source_errors'),'0'])
    s.section(104,'Failure-inclusive natural counts; no stacking of rates with different denominators')
    s.table(119,['Prescribed endpoint','Completed repair\n/ 1,413 errors','Raw repair\n/ 1,413 errors','Introduced\n/ 50,926 words','Output errors\n/ 50,926 words','Invalid/capped\n/ 2,696 cases'],[175,143,121,133,131,125],rows)
    s.note(291,['RAW repair and introduction are zero by identity. Alignment ranges are identification bounds, not confidence intervals.','Raw conservation: output errors = RAW errors - raw repair + introduced errors.','C101 conservation uses 20 raw repairs; its 18 completion-qualified repairs are a distinct utility measure.'])
    s.section(369,'Originally lexical-zero stratum (retrospective calculation; limited reconstruction)')
    damage=[]
    for i,label in enumerate(['B100 D1-U8','C101 D1-U8','ByT5 ten-pass'],1):
        damage.append([label,s.m(md('Lexical-zero cases damaged, of 1,818',i)),s.m(md('Errors in originally lexical-zero cases',i))])
    s.table(382,['Endpoint','Damaged cases / 1,818','Errors in that stratum (count)'],[240,274,314],damage)
    s.note(533,['Historical endpoint scores were independently reconstructed; detailed retrospective stratum decomposition was not','fully requalified in frontier v3. No new subgroup extraction is performed.','Training-seed and domain/pretraining uncertainty remain unmeasured; all prescribed endpoints failed WER below RAW.'])
    s.save('MEASURED RESULT/CALCULATION — Completion-qualified repairs, raw repairs, introductions, output errors and invalid/incomplete cases for the three prescribed G2 endpoints and RAW identity. '+COMMON+' Alignment ranges are not statistical intervals. C101 raw conservation uses 20 repairs, whereas completed repair is 18. Failures are retained without bare-model fallback credit. The separate lexical-zero stratum uses 1,818 cases, not the repair denominator; error totals are counts. Its recorded detailed retrospective decomposition retains limited independent reconstruction.',f'E06 `{G2}` natural endpoint fields; E08 ByT5 reconciliation; E11 `{FEASIBILITY}` §D lexical-zero table. F03.data.json records field/line/cell locators. RAW zero repair/introduction follows the approved identity baseline, not an observation invented for a missing checkpoint.',HIST+' Detailed lexical-zero decomposition remains only partially independently reconstructed, per C12.')


def f04():
    s=Sheet('F04','C101 development adaptation trajectories',1140)
    series=[]; rows=[]
    for cell,color,shape in [('D0-U8',BLUE,'circle'),('D1-U1',ORANGE,'square'),('D1-U8',PURPLE,'open')]:
        updates=[0,31,92,204,285,305] if cell=='D1-U1' else [0,248,736,1632,2280,2440]
        xs=[]; ys=[]
        for u in updates:
            key=f'G2-C101-{cell}-seed42-lr3e-4/update{u}'
            x=state(s,key,'actual_exposure'); y=nat(s,key,'wer','dec',100); xs.append(x);ys.append(y)
            rows.append([cell,x,state(s,key,'optimizer_updates'),y,nat(s,key,'completed_repair','range'),nat(s,key,'introduced','range'),nat(s,key,'invalid_or_incomplete'),nat(s,key,'source_lexical_identity')])
        series.append((cell,color,shape,xs,ys))
    p=Plot(s,82,131,337,200,0,10500000,0,100,[(0,'0'),(5000000,'5M'),(10000000,'10M')],[(0,'0'),(25,'25'),(50,'50'),(75,'75'),(100,'100')],'Full WER scale: initialization retained','Actual canonical exposure')
    z=Plot(s,511,131,337,200,0,10500000,0,12,[(0,'0'),(5000000,'5M'),(10000000,'10M')],[(0,'0'),(3,'3'),(6,'6'),(9,'9'),(12,'12')],'Post-initialization detail: 0-12%','Actual canonical exposure')
    r=raw(s);p.raw(r);z.raw(r)
    for i,(cell,color,shape,xs,ys) in enumerate(series):
        p.series(xs,ys,color,shape);z.series(xs[1:],ys[1:],color,shape)
        s.mark(52+i*267,389,color,shape);s.txt(64+i*267,394,cell+(' (predeclared endpoint)' if cell=='D1-U8' else ' (descriptive)'),11,color)
    s.table(427,['Cell','Actual canonical\nexposure','Optimizer\nupdates','WER %','Completed\nrepair /1,413','Introduced\n/50,926','Invalid\n/2,696','Lexical identity\n/2,696'],[87,151,87,110,112,108,74,99],rows,rowh=27)
    s.note(992,['Straight segments only join recorded observations; no smoothing or interpolation claim.','Alignment bounds appear as count ranges; group uncertainty is recorded in E06 but not drawn on these panels.','Early RAW equality contains zero completed repairs and is descriptive. Endpoint-only candidate gates remain failed.','Full initialization is retained above; the separate detail panel omits initialization explicitly.','Historical independent reconstruction covers these observations; seed and domain uncertainty remain unmeasured.'])
    s.save('MEASURED RESULT — The three new C101 DEVELOPMENT trajectories at six fixed observations each. The quantitative x-axis uses actual canonical exposure; exact optimizer-update counts are retained in the companion table. The full WER panel includes the 86.857401% initialization failures; the separately labelled detail panel contains post-initialization observations only. Straight segments connect observed states without smooth learning-curve inference. RAW is 2.774614%. '+COMMON+' Companion counts preserve alignment bounds, failures and source lexical identity. Early equality to RAW has zero completed repairs and is not an eligible checkpoint. Only the prescribed D1-U8 endpoint supplies scratch adequacy and it fails. Group intervals exist in E06 but are not drawn here; seed/domain uncertainty is unmeasured.',f'E06 `{G2}`, new C101 D0-U8/D1-U1/D1-U8 `tables` at updates recorded in F04.data.json; `state.actual_exposure`, `state.optimizer_updates`, and six natural fields. E07 fixed-panel observations; E09 historical independent reconstruction.',HIST)


def f05():
    s=Sheet('F05','ByT5 nominal 2/5/10-pass adaptation',820)
    xs=[];ys=[];rows=[]; schedule=[]
    for i,u in enumerate([0,7057,17642,35283]):
        key=f'G2-ByT5-D1-10pass-seed42-lr3e-4/update{u}'
        x=state(s,key,'actual_presentations');y=nat(s,key,'wer','dec',100);xs.append(x);ys.append(y)
        label=['Initialization','2-pass nominal','5-pass nominal','10-pass exact'][i]
        rows.append([label,y,nat(s,key,'completed_repair','range'),nat(s,key,'introduced','range'),nat(s,key,'invalid_or_incomplete'),s.m(j(G2,'tables',key,'generated','decoder_invalid_or_incomplete'))])
        schedule.append([label,s.m(j(SCHEDULE,'states',i,'nominal_presentations')),x,state(s,key,'optimizer_update'),s.m(j(SCHEDULE,'states',i,'presentation_offset',fmt='signed_int'))])
    p=Plot(s,82,131,337,182,0,148000,0,110,[(0,'0'),(70568,'70,568'),(141130,'141,130')],[(0,'0'),(25,'25'),(50,'50'),(75,'75'),(100,'100')],'Full scale: initialization retained','Actual presentations')
    z=Plot(s,511,131,337,182,20000,148000,2.6,3.4,[(28228,'28,228'),(70568,'70,568'),(141130,'141,130')],[(2.6,'2.6'),(2.8,'2.8'),(3,'3.0'),(3.2,'3.2'),(3.4,'3.4')],'Post-adaptation detail: 2.6-3.4%','Actual presentations')
    r=raw(s);p.raw(r);z.raw(r);p.series(xs,ys,BLUE,'circle');z.series(xs[1:],ys[1:],BLUE,'circle')
    s.table(382,['Reporting state','Nominal\npresentations','Actual\npresentations','Completed\nupdate','Offset\n(actual - nominal)'],[207,155,155,142,169],schedule)
    s.table(552,['Reporting state','Natural WER %','Completed repair\n/1,413 errors','Introduced\n/50,926 words','Natural failures\n/2,696 cases','Generated decoder\nfailures /288 cases'],[159,123,137,143,122,144],rows)
    s.note(729,['Nominal 2/5: first completed update at/after the boundary. Offsets are inside the fixed trajectory.','Only the exact ten-pass endpoint supplies adequacy, and fails WER below RAW; no checkpoint is selected.','Count ranges are alignment bounds. Sampling intervals are not drawn; seed/domain/pretraining uncertainty is unmeasured.'])
    s.save('MEASURED RESULT — One fixed seed-42 ByT5 adaptation at initialization, nominal 2-pass, nominal 5-pass and exact 10-pass states. Quantitative axes use actual presentations 0/28,228/70,568/141,130. Nominal counts are 0/28,226/70,565/141,130, with offsets 0/+2/+3/0 inside the fixed extent. Milestone labels refer to the first completed update at/after the boundary. Full initialization WER (100%) and its failures remain visible; the separate post-adaptation detail has an explicitly focused WER scale. '+COMMON+' Generated decoder failures use a separate /288 denominator; all generated outputs fail structural conformance. Count ranges are alignment bounds; no uncertainty bars are added. Only exact ten-pass adequacy applies and fails. Pretraining/data/budget differ from scratch, and no best intermediate is selected.',f'E06 `{G2}` ByT5 states; E08 `{SCHEDULE}` exact schedule/offsets and `docs/reports/G2_BYT5_SCIENTIFIC_ADAPTATION.md`. F05.data.json binds values and progress coordinates.',HIST+' Historical milestone/ten-pass reviews separately verified the nominal/actual mapping and completed-state bindings.')


def f06():
    s=Sheet('F06','D0 versus D1 natural repetition distributions',1020)
    s.section(103,'Record-balanced natural repair frequency mass (exact finite ledger counts)')
    freq=[]
    for label,col in [('D0',1),('D1',2)]:
        for tok in [(1,0),(3,2)]:
            freq.append([label,s.m(md('Repetition distribution',col,(tok[0],))),s.m(md('Repetition distribution',col,(tok[1],))),s.m(md('Natural repair records',col))])
    s.table(116,['Condition','Presentations per record','Number of records','Distinct-record denominator'],[125,229,224,250],freq)
    s.txt(36,291,'Zero-presentation repair records: D0 =',10,GREY)
    s.txt(258,291,s.m(md('Records with zero repair presentations',1)),10,GREY)
    s.txt(285,291,'D1 =',10,GREY)
    s.txt(318,291,s.m(md('Records with zero repair presentations',2)),10,GREY)
    s.note(313,['Repeated presentations are not independent new records; distinct-record denominators remain explicit.'])
    s.section(350,'Repair accounting and separate reference-as-source identity channel')
    fields=[('Natural repair records','Distinct repair records'),('Repair presentations','Repair presentations'),('Mean repair presentations per record','Mean repair repetition'),('Repair canonical exposure','Repair canonical charge'),('Separate reference-as-source identity presentations','Identity presentations (separate)'),('Identity repetition','Identity repetition: records × presentations'),('Identity canonical exposure','Identity canonical charge'),('First complete natural repair pass, ending exposure','First full repair pass: ending total exposure')]
    accounting=[]
    for row,label in fields:
        vals=[]
        for col in [1,2]:
            if row=='Identity repetition':
                vals.append(s.m(md(row,col,(0,1,2,3),fmt='frequency')))
            else: vals.append(s.m(md(row,col,fmt='dec' if row.startswith('Mean') else 'int')))
        accounting.append([label]+vals)
    accounting.append(['Charge-based repair pass equivalents',s.m(text_numbers('Charge-based natural pass equivalents reproduce',[0])),s.m(text_numbers('Charge-based natural pass equivalents reproduce',[1]))])
    s.table(362,['Quantity','D0','D1'],[438,195,195],accounting)
    s.section(688,'Phase charge table: repair and identity remain separate')
    phases=[]
    for cell in ['D0 P0','D0 P1','D0 P2','D1 P0','D1 P1','D1 P2']:
        phases.append([cell]+[s.m(md(cell,col,table_header='| Condition/phase | Repair presentations |')) for col in [1,4,5,6]])
    s.table(700,['Condition / phase','Repair\npresentations','Repair canonical\ncharge','Identity\npresentations','Identity canonical\ncharge'],[157,147,177,158,189],phases)
    s.note(935,['Exact repetition distributions were independently reaggregated in frontier v3. Detailed phase, identity and first-pass','accounting retain narrower independent coverage. No sampling interval applies to these fixed ledger counts.','D1 expands diversity at approximately fixed charge; useful transfer from more exposure remains unproved.'])
    s.save('CALCULATION — Exact natural repair frequency masses: D0 763 records presented 18 times and 261 presented 19 times; D1 8,688 presented once and 5,425 twice. Zero-presentation counts are zero. Denominators are 1,024/14,113 distinct records, with 18,693/19,538 presentations and means 18.254883/1.384397. Counts are finite ledger calculations, not independent-observation sample sizes, and no sampling bars are invented. Separate repair charge, first full repair pass, identity channel and phase accounting retain their original units. Charge-based pass equivalents (18.256312/1.386247 in E11) use full-pass charges 54,812/721,825 per the approved registry, not record counts. Increased diversity under approximately fixed charge is not a pure sample-count intervention or a test of sustained D1 training; more exposure helping is unproved.',f'E11 `{FEASIBILITY}` §§B-C tables and complete Appendices 1/3; E12 `docs/reviews/FRONTIER_POST_FEASIBILITY_SCIENTIFIC_DECISION_V3.md` §B independently reaggregates repair distributions. F06.data.json binds every numeric table cell, including all four identity-frequency tokens. Full-pass charge denominators come from F06 in `{BLUEPRINT}`.','FACT — Repair repetition distributions have historical independent reaggregation. Detailed phase/identity/first-pass accounting remains retrospective with limited independent reconstruction; mechanical arithmetic here does not upgrade it. Training-seed/generalization effects of repetition are unmeasured.')


def f07():
    s=Sheet('F07','Whole-output benefit and reference-aware oracle headroom',830)
    s.section(103,'Fixed complete proposals: outcome categories on all natural DEVELOPMENT cases')
    rows=[]
    for col,label in enumerate(['B100 D1-U8','C101 D1-U8','ByT5 exact ten-pass'],1):
        rows.append([label]+[s.m(md(row,col)) for row in ['Better than RAW','Equal to RAW','Worse than RAW','Output errors']])
    s.table(116,['Fixed endpoint','Better /2,696','Equal /2,696','Worse /2,696','Actual errors\n/50,926 words'],[240,140,140,140,168],rows)
    s.section(286,'Reference-aware oracle: NON-DEPLOYABLE ceiling (whole-output choice only)')
    ceiling=[]
    for col,label,row in [(1,'B100 D1-U8','B100-D1-U8'),(2,'C101 D1-U8','C101-D1-U8'),(3,'ByT5 exact ten-pass','ByT5 ten-pass')]:
        ceiling.append([label,s.m(md(row,1)),s.m(md(row,2)),s.m(md(row,3)),s.m(md(row,4)),s.m(md(row,5,fmt='dec'))])
    s.table(299,['Fixed endpoint','Beneficial complete\ncases /2,696','Beneficial\ngroups /52','Removable\nerrors /1,413','Oracle errors\n/50,926 words','Oracle WER %\nnon-deployable'],[184,147,103,126,135,133],ceiling)
    s.txt(36,454,'RAW baseline: 1,413 errors / 50,926 words; WER % =',11)
    s.txt(447,454,raw(s),11,bold=True)
    s.section(502,'Recorded oracle-gain sampling intervals; partial independent reconstruction')
    cis=[]
    for label in ['B100','C101','ByT5']:
        cis.append([label+' reference-aware oracle',s.m(md(label,3,(0,1),fmt='interval',table_header='| Endpoint | 95% WER interval, %'))])
    s.table(515,['Non-deployable ceiling','95% descriptive group interval (WER pp)'],[385,443],cis)
    s.note(674,['Oracle chooses RAW or one fixed complete proposal using reference errors; incomplete proposals choose RAW.','No edit mixing, new text, checkpoint choice or source-only policy is demonstrated.','Point gains were independently reaggregated in frontier v3; detailed feasibility intervals were not fully repeated.','Group sampling is not training-seed uncertainty and does not predict selectable benefit or transfer.'])
    s.save('CALCULATION — Better/equal/worse categories retain all 2,696 cases and the three prescribed fixed endpoint outputs. The reference-aware whole-output oracle is an unmistakably non-deployable ceiling: only RAW or a complete cached proposal may be selected, using the reference to compare errors; incomplete outputs choose RAW. RAW has 1,413 errors/50,926 words. Oracle errors 1,411/1,410/1,304 correspond to gains 2/3/109 across 2/3/36 of 52 groups. ByT5 headroom is 0.214036 WER pp, approximately 7.714% of RAW errors. Recorded descriptive 95% source-group gain intervals use 10,000 paired draws; point gains were independently reaggregated, but detailed oracle intervals were not fully requalified in v3. No source-only acceptance performance, new-population gain, edit mixing or checkpoint selection is shown.',f'E11 `{FEASIBILITY}` §§D-E/I tables; E12 frontier v3 §B independent point reaggregation; E06 frozen endpoint score bindings. F07.data.json includes exact report line/cell/token locators. The approved C17/C18 arithmetic is mechanically reconciled from public counts.','FACT — Whole-output point aggregates and ceilings have historical independent reaggregation. The feasibility oracle intervals retain partial independent reconstruction. Plotting does not upgrade either status; deployable benefit remains unmeasured.')


def f08():
    s=Sheet('F08','Native training and evaluation runtime',1450)
    s.section(103,'Physical recipe wall seconds: 13 attempts; components below are already included')
    rows=[]
    for i,r in enumerate(read(G1)['outcomes']):
        rows.append(['G1 '+r['recipe_id'].replace('-seed42',''),s.m(j(G1,'outcomes',i,'recipe_wall_seconds',fmt='dec')),s.m(j(G1,'outcomes',i,'training_resources','updates')),s.m(j(G1,'outcomes',i,'training_resources','summed_observed_fields','examples'))])
    for i,r in enumerate(read(ACCOUNTING)['recipes']):
        rows.append([r['recipe_id'].replace('-seed42-lr3e-4',''),s.m(j(ACCOUNTING,'recipes',i,'attempt_elapsed_seconds_MEASURED',fmt='dec')),s.m(j(ACCOUNTING,'recipes',i,'unique_logged_optimizer_updates')),s.m(j(ACCOUNTING,'recipes',i,'unique_scientific_presentations'))])
    s.table(116,['Generation / recipe','Recipe wall seconds\nMEASURED','Completed\nupdates','Unique\npresentations'],[363,198,117,150],rows)
    s.note(535,['G1: 396-case evaluations; G2: 2,984-case evaluations. These are unequal-work native timings.','Archived D0-U1 controls are rescored, not retrained; they incur zero new G2 training.'])
    s.section(602,'ByT5 components: nested inside its recipe interval; do not sum into recipe time')
    obs=[]
    for i,u in enumerate([0,7057,17642,35283]):
        path=f'experiments/manifests/generation_2/scientific-observation-G2-ByT5-D1-10pass-seed42-lr3e-4.update{u:05d}.attempt01.json'
        obs.append([['Initialization','2-pass nominal','5-pass nominal','10-pass exact'][i],s.m(j(path,'milestone','actual_presentations'))]+[s.m(j(path,k,fmt='dec')) for k in ['seconds','decode_seconds','scorer_seconds']])
    s.table(615,['Observation state','Actual\npresentations','Observation wall s\nin recipe wall','Decode s\nin observation wall','Scorer s\nin observation wall'],[179,135,176,178,160],obs)
    rindex=next(i for i,r in enumerate(read(ACCOUNTING)['recipes']) if 'ByT5' in r['recipe_id'])
    training=s.m(j(ACCOUNTING,'recipes',rindex,'attempts',0,'logged_training_seconds_MEASURED',fmt='dec'))
    s.txt(36,791,'ByT5 logged training seconds (MEASURED; included in recipe wall):',11)
    s.txt(690,791,training,11,align='right')
    s.section(850,'G1 endpoint decoding on the complete 396-case panel')
    decode=[]
    for i,r in enumerate(read(G1)['outcomes']):
        e=next(k for k,t in enumerate(r['learning_curve']) if t['nominal_endpoint']==10000000)
        decode.append([r['recipe_id'].replace('-seed42',''),s.m(j(G1,'outcomes',i,'learning_curve',e,'resources','decode_seconds',fmt='dec')),s.m(j(G1,'outcomes',i,'learning_curve',e,'resources','decoder_positions')),s.m(j(G1,'outcomes',i,'training_resources','summed_observed_fields','native_update_wall_seconds',fmt='dec'))])
    s.table(863,['G1 endpoint','Decode seconds\nin recipe wall','Decoder\npositions','Native update host s\nin recipe wall'],[310,178,128,212],decode)
    s.section(1121,'Timing scope and unavailable cost')
    s.note(1141,['Recipe wall includes training, saves and prescribed evaluation. Decode/scorer lie inside observation wall.','G1 native update host intervals and ByT5 logged training intervals are components, not extra charges.','No unnamed timing remainder is assigned to a new category. Failed CPU checks are separate from scientific replay.','Exact device kernel time: UNMEASURED. G2 all-in operational span: UNMEASURED.','Electricity, depreciation and local monetary cost: UNPRICED. Upstream pretraining cost: UNESTABLISHED.','One local native implementation; failed models and unequal comparator training do not establish overall efficiency.'])
    s.save('MEASURED RESULT — All six G1 and seven new G2 physical recipe intervals, one attempt each, with completed updates and unique presentations. G1 totals 23,128.912421 seconds (6.424698 hours), G2 totals 132,122.121229 seconds (36.700589 hours); archived D0-U1 controls add zero new G2 training. ByT5 logged training (21,143.834539 seconds) and four observation intervals are already within its 79,862.099614-second recipe interval. Decode/scorer components are nested within observations and are not added again. G1 endpoint decode and native synchronized update-host timings retain their field scopes and 396-case panel; G2 observations use 2,984 cases, so no equal-work latency comparison is claimed. Exact kernel time and G2 all-in operational span are unmeasured; electricity/depreciation/price are unpriced; pretraining is not assigned zero cost. Independent CPU review costs and retained failed review attempts are separate from scientific recipe attempts. No overall efficiency claim follows.',f'E03 `{G1}` recipe wall, training resources and endpoint evaluation resources; E10 `{ACCOUNTING}` recipes and physical_evaluations; E08 four public ByT5 observation receipts. F08.data.json binds every time/count. Aggregates/totals are checked mechanically without accessing native update logs or private evaluation payloads.','FACT — Recipe accounting and resource scopes have historical independent reconstruction. These are measured host intervals without invented timing confidence intervals; kernel traces and monetary cost remain unavailable.')


def main():
    global OUT
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir',type=Path,default=ROOT/'docs/manuscript/figures')
    args=parser.parse_args();OUT=args.output_dir;OUT.mkdir(parents=True,exist_ok=True)
    inventory=read(INVENTORY)
    for entry in inventory['evidence_sources']:
        assert hashlib.sha256((ROOT/entry['path']).read_bytes()).hexdigest()==entry['sha256'],entry['path']
    for entry in inventory['immutable_design_input_bindings']:
        assert hashlib.sha256((ROOT/entry['path']).read_bytes()).hexdigest()==entry['sha256'],entry['path']
    for func in [f01,f02,f03,f04,f05,f06,f07,f08]:
        func();print(func.__name__.upper(),'SVG/PDF/PNG/caption/data complete')


if __name__=='__main__': main()
