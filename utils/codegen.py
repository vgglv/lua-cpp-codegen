import os
import clang.cindex
from clang.cindex import CursorKind

clang.cindex.Config.set_library_file("/opt/homebrew/Cellar/llvm/20.1.4_1/lib/libclang.dylib")

INCLUDE_DIR = "src"
CPP_OUTPUT = "lua_bindings.cpp"
COMPILER_ARGS = ["-std=c++17", "-Isrc"]

def collect_header_files(directory):
    headers = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith((".h", ".hpp")):
                headers.append(os.path.join(root, file))
    return headers

def get_method_signature(m):
    name = m.spelling
    ret = m.result_type.spelling
    args = [a.type.spelling for a in m.get_arguments()]
    return name, ret, args

def generate_cpp_function(class_name, method):
    name, ret_type, args = get_method_signature(method)
    func_name = f"{class_name}_{name}"

    arg_lines, arg_names = [], []
    for i, atype in enumerate(args):
        lua_idx = i + 2
        if "string" in atype:
            arg_lines.append(f'    const char* arg{i} = luaL_checkstring(L, {lua_idx});')
            arg_names.append(f'std::string(arg{i})')
        elif "float" in atype or "double" in atype:
            arg_lines.append(f'    float arg{i} = luaL_checknumber(L, {lua_idx});')
            arg_names.append(f'arg{i}')
        else:
            arg_lines.append(f'    // TODO: Unsupported arg type: {atype}')
            arg_names.append(f'/*arg{i}*/')

    call = f'self->{name}({", ".join(arg_names)})'

    if "string" in ret_type:
        ret_line = f"    auto result = {call};\n    lua_pushstring(L, result.c_str());\n    return 1;"
    elif "float" in ret_type or "double" in ret_type:
        ret_line = f"    auto result = {call};\n    lua_pushnumber(L, result);\n    return 1;"
    elif "void" in ret_type:
        ret_line = f"    {call};\n    return 0;"
    else:
        ret_line = f"    // TODO: Unsupported return type: {ret_type}\n    return 0;"

    return f"""
int {func_name}(lua_State* L) {{
    auto* self = static_cast<{class_name}*>(luaL_checkudata(L, 1, "{class_name}"));
{chr(10).join(arg_lines)}
{ret_line}
}}"""

def generate_metatable(class_name, method_names):
    entries = "\n".join([
        f'    lua_pushcfunction(L, {class_name}_{m});\n    lua_setfield(L, -2, "{m}");'
        for m in method_names
    ])
    return f"""
void register_{class_name}(lua_State* L) {{
    luaL_newmetatable(L, "{class_name}");
    lua_pushvalue(L, -1);
    lua_setfield(L, -2, "__index");
{entries}
    lua_pop(L, 1);
}}"""

def find_classes(tu, bindings):
    def recurse(node):
        if node.kind == CursorKind.CLASS_DECL and node.is_definition():
            cname = node.spelling
            method_nodes = [c for c in node.get_children() if c.kind == CursorKind.CXX_METHOD]
            if method_nodes:
                bindings[cname] = method_nodes
        for child in node.get_children():
            recurse(child)
    recurse(tu.cursor)

def main():
    index = clang.cindex.Index.create()
    headers = collect_header_files(INCLUDE_DIR)

    bindings = {}
    for header in headers:
        tu = index.parse(header, args=COMPILER_ARGS)
        find_classes(tu, bindings)

    all_output = ["#include <lua.hpp>"]
    all_classes = []

    for class_name, methods in bindings.items():
        all_output.append(f'#include "{class_name}.h"')  # crude but replaceable
        method_names = []
        for method in methods:
            all_output.append(generate_cpp_function(class_name, method))
            method_names.append(method.spelling)
        all_output.append(generate_metatable(class_name, method_names))
        all_classes.append(f"    register_{class_name}(L);")

    all_output.append("\nvoid register_all_bindings(lua_State* L) {\n" + "\n".join(all_classes) + "\n}")

    with open(CPP_OUTPUT, "w") as f:
        f.write("\n".join(all_output))

if __name__ == "__main__":
    main()