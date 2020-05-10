#!/usr/bin/python
# FezzedOne's Drawable Generator


import os, sys, json
from PIL import Image
from math import ceil


class Error(Exception):
    def __init__(self, errorMsg):
        self.msg = errorMsg if type(errorMsg) is str else ""


class JsonList(list):
    def convertToJson(self):
        try:
            return json.dumps(self, sort_keys = True, indent = 4, separators = (',', ': '))
        except:
            print("Something went wrong trying to convert object to JSON.")


class JsonDict(dict):
    def convertToJson(self):
        try:
            return json.dumps(self, sort_keys = True, indent = 4, separators = (',', ': '))
        except:
            print("Something went wrong trying to convert object to JSON.")


def signCrop(imageObject):
    # This is an iterator! Use a for loop!
    width, height = imageObject.size
    # print("Iterator started. Image size: " + str(width) + "x" + str(height) )
    for i in range(ceil(height / 8)):
        for j in range(ceil(width / 32)):
            box = ( j * 32, i * 8, ((j+1) * 32), ((i+1) * 8) )
            # print("Iteration: (" + str(i) + ", " + str(j) + ")")
            # print(str(box))
            yield imageObject.crop(box), j, i

def frameCrop(imageObject, large=False, armour=False, singleFrame=False):
    # This is an iterator! Use a for loop!
    # Meant for use on Silverfeelin-compatible animated drawables.
    # v2.0 note: Added drawable armour support.
    frameSize = 64 if large else 32
    frameSize = 43 if armour else frameSize
    width, height = imageObject.size
    frameNum = 1
    if singleFrame:
        box = ( frameSize, 0, 2 * frameSize, frameSize )
        for x in range(1):
            yield imageObject.crop(box), 1, 1, 0
    else:
        for y in range(ceil(height / frameSize)):
            for x in range(ceil(width / frameSize)):
                frameNum += 1
                box = ( x * frameSize, y * frameSize, ((x+1) * frameSize), ((y+1) * frameSize) )
                yield imageObject.crop(box), frameNum, x, y


