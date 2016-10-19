#
# The BSD License (BSD)
#
# Copyright (c) 2016 Tintri, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.

# 3. Neither the name of the copyright holder nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#     without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#

__author__ = 'Tintri'
__copyright__ = 'Copyright 2016 Tintri Inc'
__license__ = 'BSD'
__version__ = '1.0'

import logging
import requests
import json
import types
import urllib
import inspect

TINTRI_LOG_LEVEL_DATA = 5
DEFAULT_LOGGER_NAME = 'tintri'
DEFAULT_API_VERSION = '310'

from .utils import map_to_object, object_to_json, TintriJSONEncoder

class TintriError(Exception):
    """
    Base class of all Tintri specific exceptions
    
    Args:
        cause (str): Error cause
        message (str) : Error message
        details (str): Error details
    """
    def __init__(self, cause=None, message=None, details=None):
        self.cause = cause
        self.message = message
        self.details = details
        Exception.__init__(self, cause, message, details)

class TintriServerError(TintriError):
    """
    Exception returned from Tintri server (VMstore or TGC)
    
    Args:
        status (int): HTTP status code from a REST call
        code (str): Tintri error code
        details (str): Error details 
    """
    def __init__(self, status, code=None, cause=None, message=None, details=None):
        self.status = status
        self.code = code
        TintriError.__init__(self, cause=cause, message=message, details=details)

class TintriBadRequestError(TintriServerError):
    """
    Tintri bad request error (HTTP status code: 400)
    
    Args:
        cause (str): Error cause
        message (str) : Error message
        details (str): Error details
    """
    def __init__(self, code, message, details):
        TintriServerError.__init__(self, 400, code=code, message=message, details=details)    

class TintriInvalidSessionError(TintriServerError):
    """
    Tintri invalid session error (HTTP status code: 401)
    
    Args:
        cause (str): Error cause
        message (str) : Error message
        details (str): Error details
    """
    def __init__(self, code, message, details):
        TintriServerError.__init__(self, 401, code=code, message=message, details=details)

class TintriAuthenticationError(TintriServerError):
    """
    Tintri authentication error (HTTP status code: 403)
    
    Args:
        cause (str): Error cause
        message (str) : Error message
        details (str): Error details
    """
    def __init__(self, code, message, details):
        TintriServerError.__init__(self, 403, code=code, message=message, details=details)

class TintriAuthorizationError(TintriServerError):
    """
    Tintri authorization error (HTTP status code: 403)
    
    Args:
        cause (str): Error cause
        message (str) : Error message
        details (str): Error details
    """
    def __init__(self, code, message, details):
        TintriServerError.__init__(self, 403, code=code, message=message, details=details)

class TintriAPINotFoundError(TintriServerError):
    """
    Tintri APi not found error (HTTP status code: 404)
    
    Args:
        cause (str): Error cause
        message (str) : Error message
        details (str): Error details
    """
    def __init__(self, code, message, details):
        TintriServerError.__init__(self, 404, code=code, message=message, details=details)

class TintriInternalError(TintriServerError):
    """
    Tintri internal error (HTTP status code: 500)
    
    Args:
        cause (str): Error cause
        message (str) : Error message
        details (str): Error details
    """
    def __init__(self, code, message, details):
        TintriServerError.__init__(self, 500, code=code, message=message, details=details)

