import string
import random
import hashlib
from urllib.parse import quote
from xml.etree import ElementTree


class WeChat:
    @staticmethod
    def random_str(length=16):
        chars = "".join([string.ascii_letters, string.digits])
        sa = []
        for _ in range(length):
            sa.append(random.choice(chars))
        return "".join(sa)

    @staticmethod
    def format_query_param(params, *, is_urlencode=False):
        """
        order params
        >>> params = {'appid': 'wxd930ea5d5a258f4f', 'mch_id': '10000100', 'device_info': 1000,
        ... 'body': 'test', 'nonce_str': 'ibuaiVcKdpRxkhJA'}
        >>> WeChat.format_query_param(params)
        'appid=wxd930ea5d5a258f4f&body=test&device_info=1000&mch_id=10000100&nonce_str=ibuaiVcKdpRxkhJA'
        """
        ordered_params = sorted(params)
        tmp = []
        for k in ordered_params:
            v = quote(params[k]) if is_urlencode else params[k]
            tmp.append(f"{k}={v}")
        return "&".join(tmp)

    @staticmethod
    def gen_sign(params, *, sign_type="MD5", app_key=None):
        """
        gen sign
        default sign type 'MD5', testing data from official document
        >>> params = {'appid': 'wxd930ea5d5a258f4f', 'mch_id': '10000100', 'device_info': 1000,
        ... 'body': 'test', 'nonce_str': 'ibuaiVcKdpRxkhJA'}
        >>> app_key = '192006250b4c09247ec02edce69f6a2d'
        >>> WeChat.gen_sign(params, app_key=app_key)
        '9A0A8659F005D6984697E2CA0A9CF3B7'
        """
        algo_map = {"MD5": hashlib.md5, "SHA256": hashlib.sha256}
        ordered_string = WeChat.format_query_param(params, False)
        raw_string = f"{ordered_string}&key={app_key}"
        sign = algo_map[sign_type](raw_string.encode("utf8")).hexdigest()
        return sign.upper()

    @staticmethod
    def to_xml(params):
        """dict to xml"""
        xml = ["<xml>"]
        for k, v in params.items():
            if v.isdigit():
                xml.append(f"<{k}>{v}</{k}>")
            else:
                xml.append(f"<{k}><![CDATA[{v}]]></{k}>")
        xml.append("</xml>")
        return "".join(xml)

    @staticmethod
    def to_dict(xml):
        """xml to dict"""
        dom_tree = ElementTree.fromstring(xml)
        data = {node.tag: node.text for node in dom_tree}
        return data


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)
