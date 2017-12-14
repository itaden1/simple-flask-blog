import unittest, os, urllib
import main as blog

class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = blog.app.test_client()
        self.app.secret_key = b's3cr3t'
        self.app.testing = True

    #Test that all routes return 200
    def page_status_code(self, url):
        result = self.app.get(url, follow_redirects=True)
        return result.status_code

    def test_all_pages(self):
        scode = self.page_status_code('/blog')
        self.assertEqual(scode,200)
        scode = self.page_status_code('/admin')
        self.assertEqual(scode,200)
        scode = self.page_status_code('/login')
        self.assertEqual(scode,200)
        scode = self.page_status_code('/logout')
        self.assertEqual(scode,200)
    
    #Test Login
    def login(self, username, password):
        return self.app.post('/login', data=dict(username=username, password=password), follow_redirects=True)
    
    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def test_login_logout(self):
        rv = self.login('jon','pword')
        assert b'login failed' in rv.data
        rv = self.logout()
        assert b'Blog' in rv.data
        rv = self.login('username','pword')
        assert b'login failed' in rv.data
        rv = self.login('user','pass')
        assert b'username' in rv.data
        rv = self.logout()
        assert b'logged out' in rv.data

    def test_make_post(self):
        self.login('user','pass')
        result = self.app.get('/new-post')
        self.assertEqual(result.status_code,200)
        assert b'New Post' in result.data
        self.logout()

    def test_tag_post_rel(self):
        test_id = 1
        result = self.app.get('/view-post{}'.format(test_id),follow_redirects=True)
        self.assertEqual(result.status_code,200)

    def test_post_seearch_by_tag(self):
        test_id = 1
        result = self.app.get('/posts-by-tag{}'.format(test_id))
        self.assertEqual(result.status_code, 200)

    def test_save_post_del_post(self):
        rv = self.login('user','pass')
        assert b'username' in rv.data
        title = 'test title'
        draft = 1
        content = 'test content'
        tags = [1]
        result = self.app.post('/save-post',data=dict(title=title, content=content, draft=draft,tags=tags),follow_redirects=True)
        self.assertEqual(result.status_code,200)
        self.logout()

    def test_send_mail(self):
        result = self.app.post('/send-mail',data=dict(name='Bill',email='bill@bill.com',subject='test email',message='test email'))
        assert b'ERROR' in result.data

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