def drawableArmour(framesheetToConvert, directiveFileName, headItem=False, sleevesItem=False, backItem=False, headMask=False, emotes=False, floranEmotes=False, bodyDirs=False):
    # Converts a framesheet to a drawable armour item descriptor in JSON, which may be spawned in with xSB or /spawnitem;
    # or added to a character file with starcheat; or with dump_versioned_json, make_versioned_json and a text editor.
    try:
        framesheetFile = Image.open(framesheetToConvert).convert("RGBA")
        framesheetSize = framesheetFile.size
        framesheetPixels = framesheetFile.load()
    except:
        print("Image conversion error of some sort. Maybe the first argument is not actually a PNG image? Also, be sure your other arguments are input correctly.")
        return None
    else:
        requiredImageSize = ( 0, 0 )
        drawableArmourDirectives = "?replace;ffffff00=ffffff;00000000=ffffff;ffca8a00=ffffff;e0975c00=ffffff;a8563600=ffffff;6f291900=ffffff;9bba3d00=ffffff;48832f00=ffffff;1b4c2a00=ffffff;a4784400=ffffff;754c2300=ffffff;472b1300=ffffff;e7dfbd00=ffffff;320c4000=ffffff?scale=0.4?scale=0.7?replace;a0b03e=00a10000;7e9b35=00a20000;a5ba92=00a30000;769441=00a40000;557743=00a50000;83715c=00a60000;b19c82=00a70000;7c9036=00b10000;757a32=00b20000;91a638=00b30000;748e37=00b40000;746f2c=00b50000;7a8a31=00b60000;608333=00b70000;8f953a=00b80000;736f2f=00c10000;c2d1b4=00c20000;94ae76=00c30000;788e35=00c40000;6f602f=00c50000;6a846e=00c60000;617e34=00c70000;829935=00c80000;d5ddd7=00d10000;a5b4a7=00d20000;a4945f=00d30000;a57f58=00d40000;a98c6c=00d50000;ccc0a4=00d60000;cabb9d=00d70000;a5a381=00d80000;66714c=00e10000;ada788=00e20000;778c34=00e30000;b1917c=00e40000;95ad8f=00e50000?crop;6;2;7;3?scalenearest=2?blendscreen=/objects/outpost/customsign/signplaceholder.png?replace;01a10000=3fa10000;00a10100=00a13f00;01a10100=3fa13f00;01a20000=3fa20000;00a20100=00a23f00;01a20100=3fa23f00;01a30000=3fa30000;00a30100=00a33f00;01a30100=3fa33f00;01a40000=3fa40000;00a40100=00a43f00;01a40100=3fa43f00;01a50000=3fa50000;00a50100=00a53f00;01a50100=3fa53f00;01a60000=3fa60000;00a60100=00a63f00;01a60100=3fa63f00;01a70000=3fa70000;00a70100=00a73f00;01a70100=3fa73f00;01b10000=3fb10000;00b10100=00b13f00;01b10100=3fb13f00;01b20000=3fb20000;00b20100=00b23f00;01b20100=3fb23f00;01b30000=3fb30000;00b30100=00b33f00;01b30100=3fb33f00;01b40000=3fb40000;00b40100=00b43f00;01b40100=3fb43f00;01b50000=3fb50000;00b50100=00b53f00;01b50100=3fb53f00;01b60000=3fb60000;00b60100=00b63f00;01b60100=3fb63f00;01b70000=3fb70000;00b70100=00b73f00;01b70100=3fb73f00;01b80000=3fb80000;00b80100=00b83f00;01b80100=3fb83f00;01c10000=3fc10000;00c10100=00c13f00;01c10100=3fc13f00;01c20000=3fc20000;00c20100=00c23f00;01c20100=3fc23f00;01c30000=3fc30000;00c30100=00c33f00;01c30100=3fc33f00;01c40000=3fc40000;00c40100=00c43f00;01c40100=3fc43f00;01c50000=3fc50000;00c50100=00c53f00;01c50100=3fc53f00;01c60000=3fc60000;00c60100=00c63f00;01c60100=3fc63f00;01c70000=3fc70000;00c70100=00c73f00;01c70100=3fc73f00;01c80000=3fc80000;00c80100=00c83f00;01c80100=3fc83f00;01d10000=3fd10000;00d10100=00d13f00;01d10100=3fd13f00;01d20000=3fd20000;00d20100=00d23f00;01d20100=3fd23f00;01d30000=3fd30000;00d30100=00d33f00;01d30100=3fd33f00;01d40000=3fd40000;00d40100=00d43f00;01d40100=3fd43f00;01d50000=3fd50000;00d50100=00d53f00;01d50100=3fd53f00;01d60000=3fd60000;00d60100=00d63f00;01d60100=3fd63f00;01d70000=3fd70000;00d70100=00d73f00;01d70100=3fd73f00;01d80000=3fd80000;00d80100=00d83f00;01d80100=3fd83f00;01e10000=3fe10000;00e10100=00e13f00;01e10100=3fe13f00;01e20000=3fe20000;00e20100=00e23f00;01e20100=3fe23f00;01e30000=3fe30000;00e30100=00e33f00;01e30100=3fe33f00;01e40000=3fe40000;00e40100=00e43f00;01e40100=3fe43f00;01e50000=3fe50000;00e50100=00e53f00;01e50100=3fe53f00?scale=64?crop;1;1;44;44?replace;"
        if headItem:
            drawableArmourDirectives = "?replace;FFFFFF00=FFFFFF;A26F03=FFFFFF;725310=FFFFFF;D9B035=FFFFFF;6F2919=FFFFFF;A85636=FFFFFF;E0975C=FFFFFF;6F291900=FFFFFF;A8563600=FFFFFF;E0975C00=FFFFFF?scale=0.4?scale=0.7?replace;ffffff=00a10000?crop;6;2;7;3?scalenearest=2?blendscreen=/objects/outpost/customsign/signplaceholder.png?replace;01a10000=3fa10000;00a10100=00a13f00;01a10100=3fa13f00;01a20000=3fa20000;00a20100=00a23f00;01a20100=3fa23f00;01a30000=3fa30000;00a30100=00a33f00;01a30100=3fa33f00;01a40000=3fa40000;00a40100=00a43f00;01a40100=3fa43f00;01a50000=3fa50000;00a50100=00a53f00;01a50100=3fa53f00;01a60000=3fa60000;00a60100=00a63f00;01a60100=3fa63f00;01a70000=3fa70000;00a70100=00a73f00;01a70100=3fa73f00;01b10000=3fb10000;00b10100=00b13f00;01b10100=3fb13f00;01b20000=3fb20000;00b20100=00b23f00;01b20100=3fb23f00;01b30000=3fb30000;00b30100=00b33f00;01b30100=3fb33f00;01b40000=3fb40000;00b40100=00b43f00;01b40100=3fb43f00;01b50000=3fb50000;00b50100=00b53f00;01b50100=3fb53f00;01b60000=3fb60000;00b60100=00b63f00;01b60100=3fb63f00;01b70000=3fb70000;00b70100=00b73f00;01b70100=3fb73f00;01b80000=3fb80000;00b80100=00b83f00;01b80100=3fb83f00;01c10000=3fc10000;00c10100=00c13f00;01c10100=3fc13f00;01c20000=3fc20000;00c20100=00c23f00;01c20100=3fc23f00;01c30000=3fc30000;00c30100=00c33f00;01c30100=3fc33f00;01c40000=3fc40000;00c40100=00c43f00;01c40100=3fc43f00;01c50000=3fc50000;00c50100=00c53f00;01c50100=3fc53f00;01c60000=3fc60000;00c60100=00c63f00;01c60100=3fc63f00;01c70000=3fc70000;00c70100=00c73f00;01c70100=3fc73f00;01c80000=3fc80000;00c80100=00c83f00;01c80100=3fc83f00;01d10000=3fd10000;00d10100=00d13f00;01d10100=3fd13f00;01d20000=3fd20000;00d20100=00d23f00;01d20100=3fd23f00;01d30000=3fd30000;00d30100=00d33f00;01d30100=3fd33f00;01d40000=3fd40000;00d40100=00d43f00;01d40100=3fd43f00;01d50000=3fd50000;00d50100=00d53f00;01d50100=3fd53f00;01d60000=3fd60000;00d60100=00d63f00;01d60100=3fd63f00;01d70000=3fd70000;00d70100=00d73f00;01d70100=3fd73f00;01d80000=3fd80000;00d80100=00d83f00;01d80100=3fd83f00;01e10000=3fe10000;00e10100=00e13f00;01e10100=3fe13f00;01e20000=3fe20000;00e20100=00e23f00;01e20100=3fe23f00;01e30000=3fe30000;00e30100=00e33f00;01e30100=3fe33f00;01e40000=3fe40000;00e40100=00e43f00;01e40100=3fe43f00;01e50000=3fe50000;00e50100=00e53f00;01e50100=3fe53f00?scale=64?crop;1;1;44;44?replace;"
            requiredImageSize = ( 43, 43 )
        if sleevesItem:
            drawableArmourDirectives = "?replace;00000000=000000;ffffff00=ffffff;1b4c2a00=1b4c2a;d1e16000=d1e160;9bba3d00=9bba3d;d93a3a00=d93a3a;93262500=932625;60111900=601119?scale=0.4?blendscreen=/objects/outpost/customsign/signplaceholder.png;0;-4?replace;9c4f32=e10000;702450=e10000;a95b3b=008787;c5764b=008787;837655=008787;6d2785=00c3c3;8939a6=00c3c3;aa5538=00a5a5;bab350=00a5a5;8c3b5f=00a5a5;927d48=00a5a5;aa5536=878700;bab34f=878700;8c3b5e=878700;927d47=878700;7a516b=878700?scale=0.7?replace;c6ca57=a50000;9a6534=a50000;cdd95d=a50000;c6ca58=a50000;cbc359=a50000;cdd95e=a50000;b4a84b=00c3c3;c59550=00c3c3;c5ca66=00c3c3;998367=00c3c3;c7d360=00c3c3;625684=00c3c3;afdc72=00c3c3;96d87f=00c3c3;95d87f=00c3c3?scale=0.85?replace;cfd75c=a50000;c1913e=a50000;cbc454=a50000;ccc655=a50000;cad05d=a50000;9e6740=a50000;be9643=a50000;ccc957=a50000?scale=0.925?scale=0.9625?crop;5;4;6;5?replace;ccd85f=00a10000;cdd85f=00a20000;cddb5f=00a30000;c29f45=00a40000;cdda5f=00a50000;abbf58=00a60000;bcbc5d=00b10000;c6cd61=00b20000;c3ca5e=00b30000;cfdb61=00b40000;d0de5f=00b50000;9d9a5c=00b60000;ad9b5a=00c10000;b7a256=00c20000;c6c861=00c30000;cfdd61=00c40000;cfdb60=00c50000;bfc05a=00d10000;d0dd61=00d20000;cadd64=00d30000;ccdc61=00d40000;cfdc60=00d50000;d1de61=00d60000;d1df61=00d70000;abc057=00d80000;c1bf5c=00e10000;bfbd58=00e20000;cbd35d=00e30000;b3a051=00e40000;cad15f=00e50000;c6c25f=00e60000;aab45a=00e70000;cdda60=00f10000;a9bc59=00f20000;5a4837=00600000;b9b263=00610000;b2a660=00620000;b9b663=00630000;b4ab64=00640000;b5b958=00650000;b2a36c=00660000;b7b068=00670000;bcb768=00680000;a89e5d=00690000;b4ac65=006a0000;bebe60=006b0000;c2c166=006c0000;b9b464=006d0000;a89e5e=006e0000;c0bf61=006f0000;b6b65a=00700000;6e603e=00710000;a58c59=00720000;b6b45b=00730000;c2c062=00740000;b9b85a=00750000;b9bc5b=00760000;c4cb5d=00770000;b7bd57=00780000;70673a=00790000;babb5b=007a0000;b7b65a=007b0000;b8ab50=007c0000;c9cb68=007d0000;b9b75f=007e0000;bec060=007f0000;a89e5c=00800000;b6bb59=00810000;5e3834=ffffff00;aa8344=ffffff00;7e6646=ffffff00;828349=ffffff00;886a48=ffffff00;8d6d50=ffffff00;754f43=ffffff00;9a6639=ffffff00;825e46=ffffff00;848248=ffffff00;9a7051=ffffff00;85644e=ffffff00?scalenearest=2?blendscreen=/objects/outpost/customsign/signplaceholder.png?replace;01a10000=2ea10000;00a10100=00a12e00;01a10100=2ea12e00;01a20000=2ea20000;00a20100=00a22e00;01a20100=2ea22e00;01a30000=2ea30000;00a30100=00a32e00;01a30100=2ea32e00;01a40000=2ea40000;00a40100=00a42e00;01a40100=2ea42e00;01a50000=2ea50000;00a50100=00a52e00;01a50100=2ea52e00;01a60000=2ea60000;00a60100=00a62e00;01a60100=2ea62e00;01b10000=2eb10000;00b10100=00b12e00;01b10100=2eb12e00;01b20000=2eb20000;00b20100=00b22e00;01b20100=2eb22e00;01b30000=2eb30000;00b30100=00b32e00;01b30100=2eb32e00;01b40000=2eb40000;00b40100=00b42e00;01b40100=2eb42e00;01b50000=2eb50000;00b50100=00b52e00;01b50100=2eb52e00;01b60000=2eb60000;00b60100=00b62e00;01b60100=2eb62e00;01c10000=2ec10000;00c10100=00c12e00;01c10100=2ec12e00;01c20000=2ec20000;00c20100=00c22e00;01c20100=2ec22e00;01c30000=2ec30000;00c30100=00c32e00;01c30100=2ec32e00;01c40000=2ec40000;00c40100=00c42e00;01c40100=2ec42e00;01c50000=2ec50000;00c50100=00c52e00;01c50100=2ec52e00;01d10000=2ed10000;00d10100=00d12e00;01d10100=2ed12e00;01d20000=2ed20000;00d20100=00d22e00;01d20100=2ed22e00;01d30000=2ed30000;00d30100=00d32e00;01d30100=2ed32e00;01d40000=2ed40000;00d40100=00d42e00;01d40100=2ed42e00;01d50000=2ed50000;00d50100=00d52e00;01d50100=2ed52e00;01d60000=2ed60000;00d60100=00d62e00;01d60100=2ed62e00;01d70000=2ed70000;00d70100=00d72e00;01d70100=2ed72e00;01d80000=2ed80000;00d80100=00d82e00;01d80100=2ed82e00;01e10000=2ee10000;00e10100=00e12e00;01e10100=2ee12e00;01e20000=2ee20000;00e20100=00e22e00;01e20100=2ee22e00;01e30000=2ee30000;00e30100=00e32e00;01e30100=2ee32e00;01e40000=2ee40000;00e40100=00e42e00;01e40100=2ee42e00;01e50000=2ee50000;00e50100=00e52e00;01e50100=2ee52e00;01e60000=2ee60000;00e60100=00e62e00;01e60100=2ee62e00;01e70000=2ee70000;00e70100=00e72e00;01e70100=2ee72e00;01f10000=2ef10000;00f10100=00f12e00;01f10100=2ef12e00;01f20000=2ef20000;00f20100=00f22e00;01f20100=2ef22e00;01600000=2e600000;00600100=00602e00;01600100=2e602e00;01610000=2e610000;00610100=00612e00;01610100=2e612e00;01620000=2e620000;00620100=00622e00;01620100=2e622e00;01630000=2e630000;00630100=00632e00;01630100=2e632e00;01640000=2e640000;00640100=00642e00;01640100=2e642e00;01650000=2e650000;00650100=00652e00;01650100=2e652e00;01660000=2e660000;00660100=00662e00;01660100=2e662e00;01670000=2e670000;00670100=00672e00;01670100=2e672e00;01680000=2e680000;00680100=00682e00;01680100=2e682e00;01690000=2e690000;00690100=00692e00;01690100=2e692e00;016a0000=2e6a0000;006a0100=006a2e00;016a0100=2e6a2e00;016b0000=2e6b0000;006b0100=006b2e00;016b0100=2e6b2e00;016c0000=2e6c0000;006c0100=006c2e00;016c0100=2e6c2e00;016d0000=2e6d0000;006d0100=006d2e00;016d0100=2e6d2e00;016e0000=2e6e0000;006e0100=006e2e00;016e0100=2e6e2e00;016f0000=2e6f0000;006f0100=006f2e00;016f0100=2e6f2e00;01700000=2e700000;00700100=00702e00;01700100=2e702e00;01710000=2e710000;00710100=00712e00;01710100=2e712e00;01720000=2e720000;00720100=00722e00;01720100=2e722e00;01730000=2e730000;00730100=00732e00;01730100=2e732e00;01740000=2e740000;00740100=00742e00;01740100=2e742e00;01750000=2e750000;00750100=00752e00;01750100=2e752e00;01760000=2e760000;00760100=00762e00;01760100=2e762e00;01770000=2e770000;00770100=00772e00;01770100=2e772e00;01780000=2e780000;00780100=00782e00;01780100=2e782e00;01790000=2e790000;00790100=00792e00;01790100=2e792e00;017a0000=2e7a0000;007a0100=007a2e00;017a0100=2e7a2e00;017b0000=2e7b0000;007b0100=007b2e00;017b0100=2e7b2e00;017c0000=2e7c0000;007c0100=007c2e00;017c0100=2e7c2e00;017d0000=2e7d0000;007d0100=007d2e00;017d0100=2e7d2e00;017e0000=2e7e0000;007e0100=007e2e00;017e0100=2e7e2e00;017f0000=2e7f0000;007f0100=007f2e00;017f0100=2e7f2e00;01800000=2e800000;00800100=00802e00;01800100=2e802e00;01810000=2e810000;00810100=00812e00;01810100=2e812e00?scale=47?crop;1;1;44;44?replace;"
        if backItem:
            drawableArmourDirectives = "?scale=0.4?scale=0.7?scale=0.84?crop;4;2;5;3?replace;aa836459=00a10000;bb885e4e=00a20000;cb926431=00a30000;cb95693b=00a40000;cf91601c=00a50000;ce966b4b=00a60000;e6c2a50c=00a70000;cc93662e=00b10000;cc8c5921=00b20000;c1895c3d=00b30000;bf885c41=00b40000;cb8e5d2d=00b50000;c7895728=00b60000;ac7c5558=00b70000;b8a99d5d=00b80000;d796610f=00c10000;dc955b0a=00c20000;de965b06=00c30000;c3885730=00c40000;d9945b0d=00c50000;dc955b08=00c60000;da945b0a=00c70000;dfbca11e=00c80000;ce8e5b23=00d10000;dc945b06=00d20000;cf8f5b23=00d30000;9d74526f=00d40000;d28f5916=00d50000;de965b02=00d60000;e0975c00=00d70000;ecc3a200=00d80000;d08f5b1e=00e10000;da945b08=00e20000;cd905f2f=00e30000;d8955e14=00e40000;cc8d5920=00e50000;59504932=00f10000;655c5509=00f20000;7369631b=00f30000;756c665a=00f40000;62574f32=00f50000;877d7782=00f60000;63595277=00f70000;a19d9959=00f80000?scale=2?blendscreen=/objects/outpost/customsign/signplaceholder.png?replace;01a10000=2ea10000;00a10100=00a12e00;01a10100=2ea12e00;01a20000=2ea20000;00a20100=00a22e00;01a20100=2ea22e00;01a30000=2ea30000;00a30100=00a32e00;01a30100=2ea32e00;01a40000=2ea40000;00a40100=00a42e00;01a40100=2ea42e00;01a50000=2ea50000;00a50100=00a52e00;01a50100=2ea52e00;01a60000=2ea60000;00a60100=00a62e00;01a60100=2ea62e00;01a70000=2ea70000;00a70100=00a72e00;01a70100=2ea72e00;01b10000=2eb10000;00b10100=00b12e00;01b10100=2eb12e00;01b20000=2eb20000;00b20100=00b22e00;01b20100=2eb22e00;01b30000=2eb30000;00b30100=00b32e00;01b30100=2eb32e00;01b40000=2eb40000;00b40100=00b42e00;01b40100=2eb42e00;01b50000=2eb50000;00b50100=00b52e00;01b50100=2eb52e00;01b60000=2eb60000;00b60100=00b62e00;01b60100=2eb62e00;01b70000=2eb70000;00b70100=00b72e00;01b70100=2eb72e00;01b80000=2eb80000;00b80100=00b82e00;01b80100=2eb82e00;01c10000=2ec10000;00c10100=00c12e00;01c10100=2ec12e00;01c20000=2ec20000;00c20100=00c22e00;01c20100=2ec22e00;01c30000=2ec30000;00c30100=00c32e00;01c30100=2ec32e00;01c40000=2ec40000;00c40100=00c42e00;01c40100=2ec42e00;01c50000=2ec50000;00c50100=00c52e00;01c50100=2ec52e00;01c60000=2ec60000;00c60100=00c62e00;01c60100=2ec62e00;01c70000=2ec70000;00c70100=00c72e00;01c70100=2ec72e00;01c80000=2ec80000;00c80100=00c82e00;01c80100=2ec82e00;01d10000=2ed10000;00d10100=00d12e00;01d10100=2ed12e00;01d20000=2ed20000;00d20100=00d22e00;01d20100=2ed22e00;01d30000=2ed30000;00d30100=00d32e00;01d30100=2ed32e00;01d40000=2ed40000;00d40100=00d42e00;01d40100=2ed42e00;01d50000=2ed50000;00d50100=00d52e00;01d50100=2ed52e00;01d60000=2ed60000;00d60100=00d62e00;01d60100=2ed62e00;01d70000=2ed70000;00d70100=00d72e00;01d70100=2ed72e00;01d80000=2ed80000;00d80100=00d82e00;01d80100=2ed82e00;01e10000=2ee10000;00e10100=00e12e00;01e10100=2ee12e00;01e20000=2ee20000;00e20100=00e22e00;01e20100=2ee22e00;01e30000=2ee30000;00e30100=00e32e00;01e30100=2ee32e00;01e40000=2ee40000;00e40100=00e42e00;01e40100=2ee42e00;01e50000=2ee50000;00e50100=00e52e00;01e50100=2ee52e00;01f10000=2ef10000;00f10100=00f12e00;01f10100=2ef12e00;01f20000=2ef20000;00f20100=00f22e00;01f20100=2ef22e00;01f30000=2ef30000;00f30100=00f32e00;01f30100=2ef32e00;01f40000=2ef40000;00f40100=00f42e00;01f40100=2ef42e00;01f50000=2ef50000;00f50100=00f52e00;01f50100=2ef52e00;01f60000=2ef60000;00f60100=00f62e00;01f60100=2ef62e00;01f70000=2ef70000;00f70100=00f72e00;01f70100=2ef72e00;01f80000=2ef80000;00f80100=00f82e00;01f80100=2ef82e00?scale=47?crop;1;1;44;44?replace;"
        if emotes:
            drawableArmourDirectives = "?crop;17;21;27;31?scale=0.7?replace;af8e7529=0000ff?scale=0.7?scale=0.7?scale=0.9?crop;2;1;3;2?replace;cc8c651c=00a100;c1735432=00a200;c57d5a26=00a300;c2735547=00a400;ca88611c=00a500;bf6e4f32=00a600;ffffff00=00a700;ca996f1d=00b100;c2825e06=00b200;a56a752a=00b300;c2825d05=00b400;c3815c03=00b500;cc8b6216=00c100;c174531c=00c200;c0705046=00c300;c06e505d=00c400;cc8b621e=00d100;c2765430=00d200;cc8b621f=00e100;c57d5811=00e200;c278551f=00e300;bf6e5041=00e400;bd684c58=00e500;ead1bd00=00f100;e6c8b714=00f200;ddb4a224=00f300;d39d8c40=00f400;d49e8c40=00f500;f0dfd924=00f600?scale=2?blendscreen=/ships/apex/apexT3blocks.png;6;20?multiply=00ffff?blendscreen=/ships/apex/apexT3blocks.png;-1;0?multiply=2eff2e00?scale=47?crop;1;1;44;44?replace;"
        if floranEmotes:
            drawableArmourDirectives = "?crop;17;21;27;31?scale=0.7?scale=0.7?scale=0.7?scale=0.9?crop;2;1;3;2?replace;9f4d351c=00a100;7f302232=00a200;7b312226=00a300;84332447=00a400;9c48301c=00a500;78281b32=00a600;e9d4cc00=00a700;9a553b27=00b100;6c2c1e06=00b200;6c2d1e06=00b300;6d2b1d05=00b400;6d2a1b03=00b500;9c493016=00c100;7427191c=00c200;7f2e1e50=00c300;852f205d=00c400;9c49301a=00d100;75281925=00d200;9c49301d=00e100;7129190f=00e200;7328191d=00e300;7d2a1d3f=00e400;862e2056=00e500;d3b2a500=00f100;c6a79d1d=00f200;bc92882b=00f300;b37b7147=00f400;b57d7347=00f500;edd9d42b=00f600?scale=2?blendscreen=/ships/apex/apexT3blocks.png;6;20?multiply=00ffff?blendscreen=/ships/apex/apexT3blocks.png;-1;0?multiply=2eff2e00?scale=47?crop;1;1;44;44?replace;"
        if bodyDirs:
            drawableArmourDirectives = "?scale=0.4?scale=0.7?scale=0.85?scale=0.925?scale=0.9625?scale=0.8?scale=0.8?crop;3;2;4;3?replace;b79b810f=ff00ff;a8896777=ff01ff;c28a638c=ff02ff;d39c6d7a=ff03ff;c78e638a=ff04ff;b4855b8d=ff05ff;b1875d82=ff06ff;b7a28b3f=ff07ff;9f7e5879=ff08ff;9d7f5b70=ff09ff;98785372=ff0aff;97774f77=ff0bff;9575516e=ff0cff;9a7e5a6a=ff0dff;9676516f=ff0eff;9b79527f=ff0fff;9d7b5689=ff10ff;98714a8c=ff11ff;9a775188=ff12ff;96775172=ff13ff;97775176=ff14ff;9c764d8e=ff15ff;9878527e=ff16ff;9a78547b=ff17ff;9e784f83=ff18ff;9a724a8c=ff19ff;9d754c93=ff1aff;99714993=ff1bff;9a764c8d=ff1cff;9b774d8a=ff1dff;97734a7f=ff1eff;98744c78=ff1fff;99785479=ff20ff;97765072=ff21ff;97744f7c=ff22ff;a1825e7f=ff23ff;95734e79=ff24ff;ae8e6a6a=ff01ff;bc9175a4=ff02ff;d7b5997e=ff03ff;c1987ba1=ff04ff;d5b29781=ff05ff;d0b1937d=ff06ff;b7a38c36=ff07ff;a1815b73=ff08ff;a2835d64=ff09ff;9b7b556c=ff0aff;9c7b536b=ff0bff;97795469=ff0cff;9f825d5f=ff0dff;9979546a=ff0eff;a07c5573=ff0fff;9e7c5789=ff10ff;97714a8c=ff11ff;9c785288=ff12ff;96765172=ff13ff;98785276=ff14ff;9b764d8e=ff15ff;9a79537e=ff16ff;9978537b=ff17ff;a07a527e=ff18ff;9c754c87=ff19ff;9f784d8e=ff1aff;9b744c8e=ff1bff;9b794e88=ff1cff;9c794f85=ff1dff;98764d7a=ff1eff;99764e73=ff1fff;9a78546f=ff20ff;98765068=ff21ff;9e7b5377=ff22ff;a4856076=ff23ff;9c785273=ff24ff;ded3c91c=ff25ff;dfac8215=ff26ff;e1aa7d0b=ff27ff;e0a97d10=ff28ff;f3eae310=ff29ff;87725109=ff2aff;7d603b3e=ff2bff;7c613b3a=ff2cff;77593735=ff2dff;775e3a19=ff2eff;755f3b10=ff2fff;82664130=ff30ff;7f643e34=ff31ff;83663f45=ff32ff;785c3835=ff33ff;775f3a1c=ff34ff;745d3915=ff35ff;7c603d2b=ff36ff;765d3913=ff37ff;735c390c=ff38ff;745e390c=ff39ff;735d3908=ff3aff;725d3905=ff3bff;725c3805=ff3cff;745c3903=ff3dff;f2edea18=ff3eff;f0e9e41f=ff3fff;f6f2f00f=ff40ff;e9ded733=ff41ff;ebe3dc2a=ff42ff;f1eae51e=ff43ff;f8f4f20f=ff44ff;f3ece81a=ff45ff;fbf8f708=ff46ff;d7bfa74a=ff47ff;e3d0c425=ff48ff;bd7f6424=ff49ff;bf806519=ff4aff;bf896f2a=ff4bff;8a735112=ff4cff;735e3a00=ff4dff;795f3a15=ff50ff;765c3815=ff51ff;7c5f3924=ff52ff;765b371a=ff55ff;7b5f392c=ff56ff;735b3717=ff57ff;b69c8118=ff58ff;785c3821=ff59ff;7b5f3b1c=ff5aff;785d391c=ff5bff;725a3716=ff5cff;765f3a0b=ff5dff;765f3a0a=ff5eff;745a360d=ff5fff;f2edeb14=ff60ff;f7efe81f=ff61ff;f5f0ed15=ff62ff;efe7e61a=ff63ff;f6f0ed13=ff64ff;f7f2ef11=ff65ff;fcf9f708=ff66ff;f0e4d935=ff67ff;eee4e121=ff68ff?scale=2?blendmult=/dungeons/other/wreck/key.png;748;30?blendmult=/monsters/boss/apeboss/apeboss.png;1262;395?multiply=2eff2e00?scale=47?crop;1;1;44;44?replace;"
        if False:
            pass
        else:
            if not ( headItem or headMask ):
                if backItem:
                    try:
                        sheet = Image.open("backitemtemplate.png").convert("RGBA")
                        sheetSize = sheet.size
                        sheetPixels = sheet.load()
                    except:
                        print("Template missing or invalid.")
                    else:
                        requiredImageSize = sheetSize
                        if framesheetSize != requiredImageSize:
                            print("Input image is of the wrong size for a back item.")
                            return None
                        else:
                            for x in range(0, sheetSize[0]):
                                for y in range(0, sheetSize[1]):
                                    sheetPixel = []
                                    try:
                                        sheetPixel = sheetPixels[x, y]
                                        imagePixel = framesheetPixels[x, y]
                                    except IndexError:
                                        pass
                                    else:
                                        if imagePixel[3]:
                                            hexString = ""
                                            for colourValue in sheetPixel:
                                                hexNumber = hex(colourValue)[2:] if len(hex(colourValue)[2:]) == 2 else "0" + hex(colourValue)[2:]
                                                hexString = hexString + hexNumber
                                            checkString = hexString
                                            hexString = hexString + "="
                                            for colourValue in imagePixel:
                                                hexNumber = hex(colourValue)[2:] if len(hex(colourValue)[2:]) == 2 else "0" + hex(colourValue)[2:]
                                                hexString = hexString + hexNumber
                                            hexString = hexString + ";"
                                            if checkString != "ffffff00":
                                                drawableArmourDirectives = drawableArmourDirectives + hexString
                elif emotes or floranEmotes:
                    try:
                        sheet = Image.open("emotetemplate.png").convert("RGBA")
                        sheetSize = sheet.size
                        sheetPixels = sheet.load()
                    except:
                        print("Template missing or invalid.")
                    else:
                        requiredImageSize = sheetSize
                        if framesheetSize != requiredImageSize:
                            print("Input image is of the wrong size for emote directives.")
                            return None
                        else:
                            for x in range(0, sheetSize[0]):
                                for y in range(0, sheetSize[1]):
                                    sheetPixel = []
                                    try:
                                        sheetPixel = sheetPixels[x, y]
                                        imagePixel = framesheetPixels[x, y]
                                    except IndexError:
                                        pass
                                    else:
                                        if imagePixel[3]:
                                            hexString = ""
                                            for colourValue in sheetPixel:
                                                hexNumber = hex(colourValue)[2:] if len(hex(colourValue)[2:]) == 2 else "0" + hex(colourValue)[2:]
                                                hexString = hexString + hexNumber
                                            checkString = hexString
                                            hexString = hexString + "="
                                            for colourValue in imagePixel:
                                                hexNumber = hex(colourValue)[2:] if len(hex(colourValue)[2:]) == 2 else "0" + hex(colourValue)[2:]
                                                hexString = hexString + hexNumber
                                            hexString = hexString + ";"
                                            if checkString != "ffffff00":
                                                drawableArmourDirectives = drawableArmourDirectives + hexString
                elif sleevesItem:
                    try:
                        sheet = Image.open("sleevesitemtemplate.png").convert("RGBA")
                        sheetSize = sheet.size
                        sheetPixels = sheet.load()
                    except:
                        print("Template missing or invalid.")
                    else:
                        requiredImageSize = sheetSize
                        if framesheetSize != requiredImageSize:
                            print("Input image is of the wrong size for a sleeves item.")
                            return None
                        else:
                            for x in range(0, sheetSize[0]):
                                for y in range(0, sheetSize[1]):
                                    sheetPixel = []
                                    try:
                                        sheetPixel = sheetPixels[x, y]
                                        imagePixel = framesheetPixels[x, y]
                                    except IndexError:
                                        pass
                                    else:
                                        if imagePixel[3]:
                                            hexString = ""
                                            for colourValue in sheetPixel:
                                                hexNumber = hex(colourValue)[2:] if len(hex(colourValue)[2:]) == 2 else "0" + hex(colourValue)[2:]
                                                hexString = hexString + hexNumber
                                            checkString = hexString
                                            hexString = hexString + "="
                                            for colourValue in imagePixel:
                                                hexNumber = hex(colourValue)[2:] if len(hex(colourValue)[2:]) == 2 else "0" + hex(colourValue)[2:]
                                                hexString = hexString + hexNumber
                                            hexString = hexString + ";"
                                            if checkString != "ffffff00":
                                                drawableArmourDirectives = drawableArmourDirectives + hexString
                elif bodyDirs:
                    try:
                        sheet = Image.open("bodytemplate.png").convert("RGBA")
                        sheetSize = sheet.size
                        sheetPixels = sheet.load()
                    except:
                        print("Template missing or invalid.")
                    else:
                        requiredImageSize = sheetSize
                        if framesheetSize != requiredImageSize:
                            print(
                                "Input image is of the wrong size for body directives.")
                            return None
                        else:
                            for x in range(0, sheetSize[0]):
                                for y in range(0, sheetSize[1]):
                                    sheetPixel = []
                                    try:
                                        sheetPixel = sheetPixels[x, y]
                                        imagePixel = framesheetPixels[x, y]
                                    except IndexError:
                                        pass
                                    else:
                                        if imagePixel[3]:
                                            hexString = ""
                                            for colourValue in sheetPixel:
                                                hexNumber = hex(colourValue)[2:] if len(hex(colourValue)[
                                                    2:]) == 2 else "0" + hex(colourValue)[2:]
                                                hexString = hexString + hexNumber
                                            checkString = hexString
                                            hexString = hexString + "="
                                            for colourValue in imagePixel:
                                                hexNumber = hex(colourValue)[2:] if len(hex(colourValue)[
                                                    2:]) == 2 else "0" + hex(colourValue)[2:]
                                                hexString = hexString + hexNumber
                                            hexString = hexString + ";"
                                            if checkString != "ffffff00":
                                                drawableArmourDirectives = drawableArmourDirectives + hexString
                else:
                    try:
                        sheet = Image.open("chestitemtemplate.png").convert("RGBA")
                        sheetSize = sheet.size
                        sheetPixels = sheet.load()
                    except:
                        print("Template missing or invalid.")
                    else:
                        requiredImageSize = sheetSize
                        if framesheetSize != requiredImageSize:
                            print("Input image is of the wrong size for a chest/legs item.")
                            return None
                        else:
                            for x in range(0, sheetSize[0]):
                                for y in range(0, sheetSize[1]):
                                    sheetPixel = []
                                    try:
                                        sheetPixel = sheetPixels[x, y]
                                        imagePixel = framesheetPixels[x, y]
                                    except IndexError:
                                        pass
                                    else:
                                        if imagePixel[3]:
                                            hexString = ""
                                            for colourValue in sheetPixel:
                                                hexNumber = hex(colourValue)[2:] if len(hex(colourValue)[2:]) == 2 else "0" + hex(colourValue)[2:]
                                                hexString = hexString + hexNumber
                                            checkString = hexString
                                            hexString = hexString + "="
                                            for colourValue in imagePixel:
                                                hexNumber = hex(colourValue)[2:] if len(hex(colourValue)[2:]) == 2 else "0" + hex(colourValue)[2:]
                                                hexString = hexString + hexNumber
                                            hexString = hexString + ";"
                                            if checkString != "ffffff00":
                                                drawableArmourDirectives = drawableArmourDirectives + hexString
            else:
                framePixels = framesheetFile.transpose(1).load()
                if headMask:
                    for x in range(0, 43):
                        for y in range(0, 43):
                            framePixel = []
                            try:
                                framePixel = framePixels[x, y]
                                # if framePixel[3] > 0 and framePixel[3] < 255:
                                #     print(framePixel)
                            except IndexError:
                                pass
                            else:
                                if framePixel[3]:
                                    drawableArmourDirectives = drawableArmourDirectives + "?addmask=/particles/ash/3.png;" + str(x) + ";" + str(y)
                else:
                    for x in range(0, 43):
                        for y in range(0, 43):
                            framePixel = []
                            try:
                                framePixel = framePixels[x, y]
                                # if framePixel[3] > 0 and framePixel[3] < 255:
                                #     print(framePixel)
                            except IndexError:
                                pass
                            else:
                                if framePixel[3]:
                                    hexString = ""
                                    for colourValue in framePixel:
                                        hexNumber = hex(colourValue)[2:] if len(hex(colourValue)[2:]) == 2 else "0" + hex(colourValue)[2:]
                                        hexString = hexString + hexNumber
                                    hexString = ( "0" + hex(x)[2:] if len(hex(x)[2:]) == 1 else hex(x)[2:] ) + "00" \
                                        + ( "0" + hex(y)[2:] if len(hex(y)[2:]) == 1 else hex(y)[2:] ) + "00=" + hexString + ";"
                                    drawableArmourDirectives = drawableArmourDirectives + hexString
            inventoryIcon = "pants.png:idle.1"
            itemName = "florantier6apants"
            itemCategory = "Custom Chest and Pants"
            if headItem:
                inventoryIcon = "head.png:normal"
                itemName = "coolfezhead"
                itemCategory = "Custom Hat"
            if sleevesItem:
                inventoryIcon = "fsleeve.png:idle.1"
                itemName = "aviantier6schest"
                itemCategory = "Custom Sleeves"
            if backItem:
                inventoryIcon = "back.png:idle.1"
                itemName = "tigertailback"
                itemCategory = "Custom Backwear"
            itemDescriptor = JsonDict({
                "name": itemName,
                "count": 1,
                "parameters": {
                    "description": "Custom clothing generated with FezzedOne's Drawable Generator.",
                    "shortdescription": "^orange;Custom Clothing^reset;",
                    "category": itemCategory,
                    "directives": drawableArmourDirectives[:-1], # Remove last semicolon from directive string.
                    "inventoryIcon": inventoryIcon,
                    "leveledStatusEffects": [],
                    "statusEffects": [],
                    # "tooltipFields": {
                    #     "rarityLabel": "fezTech Armour"
                    # },
                    "rarity": "Essential"
                }
            })
            if emotes or floranEmotes or bodyDirs:
                itemDescriptor = JsonDict({
                    "directives": drawableArmourDirectives[:-1]
                })
            directiveOutputFile = open(directiveFileName, "w")
            try:
                itemOutput = itemDescriptor.convertToJson()
            except:
                print("An error occurred during item output.")
            else:
                directiveOutputFile.write(itemOutput)
                return itemOutput
            finally:
                directiveOutputFile.close()


