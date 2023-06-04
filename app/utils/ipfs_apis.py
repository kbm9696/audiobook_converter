import nft_storage
from nft_storage.api import nft_storage_api


class IPFS:
    def __init__(self):
        self.nft_base_uri = 'https://api.nft.storage'

    def upload_nft_storage(self, apikey, file):
        # See configuration.py for a list of all supported configuration parameters.
        configuration = nft_storage.Configuration(
            host="https://api.nft.storage"
        )
        print('hhhhhhhhhh')
        configuration = nft_storage.Configuration(
            access_token=apikey
        )
        with nft_storage.ApiClient(configuration) as api_client:
            # Create an instance of the API class
            api_instance = nft_storage_api.NFTStorageAPI(api_client)
            body = open(file, 'rb')  # file_type |

            # example passing only required values which don't have defaults set
            try:
                # Store a file
                api_response = api_instance.store(body, _check_return_type=False)
                return (api_response)
            except nft_storage.ApiException as e:
                return ("Exception when calling NFTStorageAPI->store: %s\n" % e)

    def status_nft_storage(self, apikey, cid_):
        configuration = nft_storage.Configuration(
            host="https://api.nft.storage"
        )
        configuration = nft_storage.Configuration(
            access_token=apikey
        )

        with nft_storage.ApiClient(configuration) as api_client:
            # Create an instance of the API class
            api_instance = nft_storage_api.NFTStorageAPI(api_client)
            cid = cid_  # str | CID for the NFT

            # example passing only required values which don't have defaults set
            try:
                # Get information for the stored file CID
                api_response = api_instance.status(cid, _check_return_type=False)
                return (api_response)
            except nft_storage.ApiException as e:
                return ("Exception when calling NFTStorageAPI->status: %s\n" % e)