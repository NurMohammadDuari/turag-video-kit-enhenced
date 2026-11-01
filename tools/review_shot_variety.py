"""Find repeated geometry for director review; this is not a semantic classifier."""
import argparse,collections,json
p=argparse.ArgumentParser();p.add_argument('manifest');a=p.parse_args()
e=json.load(open(a.manifest));groups=collections.defaultdict(list)
for b in e['beats']:
 s=b.get('shot',{});signature=(s.get('backdrop'),tuple(sorted((o['type'],round(o['x']/10),round(o['y']/10)) for o in s.get('objects',[]) if o['type'] not in ['label','card','number','count_number','chat'])))
 groups[signature].append(b['id'])
warnings=[v for v in groups.values() if len(v)>1]
print(json.dumps({'shots':len(e['beats']),'repeatedArrangements':warnings,'note':'Review repeated arrangements for meaningful action and continuity. Unique geometry does not prove semantic or stylistic quality.'},indent=2))
