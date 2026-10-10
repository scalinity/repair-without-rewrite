#!/usr/bin/env python3
"""Independent export audit. Does not import the renderer or scientific code."""
import argparse
import hashlib
import json
import re
import subprocess
import xml.etree.ElementTree as ET
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

from pypdf import PdfReader
from pypdf.generic import ContentStream

ROOT = Path(__file__).resolve().parents[2]
G1 = 'experiments/manifests/six_10m_probes/descriptive-tables.attempt01.json'
G2 = 'experiments/manifests/generation_2/scientific-results.attempt01.json'
ACC = 'experiments/manifests/generation_2/scientific-accounting-independent.attempt01.json'
INVENTORY = 'experiments/manifests/manuscript_development_evidence/evidence-inventory.attempt01.json'
BASE = '2550823ca8f4f3c3ceb15a0de775e43878291422'
CHECKS = []


def check(condition, name):
    CHECKS.append(name)
    if not condition:
        raise AssertionError(name)


def load(path):
    return json.loads((ROOT / path).read_text())


def source_value(spec):
    # Separate source traversal/tokenizer and formatting implementation.
    if 'pointer' in spec:
        result = load(spec['path'])
        for part in spec['pointer']:
            result = result[part]
        values = result if isinstance(result, list) else [result]
    else:
        line = (ROOT / spec['path']).read_text().splitlines()[spec['line'] - 1]
        if 'column' in spec:
            line = line.split('|')[spec['column'] + 1]
        tokens = re.findall(r'(?<![\w.])(?:\d[\d,]*(?:\.\d+)?|\.\d+)', line)
        values = [tokens[k].replace(',', '') for k in spec['tokens']]
    values = [Decimal(str(v)) * Decimal(str(spec.get('scale', 1))) for v in values]
    is_list = len(values) != 1 or spec['format'] in ['range', 'interval', 'frequency']
    return values if is_list else values[0]


def expected_label(value, fmt):
    if fmt == 'frequency':
        return f'{value[0]:,.0f} x {value[1]:,.0f}; {value[2]:,.0f} x {value[3]:,.0f}'
    if fmt in ['range','interval']:
        lo, hi = value
        if fmt == 'range':
            return f'{lo:,.0f}' if lo == hi else f'{lo:,.0f}-{hi:,.0f}'
        return f'[{lo:.6f}, {hi:.6f}]'
    if fmt == 'int': return f'{value:,.0f}'
    if fmt == 'signed_int': return f'{value:+,.0f}' if value else '0'
    return str(value.quantize(Decimal('0.000001')))


def aggregate_checks():
    g1,g2,acc=load(G1),load(G2),load(ACC)
    check(g1['evaluation_population']=={'natural':108,'generated':288},'F01 separate natural/generated populations')
    for arm in ['B100','C101']:
        check(g1['arms'][arm]['selected_peak_lr'] is None and not g1['arms'][arm]['eligible_ranking'],'F01 null LR selection '+arm)
    for out in g1['outcomes']:
        row=next(x for x in out['learning_curve'] if x['nominal_endpoint']==10000000)['natural']
        exact=Decimal(row['output_errors'])*100/Decimal(row['reference_words'])
        receipt=Decimal(str(row['wer']))*100
        check(exact.quantize(Decimal('.000001'))==receipt.quantize(Decimal('.000001')),'G1 exact count/word WER '+out['recipe_id'])
        check(out['eligible'] is False,'G1 ineligible '+out['recipe_id'])
    for key,row in g2['tables'].items():
        n=row['natural']
        exact=Decimal(n['output_errors'])*100/Decimal(n['reference_words'])
        receipt=Decimal(str(n['wer']))*100
        check(exact.quantize(Decimal('.000001'))==receipt.quantize(Decimal('.000001')),'G2 exact count/word WER '+key)
        check(n['reference_words']==50926 and n['source_errors']==1413 and n['cases']==2696 and row['generated']['cases']==288,'G2 fixed denominators/populations '+key)
    cells={'B100':[114.858815,124.384401,111.086675,33.375879],'C101':[4.832502,6.230609,10.768566,8.041079]}
    for arm,expected in cells.items():
        effect=g2['factorial_analysis'][arm]['effects']['WER']
        keys=[g2['factorial_analysis'][arm]['cells'][cell] for cell in ['D0-U1','D0-U8','D1-U1','D1-U8']]
        observed=[round(g2['tables'][k]['natural']['wer']*100,6) for k in keys]
        check(observed==expected,'F02 approved roster '+arm)
        a,b,c,d=[Fraction(g2['tables'][k]['natural']['output_errors'],50926) for k in keys]
        raw=effect['exact_effects']['difference_in_differences']
        check((d-c)-(b-a)==Fraction(raw['numerator'],raw['denominator']),'F02 exact rational interaction '+arm)
    for arm,key in [('B100','G2-B100-D1-U8-seed42-lr3e-4/update2440'),('C101','G2-C101-D1-U8-seed42-lr3e-4/update2440'),('ByT5','G2-ByT5-D1-10pass-seed42-lr3e-4/update35283')]:
        n=g2['tables'][key]['natural']
        for i in [0,1]:
            check(n['source_errors']-n['repair'][i]+n['introduced'][i]==n['output_errors'],'F03 raw conservation '+arm+str(i))
    check(763+261==1024 and 763*18+261*19==18693,'F06 D0 distribution weighted sum')
    check(8688+5425==14113 and 8688+2*5425==19538,'F06 D1 distribution weighted sum')
    check(round(18693/1024,6)==18.254883 and round(19538/14113,6)==1.384397,'F06 exact mean repetition')
    check(round(1000665/54812,6)==18.256312 and round(1000628/721825,6)==1.386247,'F06 registered charge-based pass equivalent arithmetic')
    for actual,oracle,gain,categories in [(16997,1411,2,[2,297,2397]),(4095,1410,3,[3,2197,496]),(1650,1304,109,[67,2360,269])]:
        check(sum(categories)==2696 and 1413-oracle==gain,'F07 full proposal count/oracle conservation '+str(actual))
    check(round(109/50926*100,6)==.214036 and round(109/1413*100,3)==7.714,'F07 approved pp and RAW-relative headroom arithmetic')
    check(round(sum(x['recipe_wall_seconds'] for x in g1['outcomes']),6)==23128.912421,'F08 G1 nonoverlapping recipe total')
    check(round(sum(x['attempt_elapsed_seconds_MEASURED'] for x in acc['recipes']),6)==132122.121229,'F08 G2 nonoverlapping recipe total')
    check(round(23128.912421/3600,6)==6.424698 and round(132122.121229/3600,6)==36.700589,'F08 seconds/hour conversion')
    bs=g2['paired_group_bootstrap']['WER']
    check(bs['groups']==52 and bs['draws']==10000 and bs['seed']==42,'Descriptive bootstrap metadata')
    check(g2['model_or_cell_selection_performed'] is False and g2['D1_U8_remains_predeclared_candidate'] is True,'No retrospective model/cell selection')