class TintriPage(object):
    def __init__(self, paginated=False, auto_page=False, items=None, context={}):
        if paginated:
            json_context = json.loads(context['response_data'])
            self.__total = json_context['total'] if 'total' in json_context else None
            self.__limit = json_context['limit'] if 'limit' in json_context else None
            self.__offset = json_context['offset'] if 'offset' in json_context else None
            self.__page_number = json_context['page'] if 'page' in json_context else None
            self.__next = json_context['next'] if 'next' in json_context else None
            self.__prev = json_context['prev'] if 'prev' in json_context else None
            self.__absoluteTotal = json_context['absoluteTotal'] if 'absoluteTotal' in json_context else None
            self.__filteredTotal = json_context['filteredTotal'] if 'filteredTotal' in json_context else None
            self.__pageTotal = json_context['pageTotal'] if 'pageTotal' in json_context else None
            self.__completedIn = json_context['completedIn'] if 'completedIn' in json_context else None
            self.__lastUpdatedTime = json_context['lastUpdatedTime'] if 'lastUpdatedTime' in json_context else None
            self.__offsetMatchFound = json_context['offsetMatchFound'] if 'offsetMatchFound' in json_context else None
            self.__overflow = json_context['overflow'] if 'overflow' in json_context else None

        self.__is_paginated = paginated
        self.__auto_page = auto_page
        self.__items = items
        self.__num_items = len(self.__items)

        self.__next_page = None
        self.__prev_page = None
        self.__url = context['url']
        self.__request_class = context['request_class']
        self.__path_params = context['path_params']
        self.__response_class = context['response_class']
        self.__func = context['func']
        self.__current = 0
        self.__cur_page = self

    @property
    def limit(self):
        if self.__is_paginated:
            return self.__limit
        return len(self.__items)

    @property
    def offset(self):
        if self.__is_paginated:
            return self.__offset
        return 0

    @property
    def page_number(self):
        """Current page number"""
        if self.__is_paginated:
            return self.__page_number
        return 0

    @property
    def total(self):
        """Total number of active objects across all pages"""
        if self.__is_paginated:
            return self.__total
        return len(self.__items)

    @property
    def absoluteTotal(self):
        """Absolute number of requested objects without any qualifications including filtering, active, or deleted"""
        return self.__absoluteTotal

    @property
    def filteredTotal(self):
        """Number of objects as specified by filter. If no filter was requested, it would be same as total"""
        return self.__filteredTotal

    @property
    def pageTotal(self):
        """Total number of pages"""
        return self.__pageTotal

    @property
    def completedIn(self):
        """Time in milliseconds indicating how long it took to serve the request"""
        return self.__completedIn

    @property
    def lastUpdatedTime(self):
        """Time when the page was accessed"""
        return self.__lastUpdatedTime

    @property
    def offsetMatchFound(self):
        """Indicates if requested item(s) is/are found"""
        return self.__offsetMatchFound

    @property
    def overflow(self):
        """Flag giving notice the amount of data did not fit into the given specified or default offset"""
        return self.__overflow

    def __len__(self):
        """Length of the page is number of items in page"""
        return self.__num_items

    def __iter__(self):
        # reset current value
        self.__cur_page.__current = 0
        return self

    def next(self):
        """Iterates items in page along with navigating to next page"""
        if self.__is_paginated:
            if self.__cur_page.__current == self.__cur_page.__num_items:
                if self.__cur_page.__next is None:
                    # raise StopIteration on iterating the last item
                    # reset current page
                    self.__cur_page = self
                    raise StopIteration()
                else:
                    if self.__auto_page:
                        # retrieve next page
                        self.__cur_page = self.__cur_page.get_next_page()
                        # 49878
                        if len(self.__cur_page) == 0:
                            self.__cur_page = self
                            raise StopIteration()
                    else:
                        raise StopIteration()
            # retrieve item from the current page
            self.__cur_page.__current += 1
            return self.__cur_page.__items[self.__cur_page.__current - 1]
        else:
            if self.__cur_page.__current < self.total:
                self.__cur_page.__current += 1
                return self.__items[self.__cur_page.__current - 1]
            else:
                # raise StopIteration on iterating the last item
                raise StopIteration()

    def __getitem__(self, idx):
        """Return an item within a page if index is valid"""
        if idx >= self.__num_items:
            raise IndexError()
        return self.__items[idx]

    def get_next_page(self):
        """Return next page if it exists"""
        if self.__next:
            if self.__next_page:
                self.__next_page.__current = 0
                return self.__next_page
            else:
                q_p_string = self.__next.split("&")
                q_p = {}
                for item in q_p_string:
                    temp = item.split("=")
                    q_p[temp[0]] = temp[1]
                self.__next_page = self.__func(path_params=self.__path_params, query_params=q_p, request_class=self.__request_class, response_class=self.__response_class)
                return self.__next_page
        raise StopIteration()

    def get_prev_page(self):
        """Return previous page if it exists"""
        if self.__prev:
            if self.__prev_page:
                self.__prev_page.__current = 0
                return self.__prev_page
            else:
                q_p_string = self.__prev.split("&")
                q_p = {}
                for item in q_p_string:
                    temp = item.split("=")
                    q_p[temp[0]] = temp[1]
                self.__prev_page = self.__func(path_params=self.__path_params, query_params=q_p, request_class=self.__request_class, response_class=self.__response_class)
                return self.__prev_page
        raise StopIteration()

