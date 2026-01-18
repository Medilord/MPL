import re
from typing import List

class PascalAdvancedTranspiler:
    def __init__(self, code: str):
        self.lines = [l.strip() for l in code.split('\n') if l.strip()]
        self.python_lines: List[str] = []
        self.indent_level = 0
        self.dedent_queue = 0 

    def _get_indent(self) -> str:
        return "    " * self.indent_level

    def _clean_params(self, params_str: str) -> str:
        if not params_str: return ""
        parts = params_str.split(';')
        clean_args = []
        for part in parts:
            if ':' in part: clean_args.append(part.split(':')[0].strip())
            else: clean_args.append(part.strip())
        return ", ".join(clean_args)

    def _peek_next_line_is_begin(self, current_index: int) -> bool:
        if current_index + 1 < len(self.lines):
            return self.lines[current_index + 1].lower() == 'begin'
        return False

    def _parse_procedure(self, line: str) -> bool:
        match = re.match(r'^(procedure|function)\s+(\w+)\s*(\((.*)\))?.*$', line, re.IGNORECASE)
        if match:
            _, name, _, params = match.groups()
            clean_params = self._clean_params(params if params else "")
            self.python_lines.append(f"{self._get_indent()}def {name}({clean_params}):")
            return True
        return False

    def _parse_function_call(self, line: str) -> bool:
        if line.lower().startswith('writeln'):
            return False
            
        match = re.match(r'^(\w+)\s*\((.*)\);$', line)
        if match:
            func_name = match.group(1)
            args = match.group(2)
            self.python_lines.append(f"{self._get_indent()}{func_name}({args})")
            return True
        return False

    def _parse_while(self, line: str, idx: int) -> bool:
        match = re.match(r'^while\s+(.+)\s+do$', line, re.IGNORECASE)
        if match:
            condition = match.group(1)
            self.python_lines.append(f"{self._get_indent()}while {condition}:")
            
            if not self._peek_next_line_is_begin(idx):
                self.indent_level += 1
                self.dedent_queue += 1
            return True
        return False

    def _handle_blocks(self, line: str) -> bool:
        lower = line.lower()
        if lower == 'begin':
            self.indent_level += 1
            return True
        if lower.startswith('end'):
            if self.indent_level > 0: self.indent_level -= 1
            return True
        return False

    def _parse_assignment(self, line: str) -> bool:
        match = re.match(r'^(\w+)\s*:=\s*(.*);$', line)
        if match:
            self.python_lines.append(f"{self._get_indent()}{match.group(1)} = {match.group(2)}")
            return True
        return False

    def _parse_writeln(self, line: str) -> bool:
        match = re.match(r'^writeln\((.*)\);$', line, re.IGNORECASE)
        if match:
            self.python_lines.append(f"{self._get_indent()}print({match.group(1)})")
            return True
        return False

    def translate(self) -> str:
        
        i = 0
        while i < len(self.lines):
            line = self.lines[i]
            
            if self._handle_blocks(line): pass
            elif self._parse_procedure(line): pass 
            elif self._parse_while(line, i): pass 
            elif self._parse_writeln(line): pass
            elif self._parse_assignment(line): pass
            elif self._parse_function_call(line): pass
            else: self.python_lines.append(f"{self._get_indent()}# Skipped: {line}")

            if self.dedent_queue > 0:
                is_structural = re.match(r'^(while|procedure|function|begin)', line, re.IGNORECASE)
                if not is_structural:
                    self.indent_level -= 1
                    self.dedent_queue -= 1
            i += 1
            
        return "\n".join(self.python_lines)


pascal_source = """
procedure Process(startVal: Integer; limit: Integer);
begin
    current := startVal;
    step := 0;
    accumulator := 0;
    
    writeln('Start value:');
    writeln(current);

    while step < 5 do
    begin
        writeln('step:');
        writeln(step);
        current := current + 10;
        step := step + 1;
    end;
    
    writeln("Loop without begin-end");
    i := 0;
    while i < 3 do
        i := i + 1;     

    writeln("i:");
    writeln(i);

    outer := 0;
    while outer < 3 do
    begin
        writeln('Outer Loop Index:');
        writeln(outer);
        
        inner := 0;
        while inner < 2 do
        begin
            accumulator := accumulator + 1;
            writeln('  Inner Accumulation...');
            inner := inner + 1;
        end;
        
        outer := outer + 1;
    end;

    mathStep := 10;
    while mathStep > 0 do
    begin
        accumulator := accumulator + mathStep;
        current := current - 1;
        mathStep := mathStep - 1;
    end;
    
    writeln('Accumulator:');
    writeln(accumulator);
    writeln('Current Value:');
    writeln(current);    
end;

val := 100;
max := 50;

Process(val, max);

writeln('Program Finished Successfully.');
"""

print("_____Pascal code_____\n")
print(pascal_source)


transpiler = PascalAdvancedTranspiler(pascal_source)
python_code = transpiler.translate()
print("\n\n_____Python code_____\n")
print(python_code)

print("\n\n_____Execute program_____")
print("-" * 30)
exec(python_code)
print("-" * 30)