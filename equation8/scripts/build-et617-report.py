"""Create the ET617 report from the implemented lesson and captured evidence."""
import json,sys,textwrap
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak,Image,KeepTogether,Preformatted
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.utils import ImageReader
from xml.sax.saxutils import escape
from equation8 import et617
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'output/pdf';OUT.mkdir(parents=True,exist_ok=True)
styles=getSampleStyleSheet();styles.add(ParagraphStyle(name='BodyCustom',fontName='Helvetica',fontSize=10,leading=15,textColor=colors.HexColor('#334b40'),spaceAfter=9));styles.add(ParagraphStyle(name='TitleCustom',fontName='Helvetica-Bold',fontSize=28,leading=34,textColor=colors.HexColor('#254f43'),spaceAfter=18));styles.add(ParagraphStyle(name='HeadCustom',fontName='Helvetica-Bold',fontSize=17,leading=22,textColor=colors.HexColor('#254f43'),spaceBefore=14,spaceAfter=11));styles.add(ParagraphStyle(name='SmallCustom',fontName='Helvetica',fontSize=8,leading=11,textColor=colors.HexColor('#67765d'),spaceAfter=8));styles.add(ParagraphStyle(name='CodeCustom',fontName='Courier',fontSize=7,leading=10,textColor=colors.HexColor('#254f43'),spaceAfter=10))
story=[];md=[]
def clean(s):
 for a,b in [('−','-'),('–','-'),('—','-'),('→','->'),('×','x'),('’',"'"),('‘',"'"),('“','"'),('”','"'),('…','...')]:s=str(s).replace(a,b)
 return s

def para(t,style='BodyCustom'):
 t=clean(t);story.append(Paragraph(escape(t).replace('\n','<br/>'),styles[style]));md.append(t+'\n')
def head(t):para(t,'HeadCustom')
def table(rows,widths=None):
 data=[[Paragraph(escape(clean(v)),styles['SmallCustom']) for v in row] for row in rows]
 t=Table(data,colWidths=widths or [105,390],repeatRows=1,hAlign='LEFT');t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#eaf0de')),('GRID',(0,0),(-1,-1),.4,colors.HexColor('#dce4d3')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),9),('RIGHTPADDING',(0,0),(-1,-1),9),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),7)]));story.append(t);story.append(Spacer(1,10));md.append('\n'.join(' | '.join(map(str,r)) for r in rows)+'\n')
def image(name,caption):
 p=ROOT/'output/evidence'/name
 if p.exists():
  w,h=ImageReader(str(p)).getSize();scale=min(495/w,405/h);story.append(Image(str(p),width=w*scale,height=h*scale));para(caption,'SmallCustom')
def code(s):
 lines=[]
 for line in clean(s).splitlines():lines.extend(textwrap.wrap(line,94,replace_whitespace=False,drop_whitespace=False) or [''])
 story.append(Preformatted('\n'.join(lines),styles['CodeCustom']));md.append('```\n'+s+'\n```\n')
