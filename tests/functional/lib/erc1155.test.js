"use strict";

require("core-js/stable");

require("regenerator-runtime/runtime");

var _zemu = _interopRequireDefault(require("@zondax/zemu"));

var _errors = require("@ledgerhq/errors");

var _test = require("./test.fixture");

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

// Only LNX
const model = _test.nano_models[1];
{
  const set_plugin = (0, _test.apdu_as_string)('e01600007401010745524331313535495f947276749ce646f68ac8c248420045cb7b5ef242432a00000000000000010001473045022100ec4377d17e8d98d424bf16b29c691bc1a010825fb5b8a35de0268a9dc22eab2402206701b016fe6718bf519d18cc12e9838e9ef898cc4c143017839023c3260b2d74');
  const provide_nft_info = (0, _test.apdu_as_string)('e01400007b0101124f70656e53656120436f6c6c656374696f6e495f947276749ce646f68ac8c248420045cb7b5e0000000000000001000147304502210083e357a828f13d574b1296214a3749c194ab1df1f8a243655c053b1c72f91e0c02201ed93cfac7e87759445c4da2e4bfd6e1cf0405ea37c7293bc965948f51bef5cc');
  const sign_first = (0, _test.apdu_as_string)('e004000096058000002c8000003c800000000000000000000000f901090b8520b673dd0082bcb394495f947276749ce646f68ac8c248420045cb7b5e80b8e4f242432a0000000000000000000000006cbcd73cd8e8a42844662f0a0e76d7f79afd933d000000000000000000000000c2907efcce4011c491bbeda8a0fa63ba7aab596cabf06640f8ca8fc5e0ed471b10befcdf65a33e4300000000');
  const sign_more = (0, _test.apdu_as_string)('e00480008b00006a0000000064000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000a000000000000000000000000000000000000000000000000000000000000000043078303000000000000000000000000000000000000000000000000000000000018080');
  test('[Nano ' + model.letter + '] Transfer ERC-1155', (0, _test.zemu)(model, async (sim, eth) => {
    const current_screen = sim.getMainMenuSnapshot();
    await (0, _test.send_apdu)(eth.transport, set_plugin);
    await (0, _test.send_apdu)(eth.transport, provide_nft_info);
    await (0, _test.send_apdu)(eth.transport, sign_first);
    let sign_promise = (0, _test.send_apdu)(eth.transport, sign_more);
    await (0, _test.waitForAppScreen)(sim, current_screen);
    await sim.navigateAndCompareSnapshots('.', model.name + '_erc1155_transfer', [10, -1, 0]);
    await sign_promise;
  }));
  test('[Nano ' + model.letter + '] Transfer ERC-1155 w/o PROVIDE_NFT_INFORMATION', (0, _test.zemu)(model, async (sim, eth) => {
    const current_screen = sim.getMainMenuSnapshot();
    await (0, _test.send_apdu)(eth.transport, set_plugin);
    await (0, _test.send_apdu)(eth.transport, sign_first);
    let sign_promise = (0, _test.send_apdu)(eth.transport, sign_more);
    await (0, _test.waitForAppScreen)(sim, current_screen);
    await sim.navigateAndCompareSnapshots('.', model.name + '_erc1155_transfer_wo_info', [10, -1, 0]);
    await sign_promise;
  }));
  test('[Nano ' + model.letter + '] Transfer ERC-1155 w/o SET_PLUGIN', (0, _test.zemu)(model, async (sim, eth) => {
    const current_screen = sim.getMainMenuSnapshot();
    await (0, _test.send_apdu)(eth.transport, provide_nft_info);
    let sign_tx = (0, _test.send_apdu)(eth.transport, sign_first);
    await expect(sign_tx).rejects.toEqual(new _errors.TransportStatusError(0x6a80));
  }));
}
test('[Nano ' + model.letter + '] Batch transfer ERC-1155', (0, _test.zemu)(model, async (sim, eth) => {
  const set_plugin = (0, _test.apdu_as_string)('e01600007401010745524331313535495f947276749ce646f68ac8c248420045cb7b5e2eb2c2d60000000000000001000147304502210087b35cefc53fd94e25404933eb0d5ff08f20ba655d181de3b24ff0099dc3317f02204a216aa9e0b84bef6e20fcb036bd49647bf0cab66732b99b49ec277ffb682aa1');
  const provide_nft_info = (0, _test.apdu_as_string)('e0140000820101194f70656e536561205368617265642053746f726566726f6e74495f947276749ce646f68ac8c248420045cb7b5e00000000000000010001473045022100c74cd613a27a9f4887210f5a3a0e12745e1ba0ab3a0d284cb6485d89c3cce4e602205a13e62a91164985cf58a838f8f531c0b91b980d206a5ba8df28270023ef93a3');
  const sign_first = (0, _test.apdu_as_string)('e004000096058000002c8000003c800000000000000000000000f9020b0e850d8cfd86008301617d94495f947276749ce646f68ac8c248420045cb7b5e80b901e42eb2c2d60000000000000000000000006cbcd73cd8e8a42844662f0a0e76d7f79afd933d000000000000000000000000c2907efcce4011c491bbeda8a0fa63ba7aab596c00000000000000000000000000000000000000000000');
  const sign_more_1 = (0, _test.apdu_as_string)('e004800096000000000000000000a0000000000000000000000000000000000000000000000000000000000000012000000000000000000000000000000000000000000000000000000000000001a00000000000000000000000000000000000000000000000000000000000000003abf06640f8ca8fc5e0ed471b10befcdf65a33e430000000000006a0000000064def9d99ff495856496c028c0');
  const sign_more_2 = (0, _test.apdu_as_string)('e00480009689732473fcd0bbbe000000000000a30000000001abf06640f8ca8fc5e0ed471b10befcdf65a33e430000000000006a00000000640000000000000000000000000000000000000000000000000000000000000003000000000000000000000000000000000000000000000000000000000000000700000000000000000000000000000000000000000000000000000000000000010000');
  const sign_more_3 = (0, _test.apdu_as_string)('e00480006100000000000000000000000000000000000000000000000000000000000200000000000000000000000000000000000000000000000000000000000000043078303000000000000000000000000000000000000000000000000000000000018080');
  const current_screen = sim.getMainMenuSnapshot();
  await (0, _test.send_apdu)(eth.transport, set_plugin);
  await (0, _test.send_apdu)(eth.transport, provide_nft_info);
  await (0, _test.send_apdu)(eth.transport, sign_first);
  await (0, _test.send_apdu)(eth.transport, sign_more_1);
  await (0, _test.send_apdu)(eth.transport, sign_more_2);
  let sign_promise = (0, _test.send_apdu)(eth.transport, sign_more_3);
  await (0, _test.waitForAppScreen)(sim, current_screen);
  await sim.navigateAndCompareSnapshots('.', model.name + '_erc1155_batch_transfer', [8, -1, 0]);
  await sign_promise;
}));