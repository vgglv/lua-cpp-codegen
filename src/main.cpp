#include <iostream>
#include "GameObject.hpp"
#include "Vector2.hpp"
#include "lua.hpp"

#define SOL_ALL_SAFETIES_ON 1
#include "sol/sol.hpp"

int main() {
    sol::state lua;
    lua.open_libraries(sol::lib::base, sol::lib::io, sol::lib::table, sol::lib::math);

    auto result = lua.safe_script_file("scripts/jumping_buddy.lua");
    if (!result.valid()) {
        sol::error err = result;
        printf("Error loading script: %s\n", err.what());
        return 1;
    }
    game::GameObject player;
    player.setXY(game::Vector2{5.f, 5.f});
    sol::table myData = result;
    while(true) {
        auto result = myData["update"](&player, 0.16666f);
        if (!result.valid()) {
            sol::error err = result;
            printf("Error script: %s\n", err.what());
            break;
        }
    }

    return 0;
}
