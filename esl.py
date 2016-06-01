import json
import requests
import os
import codecs

class EslClient:

    def __init__(self, api_key, api_url):
        self.api_key = api_key
        self.api_url = api_url
        self.headers = {"Authorization": "Basic " + self.api_key}

    def query_package(self, package_id):
        """
        get details for a given package
        :param package_id: package GUID
        :return:json string
        """
        r = requests.get(url=self.api_url+'/packages/'+package_id, headers=self.headers)
        return r.text

    def query_package_evidence_summary(self, package_id):
        """
        get the evidence summary PDF for a given package
        :param package_id: package GUID
        :return: PDF buffer
        """
        r = requests.get(url=self.api_url+'/packages/'+package_id+'/evidence/summary', headers=self.headers)
        return r.content

    def query_package_audit_trail(self, package_id):
        """
        get the audit trail for a give package
        :param package_id: package GUID
        :return: json string
        """
        r = requests.get(url=self.api_url+'/packages/'+package_id+'/audit', headers=self.headers)
        return r.text

    def query_package_field_summary(self, package_id):
        """
        get the field summary for a package
        :param package_id: package GUID
        :return: json string
        """
        r = requests.get(url=self.api_url+'/packages/'+package_id+'/fieldSummary', headers=self.headers)
        return r.text

    def query_package_signing_status(self, package_id):
        """
        get the status of a give package
        :param package_id: package GUID
        :return: json string
        """
        r = requests.get(url=self.api_url+'/packages/'+package_id+'/signingStatus', headers=self.headers)
        return r.text

    def get_package_document(self, package_id, document_id):
        """
        get a document from a given package
        :param package_id: package GUID
        :param document_id:  document id
        :return: PDF buffer
        """
        r = requests.get(url=self.api_url+'/packages/'+package_id+'/documents/'+document_id+'/pdf',
                         headers=self.headers)
        return r.content

    def get_package_zip(self, package_id):
        """
        get the download package for a give package
        :param package_id: package GUID
        :return: ZIP buffer
        """
        status = json.loads(self.query_package_signing_status(package_id))
        if status['status'] == "COMPLETED":
            r = requests.get(url=self.api_url+'/packages/'+package_id+'/documents/zip', headers=self.headers)
            return r.content
        else:
            raise NameError('package has not been completed')

    def get_authentication_token(self):
        """
        get authentication token
        :return: json string
        """
        r = requests.post(url=self.api_url+'/authenticationTokens', headers=self.headers)
        return r.text

    def delete_package(self, package_id):
        """
        delete a package
        :param package_id: package GUID
        """
        r = requests.delete(url=self.api_url+'/packages/'+package_id, headers=self.headers)

    def update_package(self, package_id, json_payload):
        """
        update a give package
        :param package_id: package GUID
        :param json_payload: json payload
        :return:
        """
        d = bytes(json_payload)
        r = requests.put(url=self.api_url+'/packages/'+package_id, headers=self.headers, data=d)

    def create_package_from_template(self, json_payload, template_id):
        """
        create a package using a template
        :param json_payload: json payload
        :param template_id: template GUID
        :return: json string
        """
        d = bytes(json_payload)
        r = requests.post(url=self.api_url+'/packages/'+template_id+"/clone", headers=self.headers, data=d)
        return r.text

    def create_package_multipart(self, json_payload, docs):
        """
        create package with documents
        :param json_payload: json payload
        :param docs: documents to sign
        :return: json string
        """
        r = requests.post(url=self.api_url + '/packages', data={'payload': json_payload}, files=docs,
                          headers=self.headers)
        return r.text
'''
#testing setup
client = EslClient('api key', 'esignlive url')
guid = ''
doc_id = ''
temp_id = ''
guid_del = ''
'''

'''
# test1 for creating package
payload = codecs.open('package.json', 'r',encoding='utf8').read()
documents = {'file': open(os.getcwd()+'\document.pdf', 'rb').read()}
print(client.create_package_multipart(payload, documents))
# test1 end
'''

'''
# test2 for query package
print('TEST 2 ' + client.query_package(guid))
# test2 end
'''

'''
# test3 for getting the evidence summary for a package
with open('evidence_summary.pdf', 'wb') as f:
    f.write(client.query_package_evidence_summary(guid))
print('TEST 3 complete')
# test3 end
'''

'''
# test4 for getting the audit trail for a given package
print('TEST4 ' + client.query_package_audit_trail(guid))
# test4 end
'''

'''
# test5 get getting the package field summary
print('TEST 5 ' + client.query_package_field_summary(guid))
# test5 end
'''

'''
# test6 get the signing status for a give package
print('TEST 6 ' + client.query_package_signing_status(guid))
# test6 end
'''

'''
# test7 get document form a give package
with open('document.pdf', 'wb') as f:
    f.write(client.get_package_document(guid,doc_id))
print('TEST 7 complete')
# test7 end
'''

'''
# test8 get the download package for a given package
with open('download_package.zip', 'wb') as f:
    f.write(client.get_package_zip(guid))
print('TEST 8 complete')
# test8 end
'''

'''
# test9 get an authentication token
print('TEST 9 ' + client.get_authentication_token())
# test9 end
'''

'''
# test10 delete a package
client.delete_package(guid_del)
print('TEST 10 complete')
# test10
'''

'''
# test11 update package
documents = {'file': open(os.getcwd()+'\document.pdf', 'rb').read()}
tokens = json.loads(client.create_package_multipart(codecs.open('package.json', 'r', encoding='utf8').read(),
                                                    documents))
client.update_package(tokens['id'], codecs.open('package_update.json', 'r', encoding='utf8').read())
print('TEST 11 complete')
# test11 end
'''

'''
# test12 create a package using a template NOTE: this test assumes that the template contains 2 place holders for
#   signers in order for the test to work correctly you need to get the ids for signer placeholders and update the
#   package_template.json payload
# print(client.query_package(temp_id)) # query your template to get the signer/placeholder ids
payload = codecs.open('package_template.json', 'r',encoding='utf8').read()
print('TEST 12 ' + client.create_package_from_template(payload, temp_id))
# test12
'''