class TintriObject(object):
    """Base class for Tintri serializable classes"""
    typeId = None
    _property_map = {}
    _is_paginated = False

    def __init__(self):
        if hasattr(self.__class__, 'typeId'):
            self.typeId = self.__class__.typeId

    def _tostr(self): return '%s %s' % (self.__class__.__name__, object_to_json(self))
    def __str__(self): return self._tostr() # default str() using json format

class TintriEntity(TintriObject):
    """
    Base class for Tintri REST resources
    """
    _requires_auth = True
    _ignores_setattr = True
    _is_singleton = False
    _url = None

#     @classmethod
#     def _from_json(cls, text):
#         m = json.loads(text)
#         return map_to_object(m, cls)

    # def __init__(self):
    #     super(TintriEntity, self).__init__()
    #     if hasattr(self.__class__, 'typeId'):
    #         self.typeId = self.__class__.typeId

    # watch dog for setting illegal attributes
    def __setattr__(self, name, value):
        if hasattr(self, name) or not hasattr(self, '_ignores_setattr') or self._ignores_setattr:
            object.__setattr__(self, name, value)
        else:
            caller = inspect.stack()[1]
            if caller[3] == '__init__': # not constructor
                object.__setattr__(self, name, value)
            else:
                raise TypeError('Setting attribute %r on object of type %s is not allowed' % (name, self.__class__.__name__))

class Version(TintriObject):
    """Version class of a Tintri server across all Tintri API versions """
    _url = 'https://%s/api/info'
    _requires_auth = False

# class ObjectListBase(object):
#     """Abstract base class for object list retuned from a Tintri server"""
#     def __iter__(self):
#         raise NotImplementedError("Please Implement this method")
    
class TintriBase(object):
    """
    A version-independent Tintri base class. This class should not be instantiated; only extended sublcasses should be instantiated.
    """
    method_registry = {}

    def __init__(self, host, username=None, password=None, api_version=DEFAULT_API_VERSION, logger_name=DEFAULT_LOGGER_NAME, auto_login=True, disable_cert_warning=True, custom_client_header=None, auto_page=True):
        # Stored variables across login sessions
        self.__host = host
        self.__username = username
        self.__password = password

        self.__api_version = api_version
        self.__logger_name = logger_name
        self.__auto_login = auto_login
        self.__custom_client_header = custom_client_header

        self.__init_logging()

        if disable_cert_warning:
            import requests.packages.urllib3
            requests.packages.urllib3.disable_warnings()

        # Per-session initialization, also called after logging out
        self.__init_per_session_vars()
        # flag to paginate items if not already done by API
        # for items that are paged, this flag is used to navigate to next page
        self.__auto_page = auto_page

    def __init_per_session_vars(self):
        self.__version = None # device version
        self.__session_id = None

    def __init_logging(self):
        try: # To avoid "No handler found" warnings for Python version < 2.7
            from logging import NullHandler
        except ImportError:
            class NullHandler(logging.Handler):
                def emit(self, record): pass

        self.__logger = logging.getLogger(self.__logger_name)
        self.__logger.addHandler(NullHandler()) # defaults to the do-nothing NullHandler
        #self.__logger.setLevel(logging.INFO) # defaults to logging.INFO

        # Logger test messages
        #self.__logger.debug('debug message')
        #self.__logger.info('info message')
        # self.__logger.warn('warn message')
        # self.__logger.error('error message')
        # self.__logger.critical('critical message')

    @property # read only
    def host(self):
        """
        Tintri Server host provided by user
            
        Returns:
            str: Host name or IP address
        """
        return self.__host
    
    @property # read only
    def username(self):
        """
        Session username if user chose to cache
        
        Returns:
            str: username
        """
        return self.__username

    @property # read only
    def password(self):
        """
        Session password if user chose to cache
        
        Returns:
            str: password
        """
        return self.__password

    @property # read only
    def api_version(self):
        """
        API version provided by user, default value=v310
        
        Returns:
            str: API version
        """
        return self.__api_version

