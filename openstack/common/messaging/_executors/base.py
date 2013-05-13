# Copyright 2013 New Dream Network, LLC (DreamHost)
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import abc
import sys

from openstack.common.gettextutils import _
from openstack.common import log as logging

_LOG = logging.getLogger(__name__)


class ExecutorBase(object):

    __metaclass__ = abc.ABCMeta

    def __init__(self, conf, listener, callback):
        self.conf = conf
        self.listener = listener
        self.callback = callback

    def _process_one_message(self):
        (ctxt, message) = self.listener.poll()
        try:
            reply = self.callback(ctxt, message)
            if reply:
                self.listener.reply(ctxt, reply)
        except Exception:
            # sys.exc_info() is deleted by LOG.exception().
            exc_info = sys.exc_info()
            _LOG.error(_("Failed to process message... skipping it."),
                       exc_info=exc_info)
            self.listener.reply(failure=exc_info)
        finally:
            self.listener.done(ctxt, message)

    @abc.abstractmethod
    def start(self):
        pass

    @abc.abstractmethod
    def stop(self):
        pass

    @abc.abstractmethod
    def wait(self):
        pass
