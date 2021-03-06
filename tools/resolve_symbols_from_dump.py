import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import struct

import idatool.disassembly
import idatool.util
import windbgtool.debugger

class Util:
    def __init__(self, dump_filename = r''):
        self.Disasm = idatool.disassembly.Disasm()
        self.debugger = windbgtool.debugger.DbgEngine()
        self.debugger.load_dump(dump_filename)
        self.debugger.set_symbol_path()

    def find_address_bytes(self, type = ""):
        for addr in self.Disasm.get_addresses(4):
            bytes = self.Disasm.dump_bytes(addr, 4)
            if bytes != None and len(bytes) == 4:
                (dword, ) = struct.unpack("<L", bytes)
                if dword>0:
                    symbol = self.debugger.find_symbol(dword)
                    if symbol and symbol.find('+')<0:
                        self.Disasm.redefine(addr, 4, 'data', data_type = 'DWORD')
                        idatool.util.Cmt.set(addr, symbol, 1)
                        name = symbol.split('!')[1]
                        self.Disasm.set_name(addr, name)
                        print('%.8x %.8x %s' % (addr, dword, symbol))
            
if __name__ == '__main__':
    import logging
    import idatool.ui

    logging.basicConfig(level = logging.DEBUG)
    logger = logging.getLogger(__name__)    
   
    title = 'ResolveSymbol'
    try:
        form.on_close(form)
        form = idatool.ui.Form(title)
    except:
        form = idatool.ui.Form(title)

    form.show()

    dump_filename = form.ask_open_filename("DMP (*.dmp)")

    if dump_filename:
        util = Util(dump_filename = dump_filename)
        util.find_address_bytes()
