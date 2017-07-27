from __future__ import absolute_import, print_function

import os
import unittest

def print_importers():
    import sys
    import pprint

    print('PATH:'),
    pprint.pprint(sys.path)
    print()
    print('IMPORTERS CACHE: {')
    for name, cache_value in sys.path_importer_cache.items():
        name = name.replace(sys.prefix, '...')
        print('%s: %r' % (name, cache_value))
    print('}')


def print_importers_of(module):
    import sys
    import pprint

    print('MODULE:'),
    pprint.pprint(module)
    mod_path = module.__file__.split(os.sep)
    print()
    print('IMPORTERS USED: {')
    for i in range(len(mod_path)-1):
        parpath = os.sep.join(mod_path[:len(mod_path) - i])
        if parpath in sys.path_importer_cache:
            cached_imp = sys.path_importer_cache[parpath]
            parpath = parpath.replace(sys.prefix, '...')
            print('%s: %r' % (parpath, cached_imp))
    print('}')


class BaseMsgTestCase(unittest.TestCase):

    def assert_test_message_classes(self, TestMsg, TestMsgDeps, TestRosMsgDeps, TestRosMsg):
        self.assertTrue(TestMsg is not None)
        self.assertTrue(callable(TestMsg))
        self.assertTrue(TestMsg._type == 'tests/TestMsg')  # careful between ros package name and python package name

        self.assertTrue(TestMsgDeps is not None)
        self.assertTrue(callable(TestMsgDeps))
        self.assertTrue(
            TestMsgDeps._type == 'tests/TestMsgDeps')  # careful between ros package name and python package name

        # use it !
        self.assertTrue(TestMsg(test_bool=True, test_string='Test').test_bool)

        self.assertTrue(TestMsgDeps(
            test_bool=True,
            #test_std_bool=True,  # implicit import of std_msgs
            test_ros_deps=TestRosMsgDeps(  # dependency imported
                #test_ros_std_bool=True,  # implicit import of std_msgs
                test_ros_msg=TestRosMsg(test_ros_bool=True)  # dependency of dependency
            )))

    def assert_std_message_classes(self, Bool, Header):
        import genpy

        self.assertTrue(Bool is not None)
        self.assertTrue(callable(Bool))
        self.assertTrue(Bool._type == 'std_msgs/Bool')

        # A more complex message type
        self.assertTrue(Header is not None)
        self.assertTrue(callable(Header))
        self.assertTrue(Header._type == 'std_msgs/Header')

        # use it !
        self.assertTrue(Bool(True))
        self.assertTrue(Header(seq=42, stamp=genpy.Time(secs=21, nsecs=7), frame_id=0))


class BaseSrvTestCase(unittest.TestCase):
    def assert_test_service_classes(self,
                                    TestSrv, TestSrvRequest, TestSrvResponse,
                                    TestSrvDeps, TestSrvDepsRequest, TestSrvDepsResponse,
                                    TestRosMsgDeps, TestRosMsg):
        self.assertTrue(TestSrv is not None)
        self.assertTrue(callable(TestSrv))
        self.assertTrue(
            TestSrv._type == 'tests/TestSrv')  # careful between ros package name and python package name

        self.assertTrue(TestSrvRequest is not None)
        self.assertTrue(callable(TestSrvRequest))
        self.assertTrue(
            TestSrvRequest._type == 'tests/TestSrvRequest')  # careful between ros package name and python package name

        self.assertTrue(TestSrvResponse is not None)
        self.assertTrue(callable(TestSrvResponse))
        self.assertTrue(
            TestSrvResponse._type == 'tests/TestSrvResponse')  # careful between ros package name and python package name

        # use it !
        self.assertTrue(TestSrvRequest(test_request='Test').test_request)
        self.assertTrue(TestSrvResponse(test_response=True).test_response)

        self.assertTrue(TestSrvDeps is not None)
        self.assertTrue(callable(TestSrvDeps))
        self.assertTrue(
            TestSrvDeps._type == 'tests/TestSrvDeps')  # careful between ros package name and python package name

        self.assertTrue(TestSrvDepsRequest is not None)
        self.assertTrue(callable(TestSrvDepsRequest))
        self.assertTrue(
            TestSrvDepsRequest._type == 'tests/TestSrvDepsRequest')  # careful between ros package name and python package name

        self.assertTrue(TestSrvDepsResponse is not None)
        self.assertTrue(callable(TestSrvDepsResponse))
        self.assertTrue(
            TestSrvDepsResponse._type == 'tests/TestSrvDepsResponse')  # careful between ros package name and python package name

        # use it !
        self.assertTrue(TestSrvDepsRequest(
            test_request='Test',
            test_ros_deps=TestRosMsgDeps(  # dependency imported
                #test_ros_std_bool=True,  # implicit import of std_msgs
                test_ros_msg=TestRosMsg(test_ros_bool=True)  # dependency of dependency
            )))
        self.assertTrue(TestSrvDepsResponse(
            test_response='Test',
            #test_std_bool=True,  # implicit import of std_msgs
        ))

    def assert_std_service_classes(self, SetBool, SetBoolRequest, SetBoolResponse):
        self.assertTrue(SetBool is not None)
        self.assertTrue(callable(SetBool))
        self.assertTrue(SetBool._type == 'std_srvs/SetBool')

        self.assertTrue(SetBoolRequest is not None)
        self.assertTrue(callable(SetBoolRequest))
        self.assertTrue(SetBoolRequest._type == 'std_srvs/SetBoolRequest')

        self.assertTrue(SetBoolResponse is not None)
        self.assertTrue(callable(SetBoolResponse))
        self.assertTrue(SetBoolResponse._type == 'std_srvs/SetBoolResponse')

        # use it !
        self.assertTrue(SetBoolRequest(data=True).data)
        self.assertTrue(SetBoolResponse(success=True, message='Test').success)