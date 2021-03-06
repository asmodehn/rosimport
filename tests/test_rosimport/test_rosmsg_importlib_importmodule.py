from __future__ import absolute_import, division, print_function
"""
Testing dynamic import with importlib
"""

import os
import sys
import runpy
import logging.config

logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(asctime)s %(levelname)s %(name)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        }
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
})

# Relying on basic unittest first, to be able to easily switch the test framework in case of import conflicts.
import unittest

# Ref : http://stackoverflow.com/questions/67631/how-to-import-a-module-given-the-full-path

import importlib
import site
# Importing importer module
import rosimport

# importlib
# https://pymotw.com/3/importlib/index.html
# https://pymotw.com/2/importlib/index.html

#
# Note : we cannot assume anything about import implementation (different python version, different version of pytest)
# => we need to test them all...
#


from ._utils import (
    print_importers,
    BaseMsgTestCase,
    BaseSrvTestCase,
)



class TestImportLibMsg(BaseMsgTestCase):
    rosdeps_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'rosdeps')

    rosimporter = rosimport.RosImporter()

    @classmethod
    def setUpClass(cls):
        # This is used for message definitions, not for python code
        site.addsitedir(cls.rosdeps_path)
        cls.rosimporter.__enter__()

    @classmethod
    def tearDownClass(cls):
        cls.rosimporter.__exit__(None, None, None)

    @unittest.skipIf(not hasattr(importlib, 'import_module'), reason="importlib does not have attribute import_module")
    def test_importlib_importmodule_absolute_msg(self):
        # Verify that files exists and are dynamically importable
        std_msgs = importlib.import_module('std_msgs.msg')

        self.assert_std_message_classes(std_msgs.Bool, std_msgs.Header)

        if hasattr(importlib, 'reload'):  # recent version of importlib
            # attempting to reload
            importlib.reload(std_msgs)
        else:
            pass

        assert std_msgs is not None

    @unittest.skipIf(not hasattr(importlib, 'import_module'),
                     reason="importlib does not have attribute import_module")
    def test_importlib_importmodule_absolute_class_raises(self):
        with self.assertRaises(ImportError):
            importlib.import_module('std_msgs.msg.Bool')

    @unittest.skipIf(not hasattr(importlib, 'import_module'), reason="importlib does not have attribute import_module")
    def test_importlib_importmodule_relative_msg(self):

        assert __package__
        # Verify that files exists and are dynamically importable
        test_msgs = importlib.import_module('.msg', package=__package__)

        self.assert_test_message_classes(test_msgs.TestMsg, test_msgs.TestMsgDeps, test_msgs.TestRosMsgDeps, test_msgs.TestRosMsg)

        if hasattr(importlib, 'reload'):  # recent version of importlib
            # attempting to reload
            importlib.reload(test_msgs)
        else:
            pass

        assert test_msgs is not None

    @unittest.skipIf(not hasattr(importlib, 'import_module'), reason="importlib does not have attribute import_module")
    def test_importlib_importmodule_relative_msg_from_absolute(self):

        assert __package__
        # Verify that files exists and are dynamically importable
        test_msgs = importlib.import_module('test_rosimport.msg')

        self.assert_test_message_classes(test_msgs.TestMsg, test_msgs.TestMsgDeps, test_msgs.TestRosMsgDeps, test_msgs.TestRosMsg)

        if hasattr(importlib, 'reload'):  # recent version of importlib
            # attempting to reload
            importlib.reload(test_msgs)
        else:
            pass

        assert test_msgs is not None

    @unittest.skipIf(not hasattr(importlib, 'import_module'),
                     reason="importlib does not have attribute import_module")
    def test_importlib_importmodule_relative_class_raises(self):

        assert __package__
        with self.assertRaises(ImportError):
            importlib.import_module('.msg.TestMsg', package=__package__)

    # TODO
    # def test_double_import_uses_cache(self):  #
    #     print_importers()
    #     # Verify that files exists and are importable
    #     import std_msgs.msg as std_msgs
    #
    #     self.assertTrue(std_msgs.Bool is not None)
    #     self.assertTrue(callable(std_msgs.Bool))
    #     self.assertTrue(std_msgs.Bool._type == 'std_msgs/Bool')
    #
    #     import std_msgs.msg as std_msgs2
    #
    #     self.assertTrue(std_msgs == std_msgs2)


