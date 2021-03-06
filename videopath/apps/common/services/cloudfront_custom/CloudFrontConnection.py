from boto.cloudfront import CloudFrontConnection as _CloudFrontConnection

from videopath.apps.common.services.cloudfront_custom.invalidation import InvalidationBatch
from boto import handler
import xml.sax
from boto.cloudfront.exception import CloudFrontServerError

class CloudFrontConnection(_CloudFrontConnection):

	def create_invalidation_request(self, distribution_id, paths,
	                                caller_reference=None):
	    """Creates a new invalidation request
	        :see: http://goo.gl/8vECq
	    """
	    # We allow you to pass in either an array or
	    # an InvalidationBatch object
	    if not isinstance(paths, InvalidationBatch):
	        paths = InvalidationBatch(paths)
	    paths.connection = self
	    uri = '/%s/distribution/%s/invalidation' % (self.Version,
	                                                distribution_id)
	    response = self.make_request('POST', uri,
	                                 {'Content-Type': 'text/xml'},
	                                 data=paths.to_xml())
	    body = response.read()
	    if response.status == 201:
	        h = handler.XmlHandler(paths, self)
	        xml.sax.parseString(body, h)
	        return paths
	    else:
	        raise CloudFrontServerError(response.status, response.reason, body)

