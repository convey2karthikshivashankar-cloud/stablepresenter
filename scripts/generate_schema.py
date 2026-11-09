"""Generate the explicit, strict JSON Schema used by the runtime."""
import json
from pathlib import Path
S = {"type": "string", "minLength": 1, "maxLength": 30000}
ID = {"type": "string", "pattern": "^[A-Za-z][A-Za-z0-9_-]{0,79}$"}
DATE = {"type": "string", "format": "date"}
NUM = {"type": "number", "minimum": 0}
BOOL = {"type": "boolean"}
def enum(*v): return {"enum": list(v)}
def arr(item=S): return {"type": "array", "items": item, "maxItems": 5000}
def obj(fields, required=None): return {"type": "object", "additionalProperties": False, "properties": fields, "required": list(fields) if required is None else required}
REF = obj({"path": S, "startLine": {"type":"integer", "minimum":1}, "endLine": {"type":"integer", "minimum":1}, "sourceHash": S})
common = {"id": ID, "createdAt": DATE, "updatedAt": DATE, "revision": {"type":"integer","minimum":1}, "sourceRefs": arr(REF)}
confidence=enum("unknown","low","medium","high")
life=enum("not-examined","investigating","preliminary","corroborated","validated","inconclusive","contradicted","superseded")
fields = {
 "dimensions": {"title":S,"description":S,"scope":S,"weight":{"type":"number","exclusiveMinimum":0},"coverageStatus":enum("not-examined","investigating","evaluated"),"evidenceMaturity":confidence},
 "investigations": {"dimensionId":ID,"question":S,"status":life,"owner":S,"scopeWeight":{"type":"number","exclusiveMinimum":0},"nextStep":S},
 "findings": {"investigationId":ID,"title":S,"conclusion":S,"status":life,"confidence":confidence,"evidenceRefs":arr(ID),"implications":S,"uncertainties":arr(),"nextInvestigation":S,"severity":enum("low","medium","high","critical"),"impact":enum("favorable","adverse","mixed","neutral"),"supersedes":arr(ID)},
 "evidence": {"description":S,"kind":enum("analysis","experiment","benchmark","vendor-doc","financial-model","assumption"),"verificationStatus":enum("unverified","reviewed","validated","rejected"),"capturedAt":DATE,"reviewedBy":S,"limitations":S},
 "risks": {"description":S,"likelihood":enum("unknown","low","medium","high"),"impact":enum("low","medium","high","critical"),"evidenceRefs":arr(ID),"mitigationOptions":arr(),"status":enum("open","mitigated","closed"),"owner":S},
 "questions": {"dimensionId":ID,"question":S,"status":enum("open","answered","deferred"),"owner":S,"nextStep":S,"blocking":BOOL,"evidenceRefs":arr(ID)},
 "alternatives": {"description":S,"benefits":arr(),"drawbacks":arr(),"effortEstimate":S,"assumptions":arr(),"evidenceRefs":arr(ID),"verdict":enum("preferred","viable","rejected","unassessed")},
 "estimates": {"title":S,"category":enum("effort","cost","benefit"),"low":{"type":["number","null"],"minimum":0},"high":{"type":["number","null"],"minimum":0},"unit":enum("person-days","USD","USD/year"),"confidence":confidence,"assumptions":arr(),"evidenceRefs":arr(ID)},
 "gates": {"title":S,"status":enum("met","unmet","unknown"),"critical":BOOL,"rationale":S,"evidenceRefs":arr(ID)},
 "decisions": {"title":S,"status":enum("proposed","approved","rejected","deferred"),"owner":S,"dueOn":DATE,"rationale":S,"evidenceRefs":arr(ID)},
 "recommendations": {"conclusion":S,"rationale":S,"supportingFindings":arr(ID),"limitations":arr(),"decisionStatus":enum("pending","recommended","approved","rejected"),"stance":enum("pending","proceed","conditional-proceed","defer","do-not-proceed")},
 "activities": {"title":S,"status":enum("planned","in-progress","completed"),"owner":S,"nextStep":S,"evidenceRefs":arr(ID)}
}
collections={k:{"type":"object","propertyNames":ID,"additionalProperties":obj(common|v)} for k,v in fields.items()}
program=obj({"id":ID,"title":S,"subtitle":S,"owner":S,"scope":S,"exampleData":BOOL,"currentRecommendationId":ID})
schema={"$schema":"https://json-schema.org/draft/2020-12/schema","$id":"https://assessment-intelligence.local/schemas/assessment-v1.json","title":"Assessment State v1",**obj({"schemaVersion":{"const":"1.0"},"uiVersion":{"const":"1.0"},"asOf":DATE,"program":program,"executiveSummary":arr(),"sources":{"type":"object","additionalProperties":obj({"hash":S,"content":S})},**collections})}
root=Path(__file__).resolve().parents[1]
for p in [root/'schemas/assessment.schema.json',root/'assessment_intelligence/report.schema.json']:
 p.write_text(json.dumps(schema,indent=2)+'\n')
patch={"$schema":schema['$schema'],"title":"Restricted agent patch v1","type":"array","minItems":1,"maxItems":1000,"items":obj({"op":enum("add","replace","remove","test"),"path":{"type":"string","pattern":"^/(executiveSummary|program|dimensions|investigations|findings|evidence|risks|questions|alternatives|estimates|gates|decisions|recommendations|activities)(/[^/]+)*$"},"value":{}},["op","path"])}
patch['items']['allOf']=[{'if':{'properties':{'op':{'enum':['add','replace','test']}}},'then':{'required':['value']}}]
for p in [root/'schemas/patch.schema.json',root/'assessment_intelligence/patch.schema.json']:
 p.write_text(json.dumps(patch,indent=2)+'\n')
HASH={'type':'string','pattern':'^[a-f0-9]{64}$'}
period={'type':'string','pattern':'^[A-Za-z0-9][A-Za-z0-9_-]{0,63}$'}
envelope={'$schema':schema['$schema'],'title':'Assessment revision or approved snapshot v1',**obj({'hash':HASH,'parentHash':{'anyOf':[HASH,{'type':'null'}]},'state':schema,'provenance':obj({'actor':S,'operation':enum('ingest','records','patch','rollback'),'at':{'type':'string','format':'date-time'},'details':{'type':'object'}}),'id':period,'reportingPeriod':period,'createdAt':{'type':'string','format':'date-time'},'reviewer':S,'changeSummary':arr({'type':'object'})},['hash','parentHash','state','provenance'])}
envelope['allOf']=[{'if':{'required':['reportingPeriod']},'then':{'required':['id','reportingPeriod','createdAt','reviewer','changeSummary']}}]
for p in [root/'schemas/snapshot.schema.json',root/'assessment_intelligence/snapshot.schema.json']:
 p.write_text(json.dumps(envelope,indent=2)+'\n')