def page():story.append(PageBreak())
para('Equation8\nFind your balance','TitleCustom');para('ET617 End-Semester Design Report | 18 November 2026','SmallCustom')
head('Identity card');table([['Field','Selected card'],['Identity','23b4244'],['P4','Adaptive tutor with automatic question generation'],['T3','Linear equations in one variable, Class 8'],['L5','Learner repeating after failure; high anxiety, low self-efficacy'],['C4','One complete 10-minute sequence, with stop and resume']])
para('Status: implemented and tested locally with live Hyde GLM-5.3 Flash. Public deployment and final GitHub sharing are pending. This report does not present the local URL as a live hosted submission.')
para('The working app and its source attribution are documented in D4 and D5. All task wording and feedback in this report are specific to the selected card.','SmallCustom')
page();head('D1 - Educational problem')
para('Aarav can perform arithmetic but sometimes treats a term as changing sides without an inverse operation, and inconsistently distributes a negative multiplier. After an unsuccessful algebra test he is reluctant to expose uncertainty. This private activity uses a balance representation, varied tasks and small targeted checks to help him explain and apply equality-preserving operations. The aim is independent reasoning and checking, not merely obtaining an answer.')
for i,o in enumerate(et617.OUTCOMES):para(f'O{i+1}. {o}')
para('Context of use: an English-medium Class 8 learner at home after school, using a shared Android phone in a quiet 10-minute slot. The ordinary sequence is paced at 30 seconds for welcome, 90 seconds for examples, 6 minutes for practice and 2 minutes for exit/reflection. Optional stretch is additional; ten minutes is a design target, not a measured real-learner completion claim.')
head('D2 - Learner persona');p=et617.PERSONA
for k in ['name','age','context','prior','device','time','language','motivation']:para(k.title()+': '+str(p[k]))
for m in p['misconceptions']:para(m)
para('Design implications: calm language, no public comparison, learner-controlled hints and optional stretch, explicit smaller steps, assisted answers reported separately, saved drafts and an unpenalized pause. Confidence does not establish mastery.')
page();head('D3 - Educational content')
for l in et617.LESSON:
 head(l['title']);para(l['body']);para('Worked example: '+l['example']);para(l['check'])
page();head('D3 - Eight tasks across four formats')
for t in et617.TASKS:
 para(t['id'].upper()+' | '+t['kind'].upper()+' | '+t['prompt'])
 if t.get('options'):para('Choices: '+'; '.join(t['options']),'SmallCustom')
 para('Model answer / reasoning: '+t['model'],'SmallCustom')