class TestImportLibSrv(BaseSrvTestCase):

    ros_comm_msgs_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'rosdeps', 'ros_comm_msgs')
    # For dependencies
    rosdeps_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'rosdeps')

    rosimporter = rosimport.RosImporter()

    @classmethod
    def setUpClass(cls):
        # This is used for message definitions, not for python code
        site.addsitedir(cls.rosdeps_path)
        site.addsitedir(cls.ros_comm_msgs_path)
        cls.rosimporter.__enter__()

    @classmethod
    def tearDownClass(cls):
        cls.rosimporter.__exit__(None, None, None)

    @unittest.skipIf(not hasattr(importlib, 'import_module'), reason="importlib does not have attribute import_module")
    def test_importlib_importmodule_absolute_srv(self):
        # Verify that files exists and are dynamically importable
        std_srvs = importlib.import_module('std_srvs.srv')

        self.assert_std_service_classes(std_srvs.SetBool, std_srvs.SetBoolRequest, std_srvs.SetBoolResponse)

        if hasattr(importlib, 'reload'):  # recent version of importlib
            # attempting to reload
            importlib.reload(std_srvs)
        else:
            pass

        assert std_srvs is not None

    @unittest.skipIf(not hasattr(importlib, 'import_module'),
                     reason="importlib does not have attribute import_module")
    def test_importlib_importmodule_absolute_class_raises(self):
        with self.assertRaises(ImportError):
            importlib.import_module('std_srvs.srv.SetBool')

    @unittest.skipIf(not hasattr(importlib, 'import_module'), reason="importlib does not have attribute import_module")
    def test_importlib_importmodule_relative_srv(self):

        assert __package__
        # Verify that files exists and are dynamically importable
        test_srvs = importlib.import_module('.srv', package=__package__)
        test_msgs = importlib.import_module('.msg', package=__package__)

        self.assert_test_service_classes(test_srvs.TestSrv, test_srvs.TestSrvRequest, test_srvs.TestSrvResponse,
                                         test_srvs.TestSrvDeps, test_srvs.TestSrvDepsRequest, test_srvs.TestSrvDepsResponse,
                                         test_msgs.TestRosMsgDeps, test_msgs.TestRosMsg)

        if hasattr(importlib, 'reload'):  # recent version of importlib
            # attempting to reload
            importlib.reload(test_srvs)
        else:
            pass

        assert test_srvs is not None

    @unittest.skipIf(not hasattr(importlib, 'import_module'), reason="importlib does not have attribute import_module")
    def test_importlib_importmodule_relative_srv_from_absolute(self):

        assert __package__
        # Verify that files exists and are dynamically importable
        test_srvs = importlib.import_module('test_rosimport.srv')
        test_msgs = importlib.import_module('test_rosimport.msg')

        self.assert_test_service_classes(test_srvs.TestSrv, test_srvs.TestSrvRequest, test_srvs.TestSrvResponse,
                                         test_srvs.TestSrvDeps, test_srvs.TestSrvDepsRequest, test_srvs.TestSrvDepsResponse,
                                         test_msgs.TestRosMsgDeps, test_msgs.TestRosMsg)

        if hasattr(importlib, 'reload'):  # recent version of importlib
            # attempting to reload
            importlib.reload(test_srvs)
        else:
            pass

        assert test_srvs is not None

    @unittest.skipIf(not hasattr(importlib, 'import_module'),
                     reason="importlib does not have attribute import_module")
    def test_importlib_importmodule_relative_class_raises(self):

        assert __package__
        with self.assertRaises(ImportError):
            importlib.import_module('.srv.TestSrv', package=__package__)

    # TODO
    # def test_double_import_uses_cache(self):  #
    #     print_importers()
    #     # Verify that files exists and are importable
    #     import std_msgs.msg as std_msgs
    #
    #     self.assertTrue(std_msgs.Bool is not None)
    #     self.assertTrue(callable(std_msgs.Bool))
    #     self.assertTrue(std_msgs.Bool._type == 'std_msgs/Bool')
    #
    #     import std_msgs.msg as std_msgs2
    #
    #     self.assertTrue(std_msgs == std_msgs2)




if __name__ == '__main__':
    import pytest
    pytest.main(['-s', '-x', __file__, '--boxed'])