def convertToDrawables(imageToConvert, jsonFileName, scale="1", shipX="0", shipY="0", returnShipDrawables=False, returnSigns=False, returnAnimated=False, returnRawSigns=False):
    try:
        imagePixels = imageToConvert.load()
        scaleFloat = float(scale)
        shipXFloat = float(shipX) if ( shipX != "" ) else 0
        shipYFloat = float(shipY) if ( shipY != "" ) else 0
    except:
        print("Image conversion error of some sort. Maybe the first argument is not actually a PNG image? Also, be sure your other arguments are input correctly.")
        return None
    else:
        drawables = JsonList()
        if scaleFloat >= 0.1 or scaleFloat <= 10.0:
            if returnShipDrawables or returnSigns or returnRawSigns:
                numSigns = 0
                drawableLines = ""
                for sign in signCrop(imageToConvert):
                    numSigns += 1
                    signPixels = sign[0].load()
                    signDrawableString = "?replace;"
                    for x in range(0, 32):
                        for y in range(0, 8):
                            hexString = ""
                            try:
                                signPixel = signPixels[x, y]
                            except IndexError:
                                pass
                            else:
                                if signPixel[3]:
                                    for colourValue in signPixel:
                                        hexNumber = hex(colourValue)[2:] if len(hex(colourValue)[2:]) == 2 else "0" + hex(colourValue)[2:]
                                        hexString = hexString + hexNumber
                                    hexString = ( "0" + str(x + 1) if len(str(x + 1)) == 1 else str(x + 1) ) + "00" \
                                        + ( "0" + str(y + 1) if len(str(y + 1)) == 1 else str(y + 1) ) + "01=" + hexString + ";"
                                    # The sign format is rather weird, so this is what must be done.
                                    signDrawableString = signDrawableString + hexString
                    if not returnRawSigns:
                        if len(signDrawableString) > 9:
                            drawables.append({
                                "image": "/objects/outpost/customsign/signplaceholder.png" + signDrawableString[:-1],
                                "position": [ ( sign[1] * 4 + shipXFloat if returnShipDrawables else sign[1] * 4 * 8 ), ( sign[2] + shipYFloat if returnShipDrawables else sign[2] * 8 ) ]
                            })
                    else:
                        drawableLines = drawableLines + "/objects/outpost/customsign/signplaceholder.png" + signDrawableString[:-1] + "\n"
                if returnRawSigns:
                    rawFile = open(jsonFileName, "w")
                    print(str(numSigns) + " drawable sign(s) generated.")
                    rawFile.write(drawableLines[:-1])
                    rawFile.close()
                else:
                    jsonFile = open(jsonFileName, "w")
                    try:
                        convertedDrawables = drawables.convertToJson()
                    except:
                        print("An error occurred during drawable output.")
                    else:
                        print(str(numSigns) + " drawable sign(s) generated (some may not be in final output).")
                        jsonFile.write(convertedDrawables)
                        return convertedDrawables
                    finally:
                        jsonFile.close()
            elif returnAnimated and not ( returnShipDrawables or returnSigns ):
                for frame in frameCrop(imageToConvert):
                    framePixels = frame[0].load()
                    frameDrawableString = "?replace;"
                    for x in range(0, (64 if large else 32)):
                        for y in range(0, (64 if large else 32)):
                            hexString = ""
                            try:
                                framePixel = framePixels[x, y]
                            except IndexError:
                                pass
                            else:
                                if framePixel[3]:
                                    for colourValue in framePixel:
                                        hexNumber = hex(colourValue)[2:] if len(hex(colourValue)[2:]) == 2 else "0" + hex(colourValue)[2:]
                                        hexString = hexString + hexNumber
                                    hexString = ( ( hex(x + 1)[2:] if len(hex(x + 1)[2:]) == 2 else "0" + hex(x + 1)[2:] ) ) \
                                        + ( ( hex(y + 1)[2:] if len(hex(y + 1)[2:]) == 2 else "0" + hex(y + 1)[2:] ) ) + "0001=" + hexString
                                    frameDrawableString = frameDrawableString + hexString
                    if len(frameDrawableString) > 9:
                        drawables.append({
                            "frameNum": frame[1],
                            "frameDirectives": frameDrawableString[:-1]
                        })
                jsonFile = open(jsonFileName, "w")
                try:
                    convertedDrawables = drawables.convertToJson()
                except:
                    print("An error occurred during drawable output.")
                else:
                    jsonFile.write(convertedDrawables)
                    return convertedDrawables
                finally:
                    jsonFile.close()
            elif not ( returnShipDrawables or returnSigns or returnAnimated ):
                for x in range(0, imageToConvert.size[0]):
                    for y in range(0, imageToConvert.size[1]):
                        hexString = ""
                        for colourValue in imagePixels[x, y]:
                            hexNumber = hex(colourValue)[2:] if len(hex(colourValue)[2:]) == 2 else "0" + hex(colourValue)[2:]
                            hexString = hexString + hexNumber
                        drawables.append({
                            "image": "/particles/ash/3.png?setcolor=" + hexString + "?scalenearest=" + str(scaleFloat),
                            "position": [x * scaleFloat, y * scaleFloat]
                        })
                jsonFile = open(jsonFileName, "w")
                try:
                    convertedDrawables = drawables.convertToJson()
                except:
                    print("An error occurred during drawable output.")
                else:
                    jsonFile.write(convertedDrawables)
                    return convertedDrawables
                finally:
                    jsonFile.close()
        else:
            print("Scale is either too large or too small.")
            return False
    finally:
        pass