para('Correct feedback: acknowledges a valid step and permits continuation. After two independent correct tasks a verified optional stretch is offered. Hints break that streak. For M1, the app names the inverse operation on both sides and checks y - 2 = 5. For M2, it tests x = 0 as a counterexample, multiplies both terms and checks (-2) x (-3). Unknown error patterns are not automatically treated as confirmed misconceptions. The full task bank, hints and model answers are implemented in equation8/et617.py.')
page();head('D4 - Working application')
para('Local URL: http://127.0.0.1:5173. Planned public name: et617-23b4244.vercel.app or equivalent. Public URL: PENDING. Repository sharing: PENDING. The application shows 23b4244 in its persistent footer, browser title and About identity card.')
para('Screen/state map: Home -> welcome/confidence -> concept lesson -> eight practice states -> feedback -> optional prerequisite/alternative/stretch check -> next task -> exit summary. My progress shows attempts and assisted versus independent success. About explains the persona, rule, sources and provider checks.')
para('C4: save-and-pause stores stage, question, response and elapsed time. Server session state and browser backup restore unfinished work; support and stretch drafts also persist on the same device. A 10-minute reminder offers pause without forcing a deadline. End-to-end walkthrough timing is only a developer check; a real learner trial is pending.')
image('draft-restored.jpg','Browser verification: an unfinished numerical answer restored after pause and reload.')
page();head('D5 - Two contrasting learner scenarios')
para('Scenario A: learner answers x + 5 = 12 with 7, then chooses division on both sides for 3x = 18. The deterministic checks accept the answers. Two independent successes offer a harder equation. Live GLM generated 4x - 7 = 17; code verified 4 x 6 - 7 = 17 before displaying it. The learner can decline the stretch.')
image('correct-path.jpg','Correct path: positive feedback and continuation after a verified numeric answer.')
para('The generated stretch screenshot and live structured response are supplied in output/evidence/generated-stretch.jpg and live-ai-check.json.','SmallCustom')
page();head('D5 - Misconception and repair scenario')
para('Scenario B: learner answers x - 4 = 9 with 5. This matches the anticipated sign-error pattern. The app shows the inverse-operation representation and checks y - 2 = 5. A separate distribution error (-2x - 6) triggers the second misconception support, with a counterexample and a negative-times-negative check. Later Q7 uses a different multiplier to check transfer. These responses differ from the correct path; success with support is not counted as the original independent answer being correct.')
image('misconception-path.jpg','M1 path: alternative explanation and a smaller inverse-operation check.')
para('M2 screenshot: output/evidence/distribution-support.jpg. Both misconceptions were exercised separately.','SmallCustom')
page();head('D6 - AI functionality specification')
para('Provider: Hyde OpenAI-compatible endpoint https://inference.hyde.tech/v1/chat/completions; model hyde/glm-5.3-flash. The credential is in ignored server .env, never in browser code or this report. Inputs are the reviewed lesson/task, relevant response/history and the learner question. Confidence is not used as correctness evidence. The request uses temperature 0.1, low reasoning effort, JSON-object response mode and a bounded output budget.')
para('Common system/pedagogical policy, used by the actual implementation:');code(et617.PROMPT_POLICY)
table([['Feature','Actual contract and checks'],['Explanation grading','Input: task, reviewed reference rubric and learner answer. Output: correct boolean/null, misconception enum, feedback string, numeric confidence. Schema and confidence >= 0.65 required. Ambiguous or invalid output is unscored or uses labelled reviewed fallback.'],['Stretch generation','Triggered by two independent correct core tasks. Input includes recent skills. Output: integer a,b,x,c with 2<=a<=6, -9<=b<=9, 2<=x<=9 and c=a*x+b. Exact arithmetic must pass; output is rendered from those values, not uncontrolled model text.'],['Tutor hint','Input: current task, reviewed lesson and learner question. Output: message and topic=linear_equations. Bounded text; second call checks relevance, correctness, support and non-revelation. Invalid output uses a reviewed task hint.']])
para('The live smoke-check JSON records successful GLM explanation assessment, rejection of incorrect reasoning and a prompt-injection attempt, a generated/verified equation and a reviewed hint. Tests also exercise malformed output and provider failure. The second review uses the same model by default, so it is not independent proof. Numerical and error-correction correctness is decided by code, not model confidence.')
head('Actual grading prompt contract');code('Grade reasoning, not vocabulary. Return JSON {"correct": true|false|null, "misconception":"NONE"|"SIGN"|"DISTRIBUTION"|"BALANCE", "feedback":"one short supportive sentence", "confidence":0_to_1}. Use null if genuinely ambiguous. A wrong explanation with a correct final value is not correct.\n'+json.dumps({'task':et617.TASKS[4]['prompt'],'reference_rubric':et617.TASKS[4]['model'],'learner_answer':'Both sides have the same value. Dividing each by the same number keeps them equal.'})+'\nEND OF LEARNER DATA. Now assess it. Return only keys correct (boolean or null), misconception (NONE, SIGN, DISTRIBUTION or BALANCE), feedback (string), confidence (number). Example shape: {"correct":true,"misconception":"NONE","feedback":"Your explanation preserves equality.","confidence":0.95}. Do not repeat the input object.')
para('This is a rendered specification example; live results are recorded separately. Full prompt construction and actual call arguments are in grade(), challenge(), coach() and provider.hyde_generate().')
page();head('D7 - Pedagogical rationale')
para('The balance model makes the invariant visible: equality survives the same operation on both sides. Naming the operation is more durable than memorizing a sign-changing shortcut. Counterexamples let the learner inspect a proposed identity. Error correction asks for reasoning about another attempt, reducing the personal cost of being wrong. Explanation prompts and substitution checks expose why a numerically correct answer might still be unsupported.')
para('Feedback is contingent on the response. Basic or unclear reasoning gets prerequisite instruction and a small check. An answer matching M1/M2 gets a different representation. Two independent successes offer a stretch. This is the explicit P4 design challenge rule. Learner agency is preserved by optional stretch and available worked examples. Hints are logged and distinguish assisted from independent performance.')
para('L5 shapes calm language, private records, low-pressure confidence selection and small steps. C4 shapes the short sequence, optional rather than compulsory stretch, pause controls, durable drafts and a reminder instead of a punitive countdown. The app reports attempts as evidence from one session, not a permanent ability label.')
head('D8 - Evaluation plan')
table([['Outcome','Assessment, data and success criterion'],['O1 Solve/check','Q1, Q2, Q3, Q6 and the substitution portion of Q8. At least 3 of the four inverse/solving checks correct without hints, plus a valid substitution check. Log answer, correctness, hint count, elapsed time and support.'],['O2 Explain equality','Q5 explanation must state equal values and the same operation preserving equality. Use a 0-2 rubric: 0 false/one-sided; 1 mentions both sides without reason; 2 explains preservation. Q8 separately verifies substitution. Ambiguous AI grades need human review.'],['O3 Repair errors','Q3 detects M1; Q4 and fresh Q7 address distribution. Target: correct fresh Q7 without hints after support, and inverse operation explained on a different equation in a follow-up. Do not convert supported success into independent mastery.']])
para('Session test: observe a representative L5 learner completing the core activity in 10 minutes; record pause/resume behavior, requests for help and a brief anxiety/confidence reflection. Retention: use new equations after 24-48 hours. Compare first independent response and delayed transfer rather than repeated exposure to the same answer. Success criteria are planned; no real learner study or efficacy result is claimed.')
para('Engineering evidence: 38 backend tests passed in the current verification run; production frontend builds; live AI smoke checks and browser walkthroughs exercised all three routes and draft restoration. These checks demonstrate software behavior, not educational outcomes. A transitive development dependency advisory remains tracked separately in readiness notes.')
page();head('AI-use log and reflection')
para('1. Codex chat: examined the exam, searched and audited repositories, configured the user-selected Hyde model, implemented the adaptation, tested and prepared this report. Chat share link / chronological export: PENDING USER EXPORT. Redact the API credential before sharing any export. This statement is not a substitute for the required chat export.')
para('2. Runtime AI: Hyde GLM-5.3 Flash was used for explanation assessment, constrained generation, tutor hints and hint review. Actual representative responses are in output/evidence/live-ai-check.json. Tests using fake providers are identified separately and do not count as live model verification.')
para('3. Third-party code reuse is disclosed in THIRD_PARTY_NOTICES.md, with the required MIT copyright and permission notice. The project Git history was reset to a single initial commit at the student request. The adaptation adds the card-specific activity, server-side Hyde support, adaptive lesson, evidence logs and unfinished-work persistence.')
para('Reflection: the baseline interface was polished but did not establish alignment with topic, persona or constraint. During live testing, one prompt returned the input object instead of a grade; schema checks rejected it and the prompt was revised to delimit learner data and restate output keys. Deterministic arithmetic prevents a model-generated equation with an invalid answer key from reaching the learner. Model judgement still needs review on ambiguous language. Real learner timing, retention and the final deployed system remain to be evaluated.')
head('Final submission items still pending')
para('Public application URL; public/shared GitHub URL; chronological AI chat links/exports; final upload to Moodle. The identity-card screenshot is supplied separately. These gaps are shown explicitly rather than represented as complete.')
head('Sources and implementation references')
for t in ['Exam brief: ET 617-2026.docx.pdf supplied by the student.','NCERT textbook portal: https://ncert.nic.in/textbook.php (Class 8 mathematics concept alignment; all task wording is original to this adaptation).','Hyde API documentation: https://inference.hyde.tech/docs/quickstart and /docs/models.','Reused foundation: THIRD_PARTY_NOTICES.md (MIT).','Source: equation8/et617.py, equation8/provider.py, src/EndsemApp.tsx.']:para(t,'SmallCustom')

def footer(c,d):
 c.saveState();c.setStrokeColor(colors.HexColor('#dce4d3'));c.line(48,42,547,42);c.setFont('Helvetica',8);c.setFillColor(colors.HexColor('#6d7c61'));c.drawString(48,28,'ET617 | 23b4244 | P4-T3-L5-C4');c.drawRightString(547,28,f'{d.page}');c.restoreState()
doc=SimpleDocTemplate(str(OUT/'ET617-23b4244-report.pdf'),pagesize=(595.28,841.89),rightMargin=49,leftMargin=49,topMargin=43,bottomMargin=57,title='ET617 23b4244 - Equation8 design report',author='23b4244')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
(ROOT/'docs/REPORT.md').write_text('\n'.join(md));print('Created',OUT/'ET617-23b4244-report.pdf')