#     @api_version.setter
#     def api_version(self, api_version):
#         if api_version != self.__api_version:
#             self.__api_version = api_version
#             self.__register_entities()

    @property # read only
    def auto_login(self):
        """
        Specifies if session should auto-login in the event of session expiry, default value=True
        
        Returns:
            bool: auto_login
        """
        return self.__auto_login

    @property # read only
    def custom_client_header(self):
        """
        Value associated with 'Tintri-Api-Client' key in REST API header, default value=Tintri-PythonSDK-<PySdkVersion>
        
        Returns:
            str: Custom client header
        """
        return self.__custom_client_header
    
    @property # read only
    def logger_name(self):
        """
        Logger name provided by user
        
        Returns:
            str: logger name
        """
        return self.__logger_name
    
    @property # read only
    def logger(self):
        """
        Logger object used for logging 
        
        Returns:
            Logger: logger object
        
        """
        return self.__logger

    @property # read only
    def session_id(self):
        """
        Session ID
        
        Returns:
            str: Session ID
        """
        return self.__session_id

    @property # read only
    def version(self):
        """
        Information found in `RestApi` about API supported by server
        
        Returns:
            `RestApi`: `RestApi` object
        """
        return self.__get_version()

    @property # read only
    def auto_page(self):
        """
        auto_page flag is used to change the behavior of pagination as desired, default value=True
        
        ===============    =========    ================    ======================================================================================
        Server Response    auto_page    API Return value             Pagination
        ===============    =========    ================    ======================================================================================
             List            True            Page           No pagination as there is single page
             List            False           List           Not applicable
             Page            True            Page           On item iteration, Automatically fetches next page
             Page            False           Page           Item iteration stops at current page, user has to manually fetch next or previous page
        ===============    =========    ================    ======================================================================================

        Returns:
            bool: auto_page
        """
        return self.__auto_page

    def get_rest_methods(self):
        methods = [] + self.method_registry.keys()
        methods.sort()
        return methods

    def __get_version(self):
        if not self.__version:
            headers = {'content-type': 'application/json'}
            versionUrl = 'https://%s/api/info' % self.host
            httpResp = requests.get(versionUrl, headers=headers, verify=False)
            if httpResp.status_code is not 200:
                err = 'Failed to retrieve info page. HTTP status code: %d' % httpResp.status_code
                self.__logger.error(err)
                raise TintriServerError(httpResp.status_code, message=err)
            self.__version = map_to_object(json.loads(httpResp.text), Version)
            self.__logger.debug('%s preferredVersion:%s' % (self.__version.productName, self.__version.preferredVersion))
        return self.__version

    def __get_client_header(self):
        from .__init__ import __version__
        default_header = 'Tintri-PythonSDK-%s' % __version__
        if self.__custom_client_header:
            return '%s,%s' % (default_header, self.__custom_client_header)
        else:
            return default_header

    def login(self, username=None, password=None):
        """Login to Tintri API server, username and password won't be cached

           Args:
               username (str): Login user name.
               password (str): Login user name password.

           Returns:
               str: credentials role name
        """
        self.__get_version()
        
        if (username is None and self.__username is None) or  (password is None and self.__password is None):
            raise TintriError("Username and password need to be provided either at object instantiation or at login")
        
        login_username = self.__username if not username else username
        login_password = self.__password if not password else password

        headers = {'content-type': 'application/json', 'Tintri-Api-Client': self.__get_client_header()}
        data = {"username": login_username, "password": login_password, "typeId": "com.tintri.api.rest.vcommon.dto.rbac.RestApiCredentials"}
        login_url = 'https://%s/api/v%s/session/login' % (self.__host, self.__api_version)
        
        httpresp = requests.post(login_url, json.dumps(data), headers=headers, verify=False)
        
        if httpresp.status_code is not 200:
            err = 'Failed to authenticate to %s as user %s pwd %s. HTTP status code: %d' % (self.host, self.username, self.password, httpresp.status_code)
            self.__logger.error(err)
            try:
                json_error = json.loads(httpresp.text)
            except Exception as e:
                raise TintriServerError(httpresp.status_code, None, cause=`e`, details=err)
            raise TintriAuthenticationError(json_error['code'], json_error['message'], json_error['causeDetails'])

        self.__session_id = httpresp.cookies['JSESSIONID']
        self.__logger.debug('Logged in to %s as %s' % (self.__host, self.__username))
        return httpresp.json()

    def logout(self):
        """Logout from Tintri server"""

        if self.__session_id:
            url = 'https://%s/api/v%s/session/logout' % (self.host, self.__api_version)
            try:
                requests.get(url, verify=False)
                self.__logger.info('Logged out as user %s' % self.__username)
            except Exception as e:
                self.__logger.error('Failed to logout. Error:%s' % e)
            self.__init_per_session_vars()

    def change_password(self, new_password):
        """Change the Tintri server password

           Args:
               new_password (str): New password for logged in user.

           Returns:
               str: credentials role name
        """
        self.__get_version()

        headers = {'content-type': 'application/json', 'Tintri-Api-Client': self.__get_client_header()}
        data = {"username": self.__username, "password": self.__password, "typeId": "com.tintri.api.rest.vcommon.dto.rbac.RestApiCredentials", 'newPassword': new_password}
        login_url = 'https://%s/api/v%s/session/login' % (self.__host, self.__api_version)
        
        httpresp = requests.post(login_url, json.dumps(data), headers=headers, verify=False)
        
        if httpresp.status_code is not 200:
            err = 'Failed to change password from %s to %s for user %s on host %s. HTTP status code: %d' % (self.password, new_password, self.username, self.host, httpresp.status_code)
            self.__logger.error(err)
            try:
                json_error = json.loads(httpresp.text)
            except Exception as e:
                raise TintriServerError(httpresp.status_code, None, cause=`e`, details=err)
            raise TintriAuthenticationError(json_error['code'], json_error['message'], json_error['causeDetails'])

        self.__session_id = httpresp.cookies['JSESSIONID']
        self.__password = new_password
        self.__logger.debug('Logged in to %s as %s' % (self.__host, self.__username))
        return httpresp.json()        

    def is_logged_in(self):
        """Indicates if the Tintri server is logged into

           Returns:
               bool: True if logged in
        """
        return self.__session_id is not None # convert to boolean

    def is_vmstore(self):
        """Indicates if the Tintri server is a VMstore

           Returns:
               bool: True if logged into a VMstore
        """
        if not self.__version: self.__get_version()
        return self.__version.productName == "Tintri VMstore"

    def is_tgc(self):
        """Indicates if the Tintri server is a TGC

           Returns:
               bool: True if logged into a TGC
        """
        if not self.__version: self.__get_version()
        return self.__version.productName == "Tintri Global Center"

    def get_raw(self, url):
        httpresp = self._send_raw_http_request('GET', url)
        return httpresp.status_code, httpresp.text
    
    def post_raw(self, url, data):
        httpresp = self._send_raw_http_request('POST', url, data)
        return httpresp.status_code, httpresp.text

    def put_raw(self, url, data):
        httpresp = self._send_raw_http_request('PUT', url, data)
        return httpresp.status_code, httpresp.text

    def patch_raw(self, url, data):
        httpresp = self._send_raw_http_request('PATCH', url, data)
        return httpresp.status_code, httpresp.text

    def delete_raw(self, url):
        httpresp = self._send_raw_http_request('DELETE', url)
        return httpresp.status_code, httpresp.text

    def download_file(self, report_url, file_name):
        """
        Downloads the file pointed by URL.

        Args:
        
            report_url (str): URL returned from API from which file can be downloaded
            file_name (str): Name to be used for downloaded file 
        """
        headers = {'content-type': 'application/json'}
    
        try:
            r = requests.get(report_url, headers=headers, verify=False, stream=True)
            if r.status_code != 200:
                message = "The HTTP response for get call on: %s is %s" % (report_url, r.status_code)
                raise TintriServerError(r.status_code, message=message)
    
            with open(file_name, 'w') as file_h:
                for block in r.iter_content(4096):
                    file_h.write(block)

        except TintriServerError:
            raise    
        except requests.ConnectionError:
            raise TintriError("API Connection error occurred.")
        except requests.HTTPError:
            raise TintriError("HTTP error occurred.")
        except requests.Timeout:
            raise TintriError("Request timed out.")
        except Exception as e:
            raise TintriError("An unexpected error occurred: " + e.__str__())


    def _send_raw_http_request(self, method, url, data=None):
        self.__logger.debug('%s %s' % (method, url))
        if method in ['POST', 'PUT', 'PATCH']:
            self.__logger.log(TINTRI_LOG_LEVEL_DATA, 'Data: %s' % data)

        headers = {'content-type': 'application/json'}
        if self.__session_id:
            headers['cookie'] = 'JSESSIONID=%s' % self.__session_id

        if method in ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']:
            if method == 'GET': httpresp = requests.get(url, headers=headers, verify=False)
            elif method == 'POST': httpresp = requests.post(url, data, headers=headers, verify=False)
            elif method == 'PUT': httpresp = requests.put(url, data, headers=headers, verify=False)
            elif method == 'PATCH': httpresp = requests.patch(url, data, headers=headers, verify=False)
            elif method == 'DELETE': httpresp = requests.delete(url, headers=headers, verify=False)
            self._httpresp = httpresp # self._httpresp is for debugging only, not thread-safe
            return httpresp
        else:
            raise TintriError(None, message='Invalid HTTP method: ' + method) # This should never happen

    def _process_request(self, method, path_params=[], query_params={}, resource_url=None, request_class=None, response_class=None, data=None):
        '''
        Preprocess request
        
        How request URL is determined:
        1. if resource_url is present, use it
        2. otherwise if request_class._url is not None, use it
        3. otherwise use request_class.__name__ with lowercase of first letter
        '''
        #self.__logger.debug('method:%s pparams:%s qparams:%s rurl:%s' % (method, `path_params`, `query_params`, resource_url))
        # Puts tintri host, API version and any URL path parameters, query params in URL
        if type(path_params) in [types.ListType, types.TupleType]:
            localargs = list(path_params)
        else:
            localargs = [path_params]
            
        if resource_url:
            urltemplate = resource_url
        elif request_class is not None:
            if request_class._url:
                urltemplate = request_class._url
            else:
                urltemplate = request_class.__name__[0].lower() + request_class.__name__[1:] 
        else:
            raise Exception("Either resource_url or request_class must be provided.")
             
        if not urltemplate.startswith('/'):
            urltemplate = '/' + urltemplate
        urltemplate = r'https://%s/api/v%s' + urltemplate
        
        stack = inspect.stack()
        caller = stack[2][3]
        if caller in ['_get_one', '_update', '_patch', '_delete']:
            if request_class is not None and not request_class._is_singleton:
                urltemplate += '/%s'
                
        #self.logger.debug('urltemplate: %s, localargs: %s' % (urltemplate, localargs))
        if urltemplate.count("%s") != len(([self.host, self.api_version] + localargs)):
            raise TypeError("Incorrect API usage, please provide all the parameters for this function")

        url = urltemplate % tuple([self.host, self.api_version] + localargs)

        try:
            querystring = urllib.urlencode(query_params)
            if querystring != '':
                url = '%s?%s' % (url, querystring)
        except Exception as e:
            logging.warning('Failed to URL-encode map %s for url %s. Error:%s' % (query_params, url, e))
            raise e
