import xml.etree.ElementTree as ET
from problem_visuals.graphics.svg_handling import SvgProducer

ZONES = {
    "WA": """<path id="western-australia" d="m328.75119,368.37956c0,0 -18.02565,12.87546 -18.02565,12.87546c0,0 -24.89256,2.14591 -24.89256,2.14591c0,0 -19.74238,9.44201 -20.16927,9.30069c0.42689,0.14132 -6.8692,7.43742 -6.8692,7.8666c0,0.42918 -3.86264,8.58364 -3.86264,8.58364c0,0 -23.17583,3.43346 -23.60272,3.29214c0.42689,0.14132 -12.44857,2.28723 -12.44857,2.28723c0,0 -18.45483,5.57937 -18.88172,5.43805c0.42689,0.14132 -3.43575,7.00823 -3.43575,7.00823c0,0 -12.44628,10.72955 -12.87546,11.15873c-0.42918,0.42918 -22.31747,1.28755 -22.74436,1.14623c0.42689,0.14132 -21.4614,-9.72987 -21.88829,-9.87119c0.42689,0.14132 -1.71902,-11.87578 -2.14591,-12.0171c0.42689,0.14132 7.72299,-6.72559 7.72299,-6.72559c0,0 -2.57509,-12.44628 -2.57509,-12.44628c0,0 3.86264,-12.0171 3.86264,-12.0171c0,0 -7.2961,-10.72955 -7.72299,-10.87087c0.42689,0.14132 -11.16103,-29.04306 -11.58792,-29.18438c0.42689,0.14132 -14.1653,-24.32206 -14.59219,-24.46338c0.42689,0.14132 -21.89058,-31.18897 -22.31747,-31.33029c0.42689,0.14132 16.30663,1.85805 16.30663,1.85805c0,0 -13.30464,-24.0342 -13.30464,-24.0342c0,0 2.57509,-18.02565 2.1482,-18.16697c0.42689,0.14132 -0.00229,-16.1676 -0.00229,-16.1676c0,0 4.721,-4.29182 4.721,-4.29182c0,0 5.57937,0.85836 5.57937,0.85836c0,0 30.47193,-27.46765 30.47193,-27.46765c0,0 12.44628,-2.57509 12.44628,-2.57509c0,0 5.57937,-6.43773 5.15248,-6.57905c0.42689,0.14132 8.15217,0.5705 8.15217,0.5705c0,0 6.00855,-8.58364 5.58166,-8.72496c0.42689,0.14132 13.30235,0.5705 13.30235,0.5705c0,0 19.74238,-10.30037 19.31549,-10.44169c0.42689,0.14132 11.58563,-20.45942 11.15873,-20.60074c0.42689,0.14132 4.71871,-3.29214 4.71871,-3.29214c0,0 -4.29182,-15.02137 -4.71871,-15.16269c0.42689,0.14132 14.16072,-15.73842 13.73383,-15.87974c0.42689,0.14132 9.01053,14.30433 8.58364,14.16301c0.42689,0.14132 4.71871,-2.43377 4.71871,-2.43377c0,0 -1.28755,-7.2961 -1.28755,-7.2961c0,0 -8.15446,-7.2961 -8.58135,-7.43742c0.42689,0.14132 17.59417,1.42887 17.59417,1.42887c0,0 3.43346,-7.72528 3.43346,-7.72528c0,0 -4.721,-6.86691 -5.14789,-7.00823c0.42689,0.14132 7.72299,-5.43805 7.72299,-5.43805c0,0 6.86691,-5.15019 6.86691,-5.15019c0,0 9.01282,-9.87119 9.01282,-9.87119c0,0 16.7381,-9.01282 16.31121,-9.15414c0.42689,0.14132 12.87317,2.28723 12.44628,2.14591c0.42689,0.14132 9.43971,10.44169 9.43971,10.44169c0,0 2.14591,5.15019 2.14591,5.15019c0,0 12.87546,0.42918 12.87546,0.42918c0,0 8.15446,275.10572 8.15446,275.10572z" opacity="NaN" stroke="#000" fill="#fff"/>""",
    "NT": """<path id="northern-territory" d="m320.16755,92.41546c0,0 6.00855,0.85836 6.00855,0.85836c0,0 0.85836,-4.721 0.43147,-4.86231c0.42689,0.14131 -3.00657,-4.5797 -3.43346,-4.721c0.42689,0.14131 4.71871,-6.72561 4.71871,-6.72561c0,0 2.57509,-8.58364 2.57509,-8.58364c0,0 6.86691,-1.71673 6.86691,-1.71673c0,0 0.85836,-3.86264 0.43147,-4.00395c0.42689,0.14131 -3.43575,-3.72133 -3.86264,-3.86264c0.42689,0.14131 13.73154,-13.59252 13.73154,-13.59252c0,0 6.86691,-2.57509 6.86691,-2.57509c0,0 6.43773,2.57509 6.43773,2.57509c0,0 12.0171,-1.71673 12.0171,-1.71673c0,0 2.14591,-3.00427 1.71902,-3.14558c0.42689,0.14131 -3.00657,-5.43806 -3.00657,-5.43806c0,0 -8.58364,-5.57937 -9.01053,-5.72067c0.42689,0.14131 10.29808,-2.0046 10.29808,-2.0046c0,0 3.86264,2.57509 3.86264,2.57509c0,0 7.2961,5.15019 7.2961,5.15019c0,0 9.87119,1.71673 9.87119,1.71673c0,0 18.02565,4.721 18.02565,4.721c0,0 8.15446,2.57509 8.15446,2.57509c0,0 24.0342,-18.02565 24.0342,-18.02565c0,0 -0.85836,6.43773 -0.85836,6.43773c0,0 -12.44628,10.30037 -12.44628,10.30037c0,0 17.16728,0.85836 17.16728,0.85836c0,0 -6.86691,13.30464 -6.86691,13.30464c0,0 -2.57509,7.2961 -3.00198,7.15479c0.42689,0.14131 -8.15675,0.14131 -8.15675,0.14131c0,0 0.85836,5.15019 0.85836,5.15019c0,0 -3.43346,10.72955 -3.86035,10.58824c0.42689,0.14131 -3.00657,10.87086 -3.00657,10.87086c0,0 10.30037,12.44628 10.30037,12.44628c0,0 4.29182,0 4.29182,0c0,0 9.44201,7.2961 9.44201,7.2961c0,0 13.30464,10.30037 13.30464,10.30037c0,0 -4.721,152.78882 -5.14789,152.64752c0.42689,0.14131 -130.90283,-1.14624 -130.90283,-1.14624c0,0 -5.15019,-179.8273 -5.15019,-179.8273z" opacity="NaN" stroke="#000" fill="#fff"/>""",
    "Q": """<path id="queensland" d="m461.04866,121.84769c0,0 16.10487,3.74532 16.10487,3.74532c0,0 2.62172,4.49438 2.62172,4.49438c0,0 -0.37453,4.49438 -0.37453,4.49438c0,0 11.23595,4.49438 11.23595,4.49438c0,0 10.48689,-2.62172 10.48689,-2.62172c0,0 11.23595,-18.35206 11.23595,-18.35206c0,0 5.99251,-18.35206 5.618,-18.47691c0.3745,0.12485 -1.87269,-15.98002 -1.87269,-15.98002c0,0 2.24719,-17.22846 2.24719,-17.22846c0,0 5.24345,-7.1161 5.24345,-7.1161c0,0 -1.1236,-10.86142 -1.1236,-10.86142c0,0 14.60674,-25.8427 14.23224,-25.96755c0.3745,0.12485 7.11608,10.98627 7.11608,10.98627c0,0 -0.37453,9.3633 -0.37453,9.3633c0,0 5.24345,6.36704 5.24345,6.36704c0,0 -2.62172,4.49438 -2.62172,4.49438c0,0 5.24345,4.49438 5.24345,4.49438c0,0 -0.74906,5.24345 -0.74906,5.24345c0,0 2.24719,5.61798 2.24719,5.61798c0,0 1.1236,19.85019 1.1236,19.85019c0,0 2.99625,1.49813 2.99625,1.49813c0,0 9.3633,-3.74532 9.3633,-3.74532c0,0 3.37079,7.49064 3.37079,7.49064c0,0 8.61423,4.49438 8.61423,4.49438c0,0 -1.49813,7.49064 -1.49813,7.49064c0,0 -0.74906,5.24345 -0.74906,5.24345c0,0 3.74532,8.98876 3.37082,8.86392c0.3745,0.12485 -1.87269,4.2447 -1.87269,4.2447c0,0 7.49064,10.86142 7.49064,10.86142c0,0 2.24719,11.98502 2.24719,11.98502c0,0 -3.37079,6.74157 -3.37079,6.74157c0,0 5.61798,4.49438 5.61798,4.49438c0,0 -1.49813,7.1161 -1.49813,7.1161c0,0 5.99251,8.2397 5.61801,8.11486c0.3745,0.12485 10.86139,4.2447 10.86139,4.2447c0,0 2.99625,7.1161 2.99625,7.1161c0,0 11.23595,5.99251 11.23595,5.99251c0,0 5.24345,6.36704 5.24345,6.36704c0,0 2.99625,8.98876 2.62175,8.86392c0.3745,0.12484 4.86888,24.46941 4.86888,24.46941c0,0 3.74532,-4.86891 3.74532,-4.86891c0,0 3.74532,6.36704 3.74532,6.36704c0,0 5.24345,-1.87266 5.24345,-1.87266c0,0 5.24345,12.35955 5.24345,12.35955c0,0 -2.24719,6.74157 -2.24719,6.74157c0,0 5.61798,5.61798 5.61798,5.61798c0,0 1.87266,6.36704 1.87266,6.36704c0,0 9.73783,10.86142 9.73783,10.86142c0,0 5.24345,9.73783 5.24345,9.73783c0,0 4.11985,7.86517 4.11985,7.86517c0,0 1.1236,13.10861 1.1236,13.10861c0,0 -2.62172,8.2397 -2.62172,8.2397c0,0 -0.37453,14.98127 -0.37453,14.98127c0,0 0.74906,6.74157 0.74906,6.74157c0,0 -8.98876,0.74906 -9.36326,0.62422c0.3745,0.12484 -10.48692,0.49937 -10.48692,0.49937c0,0 -2.62172,5.61798 -2.62172,5.61798c0,0 -6.74157,1.87266 -6.74157,1.87266c0,0 -3.74532,2.24719 -3.74532,2.24719c0,0 -6.74157,-7.86517 -7.11607,-7.99001c0.3745,0.12484 -5.61801,0.12484 -5.99251,0c0.3745,0.12484 -7.11614,-2.49688 -7.49064,-2.62172c0.3745,0.12484 -4.49441,3.12109 -4.49441,3.12109c0,0 -6.36704,0.37453 -6.74154,0.24969c0.3745,0.12484 -4.86894,1.24844 -4.86894,1.24844c0,0 -108.61423,-12.73408 -108.61423,-12.73408c0,0 4.86891,-46.06741 4.86891,-46.06741c0,0 -43.44569,-5.61798 -43.44569,-5.61798c0,0 5.24345,-151.68539 5.24345,-151.68539z" opacity="NaN" stroke="#000" fill="#fff"/>""",
    "SA": """<path id="south-australia" d="m328.75119,368.80874c0,0 19.31319,0.42918 19.31319,0.42918c0,0 6.86691,-3.43346 6.86691,-3.43346c0,0 15.87974,8.58364 15.87974,8.58364c0,0 6.86691,0 6.86691,0c0,0 7.72528,5.15019 7.72528,5.15019c0,0 4.721,-0.85836 4.721,-0.85836c0,0 6.00855,3.86264 6.00855,3.86264c0,0 -1.71673,4.29182 -1.71673,4.29182c0,0 9.01282,9.44201 9.01282,9.44201c0,0 6.00855,8.15446 6.00855,8.15446c0,0 4.721,16.7381 4.721,16.7381c0,0 7.2961,-1.71673 7.2961,-1.71673c0,0 6.43773,-11.15873 6.01084,-11.30005c0.42689,0.14132 7.72299,-4.1505 7.72299,-4.1505c0,0 7.2961,-9.44201 6.86921,-9.58333c0.42689,0.14132 5.14789,-8.44232 5.14789,-8.44232c0,0 0,12.87546 0,12.87546c0,0 -6.00855,16.30892 -6.00855,16.30892c0,0 -8.58364,14.16301 -8.58364,14.16301c0,0 6.00855,0.42918 6.00855,0.42918c0,0 5.15019,-4.721 4.72329,-4.86232c0.42689,0.14132 4.71871,-8.8715 4.29182,-9.01282c0.42689,0.14132 1.28525,-3.29214 1.28525,-3.29214c0,0 6.00855,10.30037 5.58166,10.15905c0.42689,0.14132 -2.57738,8.29578 -2.57738,8.29578c0,0 -0.42918,5.15019 -0.42918,5.15019c0,0 6.00855,-0.85836 6.00855,-0.85836c0,0 5.57937,-2.14591 5.57937,-2.14591c0,0 0.42918,8.15446 0.42918,8.15446c0,0 8.15446,15.45056 8.15446,15.45056c0,0 -3.86264,11.15873 -3.86264,11.15873c0,0 19.31319,14.16301 19.31319,14.16301c0,0 10.72955,-204.71986 10.30266,-204.86118c0.42689,0.14132 -40.77459,-3.29214 -40.77459,-3.29214c0,0 -130.90054,-1.28755 -130.90054,-1.28755c0,0 3.00427,96.13679 3.00427,96.13679z" opacity="NaN" stroke="#000" fill="#fff"/>""",
    "NSW": """<path id="new-south-wales" d="m489.88761,410.98626c0,0 11.61049,0 11.23598,-0.12484c0.3745,0.12484 6.74155,13.60798 6.74155,13.60798c0,0 2.99625,-3.37079 2.62175,-3.49562c0.3745,0.12484 7.86514,1.24843 7.86514,1.24843c0,0 0.37453,9.73783 0.37453,9.73783c0,0 10.11236,5.24345 10.11236,5.24345c0,0 7.49064,8.98876 7.49064,8.98876c0,0 6.74157,-2.62172 6.74157,-2.62172c0,0 7.86517,3.74532 7.86517,3.74532c0,0 24.34457,1.87266 24.34457,1.87266c0,0 6.36704,8.2397 6.36704,8.2397c0,0 -1.1236,7.86517 -1.1236,7.86517c0,0 23.97004,12.35955 23.97004,12.35955c0,0 9.73783,-29.21348 9.36333,-29.33832c0.3745,0.12484 5.61795,-6.61674 5.99248,-6.61674c0.37453,0 4.49438,-11.61049 4.49438,-11.61049c0,0 6.36704,-10.11236 6.36704,-10.11236c0,0 8.61423,-9.3633 8.61423,-9.3633c0,0 8.2397,-5.61798 8.2397,-5.61798c0,0 3.37079,-7.86517 2.99629,-7.99001c0.3745,0.12484 7.11607,-8.48939 7.11607,-8.48939c0,0 3.37079,-8.2397 3.37079,-8.2397c0,0 -0.37453,-6.74157 -0.37453,-6.74157c0,0 8.98876,-19.47565 8.98876,-19.47565c0,0 4.49438,-11.23595 4.11988,-11.36079c0.3745,0.12484 -0.37456,-10.36205 -0.74906,-10.48689c0.3745,0.12484 -19.47569,2.37203 -19.47569,2.37203c0,0 -2.99625,4.86891 -2.99625,4.86891c0,0 -10.11236,4.86891 -10.11236,4.86891c0,0 -6.74157,-7.49064 -6.74157,-7.49064c0,0 -6.74157,-0.74906 -7.11607,-0.8739c0.3745,0.12484 -7.49067,-2.12235 -7.49067,-2.12235c0,0 -4.11985,2.62172 -4.11985,2.62172c0,0 -7.86517,0.37453 -8.23967,0.24969c0.3745,0.12484 -3.74535,1.62297 -4.11985,1.49813c0.3745,0.12484 -107.8652,-12.60924 -107.8652,-12.60924c0,0 -4.86891,85.39326 -4.86891,85.39326z" opacity="NaN" stroke="#000" fill="#fff"/>""",
    "V": """<path id="victoria" d="m486.89136,481.02371c0,0 7.86517,4.49438 7.86517,4.49438c0,0 9.3633,0.37453 9.3633,0.37453c0,0 9.73783,6.36704 9.73783,6.36704c0,0 6.74157,3.37079 6.74157,3.37079c0,0 11.23595,-11.61049 11.23595,-11.61049c0,0 10.86142,9.3633 10.86142,9.3633c0,0 10.86142,9.73783 10.86142,9.73783c0,0 3.74532,-5.24345 3.74532,-5.24345c0,0 13.85768,-8.61423 13.85768,-8.61423c0,0 27.71535,-5.24345 27.71535,-5.24345c0,0 5.24345,-5.61798 5.24345,-5.61798c0,0 -23.5955,-12.35955 -23.5955,-12.35955c0,0 1.1236,-7.86517 1.1236,-7.86517c0,0 -5.99251,-8.61423 -6.36701,-8.73907c0.3745,0.12484 -23.59553,-0.99876 -23.97004,-1.1236c0.3745,0.12484 -7.49066,-4.36955 -7.49066,-4.36955c0,0 -6.74157,3.37079 -6.74157,3.37079c0,0 -8.2397,-9.3633 -8.6142,-9.48813c0.3745,0.12484 -9.36332,-5.86767 -9.73783,-5.99251c0.3745,0.12484 -0.00003,-9.61299 -0.00003,-9.61299c0,0 -7.1161,-1.1236 -7.1161,-1.1236c0,0 -2.99625,2.62172 -2.99625,2.62172c0,0 -6.74157,-12.73408 -6.74157,-12.73408c0,0 -11.61049,0.37453 -11.61049,0.37453c0,0 -3.37079,69.66292 -3.37079,69.66292z" opacity="NaN" stroke="#000" fill="#fff"/>""",
    "T": """<path id="tasmania" d="m529.21346,525.71786c0,0 22.84644,9.73783 22.84644,9.73783c0,0 19.47565,-5.24345 19.47565,-5.24345c0,0 5.24345,13.10861 5.24345,13.10861c0,0 -4.11985,9.73783 -4.11985,9.73783c0,0 -4.86891,6.36704 -4.86891,6.36704c0,0 0.37453,8.61423 0.37453,8.61423c0,0 -4.86891,7.1161 -4.86891,7.1161c0,0 -5.24345,-5.61798 -5.61795,-5.86767c0.3745,0.24969 -1.12362,8.11486 -1.12362,8.11486c0,0 -8.2397,1.87266 -8.6142,1.62297c0.3745,0.24969 -10.11239,-0.12484 -10.11239,-0.12484c0,0 -4.49438,-11.98502 -4.49438,-11.98502c0,0 0,-11.98502 -0.3745,-12.23471c0.3745,0.24969 1.87263,-5.36828 1.87263,-5.36828c0,0 -5.99251,-8.61423 -5.99251,-8.61423c0,0 0.37453,-14.98127 0.37453,-14.98127z" opacity="NaN" stroke="#000" fill="#fff"/>""",
}

