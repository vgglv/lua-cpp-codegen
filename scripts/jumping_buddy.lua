local gameObject = {}

function gameObject.update(self, dt)
    local xy = self:getXY()
    print("X: " .. xy.x .. " Y: " .. xy.y)
    xy.x = xy.x + 1.0
    xy.y = xy.y + 1.0
    self:setXY(xy)
end

return gameObject