import unittest
import vpnlist
import tempfile
import os

class VPNTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, vpnlist.app.config['DATABASE'] = tempfile.mkstemp()
        vpnlist.app.config['TESTING'] = True
        self.app = vpnlist.app.test_client()
        vpnlist.init_db('schema.sql')

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(vpnlist.app.config['DATABASE'])

    def test_empty_db(self):
        response = self.app.get('/?lat=0&lng=0')
        assert response.data == ''

    def test_invalid_lat_list(self):
        response = self.app.get('/?la=0&lng=9')
        assert 'Invalid latitude' in response.data

    def test_invalid_lng_list(self):
        response = self.app.get('/?lat=0&lng=')
        assert 'Invalid longitude' in response.data
    
    def test_add_list_vpn(self):
        for i in range(0,10):
            for j in range(0,10):
                response = self.app.get('/addvpn?name=testvpn{0}{1}&lng={0}&lat={1}'.format(i,j))
                assert 'Added vpn: testvpn{0}{1},{0},{1}'.format(i,j) in response.data

        response = self.app.get('/?lng=0&lat=0')
        for i in range(0,10):
            for j in range(0,10):
                assert 'testvpn{0}{1}'.format(i,j) in response.data

    def test_invalid_name_add_vpn(self):
        response = self.app.get('/addvpn?lng=5&lat=5')
        assert 'Name of VPN not found in query' in response.data

    def test_invalid_lng_add_vpn(self):
        response = self.app.get('/addvpn?name=testvpn35lng=&lat=5')
        assert 'Invalid longitude' in response.data

    def test_invalid_lat_add_vpn(self):
        response = self.app.get('/addvpn?name=testvpn35&lng=5&lat=')
        assert 'Invalid latitude' in response.data
        
    def test_add_del_vpn(self):
        for i in range(0,10):
            for j in range(0,10):
                response = self.app.get('/addvpn?name=testvpn{0}{1}&lng={0}&lat={1}'.format(i,j))
                assert 'Added vpn: testvpn{0}{1},{0},{1}'.format(i,j) in response.data

        for i in range(0,10):
            for j in range(0,10):
                response = self.app.get('/delvpn?name=testvpn{0}{1}'.format(i,j))
                assert 'Deleted vpn: testvpn{0}{1}'.format(i,j) in response.data
    
    def test_invalid_del_vpn1(self):
        response = self.app.get('/delvpn?name=NOTFOUND')
        assert 'No such vpn' in response.data

    def test_invalid_del_vpn2(self):
        response = self.app.get('/delvpn')
        assert 'Name of VPN not found in query' in response.data

if __name__ == '__main__':
    unittest.main()