BG = """<rect id="bg" width="800" height="600" fill="#444444" />"""
CAPTIONS = """<g><text xml:space="preserve" text-anchor="start" font-family="Noto Sans JP" font-size="24" stroke-width="0" id="svg_14" y="283.98267" x="130.08656" stroke="#000" fill="#000000">Western Australia</text><text xml:space="preserve" text-anchor="start" font-family="Noto Sans JP" font-size="24" stroke-width="0" id="svg_15" y="153.4632" x="336.58007" stroke="#000" fill="#000000">Northern</text><text xml:space="preserve" text-anchor="start" font-family="Noto Sans JP" font-size="24" stroke-width="0" id="svg_16" y="179.43722" x="338.52812" stroke="#000" fill="#000000">Territory</text><text xml:space="preserve" text-anchor="start" font-family="Noto Sans JP" font-size="24" stroke-width="0" id="svg_17" y="232.03462" x="487.22941" stroke="#000" fill="#000000">Queensland</text><text xml:space="preserve" text-anchor="start" font-family="Noto Sans JP" font-size="24" stroke-width="0" id="svg_18" y="299.56709" x="339.17747" stroke="#000" fill="#000000">South</text><text xml:space="preserve" text-anchor="start" font-family="Noto Sans JP" font-size="24" stroke-width="0" id="svg_19" y="324.24241" x="339.17747" stroke="#000" fill="#000000">Australia</text><text xml:space="preserve" text-anchor="start" font-family="Noto Sans JP" font-size="24" stroke-width="0" id="svg_20" y="361.90475" x="502.16448" stroke="#000" fill="#000000">New South</text><text xml:space="preserve" text-anchor="start" font-family="Noto Sans JP" font-size="24" stroke-width="0" id="svg_21" y="387.87877" x="502.81383" stroke="#000" fill="#000000">Wales</text><text xml:space="preserve" text-anchor="start" font-family="Noto Sans JP" font-size="24" stroke-width="0" id="svg_22" y="470.99565" x="494.37227" stroke="#000" fill="#000000">Victoria</text><text xml:space="preserve" text-anchor="start" font-family="Noto Sans JP" font-size="24" stroke-width="0" id="svg_23" y="557.35929" x="537.87876" stroke="#000" fill="#000000">Tasmania</text></g>"""


class Australia(SvgProducer):
    def __init__(self, ipy_off: bool = False, html_width: str = "25%",
                 state: list = None, square_size: int = 20, highlight: str = "#99ff33",
                 Solution: dict = None):
        super().__init__(800, 600, ipy_off, html_width)
        svg = self.raw_svg
        svg.append(ET.fromstring(BG))
        for key in ZONES.keys():
            if Solution:
                if key in Solution:
                    svg.append(ET.fromstring(ZONES[key].replace("#fff", Solution[key])))
                    continue
            svg.append(ET.fromstring(ZONES[key]))
        svg.append(ET.fromstring(CAPTIONS))