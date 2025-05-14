#include <iostream>
#include "GameObject.hpp"
#include "Vector2.hpp"
#include "lua.hpp"

int getVariable(lua_State* L, std::string_view variableName) {
    lua_getglobal(L, variableName.data());
    auto x = lua_tonumber(L, -1);
    return static_cast<int>(x);
}

int main() {
    lua_State* L = luaL_newstate();
    luaL_dostring(L, "x = 42");
    {
        int x = getVariable(L, "x");
        std::printf("x = %d\n", x);
    }
    luaL_dostring(L, "x = x + 8");
    {
        int x = getVariable(L, "x");
        std::printf("x = %d\n", x);
    }

    lua_close(L);
    return 0;
}