def transposeDrawables(sourceImagePath, targetImagePath, outputFilePath):
    if not ( outputFilePath or sourceImagePath or targetImagePath ):
        print("Specify valid paths to all three required files.")
    else:
        try:
            sourceImageFile = Image.open(sourceImagePath).convert("RGBA")
            targetImageFile = Image.open(targetImagePath).convert("RGBA")
        except:
            print("Error loading images.")
        else:
            sourceImageSize = sourceImageFile.size
            targetImageSize = targetImageFile.size
            sourceImage = sourceImageFile.load()
            targetImage = targetImageFile.load()
            if sourceImageSize != targetImageSize:
                print("Images must be of the same size.")
            else:
                drawableString = "?replace;"
                for x in range(0, sourceImageSize[0]):
                    for y in range(0, sourceImageSize[1]):
                        hexString = ""
                        for colourValue in sourceImage[x, y]:
                            hexNumber = hex(colourValue)[2:] if len(hex(colourValue)[2:]) == 2 else "0" + hex(colourValue)[2:]
                            hexString = hexString + hexNumber
                        hexString = hexString + "="
                        for colourValue in targetImage[x, y]:
                            hexNumber = hex(colourValue)[2:] if len(hex(colourValue)[2:]) == 2 else "0" + hex(colourValue)[2:]
                            hexString = hexString + hexNumber
                        hexString = hexString + ";"
                        drawableString = drawableString + hexString
                try:
                    outputFile = open(outputFilePath, "w")
                except:
                    print("Could not open output file for writing.")
                else:
                    outputFile.write(drawableString[:-1])
                    outputFile.close()