def pdf_geometry(page, reader):
    """Read actual PDF vector paths, independently of SVG/renderer metadata."""
    points, segments, positions = [], [], []
    path = []
    for operands, operator in ContentStream(page.get_contents(),reader).operations:
        if operator == b'n': path=[]
        elif operator in [b'm',b'l',b'c',b're']:
            path.append((operator,[float(v) for v in operands]))
        elif operator in [b'S',b'f',b'f*',b'B',b'B*']:
            if len(path)==2 and path[0][0]==b'm' and path[1][0]==b'l':
                segments.append(path[0][1]+path[1][1])
            if len(path)==5 and path[0][0]==b'm' and all(p[0]==b'c' for p in path[1:]):
                ends=[path[0][1]]+[p[1][-2:] for p in path[1:]]
                xs=[p[0] for p in ends]; ys=[p[1] for p in ends]
                points.append(((min(xs)+max(xs))/2,(min(ys)+max(ys))/2))
            if len(path)==1 and path[0][0]==b're' and path[0][1][2:]==[7.0,7.0]:
                xx,yy,_,_=path[0][1];points.append((xx+3.5,yy+3.5))
            path=[]
    page.extract_text(visitor_text=lambda text,cm,tm,font,size: positions.append((text.strip(),float(tm[5]),size)) if text.strip() else None)
    return points,segments,positions


