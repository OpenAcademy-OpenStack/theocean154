from glanceclient import Client
import keystoneclient.v2_0.client as ksclient
from novaclient.v1_1 import client as nclient
import os


#Locals 
auth = {}
auth['username'] = os.environ.get('OS_USERNAME')
auth['password'] = os.environ.get('OS_PASSWORD')
auth['auth_url'] = 'http://10.0.2.15:5000/v2.0/'
auth['tenant_name'] = os.environ.get('OS_TENANT_NAME')

#Initialize authorization,  compute, and image service 
keystone = ksclient.Client(**auth)
glance = Client('1', endpoint='http://10.0.2.15:9292',token=keystone.auth_token)
nova = nclient.Client(os.environ.get('OS_USERNAME'), os.environ.get('OS_PASSWORD'),
                            os.environ.get('OS_TENANT_NAME'),
                            auth_url='http://10.0.2.15:5000/v2.0')


#Fetch list of compute nodes
images = glance.images.list()

#make vms 
for image in images:
	if image.name.find('ubuntu') > -1: 
		flavor = nova.flavors.find(name="m1.micro")
		nova.servers.create(name=image.name,
                       image=image,
                       flavor=flavor)
