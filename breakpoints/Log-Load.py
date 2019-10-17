import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import json
import pprint
import logging
import windbgtool.command
import windbgtool.log

logging.basicConfig(level = logging.DEBUG)
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    import Input
    filename = Input.GetResponse()
    
    disasm = idatool.disassembly.Disasm()
    name_and_comments = {}
    windbg_command_parser = windbgtool.log.Parser(filename)
    for log_output in windbg_command_parser.LogOutputLines:
        if not log_output.has_key('Address'):
            continue

        address = log_output['Address']
        
        comment = ''
        if log_output.has_key('Target Module'):
            comment += log_output['Target Module']
        if log_output.has_key('Target Function'):
            comment += '!' + log_output['Target Function']

        if comment == '':
            for disasm_line in log_output['DisasmLines']:
                comment += disasm_line['Line']+'\r\n'

        name_and_comments[hex(address)] = {
                            'Address': address, 
                            'Comment': comment
                        }

    print '* Loading names and comments:'
    pprint.pprint(name_and_comments)
    disasm.SaveNameAndComments(name_and_comments)
