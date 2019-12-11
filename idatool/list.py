import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import re

class Parser:
    def __init__(self, filename):
        self.Filename = filename
        self.Entries = []
        
    def parse(self):
        fd = open(self.Filename, 'r')
        
        name = ''
        addr = ''
        while 1:
            line = fd.readline()
            if not line:
                break

            toks = line.split()
            if len(toks)>2:
                if toks[2] == 'proc':
                    name = toks[1]
                    addr = toks[0].split(':')[1]

                    parsed_lines = []
                elif name and len(toks)>2 and toks[2] == 'endp':
                    self.Entries.append({
                        'Name': name, 
                        'Address': addr, 
                        'Lines': parsed_lines
                    })
                    name = ''
                    addr = ''
                elif name and line:
                    parsed_lines.append(self.parse_line(line))

        fd.close()

    def skip_spaces(self, line):
        m = re.search('^[ \t]+', line)        
        if m:
            line = line[m.end():]
        return line

    def parse_line(self, line):
        parsed_line = {'Line':line}
        # Address
        m = re.search('^[^ \t]+[ \t]+', line)
        
        if m.end() == 0:
            return

        parsed_line['Address'] = line[0:m.end()]
        line = line[m.end():]

        # Hex bytes
        insn_bytes = ''
        while 1:
            m = re.search('^([0-9a-fA-F][0-9a-fA-F] )', line)
            
            if not m:
                break

            insn_bytes += chr(int(line[:m.end()], 0x10))
            line = line[m.end():]

        parsed_line['Bytes'] = insn_bytes
        line = self.skip_spaces(line)
            
        m = re.search('^[^ \t]+', line)
        if m:
            op = line[:m.end()]
            if op.endswith(':') or op.endswith(';'):
                return

            parsed_line['Op'] = op
            line = line[m.end():]

        line = self.skip_spaces(line)
        operands = []
        for operand in re.split(', [ \t]+', line):
            operand = operand.strip()
            operands.append(operand)
        parsed_line['Operands'] = operands
        
        return parsed_line
        
    def get_names(self):
        names = []
        for entry in self.Entries:
            if 'Name' in entry:
                names.append(entry['Name'])
        return names
    
    def get_bytes(self, name):
        bytes = ''
        for entry in self.Entries:
            if 'Name' in entry and entry['Name'] == name:                
                for parsed_line in entry['Lines']:
                    print(parsed_line)
                    if parsed_line == None:
                        continue
                    bytes += parsed_line['Bytes']
        return bytes

if __name__ == '__main__':
    from optparse import OptionParser, Option

    parser = OptionParser(usage = "usage: %prog [options] args")    
    parser.add_option("-O", "--output_filename", dest = "output_filename", type = "string", default = "", metavar = "OUTPUT_FOLDER", help = "Set output folder")
    
    (options, args) = parser.parse_args(sys.argv)
    
    filename = args[1]
    
    parser = Parser(filename)
    parser.parse()
