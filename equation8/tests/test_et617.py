"""Card-specific checks: grading boundaries, adaptive branches and resume."""
import unittest
from unittest.mock import patch
from tests import test_api as api_fixture
from equation8 import et617,provider

class EndsemTests(api_fixture.ApiTests):
    def new(self):
        return self.client.post('/api/et617/sessions').json()
    def test_draft_and_pause_resume_without_keys(self):
        s=self.new();sid=s['id']
        self.client.patch('/api/et617/sessions/'+sid,json={'draft':'my unfinished reasoning','elapsed':91,'paused':True,'stage':'practice'})
        r=self.client.get('/api/et617/sessions/'+sid).json()
        self.assertEqual(r['draft'],'my unfinished reasoning');self.assertEqual(r['elapsed'],91);self.assertTrue(r['paused'])
        self.assertNotIn('answer',r['task']);self.assertNotIn('expected',r['task'])
    def test_all_three_adaptive_outcomes(self):
        t=et617.TASKS[2];fb,_=et617.feedback_for(t,'5',False,{'streak':0,'challenge_used':False})
        self.assertEqual(fb['route'],'alternative');self.assertEqual(fb['misconception'],'M1')
        fb,_=et617.feedback_for(et617.TASKS[0],'9',False,{'streak':0,'challenge_used':False});self.assertEqual(fb['route'],'prerequisite')
        fb,_=et617.feedback_for(t,'13',True,{'streak':2,'challenge_used':False});self.assertEqual(fb['route'],'harder')
    def test_sign_distribution_and_nonfinite_answers(self):
        self.assertFalse(et617.numeric('nan',7));self.assertFalse(et617.numeric('inf',7))
        self.assertTrue(et617.rubric_grade(et617.TASKS[3],'−2x + 6'))
        self.assertFalse(et617.rubric_grade(et617.TASKS[3],'-2x-6'))
    def test_hint_use_prevents_independent_streak(self):
        s=self.new();sid=s['id'];self.client.post('/api/et617/sessions/'+sid+'/hint')
        r=self.client.post('/api/et617/sessions/'+sid+'/answer',json={'answer':'7'}).json()
        self.assertEqual(r['streak'],0);self.assertEqual(r['attempts'][0]['hints'],1)
        duplicate=self.client.post('/api/et617/sessions/'+sid+'/answer',json={'answer':'7'})
        self.assertEqual(duplicate.status_code,409)
    def test_invalid_generated_equation_falls_back_and_hides_key(self):
        s=self.new();s['feedback']={'route':'harder'};et617.save(s)
        with patch.object(provider,'configured',return_value=True),patch.object(provider,'generate',return_value={'a':3,'b':1,'x':5,'c':999}):
            r=self.client.post('/api/et617/sessions/'+s['id']+'/challenge').json()
        self.assertIn('fallback',r['mode']);self.assertNotIn('expected',r)
        restored=self.client.get('/api/et617/sessions/'+s['id']).json();self.assertNotIn('expected',restored['challenge'])
    def test_uncertain_or_malformed_ai_cannot_create_mastery(self):
        with patch.object(provider,'configured',return_value=True),patch.object(provider,'generate',return_value={'correct':'true','misconception':'NONE','confidence':1,'feedback':'ok'}):
            result,mode,_=et617.grade(et617.TASKS[4],'I do not know')
        self.assertIsNone(result);self.assertIn('fallback',mode)
    def test_model_failure_uses_labelled_reviewed_support(self):
        s=self.new()
        with patch.object(provider,'generate',side_effect=provider.ProviderError('offline')):
            r=self.client.post('/api/et617/sessions/'+s['id']+'/coach',json={'question':'help'}).json()
        self.assertEqual(r['mode'],'Reviewed lesson fallback')
    def test_summary_cannot_skip_lesson(self):
        s=self.new();r=self.client.patch('/api/et617/sessions/'+s['id'],json={'stage':'summary'})
        self.assertEqual(r.status_code,400)
    def test_config_includes_card_and_roll(self):
        r=self.client.get('/api/et617/config').json();self.assertEqual(r['roll'],'23b4244');self.assertEqual(len(r['outcomes']),3)

# Reuse the isolated lifecycle without rerunning inherited baseline cases.
for _name in dir(api_fixture.ApiTests):
    if _name.startswith("test_") and _name not in EndsemTests.__dict__:
        setattr(EndsemTests, _name, None)
