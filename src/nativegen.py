#!/usr/bin/python

# This script generates code for SA-MP natives from their C declarations
# sampgdk headers like a_players.h, etc.

import os
import re
import sys

def parse_argument_list(arg_list):
	""" For each entry of the arg_list returns a tuple made of
	    argument type and name. """
	for string in arg_list:
		if len(string) == 0:
			continue
		match = re.match(r"([\w ]+ |[\w ]+\*)(\w+)$", string)
		type = match.group(1).strip()
		name = match.group(2).strip()
		yield (type, name)

def generate_native_code(type, name, arg_list):
	""" Generates C++ code for a native function. """

	# Write first line, same as function declaration + "{\n".
	code = "SAMPGDK_EXPORT " + type + " SAMPGDK_CALL " + name\
		+ "(" + ", ".join(arg_list) + ") {\n" 

	# A "static" variable that holds native address.
	code += "\tstatic AMX_NATIVE native = Natives::GetInstance().GetNativeWarn(\"" + name + "\");\n"

	# Generate code for local variables, params array and ref argument assignment.
	locals_code = ""
	params_code = "\tcell params[] = {\n\t\t0,\n"
	assign_code = ""
	expect_buffer_size = False
	for arg in parse_argument_list(arg_list):
		arg_type = arg[0]
		arg_name = arg[1]
		# Local FakeAmxHeapObject instances.
		if expect_buffer_size:
			locals_code += arg_name + ");\n"
			expect_buffer_size = False
		if arg_type == "char *":
			# Output string buffer whose size is passed via next argument.
			locals_code += "\tFakeAmxHeapObject " + arg_name + "_("
			expect_buffer_size = True
		elif arg_type == "const char *":
			# Constant string.
			locals_code += "\tFakeAmxHeapObject " + arg_name + "_(" + arg_name + ");\n"
		elif arg_type.endswith("*"):
			# Other output parameters.
			locals_code += "\tFakeAmxHeapObject " + arg_name + "_;\n"
		# The "params" array.
		if arg_type == "int" or arg_type == "bool":
			params_code += "\t\t" + arg_name
		elif arg_type == "float":
			params_code += "\t\tamx_ftoc(" + arg_name + ")"
		elif arg_type.endswith("*"):
			params_code += "\t\t" + arg_name + "_.address()"
		else:
			return None
		# Assignment of pointer arguments.
		if arg_type == "int *" or arg_type == "float *" or arg_type == "bool *":
			assign_code += "\t*" + arg_name + " = " + arg_name + "_."
			if arg_type == "int *":
				assign_code += "Get();\n"
			elif arg_type == "bool *":
				assign_code += "GetAsBool();\n"
			elif arg_type == "float *":
				assign_code += "GetAsFloat();\n"
		params_code += ",\n"
	params_code += "\t};\n"

	code += locals_code + params_code + assign_code

	if type == "bool":
		code += "\treturn FakeAmx::CallNativeBool(native, params);\n"
	elif type == "float":
		code += "\treturn FakeAmx::CallNativeFloat(native, params);\n"
	else:
		code += "\treturn FakeAmx::CallNative(native, params);\n"
	code += "}\n"

	return code

def process_native_decl(string):
	""" Returns a tuple of (type, name, arg_list) where arg_list is a
	    list of arguments and each argument is a string that consists
	    of an argument type and name (no default values can occur). """
	match = re.match(r"SAMPGDK_EXPORT (int|bool|float) SAMPGDK_CALL (\w+)\((.*)\);", string)
	if match == None:
		return None
	type = match.group(1)
	name = match.group(2)
	args = match.group(3).split(", ")
	return (type, name, args)	

def process_file(src, dest):
	""" Processes a C/C++ header file "src" finding native function
	    declarations and outputs generated code to "dest". """
	outfile = open(dest, "w")
	for line in file(src):
		native = process_native_decl(line)
		if native == None:
			continue
		code = generate_native_code(*native)
		if code == None:
			continue
		outfile.write(code + "\n")

if __name__ == '__main__':
	if len(sys.argv) <= 2:
		print "Usage: ", os.path.basename(sys.argv[0]), " <src> <dest>"
	else:
		process_file(sys.argv[1], sys.argv[2])
