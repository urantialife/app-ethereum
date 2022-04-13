from ast import List
from contextlib import contextmanager
from ctypes.wintypes import INT
import struct
from typing import Tuple

from speculos.client import SpeculosClient, ApduException

from boilerplate_client.boilerplate_cmd_builder import BoilerplateCommandBuilder, InsType
from boilerplate_client.exception import DeviceException
from boilerplate_client.transaction import Transaction


class BoilerplateCommand:
    def __init__(self,
                 client: SpeculosClient,
                 debug: bool = False) -> None:
        self.client = client
        self.builder = BoilerplateCommandBuilder(debug=debug)
        self.debug = debug
    
    def get_configuration(self) -> Tuple[int, int, int, int]:
        try:
            response = self.client._apdu_exchange(
                self.builder.get_configuration()
            )  # type: int, bytes
        except ApduException as error:
            raise DeviceException(error_code=error.sw, ins=InsType.INS_GET_VERSION)

        # response = FLAG (1) || MAJOR (1) || MINOR (1) || PATCH (1)
        assert len(response) == 4

        info, major, minor, patch = struct.unpack(
            "BBBB",
            response
        )  # type: int, int, int

        return info, major, minor, patch

    @contextmanager
    def get_public_key(self, bip32_path: str, display: bool = False, result: List = list()) -> Tuple[bytes, bytes, bytes]:
        try:
            chunk: bytes = self.builder.get_public_key(bip32_path=bip32_path, display=display)

            with self.client.apdu_exchange_nowait(cla=chunk[0], ins=chunk[1],
                                                          p1=chunk[2], p2=chunk[3],
                                                          data=chunk[5:]) as exchange:
                yield exchange
                response: bytes = exchange.receive()
                
        except ApduException as error:
            raise DeviceException(error_code=error.sw, ins=InsType.INS_GET_PUBLIC_KEY)

        # response = pub_key_len (1) ||
        #            pub_key (var) ||
        #            chain_code_len (1) ||
        #            chain_code (var)
        offset: int = 0

        pub_key_len: int = response[offset]
        offset += 1

        uncompressed_addr_len: bytes = response[offset:offset + pub_key_len]
        offset += pub_key_len
        
        eth_addr_len: int = response[offset]
        offset += 1
        
        eth_addr: bytes = response[offset:offset + eth_addr_len]
        offset += eth_addr_len

        chain_code: bytes = response[offset:]

        assert len(response) == 1 + pub_key_len + 1 + eth_addr_len + 32 # 32 -> chain_code_len
        
        result.append(uncompressed_addr_len)
        result.append(eth_addr)
        result.append(chain_code)

    @contextmanager
    def simple_sign_tx(self, bip32_path: str, transaction, result: List = list()) -> Tuple[bytes, bytes, bytes]:
        try:
            chunk: bytes = self.builder.simple_sign_tx(bip32_path=bip32_path, transaction=transaction)
        

            with self.client.apdu_exchange_nowait(cla=chunk[0], ins=chunk[1],
                                                  p1=chunk[2], p2=chunk[3],
                                                  data=chunk[5:]) as exchange:
                yield exchange
                response: bytes = exchange.receive()
        
        except ApduException as error:
            raise DeviceException(error_code=error.sw, ins=InsType.INS_SIGN_TX)

        print("HERE: ", response)

        # response = V (1) || R (32) || S (32)
        assert len(response) == 65

        v, r, s = struct.unpack("BII", response)

        result.append(v)
        result.append(r)
        result.append(s)

    def test_zemu_hard_apdu_sign(self) -> Tuple[int, int, int]:
        sign: bytes = b'\xe0\x04\x00\x00\x80\x05\x80\x00\x00\x2c\x80\x00\x00\x3c\x80\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\xf8\x69\x46\x85\x06\xa8\xb1\x5e\x00\x82\xeb\xeb\x94\x6b\x17\x54\x74\xe8\x90\x94\xc4\x4d\xa9\x8b\x95\x4e\xed\xea\xc4\x95\x27\x1d\x0f\x80\xb8\x44\x09\x5e\xa7\xb3\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x7d\x27\x68\xde\x32\xb0\xb8\x0b\x7a\x34\x54\xc0\x6b\xda\xc9\x4a\x69\xdd\xc7\xa9\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x01\x80\x80'
        provide_erc20: bytes = b'\xe0\x0a\x00\x00\x67\x03\x44\x41\x49\x6b\x17\x54\x74\xe8\x90\x94\xc4\x4d\xa9\x8b\x95\x4e\xed\xea\xc4\x95\x27\x1d\x0f\x00\x00\x00\x12\x00\x00\x00\x01\x30\x45\x02\x21\x00\xb3\xaa\x97\x96\x33\x28\x4e\xb0\xf5\x54\x59\x09\x93\x33\xab\x92\xcf\x06\xfd\xd5\x8d\xc9\x0e\x9c\x07\x00\x00\xc8\xe9\x68\x86\x4c\x02\x20\x7b\x10\xec\x7d\x66\x09\xf5\x1d\xda\x53\xd0\x83\xa6\xe1\x65\xa0\xab\xf3\xa7\x7e\x13\x25\x0e\x6f\x26\x07\x72\x80\x9b\x49\xaf\xf5'

        try:
            response = self.client._apdu_exchange(
                provide_erc20
            )  # type: int, bytes

            response = self.client._apdu_exchange(
                sign
            )
        except ApduException as error:
            raise DeviceException(error_code=error.sw, ins=InsType.INS_SIGN_TX)
        
        # response = V (1) || R (32) || S (32)
        assert len(response) == 65
        print(response.hex())

        offset: int = 0

        v: bytes = response[offset]
        offset += 1

        r: bytes = response[offset:offset + 32]
        offset += 32

        s: bytes = response[offset:]

        return v, r, s



    def sign_tx(self, bip32_path: str, transaction: Transaction) -> Tuple[int, bytes]:
        sw: int
        response: bytes = b""

        for is_last, chunk in self.builder.sign_tx(bip32_path=bip32_path, transaction=transaction):
            if is_last:
                with self.client.apdu_exchange_nowait(cla=chunk[0], ins=chunk[1],
                                                      p1=chunk[2], p2=chunk[3],
                                                      data=chunk[5:]) as exchange:
                    # Review Transaction
                    self.client.press_and_release('right')
                    # Address 1/3, 2/3, 3/3
                    self.client.press_and_release('right')
                    self.client.press_and_release('right')
                    self.client.press_and_release('right')
                    # Amount
                    self.client.press_and_release('right')
                    # Approve
                    self.client.press_and_release('both')
                    response = exchange.receive()
            else:
                response = self.client._apdu_exchange(chunk)
                print(response)

        # response = der_sig_len (1) ||
        #            der_sig (var) ||
        #            v (1)
        offset: int = 0
        der_sig_len: int = response[offset]
        offset += 1
        der_sig: bytes = response[offset:offset + der_sig_len]
        offset += der_sig_len
        v: int = response[offset]
        offset += 1

        assert len(response) == 1 + der_sig_len + 1

        return v, der_sig