#include <lua.hpp>
#include "GameObject.h"

int GameObject_setXY(lua_State* L) {
    auto* self = static_cast<GameObject*>(luaL_checkudata(L, 1, "GameObject"));
    // TODO: Unsupported arg type: const Vector2 &
    self->setXY(/*arg0*/);
    return 0;
}

int GameObject_getXY(lua_State* L) {
    auto* self = static_cast<GameObject*>(luaL_checkudata(L, 1, "GameObject"));

    // TODO: Unsupported return type: Vector2
    return 0;
}

void register_GameObject(lua_State* L) {
    luaL_newmetatable(L, "GameObject");
    lua_pushvalue(L, -1);
    lua_setfield(L, -2, "__index");
    lua_pushcfunction(L, GameObject_setXY);
    lua_setfield(L, -2, "setXY");
    lua_pushcfunction(L, GameObject_getXY);
    lua_setfield(L, -2, "getXY");
    lua_pop(L, 1);
}

void register_all_bindings(lua_State* L) {
    register_GameObject(L);
}