#         querystring = ''
#         if query_params:
#             for k in query_params:
#                 querystring += '&%s=%s' % (k, urllib.quote(str(query_params[k])))
#             querystring = querystring[1:]
#             url = '%s?%s' % (url, querystring)

        jsondata = data
        if not type(data) in types.StringTypes:
            jsondata = json.dumps(data, cls=TintriJSONEncoder)
    
        return method, url, jsondata

    def _json_object_to_object(self, json_object, entity_class, context={}):
        if type(json_object) == types.DictionaryType:
            if hasattr(entity_class, '_is_paginated') and entity_class._is_paginated:
                try:
                    if hasattr(self, '_process_page'):
                        return self._process_page(json_object, entity_class, context)
                    else:
                        raise AttributeError('Class %s does not have _process_page() method' % entity_class.__name__)
                except ValueError:
                    return map_to_object(json_object, entity_class)
            else:
                return map_to_object(json_object, entity_class)
        elif type(json_object) == types.ListType:
            objects = []
            for obj in json_object:
                objects.append(map_to_object(obj, entity_class))

            # if auto_page is set, return a page with the items
            if 'typeId' in json_object and json_object['typeId'] == 'com.tintri.api.rest.v310.dto.Page' and self.__auto_page:
                return TintriPage(paginated=entity_class._is_paginated, items=objects, context=context)
            else:
                return objects
        else:
            return json_object # Return any other type as is, such as None, string, number, boolean

    def _process_response(self, method, url, response, request_class, response_class, query_params, path_params):
        if response.status_code == 204:
            return None
        elif response.status_code == 200:
            return self._process_result(method, url, response, request_class, response_class, query_params, path_params)
        else:
            return self._process_error(method, url, response.status_code, response.text)

    def _process_result(self, method, url, response, request_class, response_class, query_params, path_params):
        cls = response_class and response_class or request_class
        if cls in [types.StringType, types.UnicodeType]: # if we expect string type result, no need for further processing
            return response.text
        else:
            # prepare context to hold url and data along with method to navigate pages
            context = { 'method': method, 'url': url, 'query_params': query_params, 'response_class': response_class, 'func': self._get_all, 'request_class': request_class, 'path_params': path_params, 'response_data': response.text }
            return self._json_object_to_object(json.loads(response.text), cls, context=context) # first load JSON to a Python list or dict

    def _process_error(self, method, url, status_code, response_data):
        try:
            jsonError = json.loads(response_data)
        except ValueError as e:
            self.__logger.warning("Failed to decode result. url:%s status:%s error:%s data:%s" % (url, status_code, e, response_data))
            raise TintriServerError(status_code, cause=e, message="Failed to decode result. url:%s status:%s error:%s data:%s" % (url, status_code, e, response_data))
        except Exception as e:
            self.__logger.warning("HTTP request failed. URL:%s Status Code:%s Error:%s Text:%s" % (url, status_code, e, response_data))
            raise TintriServerError(status_code, None, cause=`e`, details=response_data)

        if type(jsonError) == types.DictionaryType:
            self.__logger.info('Server error. url:%s status:%s code:%s message:%s cause:%s' % (url, status_code, jsonError['code'], jsonError['message'], jsonError['causeDetails']))
            if status_code == 400:
                raise TintriBadRequestError(jsonError['code'], jsonError['message'], jsonError['causeDetails'])
            elif status_code == 401:
                raise TintriInvalidSessionError(jsonError['code'], jsonError['message'], jsonError['causeDetails'])
            elif status_code == 403:
                raise TintriAuthorizationError(jsonError['code'], jsonError['message'], jsonError['causeDetails'])
            elif status_code == 404:
                raise TintriAPINotFoundError(jsonError['code'], jsonError['message'], jsonError['causeDetails'])
            elif status_code == 500:
                raise TintriInternalError(jsonError['code'], jsonError['message'], jsonError['causeDetails'])
            else:
                raise TintriServerError(status_code, code=jsonError['code'], message=jsonError['message'], details=jsonError['causeDetails'])
        else:
            self.__logger.info('Server error. url:%s status:%s Unknown error:%s' % (url, status_code, response_data))
            raise TintriServerError(status_code, code=None, message='Unknown error', details=response_data)
            
    def _send_http_request(self, method, path_params=[], query_params={}, resource_url=None, request_class=None, response_class=None, data=None):
        """
        data is either json string or object. If object, will call object.toJson()
        if entity_class is specified, use it to deserialize JSON. Otherwise use cls
        """
        #print 'method:%s path_params:%s query_params:%s resource_url:%s request_class:%s response_class:%s returns_list:%s' % (method, `path_params`, query_params, resource_url, request_class and request_class.__name__ or None, response_class, returns_list)
        _method, _url, _data = self._process_request(method, path_params, query_params, resource_url, request_class, response_class, data)
        #print 'method:%s url:%s data:%s' % (_method, _url, _data)

        try:
            httpresp = self._send_raw_http_request(_method, _url, _data)
            self.__logger.log(TINTRI_LOG_LEVEL_DATA, 'Response: %s' % httpresp.text)
            return self._process_response(_method, _url, httpresp, request_class, response_class, query_params, path_params)
        except TintriInvalidSessionError as e:
            if self.__auto_login and self.__username is not None and self.__password is not None and e.code == "ERR-API-0104":
                # On error due to invalid session, login and retry
                self.login()
                httpresp = self._send_raw_http_request(_method, _url, _data)
                self.__logger.log(TINTRI_LOG_LEVEL_DATA, 'Response: %s' % httpresp.text)
                return self._process_response(_method, _url, httpresp, request_class, response_class, query_params, path_params)
            else:
                raise

    def _get_one(self, path_params=[], query_params={}, resource_url=None, request_class=None, response_class=None, name=None):
        return self._send_http_request('GET', path_params, query_params, resource_url, request_class, response_class)

    def _get_all(self, path_params=[], query_params={}, resource_url=None, request_class=None, response_class=None, name=None):
        return self._send_http_request('GET', path_params, query_params, resource_url, request_class, response_class)

    def _create(self, obj, path_params=[], query_params={}, resource_url=None, request_class=None, response_class=None, name=None):
        return self._send_http_request('POST', path_params, query_params, resource_url, request_class, response_class, data=obj)

    def _update(self, obj, path_params=[], query_params={}, resource_url=None, request_class=None, response_class=None, name=None):
        return self._send_http_request('PUT', path_params, query_params, resource_url, request_class, response_class, obj)

    def _patch(self, obj, path_params=[], query_params={}, resource_url=None, request_class=None, response_class=None, name=None):
        return self._send_http_request('PATCH', path_params, query_params, resource_url, request_class, response_class, obj)

    def _delete(self, path_params=[], query_params={}, resource_url=None, request_class=None, response_class=None, name=None):
        return self._send_http_request('DELETE', path_params, query_params, resource_url, request_class, response_class)
