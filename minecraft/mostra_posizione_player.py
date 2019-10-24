#!/usr/bin/env python3

from mcpi.minecraft import Minecraft

mc = Minecraft.create ()

def main ():
    pos = mc.player.getTilePos ()
    print ( "Il player si trova in: x = %s, y = %s, z = %s" % ( pos.x, pos.y, pos.z ) )


if __name__ == '__main__':
    main ()
