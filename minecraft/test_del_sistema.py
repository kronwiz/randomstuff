from mcpi.minecraft import Minecraft
from mcpi import block

mc = Minecraft.create()

pos = mc.player.getTilePos ()

mc.setBlock ( pos.x + 1, pos.y + 1, pos.z + 1, block.WOOD )
