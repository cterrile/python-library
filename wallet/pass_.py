import logging

from wallet import common


LOGGER = logging.getLogger('urbanairship')


def get_pass(wallet, pass_id=None, external_id=None):
    """Retrieve a pass.

    Args:
        wallet (obj): A wallet client object.
        pass_id (str): The pass ID of the pass you wish to retrieve.
        pass_external_id (str): The external ID of the pass you wish to
        retrieve.

    Returns:
        A pass object.

    Example:
        >>> my_pass = Pass.get_pass(pass_external_id=12345)
        <id:67890745, templateId:51010>
    """
    if not (pass_id or external_id) or (pass_id and external_id):
        raise ValueError('Please specify only one of pass_id or external_id.')

    response = wallet.request(
        method='GET',
        body=None,
        url=Pass.build_url(
            common.PASS_BASE_URL,
            main_id=pass_id,
            pass_external_id=external_id
        ),
        version=1.2
    )
    payload = response.json()
    return Pass.from_data(payload)


def delete_pass(wallet, pass_id=None, external_id=None):
    """Delete a pass.

    Arguments:
        wallet (obj): A UA Wallet object.
        pass_id (str or int): The ID of the pass you wish to delete.
        external_id (str or int): The external ID of the pass you wish
            to delete.

    Returns:
        A response object.

    Raises:
        ValueError: If neither, or both, of pass_id and external_id
            are specified.

    Example:
        >>> delete_pass(ua_wallet, pass_id='123456')
        <Response [200]>
    """
    if not (pass_id or external_id) or (pass_id and external_id):
        raise ValueError('Please specify only one of pass_id or external_id.')

    response = wallet.request(
        method='DELETE',
        body=None,
        url=Pass.build_url(
            common.PASS_BASE_URL,
            main_id=pass_id,
            pass_external_id=external_id
        ),
        version=1.2
    )
    LOGGER.info('Successful pass deletion: {}'.format(
        pass_id if pass_id else external_id
    ))
    return response


class Pass(object):


    @classmethod
    def from_data(cls, data):
        return data

    @staticmethod
    def build_url(
        base_url,
        main_id=None,
        template_external_id=None,
        pass_external_id=None
    ):
        if main_id and not (template_external_id or pass_external_id):
            return base_url.format(main_id)
        elif template_external_id and not (main_id or pass_external_id):
            return base_url.format('id/' + str(external_id))
        elif pass_external_id and main_id and not template_external_id:
            return base_url.format(str(main_id) + '/id/' + str(pass_external_id))
        elif template_external_id and pass_external_id and not main_id:
            return base_url.format(
                'id/' + str(template_external_id) + '/id/' + str(pass_external_id)
            )
        else:
            return base_url.format('')