def exports(directory):
    summary={}
    for ident in ['F01','F02','F03','F04','F05','F06','F07','F08']:
        data=json.loads((directory/(ident+'.data.json')).read_text())
        measurements={m['id']:m for m in data['measurements']}
        values={}
        for m in measurements.values():
            values[m['id']]=source_value(m['source'])
            v=values[m['id']]
            recorded=[str(x) for x in v] if isinstance(v,list) else str(v)
            check(recorded==m['value'],m['id']+' source value')
            check(expected_label(v,m['source']['format'])==m['label'],m['id']+' source precision/format')
        for path,digest in data['source_sha256'].items():
            check(hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest,ident+' source byte identity '+path)
        xml=ET.parse(directory/(ident+'.svg'))
        pdf=PdfReader(directory/(ident+'.pdf'))
        check(len(pdf.pages)==1,ident+' one vector page')
        page=pdf.pages[0];pdftext=page.extract_text()
        points,segments,text_positions=pdf_geometry(page,pdf)
        height=data['page_points'][1]
        def pdf_near(a,b): return abs(float(a)-float(b))<.001
        labels,marks=[],[]
        for el in xml.iter():
            mid=el.get('data-measurement')
            if not mid: continue
            check(mid in measurements,ident+' SVG known measurement '+mid)
            role=el.get('data-role')
            if role=='label':
                check(el.text==measurements[mid]['label'],mid+' SVG displayed numeric label')
                check(any(text==el.text and pdf_near(ypos,height-float(el.get('y'))) for text,ypos,size in text_positions),mid+' PDF label and placement match')
                labels.append(el.text)
            if role in ['point','baseline','interval']:
                ymin,ymax=map(Decimal,el.get('data-y-domain').split())
                bottom,top=map(Decimal,el.get('data-y-pixels').split())
                def y(v): return bottom+(v-ymin)/(ymax-ymin)*(top-bottom)
                def near(a,b): return abs(Decimal(a)-b)<Decimal('.000002')
                v=values[mid]
                if role=='point':
                    yy=Decimal(el.get('cy')) if el.tag.endswith('circle') else Decimal(el.get('y'))+Decimal('3.5')
                    check(near(yy,y(v)),mid+' plotted y matches receipt')
                    xx=Decimal(el.get('cx')) if el.tag.endswith('circle') else Decimal(el.get('x'))+Decimal('3.5')
                    check(any(pdf_near(xpos,xx) and pdf_near(ypos,Decimal(height)-y(v)) for xpos,ypos in points),mid+' PDF vector point matches receipt')
                    if el.get('data-x-measurement'):
                        xid=el.get('data-x-measurement');xv=values[xid]
                        xmin,xmax=map(Decimal,el.get('data-x-domain').split());left,right=map(Decimal,el.get('data-x-pixels').split())
                        xx=Decimal(el.get('cx')) if el.tag.endswith('circle') else Decimal(el.get('x'))+Decimal('3.5')
                        check(near(xx,left+(xv-xmin)/(xmax-xmin)*(right-left)),xid+' plotted actual progress matches receipt')
                elif role=='baseline':
                    check(near(el.get('y1'),y(v)) and near(el.get('y2'),y(v)),mid+' plotted RAW baseline')
                    check(any(pdf_near(x1,el.get('x1')) and pdf_near(x2,el.get('x2')) and pdf_near(y1,height-float(y(v))) and pdf_near(y2,y1) for x1,y1,x2,y2 in segments),mid+' PDF vector RAW baseline')
                else:
                    check(near(el.get('y1'),y(v[0])) and near(el.get('y2'),y(v[1])),mid+' plotted recorded group interval')
                    check(any(pdf_near(x1,el.get('x1')) and pdf_near(x2,x1) and pdf_near(y1,height-float(y(v[0]))) and pdf_near(y2,height-float(y(v[1]))) for x1,y1,x2,y2 in segments),mid+' PDF vector group interval')
                marks.append(mid)
        check(not list(page.images),ident+' PDF contains no raster scientific content')
        for label in labels: check(label in pdftext,ident+' PDF contains displayed numeric label '+label)
        check((directory/(ident+'.png')).read_bytes().startswith(b'\x89PNG'),ident+' PNG preview exists')
        check((directory/(ident+'.caption.md')).read_text().endswith('MANUSCRIPT_FIGURE_PREPARED\n'),ident+' caption disposition')
        summary[ident]={'source_measurements':len(measurements),'displayed_numeric_labels':len(labels),'plotted_numeric_marks':len(marks),'vector_PDF':True}
    # Explicit cross-check against approved oracle interval labels prevents leading-decimal parsing errors.
    f7=json.loads((directory/'F07.data.json').read_text())
    intervals=[m['label'] for m in f7['measurements'] if m['source']['format']=='interval']
    check(intervals==['[0.000000, 0.010418]','[0.000000, 0.013181]','[0.154027, 0.288196]'],'F07 approved oracle interval units/leading decimals')
    return summary


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--figure-dir',type=Path,default=ROOT/'docs/manuscript/figures')
    parser.add_argument('--receipt',type=Path)
    args=parser.parse_args()
    inv=load(INVENTORY)
    for entry in inv['evidence_sources']+inv['verified_public_receipt_bindings']+inv['immutable_design_input_bindings']:
        check(hashlib.sha256((ROOT/entry['path']).read_bytes()).hexdigest()==entry['sha256'],'Accepted inventory hash '+entry['path'])
    check(subprocess.check_output(['git','show',BASE+':ORCHESTRATION.html'],cwd=ROOT)==(ROOT/'ORCHESTRATION.html').read_bytes(),'ORCHESTRATION unchanged from preparation')
    aggregate_checks()
    summary=exports(args.figure_dir)
    receipt={'schema':'manuscript_figure_mechanical_validation_v1','scope':'PUBLIC_AGGREGATES_AND_VECTOR_EXPORTS_ONLY','preparation_checkpoint':BASE,'checks_passed':len(CHECKS),'figures':summary,'historical_independent_status_not_upgraded':True,'scientific_tests':'NOT_RUN','private_payload_reconstruction':'NOT_RUN','new_bootstrap':'NOT_RUN','status':'PASS_MECHANICAL_FIGURE_DATA_VALIDATION'}
    if args.receipt:
        args.receipt.parent.mkdir(parents=True,exist_ok=True)
        args.receipt.write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))


if __name__=='__main__': main()