def main():
    try:
        imageFile = sys.argv[1]
    except IndexError:
        imageFile = None
        print("Missing image file path argument.")
    try:
        option = sys.argv[2]
    except IndexError:
        option = ""
    try:
        arg1, arg2 = sys.argv[3], sys.argv[4]
    except IndexError:
        arg1, arg2 = "", ""
    if imageFile:
        imageFileName, imageFileExt = os.path.splitext(imageFile)
        jsonFileName = imageFileName + ".json"
        print("Drawables will be exported to " + jsonFileName)
        if imageFile == "--help":
            print("""HELP FOR RENO'S DRAWABLE CONVERTER

            reno-drawable-converter <path to PNG image> <option>

            Outputs Starbound image drawables in a JSON file which has the same name as the image. E.g:
                reno-drawable-converter someimage.png
            will cause the output to be saved to someimage.json. Only the first option argument will do anything.
            Only PNG images will work with the converter. If you have a non-PNG image you wish to convert, export
            it as PNG with your preferred image editor or format converter.

            Use --version or -v without a file argument to display the version number.

            If no options are added, the script will output particle drawables by default.

            OPTIONS
                --sign
                    Outputs drawables in sign format. Useful for image drawables larger than
                    about 100x100. Use this option to reduce lag when displaying the drawables.
                --rawsign
                    Outputs drawables in raw sign format. Useful for directive scripting.
                --shipworld [baseX] [baseY]
                    Outputs drawables that can be used in shipworld .structure files. Great
                    for making custom ships. baseX and baseY may be omitted, but should be
                    set to the coordinates used to place shipship.png in the .structure file
                    generated by your dungeon editing programme.
                --scale <number>
                    Scales the drawable output. Does not work with any of the above options.
                    The scale must be between 0.1 and 10, inclusive. Try 0.5 for one-pixel
                    drawables or 1.5 for Minecraft-like drawables.
                --anim
                    Outputs frame directives compatible with Silverfeelin's animation API.
                --armour
                    Outputs a drawable armour item descriptor.
                --sleeves
                    Outputs a drawable sleeves item descriptor.
                --back
                    Outputs a drawable back item descriptor.
                --hat
                    Outputs a drawable hat item descriptor.
                --emotes
                    Outputs emote directives.
                --floranemotes
                    Outputs floran emote directives.
                --body
                    Outputs body directives.
                --transpose <targetImageFile> <outputFile>
                    Outputs transposed directives. Generally used with in-game directive canvases.
                    Argument before `--transpose` is the source image file.

            """)
        elif imageFile == "--version" or imageFile == "-v":
            print("Reno's Drawable Generator -- version 2.0")
        elif imageFileExt.lower() == ".png":
            if option == "--shipworld":
                convertToDrawables(Image.open(imageFile).convert("RGBA").transpose(1), jsonFileName, scale="1", returnShipDrawables=True, shipX=arg1, shipY=arg2)
            elif option == "--sign":
                convertToDrawables(Image.open(imageFile).convert("RGBA").transpose(1), jsonFileName, scale="1", returnSigns=True)
            elif option == "--rawsign":
                convertToDrawables(Image.open(imageFile).convert("RGBA").transpose(1), jsonFileName, scale="1", returnRawSigns=True)
            elif option == "--anim":
                convertToDrawables(Image.open(imageFile).convert("RGBA").transpose(1), jsonFileName, scale="1", returnAnimated=True)
            elif option == "--scale":
                convertToDrawables(Image.open(imageFile).convert("RGBA").transpose(1), jsonFileName, scale=arg1)
            elif option == "--armour":
                drawableArmour(imageFile, jsonFileName, headItem=False, sleevesItem=False, backItem=False, headMask=False, emotes=False, floranEmotes=False, bodyDirs=False)
            elif option == "--hat":
                drawableArmour(imageFile, jsonFileName, headItem=True, sleevesItem=False, backItem=False, headMask=False, emotes=False, floranEmotes=False, bodyDirs=False)
            elif option == "--mask":
                drawableArmour(imageFile, jsonFileName, headItem=False, sleevesItem=False, backItem=False, headMask=True, emotes=False, floranEmotes=False, bodyDirs=False)
            elif option == "--sleeves":
                drawableArmour(imageFile, jsonFileName, headItem=False, sleevesItem=True, backItem=False, headMask=False, emotes=False, floranEmotes=False, bodyDirs=False)
            elif option == "--back":
                drawableArmour(imageFile, jsonFileName, headItem=False, sleevesItem=False, backItem=True, headMask=False, emotes=False, floranEmotes=False, bodyDirs=False)
            elif option == "--emotes":
                drawableArmour(imageFile, jsonFileName, headItem=False, sleevesItem=False, backItem=False, headMask=False, emotes=True, floranEmotes=False, bodyDirs=False)
            elif option == "--floranemotes":
                drawableArmour(imageFile, jsonFileName, headItem=False, sleevesItem=False, backItem=False, headMask=False, emotes=False, floranEmotes=True, bodyDirs=False)
            elif option == "--body":
                drawableArmour(imageFile, jsonFileName, headItem=False, sleevesItem=False, backItem=False, headMask=False, emotes=False, floranEmotes=False, bodyDirs=True)
            elif option == "--transpose":
                if ( arg1 != "" ) and ( arg2 != "" ):
                    transposeDrawables(imageFile, arg1, arg2)
                else:
                    print("Missing target image file and output file path arguments.")
            else:
                convertToDrawables(Image.open(imageFile).convert("RGBA").transpose(1), jsonFileName, scale="1")


if __name__ == "__main__":
    main()
