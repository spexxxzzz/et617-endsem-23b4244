"""Exercise the stateless API across clients and reject edited checkpoints."""
import os
import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from equation8 import checkpoints
from api.index import app

class VercelTests(unittest.TestCase):
    def setUp(self):
        self.environment=patch.dict(os.environ,{'VERCEL':'1','SESSION_SECRET':'equation8-test-only-secret-not-for-production','HYDE_API_KEY':'','GEMINI_API_KEY':''})
        self.environment.start()
    def tearDown(self):self.environment.stop()
    def test_checkpoint_restores_after_function_restart(self):
        with TestClient(app) as c:
            s=c.post('/api/et617/sessions').json();sid=s['id'];token=s['session_token']
            self.assertNotIn('answer',s['task'])
            s=c.patch('/api/et617/sessions/'+sid,json={'session_token':token,'draft':'7','paused':True,'elapsed':55}).json()
        # New ASGI client represents a fresh function instance; no SQLite read needed.
        with TestClient(app) as c:
            r=c.post('/api/et617/sessions/'+sid+'/restore',json={'session_token':s['session_token']})
            self.assertEqual(r.status_code,200);s=r.json();self.assertEqual(s['draft'],'7');self.assertTrue(s['paused']);self.assertEqual(s['elapsed'],55)
            s=c.post('/api/et617/sessions/'+sid+'/answer',json={'session_token':s['session_token'],'answer':'7'}).json()
            self.assertTrue(s['feedback']['correct']);self.assertEqual(len(s['attempts']),1)
    def test_tampering_and_cross_session_use_are_rejected(self):
        with TestClient(app) as c:
            s=c.post('/api/et617/sessions').json();token=s['session_token'];sid=s['id']
            bad=token[:30]+('A' if token[30]!='A' else 'B')+token[31:]
            self.assertEqual(c.post('/api/et617/sessions/'+sid+'/restore',json={'session_token':bad}).status_code,400)
            self.assertEqual(c.post('/api/et617/sessions/other-session/restore',json={'session_token':token}).status_code,404)
    def test_key_rotation_invalidates_old_checkpoint(self):
        state={'id':'sample','draft':'private answer'};token=checkpoints.seal(state)
        self.assertNotIn('private answer',token)
        with patch.dict(os.environ,{'SESSION_SECRET':'different-encryption-secret'}):
            with self.assertRaises(Exception):checkpoints.unseal(token)
